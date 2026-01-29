from pathlib import Path

def create_project(project_name: str) -> None:
    root = Path(project_name)
    package_name = project_name.replace("-", "_")
    package = root / package_name

    # Create directories
    (package).mkdir(parents=True, exist_ok=True)
    (root / "tests").mkdir(exist_ok=True)

    # Package files
    (package / "__init__.py").write_text("")
    (package / "core.py").write_text(
        "def hello():\n"
        "    return 'Hello from your new Python project'\n"
    )

    # Tests
    (root / "tests" / "test_core.py").write_text(
        f"from {package_name}.core import hello\n\n"
        "def test_hello():\n"
        "    assert hello()\n"
    )

    # README
    (root / "README.md").write_text(
        f"# {project_name}\n\n"
        "Generated using auto-gen-py-project\n"
    )

    # pyproject.toml
    (root / "pyproject.toml").write_text(
        f"""
[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[project]
name = "{project_name}"
version = "0.1.0"
description = "Auto generated Python project"
requires-python = ">=3.8"
""".strip()
    )

    # .gitignore
    (root / ".gitignore").write_text(
        "__pycache__/\n"
        "*.pyc\n"
        ".env\n"
        "dist/\n"
        "build/\n"
    )

    # LICENSE
    (root / "LICENSE").write_text("MIT License\n")

    print(f"✅ Project '{project_name}' created successfully")
