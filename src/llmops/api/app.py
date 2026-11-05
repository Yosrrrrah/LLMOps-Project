"""Minimal FastAPI application for the foundational runtime."""

from fastapi import FastAPI

from llmops.config import settings
from llmops.utils.logging import configure_logging

configure_logging(settings.log_level)

app = FastAPI(title=settings.app_name, version="0.1.0")


@app.get("/health/live")
def liveness() -> dict[str, str]:
    return {"status": "alive"}


@app.get("/health/ready")
def readiness() -> dict[str, str]:
    return {"status": "ready", "environment": settings.environment}


@app.get("/api/v1/status")
def status() -> dict[str, str]:
    return {"service": settings.app_name, "environment": settings.environment}
