"""Unit tests for environment configuration."""

from llmops.config import Settings


def test_invalid_port(monkeypatch) -> None:
    monkeypatch.setenv("LLMOPS_PORT", "not-a-number")
    try:
        Settings.from_environment()
    except ValueError as exc:
        assert "LLMOPS_PORT" in str(exc)
    else:
        raise AssertionError("Expected invalid LLMOPS_PORT to fail")


def test_valid_environment(monkeypatch) -> None:
    monkeypatch.setenv("LLMOPS_APP_NAME", "TestLLMOps")
    monkeypatch.setenv("LLMOPS_PORT", "9000")
    settings = Settings.from_environment()
    assert settings.app_name == "TestLLMOps"
    assert settings.port == 9000
