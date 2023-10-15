import logging
import typing

import openai
import openai.error

import lib.app.settings as app_settings
import lib.models as models


class EmbeddingRepository:
    """A service for getting embeddings from OpenAI."""

    def __init__(self, settings: app_settings.Settings) -> None:
        """Initialize the service with an OpenAI API key."""
        self.llm = openai.api_key = settings.openai.api_key.get_secret_value()
        self.logger = logging.getLogger(__name__)

    def get_embedding(self, text: str, model: str = "text-embedding-ada-002") -> models.Embedding | None:
        """Get the embedding for a given text."""
        try:
            response: dict[str, typing.Any] = openai.Embedding.create(
                input=text,
                model=model,
            )  # type: ignore[reportGeneralTypeIssues]
            return models.Embedding(**response["data"][0]["embedding"])
        except openai.error.OpenAIError:
            self.logger.exception("Failed to get sync embedding for: %s", text)

    async def aget_embedding(self, text: str, model: str = "text-embedding-ada-002") -> models.Embedding | None:
        """Get the embedding for a given text.[Async]"""
        try:
            response: dict[str, typing.Any] = await openai.Embedding.acreate(
                input=text,
                model=model,
            )  # type: ignore[reportGeneralTypeIssues]
            return models.Embedding(root=response["data"][0]["embedding"])

        except openai.error.OpenAIError:
            self.logger.exception("Failed to get async embedding for: %s", text)
