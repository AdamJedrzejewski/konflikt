import json
import os
from abc import ABC, abstractmethod
from pathlib import Path

import jsonschema

PROMPTS_DIR = Path(__file__).parent / "prompts"


class _StructureError(Exception):
    """Raised when LLM output is missing required top-level structure."""
    pass


def _validate_structure(parsed: dict, schema: dict) -> None:
    """Validate only that required top-level keys exist and are correct types.
    Does NOT check enum values — allows free text in fields."""
    if not isinstance(parsed, dict):
        raise _StructureError("Output is not a JSON object")
    required = schema.get("required", [])
    for key in required:
        if key not in parsed:
            raise _StructureError(f"Missing required field: {key}")
    # Check that arrays are actually arrays
    props = schema.get("properties", {})
    for key, prop_schema in props.items():
        if key in parsed and prop_schema.get("type") == "array":
            if not isinstance(parsed[key], list):
                raise _StructureError(f"Field '{key}' should be array, got {type(parsed[key]).__name__}")


def _load_prompt(filename: str) -> str:
    return (PROMPTS_DIR / filename).read_text(encoding="utf-8")


def _load_json(filename: str) -> dict:
    return json.loads((PROMPTS_DIR / filename).read_text(encoding="utf-8"))


def _normalize_llm_output(parsed: dict) -> dict:
    """Fix common LLM formatting mistakes before schema validation."""
    # Fix Polish inflection: krytyczne → krytyczny, wysokie → wysokie stays (valid in some enums)
    _INFLECTION_FIXES = {
        "krytyczne": "krytyczny",
        "wysokie": "wysokie",  # keep as-is, only fix risk_level
        "niskie": "niskie",
    }
    if "risk_level" in parsed:
        parsed["risk_level"] = _INFLECTION_FIXES.get(parsed["risk_level"], parsed["risk_level"])

    # Fix roles: LLM sometimes uses entity name as key instead of entity_id
    if "roles" in parsed and isinstance(parsed["roles"], list):
        for role in parsed["roles"]:
            if isinstance(role, dict) and "entity_id" not in role:
                # Find the first key that looks like an entity reference
                for key in list(role.keys()):
                    if key != "role_type" and key.startswith("entity"):
                        role["entity_id"] = role.pop(key)
                        break

    return parsed


class LLMAdapter(ABC):
    """Provider-agnostic interface for LLM operations."""

    @abstractmethod
    async def extract(self, user_input: str) -> dict:
        """Extract structured data from free-text case description."""
        ...

    @abstractmethod
    async def evaluate_schematic(self, structured_input: dict) -> dict:
        """Evaluate conflict using rule-based schematic analysis."""
        ...

    @abstractmethod
    async def evaluate_independent(self, structured_input: dict) -> dict:
        """Evaluate conflict using independent LLM analysis."""
        ...

    @abstractmethod
    async def evaluate_article(self, article: dict, extraction: dict) -> dict:
        """Evaluate whether a single KERP article applies to the extracted facts."""
        ...

    @abstractmethod
    async def analyze_simple(self, fact_pattern: str, articles_catalog: list[dict]) -> dict:
        """Single-shot LLM analysis: cala ocena konfliktu interesow w jednym wywolaniu."""
        ...

    def load_articles_catalog(self) -> list[dict]:
        """Return list of KERP articles in evaluation order."""
        catalog = _load_json("articles_catalog.json")
        return catalog.get("articles", [])

    @staticmethod
    def _build_simple_payload(fact_pattern: str, articles_catalog: list[dict]) -> str:
        """Buduje user payload: pelny katalog KERP + casus."""
        articles_block = "\n\n".join(
            f"## {a.get('article')} ({a.get('id')})\n"
            f"Konfiguracja: {a.get('configuration_pl')}\n"
            f"Waivable: {a.get('waivable')}\n"
            f"Logika przeslanek: {a.get('premises_logic')}\n"
            f"Tekst: {a.get('text')}\n"
            f"Przeslanki:\n" + "\n".join(f"- {p}" for p in a.get("premises", []))
            for a in articles_catalog
        )
        return (
            "# KATALOG ARTYKULOW KERP\n\n"
            f"{articles_block}\n\n"
            "# STAN FAKTYCZNY (kazus radcy prawnego)\n\n"
            f"{fact_pattern}\n\n"
            "Przeprowadz pelna analize zgodnie z instrukcja systemowa i zwroc JSON."
        )


