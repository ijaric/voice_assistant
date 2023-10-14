import pydantic


class Embedding(pydantic.RootModel[list[float]]):
    root: list[float]
