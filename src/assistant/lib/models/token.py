import uuid

import pydantic


# TODO: TBU
class Token(pydantic.BaseModel):
    sub: uuid.UUID
    exp: int | None = None
