import lib.app.settings as app_settings
import lib.models as models
import lib.tts.models as tts_models


class TTSService:
    def __init__(
        self,
        settings: app_settings.Settings,
        tts_repositories: list[tts_models.TTSRepositoryProtocol],
    ):
        self.settings = settings
        self.tts_repositories = tts_repositories

    def get_audio_as_bytes_from_text(self, tts_request: models.TTSCreateRequestModel) -> models.TTSCreateResponseModel:
        for repository in self.tts_repositories:
            voice_model = repository.get_voice_model_by_name(tts_request.voice_model_name)
            if voice_model:
                audio_response = repository.get_audio_as_bytes_from_text(tts_request.text)
                break
        else:
            raise ValueError(f"Voice model {tts_request.voice_model_name} not found")
        return audio_response

    def get_voice_model_by_name(self, voice_model_name: str) -> models.BaseVoiceModel | None:
        for repository in self.tts_repositories:
            voice_model = repository.get_voice_model_by_name(voice_model_name)
            if voice_model:
                return voice_model

    def get_list_voice_models_by_fields(
        self, fields: models.TTSSearchVoiceRequestModel
    ) -> list[tts_models.VOICE_MODELS_TYPE]:
        response_models: list[tts_models.VOICE_MODELS_TYPE] = []
        for repository in self.tts_repositories:
            voice_models = repository.get_voice_models_by_fields(fields)
            if voice_models.models:
                response_models.extend(voice_models.models)
        return response_models
