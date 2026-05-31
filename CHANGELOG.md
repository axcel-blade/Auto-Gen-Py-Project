# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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

[Unreleased]: https://github.com/axcel-blade/auto-gen-py-project/compare/v0.2.0...HEAD
[0.2.0]: https://github.com/axcel-blade/auto-gen-py-project/compare/v0.1.4...v0.2.0
[0.1.4]: https://github.com/axcel-blade/auto-gen-py-project/compare/v0.1.3...v0.1.4
[0.1.3]: https://github.com/axcel-blade/auto-gen-py-project/compare/v0.1.2...v0.1.3
[0.1.2]: https://github.com/axcel-blade/auto-gen-py-project/compare/v0.1.1...v0.1.2
[0.1.1]: https://github.com/axcel-blade/auto-gen-py-project/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/axcel-blade/auto-gen-py-project/releases/tag/v0.1.0
