import uuid

import pydantic


class Token(pydantic.BaseModel):
    sub: uuid.UUID
    exp: int | None = None
