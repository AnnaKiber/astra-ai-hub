"""Add user role

Revision ID: e6b995733110
Revises: 703b43564a0d
Create Date: 2026-08-17
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "e6b995733110"
down_revision: Union[str, Sequence[str], None] = "703b43564a0d"
branch_labels = None
depends_on = None


user_role = sa.Enum(
    "admin",
    "manager",
    "user",
    name="userrole",
)


def upgrade() -> None:
    user_role.create(op.get_bind(), checkfirst=True)

    op.add_column(
        "users",
        sa.Column(
            "role",
            user_role,
            nullable=False,
            server_default="user",
        ),
    )


def downgrade() -> None:
    op.drop_column("users", "role")
    user_role.drop(op.get_bind(), checkfirst=True)