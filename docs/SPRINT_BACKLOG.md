# Sprint Backlog

This backlog defines planned work, not completed work. Each sprint must finish with a reviewed, merged increment. “Expected commits” and “expected pull requests” describe planned Git activity and must not be interpreted as existing repository history.

## Definition of Ready

A task is ready when it has:

- one primary developer;
- explicit acceptance criteria;
- expected source files;
- dependencies;
- required tests;
- a branch name;
- an expected commit sequence;
- a reviewer;

## Definition of Done — all sprints

- Acceptance criteria pass.
- Required unit/integration tests pass.
- No generated model, database or report artifacts are committed unintentionally.
- Documentation matches the implementation.
- The pull request has at least one review from the other developer.
- The sprint increment can be demonstrated without undocumented manual edits.

---

# Sprint 0 — Repository and Engineering Foundation

## Objective

Create the Python repository structure, engineering tooling and CI baseline.

## Developer A tasks

1. Initialize package layout and test configuration.
2. Create primary dependency manifests.
3. Add initial architecture and coding-documentation files.
4. Create test fixture conventions.

### Responsible files

- `pyproject.toml`
- `requirements.txt`
- `requirements-test.txt`
- `requirements-serve.txt`
- `tests/conftest.py`
- `docs/`

### Planned commits

```text
chore(project): initialize Python package layout
chore(deps): define application and test dependencies
test(project): add shared pytest configuration
```

## Developer B tasks

1. Configure repository metadata and ignore rules.
2. Add issue and pull-request templates.
3. Add initial lint and test workflows.
4. Document review and branch conventions.

### Responsible files

- `.gitignore`
- `.github/ISSUE_TEMPLATE/*`
- `.github/pull_request_template.md`
- `.github/workflows/ci.yml`
- `CONTRIBUTING.md`

### Planned commits

```text
chore(repo): add ignore and GitHub templates
ci(repo): add initial lint workflow
ci(repo): add initial unit-test workflow
```

## Task dependencies

- Developer A Python configuration precedes Developer B CI test dependency caching.
- Both branches integrate at the repository-root pull request.

## Integration pull request

- `integration/repository-foundation`
- Required review: both developers.

## Acceptance criteria

- Python 3.11 virtual environment installs dependencies.
- pytest discovers the test directory.
- Ruff accepts or intentionally reports an empty initial codebase.
- CI runs on a pull request and on main.

## Tests before merge

- `python -m pytest`
- `python -m ruff check .`
- GitHub Actions lint/test jobs

---

# Sprint 1 — Configuration, Utilities and Synthetic Data

## Objective

Create centralized configuration, deterministic data, prompts, logs and basic PII masking.

## Developer A tasks

### A1. Configuration and project paths

Implement shared project-root resolution and environment overrides in a dedicated module.

### A2. Dataset generator

Implement deterministic AuroraSync support examples, topics, JSONL utilities and train/validation splitting.

### A3. Prompt utilities

Implement discovery and loading of prompt files and chat-message construction.

### Planned commits

```text
feat(config): load centralized YAML configuration
feat(data): generate deterministic support examples
feat(data): add JSONL read, write and split helpers
test(data): validate data reproducibility and topic coverage
feat(prompts): load and validate prompt versions
```

### Responsible files

- `configs/config.yaml`
- `src/utils/config.py`
- `src/utils/prompts.py`
- `src/data/dataset.py`
- `src/data/__init__.py`
- `tests/test_dataset.py`
- `tests/test_prompts_and_config.py`

## Developer B tasks

### B1. Structured logging

Implement JSON logging with UTC timestamps and preserved non-control fields.

### B2. Basic PII masking

Implement masking for personal email addresses and phone candidates while preserving approved product domains.

### B3. Utility documentation

Document logging and privacy field conventions.

### Planned commits

```text
feat(logging): add JSON formatter and logger helpers
test(logging): validate structured JSON output
feat(pii): mask personal email and phone data
test(pii): cover masking and allowed-domain behavior
```

### Responsible files

- `src/utils/logging_utils.py`
- `src/utils/pii.py`
- `src/utils/__init__.py`
- `tests/test_pii.py`
- `tests/test_prompts_and_config.py`

## Dependencies

- Sprint 0 project layout.
- Developer A creates configuration keys before Developer B validates configuration.
- Developer A dataset contract precedes training implementation in Sprint 2.

## Integration pull requests

