"""Rejestr uwag testerów do wyników analiz (etap 3)."""
import csv
import io
import uuid

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.auth import CurrentUser, get_current_user, get_owned_analysis, require_operator
from app.core.config import APP_VERSION
from app.core.deps import get_db
from app.models.db_models import Feedback
from app.models.schemas import FeedbackCreateRequest, FeedbackResponse

router = APIRouter(prefix="/api/v1", tags=["feedback"])

KIND_LABELS = {
    "wynik": "Błędna ocena konfliktu",
    "podstawa": "Brak lub błąd podstawy (przepis, orzeczenie, komentarz)",
    "wyjasnienie": "Niejasne lub niepełne wyjaśnienie",
    "fakty": "Pominięty fakt albo brakujące pytanie",
    "techniczny": "Błąd techniczny",
    "inne": "Inne",
}


def _number(feedback_id: int) -> str:
    return f"U-{feedback_id:04d}"


def _response(item: Feedback) -> FeedbackResponse:
    return FeedbackResponse(
        id=item.id,
        number=_number(item.id),
        analysis_id=item.analysis_id,
        author_email=item.author.email,
        created_at=item.created_at,
        kind=item.kind,
        description=item.description,
        expected=item.expected,
        source=item.source,
        app_version=item.app_version,
        knowledge_version=item.knowledge_version,
        status=item.status,
    )


def _visible(query, current: CurrentUser):
    query = query.options(selectinload(Feedback.author)).order_by(Feedback.id.desc())
    return query if current.is_operator else query.where(Feedback.author_id == current.user.id)


@router.post("/analyze/{analysis_id}/feedback", response_model=FeedbackResponse, status_code=201)
async def create_feedback(
    analysis_id: uuid.UUID,
    request: FeedbackCreateRequest,
    db: AsyncSession = Depends(get_db),
    current: CurrentUser = Depends(get_current_user),
):
    """Zapisuje uwagę do wyniku. Wersja aplikacji i wiedzy dołączana automatycznie."""
    analysis = await get_owned_analysis(analysis_id, current, db)
    knowledge = (analysis.final_result or {}).get("knowledge") or {}
    item = Feedback(
        analysis_id=analysis.id,
        author_id=current.user.id,
        kind=request.kind,
        description=request.description.strip(),
        expected=(request.expected or "").strip() or None,
        source=(request.source or "").strip() or None,
        app_version=APP_VERSION,
        knowledge_version=knowledge.get("version"),
        status="NOWA",
    )
    db.add(item)
    await db.commit()
    item = (await db.execute(_visible(select(Feedback).where(Feedback.id == item.id), current))).scalar_one()
    return _response(item)


@router.get("/analyze/{analysis_id}/feedback", response_model=list[FeedbackResponse])
async def list_analysis_feedback(
    analysis_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current: CurrentUser = Depends(get_current_user),
):
    """Uwagi do jednej analizy: tester widzi własne, operator wszystkie."""
    await get_owned_analysis(analysis_id, current, db)
    result = await db.execute(_visible(select(Feedback).where(Feedback.analysis_id == analysis_id), current))
    return [_response(i) for i in result.scalars().all()]


@router.get("/feedback", response_model=list[FeedbackResponse])
async def list_feedback(
    db: AsyncSession = Depends(get_db),
    current: CurrentUser = Depends(get_current_user),
):
    """Rejestr uwag: tester widzi własne, operator wszystkie."""
    result = await db.execute(_visible(select(Feedback), current))
    return [_response(i) for i in result.scalars().all()]


@router.get("/feedback/export.csv")
async def export_feedback(
    db: AsyncSession = Depends(get_db),
    current: CurrentUser = Depends(require_operator),
):
    """Eksport całego rejestru do CSV (Excel: separator średnik, kodowanie UTF-8 z BOM)."""
    result = await db.execute(_visible(select(Feedback), current))
    buffer = io.StringIO()
    buffer.write("﻿")
    writer = csv.writer(buffer, delimiter=";")
    writer.writerow(["Numer", "Data", "Autor", "Analiza", "Rodzaj", "Opis", "Oczekiwane rozstrzygnięcie",
                     "Źródło", "Wersja aplikacji", "Wersja wiedzy", "Status"])
    for i in result.scalars().all():
        writer.writerow([_number(i.id), i.created_at.isoformat(), i.author.email, str(i.analysis_id),
                         KIND_LABELS.get(i.kind, i.kind), i.description, i.expected or "", i.source or "",
                         i.app_version, i.knowledge_version or "", i.status])
    return StreamingResponse(
        iter([buffer.getvalue()]),
        media_type="text/csv; charset=utf-8",
        headers={"Content-Disposition": 'attachment; filename="obsil_uwagi.csv"'},
    )
