# auto-gen-py-project

[![PyPI version](https://img.shields.io/pypi/v/auto-gen-py-project)](https://pypi.org/project/auto-gen-py-project/)
[![Python](https://img.shields.io/pypi/pyversions/auto-gen-py-project)](https://pypi.org/project/auto-gen-py-project/)
[![License: AGPL v3](https://img.shields.io/badge/License-AGPL_v3-blue.svg)](LICENSE)
[![CI](https://github.com/axcel-blade/Auto-Gen-Py-Project/actions/workflows/ci.yml/badge.svg)](https://github.com/axcel-blade/Auto-Gen-Py-Project/actions/workflows/ci.yml)

CLI tool that scaffolds a production-ready Python project — with a built-in Gradle-inspired build system (`pybuild`).

---

## Table of Contents

- [Overview](#overview)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Generated Project Layout](#generated-project-layout)
- [pybuild — Task Runner](#pybuild--task-runner)
  - [Built-in tasks](#built-in-tasks)
  - [Defining tasks](#defining-tasks)
  - [Task features](#task-features)
  - [CLI flags](#cli-flags)
  - [Example output](#example-output)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

`auto-gen-py-project` generates a standards-aligned Python project in one command. The scaffold mirrors a Gradle Java project structure and includes everything needed to start developing immediately.

`pybuild` is the built-in task runner. It resolves and executes tasks in dependency order via a DAG — just like Gradle's `build.gradle` — and supports incremental builds, parallel execution, coverage reports, and more.

---

## Requirements

- Python 3.8+ (3.10+ recommended)
- `pip` available in your environment
- Windows, Linux, or macOS

---

## Installation

```bash
git clone https://github.com/axcel-blade/auto-gen-py-project.git
cd auto-gen-py-project
python -m pip install --upgrade pip build
python -m pip install .
```

---

## Usage

**Scaffold a new project folder:**

```bash
auto-gen-py-project my_project
```

**Initialize inside the current folder:**

```bash
auto-gen-py-project my_project --init
```

**Without the CLI on your `PATH`:**

```bash
python -m auto_gen_py_project my_project
python -m auto_gen_py_project my_project --init
```

---

## Generated Project Layout

```text
my_project/
├── src/
│   ├── __init__.py
│   ├── main.py
│   └── resources/          ← static assets, config files, data
├── tests/
│   ├── conftest.py          ← shared fixtures, src/ on sys.path
│   └── test_main.py
├── .github/
│   └── workflows/
│       └── ci.yml           ← matrix CI + coverage + build verification
├── pybuild.py               ← task definitions
├── pybuild                  ← Unix wrapper script (Gradle Wrapper equivalent)
├── pybuild.bat              ← Windows wrapper script
├── pyproject.toml           ← project metadata + dev/test/lint dep groups
├── .venv/                   ← project-local virtual environment
├── README.md
├── LICENSE
└── .gitignore
```

---

## pybuild — Task Runner

Every generated project includes a `pybuild.py` with pre-wired tasks organised into groups.

### Built-in tasks

| Group | Task | Equivalent Gradle task | What it does |
|---|---|---|---|
| verification | `clean` | `clean` | Remove build artefacts |
| verification | `lint` | `checkstyle` | Run ruff linter |
| verification | `typecheck` | `pmd` | Run mypy type checker |
| verification | `test` | `test` | Run pytest, write JUnit XML |
| verification | `coverage` | `jacocoTestReport` | Run pytest-cov, HTML + XML reports |
| verification | `check` | `check` | lint + test together |
| build | `assemble` | `assemble` | Package without running tests |
| build | `build` | `build` | Full build: test then package |
| build | `publish` | `publish` | Upload to PyPI via twine |
| application | `run` | `run` | Execute `src/main.py` |
| utility | `lock` | lockfile | Freeze env to `requirements.lock` |
| utility | `check_env` | — | Print Python + env info |

### Defining tasks

```python
# pybuild.py
from auto_gen_py_project.build_system import task

@task(group="verification")
def clean():
    shutil.rmtree("dist", ignore_errors=True)

@task(depends_on=["clean"], group="verification")
def test():
    subprocess.run(["pytest"], check=True)

@task(depends_on=["test"], group="build")
def build():
    subprocess.run(["python", "-m", "build"], check=True)
```

### Task features

**Task groups** — `group=` organises tasks in `--list` output, just like Gradle.

**UP-TO-DATE checks** — declare `inputs` and `outputs`; tasks are skipped when nothing changed:

```python
@task(inputs=["schema.json"], outputs=["generated.py"])
def generate():
    ...
```

**Conditional execution** — `only_if` skips a task at runtime:

```python
@task(only_if=lambda: os.environ.get("CI") == "true")
def upload_coverage():
    ...
```

**Enable/disable** — `enabled=False` disables a task without removing it:

```python
@task(enabled=bool(shutil.which("mypy")))
def typecheck():
    ...
```

**Lifecycle hooks** — `do_first` / `do_last` append actions without redefining the task:

```python
task_obj = list_tasks()["test"]
task_obj.do_first(lambda: print("setup"))
task_obj.do_last(lambda: print("teardown"))
```

**Finalizers** — always run after a task, even on failure:

```python
@task(finalized_by=["cleanup"])
def integration_test():
    ...
```

**Ordering constraints** — `must_run_after` reorders without adding dependencies:

```python
@task(must_run_after=["lint"])
def typecheck():
    ...
```

**pybuild.properties** — external key=value config loaded automatically:

```properties
# pybuild.properties
publish.repo=pypi
```

```python
from auto_gen_py_project.build_system import properties
repo = properties.get("publish.repo", "testpypi")
```

### CLI flags

```bash
pybuild build                 # run 'build' and its dependencies
pybuild clean test            # run 'clean', then 'test'
pybuild --list                # list all tasks grouped by group
pybuild --dry-run build       # show what would run without executing
pybuild --parallel build      # run independent tasks concurrently
pybuild --continue build      # keep going after a failure
pybuild --rerun-tasks build   # force re-run ignoring UP-TO-DATE cache
pybuild --info build          # show task inputs/outputs
pybuild --debug build         # show full dependency info
pybuild --quiet build         # suppress all output
pybuild -f other/pybuild.py build  # custom build file
python pybuild.py build       # without installing pybuild
```

### Example output

```
> Build: 3 task(s) to execute

> Task :clean
  [DONE] 0.01s

> Task :test
  [DONE] 1.23s

> Task :build
  [DONE] 0.87s

BUILD SUCCESSFUL in 2.11s
3 actionable task(s): 3 executed
```

With `--list`:

```
verification
------------
  clean        Remove build artefacts
  lint         Run ruff linter
  test         Run the full test suite
  coverage     Run tests with coverage
  check        lint + test together

build
-----
  assemble     Package without running tests
  build        Full build: test then package
  publish      Upload to PyPI  [disabled]
```

---

## Troubleshooting

```bash
# Show all CLI options
python -m auto_gen_py_project --help
pybuild --help

# List all available tasks
pybuild --list

# Check Python and pip versions
python --version
python -m pip --version
```

| Problem | Fix |
|---|---|
| `pybuild: command not found` | Run `pip install -e .` or use `python pybuild.py <task>` |
| `TaskNotFoundError` | Check spelling; run `pybuild --list` to see available tasks |
| `CyclicDependencyError` | Review `depends_on` chains in `pybuild.py` for loops |
| Build file not found | Run from the directory containing `pybuild.py`, or pass `-f path/to/pybuild.py` |
| Task always re-runs | Declare `inputs=` and `outputs=` to enable UP-TO-DATE skipping |
| Want to force re-run | Pass `--rerun-tasks` to ignore the UP-TO-DATE cache |

---

## Contributing

Contributions are welcome. This project uses **Git Flow**.

See [CONTRIBUTING.md](CONTRIBUTING.md) for the full workflow — branch commands, PR rules, CI overview, release process, and rollback guide.

See [CHANGELOG.md](CHANGELOG.md) for version history.

---

## License

Licensed under the [GNU General Public License v3](LICENSE).