- `feature/config-data-utilities` — Developer A
- `feature/logging-pii-utilities` — Developer B
- `integration/foundation-utilities` — final combined review

## Acceptance criteria

- The same seed and sample count produce the same dataset.
- Train and validation rows are disjoint.
- Every keyword expected by a row exists in that row's expected response.
- Unknown prompt versions raise a clear error.
- Email and phone masking occurs before persistence boundaries.
- Relative project paths resolve consistently.

## Tests before merge

- `pytest tests/test_dataset.py`
- `pytest tests/test_prompts_and_config.py`
- `pytest tests/test_pii.py`
- full unit suite and Ruff

---

# Sprint 2 — Training and Model Registry

## Objective

Create a deterministic LoRA training pipeline and register a candidate adapter in MLflow.

## Developer A tasks

### A1. Model loading contract

Implement resolution inputs, source types and loading entry points without coupling evaluation to API code.

### A2. Training CLI

Implement full and smoke profiles, chat tokenization, response-label masking and LoRA configuration.

### A3. Model artifact output

Save adapters and optional merged full models according to configured locations.

### Planned commits

```text
feat(model): add source resolution contracts
feat(training): add LoRA training CLI
feat(training): mask prompt tokens from answer labels
test(training): validate label masking and dataset tokenization
feat(training): expose full and smoke profiles
```

### Responsible files

- `src/train.py`
- `src/model_io.py`
- `tests/test_train_helpers.py`
- `tests/test_gate_registry_model_io.py`

## Developer B tasks

### B1. Registry abstraction

Implement experiment setup, model registration, alias lookup, artifact path remapping and registry availability checks.

### B2. Lightweight registry tests

Use temporary SQLite and registry doubles to keep ordinary tests model-free.

### B3. Runtime registry documentation

Document artifact ownership and host/container path behavior.

### Planned commits

```text
feat(registry): add MLflow experiment setup
feat(registry): register and alias adapters
feat(registry): remap host artifact paths
 test(registry): cover unavailable registry and alias lookup
```

### Responsible files

- `src/registry.py`
- `tests/test_gate_registry_model_io.py`

## Dependencies

- Sprint 1 dataset JSONL contract.
- Sprint 1 prompt loader.
- Registry implementation must precede training registration calls.

## Integration tasks

- Developer A connects training results to registry registration.
- Developer B ensures adapter paths resolve after the training run.
- Integration branch runs the smoke-training pipeline once with a local lightweight configuration.

## Integration pull request

- `feature/model-training`
- `feature/mlflow-registry`
- `integration/training-registry`

## Acceptance criteria

- Smoke training completes with reduced data and configured step count.
- Prompt tokens are excluded from loss using `-100`.
- An MLflow run exists and logs parameters, metrics and artifacts.
- One adapter version receives the `candidate` alias.
- Registry unavailable behavior does not hang indefinitely.

## Tests before merge

- helper, tokenization and label tests;
- registry availability and alias tests;
- a designated smoke-training integration test;
- full unit suite and Ruff.

---

# Sprint 3 — Evaluation and Promotion

## Objective

Implement evaluation metrics, quality gates and safe promotion to production.

## Developer A tasks

### A1. Evaluation loop

Implement a model-independent evaluation function and smoke/full reports.

### A2. Text metrics

Implement dependency-free ROUGE-L, normalized keyword matches and coverage metrics.

### A3. MLflow metric attachment

Attach evaluation metrics to runs and model-version tags.

### Planned commits

```text
feat(evaluation): run validation samples through generated output
feat(metrics): implement ROUGE-L and keyword metrics
feat(evaluation): write machine-readable reports
feat(evaluation): attach metrics to MLflow model versions
```

### Responsible files

- `src/evaluate.py`
- `src/utils/text_metrics.py`
- `tests/test_metrics_eval.py`
- `tests/test_gate_registry_model_io.py`

## Developer B tasks

### B1. Gate decision logic

Implement threshold checks and production-regression comparisons as pure functions.

### B2. Promotion workflow

Validate report freshness and candidate identity, then update production alias and local adapter copy.

### B3. Promotion reporting

Write promotion decision JSON and clear non-zero exit behavior.

### Planned commits

```text
feat(gate): implement quality-gate checks
feat(promotion): validate candidate evaluation report
feat(promotion): update production alias and adapter copy
test(promotion): protect production on failed gates
```

### Responsible files

- `src/gate.py`
- `scripts/promote_model.py`
- `tests/test_gate_registry_model_io.py`

