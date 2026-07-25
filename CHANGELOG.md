# Changelog

All notable changes to **auto-gen-py-project** are documented here.

## 1.3.4

### Added

- Console script ``auto_gen_py_project`` (underscore) alongside ``auto-gen-py-project`` for all OS
- Flag-style actions: ``--init``, ``--create``, ``--doctor``, ``--list-templates``, ``--version``
- ``--init`` scaffolds a simple Python project **into** the current or ``--path`` folder

### Changed

- Docs emphasize ``auto_gen_py_project --init`` for in-folder scaffolding
- Version bump across package metadata and community docs

## 1.3.3

### Fixed

- Plain ``init`` no longer treats a missing PATH as the current directory (Typer ``Path`` coercion), so it creates ``./my-project/`` even when cwd is not empty

### Changed

- Version bump across package metadata and community docs

## 1.3.2

### Changed

- Plain ``init`` (no PATH) creates a new root folder (default ``./my-project/``) and scaffolds a simple library project inside
- ``init PATH`` creates the folder if it is missing, then fills it
- Docs / cookbook updated for the new ``init`` behavior
- Version bump across package metadata and community docs

## 1.3.1

### Added

- Optional lockfile generation for scaffolds: `--lock` with `-m uv` or `-m poetry` (`uv lock` / `poetry lock`)
- Example plugin packages under `examples/`: `auto-gen-py-project-fastapi`, `-django`, `-ai`
- CLI resolves plugin template ids (e.g. `fastapi-extended`) for `new` / `init`

### Fixed

- Template entry-point loader correctly handles callable `get_root()` helpers

### Changed

- Confirmed v1.3.0 on TestPyPI and PyPI; TODO updated
- Version bump across package metadata and community docs

## 1.3.0

### Added

- Declared **Windows, macOS, and Linux** support in PyPI classifiers, README, FAQ, and `doctor`
- Platform badge and supported-platforms table in README
- OS-specific PATH fix hints in `doctor` (PowerShell on Windows; `export PATH=…` on macOS/Linux)

### Changed

- CI already matrix-tests Ubuntu, Windows, and macOS (Python 3.12 / 3.13) — documented as supported platforms
- Version bump across package metadata and community docs

## 1.2.9

### Fixed

- CI `doctor` test expects display name **Auto-Gen-Py-Project** (unblocks PyPI publish after v1.2.8)

### Changed

- Version bump across package metadata and community docs

## 1.2.8

### Changed

- Version / doctor / wizard UI title shows **Auto-Gen-Py-Project** (CLI command name unchanged)
- Version bump across package metadata and community docs

## 1.2.7

### Changed

- Package metadata author set to **Axcel Blade** (was ΓÇ£auto-gen-py-project contributorsΓÇ¥)
- Version bump across package metadata and community docs

## 1.2.6

### Added

- Root flags `--version` / `-V` (same output as `auto-gen-py-project version`)
- `doctor` reports whether the CLI is on `PATH` and prints Windows Scripts PATH fix help

### Changed

- `version` prints a plain `auto-gen-py-project X.Y.Z` line plus a panel
- README documents version checks and the `python -m auto_gen_py_project` fallback
- Version bump across package metadata and community docs

## 1.2.5

### Added

- CD publishes to **production PyPI** after TestPyPI on each GitHub Release (`PYPI_API_TOKEN` / Trusted Publisher)

### Changed

- Documented dual TestPyPI + PyPI publishing in `docs/publishing.md`
- Version bump across package metadata and community docs

## 1.2.4

### Changed

- Dropped ΓÇ£AI-readyΓÇ¥ marketing from README and docs; packaging is a template scaffolder only
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
