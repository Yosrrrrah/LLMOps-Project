# LLMOps Platform Foundation

This repository contains the initial, intentionally minimal foundation for an incrementally developed LLMOps platform. It provides application configuration, structured logging, health endpoints, Python packaging, automated tests, and linting. Model lifecycle, training, inference, monitoring, and deployment features are added in later approved sprints.

## Requirements

- Python 3.11 or newer
- pip or another standards-compatible Python package installer

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
Copy-Item .env.example .env
```

## Run the API

```powershell
python -m llmops
```

The service is available at `http://127.0.0.1:8000`. Open the interactive API documentation at `http://127.0.0.1:8000/docs`.

Health endpoints:

- `GET /health/live`
- `GET /health/ready`
- `GET /api/v1/status`

## Verify the foundation

```powershell
python -m pytest
python -m ruff check .
python -m ruff format --check .
```

## Project layout

```text
src/llmops/       Installable application package
  api/            FastAPI application and routes
  utils/          Shared logging and future utilities
configs/          Runtime configuration added in later sprints
prompts/          Versioned prompts added in later sprints
scripts/          Operational automation
tests/unit/       Deterministic unit tests
tests/integration/ Service and cross-component tests
 docs/            Architecture, roadmap, and team documentation
```

See `docs/SYSTEM_ARCHITECTURE.md`, `docs/DEVELOPMENT_ROADMAP.md`, and `docs/GIT_WORKFLOW.md` before adding implementation work. Generated models, databases, reports, credentials, and local environments must not be committed.
