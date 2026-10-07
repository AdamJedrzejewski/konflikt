"""Initial migration - create users, analyses, audit_log, clarifications tables.

Revision ID: 001_initial
Revises:
Create Date: 2026-05-04
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB, UUID

# revision identifiers, used by Alembic.
revision = "001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # --- users ---
    op.create_table(
        "users",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("sub", sa.String, unique=True, nullable=False),
        sa.Column("email", sa.String, nullable=False),
        sa.Column("nr_wpisu", sa.String, nullable=True),
        sa.Column("izba", sa.String, nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
        ),
        sa.Column(
            "last_login",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
        ),
        sa.Column("is_active", sa.Boolean, default=True),
    )

    # --- analyses ---
    op.create_table(
        "analyses",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "user_id",
            UUID(as_uuid=True),
            sa.ForeignKey("users.id"),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
        ),
        sa.Column(
            "status",
            sa.Enum(
                "pending",
                "extracting",
                "analyzing",
                "complete",
                "error",
                name="analysisstatus",
            ),
            default="pending",
        ),
        sa.Column("fact_pattern_raw", sa.Text, nullable=False),
        sa.Column("extraction_result", JSONB, nullable=True),
        sa.Column("schematic_result", JSONB, nullable=True),
        sa.Column("independent_result", JSONB, nullable=True),
        sa.Column("final_result", JSONB, nullable=True),
        sa.Column("conflict_classification", sa.String, nullable=True),
        sa.Column("risk_level", sa.String, nullable=True),
        sa.Column("confidence_level", sa.String, nullable=True),
        sa.Column("iterations", sa.Integer, default=0),
        sa.Column("processing_time_ms", sa.Integer, nullable=True),
    )

    # --- audit_log ---
    op.create_table(
        "audit_log",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "analysis_id",
            UUID(as_uuid=True),
            sa.ForeignKey("analyses.id"),
            nullable=False,
        ),
        sa.Column(
            "user_id",
            UUID(as_uuid=True),
            sa.ForeignKey("users.id"),
            nullable=False,
        ),
        sa.Column("event_type", sa.String, nullable=False),
        sa.Column("event_data", JSONB, nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
        ),
        sa.Column("ip_address", sa.String, nullable=True),
    )

    # --- clarifications ---
    op.create_table(
        "clarifications",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "analysis_id",
            UUID(as_uuid=True),
            sa.ForeignKey("analyses.id"),
            nullable=False,
        ),
        sa.Column("question", sa.Text, nullable=False),
        sa.Column("answer", sa.Text, nullable=True),
        sa.Column("iteration", sa.Integer, nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
        ),
    )


def downgrade() -> None:
    op.drop_table("clarifications")
    op.drop_table("audit_log")
    op.drop_table("analyses")
    op.drop_table("users")
    op.execute("DROP TYPE IF EXISTS analysisstatus")
