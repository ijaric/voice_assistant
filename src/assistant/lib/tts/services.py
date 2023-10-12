import lib.app.settings as app_settings
import lib.models as models
import lib.tts.models as tts_models


class TTSService:
    def __init__(
        self,
        settings: app_settings.Settings,
        repositories: dict[models.VoiceModelProvidersEnum, tts_models.TTSRepositoryProtocol],
    ):
        self.settings = settings
        self.repositories = repositories

    def get_audio_as_bytes(self, request: models.TTSCreateRequestModel) -> models.TTSCreateResponseModel:
        model = request.voice_model
        repository = self.repositories[model.provider]
        audio_response = repository.get_audio_as_bytes(request)
        return audio_response

    def get_voice_model_by_name(self, voice_model_name: str) -> models.BaseVoiceModel | None:
        for repository in self.repositories.values():
            voice_model = repository.get_voice_model_by_name(voice_model_name)
            if voice_model:
                return voice_model

    def get_list_voice_models_by_fields(
        self, fields: models.TTSSearchVoiceRequestModel
    ) -> list[models.AVAILABLE_MODELS_TYPE]:
        response_models: list[models.AVAILABLE_MODELS_TYPE] = []
        for repository in self.repositories.values():
            voice_models = repository.get_voice_models_by_fields(fields)
            if voice_models.models:
                response_models.extend(voice_models.models)
        return response_models
