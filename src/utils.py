"""Utility helpers: logging configuration and filesystem helpers."""

from __future__ import annotations

import logging
from pathlib import Path


def get_logger(name: str) -> logging.Logger:
    """Return a configured module-level logger.

    Args:
        name: Logger name, typically __name__ of the calling module.

    Returns:
        A logging.Logger instance with a stream handler attached once.
    """
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger


def ensure_dir(path: Path) -> Path:
    """Create a directory (and parents) if it does not already exist.

    Args:
        path: Directory path to create.

    Returns:
        The same path, for chaining.
    """
    path.mkdir(parents=True, exist_ok=True)
    return path
