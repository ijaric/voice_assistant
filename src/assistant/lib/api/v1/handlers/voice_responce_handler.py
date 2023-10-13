import fastapi

import lib.models.tts.voice as models_tts_voice
import lib.stt.services as stt_services


class VoiceResponseHandler:
    def __init__(
        self,
        stt: stt_services.SpeechService,
    ):
        self.stt = stt
        self.router = fastapi.APIRouter()
        self.router.add_api_route(
            "/",
            self.voice_response,
            methods=["POST"],
            summary="Ответ голосового помощника",
            description="Ответ голосового помощника",
        )

    async def voice_response(
        self,
        voice: bytes = fastapi.File(...),
        voice_model: models_tts_voice.VoiceModelProvidersEnum = fastapi.Depends(),
    ) -> dict[str, str]:
        voice_text: str = await self.stt.recognize(voice)
        return {"text": voice_text}
