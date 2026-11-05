# Foundation Architecture

## Scope

Sprint 0 established the executable service foundation. Sprint 1 adds centralized configuration, deterministic synthetic support data, JSONL storage helpers, and versioned prompt loading. Model loading, training, registry integration, generation, and monitoring remain future work.

## Runtime boundaries

```text
process entry point
  -> YAML configuration with environment overrides
  -> JSON logging
  -> FastAPI application factory
  -> health and status routes

dataset configuration
  -> deterministic AuroraSync examples
  -> JSONL serialization
  -> seeded train/validation split

prompt version + user instruction
  -> versioned prompt loader
  -> system/user chat messages
```

`python -m llmops` and the `llmops-api` console script both enter the same application runner. Tests import the FastAPI application directly, avoiding a required server subprocess.

## Configuration contract

`src/llmops/config.py` loads `configs/config.yaml` and applies `LLMOPS_` environment overrides. Environment values take precedence over YAML values, which take precedence over defaults. Relative data and prompt directories resolve from the project root; absolute paths remain absolute. `Settings.from_environment` validates ports, sample count, validation fraction, and log level before the API or data utilities use those values.

## Dataset contract

`src/llmops/data/dataset.py` produces immutable support examples with the JSONL keys `id`, `topic`, `instruction`, `response`, and `keywords`. Generation is deterministic for a given sample count and seed. The train/validation splitter uses a separate seed, requires unique IDs, and returns disjoint sets while preserving source order within each result. JSONL parsing reports the source file and line for invalid rows. The `llmops-generate-data` command writes configured `train.jsonl` and `validation.jsonl` files to the configured data directory.

## Prompt contract

Versioned prompts are stored as `prompts/v<number>.txt`. `src/llmops/utils/prompts.py` discovers versions, loads an explicit or configured default version, and combines it with an instruction as system and user chat messages. Unknown versions raise `PromptVersionNotFoundError`; prompt content is not fetched from a network service.

## Subsequent boundaries

- Sprint 2 adds training and MLflow registry adapters.
- Sprint 3 adds evaluation, quality gates, and promotion.
- Sprint 4 adds the model backend and generation routes.
- Sprint 5 adds persistent monitoring, feedback, and metrics.
- Sprint 6 adds drift and retraining decisions.
- Later sprints add container, CI/CD, and Kubernetes delivery.

## Configuration principles

Environment variables are prefixed with `LLMOPS_` and are converted at startup. Invalid configuration fails with a clear error instead of being silently accepted. Real registry URLs and credentials must be supplied through local environment files or deployment secrets, never source control.

## Testability

The foundation separates:

- package configuration from runtime behavior;
- application construction from server startup;
- health reporting from future model readiness;
- synthetic data generation and prompt loading from model dependencies;
- deterministic unit tests from integration tests and expensive model tests.
