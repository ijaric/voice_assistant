import typing
from enum import Enum

import pydantic
import pydantic_settings

import lib.app.split_settings.utils as app_split_settings_utils


class QueueNames(Enum):
    STT = "stt_queue"
    TTS = "tts_queue"


class RabbitMQSettings(pydantic_settings.BaseSettings):
    """RabbitMQ settings."""

    class Queues:
        TTS = QueueNames.TTS
        STT = QueueNames.STT

    model_config = pydantic_settings.SettingsConfigDict(
        env_file=app_split_settings_utils.ENV_PATH,
        env_prefix="RABBITMQ_",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    host: str = "localhost"
    port: int = 5672
    user: str = "guest"
    password: pydantic.SecretStr = pydantic.Field(
        default=..., validation_alias=pydantic.AliasChoices("password", "rabbitmq_password")
    )
    queues: Queues = Queues()
    exchange: str = "message_exchange"
    exchange_type: str = "direct"
    max_pool_size: int = 10

    @property
    def amqp_url(self) -> str:
        password = self.password.get_secret_value()
        return f"amqp://{self.user}:{password}@{self.host}:{self.port}"
