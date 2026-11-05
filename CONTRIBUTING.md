# Contributing

## Development model

This repository uses a two-developer Git workflow based on `develop` and short-lived topic branches.

- `main` contains release-ready code.
- `develop` contains reviewed work accepted for the next release.
- `main` is updated from `develop` only for a validated release.
- Feature, fix, operations, documentation, test and integration work starts from `develop` unless a release process explicitly says otherwise.

No current commit, branch, contribution or release is assumed to exist merely because it is described in this document.

## Environment

Use Python 3.11 unless project documentation specifies a later supported version.

Before starting work:

```bash
git switch develop
git pull --ff-only origin develop
python -m venv .venv
```

Use project-specific setup commands from the README when those commands exist. Do not commit virtual environments, generated models, databases, credentials or local reports.

## Developer branches

Developer A uses:

```text
<type>/a/<short-description>
```

Developer B uses:

```text
<type>/b/<short-description>
```

Examples:

```text
feature/a/synthetic-dataset
feature/b/fastapi-generation
fix/a/artifact-path-resolution
ops/b/docker-compose-platform
docs/a/model-lifecycle
```

Shared integration work uses:

```text
integration/<short-description>
```

## Commit convention

Every commit uses Conventional Commits:

```text
<type>(<scope>): <imperative summary>
```

Allowed types include:

- `feat`
- `fix`
- `docs`
- `test`
- `chore`
- `ci`
- `ops`
- `refactor`
- `perf`
- `revert`

Examples:

```text
docs(git): add collaborative workflow
docs(git): add GitHub issue templates
feat(data): generate deterministic support examples
test(data): validate split invariants
fix(registry): remap container artifact paths
ci(test): run unit tests on pull requests
```

Prefer one logical change per commit. Explain why a non-obvious change is needed in the body when necessary.

## Pull Request process

1. Create or select a GitHub Issue before implementation.
2. Create a branch from the current `develop`.
3. Implement and test the issue.
4. Push the branch.
5. Open a pull request into `develop`.
6. Complete the PR template.
7. Ensure required status checks pass.
8. Obtain at least one approval from the other developer.
9. Resolve comments and merge using Squash and Merge for normal work.
10. Delete the topic branch after merge.

Pull requests must:

- link the issue;
- state the implementation approach;
- identify acceptance criteria;
- list tests run;
- identify files owned by the other developer that were affected;
- call out configuration, security, privacy and deployment impact;
- avoid generated artifacts unless an issue explicitly requires them.

## Code review rules

The repository is restricted to two developers, so every PR requires one reviewer who is not the author.

Review comments are categorized as:

- **blocking**: correctness, security, privacy, test, API-contract or release risk;
- **suggestion**: optional improvement;
- **question**: clarification required before approval;
- **nit**: style or presentation, must not block on its own.

Authors must reply to every blocking comment and every unresolved review thread. Reviewers must not approve work they have not reasonably examined.

## Testing expectations

Run the smallest relevant test set during development, then the broader suite before requesting final review.

Examples:

```bash
python -m pytest tests/test_dataset.py
python -m ruff check .
python -m pytest
```

Infrastructure changes require the tests documented in the related sprint backlog, such as container or Compose smoke checks.

## Merge strategy

Use **Squash and Merge** for normal topic branches. This creates one reviewed change on `develop` with a Conventional Commit-formatted PR title.

Use **Merge Commit** only for an explicit integration or release branch where retaining the individual commit sequence has operational value.

Use rebase only to update a personal topic branch before opening or updating a pull request. Do not rewrite commits that have already been merged.

## Generated files

Generated files must be kept out of source commits unless explicitly required for a reproducible, reviewed artifact. Typical exclusions include:

- virtual environments;
- model caches and downloaded weights;
- MLflow databases and artifacts;
- SQLite monitoring data;
- generated reports;
- local DVC storage;
- credentials and environment files.

## Issues and labels

Create one GitHub Issue for every planned behavior, bug, operation, documentation or CI change. Apply labels for type, priority and sprint or component when the repository labels exist.

Recommended baseline labels:

```text
feature, bug, documentation, infrastructure, ci,
test, model, data, api, monitoring, security,
priority: high, priority: medium, priority: low,
sprint: 00 ... sprint: 10
```

## Documentation

Architectural and operational behavior changes require documentation updates in the same pull request. Do not document a branch, commit, merge, CI run or release as complete unless that GitHub state actually exists.
