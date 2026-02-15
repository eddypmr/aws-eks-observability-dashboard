"""Tests for /api/status."""

from __future__ import annotations


def test_status_endpoint_returns_random_latency(client):
    response = client.get("/api/status")
    payload = response.json()

    assert response.status_code == 200
    assert payload["up"] is True
    assert isinstance(payload["latency_ms"], int)
    assert 1 <= payload["latency_ms"] <= 500

