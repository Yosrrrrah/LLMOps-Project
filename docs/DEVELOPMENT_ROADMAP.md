# Development Roadmap

## Delivery assumptions

- Sprint length: two weeks.
- Team size: two developers.
- Average workload: approximately eight story points per developer per sprint.
- One primary owner per source file.
- Pull-request reviews are performed by the non-owner.
- Model/GPU work is scheduled after deterministic unit contracts stabilize.

## Sprint sequence

| Sprint | Increment | Primary result |
|---|---|---|
| 0 | Repository foundation | Reproducible project skeleton and CI baseline |
| 1 | Configuration and data | Deterministic data, prompts, logging and PII utilities |
| 2 | Training and registry | Smoke-trained candidate registered in MLflow |
| 3 | Evaluation and promotion | Machine-readable gate and production adapter |
| 4 | Inference service | Browser and API generation service |
| 5 | Monitoring and feedback | SQLite, metrics and feedback UI |
| 6 | Drift and retraining | Closed monitoring and retraining decision loop |
| 7 | Docker Compose | Multi-service local platform |
| 8 | CI/CD | Automated pipeline validation and image publication |
| 9 | Kubernetes | Deployable manifests and resilient startup |
| 10 | Hardening | Security review, release rehearsal and documentation |

## Critical path

```text
S0 repository
→ S1 contracts and data
→ S2 training and registry
→ S3 evaluation and promotion
→ S4 serving
→ S5 monitoring/feedback
→ S6 drift/retraining
→ S7 Compose
→ S8 CI/CD
→ S9 Kubernetes
→ S10 release hardening
```

## Milestone 1 — Foundation

### Sprints 0–1

**Outcome:** A clean checkout creates an environment, produces reproducible data, validates prompts, emits structured logs and masks basic PII.

**Exit criteria:**

- Lint passes.
- Unit tests discover and pass.
- Data generated twice from the same seed is identical.
- Documentation identifies ownership for initial modules.

## Milestone 2 — Model lifecycle

### Sprints 2–3

**Outcome:** A smoke model is trained, registered, evaluated and promoted through reproducible gates.

**Exit criteria:**

- Candidate alias exists in a temporary or local MLflow database.
- Evaluation report and promotion report are schema-valid JSON.
- Failed gate does not alter production alias.
- Production adapter can be loaded locally.

## Milestone 3 — Model service

### Sprints 4–5

**Outcome:** The model and browser UI run through an API; generation requests and feedback are persisted and exposed as metrics.

**Exit criteria:**

- Model-free API tests pass.
- Live smoke-adapter generation passes.
- Feedback references a known request.
- Persisted prompts have masked email addresses and phone numbers.

## Milestone 4 — Managed monitoring

### Sprint 6

**Outcome:** Shifted traffic produces a documented drift report, and feedback/drift triggers can initiate a retraining decision.

**Exit criteria:**

- Same-distribution windows do not alarm in the agreed regression tests.
- Shifted traffic alarms and produces JSON/HTML reports.
- Retraining decision is deterministic and supports dry-run.

## Milestone 5 — Platform delivery

### Sprints 7–9

**Outcome:** The complete platform runs in Docker Compose and has CI/CD and Kubernetes delivery resources.

**Exit criteria:**

- Two API replicas answer through nginx.
- Prometheus discovers expected targets.
- Grafana and MLflow are healthy.
- Containers run as non-root.
- Kubernetes resources apply and probes reach the correct readiness endpoint.

## Milestone 6 — Release

### Sprint 10

**Outcome:** A documented, rehearsed release candidate with recorded limitations and defense material.

**Exit criteria:**

- Fresh checkout setup is successful.
- All required release checks pass.
- Public deployment boundaries are documented.
- Architecture documentation matches code.

## Workflow guardrails

1. Start implementation only after interface and file ownership are agreed.
2. Keep expensive model tests in designated integration targets.
3. Merge data contracts before dependent training code.
4. Merge fake-backend API code before real-model integration.
5. Merge monitoring storage before drift report integration.
6. Merge container runtime before Compose orchestration.
7. Merge CI only after underlying smoke commands are proven locally.
8. Merge Kubernetes artifacts only after container behavior is stable.

## Stop conditions

Work should stop and be escalated when:

- a quality gate cannot be reproduced locally;
- a registry artifact cannot be resolved outside its original machine;
- shared monitoring writes are unreliable under replicas;
- model loading exceeds the documented startup budget;
- security or privacy boundaries are unresolved;
- CI depends on undocumented external credentials.
