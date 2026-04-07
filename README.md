# auto-gen-py-project

🚀 **auto-gen-py-project** is a lightweight Python CLI tool that instantly scaffolds a clean, modern, standards-compliant Python project — so you can skip the boilerplate and get straight to building.

Built around current Python best practices (**PEP 517 / PEP 621**).

---

## ✨ Features

- 📁 Standard `src/` layout with a ready-to-run entry point
- ⚡ One-command project creation
- 🧪 Test setup included out of the box
- 🛠️ Modern `pyproject.toml` based packaging
- 🖥️ Cross-platform: Windows, Linux, macOS
- 📂 Optional in-place initialization with `-i`
- 🔗 Zero runtime dependencies

---

## 🚀 Installation

```bash
python -m pip install --upgrade build
python -m pip install .
```

---

## 🚀 Usage

### Create a new project folder

```bash
auto-gen-py-project my_project
```

Creates a new `my_project/` folder with the full project structure inside.

### Initialize in the current folder

```bash
mkdir my_project && cd my_project
auto-gen-py-project my_project -i
# or
auto-gen-py-project my_project --init
```

### If the CLI is not on your PATH

```bash
python -m auto_gen_py_project my_project
python -m auto_gen_py_project my_project -i
```

---

## 📁 Generated Project Structure

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

`run.py` at the project root adds `src/` to the Python path and calls `main()`, giving you a convenient entry point during development:

```bash
python run.py
```

---

## 📌 Command Line Options

| Flag | Long Form | Description |
|------|-----------|-------------|
| `-i` | `--init` | Initialize in the current folder instead of creating a new one |

---

## 📜 License

GNU General Public License v3