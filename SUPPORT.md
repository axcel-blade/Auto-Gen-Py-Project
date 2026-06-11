# Support

## How to Get Help

### Bug Reports & Feature Requests

Open an issue on [GitHub Issues](https://github.com/axcel-blade/auto-gen-py-project/issues).

Use the appropriate issue template:
- **Bug report** — for unexpected behavior or errors
- **Feature request** — for new functionality

### Questions & Discussions

For general questions, use [GitHub Discussions](https://github.com/axcel-blade/auto-gen-py-project/discussions).

### Security & Sensitive Matters

For security vulnerabilities or sensitive reports, see [SECURITY.md](SECURITY.md) and open a [GitHub Issue](https://github.com/axcel-blade/Auto-Gen-Py-Project/issues/new).

---

## Useful Resources

| Resource | Description |
|---|---|
| [README.md](README.md) | Installation, usage, and full pybuild CLI reference |
| [PYTHON_BUILD_FEATURES.md](PYTHON_BUILD_FEATURES.md) | Complete Gradle → pybuild feature mapping |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Git Flow workflow, branch model, CI overview, release process |
| [CHANGELOG.md](CHANGELOG.md) | Full version history |

---

## Common Issues

| Problem | Solution |
|---|---|
| `pybuild: command not found` | Run `pip install -e .` or use `python pybuild.py <task>` |
| `TaskNotFoundError` | Run `pybuild --list` to see all available tasks |
| `CyclicDependencyError` | Review `depends_on` chains in `pybuild.py` for circular references |
| Task always re-runs | Declare `inputs=` and `outputs=` on the task to enable UP-TO-DATE skipping |
| Build file not found | Run from the directory containing `pybuild.py`, or pass `-f path/to/pybuild.py` |
| Coverage task fails | Install `pytest-cov`: `pip install pytest-cov` or `pip install -e ".[dev]"` |
