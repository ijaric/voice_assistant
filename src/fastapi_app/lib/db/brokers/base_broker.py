import abc
import typing

import lib.models.broker_message as lib_models_broker_message

T = typing.TypeVar("T", bound="BasePublisher")


class BasePublisher(abc.ABC):
    @abc.abstractmethod
    async def connect(self) -> None:
        pass

    @abc.abstractmethod
    async def dispose(self) -> None:
        pass

    @abc.abstractmethod
    async def publish_message(self, message_body: lib_models_broker_message.BrokerMessage, routing_key: str) -> None:
        pass
