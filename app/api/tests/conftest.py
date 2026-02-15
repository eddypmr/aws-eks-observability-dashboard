"""Pytest fixtures for API tests."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from api_service.app import app


@pytest.fixture()
def client() -> TestClient:
    with TestClient(app, raise_server_exceptions=False) as test_client:
        yield test_client

