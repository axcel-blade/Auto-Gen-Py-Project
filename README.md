# Auto Gen Py Project

Simple CLI tool that scaffolds a clean Python project structure — with a built-in Gradle-inspired build system (`pybuild`).

## Description

`auto-gen-py-project` helps you start Python projects faster by generating a standards-aligned layout out of the box. It creates a project with `src/`, tests, `run.py`, `pyproject.toml`, `.gitignore`, `LICENSE`, a local `.venv`, and a ready-to-use `build.py` that wires up `pybuild` — a Gradle-inspired task runner for Python.

`pybuild` lets you define tasks with dependencies (a DAG) and execute them in the correct order from a simple `build.py` file, just like Gradle's `build.gradle`.

## Getting Started

### Dependencies

- Python 3.8+ (3.10+ recommended)
- `pip` available in your environment
- OS: Windows, Linux, or macOS

### Installing

Clone or download this repository:

```bash
git clone https://github.com/axcel-blade/auto-gen-py-project.git
cd auto-gen-py-project
```

Install the CLI (includes `pybuild`):

```bash
python -m pip install --upgrade pip build
python -m pip install .
```

### Executing program

Create a new project folder:

```bash
auto-gen-py-project my_project
```

Initialize in the current folder:

```bash
auto-gen-py-project my_project --init
```

If the command is not on your `PATH`, use module mode:

```bash
python -m auto_gen_py_project my_project
python -m auto_gen_py_project my_project --init
```

Generated project structure:

```text
my_project/
├── src/
│   ├── __init__.py
│   └── main.py
├── tests/
│   └── test_main.py
├── build.py          ← pybuild task definitions
├── .venv/
├── run.py
├── README.md
├── pyproject.toml
├── LICENSE
└── .gitignore
```

---

## pybuild — Gradle-like Build System

Every generated project includes a `build.py` with pre-wired tasks. The `pybuild` CLI executes them in dependency order.

### Defining tasks

```python
# build.py
from auto_gen_py_project.build_system import task, run_task

# Decorator style
@task
def clean():
    """Remove build artefacts."""
    shutil.rmtree("dist", ignore_errors=True)

@task(depends_on=["clean"])
def test():
    """Run the test suite."""
    subprocess.run(["pytest"], check=True)

@task(depends_on=["test"])
def build():
    """Build wheel and sdist."""
    subprocess.run(["python", "-m", "build"], check=True)

# --- or Gradle-style function calls ---
task("clean", action=clean_fn)
task("test",  depends_on=["clean"], action=test_fn)
task("build", depends_on=["test"],  action=build_fn)
```

### Running tasks

```bash
pybuild build          # runs: clean → test → build
pybuild test           # runs: clean → test
pybuild clean test     # explicit sequence
pybuild --list         # list all tasks and their dependencies
pybuild --quiet build  # suppress output
pybuild -f path/to/build.py build   # custom build file
python build.py build  # without installing pybuild
```

Example output (Gradle-style):

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

- Tasks form a **directed acyclic graph (DAG)**. `pybuild` resolves the correct execution order via topological sort.
- Cycles are detected and reported with the full dependency path.
- Each task name is unique within a build file; re-registering overwrites the previous definition.
- Tasks with no action are valid placeholders (lifecycle hooks).

### Error handling

| Scenario | Exception raised |
|---|---|
| Requested task does not exist | `TaskNotFoundError` |
| Dependency references missing task | `TaskNotFoundError` |
| Cycle in dependency graph | `CyclicDependencyError` |
| Task action raises an exception | `TaskExecutionError` |

---

## Help

For command options and usage help:

```bash
python -m auto_gen_py_project --help
pybuild --help
```

If installation fails, check:

```bash
python --version
python -m pip --version
```

Common issues:

| Problem | Fix |
|---|---|
| `pybuild: command not found` | Run `pip install -e .` or use `python build.py <task>` |
| `TaskNotFoundError` | Check spelling; run `pybuild --list` to see available tasks |
| `CyclicDependencyError` | Review `depends_on` chains in your `build.py` for loops |
| Build file not found | Run `pybuild` from the directory containing `build.py`, or pass `-f path/to/build.py` |

---

## Authors

- Axcel Blade — [srikanthfernando3@gmail.com](mailto:srikanthfernando3@gmail.com)

## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

This project uses **Git Flow**. The short version:

```
main      ← production, tagged releases only
develop   ← default integration branch, base for all features
feature/* ← one branch per feature, PR → develop
release/* ← release prep (version bump, changelog), PR → main then back-merge → develop
hotfix/*  ← urgent production patches, PR → main then back-merge → develop
```

Full details — commands, PR rules, branch protections, rollback — in [CONTRIBUTING.md](CONTRIBUTING.md).

Don't forget to give the project a star! Thanks again!

Top contributors:

<a href="https://github.com/axcel-blade/auto-gen-py-project/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=axcel-blade/auto-gen-py-project" alt="contrib.rocks image" />
</a>

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Local development

```bash
# Install in editable mode (registers pybuild CLI)
pip install -e .

# Run tests
python -m pytest tests/test_build_system.py -v   # fast (no venv creation)
python -m pytest tests/ -v                        # full suite (slow — creates venvs)

# Use pybuild task pipeline on this project
pybuild --list
pybuild test
pybuild build
```

### CI / CD overview

| Workflow | File | Trigger | What it does |
|---|---|---|---|
| CI | `ci.yml` | push to `develop`/`feature/*`/`release/*`/`hotfix/*`; PR to `main`/`develop` | Tests (3.9/3.11/3.13), build check, version consistency |
| Release & Publish | `release.yml` | GitHub Release published | Tests, build wheel+sdist, publish to PyPI via OIDC |

### Required GitHub settings

- **PyPI Trusted Publisher** — set up at [pypi.org/manage/account/publishing](https://pypi.org/manage/account/publishing/); no `TWINE_PASSWORD` secret needed.
- **Environment named `pypi`** in repository Settings → Environments.
- **Branch protection on `main`**: require `Test (3.9)`, `Test (3.11)`, `Test (3.13)`, `Build verification`, `Version consistency` + 1 review + up-to-date branch.
- **Branch protection on `develop`**: require `Test (*)`, `Build verification` + 1 review.

### Release process (Git Flow)

```bash
# 1. Cut a release branch from develop
git checkout develop && git pull
git checkout -b release/0.3.0

# 2. Bump version in __init__.py and setup.py, update CONTRIBUTING.md / README.md

# 3. Merge into main and tag
git checkout main && git merge --no-ff release/0.3.0
git tag -a v0.3.0 -m "Release 0.3.0"
git push origin main --tags

# 4. Back-merge into develop
git checkout develop && git merge --no-ff release/0.3.0
git push origin develop

# 5. Publish a GitHub Release from the tag → release.yml handles PyPI
```

### Rollback a bad release

```bash
# Yank on PyPI (marks as "avoid" — does not delete)
twine yank auto-gen-py-project==X.Y.Z --reason "describe the issue"

# Remove GitHub Release and tag
gh release delete vX.Y.Z --yes
git tag -d vX.Y.Z && git push origin --delete vX.Y.Z

# Fix via hotfix/* branch, then re-release with a patch version
```

## Version History

- 0.2.0
  - Adopt Git Flow branching model (`main` / `develop` / `feature/*` / `release/*` / `hotfix/*`)
  - Add Gradle-inspired build system (`pybuild` CLI + `auto_gen_py_project.build_system` package)
  - Generated projects include a ready-to-use `build.py` with `clean → lint → test → build` tasks
  - DAG-based task dependency resolution with cycle detection
  - Three task registration styles: bare decorator, decorator with options, function-call DSL
  - Add CI workflow (`ci.yml`) — matrix builds on Python 3.9/3.11/3.13 + version-consistency check
  - Replace `workflow.yml` with `release.yml` — adds pre-publish test gate
  - Add `CONTRIBUTING.md` with full Git Flow commands, branch protection config, rollback guide
  - 23 new tests covering Task, Registry, DAG, Runner, and DSL
- 0.1.3
  - Align package metadata and version across project files
  - Add `auto-gen-py-project` console command entry point
  - Remove GitHub Packages workflow and keep PyPI publishing workflow
- 0.1.2
  - Create `.venv` inside generated project folders (including `--init`)
  - Add `.venv/` to generated `.gitignore`
- 0.1
  - Initial release

## License

This project is licensed under the GNU General Public License v3 — see the `LICENSE` file for details.
