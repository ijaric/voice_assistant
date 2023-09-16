import dataclasses
import json
import typing


class Handler(typing.Protocol):
    def __call__(self) -> "Response":
        ...


@dataclasses.dataclass
class Response:
    code: int
    body: str


def get_response_from_dataclass(body: object) -> Response:
    assert dataclasses.is_dataclass(body), "body must be a dataclass"

    return Response(code=200, body=json.dumps(dataclasses.asdict(body)))
