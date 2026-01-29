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

---

## 🚀 Usage

Generate a new Python project:

```bash
auto-gen-py-project my_project
```

If the CLI is not available on your PATH:

```bash
python -m auto_gen_py_project my_project
```

---

## 📁 Generated Project Structure

```text
my_project/
├── my_project/
│   ├── __init__.py
│   └── core.py
├── tests/
│   └── test_core.py
├── README.md
├── pyproject.toml
├── LICENSE
└── .gitignore
```

---

## 📌 Why auto-gen-py-project?

- Enforces consistent project structure
- Encourages testing from day one
- Uses modern Python packaging standards
- Ideal for both quick prototypes and production-ready packages

---

## 📜 License

GNU General Public License v3