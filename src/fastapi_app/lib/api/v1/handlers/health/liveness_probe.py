import fastapi

import lib.api.v1.schemas as api_shemas

router = fastapi.APIRouter()


@router.get(
    "/",
    response_model=api_shemas.Healthy,
    summary="Статус работоспособности",
    description="Проверяет доступность сервиса FastAPI.",
)
async def health():
    return api_shemas.Healthy(status="healthy")
