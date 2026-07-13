"""Rich logging helpers."""

from __future__ import annotations

import logging
from typing import Optional

from rich.console import Console
from rich.logging import RichHandler

_CONSOLE = Console(stderr=True)
_CONFIGURED = False


def get_console() -> Console:
    return _CONSOLE


def setup_logging(*, debug: bool = False, level: str = "INFO") -> logging.Logger:
    global _CONFIGURED
    logger = logging.getLogger("auto_gen_py_project")
    logger.handlers.clear()
    logger.setLevel(logging.DEBUG if debug else getattr(logging, level.upper(), logging.INFO))
    logger.propagate = False
    handler = RichHandler(console=_CONSOLE, show_path=debug, rich_tracebacks=True, markup=True)
    handler.setFormatter(logging.Formatter("%(message)s"))
    logger.addHandler(handler)
    _CONFIGURED = True
    return logger


def get_logger(name: str = "auto_gen_py_project") -> logging.Logger:
    if not _CONFIGURED:
        setup_logging()
    return logging.getLogger(name)
