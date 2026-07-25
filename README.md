# auto-gen-py-project

Python project generator — scaffolds production-ready repos from templates, with plugins, an interactive wizard, and optional tooling (Docker, GitHub Actions, pre-commit, venv).

[![CI](https://github.com/axcel-blade/Auto-Gen-Py-Project/actions/workflows/ci.yml/badge.svg)](https://github.com/axcel-blade/Auto-Gen-Py-Project/actions/workflows/ci.yml)
[![PyPI version](https://img.shields.io/badge/version-1.3.4-blue.svg)](https://pypi.org/project/auto-gen-py-project/)
[![Python 3.12+](https://img.shields.io/badge/python-3.12%2B-blue.svg)](https://www.python.org/downloads/)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)](https://pypi.org/project/auto-gen-py-project/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE.md)

## Install

```bash
pip install --upgrade auto-gen-py-project
```

From source:

```bash
python -m pip install -e ".[dev]"
```

### Show version

```bash
auto-gen-py-project version
# or
auto-gen-py-project --version
```

If the `auto-gen-py-project` command is not recognized, the scripts folder is not on `PATH` (can happen on Windows, macOS, or Linux). Use:

```bash
python -m auto_gen_py_project version
```

Then run `python -m auto_gen_py_project doctor` for OS-specific PATH fix instructions.

## Supported platforms

| OS | Support | Notes |
|----|---------|--------|
| **Windows** | Yes | PowerShell / CMD; use `python -m …` if Scripts is not on PATH |
| **macOS** | Yes | Terminal / zsh; same CLI and templates |
| **Linux** | Yes | Ubuntu and other distros; CI runs on Ubuntu |

Requires **Python 3.12+**. CI tests all three OSes on Python 3.12 and 3.13.

## Quick start

Flag style (recommended on every OS — Windows, macOS, Linux):

```bash
# Create project files in the current folder
auto_gen_py_project --init --force

# Or into a specific folder
auto_gen_py_project --init --path ./myapp --name myapp --force

auto_gen_py_project --version
auto_gen_py_project --doctor
auto_gen_py_project --list-templates
auto_gen_py_project --create
```

Also available as `python -m auto_gen_py_project …` and hyphenated `auto-gen-py-project …`.

Subcommands still work:

```bash
# Plain init: creates ./my-project/ with a simple Python library inside
auto_gen_py_project init

# Named root folder
auto_gen_py_project init --name CoolLib

# Explicit path (folder is created if missing)
auto_gen_py_project init ./services/api -n api -t library

auto_gen_py_project create
auto_gen_py_project new MyApp --template fastapi --docker
auto_gen_py_project list-templates
auto_gen_py_project doctor
```

Also available as: `python -m auto_gen_py_project …`

## Commands

| Command | Description |
|---------|-------------|
| `init` / `--init` | Create a simple Python project in a folder (`--init` = current/specific folder) |
| `create` | Interactive wizard |
| `new NAME` | Create a project from a template |
| `list-templates` | List templates / project types |
| `install-template` | Install a template plugin (or local sample) |
| `doctor` | Environment diagnostics |
| `update` | Upgrade from PyPI |
| `version` | Show version (`1.3.4`) |
| `config` | Show / write user defaults |
| `plugin list\|install\|remove` | Plugin management |

## Lockfiles (uv / poetry)

```bash
auto-gen-py-project new App -t library -m uv --lock
auto-gen-py-project init ./svc -n svc -t fastapi -m poetry --lock
```

Requires the `uv` or `poetry` binary on `PATH`. Soft-fails with a warning if missing.

## Project types

`library`, `cli`, `fastapi`, `flask`, `django`, `data-science`, `machine-learning`, `ai`, `computer-vision`, `rest-api`, `microservice`, `desktop`, `automation`, `async`, `pypi-package`, `jupyter`

## Configuration

User defaults (TOML / YAML / JSON), searched in the current directory, `~/.config/auto-gen-py-project/`, and `$HOME`:

- `auto-gen-py-project.toml`
- `auto-gen-py-project.yaml`
- `auto-gen-py-project.json`

Example:

```toml
[defaults]
author = "Ada Lovelace"
email = "ada@example.com"
license = "MIT"
python_version = "3.12"
package_manager = "pip"
generate_lock = false
ci_provider = "github-actions"
use_docker = false
use_git = true
```

## Plugins

Third-party packages can expose entry points:

```toml
[project.entry-points."auto_gen_py_project.plugins"]
my = "my_pkg.plugin:MyPlugin"

[project.entry-points."auto_gen_py_project.templates"]
extra = "my_pkg.templates:get_root"
```

```bash
# Local example plugins (see examples/)
pip install -e ./examples/auto-gen-py-project-fastapi
pip install -e ./examples/auto-gen-py-project-django
pip install -e ./examples/auto-gen-py-project-ai
auto-gen-py-project list-templates
auto-gen-py-project new Demo -t fastapi-extended
auto-gen-py-project plugin list
```

## Template hints

Pass a short description to pick a matching built-in template by keywords (no external services):

```bash
auto-gen-py-project new Shop --describe "FastAPI inventory service with Docker"
```

## Documentation

- [User guide](docs/user-guide.md)
- [Templates & plugins](docs/templates-plugins.md)
- [API](docs/api.md)
- [Changelog](CHANGELOG.md)
- [Roadmap](ROADMAP.md)
- [Wiki pages](wiki/Home.md)

## Development

```bash
python -m pip install -e ".[dev]"
pytest
```

Git Flow branches: `main`, `develop`, `feature/*`, `release/*`, `hotfix/*`.

## License

MIT — see [LICENSE.md](LICENSE.md).
