# Python Build System Features

A mapping of Gradle's core build features to their Python equivalents, with a focus on how this project's `pybuild` task runner implements them.

---

## 1. Dependency Management

Python manages dependencies through `pip` and `pyproject.toml`.

- `pip` downloads and installs packages from PyPI automatically.
- `pyproject.toml` declares all project dependencies in one place.
- Transitive dependencies are resolved and installed automatically.
- `pip-tools`, `Poetry`, or `uv` can lock exact versions for reproducibility.

### Example

```toml
# pyproject.toml
[project]
dependencies = [
    "requests>=2.28",
    "click>=8.0",
]

[project.optional-dependencies]
dev = ["pytest", "coverage"]
```

```bash
# Install all dependencies
pip install .

# Install with dev extras
pip install ".[dev]"
```

---

## 2. Build Automation

`pybuild` is this project's Gradle-inspired task runner. It automates common development tasks via a `pybuild.py` file.

Common automated tasks:

- `clean` — remove build artefacts
- `lint` — run code style checks
- `test` — run the test suite
- `build` — package the project
- `publish` — upload to PyPI

### Example

```python
# pybuild.py
import shutil
import subprocess
from auto_gen_py_project.build_system import task

@task
def clean():
    """Remove build artefacts."""
    shutil.rmtree("dist", ignore_errors=True)
    shutil.rmtree("build", ignore_errors=True)

@task(depends_on=["clean"])
def test():
    """Run the test suite."""
    subprocess.run(["pytest", "-v"], check=True)

@task(depends_on=["test"])
def build():
    """Build wheel and sdist."""
    subprocess.run(["python", "-m", "build"], check=True)
```

```bash
pybuild build    # runs: clean → test → build
pybuild --list   # list all available tasks
```

---

## 3. Incremental Builds

`pybuild` uses a DAG (directed acyclic graph) of task dependencies to execute only what is needed.

- Tasks run in topological order.
- Skipped tasks are not re-executed in the same run.
- Tools like `watchfiles` or `pytest-watch` enable file-change-triggered re-runs.

### Example

```bash
# Only the test task and its dependencies run — not build
pybuild test
```

---

## 4. Build Cache

Python tools support caching at multiple levels:

- `functools.lru_cache` / `functools.cache` — in-memory function-level caching.
- `joblib.Memory` — disk-based result caching for expensive computations.
- `pip` caches downloaded wheels in `~/.cache/pip`.
- GitHub Actions caches the `pip` cache between CI runs for faster builds.

### Example

```python
# Cache expensive computation results
from functools import cache

@cache
def expensive_step():
    # result is cached for repeated calls in the same process
    ...
```

```yaml
# GitHub Actions pip cache
- uses: actions/cache@v4
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('**/pyproject.toml') }}
```

---

## 5. Multi-Project Builds

Large Python monorepos can host multiple packages, each with its own `pyproject.toml`.

- `pybuild` tasks can be chained across sub-projects by calling `subprocess.run`.
- Tools like `Hatch`, `Poetry`, or `uv workspaces` provide workspace-level management.

### Example

```
monorepo/
├── packages/
│   ├── core/
│   │   └── pyproject.toml
│   └── api/
│       └── pyproject.toml
└── pybuild.py   ← orchestrates all sub-projects
```

```python
# pybuild.py — root-level orchestration
@task
def test_all():
    for pkg in ["packages/core", "packages/api"]:
        subprocess.run(["pybuild", "test"], cwd=pkg, check=True)
```

---

## 6. Plugin System

`pybuild` is extended by defining custom task functions in `pybuild.py`.

- Any Python function decorated with `@task` becomes a first-class build step.
- Shared task libraries can be imported from internal packages.
- `setuptools` entry points allow third-party CLI plugins.

### Common Tool Plugins

| Tool | Purpose |
|---|---|
| `pytest` | Test execution |
| `coverage` | Code coverage |
| `black` | Code formatting |
| `ruff` | Linting and style |
| `mypy` | Static type checking |
| `twine` | Package publishing |
| `sphinx` | Documentation generation |

