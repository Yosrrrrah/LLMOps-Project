# Team Responsibilities

## Developer A — Model and Data Platform

### Primary ownership

- `src/data/`
- `src/train.py`
- `src/evaluate.py`
- `src/gate.py`
- `src/registry.py`
- `src/model_io.py`
- `src/utils/prompts.py`
- `src/utils/text_metrics.py`
- training and promotion scripts
- feedback-to-training-data scripts
- model lifecycle tests

### Expected strengths and responsibilities

- Dataset design and reproducibility.
- Hugging Face model loading.
- LoRA and optimization behavior.
- MLflow experiment and registry contracts.
- Evaluation metrics and quality gates.
- Production-model selection and artifact export.
- Training data derived from feedback.
- Model lifecycle documentation.

## Developer B — Service and Operations Platform

### Primary ownership

- `src/serve/`
- `src/monitor/store.py`
- `src/monitor/drift.py`
- `src/monitor/triggers.py`
- `src/utils/config.py`
- `src/utils/logging_utils.py`
- `src/utils/pii.py`
- Docker and Compose files
- `nginx/`
- `monitoring/`
- `k8s/`
- `.github/workflows/`
- API, drift and infrastructure tests

### Expected strengths and responsibilities

- FastAPI request contracts and browser UI.
- SQLite persistence and concurrency behavior.
- Prometheus and Grafana integration.
- Statistical drift reports and operational triggers.
- Container and orchestration design.
- CI/CD and deployment validation.
- Service runtime documentation.

## Integration ownership

Some tasks are intentionally owned by one developer with interface review from the other:

| Integration | Primary implementer | Required reviewer |
|---|---|---|
| Dataset to training | Developer A | Developer B |
| Production adapter to backend | Developer A and B | Both |
| API response to SQLite logging | Developer B | Developer A |
| Feedback to retraining data | Developer A and B | Both |
| Drift report to metrics | Developer B | Developer A |
| Production model image | Developer A and B | Both |
| Compose to CI | Developer B | Developer A |
| Kubernetes artifact startup | Developer A and B | Both |

## Shared-file rule

Shared files must be assigned a primary owner before editing starts. Examples include:

- `configs/config.yaml`
- `Makefile`
- `README.md`
- `docker-compose.yml`
- tests that exercise multiple modules

For shared files, the owner creates the first implementation and the other developer reviews and proposes changes through the pull request. No developer should force-push over the other developer's work.

## Sprint accountability

Each sprint backlog must identify:

- Developer A tasks.
- Developer B tasks.
- file ownership.
- task dependencies.
- integration branches.
- commits expected before merge.
- pull requests and required reviewers.

## Individual defense areas

### Developer A should defend

1. LoRA tokenization and label masking.
2. Dataset reproducibility and split integrity.
3. MLflow run and alias lifecycle.
4. Evaluation metric validity.
5. Quality-gate correctness and stale-report prevention.
6. Production fallback resolution.
7. Feedback-data transformation.

### Developer B should defend

1. API lifecycle and readiness semantics.
2. Backend concurrency and failure isolation.
3. Monitoring schema and feedback consistency.
4. PII masking limitations.
5. Drift calculation and report generation.
6. Container and replica orchestration.
7. CI/CD dependency and artifact flow.

## Review rotation

- Developer A reviews Developer B's serving, infrastructure and test pull requests.
- Developer B reviews Developer A's training, registry and data pull requests.
- Integration pull requests require both developers and a final sprint demonstration.
