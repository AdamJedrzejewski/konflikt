import asyncio
import json
import jsonschema

from app.adapters.codex_transport import CodexSession
from app.adapters.llm_adapter import LLMAdapter, _load_json, _load_prompt


class CodexChatGPTAdapter(LLMAdapter):
    """OBSIL local tests using the user's existing ChatGPT login in Codex."""
    def __init__(self):
        from app.core.config import settings
        self.model = settings.llm_model_name
        self.executable = settings.codex_executable
        self.timeout = settings.llm_timeout_seconds
        self.effort = settings.codex_reasoning_effort
        self.last_metadata = {}

    async def call_json(self, instruction, payload, schema):
        def run():
            with CodexSession(self.executable, self.timeout) as session:
                return session.complete(instruction, payload, schema, self.model, self.effort)
        parsed, self.last_metadata = await asyncio.to_thread(run)
        jsonschema.validate(parsed, schema)
        return parsed

    async def _operation(self, name, payload):
        if not isinstance(payload, str):
            payload = json.dumps(payload, ensure_ascii=False)
        return await self.call_json(_load_prompt(name + "_system.txt"), payload, _load_json(name + "_schema.json"))

    async def extract(self, user_input):
        return await self._operation("extraction", user_input)

    async def evaluate_schematic(self, structured_input):
        return await self._operation("schematic", structured_input)

    async def evaluate_independent(self, structured_input):
        return await self._operation("independent", structured_input)

    async def evaluate_article(self, article, extraction):
        return await self._operation("article_check", {"article": article, "extraction": extraction})

    async def analyze_simple(self, fact_pattern, articles_catalog):
        return await self._operation("simple_analysis", self._build_simple_payload(fact_pattern, articles_catalog))
