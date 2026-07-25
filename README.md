# auto-gen-py-project

Python project generator — scaffolds production-ready repos from templates, with plugins, an interactive wizard, and optional tooling (Docker, GitHub Actions, pre-commit, venv).

[![CI](https://github.com/axcel-blade/Auto-Gen-Py-Project/actions/workflows/ci.yml/badge.svg)](https://github.com/axcel-blade/Auto-Gen-Py-Project/actions/workflows/ci.yml)
[![PyPI version](https://img.shields.io/badge/version-1.2.9-blue.svg)](https://pypi.org/project/auto-gen-py-project/)
[![Python 3.12+](https://img.shields.io/badge/python-3.12%2B-blue.svg)](https://www.python.org/downloads/)
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

If PowerShell says the command is not recognized, the Scripts folder is not on `PATH`. Use:

```bash
python -m auto_gen_py_project version
```

Then run `python -m auto_gen_py_project doctor` for PATH fix instructions (common on Windows user installs).

## Quick start

```bash
auto-gen-py-project create
auto-gen-py-project new MyApp --template fastapi --docker
auto-gen-py-project init ./service --name payments --template microservice
auto-gen-py-project list-templates
auto-gen-py-project doctor
```

Also available as: `python -m auto_gen_py_project …`

## Commands

| Command | Description |
|---------|-------------|
| `init` | Non-interactive init into a directory |
| `create` | Interactive wizard |
| `new NAME` | Create a project from a template |
| `list-templates` | List templates / project types |
| `install-template` | Install a template plugin (or local sample) |
| `doctor` | Environment diagnostics |
| `update` | Upgrade from PyPI |
| `version` | Show version (`1.2.9`) |
| `config` | Show / write user defaults |
| `plugin list\|install\|remove` | Plugin management |

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
pip install auto-gen-py-project-fastapi
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
