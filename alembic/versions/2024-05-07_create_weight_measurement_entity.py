"""create weight measurement entity

Revision ID: 1b6ea1364d25
Revises: 24256a69abac
Create Date: 2024-05-07 09:21:24.447963

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "1b6ea1364d25"
down_revision = "24256a69abac"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "weight_measurement",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("date", sa.DateTime(), nullable=False),
        sa.Column("weight", sa.Float(), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["user.id"], ondelete="CASCADE"),
    )


def downgrade() -> None:
    op.drop_table("weight_measurement")