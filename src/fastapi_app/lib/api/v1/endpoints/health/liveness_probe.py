import fastapi

import lib.api.schemas as api_shemas

router = fastapi.APIRouter()


@router.get(
    "/",
    response_model=api_shemas.entity.Healthy,
    summary="Статус работоспособности",
    description="Проверяет доступность сервиса FastAPI.",
)
async def liveness_probe():
    return api_shemas.entity.Healthy(status="healthy")
