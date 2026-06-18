"""Initial RAGOps schema
Revision ID: 001
Create Date: 2024-01-01
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("CREATE SCHEMA IF NOT EXISTS auth")
    op.execute("CREATE SCHEMA IF NOT EXISTS rag")
    op.execute("CREATE SCHEMA IF NOT EXISTS eval")
    op.execute("CREATE SCHEMA IF NOT EXISTS billing")
    
    op.create_table(
        "tenants",
        sa.Column("id", postgresql.UUID(), primary_key=True),
        sa.Column("slug", sa.String(63), unique=True, nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("plan", sa.String(50), nullable=False),
        sa.Column("is_active", sa.Boolean(), default=True),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True),
                  server_default=sa.text("NOW()")),
        schema="auth",
    )
    op.create_table(
        "users",
        sa.Column("id", postgresql.UUID(), primary_key=True),
        sa.Column("tenant_id", postgresql.UUID(), nullable=False),
        sa.Column("email", sa.String(255), nullable=False),
        sa.Column("hashed_password", sa.String(255)),
        sa.Column("roles", postgresql.ARRAY(sa.String())),
        sa.Column("is_active", sa.Boolean(), default=True),
        schema="auth",
    )
    op.execute("ALTER TABLE auth.users ENABLE ROW LEVEL SECURITY;")
    op.execute("""
        CREATE POLICY tenant_isolation ON auth.users
          USING (tenant_id = current_setting('app.tenant_id')::uuid);
    """)