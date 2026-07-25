# TODO

Task tracking for **auto-gen-py-project** v1.3.3+.

## Near term

- [x] Confirm v1.3.0 on TestPyPI and PyPI via CD (`TEST_PYPI_API_TOKEN` / `PYPI_API_TOKEN`)
- [x] Enable production PyPI deploy in CD
- [x] Add `uv`/`poetry` lockfile generation options for scaffolds (`--lock`, `-m`)
- [ ] Add end-to-end snapshot tests for each built-in project type
- [ ] Document custom template authoring with more examples

## Plugin ecosystem

- [x] Example plugin package `auto-gen-py-project-fastapi` (extended template)
- [x] Example plugin package `auto-gen-py-project-django`
- [x] Example plugin package `auto-gen-py-project-ai`

## Quality

- [ ] Raise coverage toward 90%+ on core generator paths
- [ ] Add mypy strict checking in CI
- [ ] Add pre-commit config to this repository

## Docs

- [ ] Expand wiki Cookbook pages
- [ ] Record a short CLI demo GIF for the README
