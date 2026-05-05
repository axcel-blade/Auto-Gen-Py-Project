# auto-gen-py-project

Simple CLI tool that scaffolds a clean Python project structure with modern packaging files, tests, and a local virtual environment.

## Description

`auto-gen-py-project` helps you start Python projects faster by generating a standards-aligned layout out of the box. It creates a project with `src/`, tests, `run.py`, `pyproject.toml`, `.gitignore`, `LICENSE`, and a local `.venv` directory inside the generated project folder. The goal is to remove repetitive setup so you can focus on implementation.

## Getting Started

### Dependencies

- Python 3.8+ (3.10+ recommended)
- `pip` available in your environment
- OS: Windows, Linux, or macOS

### Installing

- Clone or download this repository:

```bash
git clone https://github.com/axcel-blade/auto-gen-py-project.git
cd auto-gen-py-project
```

- Install the CLI locally:

```bash
python -m pip install --upgrade pip build
python -m pip install .
```

### Executing program

- Create a new project folder:

```bash
auto-gen-py-project my_project
```

- Initialize in the current folder:

```bash
auto-gen-py-project my_project --init
```

- If command is not on your `PATH`, use module mode:

```bash
python -m auto_gen_py_project my_project
python -m auto_gen_py_project my_project --init
```

Generated project structure:

```text
my_project/
├── src/
│   ├── __init__.py
│   └── main.py
├── tests/
│   └── test_main.py
├── .venv/
├── run.py
├── README.md
├── pyproject.toml
├── LICENSE
└── .gitignore
```

## Help

For command options and usage help:

```bash
python -m auto_gen_py_project --help
```

If installation fails, check:

```bash
python --version
python -m pip --version
```

## Authors

- Axcel Blade

## Contributing

Contributions are welcome and appreciated.

1. Fork the project
2. Create your branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m "Add some AmazingFeature"`)
4. Push your branch (`git push origin feature/AmazingFeature`)
5. Open a pull request

## Version History

- 0.1.2
  - Create `.venv` inside generated project folders (including `--init`)
  - Add `.venv/` to generated `.gitignore`
- 0.1
  - Initial release

## License

This project is licensed under the GNU General Public License v3 - see the `LICENSE` file for details.
