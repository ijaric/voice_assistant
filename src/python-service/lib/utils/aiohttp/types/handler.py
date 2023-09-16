import typing

import aiohttp.web as aiohttp_web


class HandlerProtocol(typing.Protocol):
    async def process(self, request: aiohttp_web.Request) -> aiohttp_web.Response:
        ...


__all__ = [
    "HandlerProtocol",
]
