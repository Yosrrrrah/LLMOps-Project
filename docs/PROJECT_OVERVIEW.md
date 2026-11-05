# Project Overview

## Purpose

This project is a two-person engineering exercise to build, from an empty repository, a complete local LLMOps platform for the fictional customer-support assistant **AuroraSync Support**.

The implementation must demonstrate the complete lifecycle of a small language model:

1. Generate a reproducible support dataset.
2. Fine-tune a small open model with parameter-efficient LoRA adapters.
3. Record experiments and artifacts in MLflow.
4. Evaluate the candidate model.
5. Promote only candidates that satisfy configured quality gates.
6. Serve production inference through FastAPI.
7. Record requests, feedback and operational metrics.
8. Detect distribution drift.
9. Trigger retraining using configurable thresholds.
10. Package and operate the system with Docker, Docker Compose, CI/CD and Kubernetes manifests.

This plan describes intended future work. It does not claim that repository history or implementation exists yet.

## Target architecture

```text
Synthetic/support datasets
        |
        v
LoRA training + MLflow
        |
        v
Evaluation + quality gate
        |
        v
Production adapter/model resolution
        |
        v
nginx + FastAPI API replicas
        |
        +--> SQLite request and feedback store
        +--> Prometheus metrics
        +--> JSON/HTML drift reports
        |
        v
Feedback processing and retraining trigger
```

## Scope

### In scope

- Python 3.11 application source and utilities.
- Hugging Face base-model download and local cache.
- LoRA training and smoke/full training profiles.
- MLflow experiment tracking and Model Registry aliases.
- Deterministic synthetic dataset and versioned prompts.
- Evaluation metrics, quality gate and production promotion.
- FastAPI generation API, readiness endpoints and browser UI.
- SQLite monitoring storage and basic PII masking.
- Prometheus metrics and Grafana dashboards.
- Drift calculation and retraining decision automation.
- Dockerfile, Docker Compose, nginx and Kubernetes resources.
- GitHub Actions CI/CD.
- Unit, integration and deployment validation.

### Out of initial scope

- A paid external LLM API.
- Multi-tenant customer accounts.
- Enterprise identity federation.
- A production-grade clinical/legal/compliance model approval system.
- A distributed database for monitoring data.
- Streaming generation.
- Vector retrieval or an external knowledge base.

## Engineering principles

- Every sprint must finish with a runnable, testable increment.
- Configuration is centralized in `configs/config.yaml`.
- Interfaces are stabilized before dependent implementation starts.
- No developer should edit another developer's files simultaneously.
- Unit tests must be local and deterministic.
- Model downloads and GPU-dependent tests must be isolated from ordinary unit tests.
- Monitoring and model-loading failures must not invalidate core serving contracts unexpectedly.
- Documentation must describe implemented behavior, not aspirations, at the end of each sprint.

## Two-person delivery model

- **Developer A** owns the model/data lifecycle: data, training, registry, evaluation, promotion and retraining-data preparation.
- **Developer B** owns service and operations: API, monitoring store, metrics, UI, drift presentation, containers, CI/CD and Kubernetes.
- Cross-cutting contracts are developed by the owner, reviewed by the other developer, and integrated through a dedicated integration branch when required.

## Success definition

The project is successful when a reviewer can clone an empty or tagged repository, follow the documented setup, generate a dataset, run a smoke training/evaluation/promotion cycle, start the API and execute the monitoring/feedback/drift loop.

The final delivery must include documented limitations and distinguish demonstration infrastructure from production-ready infrastructure.
