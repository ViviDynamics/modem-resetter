import asyncio
import logging
import os

from sys import stdout


ASYNCIO_EVENT_LOOP = asyncio.get_event_loop()
LOGGER_NAME = os.getenv('LOGGER_NAME', 'modem-resetter')
LOGGER_FORMAT = os.getenv('LOGGER_FORMAT', "%(asctime)s %(name)-12s %(levelname)-8s %(message)s")
LOG_LEVEL = os.getenv('LOGGER_LEVEL', logging.getLevelName(logging.INFO))
logger = logging.getLogger(LOGGER_NAME)


def configure_logger():
    logger.setLevel(LOG_LEVEL)
    log_formatter = logging.Formatter(LOGGER_FORMAT)
    console_handler = logging.StreamHandler(stdout)
    console_handler.setFormatter(log_formatter)
    logger.addHandler(console_handler)


configure_logger()