## Dependencies

- Sprint 2 registry candidate alias.
- Sprint 2 resolved adapter directory.
- Evaluation report contract precedes promotion script.

## Acceptance criteria

- Evaluation report identifies the exact candidate version.
- Gate thresholds can be selected for smoke or full mode.
- Production regression cannot exceed configured tolerance.
- Failed gates do not change production alias or local adapter.
- Stale or mismatched evaluation reports fail with exit code two.

## Tests before merge

- text metrics with known strings;
- gate pass/fail/regression cases;
- stale and mismatched report tests;
- successful and failed promotion integration tests;
- full unit suite and Ruff.

## Expected pull requests

- `feature/model-evaluation`
- `feature/quality-gate-promotion`
- `integration/evaluation-promotion`

---

# Sprint 4 — Serving API

## Objective

Serve the production adapter through FastAPI with a fake-backend unit boundary and browser UI.

## Developer A tasks

### A1. Backend lifecycle

Implement model loading resolution, async startup state and serialized generation.

### A2. Backend contract tests

Use fake tokenizer/model objects to test loading and generation separately from HTTP behavior.

### A3. Live adapter integration

Run API startup against a smoke-trained adapter when available.

### Planned commits

```text
feat(backend): load resolved production model in background
feat(backend): serialize generation requests
feat(backend): expose readiness and model metadata
 test(backend): verify generation contract with doubles
```

### Responsible files

- `src/serve/backend.py`
- `src/model_io.py`
- `tests/test_backend.py`
- `tests/test_gate_registry_model_io.py`

## Developer B tasks

### B1. API application

Implement application factory, lifespan startup and health/readiness endpoints.

### B2. HTTP schemas

Implement request validation and response contracts.

### B3. Browser UI

Implement generation and status interface using the API contract.

### Planned commits

```text
feat(api): create FastAPI application factory
feat(api): add health, readiness and generation routes
feat(api): validate generation and feedback request schemas
feat(ui): add support chat interface
 test(api): cover schema and readiness behavior
```

### Responsible files

- `src/serve/app.py`
- `src/serve/schemas.py`
- `src/serve/static/index.html`
- `src/serve/__init__.py`
- `tests/test_api.py`

## Dependencies

- Sprint 3 production adapter resolution.
- API schema must stabilize before UI implementation.

## Acceptance criteria

- API startup succeeds without immediate model loading failure.
- `/health` remains available while loading.
- `/ready` returns 503 until model readiness.
- Generate contract validates range limits.
- Fake backend tests require neither Torch nor the base model.
- Browser can display loading, success and generation failure states.

## Tests before merge

- schema validation;
- fake backend generation;
- loading/not-ready/readiness behavior;
- static page response;
- live smoke-adapter integration;
- full suite and Ruff.

## Expected pull requests

- `feature/serving-backend`
- `feature/serving-api`
- `integration/serving-adapter`

---

# Sprint 5 — Monitoring, Metrics and Feedback

## Objective

Persist requests, collect feedback and expose operational metrics.

## Developer A tasks

### A1. Feedback data contract

Define masked request/response records used for later feedback export.

### A2. Feedback aggregation contract tests

Validate expected feedback count and joined-row formats.

### A3. Retraining-consumption documentation

Document how positive feedback and negative review records differ.

### Planned commits

```text
feat(feedback): define request-feedback export contract
 test(feedback): validate count and joined-row shapes
 docs(feedback): document training-data assumptions
```

### Responsible files

- `src/monitor/store.py` interface expectations
- `scripts/export_feedback.py` contract only if implementation starts
- `tests/test_store_and_triggers.py`
- `docs/`

## Developer B tasks

### B1. SQLite store

Implement request/feedback tables, masks, indexes, busy timeout and upsert behavior.

### B2. Prometheus metrics

Implement counters, histograms and gauges.

### B3. API integration and UI feedback

Record successful requests, expose feedback endpoint and add buttons.

### Planned commits

```text
feat(monitoring): add SQLite request and feedback schema
feat(monitoring): mask prompts before persistence
feat(api): integrate request logging and feedback
test(monitoring): test feedback and request consistency
feat(metrics): expose Prometheus counters and histograms
feat(ui): add feedback controls
```

### Responsible files

- `src/monitor/store.py`
- `src/serve/metrics.py`
- `src/serve/app.py`
- `src/serve/static/index.html`
- `tests/test_store_and_triggers.py`
- `tests/test_api.py`

