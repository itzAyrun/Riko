import logging
from logging.handlers import RotatingFileHandler

from discord.utils import setup_logging

from config import settings


def configure_logging() -> logging.Logger:
    """Set up logging for the bot."""

    # setup library's logger and grab it as the root logger
    setup_logging()
    logger = logging.getLogger()

    # Add a Rotating File Handler
    file_handler = RotatingFileHandler(
        filename=settings["logger.filepath"],
        mode=settings["logger.mode"],
        maxBytes=settings["logger.max_bytes"],
        backupCount=settings["logger.backup_count"],
        encoding=settings["logger.encoding"],
    )

    file_handler.setFormatter(logging.Formatter(settings["logger.format"]))
    logger.addHandler(file_handler)

    return logger
