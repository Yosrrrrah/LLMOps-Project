"""Application configuration loaded from environment variables."""

import os
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Settings:
    app_name: str = "LLMOps"
    environment: str = "local"
    host: str = "127.0.0.1"
    port: int = 8000
    log_level: str = "INFO"

    @classmethod
    def from_environment(cls) -> "Settings":
        return cls(
            app_name=os.getenv("LLMOPS_APP_NAME", "LLMOps"),
            environment=os.getenv("LLMOPS_ENVIRONMENT", "local"),
            host=os.getenv("LLMOPS_HOST", "127.0.0.1"),
            port=_port_from_environment(),
            log_level=os.getenv("LLMOPS_LOG_LEVEL", "INFO").upper(),
        )


def _port_from_environment() -> int:
    raw_port = os.getenv("LLMOPS_PORT", "8000")
    try:
        port = int(raw_port)
    except ValueError as exc:
        raise ValueError("LLMOPS_PORT must be an integer") from exc
    if not 1 <= port <= 65535:
        raise ValueError("LLMOPS_PORT must be between 1 and 65535")
    return port


settings = Settings.from_environment()
