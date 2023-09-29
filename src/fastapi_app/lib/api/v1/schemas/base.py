import uuid

import pydantic


class TokenSchema(pydantic.BaseModel):
    sub: uuid.UUID
    exp: int | None = None


class HealthSchema(pydantic.BaseModel):
    status: str = pydantic.Field(..., example="healthy", description="Схема доступности сервиса")
