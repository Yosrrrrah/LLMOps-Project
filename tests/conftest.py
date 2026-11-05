"""Shared pytest fixtures."""

import pytest
from fastapi.testclient import TestClient

from llmops.api.app import app


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)
