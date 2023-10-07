from typing import Protocol


class STTProtocol(Protocol):
    async def speech_to_text(self, audio: bytes) -> str:
        ...


class SpeechService:
    def __init__(self, repository: STTProtocol):
        self.repository = repository

    async def recognize(self, audio: bytes) -> str:
        return await self.repository.speech_to_text(audio)
