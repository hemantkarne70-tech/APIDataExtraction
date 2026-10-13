import os
import logging
from logging.handlers import RotatingFileHandler
import Config as config

def get_logger(log_file="apidata.log"):
    os.makedirs(config.LOG_PATH, exist_ok=True)

    log_path = os.path.join(config.LOG_PATH, log_file)

    logger_name = os.path.splitext(log_file)[0]
    logger = logging.getLogger(logger_name)

    # Prevent duplicate handlers
    if logger.handlers:
        return logger

    logger.setLevel(logging.DEBUG)
    logger.propagate = False

    # Log format
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # File handler: 10 MB per file, keep 5 backup files
    file_handler = RotatingFileHandler(
        log_path,
        maxBytes=10 * 1024 * 1024,
        backupCount=5,
        encoding="utf-8"
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
