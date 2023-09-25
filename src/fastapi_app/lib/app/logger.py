import pydantic_settings


class LoggingSettings(pydantic_settings.BaseSettings):
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    log_default_handlers: list[str] = [
        "console",
    ]

    log_level_handlers: str = "DEBUG"
    log_level_loggers: str = "INFO"
    log_level_root: str = "INFO"


log_settings = LoggingSettings()


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {"format": log_settings.log_format},
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": "%(levelprefix)s %(message)s",
            "use_colors": None,
        },
        "access": {
            "()": "uvicorn.logging.AccessFormatter",
            "fmt": "%(levelprefix)s %(client_addr)s - '%(request_line)s' %(status_code)s",
        },
    },
    "endpoints": {
        "console": {
            "level": log_settings.log_level_handlers,
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
        "access": {
            "formatter": "access",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
    },
    "loggers": {
        "": {
            "endpoints": log_settings.log_default_handlers,
            "level": log_settings.log_level_loggers,
        },
        "uvicorn.error": {
            "level": log_settings.log_level_loggers,
        },
        "uvicorn.access": {
            "endpoints": ["access"],
            "level": log_settings.log_level_loggers,
            "propagate": False,
        },
    },
    "root": {
        "level": log_settings.log_level_root,
        "formatter": "verbose",
        "endpoints": log_settings.log_default_handlers,
    },
}
