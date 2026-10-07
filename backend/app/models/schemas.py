from datetime import datetime
from uuid import UUID

from typing import Literal

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


FeedbackKind = Literal["wynik", "podstawa", "wyjasnienie", "fakty", "techniczny", "inne"]


class FeedbackCreateRequest(BaseModel):
    kind: FeedbackKind
    description: str = Field(min_length=5, max_length=10000)
    expected: str | None = Field(default=None, max_length=10000)
    source: str | None = Field(default=None, max_length=2000)


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


class FeedbackResponse(BaseModel):
    id: int
    number: str
    analysis_id: UUID
    author_email: str
    created_at: datetime
    kind: str
    description: str
    expected: str | None = None
    source: str | None = None
    app_version: str
    knowledge_version: str | None = None
    status: str
