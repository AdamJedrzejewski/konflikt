"""Rejestr uwag testerów (feedback).

Revision ID: 002_feedback
Revises: 001_initial
Create Date: 2026-10-07
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

revision = "002_feedback"
down_revision = "001_initial"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "feedback",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("analysis_id", UUID(as_uuid=True), sa.ForeignKey("analyses.id"), nullable=False),
        sa.Column("author_id", UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("kind", sa.String, nullable=False),
        sa.Column("description", sa.Text, nullable=False),
        sa.Column("expected", sa.Text, nullable=True),
        sa.Column("source", sa.Text, nullable=True),
        sa.Column("app_version", sa.String, nullable=False),
        sa.Column("knowledge_version", sa.String, nullable=True),
        sa.Column("status", sa.String, nullable=False, server_default="NOWA"),
    )
    op.create_index("ix_feedback_analysis_id", "feedback", ["analysis_id"])
    op.create_index("ix_feedback_author_id", "feedback", ["author_id"])


def downgrade() -> None:
    op.drop_index("ix_feedback_author_id", table_name="feedback")
    op.drop_index("ix_feedback_analysis_id", table_name="feedback")
    op.drop_table("feedback")
