import mimetypes
import tempfile

import magic
import openai

import lib.app.settings as app_settings
import lib.models as models


class OpenaiSpeech:
    def __init__(self, settings: app_settings.Settings):
        self.settings = settings
        openai.api_key = self.settings.openai.api_key.get_secret_value()

    @staticmethod
    def __get_file_extension_from_bytes(audio: bytes) -> str | None:
        mime: magic.Magic = magic.Magic(mime=True)
        mime_type: str = mime.from_buffer(audio)
        extension: str | None = mimetypes.guess_extension(mime_type)
        if extension:
            extension = extension.replace(".", "")
        return extension

    async def recognize(self, audio: bytes) -> str:
        file_extension: str | None = self.__get_file_extension_from_bytes(audio)
        if not file_extension:
            raise ValueError("File extension is not supported")

        voice: models.SttVoice = models.SttVoice(
            audio_size=int(len(audio) / 1024),
            audio_format=file_extension,
            audio_data=audio,
            voice_settings=self.settings.voice,
        )

        try:
            with tempfile.NamedTemporaryFile(suffix=f".{file_extension}") as temp_file:
                temp_file.write(voice.audio_data)
                temp_file.seek(0)
                transcript = openai.Audio.transcribe("whisper-1", temp_file)  # type: ignore
        except openai.error.InvalidRequestError as e:  # type: ignore
            raise ValueError(f"OpenAI API error: {e}")
        except openai.error.OpenAIError as e:  # type: ignore
            raise ValueError(f"OpenAI API error: {e}")

        return transcript.text  # type: ignore
