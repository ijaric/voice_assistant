import uuid

import sqlalchemy
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declared_attr


class BaseMixin:
    @declared_attr
    def id(cls):
        return sqlalchemy.Column(
            UUID(as_uuid=True),
            primary_key=True,
            default=uuid.uuid4,
            unique=True,
            nullable=False,
        )

    @declared_attr
    def created_at(cls):
        return sqlalchemy.Column(sqlalchemy.DateTime, server_default=sqlalchemy.sql.func.now())

    @declared_attr
    def updated_at(cls):
        return sqlalchemy.Column(sqlalchemy.DateTime, server_default=sqlalchemy.sql.func.now())
