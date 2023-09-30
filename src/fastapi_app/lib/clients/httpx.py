# Purpose: Provide an example of an async http client for the application
import contextlib
import typing

import httpx


@contextlib.asynccontextmanager
async def get_http_client() -> typing.AsyncGenerator[httpx.AsyncClient, None]:
    client = httpx.AsyncClient()  # Insert your own settings here
    async with client as ac:
        yield ac
