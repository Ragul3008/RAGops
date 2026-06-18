"""Evaluation tables
Revision ID: 003
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '003'
down_revision = '002'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "evaluation_runs",
        sa.Column("id", postgresql.UUID(), primary_key=True),
        sa.Column("project_id", postgresql.UUID(), nullable=False),
        sa.Column("tenant_id", postgresql.UUID(), nullable=False),
        sa.Column("status", sa.String(50), default="queued"),
        sa.Column("metrics", postgresql.JSONB()),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True)),
        sa.Column("completed_at", sa.TIMESTAMP(timezone=True)),
        schema="eval",
    )
    op.create_table(
        "eval_samples",
        sa.Column("id", postgresql.UUID(), primary_key=True),
        sa.Column("run_id", postgresql.UUID(), nullable=False),
        sa.Column("question", sa.Text(), nullable=False),
        sa.Column("answer", sa.Text()),
        sa.Column("contexts", postgresql.ARRAY(sa.Text())),
        sa.Column("ground_truth", sa.Text()),
        sa.Column("scores", postgresql.JSONB()),
        schema="eval",
    )