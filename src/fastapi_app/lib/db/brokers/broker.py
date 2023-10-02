from contextlib import asynccontextmanager
from typing import AsyncGenerator, Type

import lib.api.schemas as api_schemas


class BrokerPublisher:
    def __init__(self, broker_class: Type, settings: object):
        self.broker = broker_class(settings)

    async def connect(self):
        await self.broker.connect()

    async def dispose(self):
        await self.broker.dispose()

    async def publish_message(self, message_body: api_schemas.BrokerMessage, routing_key: str):
        await self.broker.publish_message(message_body, routing_key)

    @asynccontextmanager
    async def get_connection(self) -> AsyncGenerator:
        async with self.broker.get_connection() as conn:
            yield conn
