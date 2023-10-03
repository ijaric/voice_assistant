import uuid

import sqlalchemy
import sqlalchemy.dialects.postgresql
import sqlalchemy.ext.declarative
import sqlalchemy.orm


class Base(sqlalchemy.orm.DeclarativeBase):
    """Base class for all models."""

    pass


class IdCreatedUpdatedBaseMixin(Base):
    @sqlalchemy.ext.declarative.declared_attr
    def uuid(cls):
        return sqlalchemy.Column(
            sqlalchemy.dialects.postgresql.UUID(as_uuid=True),
            primary_key=True,
            default=uuid.uuid4,
            unique=True,
            nullable=False,
        )

    @sqlalchemy.ext.declarative.declared_attr
    def created_at(cls):
        return sqlalchemy.Column(sqlalchemy.DateTime, server_default=sqlalchemy.sql.func.now())

    @sqlalchemy.ext.declarative.declared_attr
    def updated_at(cls):
        return sqlalchemy.Column(sqlalchemy.DateTime, server_default=sqlalchemy.sql.func.now())

    @sqlalchemy.ext.declarative.declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
