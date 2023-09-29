import uuid

import pydantic


class TokenResponseModel(pydantic.BaseModel):
    sub: uuid.UUID
    exp: int | None = None


class HealthResponseModel(pydantic.BaseModel):
    status: str = pydantic.Field(..., example="healthy", description="Схема доступности сервиса")
