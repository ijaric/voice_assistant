import http

import fastapi

import lib.models as models
import lib.tts.services as tts_service


class TTSHandler:
    def __init__(
        self,
        tts: tts_service.TTSService,
    ):
        self.tts = tts
        self.router = fastapi.APIRouter()
        self.router.add_api_route(
            "/fields",
            self.get_by_fields,
            methods=["POST"],
            summary="Получение моделей по полю",
            description="Возвращает список моделей с указанными полями",
        )
        self.router.add_api_route(
            "/name",
            self.get_by_name,
            methods=["POST"],
            summary="Получение модели по имени",
            description="Позволяет получить одну модель по её имени",
        )
        self.router.add_api_route(
            "/",
            self.get_all,
            methods=["GET"],
            summary="Получение всех доступных моделей",
            description="Возвращает список всех доступных моделей",
        )
        self.router.add_api_route(
            "/languages",
            self.get_languages,
            methods=["GET"],
            summary="Получение всех доступных языков",
            description="Возвращает список всех доступных языков",
        )

    async def get_by_fields(
        self,
        data: models.TTSSearchVoiceRequestModel,
    ) -> list[models.AVAILABLE_MODELS_TYPE]:
        response = await self.tts.get_list_voice_models_by_fields(data)
        return response

    async def get_by_name(
        self,
        model_name: str,
    ) -> models.BaseVoiceModel:
        response = await self.tts.get_voice_model_by_name(model_name)
        if not response:
            raise fastapi.HTTPException(status_code=http.HTTPStatus.BAD_REQUEST, detail="Model not found")
        return response

    async def get_all(self) -> list[models.AVAILABLE_MODELS_TYPE]:
        return await self.tts.get_all_models()

    @classmethod
    async def get_languages(cls) -> dict[str, str]:
        return {language.name: language.value for language in models.BaseLanguageCodesEnum}
