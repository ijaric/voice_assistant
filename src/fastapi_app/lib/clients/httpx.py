import contextlib
import typing

import httpx


@contextlib.asynccontextmanager
async def get_async_http_session(
    settings: dict[str, typing.Any] | None = None
) -> typing.AsyncGenerator[httpx.AsyncClient, None]:
    """Async http client."""
    if settings is None:
        settings = {}
    client = httpx.AsyncClient(**settings)  # Insert your own settings here
    async with client as ac:
        yield ac
