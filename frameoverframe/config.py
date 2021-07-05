"""Frameoverframe configurations."""

# extensions = ["JPG", "ARW", "CR2"]  # not sure if this ever gets used??

# These should be case insensitive. Hopefully.
RAW_EXTENSIONS = [".CR2", ".ARW", ".NEF", ".DNG"]

UNLINKABLE_FILES = [".DS_Store", "Thumbs.db"]

LOGFILE = "frameoverframe.log"

LOGGING_CONFIG = {
    "version": 1,
    "formatters": {
        "simple": {
            "format": "%(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "detailed": {
            "format": "%(asctime)s -  %(levelname)s - %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "simple",
            "stream": "ext://sys.stdout",
        },
        "file": {
            "level": "DEBUG",
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "detailed",
            "filename": LOGFILE,
            "maxBytes": 10485760,  # 10MB
            "backupCount": 3,
        },
    },
    # include "file" in the list of handlers to log to the file too.
    "loggers": {
        "frameoverframe": {
            "level": "INFO",
            "handlers": [
                "console",
            ],
        },
    },
    "disable_existing_loggers": False,
}
