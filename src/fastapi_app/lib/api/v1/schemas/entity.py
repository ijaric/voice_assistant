import uuid

import pydantic


class Token(pydantic.BaseModel):
    sub: uuid.UUID
    exp: int | None = None


class Healthy(pydantic.BaseModel):
    status: str = pydantic.Field(..., example="healthy", description="Схема доступности сервиса")