### Example

```python
# pybuild.py — custom lint plugin-style task
@task(depends_on=["clean"])
def lint():
    """Run ruff and mypy."""
    subprocess.run(["ruff", "check", "src/"], check=True)
    subprocess.run(["mypy", "src/"], check=True)
```

---

## 7. Task-Based Architecture

Everything in `pybuild` is a task. Tasks can depend on other tasks, forming a DAG.

| Gradle Task | pybuild Equivalent |
|---|---|
| `clean` | `pybuild clean` |
| `test` | `pybuild test` |
| `build` | `pybuild build` |
| `jar` | `pybuild build` (produces `.whl`) |
| `bootRun` | `pybuild run` |

### Registration Styles

```python
# Style 1 — bare decorator
@task
def clean(): ...

# Style 2 — decorator with options
@task(depends_on=["clean"], description="Run tests")
def test(): ...

# Style 3 — function-call DSL (Gradle-style)
task("build", depends_on=["test"], action=build_fn)
```

---

## 8. Python DSL (`pybuild.py`)

Where Gradle uses a Groovy DSL (`build.gradle`), `pybuild` uses plain Python (`pybuild.py`). Python is more readable and requires no new language to learn.

### Groovy (Gradle)

```groovy
// build.gradle
task clean(type: Delete) {
    delete buildDir
}
task test(dependsOn: clean) {
    doLast { exec { commandLine 'pytest' } }
}
```

### Python (pybuild)

```python
# pybuild.py
@task
def clean():
    shutil.rmtree("dist", ignore_errors=True)

@task(depends_on=["clean"])
def test():
    subprocess.run(["pytest"], check=True)
```

---

## 9. Type-Annotated Build Scripts

Where Gradle offers a Kotlin DSL for type safety, Python build scripts gain type safety through standard type annotations and `mypy`.

```python
# pybuild.py — fully typed
from collections.abc import Callable
from auto_gen_py_project.build_system import task

@task(depends_on=["lint"])
def test() -> None:
    """Run pytest with coverage."""
    subprocess.run(["pytest", "--cov=src"], check=True)
```

---

## 10. Testing Support

Python has a rich testing ecosystem.

| Tool | Purpose |
|---|---|
| `pytest` | Test execution and discovery |
| `unittest` | Built-in standard library test framework |
| `coverage` | Code coverage measurement |
| `pytest-cov` | Coverage plugin for pytest |
| `hypothesis` | Property-based testing |
| `responses` / `httpretty` | HTTP mocking |
| `pytest-mock` | Mock integration |

### Example

```python
# tests/test_main.py
import pytest
from src.main import my_function

def test_basic():
    assert my_function(2) == 4

@pytest.mark.parametrize("n,expected", [(1, 1), (3, 9)])
def test_parametrized(n, expected):
    assert my_function(n) == expected
```

```bash
pybuild test            # run full suite via pybuild
pytest -v               # run directly
pytest --cov=src -v     # with coverage report
```

---

## 11. Continuous Integration Support

This project ships CI/CD workflows for GitHub Actions out of the box.

| Workflow | File | Trigger |
|---|---|---|
| CI | `.github/workflows/ci.yml` | Push to `develop`/`feature/*`/`release/*`; PR to `main` |
| Release & Publish | `.github/workflows/release.yml` | GitHub Release published |

Integrates with:

- **GitHub Actions** — matrix builds across Python 3.9, 3.11, 3.13
- **Jenkins** — call `pybuild test build` from a `Jenkinsfile`
- **GitLab CI/CD** — use `pybuild` commands in `.gitlab-ci.yml`
- **Azure DevOps** — run `pybuild` in a pipeline YAML step

### Example CI step

```yaml
# .github/workflows/ci.yml
- name: Run tests
  run: pybuild test
```

---

## 12. Python Wrapper (Environment Pinning)

Gradle Wrapper ensures everyone uses the same Gradle version. Python equivalents:

