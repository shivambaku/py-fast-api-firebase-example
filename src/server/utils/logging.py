import logging
import logging.config
import os

env = os.getenv("APP_ENV", "dev")

if env == "dev" or env == "test":
    os.mkdir("logs") if not os.path.exists("logs") else None

    logging_config = {
        "version": 1,
        "disable_existing_loggers": True,
        "root": {"level": "NOTSET", "handlers": ["file"], "propagate": False},
        "handlers": {
            "file": {
                "class": "logging.handlers.TimedRotatingFileHandler",
                "level": "DEBUG",
                "formatter": "json",
                "when": "D",
                "backupCount": 5,
                "filename": "./logs/backend.log",
            }
        },
        "formatters": {
            "json": {
                "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
                "format": "%(asctime)s %(levelname)s %(filename)s:%(lineno)s %(message)s",  # noqa: E501
                "rename_fields": {
                    "asctime": "time",
                    "levelname": "level",
                    "filename": "file",
                    "lineno": "line",
                },
                "json_indent": 4,
            }
        },
    }

    logging.config.dictConfig(logging_config)

logger = logging.getLogger(__name__)
