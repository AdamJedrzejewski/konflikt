from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


# --- Request schemas ---


class AnalysisCreateRequest(BaseModel):
    fact_pattern: str = Field(min_length=50)


class ClarificationAnswer(BaseModel):
    question_id: UUID
    answer: str


class ClarificationAnswerRequest(BaseModel):
    analysis_id: UUID
    answers: list[ClarificationAnswer]


# --- Response schemas ---


class ClarificationQuestion(BaseModel):
    id: UUID
    question: str


class AnalysisResponse(BaseModel):
    id: UUID
    status: str
    conflict_classification: str | None = None
    risk_level: str | None = None
    confidence_level: str | None = None
    final_result: dict | None = None
    clarifying_questions: list[ClarificationQuestion] = []
    created_at: datetime

    model_config = {"from_attributes": True}


class AnalysisListResponse(BaseModel):
    items: list[AnalysisResponse]
    total: int
