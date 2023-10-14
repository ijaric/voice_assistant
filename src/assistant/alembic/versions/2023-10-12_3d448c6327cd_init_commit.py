"""init commit

Revision ID: 3d448c6327cd
Revises: 
Create Date: 2023-10-12 00:01:42.248941

"""
from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

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
    op.add_column("person_film_work", sa.Column("id", sa.UUID(), autoincrement=False, nullable=False))
    op.drop_constraint(None, "person_film_work", type_="foreignkey")
    op.drop_constraint(None, "person_film_work", type_="foreignkey")
    op.alter_column(
        "person_film_work", "role", existing_type=sa.String(length=50), type_=sa.TEXT(), existing_nullable=False
    )
    op.alter_column("person", "modified", existing_type=postgresql.TIMESTAMP(timezone=True), nullable=True)
    op.alter_column("person", "created", existing_type=postgresql.TIMESTAMP(timezone=True), nullable=True)
    op.alter_column("person", "full_name", existing_type=sa.String(), type_=sa.TEXT(), existing_nullable=False)
    op.drop_constraint(None, "genre_film_work", type_="foreignkey")
    op.drop_constraint(None, "genre_film_work", type_="foreignkey")
    op.alter_column("genre", "modified", existing_type=postgresql.TIMESTAMP(timezone=True), nullable=True)
    op.alter_column("genre", "created", existing_type=postgresql.TIMESTAMP(timezone=True), nullable=True)
    op.alter_column("genre", "description", existing_type=sa.String(), type_=sa.TEXT(), existing_nullable=True)
    op.alter_column("genre", "name", existing_type=sa.String(), type_=sa.TEXT(), existing_nullable=False)
    op.alter_column("film_work", "modified", existing_type=postgresql.TIMESTAMP(timezone=True), nullable=True)
    op.alter_column("film_work", "created", existing_type=postgresql.TIMESTAMP(timezone=True), nullable=True)
    op.alter_column("film_work", "type", existing_type=sa.String(), type_=sa.TEXT(), existing_nullable=False)
    op.alter_column("film_work", "file_path", existing_type=sa.String(), type_=sa.TEXT(), existing_nullable=True)
    op.alter_column("film_work", "creation_date", existing_type=sa.DateTime(), type_=sa.DATE(), existing_nullable=True)
    op.alter_column("film_work", "description", existing_type=sa.String(), type_=sa.TEXT(), existing_nullable=True)
    op.alter_column("film_work", "title", existing_type=sa.String(), type_=sa.TEXT(), existing_nullable=False)
    op.create_table(
        "django_migrations",
        sa.Column("id", sa.BIGINT(), autoincrement=True, nullable=False),
        sa.Column("app", sa.VARCHAR(length=255), autoincrement=False, nullable=False),
        sa.Column("name", sa.VARCHAR(length=255), autoincrement=False, nullable=False),
        sa.Column("applied", postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=False),
    )
    op.create_table(
        "django_admin_log",
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column("action_time", postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=False),
        sa.Column("object_id", sa.TEXT(), autoincrement=False, nullable=True),
        sa.Column("object_repr", sa.VARCHAR(length=200), autoincrement=False, nullable=False),
        sa.Column("action_flag", sa.SMALLINT(), autoincrement=False, nullable=False),
        sa.Column("change_message", sa.TEXT(), autoincrement=False, nullable=False),
        sa.Column("content_type_id", sa.INTEGER(), autoincrement=False, nullable=True),
        sa.Column("user_id", sa.INTEGER(), autoincrement=False, nullable=False),
        sa.CheckConstraint("action_flag >= 0", name="django_admin_log_action_flag_check"),
    )
    op.create_table(
        "django_session",
        sa.Column("session_key", sa.VARCHAR(length=40), autoincrement=False, nullable=False),
        sa.Column("session_data", sa.TEXT(), autoincrement=False, nullable=False),
        sa.Column("expire_date", postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=False),
    )
    op.create_table(
        "auth_permission",
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column("name", sa.VARCHAR(length=255), autoincrement=False, nullable=False),
        sa.Column("content_type_id", sa.INTEGER(), autoincrement=False, nullable=False),
        sa.Column("codename", sa.VARCHAR(length=100), autoincrement=False, nullable=False),
    )
    op.create_table(
        "django_content_type",
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column("app_label", sa.VARCHAR(length=100), autoincrement=False, nullable=False),
        sa.Column("model", sa.VARCHAR(length=100), autoincrement=False, nullable=False),
    )
    op.create_table(
        "auth_user",
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column("password", sa.VARCHAR(length=128), autoincrement=False, nullable=False),
        sa.Column("last_login", postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=True),
        sa.Column("is_superuser", sa.BOOLEAN(), autoincrement=False, nullable=False),
        sa.Column("username", sa.VARCHAR(length=150), autoincrement=False, nullable=False),
        sa.Column("first_name", sa.VARCHAR(length=150), autoincrement=False, nullable=False),
        sa.Column("last_name", sa.VARCHAR(length=150), autoincrement=False, nullable=False),
        sa.Column("email", sa.VARCHAR(length=254), autoincrement=False, nullable=False),
        sa.Column("is_staff", sa.BOOLEAN(), autoincrement=False, nullable=False),
        sa.Column("is_active", sa.BOOLEAN(), autoincrement=False, nullable=False),
        sa.Column("date_joined", postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=False),
    )
    op.create_table(
        "auth_user_user_permissions",
        sa.Column("id", sa.BIGINT(), autoincrement=True, nullable=False),
        sa.Column("user_id", sa.INTEGER(), autoincrement=False, nullable=False),
        sa.Column("permission_id", sa.INTEGER(), autoincrement=False, nullable=False),
    )
    op.create_table(
        "auth_group_permissions",
        sa.Column("id", sa.BIGINT(), autoincrement=True, nullable=False),
        sa.Column("group_id", sa.INTEGER(), autoincrement=False, nullable=False),
        sa.Column("permission_id", sa.INTEGER(), autoincrement=False, nullable=False),
    )
    op.create_table(
        "auth_user_groups",
        sa.Column("id", sa.BIGINT(), autoincrement=True, nullable=False),
        sa.Column("user_id", sa.INTEGER(), autoincrement=False, nullable=False),
        sa.Column("group_id", sa.INTEGER(), autoincrement=False, nullable=False),
    )
    op.create_table(
        "auth_group",
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column("name", sa.VARCHAR(length=150), autoincrement=False, nullable=False),
    )
    op.drop_table("chat_history", schema="content")
    # ### end Alembic commands ###
