import logging
import sys
import os
from typing import Dict


class Formatter(logging.Formatter):
    white: str = "\033[37m"
    cyan: str = "\033[36m"
    green: str = "\033[32m"
    yellow: str = "\033[33m"
    red: str = "\033[31m"
    magenta: str = "\033[35m"

    FORMATTERS: Dict[int, logging.Formatter]

    def __init__(self, fmt: str, *args, **kwargs):
        super(Formatter, self).__init__(*args, **kwargs)
        self.FORMATTERS = {
            logging.NOTSET: logging.Formatter(self.white + fmt, *args, **kwargs),
            logging.DEBUG: logging.Formatter(self.cyan + fmt, *args, **kwargs),
            logging.INFO: logging.Formatter(self.green + fmt, *args, **kwargs),
            logging.WARN: logging.Formatter(self.yellow + fmt, *args, **kwargs),
            logging.ERROR: logging.Formatter(self.red + fmt, *args, **kwargs),
            logging.CRITICAL: logging.Formatter(self.magenta + fmt)
        }

    def format(self, record: logging.LogRecord) -> str:
        return self.FORMATTERS.get(record.levelno, 0).format(record)


def get_logger(name: str) -> logging.Logger:
    log_format = "[%(asctime)s: %(name)s - %(levelname)s]\033[39m %(message)s"

    logger = logging.getLogger(name=name)
    logger.setLevel(os.environ.get("LOG_LEVEL", logging.INFO))

    console_handler = logging.StreamHandler(stream=sys.stdout)
    console_handler.setFormatter(Formatter(log_format))
    logger.addHandler(console_handler)

    logger.propagate = False
    return logger
