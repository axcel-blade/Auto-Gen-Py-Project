# Roadmap

Future plans for **auto-gen-py-project**.

## v1.2.x (current)

- MIT-licensed package distribution
- Stable CLI (`create`, `new`, `init`, plugins, doctor)
- Built-in scaffolds for common Python project types
- Config file defaults (TOML / YAML / JSON)
- Extensible AI provider interface (heuristic default)

## v1.3

- Richer custom-template marketplace / install-from-git
- Optional interactive prompts declared in `template.json`
- Better package-manager-specific project files (Poetry/Hatch/PDM layouts)

## v1.4

- First-class AI-assisted generation plugins (opt-in)
- Template recommendation from natural-language descriptions with pluggable backends
- Post-generation “doctor” suggestions inside the new project

## v2.0

- Stable public plugin API (semver guarantees)
- Multi-language template packs beyond Python (if demand warrants)
- Workspace / monorepo generator mode

See also [TODO.md](TODO.md) for actionable checklist items and [CHANGELOG.md](CHANGELOG.md) for shipped work.