class AnthropicAdapter(LLMAdapter):
    """Adapter for Anthropic Claude API (dev/beta)."""

    def __init__(self) -> None:
        import anthropic
        from app.core.config import settings

        api_key = settings.llm_api_key
        if not api_key:
            raise ValueError("LLM_API_KEY environment variable is required")

        self._client = anthropic.AsyncAnthropic(api_key=api_key)
        self._model = settings.llm_model_name
        self._extraction_system = _load_prompt("extraction_system.txt")
        self._extraction_schema = _load_json("extraction_schema.json")
        self._schematic_system = _load_prompt("schematic_system.txt")
        self._schematic_schema = _load_json("schematic_schema.json")
        self._independent_system = _load_prompt("independent_system.txt")
        self._independent_schema = _load_json("independent_schema.json")
        self._article_check_system = _load_prompt("article_check_system.txt")
        self._article_check_schema = _load_json("article_check_schema.json")
        self._simple_analysis_system = _load_prompt("simple_analysis_system.txt")
        self._simple_analysis_schema = _load_json("simple_analysis_schema.json")

    async def _call(self, system_prompt: str, user_content: str, schema: dict, strict: bool = True) -> dict:
        """Call Claude with retry on JSON validation errors."""
        last_error = None

        for attempt in range(3):
            try:
                response = await self._client.messages.create(
                    model=self._model,
                    max_tokens=4096,
                    system=system_prompt,
                    messages=[{"role": "user", "content": user_content}],
                )

                raw_text = response.content[0].text
                # Strip markdown code fences if present
                if raw_text.strip().startswith("```"):
                    raw_text = raw_text.strip().split("\n", 1)[1].rsplit("```", 1)[0].strip()
                parsed = json.loads(raw_text)
                parsed = _normalize_llm_output(parsed)
                if strict:
                    jsonschema.validate(parsed, schema)
                else:
                    _validate_structure(parsed, schema)
                return parsed

            except (json.JSONDecodeError, jsonschema.ValidationError, _StructureError) as e:
                last_error = e
                if attempt < 2:
                    continue
            except Exception:
                raise

        raise ValueError(
            f"LLM output failed validation after 3 attempts: {last_error}"
        )

    async def extract(self, user_input: str) -> dict:
        return await self._call(self._extraction_system, user_input, self._extraction_schema, strict=False)

    async def evaluate_schematic(self, structured_input: dict) -> dict:
        return await self._call(
            self._schematic_system,
            json.dumps(structured_input, ensure_ascii=False, indent=2),
            self._schematic_schema,
        )

    async def evaluate_independent(self, structured_input: dict) -> dict:
        return await self._call(
            self._independent_system,
            json.dumps(structured_input, ensure_ascii=False, indent=2),
            self._independent_schema,
        )

    async def evaluate_article(self, article: dict, extraction: dict) -> dict:
        user_payload = {
            "article_id": article.get("id"),
            "article": article.get("article"),
            "configuration": article.get("configuration_pl"),
            "waivable": article.get("waivable"),
            "result_if_applies": article.get("result_if_applies"),
            "premises_logic": article.get("premises_logic", "AND_ALL"),
            "article_text": article.get("text"),
            "premises": article.get("premises", []),
            "extraction": extraction,
        }
        return await self._call(
            self._article_check_system,
            json.dumps(user_payload, ensure_ascii=False, indent=2),
            self._article_check_schema,
            strict=False,
        )

    async def analyze_simple(self, fact_pattern: str, articles_catalog: list[dict]) -> dict:
        user_payload = self._build_simple_payload(fact_pattern, articles_catalog)
        return await self._call(
            self._simple_analysis_system,
            user_payload,
            self._simple_analysis_schema,
            strict=False,
        )


