import logging

import lib.app.split_settings as app_split_settings
import lib.clients as clients
import lib.models as models
import lib.tts.repositories.base as tts_repositories_base

logger = logging.getLogger(__name__)


class TTSYandexRepository(tts_repositories_base.TTSBaseRepository):
    def __init__(
        self,
        tts_settings: app_split_settings.TTSYandexSettings,
        client: clients.AsyncHttpClient,
        is_models_from_api: bool = False,
    ):
        self.tts_settings = tts_settings
        if is_models_from_api:
            logger.warning("Yandex TTS doesn't support getting models from API")
        super().__init__(client, is_models_from_api=False)

    @property
    async def voice_models(self) -> models.YandexListVoiceModelsModel:
        return models.YandexListVoiceModelsModel()

    async def get_audio_as_bytes(self, request: models.TTSCreateRequestModel) -> models.TTSCreateResponseModel:
        if not isinstance(request.voice_model, models.YandexVoiceModel):
            raise ValueError("Yandex TTS support only YandexVoiceModel")
        data = {
            "text": request.text,
            "lang": request.voice_model.languages[0].value,
            "voice": request.voice_model.voice_id,
            "emotion": request.voice_model.role,
            "format": self.tts_settings.audio_format,
            "sampleRateHertz": self.tts_settings.sample_rate_hertz,
        }
        response = await self.http_client.post(
            "/tts:synthesize",
            data=data,
        )
        return models.TTSCreateResponseModel(audio_content=response.content)

    async def get_voice_models_by_fields(
        self, fields: models.TTSSearchVoiceRequestModel
    ) -> models.YandexListVoiceModelsModel:
        list_voice_models = await self.get_list_voice_models_by_fields(fields)
        return models.YandexListVoiceModelsModel(models=list_voice_models)  # type: ignore
