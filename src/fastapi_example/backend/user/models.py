import dataclasses


@dataclasses.dataclass
class User:
    id: int  # pylint: disable=C0103
    name: str


__all__ = [
    "User",
]
