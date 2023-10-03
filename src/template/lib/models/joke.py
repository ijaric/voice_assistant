import pydantic


class Joke(pydantic.BaseModel):
    """Joke model."""

    id_field: int = pydantic.Field(alias="id")
    type_field: str = pydantic.Field(alias="type")
    setup: str
    punchline: str
