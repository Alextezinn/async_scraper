import sys

from constants import PATH_LOG_FILE


config = {
    "handlers": [
        {"sink": sys.stdout, "colorize": True, "format": "<green>{time:YYYY-MM-DD at HH:mm:ss}</green> | {level} | <red>{message}</red>"},
        {"sink": PATH_LOG_FILE, "level": "DEBUG", "rotation": "10 MB",
         "compression": "zip", "serialize": True},
    ]
}