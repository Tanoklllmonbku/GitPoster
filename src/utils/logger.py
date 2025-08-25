# utils/logger.py
import logging
import os
from logging import LoggerAdapter
from pathlib import Path
from logging.handlers import RotatingFileHandler


class ColoredFormatter(logging.Formatter):
    COLORS = {
        'DEBUG': '\033[2;36m',
        'INFO': '\033[0;32m',
        'WARNING': '\033[0;33m',
        'ERROR': '\033[0;31m',
        'CRITICAL': '\033[1;31m'
    }
    RESET = '\033[0m'

    def format(self, record):
        log_color = self.COLORS.get(record.levelname, self.RESET)
        record.levelname = f"{log_color}{record.levelname}{self.RESET}"
        return super().format(record)


def setup_logger(
        version: str,
        name: str = 'GitPoster',
        log_file: str = None,
        level: int = logging.INFO
) -> logging.Logger:
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    # Передаём версию в формат через placeholder
    file_formatter = logging.Formatter(
        f'{version} - %(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_formatter = ColoredFormatter(
        f'{version} - %(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)

        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=10 * 1024 * 1024,
            backupCount=5,
            encoding='utf-8'
        )
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

    logger.setLevel(level)
    return logger


def get_logger(version: str) -> logging.Logger:
    """Получение глобального логгера проекта"""
    log_file = 'logs/system.log'
    return setup_logger(version, 'GitPoster', log_file)