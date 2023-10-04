import abc

import lib.app.settings as app_settings
import lib.tts.models as tts_models


class BaseTTSService(abc.ABC):
    def __init__(
        self,
        settings: app_settings.Settings,
    ):
        self.settings = settings

    @abc.abstractmethod
    def get_tts(self, tts_request: tts_models.TTSRequestModel) -> tts_models.TTSResponseModel:
        raise NotImplementedError()
