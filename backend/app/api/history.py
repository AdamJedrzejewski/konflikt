from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_db
from app.models.db_models import Analysis, AuditLog
from app.models.schemas import AnalysisListResponse, AnalysisResponse


def _status_str(status) -> str:
    return status.value if hasattr(status, 'value') else str(status)

router = APIRouter(prefix="/api/v1", tags=["history"])


@router.get("/history", response_model=AnalysisListResponse)
async def get_history(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    # user: User = Depends(get_current_user)  # auth w fazie 7
):
    """Lista analiz użytkownika (posortowane od najnowszej). Bez fact_pattern_raw w liście."""
    total_result = await db.execute(select(func.count(Analysis.id)))
    total = total_result.scalar_one()

    result = await db.execute(
        select(Analysis)
        .order_by(Analysis.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
    analyses = result.scalars().all()

    items = [
        AnalysisResponse(
            id=a.id,
            status=_status_str(a.status),
            conflict_classification=a.conflict_classification,
            risk_level=a.risk_level,
            confidence_level=a.confidence_level,
            final_result=None,
            created_at=a.created_at,
        )
        for a in analyses
    ]

    return AnalysisListResponse(items=items, total=total)


@router.get("/history/{analysis_id}", response_model=AnalysisResponse)
async def get_analysis_detail(
    analysis_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    """Pełny wynik analizy z uzasadnieniem."""
    result = await db.execute(select(Analysis).where(Analysis.id == analysis_id))
    analysis = result.scalar_one_or_none()

    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")

    return AnalysisResponse(
        id=analysis.id,
        status=_status_str(analysis.status),
        conflict_classification=analysis.conflict_classification,
        risk_level=analysis.risk_level,
        confidence_level=analysis.confidence_level,
        final_result=analysis.final_result,
        created_at=analysis.created_at,
    )


@router.get("/admin/audit", tags=["admin"])
async def get_audit_log(
    analysis_id: UUID | None = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: AsyncSession = Depends(get_db),
):
    """Audit log — tylko dla admina (auth w fazie 7). Na razie brak zabezpieczenia."""
    query = select(AuditLog).order_by(AuditLog.created_at.desc())

    if analysis_id is not None:
        query = query.where(AuditLog.analysis_id == analysis_id)

    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    logs = result.scalars().all()

    return [
        {
            "id": str(log.id),
            "analysis_id": str(log.analysis_id),
            "user_id": str(log.user_id),
            "event_type": log.event_type,
            "event_data": log.event_data,
            "ip_address": log.ip_address,
            "created_at": log.created_at.isoformat(),
        }
        for log in logs
    ]
