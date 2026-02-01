# auto-gen-py-project

🚀 **auto-gen-py-project** is a lightweight Python CLI tool that instantly generates a clean, modern, and standards-compliant Python project structure.

Built around current Python best practices (**PEP 517 / PEP 621**), it helps you bootstrap projects consistently and quickly—so you can focus on writing code, not scaffolding.

Ideal for:
- 📦 Python libraries & packages
- 🖥️ Command-line tools
- 🤖 ML / AI projects
- 🛠️ Internal tooling
- 🌍 Open-source projects

---

## ✨ Features

- 📁 Generates a standard Python package layout
- ⚡ One-command project creation
- 🧪 Test setup included by default
- 🧩 Zero runtime dependencies
- 🛠️ Fully `pyproject.toml` based (modern Python)
- 🖥️ Cross-platform: Windows, Linux, macOS
- 📂 Optional in-place initialization with `-i` flag

---

## 🚀 Installation

Before installing, upgrade the build package:

```bash
python -m pip install --upgrade build
```

Then install the package:

```bash
python -m pip install .
```
---

## 🚀 Usage

### Create a new project folder

Generate a new Python project in a new folder:

```bash
auto-gen-py-project my_project
```

This creates a new folder named `my_project/` with the full project structure inside.

### Initialize in current folder

Initialize the project layout directly in the current folder without creating a subfolder:

```bash
mkdir my_project
cd my_project
auto-gen-py-project my_project -i
```

Or using the long form:

```bash
auto-gen-py-project my_project --init
```

If the CLI is not available on your PATH:

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
├── README.md
├── pyproject.toml
├── LICENSE
└── .gitignore
```

---

## 📌 Command Line Options

| Flag | Long Form | Description |
|------|-----------|-------------|
| `-i` | `--init` | Initialize project layout in current folder instead of creating a new folder |

---

## 📌 Why auto-gen-py-project?

- Enforces consistent project structure
- Encourages testing from day one
- Uses modern Python packaging standards
- Ideal for both quick prototypes and production-ready packages

---

## 📜 License

GNU General Public License v3