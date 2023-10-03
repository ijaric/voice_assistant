import dataclasses
import enum
import typing

import multidict

import tests.core.settings as functional_settings


class MethodsEnum(enum.Enum):
    GET = "get"
    POST = "post"
    PUT = "put"
    DELETE = "delete"
    PATCH = "patch"


@dataclasses.dataclass
class HTTPResponse:
    body: dict[str, typing.Any] | str
    headers: multidict.CIMultiDictProxy[str]
    status_code: int


class MakeResponseCallableType(typing.Protocol):
    async def __call__(
        self,
        api_method: str = "",
        url: str = functional_settings.tests_settings.api.get_api_url(),
        method: MethodsEnum = MethodsEnum.GET,
        headers: dict[str, str] = functional_settings.tests_settings.project.headers,
        body: dict[str, typing.Any] | None = None,
        jwt_token: str | None = None,
    ) -> HTTPResponse:
        ...
