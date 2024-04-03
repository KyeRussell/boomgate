from typing import Literal
import logging
import logging.config
import rich


def configure_logging(
    level: Literal["DEBUG", "INFO"] = "INFO",
    console: rich.console.Console | None = None,
):
    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "rich": {
                "format": "{message}",
                "datefmt": "[%X]",
                "style": "{",
            },
        },
        "handlers": {
            "console": {
                "class": "rich.logging.RichHandler",
                "level": "NOTSET",
                "formatter": "rich",
                "rich_tracebacks": True,
                "console": console,
            },
        },
        "loggers": {
            "boomgate": {
                "handlers": ["console"],
                "level": level,
                "propagate": False,
            },
        },
    }

    logging.config.dictConfig(LOGGING)
