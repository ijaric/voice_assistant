import datetime
import uuid

import sqlalchemy as sa
import sqlalchemy.orm as sa_orm
import sqlalchemy.sql as sa_sql

import lib.orm_models.base as base_models


class ChatHistory(base_models.Base):
    __tablename__: str = "chat_history"  # type: ignore[reportIncompatibleVariableOverride]

    id: sa_orm.Mapped[uuid.UUID] = sa_orm.mapped_column(primary_key=True, default=uuid.uuid4)
    session_id: sa_orm.Mapped[uuid.UUID] = sa_orm.mapped_column(nullable=False, unique=True)
    channel: sa_orm.Mapped[str] = sa_orm.mapped_column()
    user_id: sa_orm.Mapped[str] = sa_orm.mapped_column()
    content: sa_orm.Mapped[sa.JSON] = sa_orm.mapped_column(sa.JSON)
    created: sa_orm.Mapped[datetime.datetime] = sa_orm.mapped_column(
        sa.DateTime(timezone=True), server_default=sa_sql.func.now()
    )
    modified: sa_orm.Mapped[datetime.datetime] = sa_orm.mapped_column(
        sa.DateTime(timezone=True), server_default=sa_sql.func.now(), onupdate=sa_sql.func.now()
    )