| Mechanism | How it works |
|---|---|
| `.python-version` | `pyenv` reads this to auto-switch Python versions |
| `pyproject.toml` `requires-python` | Declares the minimum supported Python version |
| `venv` / `.venv` | Isolates project dependencies from the global environment |
| `uv` | Ultra-fast resolver; locks Python + packages in `uv.lock` |

Generated projects include a local `.venv` created automatically by `auto-gen-py-project`.

```toml
# pyproject.toml
[project]
requires-python = ">=3.8"
```

```bash
# Recreate the environment anywhere
python -m venv .venv
.venv/Scripts/activate   # Windows
pip install -e ".[dev]"
```

---

## 13. Artifact Publishing

Python packages are published to PyPI (or private registries) using standard tools.

| Tool | Purpose |
|---|---|
| `build` | Creates `.whl` and `.tar.gz` source dist |
| `twine` | Uploads distributions to PyPI |
| OIDC Trusted Publisher | Passwordless PyPI publishing from GitHub Actions |
| `flit` | Simplified packaging and publishing |

### Example

```bash
# Build
python -m build

# Publish (manual)
twine upload dist/*

# Publish via pybuild
pybuild publish
```

```yaml
# release.yml — automated PyPI publish on GitHub Release
- name: Publish to PyPI
  uses: pypa/gh-action-pypi-publish@release/v1
```

---

## 14. Cross-Platform Support

Python and `pybuild` run on Windows, Linux, and macOS without modification.

- `pybuild` uses `subprocess` with list-style args (avoids shell quoting issues).
- `pathlib.Path` handles file paths cross-platform.
- Generated projects include platform-aware `.gitignore` entries.

### Example

```python
# Cross-platform path handling in pybuild.py
from pathlib import Path

@task
def clean():
    dist = Path("dist")
    if dist.exists():
        shutil.rmtree(dist)
```

---

## 15. IDE Integration

Python projects generated by `auto-gen-py-project` work out-of-the-box with:

| IDE | Integration |
|---|---|
| **VS Code** | Python extension auto-detects `.venv`; `pybuild.py` tasks via Terminal |
| **PyCharm** | Detects `pyproject.toml`; run configurations for `pybuild` |
| **IntelliJ IDEA** | Python plugin + `pyproject.toml` support |
| **Neovim / Vim** | LSP via `pylsp` or `pyright` |

`pybuild --list` outputs all available tasks so any terminal-aware editor can discover them.

---

## 16. Performance Optimization

| Feature | Python Equivalent |
|---|---|
| Incremental builds | DAG-based task skipping in `pybuild` |
| Parallel execution | `concurrent.futures.ThreadPoolExecutor` in custom tasks |
| Build cache | `pip` wheel cache; `joblib`; GitHub Actions cache |
| Configuration caching | Import-time module caching in `pybuild.py` |
| Daemon process | `pytest-xdist` for parallel test workers |

### Example: parallel tasks in pybuild

```python
# pybuild.py — run lint and type-check in parallel
import concurrent.futures

@task(depends_on=["clean"])
def check():
    """Run lint and type checking in parallel."""
    with concurrent.futures.ThreadPoolExecutor() as pool:
        f1 = pool.submit(subprocess.run, ["ruff", "check", "src/"], check=True)
        f2 = pool.submit(subprocess.run, ["mypy", "src/"], check=True)
        f1.result()
        f2.result()
```

---

## 17. Security Features

| Feature | Tool |
|---|---|
| Dependency vulnerability scanning | `pip-audit`, `safety` |
| Dependency verification (hashes) | `pip --require-hashes`, `pip-tools` |
| Secure credential management | Environment variables; GitHub Actions secrets |
| Signed artifact support | `sigstore` (PEP 740) |
| Dependabot alerts | GitHub's built-in `dependabot.yml` |

### Example

```bash
# Audit installed packages for known CVEs
pip-audit

# Generate locked requirements with hashes
pip-compile --generate-hashes requirements.in
```

---

## 18. Configuration Management

Python provides multiple layers of configuration management.

| Layer | Tool |
|---|---|
| Project metadata | `pyproject.toml` |
| Environment variables | `python-dotenv`, `os.environ` |
| Typed settings | `pydantic-settings` |
| Build profiles | Environment-specific task conditions in `pybuild.py` |
| CLI properties | `click`, `argparse` |

