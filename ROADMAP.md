# Roadmap

Future plans for **auto-gen-py-project**.

## v1.3.x (current)

- Cross-platform CLI: **Windows, macOS, and Linux** (CI matrix + PyPI classifiers)
- MIT-licensed package distribution via **LICENSE.md**
- Release CD publishes **TestPyPI then PyPI** (OIDC Trusted Publisher or `TEST_PYPI_API_TOKEN` / `PYPI_API_TOKEN`)
- Stable CLI (`create`, `new`, `init`, plugins, doctor)
- Built-in scaffolds for common Python project types
- Config file defaults (TOML / YAML / JSON)
- Extensible plugin and template APIs
- Optional keyword-based template hints via `--describe`

## v1.3+

- Richer custom-template marketplace / install-from-git
- Optional interactive prompts declared in `template.json`
- Better package-manager-specific project files (Poetry/Hatch/PDM layouts)

## v1.4

- Richer template recommendation from project descriptions
- Post-generation “doctor” suggestions inside the new project

## v2.0

- Stable public plugin API (semver guarantees)
- Multi-language template packs beyond Python (if demand warrants)
- Workspace / monorepo generator mode

See also [TODO.md](TODO.md) for actionable checklist items and [CHANGELOG.md](CHANGELOG.md) for shipped work.
