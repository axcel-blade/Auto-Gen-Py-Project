# Changelog

All notable changes to **auto-gen-py-project** are documented here.

## 1.2.4

### Changed

- Dropped “AI-ready” marketing from README and docs; packaging is a template scaffolder only
- Renamed CLI flag `--ai` to `--describe` for keyword-based template hints (no LLM / network)
- Clarified FAQ, API, Cookbook, and ROADMAP that hints are offline heuristics
- Version bump across package metadata and community docs

## 1.2.3

### Fixed

- CD publishes **TestPyPI only**; added `id-token: write` so TestPyPI OIDC/token publish works
- Removed production PyPI deploy job that failed Trusted Publishing

## 1.2.2

### Fixed

- Release CD can publish using `TEST_PYPI_API_TOKEN` / `PYPI_API_TOKEN` when Trusted Publishing is not configured

### Changed

- Documented TestPyPI account `axcelblade` and GitHub secret setup in `docs/publishing.md`

## 1.2.1

### Changed

- Keep **LICENSE.md** as the sole license file (removed root `LICENSE`)
- Point README badge and license links at `LICENSE.md`
- Documentation version bump to 1.2.1

## 1.2.0

### Changed

- Relicensed the package from AGPL-3.0-or-later to **MIT**
- Updated community docs, badges, and SPDX metadata for MIT
- Version bump across package metadata and documentation

## 1.1.0

### Added

- Full project-generator rewrite with Typer CLI, Jinja2 templates, and plugin entry points
- Interactive `create` wizard and non-interactive `new` / `init`
- Built-in scaffolds for 16 project types
- Integrations: git, venv, Docker, GitHub Actions, pre-commit, VS Code
- Optional keyword-based template hints (`--describe`)
- GitHub community docs: TODO, ROADMAP, wiki pages, discussion templates

### Changed

- Package focus is now project scaffolding (`auto-gen-py-project`), not the previous build-runner scaffold
- Documentation refreshed for v1.1.0

### Removed

- Legacy `pybuild` / Gradle-style build-system modules from this package

## 1.0.0

- Initial generator-oriented release baseline (superseded by later releases)
