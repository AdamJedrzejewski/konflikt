import enum
import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, Integer, String, Text, func, JSON
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import Uuid as UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

JSON_PAYLOAD = JSONB().with_variant(JSON(), "sqlite")


class AnalysisStatus(str, enum.Enum):
    pending = "pending"
    extracting = "extracting"
    analyzing = "analyzing"
    complete = "complete"
    error = "error"


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    sub: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False)
    nr_wpisu: Mapped[str | None] = mapped_column(String, nullable=True)
    izba: Mapped[str | None] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    last_login: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    analyses: Mapped[list["Analysis"]] = relationship(back_populates="user")
    audit_logs: Mapped[list["AuditLog"]] = relationship(back_populates="user")


class Analysis(Base):
    __tablename__ = "analyses"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    status: Mapped[AnalysisStatus] = mapped_column(Enum(AnalysisStatus), default=AnalysisStatus.pending)

    fact_pattern_raw: Mapped[str] = mapped_column(Text, nullable=False)
    extraction_result: Mapped[dict | None] = mapped_column(JSON_PAYLOAD, nullable=True)
    schematic_result: Mapped[dict | None] = mapped_column(JSON_PAYLOAD, nullable=True)
    independent_result: Mapped[dict | None] = mapped_column(JSON_PAYLOAD, nullable=True)
    final_result: Mapped[dict | None] = mapped_column(JSON_PAYLOAD, nullable=True)

    conflict_classification: Mapped[str | None] = mapped_column(String, nullable=True)
    risk_level: Mapped[str | None] = mapped_column(String, nullable=True)
    confidence_level: Mapped[str | None] = mapped_column(String, nullable=True)

    iterations: Mapped[int] = mapped_column(Integer, default=0)
    processing_time_ms: Mapped[int | None] = mapped_column(Integer, nullable=True)

    user: Mapped["User"] = relationship(back_populates="analyses")
    audit_logs: Mapped[list["AuditLog"]] = relationship(back_populates="analysis")
    clarifications: Mapped[list["Clarification"]] = relationship(back_populates="analysis")


class AuditLog(Base):
    __tablename__ = "audit_log"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    analysis_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("analyses.id"), nullable=False)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    event_type: Mapped[str] = mapped_column(String, nullable=False)
    event_data: Mapped[dict | None] = mapped_column(JSON_PAYLOAD, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    ip_address: Mapped[str | None] = mapped_column(String, nullable=True)

    analysis: Mapped["Analysis"] = relationship(back_populates="audit_logs")
    user: Mapped["User"] = relationship(back_populates="audit_logs")


class Clarification(Base):
    __tablename__ = "clarifications"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    analysis_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("analyses.id"), nullable=False)
    question: Mapped[str] = mapped_column(Text, nullable=False)
    answer: Mapped[str | None] = mapped_column(Text, nullable=True)
    iteration: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    analysis: Mapped["Analysis"] = relationship(back_populates="clarifications")
