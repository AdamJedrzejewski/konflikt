import logging
import time
import uuid
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.llm_adapter import LLMAdapter
from app.models.db_models import Analysis, AnalysisStatus, AuditLog, Clarification
from app.rules.engine import EngineResult, RuleEngine

logger = logging.getLogger(__name__)


class AnalysisOrchestrator:
    def __init__(self, llm_adapter: LLMAdapter, rule_engine: RuleEngine, db_session: AsyncSession):
        self.llm = llm_adapter
        self.rules = rule_engine
        self.db = db_session
        self.articles = llm_adapter.load_articles_catalog()

    async def run_analysis(self, analysis_id: UUID, fact_pattern: str) -> dict:
        """Jedno wywołanie z wybraną bazą, zapis wyniku lub jawnego błędu."""
        start_time = time.time()

        analysis = await self._get_analysis(analysis_id)
        user_id = analysis.user_id

        try:
            await self._update_status(analysis, AnalysisStatus.analyzing)
            await self._write_audit(analysis_id, user_id, "analysis_started", {
                "mode": "single_shot_llm",
                "fact_pattern_length": len(fact_pattern),
            })

            logger.info("Starting single-shot LLM analysis for %s", analysis_id)
            from app.core.config import settings
            if settings.knowledge_mode == "experimental":
                from app.services.knowledge_analysis import analyze_with_knowledge
                llm_result = await analyze_with_knowledge(self.llm, fact_pattern, settings.knowledge_project_path)
            elif settings.knowledge_mode == "off":
                llm_result = await self.llm.analyze_simple(fact_pattern, self.articles)
            else:
                raise ValueError("Nieznany tryb wiedzy; analiza zatrzymana bez zastąpienia starszym katalogiem.")
            logger.info("LLM analysis complete for %s", analysis_id)

            final = self._build_final_from_simple(llm_result)
            for key in ("knowledge", "sources_used", "record_ids", "knowledge_gaps", "checked_points", "unassessed_scope", "review_addenda", "result_guard", "model_connection", "source", "mode"):
                if key in llm_result:
                    final[key] = llm_result[key]
            final.setdefault("model_connection", getattr(self.llm, "last_metadata", {"provider": settings.llm_provider, "model": settings.llm_model_name}))
            await self._save_final(analysis, final, start_time)
            await self._write_audit(analysis_id, user_id, "analysis_complete", {
                "mode": final.get("mode", "llm_only"),
                "knowledge_version": final.get("knowledge", {}).get("version"),
                "classification": final.get("conflict_classification"),
                "applies_count": sum(
                    1 for a in final.get("article_evaluations", []) if a.get("applies")
                ),
            })
            return final

        except Exception as e:
            logger.exception("Analysis %s failed: %s", analysis_id, e)
            try:
                fallback = self._build_error_fallback(e, None)
                analysis.final_result = fallback
                analysis.conflict_classification = fallback["conflict_classification"]
                analysis.risk_level = fallback["risk_level"]
                analysis.confidence_level = fallback["confidence_level"]
                analysis.status = AnalysisStatus.error
                analysis.processing_time_ms = int((time.time() - start_time) * 1000)
                await self.db.commit()
                await self._write_audit(analysis_id, user_id, "analysis_error_fallback", {
                    "error_type": type(e).__name__,
                    "error_message": str(e),
                })
                return fallback
            except Exception as db_err:
                logger.error("Failed to save error_fallback for analysis %s: %s", analysis_id, db_err)
                try:
                    analysis.status = AnalysisStatus.error
                    await self.db.commit()
                except Exception:
                    pass
                raise

    async def _evaluate_articles_sequentially(
        self, analysis_id: UUID, user_id: UUID, extraction: dict
    ) -> list[dict]:
        """Iteruje po katalogu artykulow KERP, kazdy ewaluowany osobnym wywolaniem LLM.
        Early-stop: pierwszy non-waivable artykul ktory applies=true z confidence>=srednia."""
        results: list[dict] = []
        for article in self.articles:
            article_id = article.get("id")
            logger.info("Evaluating article %s for analysis %s", article_id, analysis_id)
            try:
                evaluation = await self.llm.evaluate_article(article, extraction)
            except Exception as e:
                logger.warning("Article %s evaluation failed: %s", article_id, e)
                evaluation = {
                    "article_id": article_id,
                    "applies": False,
                    "confidence": "niska",
                    "matched_premises": [],
                    "unmatched_premises": [],
                    "missing_facts": [f"Blad ewaluacji: {e}"],
                    "justification": f"Nie udalo sie uzyskac oceny LLM dla {article_id}.",
                    "relevant_entities": [],
                    "_error": str(e),
                }
            entry = {
                "article_id": article_id,
                "article": article.get("article"),
                "configuration": article.get("configuration_pl"),
                "waivable": article.get("waivable"),
                "result_if_applies": article.get("result_if_applies"),
                "evaluation": evaluation,
                "applies": bool(evaluation.get("applies")),
                "confidence": evaluation.get("confidence", "niska"),
            }
            results.append(entry)
            await self._write_audit(analysis_id, user_id, "article_evaluated", {
                "article_id": article_id,
                "applies": entry["applies"],
                "confidence": entry["confidence"],
            })
            if entry["applies"] and not article.get("waivable", True) and entry["confidence"] == "wysoka":
                logger.info("Early-stop: %s applies non-waivable (high confidence), skipping remaining articles", article_id)
                await self._write_audit(analysis_id, user_id, "sequential_early_stop", {
                    "article_id": article_id,
                    "remaining": len(self.articles) - len(results),
                })
                break
        return results

    async def resume_after_clarification(self, analysis_id: UUID, answers: list[dict]) -> dict:
        """Wznawia analize po dostarczeniu odpowiedzi na pytania."""
        analysis = await self._get_analysis(analysis_id)

        clarification_text = "\n".join(
            f"Pytanie: {a['question']}\nOdpowiedz: {a['answer']}" for a in answers
        )
        enriched_fact_pattern = f"{analysis.fact_pattern_raw}\n\n--- Uzupelnienia ---\n{clarification_text}"

        return await self.run_analysis(analysis_id, enriched_fact_pattern)

    async def _get_analysis(self, analysis_id: UUID) -> Analysis:
        result = await self.db.execute(select(Analysis).where(Analysis.id == analysis_id))
        return result.scalar_one()

    async def _update_status(self, analysis: Analysis, status: AnalysisStatus) -> None:
        analysis.status = status
        await self.db.commit()

    async def _save_clarifying_questions(self, analysis_id: UUID, questions: list[str], iteration: int) -> None:
        for q in questions:
            self.db.add(Clarification(
                id=uuid.uuid4(),
                analysis_id=analysis_id,
                question=q,
                iteration=iteration,
            ))
        await self.db.commit()

    async def _save_final(self, analysis: Analysis, final: dict, start_time: float) -> None:
        analysis.final_result = final
        analysis.conflict_classification = final.get("conflict_classification")
        analysis.risk_level = final.get("risk_level")
        analysis.confidence_level = final.get("confidence_level")
        analysis.status = AnalysisStatus.complete
        analysis.processing_time_ms = int((time.time() - start_time) * 1000)
        await self.db.commit()

    async def _write_audit(self, analysis_id: UUID, user_id: UUID, event_type: str, data: dict | None = None) -> None:
        self.db.add(AuditLog(
            id=uuid.uuid4(),
            analysis_id=analysis_id,
            user_id=user_id,
            event_type=event_type,
            event_data=data,
        ))
        await self.db.commit()

    def _build_final_from_rules(self, engine_result: EngineResult, extraction: dict) -> dict:
        matched = engine_result.matched_hard + engine_result.matched_soft
        legal_basis = [m.article for m in matched]
        justification = "; ".join(m.description_pl for m in matched if m.description_pl)

        return {
            "entities": extraction.get("entities", []),
            "roles": extraction.get("roles", []),
            "relationships": extraction.get("relationships", []),
            "matter_type": extraction.get("matter_type", ""),
            "missing_information": extraction.get("missing_information", []),
            "analysis_completeness": "pelna",
            "risk_level": "krytyczny",
            "conflict_classification": engine_result.overall_result,
            "justification": justification,
            "confidence_level": "wysoki",
            "legal_basis": legal_basis,
            "rule_matches": [{"rule_id": m.rule_id, "article": m.article, "result": m.result} for m in matched],
            "article_evaluations": [],
            "discrepancies": [],
            "source": "rule_engine",
        }

    def _build_final_from_articles(
        self, article_results: list[dict], engine_result: EngineResult, extraction: dict
    ) -> dict:
        """Agreguje wyniki sekwencyjnej ewaluacji artykulow + porownuje z rule_engine.

        Tryby (mode):
          - "anchored": rule_engine znalazl hard match → comparator dziala, discrepancies + penalizacja confidence
          - "llm_only": brak hard matchow → wynik wylacznie z LLM, bez discrepancies/penalizacji
        """
        has_hard_anchor = bool(engine_result.matched_hard)
        mode = "anchored" if has_hard_anchor else "llm_only"

        applies = [r for r in article_results if r.get("applies")]
        applies_non_waivable = [r for r in applies if not r.get("waivable", True)]
        applies_waivable = [r for r in applies if r.get("waivable", False)]

        if applies_non_waivable:
            classification = "CONFLICT"
            risk_level = "krytyczny"
            confidence_level = self._aggregate_confidence(applies_non_waivable)
        elif applies_waivable:
            classification = "CONFLICT_WAIVABLE"
            risk_level = "umiarkowane"
            confidence_level = self._aggregate_confidence(applies_waivable)
        else:
            classification = "NO_CONFLICT"
            risk_level = "niskie"
            confidence_level = self._aggregate_confidence(article_results) if article_results else "niski"

        # Porownanie z rule_engine — tylko w trybie anchored
        discrepancies: list[dict] = []
        if mode == "anchored":
            rule_articles = {m.article for m in engine_result.matched_hard + engine_result.matched_soft}
            llm_applied_articles = {r.get("article") for r in applies}
            for ra in rule_articles:
                if ra not in llm_applied_articles:
                    discrepancies.append({
                        "type": "rule_engine_flagged_llm_disagreed",
                        "article": ra,
                        "note": "Rule engine wykrył dopasowanie, LLM uznał ze artykul nie ma zastosowania.",
                    })
            for la in llm_applied_articles:
                if la and la not in rule_articles:
                    discrepancies.append({
                        "type": "llm_applied_rule_engine_silent",
                        "article": la,
                        "note": "LLM uznał ze artykul ma zastosowanie, rule engine nie znalazl matcha.",
                    })

            if discrepancies and confidence_level != "niski":
                confidence_level = "umiarkowany"

        legal_basis = sorted({r.get("article") for r in applies if r.get("article")})
        justification_parts = []
        for r in applies:
            ev = r.get("evaluation", {})
            if ev.get("justification"):
                justification_parts.append(f"[{r.get('article')}] {ev['justification']}")
        if not justification_parts:
            justification_parts.append(
                "Zaden z badanych artykulow KERP (art. 30, 27, 28, 29, 26, 26a) nie ma zastosowania do stanu faktycznego."
            )

        all_missing_facts: list[str] = []
        for r in article_results:
            ev = r.get("evaluation", {})
            for mf in ev.get("missing_facts", []):
                if mf and mf not in all_missing_facts:
                    all_missing_facts.append(mf)

        return {
            "entities": extraction.get("entities", []),
            "roles": extraction.get("roles", []),
            "relationships": extraction.get("relationships", []),
            "matter_type": extraction.get("matter_type", ""),
            "missing_information": extraction.get("missing_information", []) + all_missing_facts,
            "analysis_completeness": "pelna" if not all_missing_facts else "czesciowa",
            "risk_level": risk_level,
            "conflict_classification": classification,
            "justification": " | ".join(justification_parts),
            "confidence_level": confidence_level,
            "legal_basis": legal_basis,
            "rule_matches": [
                {"rule_id": m.rule_id, "article": m.article, "result": m.result}
                for m in engine_result.matched_hard + engine_result.matched_soft
            ],
            "article_evaluations": article_results,
            "discrepancies": discrepancies,
            "source": "sequential_articles",
            "mode": mode,
        }

    def _build_final_from_simple(self, llm_result: dict) -> dict:
        """Mapuje single-shot wynik LLM na format final_result kompatybilny z frontendem."""
        article_evals = llm_result.get("article_evaluations", []) or []
        applies = [a for a in article_evals if a.get("applies")]

        return {
            "entities": llm_result.get("entities", []),
            "roles": llm_result.get("roles", []),
            "relationships": llm_result.get("relationships", []),
            "matter_type": llm_result.get("matter_type", ""),
            "missing_information": llm_result.get("missing_information", []),
            "analysis_completeness": llm_result.get("analysis_completeness", "niedostateczna"),
            "risk_level": llm_result.get("risk_level", "nieznane"),
            "conflict_classification": llm_result.get("conflict_classification", "UNKNOWN"),
            "justification": llm_result.get("justification", ""),
            "confidence_level": llm_result.get("confidence_level", "umiarkowany"),
            "legal_basis": llm_result.get("legal_basis", []),
            "rule_matches": [],
            "article_evaluations": article_evals,
            "applies_count": len(applies),
            "discrepancies": [],
            "source": "single_shot_llm",
            "mode": "llm_only",
        }

    @staticmethod
    def _build_error_fallback(exc: Exception, extraction: dict | None) -> dict:
        """Buduje final_result dla scenariusza bledu — frontend zawsze ma co pokazac."""
        msg = (
            f"Analiza nie powiodla sie: {type(exc).__name__}. "
            "Sprobuj ponownie za chwile lub skontaktuj sie z administratorem."
        )
        return {
            "entities": (extraction or {}).get("entities", []),
            "roles": (extraction or {}).get("roles", []),
            "relationships": (extraction or {}).get("relationships", []),
            "matter_type": (extraction or {}).get("matter_type", ""),
            "missing_information": [],
            "analysis_completeness": "niedostateczna",
            "risk_level": "nieznane",
            "conflict_classification": "UNKNOWN",
            "justification": msg,
            "confidence_level": "niski",
            "legal_basis": [],
            "rule_matches": [],
            "article_evaluations": [],
            "discrepancies": [],
            "source": "error_fallback",
            "mode": "error_fallback",
            "error": {"type": type(exc).__name__, "message": str(exc)},
        }

    @staticmethod
    def _aggregate_confidence(results: list[dict]) -> str:
        """Najnizsza pewnosc decyduje (slabe ogniwo)."""
        order = {"wysoka": 3, "srednia": 2, "niska": 1}
        if not results:
            return "niski"
        worst = min(order.get(r.get("confidence", "niska"), 1) for r in results)
        return {3: "wysoki", 2: "umiarkowany", 1: "niski"}[worst]
