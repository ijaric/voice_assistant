import pydantic


class JokeResponse(pydantic.BaseModel):
    id_field: int = pydantic.Field(alias="id")
    joke: str
    category: str
