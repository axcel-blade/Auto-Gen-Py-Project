# Contributing

Thanks for contributing to **auto-gen-py-project** (v1.2.1).

## Git Flow

| Branch | Purpose |
|--------|---------|
| `main` | Production-ready releases |
| `develop` | Integration branch for finished features |
| `feature/*` | New features and non-trivial changes |
| `release/*` | Release hardening (version bumps, docs, fixes) |
| `hotfix/*` | Urgent fixes branched from `main` |

Typical path: `feature/*` → `develop` → `release/x.y.z` → `main` (tag) and back-merge to `develop`.

## Setup

```bash
python -m pip install -e ".[dev]"
pytest
```

## Guidelines

- Python 3.12+, type hints, comments/docstrings on public APIs
- Keep generators, plugins, and CLI modular (SOLID / Clean Architecture)
- Add unit tests for new templates and integration tests for CLI flows
- Update `CHANGELOG.md`, `README.md`, and version strings (`pyproject.toml`, `auto_gen_py_project/__init__.py`) when releasing
- Do not commit secrets, caches, or generated `dist/` artifacts

## Pull requests

1. Branch from `develop` using `feature/<short-name>`
2. Run `pytest`
3. Open a PR into `develop` with a clear summary and test plan
4. Link related issues

See [.github/PULL_REQUEST_TEMPLATE.md](.github/PULL_REQUEST_TEMPLATE.md).

## License

Contributions are accepted under the project **MIT** license. See [LICENSE.md](LICENSE.md).
