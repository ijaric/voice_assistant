import lib.models.broker_message as lib_models_broker_message


class BrokerPublisher:
    def __init__(self, broker_class: type, settings: object):
        self.broker = broker_class(settings)

    async def connect(self):
        await self.broker.connect()

    async def dispose(self):
        await self.broker.dispose()

    async def publish_message(self, message_body: lib_models_broker_message.BrokerMessage, routing_key: str):
        await self.broker.publish_message(message_body, routing_key)
