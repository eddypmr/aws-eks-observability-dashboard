"""Logging setup for the API service."""

from __future__ import annotations

import logging


def configure_logging() -> None:
    """Configure a basic logging setup."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )

