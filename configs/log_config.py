import os
import pathlib
import logging.config


def setup_logger(_mode):
  log_dict = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
      "simple": {
        "format": "%(asctime)s : [%(filename)s:%(lineno)d] %(levelname)s -%(message)s"
      }
    },
    "handlers": {
      "console": {
        "formatter": "simple",
        "class": "logging.StreamHandler",
        "level": "DEBUG",
        "stream": "ext://sys.stdout"
      },
      "info_file_handler": {
        "class": "logging.handlers.RotatingFileHandler",
        "level": "DEBUG",
        "formatter": "simple",
        "filename": os.path.join(pathlib.Path(__file__).parent.parent, "logs", "app.log"),
        "maxBytes": 10485760,
        "backupCount": 20,
        "encoding": "utf8"
      }
    },

    "root": {
      "handlers": ["console", "info_file_handler"],
      "level": "INFO"
    }
  }
  logging.config.dictConfig(log_dict)
