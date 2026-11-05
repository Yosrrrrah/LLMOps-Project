# Git and GitHub Workflow

## Repository state

This document defines the intended workflow. It must not be interpreted as evidence that any commit, branch, pull request, review, CI run or release already exists.

## Repository initialization

The planned initial repository operations are:

```bash
git init -b main
# Connect the repository only after the GitHub URL is approved.
git remote add origin <approved-github-url>
git add CONTRIBUTING.md docs/GIT_WORKFLOW.md .github/
git commit -m "docs(git): establish collaborative workflow"
git push -u origin main
```

### Command explanation

- `git init -b main` creates a repository whose default branch is `main`.
- `git remote add origin` stores the approved GitHub repository address under the name `origin`.
- `git add` stages only collaboration files selected for the initial commit.
- `git commit` creates the initial local commit.
- `git push -u origin main` publishes the commit and sets `main` to track the remote branch.

If GitHub is initialized with a README before local work begins, clone that repository and adapt the initial commit rather than creating a parallel history.

## Persistent branches

### `main`

- contains release-ready code only;
- accepts reviewed pull requests;
- has direct push and force-push disabled;
- receives normal implementation work only through a release pull request.

Create and publish `develop` after confirming the initial `main` baseline:

```bash
git switch -c develop
git push -u origin develop
```

- `develop` is the integration branch for accepted work;
- topic branches start from `develop`;
- `develop` receives pull requests, not unreviewed direct pushes.

## Developer branches

Developer A branches begin with the developer identifier `a`:

```text
<type>/a/<short-description>
```

Developer B branches begin with `b`:

```text
<type>/b/<short-description>
```

Examples:

```bash
git switch develop
git pull --ff-only origin develop
git switch -c feature/a/synthetic-dataset

git switch develop
git pull --ff-only origin develop
git switch -c feature/b/fastapi-generation
```

Shared work uses:

```text
integration/<short-description>
release/<major.minor.patch>
```

## Branch naming rules

| Prefix | Purpose |
|---|---|
| `feature/` | New behavior |
| `fix/` | Defect correction |
| `test/` | Test-only work |
| `docs/` | Documentation |
| `ops/` | Container, deployment or infrastructure |
| `ci/` | GitHub Actions and automation |
| `refactor/` | Behavior-preserving refactor |
| `integration/` | Cross-developer integration |
| `release/` | Release preparation |
| `hotfix/` | Urgent production correction |

Rules:

- lowercase names;
- hyphens between words;
- short descriptive names;
- personal branches include `a` or `b`;
- no spaces or generated-artifact names;
- delete merged topic branches.

## Conventional Commits

Use:

```text
<type>(<scope>): <imperative summary>
```

Recommended types are `feat`, `fix`, `docs`, `test`, `refactor`, `perf`, `chore`, `ci`, `ops`, and `revert`.

Examples:

```text
docs(git): establish collaborative workflow
feat(data): generate deterministic support examples
test(data): validate train validation split
fix(registry): remap container artifact paths
ci(test): run unit tests for pull requests
ops(compose): add API replica health checks
```

Keep commits focused on one logical change and do not commit virtual environments, credentials, model downloads, databases or generated reports.

## Daily development flow

```bash
# Synchronize integration history before branching.
git switch develop
git pull --ff-only origin develop

# Create the personal topic branch.
git switch -c feature/a/<short-description>

# Implement and test.
git add <explicit-file-list>
git commit -m "feat(<scope>): <summary>"
git push -u origin feature/a/<short-description>
```

### Explanation

- `git switch develop` selects the integration branch.
- `git pull --ff-only origin develop` applies remote commits only if the local branch can advance without divergence.
- `git switch -c` creates and checks out a branch in one command.
- Explicitly listing files in `git add` avoids accidentally staging generated output.
- `git commit` records the staged change locally.
- `git push -u` publishes the branch and sets upstream tracking.

Open the GitHub pull request against `develop`, complete the PR template and request review after CI succeeds.

## Pull Request workflow

