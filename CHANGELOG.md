# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.3.0] - 2026-06-11

### Added

**pybuild task lifecycle features (Gradle parity)**
- `Task.group` — organise tasks into named groups; `--list` output is now grouped like Gradle's `--tasks`
- `Task.enabled` — disable a task without removing it (`enabled=False`)
- `Task.only_if` — conditional callable predicate; task is skipped at runtime when it returns `False`
- `Task.inputs` / `Task.outputs` — declare file dependencies for UP-TO-DATE fingerprinting
- `Task.finalized_by` — finalizer tasks always run after the triggering task, even on failure
- `Task.must_run_after` — ordering constraint that reorders the plan without adding dependencies
- `Task.do_first()` / `Task.do_last()` — prepend or append actions without redefining the task

**pybuild runner features**
- **UP-TO-DATE incremental builds** — SHA-256 fingerprints of `inputs`/`outputs` cached in `.pybuild-cache.json`; unchanged tasks are skipped and reported `UP-TO-DATE`
- **`--dry-run` / `-m`** — print the execution plan without running any tasks
- **`--continue`** — keep executing independent tasks after a failure
- **`--parallel` / `-p`** — level-based `ThreadPoolExecutor`; independent tasks run concurrently
- **`--rerun-tasks`** — force re-execution of all tasks, ignoring the UP-TO-DATE cache
- **Log levels** — `--info`/`-i` (show inputs/outputs), `--debug`/`-d` (show dependency lists), `--quiet`/`-q` (silent)
- **`pybuild.properties`** — external `key=value` config file loaded automatically before the build file

**Generator — generated project scaffold**
- `src/resources/` directory with `.gitkeep` (equivalent to Gradle's `src/main/resources/`)
- `pybuild` Unix wrapper script + `pybuild.bat` Windows wrapper (equivalent to Gradle Wrapper)
- `pyproject.toml` now includes `[project.optional-dependencies]` with `dev`, `test`, and `lint` groups (equivalent to `testImplementation` / `compileOnly`), plus `[tool.pytest.ini_options]` and `[tool.coverage.run]` sections
- `tests/conftest.py` generated with `src/` on `sys.path` for all tests
- `.github/workflows/ci.yml` generated with matrix builds (3.9/3.11/3.13), JUnit XML test result upload, coverage job with HTML + XML report upload, and build verification job
- Generated `pybuild.py` now includes tasks: `check`, `assemble`, `run`, `coverage`, `lock`, `check_env` — all with task groups

**Project's own pybuild.py tasks**
- `check` — lint + test together (Gradle `check` equivalent)
- `assemble` — package without running tests (Gradle `assemble` equivalent)
- `run` — execute the CLI entry point
- `coverage` — `pytest-cov` with HTML report to `build/reports/coverage/` and XML to `build/reports/coverage.xml`
- `lock` — freeze the environment to `requirements.lock`
- `check_env` — print Python version and environment info

**CI/CD**
- `ci.yml`: added `--junit-xml` flag to pytest, test result artifact upload per Python version, dedicated `coverage` job with HTML + XML artifact upload, ruff lint step on all matrix runs
- `cd.yml`: added `--junit-xml` flag and test result artifact upload

### Fixed
- Finalizer tasks now always run even when the triggering task fails (runner was breaking out of the loop before executing finalizers)
- Removed unused `LOG_NORMAL` and `LOG_QUIET` imports in `tests/test_build_system.py` (ruff F401)
- `.gitignore` updated to cover `.venv/`, `.pybuild-cache.json`, `requirements.lock`, `htmlcov/`, `.coverage`, `coverage.xml`

## [0.2.1] - 2026-05-31

### Fixed
- Renamed `build.py` to `pybuild.py` to prevent shadowing Python's `build` package when running `python -m build`
- Removed unused import of `main` in `tests/test_main.py` (ruff F401)

### Changed
- Updated LICENSE from GPL v3 to AGPL v3
- Refactored README — removed dev/ops content, added badges and table of contents
- Added CD pipeline (`cd.yml`) — production to PyPI on GitHub Release
- Removed `release.yml`, superseded by `cd.yml`
- Added community health files: `CHANGELOG.md`, `SECURITY.md`, `CODE_OF_CONDUCT.md`, `SUPPORT.md`
- Added GitHub templates: PR template, bug report, feature request issue templates

## [0.2.0] - 2026-05-31

### Added
- Python build system (`pybuild`) — a Gradle-inspired task runner
- `PYTHON_BUILD_FEATURES.md` documenting the full Gradle → pybuild feature mapping
- Task dependency DAG resolution with cycle detection
- `@task` decorator and function-call DSL for defining tasks
- `--list`, `--quiet`, and `-f` CLI flags for `pybuild`
- Custom exceptions: `TaskNotFoundError`, `CyclicDependencyError`, `TaskExecutionError`

### Changed
- Updated project structure and documentation

## [0.1.4] - 2025-01-01

### Changed
- Bumped version to 0.1.4
- Updated GitHub Actions workflows

## [0.1.3] - 2025-01-01

### Changed
- Reverted version number to 0.1.3
- Removed GitHub Packages workflow; kept PyPI publish path only

## [0.1.2] - 2025-01-01

### Added
- GitHub Packages publish setup and workflow

## [0.1.1] - 2025-01-01

### Changed
- Replaced MIT License with GNU General Public License v3

## [0.1.0] - 2025-01-01

### Added
- Initial release
- CLI scaffolding tool (`auto-gen-py-project`)
- Generates `src/`, tests, `run.py`, `pyproject.toml`, `.gitignore`, `LICENSE`, `.venv`, and `pybuild.py`

[Unreleased]: https://github.com/axcel-blade/auto-gen-py-project/compare/v0.3.0...HEAD
[0.3.0]: https://github.com/axcel-blade/auto-gen-py-project/compare/v0.2.1...v0.3.0
[0.2.1]: https://github.com/axcel-blade/auto-gen-py-project/compare/v0.2.0...v0.2.1
[0.2.0]: https://github.com/axcel-blade/auto-gen-py-project/compare/v0.1.4...v0.2.0
[0.1.4]: https://github.com/axcel-blade/auto-gen-py-project/compare/v0.1.3...v0.1.4
[0.1.3]: https://github.com/axcel-blade/auto-gen-py-project/compare/v0.1.2...v0.1.3
[0.1.2]: https://github.com/axcel-blade/auto-gen-py-project/compare/v0.1.1...v0.1.2
[0.1.1]: https://github.com/axcel-blade/auto-gen-py-project/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/axcel-blade/auto-gen-py-project/releases/tag/v0.1.0
