import asyncio
import typing

import fastapi
import httpx
import pytest_asyncio  # type: ignore[reportMissingImports]

import lib.app as lib_app
import tests.core.settings as tests_core_settings
import tests.functional.models as functional_models


@pytest_asyncio.fixture  # type: ignore[reportUntypedFunctionDecorator]
async def http_client(
    base_url: str = tests_core_settings.tests_settings.api.get_api_url(),
) -> typing.AsyncGenerator[httpx.AsyncClient, typing.Any]:
    session = httpx.AsyncClient(base_url=base_url)
    yield session
    await session.aclose()


@pytest_asyncio.fixture  # type: ignore[reportUntypedFunctionDecorator]
async def make_request(http_client: httpx.AsyncClient):
    async def inner(
        api_method: str = "",
        method: functional_models.MethodsEnum = functional_models.MethodsEnum.GET,
        headers: dict[str, str] = tests_core_settings.tests_settings.project.headers,
        body: dict[str, typing.Any] | None = None,
        jwt_token: str | None = None,
    ) -> functional_models.HTTPResponse:
        if jwt_token is not None:
            headers["Authorization"] = f"Bearer {jwt_token}"

        client_params = {"json": body, "headers": headers}
        if method == functional_models.MethodsEnum.GET:
            del client_params["json"]

        response = await getattr(http_client, method.value)(api_method, **client_params)
        return functional_models.HTTPResponse(
            body=response.json(),
            headers=response.headers,
            status_code=response.status_code,
        )

    return inner


@pytest_asyncio.fixture(scope="session")  # type: ignore[reportUntypedFunctionDecorator]
def app() -> fastapi.FastAPI:
    settings = lib_app.Settings()
    application = lib_app.Application.from_settings(settings)
    fastapi_app = application._fastapi_app  # type: ignore[reportPrivateUsage]
    return fastapi_app


@pytest_asyncio.fixture  # type: ignore[reportUntypedFunctionDecorator]
async def app_http_client(
    app: fastapi.FastAPI,
    base_url: str = tests_core_settings.tests_settings.api.get_api_url(),
) -> typing.AsyncGenerator[httpx.AsyncClient, typing.Any]:
    session = httpx.AsyncClient(app=app, base_url=base_url)
    yield session
    await session.aclose()


# @pytest_asyncio.fixture(scope="session")
# def engine() -> collections_abc.Generator[sqlalchemy_ext_asyncio.AsyncEngine, typing.Any, None]:
#     engine = sqlalchemy_ext_asyncio.create_async_engine(tests_core_settings.tests_settings.postgres.db_uri_async)
#     yield engine
#     engine.sync_engine.dispose()
#
#
# @pytest_asyncio.fixture
# async def create(engine: sqlalchemy_ext_asyncio.AsyncEngine) -> collections_abc.AsyncGenerator[None, typing.Any]:
#     async with engine.begin() as conn:
#         await conn.run_sync(tests_unit_models.Base.metadata.create_all)
#     yield
#     async with engine.begin() as conn:
#         await conn.run_sync(tests_unit_models.Base.metadata.drop_all)
#
#
# @pytest_asyncio.fixture
# async def session(
#     engine: sqlalchemy_ext_asyncio.AsyncEngine, create: collections_abc.AsyncGenerator[None, typing.Any]
# ) -> collections_abc.AsyncGenerator[sqlalchemy_ext_asyncio.AsyncSession, typing.Any]:
#     async with sqlalchemy_ext_asyncio.AsyncSession(engine) as session:
#         yield session


@pytest_asyncio.fixture(scope="session")  # type: ignore[reportUntypedFunctionDecorator]
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
