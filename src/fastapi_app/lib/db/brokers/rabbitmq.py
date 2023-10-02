import asyncio
import contextlib
import json

import aio_pika

import lib.api.schemas as api_schemas
import lib.app.split_settings as app_split_settings
import lib.db.brokers as db_brokers


class RabbitMQPublisher(db_brokers.base_broker.BasePublisher):
    def __init__(self, settings: app_split_settings.RabbitMQSettings()):
        self.settings = settings
        self.connection = None
        self.channel = None
        self.pool = asyncio.Queue()
        self.pool_size = settings.max_pool_size

    async def connect(self):
        self.connection = await aio_pika.connect(self.settings.amqp_url)
        self.channel = await self.connection.channel()
        await self.channel.set_qos(prefetch_count=1)
        exchange = await self.channel.declare_exchange(self.settings.exchange, aio_pika.ExchangeType.DIRECT)

        for attr_name, attr_value in vars(self.settings.Queues).items():
            if not attr_name.startswith("__"):
                queue = await self.channel.declare_queue(attr_value.value)
                await queue.bind(exchange, attr_value.value)

    async def dispose(self):
        await self.channel.close()
        await self.connection.close()

    async def publish_message(self, message_body: api_schemas.BrokerMessage, routing_key: str):
        message = aio_pika.Message(content_type="application/json", body=json.dumps(message_body).encode())
        await self.channel.default_exchange.publish(message, routing_key=routing_key)

    @contextlib.asynccontextmanager
    async def get_connection(self):
        if self.pool.empty() and self.pool.qsize() < self.pool_size:
            await self.connect()
            await self.pool.put(self)

        conn = await self.pool.get()
        try:
            yield conn
        finally:
            await self.pool.put(conn)
