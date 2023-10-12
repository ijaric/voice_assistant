import logging
import uuid

import sqlalchemy as sa
import sqlalchemy.exc
import sqlalchemy.ext.asyncio as sa_asyncio

import lib.models as models
import lib.orm_models as orm_models


class ChatHistoryRepository:
    def __init__(self, pg_async_session: sa_asyncio.async_sessionmaker[sa_asyncio.AsyncSession]) -> None:
        self.pg_async_session = pg_async_session
        self.logger = logging.getLogger(__name__)

    async def get_last_session_id(self, request: models.RequestLastSessionId) -> uuid.UUID | None:
        """Get a new session ID."""

        try:
            async with self.pg_async_session() as session:
                statement = (
                    sa.select(orm_models.ChatHistory)
                    .filter_by(channel=request.channel, user_id=request.user_id)
                    .filter(
                        (
                            sa.func.extract("epoch", orm_models.ChatHistory.created)
                            - sa.func.extract("epoch", orm_models.ChatHistory.modified) / 60
                        )
                        <= request.minutes_ago
                    )
                    .order_by(orm_models.ChatHistory.created.desc())
                    .limit(1)
                )
                result = await session.execute(statement)

                chat_session = result.scalars().first()
                if chat_session:
                    return chat_session.id
        except sqlalchemy.exc.SQLAlchemyError as error:
            self.logger.exception("Error: %s", error)
