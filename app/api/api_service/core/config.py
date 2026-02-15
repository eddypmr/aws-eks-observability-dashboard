"""Configuration helpers for environment-backed settings."""

from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class VersionInfo:
    """Data returned by the version endpoint."""

    commit: str
    build_time: str
    environment: str


def get_version_info() -> VersionInfo:
    """Read version metadata from environment variables with safe defaults."""
    return VersionInfo(
        commit=os.getenv("COMMIT_SHA", "unknown"),
        build_time=os.getenv("BUILD_TIME", "unknown"),
        environment=os.getenv("ENVIRONMENT", "dev"),
    )

