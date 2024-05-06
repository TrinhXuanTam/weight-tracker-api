"""create role fixtures

Revision ID: 24256a69abac
Revises: 540aa03659e2
Create Date: 2024-05-06 15:33:28.081575

"""
from alembic import op
import datetime
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from src.modules.auth.constants import UserRole

# revision identifiers, used by Alembic.
revision = "24256a69abac"
down_revision = "540aa03659e2"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.bulk_insert(
        sa.table(
            "role",
            sa.column("id", sa.Integer()),
            sa.column("name", sa.String()),
            sa.column("created_at", sa.DateTime()),
            sa.column("updated_at", sa.DateTime()),
        ),
        [
            {"id": index + 1, "name": role.value, "created_at": datetime.datetime.now(), "updated_at": datetime.datetime.now()} for index, role in enumerate(UserRole)
        ],
    )
    op.execute("SELECT setval('role_id_seq', (SELECT MAX(id) FROM role))")


def downgrade() -> None:
    op.execute("TRUNCATE TABLE role CASCADE")
    op.execute("SELECT setval('role_id_seq', 1, false)")
