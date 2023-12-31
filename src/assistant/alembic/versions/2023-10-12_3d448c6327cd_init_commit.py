"""init commit

Revision ID: 3d448c6327cd
Revises:
Create Date: 2023-10-12 00:01:42.248941

"""
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "3d448c6327cd"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "chat_history",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("session_id", sa.Uuid(), nullable=False),
        sa.Column("channel", sa.String(), nullable=False),
        sa.Column("user_id", sa.String(), nullable=False),
        sa.Column("content", sa.JSON(), nullable=False),
        sa.Column("created", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("modified", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        schema="content",
    )


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("chat_history", schema="content")
    # ### end Alembic commands ###
