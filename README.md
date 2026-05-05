# auto-gen-py-project

Simple CLI tool that generates a clean Python project structure with modern packaging files and starter code.

## Description

`auto-gen-py-project` scaffolds a standards-aligned Python project so you can skip repetitive setup and start development quickly. It creates a ready-to-run structure that includes a `src/` package, tests, `run.py`, `pyproject.toml`, `README.md`, `LICENSE`, and `.gitignore`. The generated output follows modern Python packaging practices (PEP 517 / PEP 621 style) and supports cross-platform usage on Windows, Linux, and macOS.

## Getting Started

### Dependencies

- Python 3.8+ recommended
- `pip` available in your environment
- Tested for Windows, Linux, and macOS

### Installing

Install from this repository root:

```bash
python -m pip install --upgrade build
python -m pip install .
```

### Executing program

Create a new project folder:

```bash
auto-gen-py-project my_project
```

Initialize in the current folder:

```bash
python -m auto_gen_py_project my_project --init
```

If the CLI executable is on your `PATH`, you can also run:

```bash
auto-gen-py-project my_project --init
```

During development, you can run:

```bash
python run.py
```

`run.py` adds `src/` to the import path and executes `main()`.

Generated project structure:

```text
my_project/
├── src/
│   ├── __init__.py
│   └── main.py
├── tests/
│   └── test_main.py
├── run.py
├── README.md
├── pyproject.toml
├── LICENSE
└── .gitignore
```

## Help

If the command is not recognized, run it via module mode:

```bash
python -m auto_gen_py_project --help
```

If installation issues occur, verify your Python and pip setup:

```bash
python --version
python -m pip --version
```

## Authors

- AXCEL BLADE

## Version History

- 0.1
  - Initial release with project scaffolding CLI

## License

This project is licensed under the GNU General Public License v3 - see the `LICENSE` file for details.

## Acknowledgments

- Python packaging standards (PEP 517 / PEP 621)
- GitHub Actions and PyPA publishing workflow references