1. Create or select an Issue.
2. Create a topic branch from current `develop`.
3. Implement acceptance criteria.
4. Run focused and broader checks.
5. Push the branch and open a PR into `develop`.
6. Complete implementation, test, security and deployment sections.
7. Obtain at least one approval from the other developer.
8. Resolve all blocking comments.
9. Confirm required checks pass.
10. Squash and merge normal topic work.
11. Delete the merged topic branch.

A reviewer should examine correctness before style. Blocking findings include incorrect behavior, security/privacy exposure, broken interfaces, missing tests and deployment risk.

## Code review rules

- Authors cannot approve or merge their own PRs.
- At least one approval is required; by policy this must come from the other developer.
- New commits invalidate previous approvals when stale approvals are enabled.
- Authors must not force-push while actively resolving a review.
- Reviewers mark blocking issues separately from suggestions or questions.
- Every blocking comment must be addressed before merge.
- A shared-file integration change requires both developers.

## Merge strategy

### Topic branches

Use **Squash and Merge** into `develop`. Configure the pull-request title using Conventional Commit format because GitHub can use that title for the squash commit.

### Integration branches

Use **Squash and Merge** unless retaining commit sequence is intentionally necessary. Document exceptions.

### Releases

Update `main` only through an approved, CI-passing pull request from a release branch or `develop`.

Before a release PR:

```bash
git switch develop
git pull --ff-only origin develop
git switch -c release/1.0.0
git push -u origin release/1.0.0
```

Tag an actual approved commit only after merge and validation:

```bash
git switch main
git pull --ff-only origin main
git tag -a v1.0.0 -m "Release 1.0.0"
git push origin v1.0.0
```

## Updating a personal branch

```bash
git switch develop
git pull --ff-only origin develop
git switch feature/a/<short-description>
git rebase develop
```

`git rebase` replay is destructive to shared branch history. Do not rebase commits already used by another developer without coordination.

Resolve conflicts and continue:

```bash
git add <resolved-files>
git rebase --continue
```

If a personal rebased branch has already been pushed and requires force-update, prefer:

```bash
git push --force-with-lease origin feature/a/<short-description>
```

`--force-with-lease` rejects an update if unexpected remote commits appear since the developer last fetched.

## GitHub Issues and labels

Create one issue for each behavior, defect, infrastructure task, test or documentation change. Recommended baseline labels:

```text
feature, bug, documentation, infrastructure, ci, test,
model, data, api, monitoring, security,
priority:high, priority:medium, priority:low,
sprint:00 ... sprint:10
```

Configure suggested milestones for Sprints 00–10. Each issue should contain acceptance criteria, primary developer, dependencies, planned files, test strategy and branch name.

## Branch protection recommendations

### Protect `main`

- require pull requests before merging;
- require at least one approving review;
- dismiss stale approvals when new commits arrive;
- require selected status checks to pass;
- require branches to be up to date;
- prohibit direct pushes, force-pushes and deletion;
- include administrators in the rules where practical.

Recommended checks:

```text
lint
unit-tests
model-smoke
container-smoke
compose-integration
kubernetes-validation
```

Enable each check only after the corresponding GitHub Actions job exists with a stable name.

### Protect `develop`

- require pull requests;
- require one approval from the other developer;
- require lint and unit-test checks;
- prohibit direct pushes and force-pushes;
- require the branch to be current before merge;
- consider linear history with Squash and Merge.

## Repository settings

- allow Squash and Merge;
- automatically delete merged topic branches;
- enable Dependabot alerts and security updates;
- use read-only Actions defaults unless a workflow needs write/package permissions;
- avoid signed-commit requirements until both developers have a consistent signing configuration.

## Secret and artifact policy

Never commit `.venv/`, credentials, `mlflow.db`, `mlruns/`, `data/monitoring.db`, model caches, generated reports, `.env` files, keys or tokens. Store required CI secrets only in GitHub Actions secrets and verify that logs never print them.

## Conflict prevention

- assign one primary file owner per branch;
- avoid simultaneous editing of the same file;
- stabilize shared interfaces before dependent work;
- keep pull requests small;
- use integration branches only for cross-owner validation;
- synchronize `develop` frequently;
- update shared configuration and documentation through reviewed pull requests.

## No fabricated history

No commit, branch, pull request, review, CI result or release should be reported as complete unless its actual repository evidence exists.
