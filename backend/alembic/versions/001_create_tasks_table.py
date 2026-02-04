"""Create tasks table.

Revision ID: 001
Revises: None
Create Date: 2026-01-19

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "tasks",
        sa.Column("id", sa.String(length=36), nullable=False),  # Changed from Integer to String to match model
        sa.Column("user_id", sa.String(length=255), nullable=False),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("completed", sa.Boolean(), nullable=False, default=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("idx_tasks_user_id", "tasks", ["user_id"])
    op.create_index("idx_tasks_user_created", "tasks", ["user_id", "created_at"])


def downgrade() -> None:
    op.drop_index("idx_tasks_user_created")
    op.drop_index("idx_tasks_user_id")
    op.drop_table("tasks")
