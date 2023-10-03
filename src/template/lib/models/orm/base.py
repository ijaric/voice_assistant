import datetime
import uuid

import sqlalchemy
import sqlalchemy.dialects.postgresql
import sqlalchemy.ext.declarative
import sqlalchemy.orm as sa_orm
import sqlalchemy.sql as sa_sql


class Base(sa_orm.DeclarativeBase):
    """Base class for all models."""

    @sqlalchemy.ext.declarative.declared_attr.directive
    def __tablename__(cls):
        return cls.__name__.lower()

    __mapper_args__ = {"eager_defaults": True}

    id: sa_orm.Mapped[uuid.UUID] = sa_orm.mapped_column(primary_key=True, default=uuid.uuid4)


class IdCreatedUpdatedBaseMixin:
    # id: sa_orm.Mapped[int] = sa_orm.mapped_column(primary_key=True)
    # id_field: sa_orm.Mapped[uuid.UUID] = sa_orm.mapped_column(name="uuid", primary_key=True, unique=True, default=uuid.uuid4, nullable=False)
    created: sa_orm.Mapped[datetime.datetime] = sa_orm.mapped_column(server_default=sa_sql.func.now())
    updated: sa_orm.Mapped[datetime.datetime] = sa_orm.mapped_column(
        server_default=sa_sql.func.now(), onupdate=sa_sql.func.now()
    )

    # __mapper_args__ = {"eager_defaults": True}

    # @sqlalchemy.ext.declarative.declared_attr.directive
    # def __tablename__(cls) -> str:
    #     return cls.__name__.lower()
