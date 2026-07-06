# -*- coding: utf-8 -*-

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

LOG_PATH = Path.home() / ".lead_profiler.log"


def setup_logging(level: str = "INFO") -> None:
    """Configure root logging with a console handler and a rotating file handler."""
    root = logging.getLogger()
    root.setLevel(level)

    formatter = logging.Formatter(
        "%(asctime)s %(levelname)s %(name)s: %(message)s"
    )

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    file_handler = RotatingFileHandler(
        LOG_PATH, maxBytes=1_000_000, backupCount=1, encoding="utf-8"
    )
    file_handler.setFormatter(formatter)

    root.handlers = [stream_handler, file_handler]