## Dependencies

- Sprint 4 API response and request ID contract.
- Feedback joining contract precedes Sprint 6 export scripts.

## Acceptance criteria

- Successful generation inserts a request.
- Feedback references only an existing request.
- Feedback can be updated once per request.
- Email address persistence is masked.
- Metrics include request, error, token and feedback series.
- UI feedback reports success/failure distinctly.

## Tests before merge

- store schema and round-trip;
- feedback not-found behavior;
- concurrent-write integration;
- API metric assertions;
- PII persistence assertions;
- full unit suite and Ruff.

## Expected pull requests

- `feature/feedback-contract`
- `feature/monitoring-store-metrics`
- `integration/feedback-api`

---

# Sprint 6 — Drift Detection and Retraining

## Objective

Complete the closed-loop drift and feedback retraining decision.

## Developer A tasks

### A1. Feedback export

Convert thumbs-up feedback into deduplicated training rows and thumbs-down into review records.

### A2. Feedback merging

Merge valid feedback with synthetic data and avoid duplicate request IDs.

### A3. Retraining orchestration

Implement DVC and model pipeline orchestration, including smoke/full flags.

### Planned commits

```text
feat(feedback): export approved feedback examples
feat(feedback): merge and deduplicate training rows
feat(retraining): orchestrate retraining pipeline
 test(feedback): verify export and merge idempotency
```

### Responsible files

- `scripts/export_feedback.py`
- `scripts/merge_feedback.py`
- `scripts/check_and_retrain.py`
- `scripts/dvc_snapshot.py`
- `tests/test_store_and_triggers.py`

## Developer B tasks

### B1. Drift calculations

Implement length KS, token PSI, Jensen-Shannon, out-of-vocabulary and combined drift score.

### B2. Reports and triggers

Generate JSON/HTML output and expose the score through metrics.

### B3. Traffic simulation

Create repeatable normal and shifted traffic for demonstration.

### Planned commits

```text
feat(drift): implement length and distribution statistics
feat(drift): generate JSON and HTML reports
feat(drift): implement threshold trigger decisions
feat(demo): add traffic simulation
 test(drift): cover stable, shifted and insufficient samples
```

### Responsible files

- `src/monitor/drift.py`
- `src/monitor/triggers.py`
- `scripts/simulate_traffic.py`
- `src/serve/metrics.py`
- `tests/test_drift.py`
- `tests/test_store_and_triggers.py`

## Dependencies

- Sprint 5 request and feedback store.
- Developer A merge contract depends on Developer B exact stored prompt/response fields.
- API drift gauge depends on JSON report format.

## Acceptance criteria

- Stable synthetic distributions do not trigger drift in regression seeds.
- Significant length and content shifts trigger drift.
- Insufficient data produces an explicit status instead of a score alarm.
- Retraining trigger supports drift and negative-feedback reasons.
- Dry-run never executes training.
- Export and merge are idempotent.

## Tests before merge

- PSI/JS known-data assertions;
- KS length shift;
- no-false-alarm seeds;
- insufficient-data behavior;
- feedback trigger thresholds;
- export/merge tests;
- simulated traffic integration;
- full suite and Ruff.

## Expected pull requests

- `feature/feedback-retraining`
- `feature/drift-monitoring`
- `integration/closed-loop-retraining`

---

# Sprint 7 — Docker Compose Platform

## Objective

Package and operate the API and supporting infrastructure through Docker Compose.

## Developer A tasks

### A1. Runtime artifact contract

Verify the production adapter layout, model cache and registry fallback in container mounts.

### A2. Container startup tests

Define readiness assertions and generation prompts for runtime validation.

### A3. Container documentation

Document required mount ownership and artifact layout.

### Planned commits

```text
feat(container): validate production adapter mount contract
 test(container): add model startup smoke checks
 docs(container): document runtime model layout
```

### Responsible files

- runtime contract tests
- `Dockerfile` model behavior sections
- `scripts/`
- `README.md`

## Developer B tasks

### B1. Docker image

Create runtime and MLflow stages with non-root runtime execution.

### B2. Compose platform

Create API, MLflow, nginx, Prometheus and Grafana services.

### B3. Observability configuration

Configure scrape targets, provisioning and dashboard.

### Planned commits

