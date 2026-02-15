"""Tests for /api/version."""

from __future__ import annotations


def test_version_uses_environment_variables(client, monkeypatch):
    monkeypatch.setenv("COMMIT_SHA", "abc123")
    monkeypatch.setenv("BUILD_TIME", "2026-02-15T00:00:00Z")
    monkeypatch.setenv("ENVIRONMENT", "prod")

    response = client.get("/api/version")

    assert response.status_code == 200
    assert response.json() == {
        "commit": "abc123",
        "build_time": "2026-02-15T00:00:00Z",
        "environment": "prod",
    }


def test_version_uses_safe_defaults_when_missing_env(client, monkeypatch):
    monkeypatch.delenv("COMMIT_SHA", raising=False)
    monkeypatch.delenv("BUILD_TIME", raising=False)
    monkeypatch.delenv("ENVIRONMENT", raising=False)

    response = client.get("/api/version")

    assert response.status_code == 200
    assert response.json() == {
        "commit": "unknown",
        "build_time": "unknown",
        "environment": "dev",
    }

