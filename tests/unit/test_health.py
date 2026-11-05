"""Unit tests for foundational HTTP endpoints."""


def test_liveness(client) -> None:
    response = client.get("/health/live")
    assert response.status_code == 200
    assert response.json() == {"status": "alive"}


def test_readiness(client) -> None:
    response = client.get("/health/ready")
    assert response.status_code == 200
    assert response.json()["status"] == "ready"


def test_status(client) -> None:
    response = client.get("/api/v1/status")
    assert response.status_code == 200
    assert response.json()["service"] == "LLMOps"
