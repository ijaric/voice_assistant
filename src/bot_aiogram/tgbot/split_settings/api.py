import pydantic_settings

import tgbot.split_settings.utils as split_settings_utils


class ApiSettings(pydantic_settings.BaseSettings):
    model_config = pydantic_settings.SettingsConfigDict(
        env_file=split_settings_utils.ENV_PATH,
        env_prefix="API_",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    url: str
    port: int
    protocol: str

    @property
    def api_url(self) -> str:
        return f"{self.protocol}://{self.url}:{self.port}"