class GoogleAIAdapter(LLMAdapter):
    """Adapter dla Google AI (Gemini). Dev/beta — model gemini-2.0-flash."""

    def __init__(self) -> None:
        from google import genai
        from google.genai import types as genai_types
        from app.core.config import settings

        api_key = settings.llm_api_key
        if not api_key:
            raise ValueError("LLM_API_KEY environment variable is required")

        self._client = genai.Client(api_key=api_key)
        self._model_name = settings.llm_model_name
        self._genai_types = genai_types
        self._extraction_system = _load_prompt("extraction_system.txt")
        self._extraction_schema = _load_json("extraction_schema.json")
        self._schematic_system = _load_prompt("schematic_system.txt")
        self._schematic_schema = _load_json("schematic_schema.json")
        self._independent_system = _load_prompt("independent_system.txt")
        self._independent_schema = _load_json("independent_schema.json")
        self._article_check_system = _load_prompt("article_check_system.txt")
        self._article_check_schema = _load_json("article_check_schema.json")
        self._simple_analysis_system = _load_prompt("simple_analysis_system.txt")
        self._simple_analysis_schema = _load_json("simple_analysis_schema.json")

    async def _call(self, system_prompt: str, user_content: str, schema: dict, strict: bool = True) -> dict:
        """Wywołuje Gemini z retry przy błędach parsowania JSON."""
        import asyncio
        full_prompt = f"{system_prompt}\n\n---\n\n{user_content}"
        config = self._genai_types.GenerateContentConfig(
            temperature=0.1,
            response_mime_type="application/json",
        )
        last_error = None
        for attempt in range(3):
            try:
                response = await asyncio.to_thread(
                    self._client.models.generate_content,
                    model=self._model_name,
                    contents=full_prompt,
                    config=config,
                )
                raw = response.text.strip()
                if raw.startswith("```"):
                    raw = raw.split("\n", 1)[1].rsplit("```", 1)[0].strip()
                parsed = json.loads(raw)
                parsed = _normalize_llm_output(parsed)
                if strict:
                    jsonschema.validate(parsed, schema)
                else:
                    # Soft validation: check structure only (required top-level keys)
                    _validate_structure(parsed, schema)
                return parsed
            except json.JSONDecodeError as e:
                last_error = e
                if attempt < 2:
                    continue
            except jsonschema.ValidationError as e:
                last_error = e
                if attempt < 2:
                    continue
            except _StructureError as e:
                last_error = e
                if attempt < 2:
                    continue
            except Exception:
                raise
        raise ValueError(f"Google AI output failed validation after 3 attempts: {last_error}")

    async def extract(self, user_input: str) -> dict:
        return await self._call(self._extraction_system, user_input, self._extraction_schema, strict=False)

    async def evaluate_schematic(self, structured_input: dict) -> dict:
        return await self._call(
            self._schematic_system,
            json.dumps(structured_input, ensure_ascii=False, indent=2),
            self._schematic_schema,
        )

    async def evaluate_independent(self, structured_input: dict) -> dict:
        return await self._call(
            self._independent_system,
            json.dumps(structured_input, ensure_ascii=False, indent=2),
            self._independent_schema,
        )

    async def evaluate_article(self, article: dict, extraction: dict) -> dict:
        user_payload = {
            "article_id": article.get("id"),
            "article": article.get("article"),
            "configuration": article.get("configuration_pl"),
            "waivable": article.get("waivable"),
            "result_if_applies": article.get("result_if_applies"),
            "premises_logic": article.get("premises_logic", "AND_ALL"),
            "article_text": article.get("text"),
            "premises": article.get("premises", []),
            "extraction": extraction,
        }
        return await self._call(
            self._article_check_system,
            json.dumps(user_payload, ensure_ascii=False, indent=2),
            self._article_check_schema,
            strict=False,
        )

    async def analyze_simple(self, fact_pattern: str, articles_catalog: list[dict]) -> dict:
        user_payload = self._build_simple_payload(fact_pattern, articles_catalog)
        return await self._call(
            self._simple_analysis_system,
            user_payload,
            self._simple_analysis_schema,
            strict=False,
        )


def create_adapter(provider: str | None = None) -> LLMAdapter:
    """Factory function for creating LLM adapters."""
    from app.core.config import settings

    provider = provider or settings.llm_provider
    if provider == "codex_chatgpt":
        from app.adapters.codex_adapter import CodexChatGPTAdapter
        return CodexChatGPTAdapter()
    if provider == "anthropic":
        return AnthropicAdapter()
    if provider == "google":
        return GoogleAIAdapter()
    raise ValueError(f"Nieznany provider: {provider}")
