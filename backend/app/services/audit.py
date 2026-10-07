import uuid
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.db_models import AuditLog


class AuditService:
    EVENTS = {
        "analysis_created": "Utworzono analizę",
        "extraction_start": "Rozpoczęto ekstrakcję",
        "extraction_complete": "Ekstrakcja zakończona",
        "clarification_requested": "Zadano pytania uzupełniające",
        "clarification_received": "Otrzymano odpowiedzi",
        "rule_engine_start": "Uruchomiono rule engine",
        "rule_engine_match": "Reguła dopasowana",
        "llm_schematic_start": "Analiza schematyczna - start",
        "llm_schematic_complete": "Analiza schematyczna - koniec",
        "llm_independent_start": "Analiza niezależna - start",
        "llm_independent_complete": "Analiza niezależna - koniec",
        "comparison_divergent": "Wyniki rozbieżne - iteracja",
        "analysis_complete": "Analiza zakończona",
        "analysis_error": "Błąd analizy",
    }

    async def log(
        self,
        db: AsyncSession,
        analysis_id: uuid.UUID,
        user_id: uuid.UUID,
        event_type: str,
        data: dict[str, Any] | None = None,
        ip: str | None = None,
    ) -> AuditLog:
        entry = AuditLog(
            id=uuid.uuid4(),
            analysis_id=analysis_id,
            user_id=user_id,
            event_type=event_type,
            event_data=data,
            ip_address=ip,
        )
        db.add(entry)
        await db.flush()
        return entry
