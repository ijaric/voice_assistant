import logging

import httpx
import pydantic

import lib.models.joke as joke_models


class JokeService:
    def __init__(self, http_client: httpx.AsyncClient):
        self.http_client = http_client
        self.logger = logging.getLogger(__name__)

    async def get_joke(self) -> joke_models.Joke | None:
        try:
            async with self.http_client as client:
                response = await client.get("https://official-joke-api.appspot.com/random_joke")
                content = response.json()
                return joke_models.Joke(**content)
        except pydantic.ValidationError as error:
            self.logger.exception("Validation Error: %s", error)
        except httpx.HTTPError as error:
            self.logger.exception("HTTP Error: %s", error)
