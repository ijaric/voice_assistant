import abc
import contextlib
import typing

import lib.api.schemas as api_schemas

T = typing.TypeVar("T", bound="BasePublisher")


class BasePublisher(abc.ABC):
    @abc.abstractmethod
    async def connect(self) -> None:
        pass

    @abc.abstractmethod
    async def dispose(self) -> None:
        pass

    @abc.abstractmethod
    async def publish_message(self, message_body: api_schemas.broker_message.BrokerMessage, routing_key: str) -> None:
        pass

    @abc.abstractmethod
    async def get_connection(self) -> contextlib.AbstractAsyncContextManager[T]:
        pass
