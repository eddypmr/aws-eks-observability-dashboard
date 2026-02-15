"""Tests for global error handling."""

from __future__ import annotations

from api_service.routers import status as status_router


def test_unhandled_exception_returns_uniform_500(client, monkeypatch):
    def _raise_error() -> int:
        raise RuntimeError("forced failure")

    monkeypatch.setattr(status_router, "get_latency_ms", _raise_error)

    response = client.get("/api/status")

    assert response.status_code == 500
    assert response.json() == {
        "error": {"message": "Internal Server Error", "status_code": 500}
    }


def test_not_found_uses_uniform_http_error_payload(client):
    response = client.get("/api/does-not-exist")

    assert response.status_code == 404
    assert response.json() == {"error": {"message": "Not Found", "status_code": 404}}

