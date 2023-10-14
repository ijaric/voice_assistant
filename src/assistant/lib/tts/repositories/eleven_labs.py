import typing

import lib.app.split_settings as app_split_settings
import lib.clients as clients
import lib.models as models
import lib.tts.repositories.base as tts_repositories_base


class TTSElevenLabsRepository(tts_repositories_base.TTSBaseRepository):
    def __init__(
        self,
        tts_settings: app_split_settings.TTSElevenLabsSettings,
        client: clients.AsyncHttpClient,
        is_models_from_api: bool = False,
    ):
        self.tts_settings = tts_settings
        super().__init__(client, is_models_from_api)

    @property
    async def voice_models(self) -> models.ElevenLabsListVoiceModelsModel:
        if self.is_models_from_api:
            return models.ElevenLabsListVoiceModelsModel.from_api(await self.get_all_models_dict_from_api())
        return models.ElevenLabsListVoiceModelsModel()

    async def get_all_models_dict_from_api(self) -> list[dict[str, typing.Any]]:
        response = await self.http_client.get("/models")
        return response.json()

    async def get_audio_as_bytes(self, request: models.TTSCreateRequestModel) -> models.TTSCreateResponseModel:
        if not isinstance(request.voice_model, models.ElevenLabsVoiceModel):
            raise ValueError("ElevenLabs TTS support only ElevenLabsVoiceModel")
        response = await self.http_client.post(
            f"/text-to-speech/{self.tts_settings.default_voice_id}",
            json={"text": request.text, "model_id": request.voice_model.voice_id},
        )
        return models.TTSCreateResponseModel(audio_content=response.content)

    async def get_voice_models_by_fields(
        self, fields: models.TTSSearchVoiceRequestModel
    ) -> models.ElevenLabsListVoiceModelsModel:
        list_voice_models = await self.get_list_voice_models_by_fields(fields)
        return models.ElevenLabsListVoiceModelsModel(models=list_voice_models)  # type: ignore
