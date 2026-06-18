"""RAG core tables
Revision ID: 002
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "projects",
        sa.Column("id", postgresql.UUID(), primary_key=True),
        sa.Column("tenant_id", postgresql.UUID(), nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("description", sa.Text()),
        sa.Column("vectorstore_config", postgresql.JSONB()),
        sa.Column("llm_config", postgresql.JSONB()),
        sa.Column("embedding_config", postgresql.JSONB()),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True)),
        schema="rag",
    )
    op.create_table(
        "documents",
        sa.Column("id", postgresql.UUID(), primary_key=True),
        sa.Column("project_id", postgresql.UUID(), nullable=False),
        sa.Column("tenant_id", postgresql.UUID(), nullable=False),
        sa.Column("filename", sa.String(512), nullable=False),
        sa.Column("mime_type", sa.String(127)),
        sa.Column("size_bytes", sa.BigInteger()),
        sa.Column("status", sa.String(50), default="pending"),
        sa.Column("chunk_count", sa.Integer()),
        sa.Column("s3_key", sa.String(512)),
        sa.Column("metadata", postgresql.JSONB()),
        schema="rag",
    )
    op.create_index(
        "idx_documents_tenant_project",
        "documents",
        ["tenant_id","project_id"],
        schema="rag",
    )