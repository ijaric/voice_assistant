import logging

import httpx
import pydantic

import lib.joke.repository as joke_repository
import lib.models as models


class JokeService:
    def __init__(self, repository: joke_repository.JokeRepository):
        self.repository = repository
        self.logger = logging.getLogger(__name__)

    async def get_joke(self) -> models.Joke | None:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get("https://official-joke-api.appspot.com/random_joke")
                content = response.json()
                self.logger.info("Joke retrieved from API")
                formatted_joke = models.JokeORM(
                    type_field=content["type"], setup=content["setup"], punchline=content["punchline"]
                )
                await self.repository.add_joke(formatted_joke)
                self.logger.info("Joke added to database")
                return models.Joke(**content)
        except pydantic.ValidationError as error:
            self.logger.exception("Validation Error: %s", error)
        except httpx.HTTPError as error:
            self.logger.exception("HTTP Error: %s", error)