### Example

```python
# pybuild.py — environment-aware task
import os

@task(depends_on=["test"])
def publish():
    """Publish to PyPI or Test PyPI depending on environment."""
    repo = os.getenv("PUBLISH_REPO", "testpypi")
    subprocess.run(
        ["twine", "upload", "--repository", repo, "dist/*"],
        check=True,
    )
```

```bash
PUBLISH_REPO=pypi pybuild publish    # publish to production PyPI
pybuild publish                       # defaults to testpypi
```

---

## 19. Custom Build Logic

`pybuild` makes custom build logic a first-class citizen — any Python code can be a task.

```python
# pybuild.py — custom code generation task
import json
from pathlib import Path

@task
def generate_schema():
    """Auto-generate JSON schema from dataclasses."""
    from src.models import MyModel
    schema = MyModel.schema()
    Path("docs/schema.json").write_text(json.dumps(schema, indent=2))

@task(depends_on=["generate_schema", "test"])
def build():
    subprocess.run(["python", "-m", "build"], check=True)
```

Shared build logic can live in a dedicated package and be imported across projects:

```python
# shared_build/tasks.py
from auto_gen_py_project.build_system import task

@task
def lint():
    subprocess.run(["ruff", "check", "src/"], check=True)
```

---

## 20. Reporting and Analytics

| Report Type | Tool |
|---|---|
| Test results | `pytest` console output; `pytest --junit-xml=report.xml` |
| Code coverage | `coverage html` generates an HTML report in `htmlcov/` |
| Build performance | `pybuild` prints per-task elapsed time |
| Dependency analysis | `pipdeptree`, `pip-audit` |
| Code quality metrics | `ruff`, `pylint`, `radon` (complexity), `xenon` |

### Example

```bash
# Generate HTML coverage report
pytest --cov=src --cov-report=html

# View dependency tree
pipdeptree

# pybuild prints timing automatically
pybuild build
# > Task :clean  [DONE] 0.01s
# > Task :test   [DONE] 1.23s
# > Task :build  [DONE] 0.87s
# BUILD SUCCESSFUL in 2.11s
```

---

## Key Advantages of the Python Approach

| Advantage | Description |
|---|---|
| No new language | `pybuild.py` is plain Python — no Groovy or Kotlin to learn |
| Fast setup | `pip install auto-gen-py-project` and `auto-gen-py-project my_project` |
| Flexible | Any Python library is available inside tasks |
| Portable | Works on Windows, Linux, macOS without extra tooling |
| Readable | Python's syntax is cleaner than Groovy DSL for most developers |
| Ecosystem | Thousands of PyPI packages usable directly in build scripts |

---

## Common Use Cases

| Use Case | pybuild Tasks |
|---|---|
| Python Application | `clean → lint → test → build` |
| Library Development | `clean → lint → test → build → publish` |
| FastAPI / Flask API | `clean → lint → test → build → docker-build` |
| Data Science | `clean → generate-data → train → evaluate` |
| CLI Tool | `clean → test → build → install` |
| Microservices | Root `pybuild.py` orchestrates multiple sub-project `pybuild` calls |

---

## Quick Reference: Gradle → Python

| Gradle Feature | Python Equivalent |
|---|---|
| `build.gradle` | `pybuild.py` |
| `@task` | `@task` decorator in `pybuild` |
| `dependsOn` | `depends_on=[...]` in `@task` |
| `gradle build` | `pybuild build` |
| `gradle --tasks` | `pybuild --list` |
| `gradle clean` | `pybuild clean` |
| `gradle test` | `pybuild test` |
| `settings.gradle` | `pyproject.toml` |
| Gradle Wrapper | `venv` + `pyproject.toml` `requires-python` |
| Maven Central | PyPI (`pypi.org`) |
| `./gradlew` | `pybuild` (or `python pybuild.py`) |
| Groovy DSL | Python |
| Kotlin DSL | Python + type annotations + `mypy` |