```text
feat(docker): add API and MLflow runtime stages
feat(compose): add multi-service platform
feat(proxy): configure nginx replicas
feat(observability): configure Prometheus and Grafana
 test(compose): add platform smoke validation
```

### Responsible files

- `Dockerfile`
- `.dockerignore`
- `docker-compose.yml`
- `nginx/nginx.conf`
- `monitoring/prometheus.yml`
- `monitoring/grafana/*`

## Dependencies

- Sprint 4 runtime backend.
- Sprint 5 metrics.
- Sprint 6 drift report.
- Production adapter artifact or model resolution fallback.

## Acceptance criteria

- API container starts and reaches readiness or reports an explicit startup failure.
- Two API replicas answer through nginx.
- MLflow, Prometheus and Grafana are reachable.
- Prometheus finds both API targets where applicable.
- Container runtime executes as non-root.
- Monitoring data uses mounted writable storage.

## Tests before merge

- Docker build;
- container health/readiness;
- container generation;
- Compose startup;
- two-replica nginx test;
- Prometheus target test;
- Grafana and MLflow health;
- full unit suite and Ruff.

## Expected pull requests

- `ops/container-model-mounts`
- `ops/docker-compose-platform`
- `integration/compose-validation`

---

# Sprint 8 — CI/CD

## Objective

Automate repository validation, model smoke work, deployment smoke work and image publication.

## Developer A tasks

### A1. Pipeline integration

Create model/data smoke commands suitable for CI.

### A2. Promotion artifact validation

Upload or validate production adapter artifacts only after gate success.

### A3. Pipeline diagnostics

Document and test report artifact collection.

### Planned commits

```text
ci(pipeline): add data and model smoke stage
ci(pipeline): validate and publish promotion artifacts
ci(pipeline): retain reports for failures
```

### Responsible files

- `.github/workflows/ci.yml`
- `Makefile`
- evaluation/promotion scripts

## Developer B tasks

### B1. CI jobs

Create lint, unit, Docker and Compose jobs.

### B2. CD workflow

Publish runtime images on semantic tags to GHCR.

### B3. Permissions and caches

Limit permissions, add model cache and avoid undocumented secrets.

### Planned commits

```text
ci(repo): add lint and unit-test jobs
ci(deploy): add Docker smoke validation
ci(deploy): add Compose integration validation
ci(release): publish runtime image for semantic tags
```

### Responsible files

- `.github/workflows/ci.yml`
- `.github/workflows/cd.yml`

## Dependencies

- Sprint 7 proven Docker and Compose commands.
- Sprint 3 promotion report behavior.
- Sprint 6 drift and traffic commands.

## Acceptance criteria

- Pull request runs lint and unit tests.
- Pipeline runs smoke data, training, evaluation and promotion.
- Docker smoke consumes a valid production adapter artifact.
- Compose validates two replicas.
- Semantic tag publishes the runtime image.
- Workflow uses the minimum required permissions.

## Tests before merge

- workflow syntax validation;
- lint job;
- unit-test job;
- model smoke job;
- Docker job;
- Compose job;
- deliberate failure test;
- semantic-tag publication rehearsal.

## Expected pull requests

- `ci/model-pipeline`
- `ci/deployment-pipeline`
- `ci/end-to-end`

---

# Sprint 9 — Kubernetes

## Objective

Add deployable Kubernetes resources and define persistent artifact requirements.

## Developer A tasks

### A1. Kubernetes startup contract

Ensure startup and readiness expose resolved model/prompt identity.

### A2. Artifact packaging

Define production adapter and cache mount strategy.

### A3. Kubernetes documentation

Document model-source fallback and restart behavior.

### Planned commits

```text
feat(kubernetes): document and expose startup artifact contract
fix(kubernetes): make startup adapter resolution explicit
 docs(kubernetes): add kind/minikube runbook
```

### Responsible files

- model resolution files
- startup tests
- `docs/kubernetes.md`

## Developer B tasks

### B1. Kubernetes manifests

Create Deployment, Service, HPA and Kustomization resources.

### B2. Probes and security

Configure startup/readiness/liveness, resources, non-root identity and metrics annotations.

### B3. Persistence strategy

Define persistent cache and production artifact strategy rather than relying on ephemeral emptyDir forever.

### Planned commits

```text
feat(kubernetes): add API deployment and service
feat(kubernetes): add probes and CPU HPA
feat(kubernetes): add model storage strategy
 test(kubernetes): validate manifests and service health
```

### Responsible files

