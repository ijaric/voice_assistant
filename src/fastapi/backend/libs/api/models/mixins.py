import uuid

import sqlalchemy
from sqlalchemy import Column, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declared_attr


class BaseMixin:
    @declared_attr
    def id(cls):
        return Column(
            UUID(as_uuid=True),
            primary_key=True,
            default=uuid.uuid4,
            unique=True,
            nullable=False,
        )

    @declared_attr
    def created_at(cls):
        return Column(DateTime, server_default=sqlalchemy.func.now())

    @declared_attr
    def updated_at(cls):
        return Column(DateTime, server_default=sqlalchemy.func.now())
    
