# Contributing to Auto Gen Py Project

Thank you for considering a contribution. This project uses **Git Flow** for branch management.

---

## Branch Model

```
main ──────────────────────────────────────────────────── production
  │                                                            ▲
  │  (hotfix/* merged into both main and develop)             │
  │                                                            │
develop ────────────────────────────────────────────── integration
  │                ▲              ▲
  │  feature/*     │  release/*   │
  └──────────────►─┘              │
                                  └── merged into main + develop
```

| Branch | Branched from | Merges into | Purpose |
|---|---|---|---|
| `main` | — | — | Production-ready code only. Every commit is a release. |
| `develop` | `main` | — | Latest development. Default branch for feature work. |
| `feature/*` | `develop` | `develop` | New functionality. One branch per feature. |
| `release/*` | `develop` | `main` + `develop` | Release preparation — version bump, changelog, final fixes. |
| `hotfix/*` | `main` | `main` + `develop` | Urgent production patches. Bypasses the feature/release cycle. |

---

## Day-to-Day Workflow

### 1. Feature development

```bash
# Start a feature from develop
git checkout develop
git pull origin develop
git checkout -b feature/my-feature

# ... do work, commit often ...

# Push and open a PR targeting develop
git push -u origin feature/my-feature
# → GitHub PR: base = develop
```

CI runs automatically on `feature/*` pushes and on the PR. The PR requires:
- All CI checks green (`Test`, `Coverage`, `Build verification`)
- At least one approving review
- Branch up-to-date with `develop`

Once merged, delete the feature branch.

---

### 2. Preparing a release

```bash
# Cut a release branch from develop
git checkout develop
git pull origin develop
git checkout -b release/0.3.0

# Bump versions
# - auto_gen_py_project/__init__.py  →  __version__ = "0.3.0"
# - setup.py                         →  version="0.3.0"

git commit -am "chore: bump version to 0.3.0"
git push -u origin release/0.3.0
```

On the release branch you may:
- Fix release-blocking bugs (no new features)
- Update `CHANGELOG.md` with the release date
- Tweak packaging metadata

The `version-check` CI job will fail if `__init__.py` and `setup.py` disagree on the version.

#### Finishing the release

```bash
# 1. Merge into main
git checkout main
git merge --no-ff release/0.3.0 -m "release: merge release/0.3.0 into main"
git tag -a v0.3.0 -m "Release 0.3.0"
git push origin main --tags

# 2. Back-merge into develop to stay in sync
git checkout develop
git merge --no-ff release/0.3.0 -m "chore: back-merge release/0.3.0 into develop"
git push origin develop

# 3. Delete the release branch
git branch -d release/0.3.0
git push origin --delete release/0.3.0

# 4. Publish a GitHub Release from the tag → triggers the publish workflow
#    GitHub UI: Releases → Draft a new release → choose tag v0.3.0
```

---

### 3. Hotfixes

```bash
# Branch from main (NOT develop)
git checkout main
git pull origin main
git checkout -b hotfix/fix-crash

# ... fix the bug, bump the patch version ...
# auto_gen_py_project/__init__.py  →  __version__ = "0.3.1"
# setup.py                         →  version="0.3.1"

git commit -am "fix: resolve crash on empty project name"
git push -u origin hotfix/fix-crash
# → GitHub PR: base = main
```

Once reviewed and merged:

```bash
# Tag the fix on main
git checkout main
git pull origin main
git tag -a v0.3.1 -m "Hotfix 0.3.1"
git push origin main --tags

# Back-merge into develop
git checkout develop
git merge --no-ff hotfix/fix-crash -m "chore: back-merge hotfix/fix-crash into develop"
git push origin develop

# Delete the hotfix branch
git branch -d hotfix/fix-crash
git push origin --delete hotfix/fix-crash

# Publish a GitHub Release from the tag → triggers the publish workflow
```

---

## Version Numbering

This project uses **semantic versioning** (`MAJOR.MINOR.PATCH`):

| Change type | Version bump | Example |
|---|---|---|
| New feature (backward-compatible) | MINOR | `0.2.0 → 0.3.0` |
| Bug fix or small improvement | PATCH | `0.3.0 → 0.3.1` |
| Breaking API change | MAJOR | `0.x → 1.0.0` |

Version must be identical in **both** of these files before a release branch is merged:

```
auto_gen_py_project/__init__.py   __version__ = "X.Y.Z"
setup.py                          version="X.Y.Z"
```

The `version-check` CI job enforces this automatically on `release/*`, `hotfix/*`, and PRs to `main`.

---

## CI Overview

| Workflow | Trigger | Jobs |
|---|---|---|
| `ci.yml` | Push to `develop`/`feature/*`/`release/*`/`hotfix/*`; PR to `main`/`develop` | Test matrix (3.9/3.11/3.13) with JUnit XML upload, Coverage report with HTML+XML upload, Build verification, Version check (release/hotfix only) |
| `cd.yml` | Push to `main`; GitHub Release published | Pre-deploy tests with JUnit XML upload, Build distributions, Deploy to PyPI (release only) |

---

## Recommended Branch Protections (GitHub Settings)

### `main`
- Require pull request before merging
- Require 1 approving review
- Require status checks: `Test (3.9)`, `Test (3.11)`, `Test (3.13)`, `Coverage report`, `Build verification`, `Version consistency`
- Require branches to be up-to-date before merging
- Do not allow force-pushes
- Do not allow deletions

### `develop`
- Require pull request before merging
- Require 1 approving review
- Require status checks: `Test (3.9)`, `Test (3.11)`, `Test (3.13)`, `Build verification`
- Require branches to be up-to-date before merging
- Do not allow force-pushes

---

## Running Checks Locally

```bash
# Install in editable mode with all dev dependencies
pip install -e ".[dev]"

# Run the build-system test suite (fast — no venv creation)
python -m pytest tests/test_build_system.py -v

# Run the full suite including slow generator tests (~13 min — creates real venvs)
python -m pytest tests/ -v

# Lint
python -m ruff check auto_gen_py_project/ tests/

# Type check
python -m mypy auto_gen_py_project/ --ignore-missing-imports

# Use pybuild for the full task pipeline
pybuild --list
pybuild check          # lint + test
pybuild coverage       # test with HTML + XML coverage report
pybuild build          # test + package
pybuild --dry-run build  # preview without executing
pybuild --parallel build # run independent tasks concurrently

# Generate a lock file
pybuild lock

# Check version consistency before opening a PR to main
python -c "
import re, pathlib
iv = re.search(r'__version__\s*=\s*\"([^\"]+)\"', pathlib.Path('auto_gen_py_project/__init__.py').read_text()).group(1)
sv = re.search(r'version=\"([^\"]+)\"', pathlib.Path('setup.py').read_text()).group(1)
assert iv == sv, f'Version mismatch: __init__.py={iv}, setup.py={sv}'
print(f'Versions match: {iv}')
"
```

---

## Rollback a Bad Release

```bash
# 1. Yank the broken version on PyPI (marks it as "avoid" without deleting)
pip install twine
twine yank auto-gen-py-project==X.Y.Z --reason "critical bug — use X.Y.W instead"

# 2. Delete the GitHub Release (UI) or via CLI
gh release delete vX.Y.Z --yes

# 3. Delete the tag locally and remotely
git tag -d vX.Y.Z
git push origin --delete vX.Y.Z

# 4. Create a hotfix/* branch from main to fix the issue, then re-release
```

---

## Questions or Ideas?

Open an issue on [GitHub Issues](https://github.com/axcel-blade/auto-gen-py-project/issues).  
All contributions are welcome and appreciated.
