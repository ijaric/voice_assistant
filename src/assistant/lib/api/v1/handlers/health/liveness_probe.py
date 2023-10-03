import fastapi

import lib.api.v1.schemas as api_shemas

basic_router = fastapi.APIRouter()


@basic_router.get(
    "/",
    response_model=api_shemas.HealthResponse,
    summary="Статус работоспособности",
    description="Проверяет доступность сервиса FastAPI.",
)
async def health():
    return api_shemas.HealthResponse(status="healthy")
