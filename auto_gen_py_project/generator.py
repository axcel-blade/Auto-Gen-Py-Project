from pathlib import Path

def create_project(project_name: str, init_in_current_folder: bool = False) -> None:
    """
    Create a new Python project structure.
    
    Args:
        project_name: Name of the project
        init_in_current_folder: If True, creates files in current folder. 
                               If False, creates a new folder with project_name
    """
    if init_in_current_folder:
        root = Path(".")
    else:
        root = Path(project_name)
    
    #package_name = project_name.replace("-", "_")
    package_name = "src"
    package = root / package_name

    # Create directories
    (package).mkdir(parents=True, exist_ok=True)
    (root / "tests").mkdir(exist_ok=True)

    # Package files
    (package / "__init__.py").write_text("")
    (package / "main.py").write_text(
        "def main():\n"
        "    print('Hello World!')\n"
        "\n"
        "if __name__ == '__main__':\n"
        "    main()\n"
    )

    # Tests
    (root / "tests" / "test_main.py").write_text(
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

    # run.py
    (root / "run.py").write_text(
        '# run.py\n'
        '"""Project root entry point."""\n'
        '\n'
        'import sys\n'
        'import os\n'
        '\n'
        '# Add src/ to path so all modules can import each other by name\n'
        'sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))\n'
        '\n'
        'from main import main\n'
        '\n'
        'if __name__ == "__main__":\n'
        '    main()\n'
    )

    location = "current folder" if init_in_current_folder else f"'{project_name}'"
    print(f"✅ Project '{project_name}' created successfully in {location}")