import pydantic_settings

import lib.app.split_settings.utils as app_split_settings_utils


class ApiSettings(pydantic_settings.BaseSettings):
    model_config = pydantic_settings.SettingsConfigDict(
        env_file=app_split_settings_utils.ENV_PATH,
        env_prefix="API_",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    protocol: str = "http"
    host: str = "0.0.0.0"
    port: int = 8000

    def get_api_url(self):
        return f"{self.protocol}://{self.host}:{self.port}/api/v1"
