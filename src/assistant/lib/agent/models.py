import datetime
import uuid

import pydantic


class Movie(pydantic.BaseModel):
    id: uuid.UUID
    title: str
    description: str | None = None
    rating: float
    type: str
    created: datetime.datetime
    modified: datetime.datetime


class Embedding(pydantic.RootModel[list[float]]):
    root: list[float]
