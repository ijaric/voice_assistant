import json

import aiohttp.web as aiohttp_web

import lib.utils.aiohttp as aiohttp_utils


class LivenessProbeHandler(aiohttp_utils.HandlerProtocol):
    async def process(self, request: aiohttp_web.Request) -> aiohttp_web.Response:
        return aiohttp_web.Response(
            status=200,
            body=json.dumps(obj={"status": "healthy"}),
        )


__all__ = [
    "LivenessProbeHandler",
]
