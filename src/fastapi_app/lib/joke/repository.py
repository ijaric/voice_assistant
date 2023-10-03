import logging

import sqlalchemy.exc
import sqlalchemy.ext.asyncio as sa_asyncio

import lib.models as models


class JokeRepository:
    def __init__(self, async_session: sa_asyncio.async_sessionmaker[sa_asyncio.AsyncSession]):
        self.async_session = async_session
        self.logger = logging.getLogger(__name__)

    async def get_joke_by(self, id: int) -> models.JokeORM | None:
        try:
            async with self.async_session() as session:
                joke = await session.get(models.JokeORM, id)
                return joke
        except sqlalchemy.exc.SQLAlchemyError as error:
            self.logger.exception("Error: %s", error)

    async def add_joke(self, joke: models.JokeORM) -> models.JokeORM | None:
        try:
            async with self.async_session() as session:
                session.add(joke)
                await session.commit()
                await session.refresh(joke)
                return joke
        except sqlalchemy.exc.SQLAlchemyError as error:
            self.logger.exception("Error: %s", error)
