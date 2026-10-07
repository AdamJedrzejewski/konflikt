import uuid

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.llm_adapter import create_adapter
from app.core.auth import CurrentUser, get_current_user, get_owned_analysis
from app.core.database import get_db
from app.models.db_models import Analysis, AnalysisStatus, Clarification
from app.models.schemas import AnalysisCreateRequest, AnalysisResponse, ClarificationAnswerRequest
from app.rules.engine import RuleEngine
from app.services.orchestrator import AnalysisOrchestrator

router = APIRouter(prefix="/api/v1", tags=["analysis"])

# Singleton rule engine (loaded once at startup)
_rule_engine = RuleEngine()



def _status_str(status) -> str:
    """Convert AnalysisStatus enum or string to string."""
    return status.value if hasattr(status, 'value') else str(status)


async def _run_orchestrator(analysis_id: uuid.UUID, fact_pattern: str) -> None:
    """Background task that runs the analysis orchestrator."""
    import logging
    logger = logging.getLogger(__name__)

    from app.core.database import AsyncSessionLocal

    try:
        logger.info("Background task started for analysis %s", analysis_id)
        async with AsyncSessionLocal() as db:
            adapter = create_adapter()
            logger.info("Adapter created: %s", type(adapter).__name__)
            orchestrator = AnalysisOrchestrator(adapter, _rule_engine, db)
            await orchestrator.run_analysis(analysis_id, fact_pattern)
            logger.info("Analysis %s completed successfully", analysis_id)
    except Exception as e:
        logger.exception("Background task failed for analysis %s: %s", analysis_id, e)
        try:
            async with AsyncSessionLocal() as db:
                result = await db.execute(select(Analysis).where(Analysis.id == analysis_id))
                analysis = result.scalar_one_or_none()
                if analysis is None:
                    raise RuntimeError(f"Analysis {analysis_id} disappeared before failure could be saved")

                fallback = AnalysisOrchestrator._build_error_fallback(e, None)
                analysis.final_result = fallback
                analysis.conflict_classification = fallback["conflict_classification"]
                analysis.risk_level = fallback["risk_level"]
                analysis.confidence_level = fallback["confidence_level"]
                analysis.status = AnalysisStatus.error
                await db.commit()
        except Exception:
            logger.exception("Failed to save startup error for analysis %s", analysis_id)
            raise


@router.post("/analyze", response_model=AnalysisResponse, status_code=202)
async def create_analysis(
    request: AnalysisCreateRequest,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
    current: CurrentUser = Depends(get_current_user),
):
    """
    Tworzy nową analizę. Uruchamia orchestrator w tle (BackgroundTasks).
    Zwraca analysis_id i status=pending natychmiast.
    Klient powinien pollować GET /analyze/{id} po wynik.
    """
    analysis = Analysis(
        id=uuid.uuid4(),
        user_id=current.user.id,
        fact_pattern_raw=request.fact_pattern,
        status="pending",
    )
    db.add(analysis)
    await db.commit()
    await db.refresh(analysis)

    background_tasks.add_task(_run_orchestrator, analysis.id, request.fact_pattern)

    return AnalysisResponse(
        id=analysis.id,
        status=_status_str(analysis.status),
        created_at=analysis.created_at,
    )


@router.get("/analyze/{analysis_id}", response_model=AnalysisResponse)
async def get_analysis(
    analysis_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current: CurrentUser = Depends(get_current_user),
):
    """Pobiera status i wynik analizy (autor albo operator)."""
    analysis = await get_owned_analysis(analysis_id, current, db)

    # Pobierz pytania uzupełniające jeśli status pending i są pytania
    questions = []
    if analysis.status == "pending":
        clarifications_result = await db.execute(
            select(Clarification)
            .where(Clarification.analysis_id == analysis_id, Clarification.answer.is_(None))
        )
        questions = [
            {"id": c.id, "question": c.question}
            for c in clarifications_result.scalars().all()
        ]

    return AnalysisResponse(
        id=analysis.id,
        status=_status_str(analysis.status),
        conflict_classification=analysis.conflict_classification,
        risk_level=analysis.risk_level,
        confidence_level=analysis.confidence_level,
        final_result=analysis.final_result,
        clarifying_questions=questions,
        created_at=analysis.created_at,
    )


@router.post("/analyze/{analysis_id}/clarify")
async def submit_clarification(
    analysis_id: uuid.UUID,
    request: ClarificationAnswerRequest,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
    current: CurrentUser = Depends(get_current_user),
):
    """Dostarcza odpowiedzi na pytania uzupełniające, wznawia analizę (autor albo operator)."""
    analysis = await get_owned_analysis(analysis_id, current, db)

    if analysis.status != "pending":
        raise HTTPException(status_code=400, detail="Analysis is not awaiting clarification")

    # Zapisz odpowiedzi
    answers_for_orchestrator = []
    for answer in request.answers:
        clarification_result = await db.execute(
            select(Clarification).where(
                Clarification.id == answer.question_id,
                Clarification.analysis_id == analysis_id,
            )
        )
        clarification = clarification_result.scalar_one_or_none()
        if clarification:
            clarification.answer = answer.answer
            answers_for_orchestrator.append({
                "question": clarification.question,
                "answer": answer.answer,
            })

    await db.commit()

    # Wznów analizę w tle
    async def _resume(aid: uuid.UUID, answers: list[dict]) -> None:
        from app.core.database import AsyncSessionLocal

        async with AsyncSessionLocal() as session:
            adapter = create_adapter()
            orchestrator = AnalysisOrchestrator(adapter, _rule_engine, session)
            await orchestrator.resume_after_clarification(aid, answers)

    background_tasks.add_task(_resume, analysis_id, answers_for_orchestrator)

    return {"status": "processing", "message": "Clarification received, analysis resumed"}
