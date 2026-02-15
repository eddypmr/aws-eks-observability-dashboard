"""Version endpoint."""

from __future__ import annotations

from fastapi import APIRouter

from api_service.core.config import get_version_info

router = APIRouter()


@router.get("/version")
def get_version() -> dict[str, str]:
    version_info = get_version_info()
    return {
        "commit": version_info.commit,
        "build_time": version_info.build_time,
        "environment": version_info.environment,
    }