- `k8s/deployment.yaml`
- `k8s/service.yaml`
- `k8s/hpa.yaml`
- `k8s/kustomization.yaml`

## Dependencies

- Sprint 8 container runtime image.
- Sprint 4 readiness contract.
- Metrics-server availability for HPA runtime tests.

## Acceptance criteria

- Kustomize resources validate.
- Pods become ready only after model loading.
- Service routes only ready replicas.
- HPA configuration references the Deployment.
- Runtime non-root UID does not conflict with mounted storage.
- Persistent artifact approach is documented and demonstrated or acknowledged as deployment configuration.

## Tests before merge

- manifest dry validation;
- kind/minikube apply;
- readiness and liveness behavior;
- service generation;
- HPA scale behavior;
- rolling restart;
- full suite and Ruff.

## Expected pull requests

- `ops/kubernetes-artifacts`
- `ops/kubernetes-manifests`
- `integration/kubernetes-validation`

---

# Sprint 10 — Hardening and Release

## Objective

Produce a secure, reproducible and defensible release candidate.

## Developer A tasks

- Add authentication boundary abstractions or explicit local-only deployment safeguards.
- Improve model lifecycle failure and rollback documentation.
- Complete safety, evaluation and promotion review checklist.
- Document individual model-lifecycle defense areas.

### Planned commits

```text
sec(model): define API identity boundary
feat(governance): document promotion and rollback checks
 docs(model): complete model lifecycle guide
```

### Responsible files

- API identity integration files agreed with Developer B
- model lifecycle documentation
- promotion and rollback tests

## Developer B tasks

- Add API abuse/rate-limit behavior or clearly documented test boundary.
- Review monitoring persistence, retention, credentials and backups.
- Complete architecture, operations and fresh-machine setup guide.
- Prepare infrastructure release rehearsal.

### Planned commits

```text
sec(api): add rate-limit configuration
ops(monitoring): document retention and backup strategy
 docs(operations): complete architecture and runbook
 test(release): add final release rehearsal checks
```

### Responsible files

- FastAPI protection configuration
- infrastructure documentation
- deployment credentials and config review
- release test scripts

## Dependencies

- All previous sprint increments merged.
- Documentation must reflect actual code behavior.

## Acceptance criteria

- No default production credentials or undocumented secrets.
- Public API boundary is explicitly protected or local-only.
- High-risk privacy gaps are documented.
- Architecture diagrams match runtime components.
- Fresh setup instructions pass on a clean environment.
- Both developers can run a complete demonstration.

## Tests before merge

- full unit suite;
- API integration suite;
- container/Compose suite;
- smoke training/evaluation/promotion suite;
- drift simulation;
- security configuration validation;
- Kubernetes smoke where resources are available;
- final release rehearsal.

## Expected pull requests

- `hardening/model-governance`
- `hardening/service-operations`
- `release/v1.0`

---

# Backlog summary by developer

## Developer A primary backlog

| Sprint | Focus |
|---|---|
| 0 | Python packages and test configuration |
| 1 | Configuration, data and prompts |
| 2 | Training and model loading |
| 3 | Evaluation and metrics |
| 4 | Backend lifecycle |
| 5 | Feedback data contract |
| 6 | Feedback export and merge |
| 7 | Container artifact contract |
| 8 | Model pipeline CI |
| 9 | Kubernetes model startup |
| 10 | Model governance and release |

## Developer B primary backlog

| Sprint | Focus |
|---|---|
| 0 | Repository/CI foundation |
| 1 | Logging and PII |
| 2 | Registry and artifact paths |
| 3 | Quality gate and promotion |
| 4 | API and UI |
| 5 | SQLite, metrics and feedback |
| 6 | Drift, reports and triggers |
| 7 | Docker and Compose |
| 8 | Deployment CI/CD |
| 9 | Kubernetes manifests |
| 10 | Security and operations |

## Sprint-level integration ownership

1. S0 repository merge is joint.
2. S1 configuration, prompts and logging integration requires both.
3. S2 training/registry integration is a joint smoke pipeline.
4. S3 evaluation/promotion integration tests gate behavior.
5. S4 backend/API integration validates real model startup.
6. S5 request/feedback integration validates persistence and UI.
7. S6 feedback/drift integration validates closed-loop decisions.
8. S7 container/model integration validates runtime artifact access.
9. S8 all pipeline stages must use shared CI contracts.
10. S9 model startup and Kubernetes probes require both owners.
