"""Create users table.

Revision ID: 002
Revises: 001
Create Date: 2026-01-27

"""
from typing import Sequence, Union
import uuid

import sqlalchemy as sa
from alembic import op

revision: str = "002"
down_revision: Union[str, None] = "001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create users table with string primary key to match JWT token format
    op.create_table(
        "users",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("email", sa.String(length=255), nullable=False, unique=True),
        sa.Column("full_name", sa.String(length=100), nullable=True),
        sa.Column("hashed_password", sa.String(length=255), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False,
                  server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False,
                  server_default=sa.func.now()),
    )
    op.create_index("ix_users_email", "users", ["email"], unique=True)

    # SQLite doesn't support ALTER TABLE ADD CONSTRAINT, so we won't add the foreign key constraint
    # The application logic will enforce the relationship


def downgrade() -> None:
    op.drop_index("ix_users_email")
    op.drop_table("users")