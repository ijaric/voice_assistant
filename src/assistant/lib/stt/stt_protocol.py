from typing import Protocol


class STTProtocol(Protocol):
    async def recognize(self, audio: bytes) -> str:
        ...
