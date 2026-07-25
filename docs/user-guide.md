# User guide

**auto-gen-py-project** v1.3.2 generates production-ready Python projects from templates on **Windows, macOS, and Linux** (Python 3.12+).

## Install

```bash
pip install auto-gen-py-project
# or from a clone
python -m pip install -e ".[dev]"
```

## Create a project

Interactive:

```bash
auto-gen-py-project create
```

Non-interactive:

```bash
auto-gen-py-project new PaymentsAPI -t fastapi --docker --venv --install
```

Initialize a simple Python project (creates the root folder):

```bash
auto-gen-py-project init
# → ./my-project/ with library scaffold

auto-gen-py-project init --name mylib
# → ./mylib/

auto-gen-py-project init ./service --name payments --template library
# → creates ./service/ if missing, then scaffolds inside
```

## What gets generated

- `pyproject.toml`, `README.md`, `LICENSE`, `.gitignore`, `.editorconfig`
- `src/<package>/`, `tests/`, `docs/`, `examples/`, `scripts/`, `assets/`
- Optional: Docker, docker-compose, GitHub Actions, pre-commit, VS Code settings
- Optional: git init, virtualenv, dependency install

## Package managers

Set `package_manager` in config or accept the wizard default: `pip`, `uv`, `poetry`, `hatch`, `pdm`.

Installation uses the selected tool when `--install` is enabled and the binary is available; otherwise pip is used.

## Custom templates

Create a folder with `template.json` and a `template/` directory of Jinja2 files (optional `.j2` suffix). Path segments may include `{{ package_name }}`.

See [templates-plugins.md](templates-plugins.md).
