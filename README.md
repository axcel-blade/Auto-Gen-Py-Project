# auto-gen-py-project

[![PyPI version](https://img.shields.io/pypi/v/auto-gen-py-project)](https://pypi.org/project/auto-gen-py-project/)
[![Python](https://img.shields.io/pypi/pyversions/auto-gen-py-project)](https://pypi.org/project/auto-gen-py-project/)
[![License: AGPL v3](https://img.shields.io/badge/License-AGPL_v3-blue.svg)](LICENSE)
[![CI](https://github.com/axcel-blade/Auto-Gen-Py-Project/actions/workflows/ci.yml/badge.svg)](https://github.com/axcel-blade/Auto-Gen-Py-Project/actions/workflows/ci.yml)

CLI tool that scaffolds a clean Python project — with a built-in Gradle-inspired build system (`pybuild`).

---

## Table of Contents

- [Overview](#overview)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [pybuild — Task Runner](#pybuild--task-runner)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

`auto-gen-py-project` generates a standards-aligned Python project layout in one command. The scaffold includes `src/`, tests, `run.py`, `pyproject.toml`, `.gitignore`, `LICENSE`, a local `.venv`, and a ready-to-use `pybuild.py` powered by `pybuild`.

`pybuild` lets you define tasks with dependencies (a DAG) and execute them in the correct order — just like Gradle's `build.gradle`.

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

**Generated project layout:**

```text
my_project/
├── src/
│   ├── __init__.py
│   └── main.py
├── tests/
│   └── test_main.py
├── pybuild.py        ← pybuild task definitions
├── .venv/
├── run.py
├── README.md
├── pyproject.toml
├── LICENSE
└── .gitignore
```

---

## pybuild — Task Runner

Every generated project includes a `pybuild.py` with pre-wired tasks. `pybuild` resolves and runs them in dependency order.

### Defining tasks

```python
# pybuild.py
from auto_gen_py_project.build_system import task

# Decorator style
@task
def clean():
    shutil.rmtree("dist", ignore_errors=True)

@task(depends_on=["clean"])
def test():
    subprocess.run(["pytest"], check=True)

@task(depends_on=["test"])
def build():
    subprocess.run(["python", "-m", "build"], check=True)

# Gradle-style function calls
task("clean", action=clean_fn)
task("test",  depends_on=["clean"], action=test_fn)
task("build", depends_on=["test"],  action=build_fn)
```

### Running tasks

```bash
pybuild build           # runs: clean → test → build
pybuild test            # runs: clean → test
pybuild clean test      # explicit sequence
pybuild --list          # list all tasks and dependencies
pybuild --quiet build   # suppress per-task output
pybuild -f path/pybuild.py build  # custom build file
python pybuild.py build           # without installing pybuild
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

### How it works

- Tasks form a **directed acyclic graph (DAG)**; execution order is resolved via topological sort.
- Cycles are detected and reported with the full dependency path.
- Each task name is unique within a build file; re-registering overwrites the previous definition.
- Tasks with no action are valid lifecycle placeholders.

### Errors

| Exception | Cause |
|---|---|
| `TaskNotFoundError` | Task name does not exist or a dependency is missing |
| `CyclicDependencyError` | Circular `depends_on` chain detected |
| `TaskExecutionError` | Task action raised an exception at runtime |

---

## Troubleshooting

```bash
# Show all CLI options
python -m auto_gen_py_project --help
pybuild --help

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

---

## Contributing

Contributions are welcome. This project uses **Git Flow**.

See [CONTRIBUTING.md](CONTRIBUTING.md) for the full workflow — branch commands, PR rules, CI overview, release process, and rollback guide.

See [CHANGELOG.md](CHANGELOG.md) for version history.

---

## License

Licensed under the [GNU General Public License v3](LICENSE).
