import pydantic_settings

import lib.app.split_settings.utils as app_split_settings_utils


class AgentSettings(pydantic_settings.BaseSettings):
    model_config = pydantic_settings.SettingsConfigDict(
        env_file=app_split_settings_utils.ENV_PATH,
        env_prefix="AGENT_",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    embeddings_limit: int = 5
