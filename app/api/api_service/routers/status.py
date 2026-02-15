"""Status endpoint."""

from __future__ import annotations

from fastapi import APIRouter

from api_service.services.status_service import get_latency_ms

router = APIRouter()


@router.get("/status")
def get_status() -> dict[str, int | bool]:
    return {"up": True, "latency_ms": get_latency_ms()}

