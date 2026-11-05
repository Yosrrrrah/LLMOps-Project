# Foundation Architecture

## Scope

Sprint 0 establishes executable boundaries only. It does not implement model loading, training, registry integration, inference, monitoring, or data generation.

## Runtime boundaries

```text
process entry point
  -> configuration
  -> JSON logging
  -> FastAPI application factory
  -> health and status routes
```

`python -m llmops` and the `llmops-api` console script both enter the same application runner. Tests import the FastAPI application directly, avoiding a required server subprocess.

## Subsequent boundaries

- Sprint 1 adds configuration, data, prompts, logging, and PII utilities.
- Sprint 2 adds training and MLflow registry adapters.
- Sprint 3 adds evaluation, quality gates, and promotion.
- Sprint 4 adds the model backend and generation routes.
- Sprint 5 adds persistent monitoring, feedback, and metrics.
- Sprint 6 adds drift and retraining decisions.
- Later sprints add container, CI/CD, and Kubernetes delivery.

## Configuration principles

Environment variables are prefixed with `LLMOPS_` and are converted at startup. Invalid ports fail with a clear configuration error instead of being silently accepted. Real registry URLs and credentials must be supplied through local environment files or deployment secrets, never source control.

## Testability

The foundation separates:

- package configuration from runtime behavior;
- application construction from server startup;
- health reporting from future model readiness;
- deterministic unit tests from integration tests and expensive model tests.
