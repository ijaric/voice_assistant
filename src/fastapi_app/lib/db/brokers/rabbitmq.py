import asyncio
import contextlib
import json
import logging

import aio_pika

import lib.app.split_settings as app_split_settings
import lib.db.brokers as db_brokers
import lib.models.broker_message as models_broker_message


class RabbitMQPublisher(db_brokers.base_broker.BasePublisher):
    def __init__(self, settings: app_split_settings.RabbitMQSettings()):
        self.settings = settings
        self.connection = None
        self.logger = logging.getLogger(__name__)
        self.pool = asyncio.Queue(maxsize=settings.max_pool_size)

    async def connect(self):
        try:
            self.connection = await aio_pika.connect(self.settings.amqp_url)

            for _ in range(self.settings.max_pool_size):
                channel = await self.connection.channel()
                await channel.set_qos(prefetch_count=1)
                await self.pool.put(channel)

        except Exception as e:
            self.logger.error(f"Failed to dispose resources: {e}")
            raise

    async def dispose(self):
        try:
            while not self.pool.empty():
                print("Closing channel")
                channel = await self.pool.get()
                await channel.close()

            if self.connection:
                await self.connection.close()
        except Exception as e:
            self.logger.error(f"Failed to dispose resources: {e}")
            raise

    @contextlib.asynccontextmanager
    async def __get_channel(self):
        if not self.connection:
            await self.connect()

        if self.pool.empty():
            channel = await self.connection.channel()
            await self.pool.put(channel)

        channel = await self.pool.get()
        try:
            yield channel
        finally:
            await self.pool.put(channel)

    async def publish_message(self, message_body: models_broker_message.BrokerMessage, routing_key: str):
        try:
            async with self.__get_channel() as channel:
                message = aio_pika.Message(content_type="application/json", body=json.dumps(message_body).encode())
                await channel.default_exchange.publish(message, routing_key=routing_key)
        except Exception as e:
            logging.error(f"Failed to publish message: {e}")
            raise
