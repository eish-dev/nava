import logging
import sys
from typing import Any
from loguru import logger
from pathlib import Path

# Configure loguru logger
def setup_logging() -> None:
    # Remove default logger
    logger.remove()
    
    # Log format
    log_format = (
        "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
        "<level>{message}</level>"
    )

    # Add console handler
    logger.add(
        sys.stdout,
        format=log_format,
        level="INFO",
        colorize=True
    )

    # Add file handler
    log_file = Path("logs/app.log")
    log_file.parent.mkdir(parents=True, exist_ok=True)
    logger.add(
        log_file,
        format=log_format,
        level="DEBUG",
        rotation="500 MB",
        retention="10 days"
    )

# Create a class to intercept standard library logging
class InterceptHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage()) 