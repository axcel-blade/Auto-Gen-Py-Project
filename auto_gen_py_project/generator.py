# auto_gen_py_project/generator.py

import venv
from pathlib import Path

_BUILD_PY_TEMPLATE = '''\
"""pybuild.py — pybuild task definitions for {project_name}.

Run tasks with:
  pybuild <task>           # e.g. pybuild build
  pybuild --list           # list all tasks
  python pybuild.py <task> # without installing pybuild
"""

import shutil
import subprocess
import sys
from pathlib import Path

from auto_gen_py_project.build_system import task, run_task


# ---------------------------------------------------------------------------
# Task definitions
# ---------------------------------------------------------------------------

@task
def clean():
    """Remove build artefacts."""
    for d in ("build", "dist", "__pycache__", ".pytest_cache"):
        shutil.rmtree(d, ignore_errors=True)
    for p in Path(".").rglob("*.pyc"):
        p.unlink(missing_ok=True)


@task(depends_on=["clean"])
def test():
    """Run the test suite with pytest."""
    subprocess.run([sys.executable, "-m", "pytest", "tests/", "-v"], check=True)


@task(depends_on=["test"])
def build():
    """Build source distribution and wheel."""
    subprocess.run([sys.executable, "-m", "build"], check=True)


# ---------------------------------------------------------------------------
# Direct execution: python pybuild.py <task>
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "build"
    run_task(target)
'''


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
        ".venv/\n"
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

    # pybuild.py — Gradle-like task file (named pybuild.py to avoid shadowing the `build` package)
    (root / "pybuild.py").write_text(_BUILD_PY_TEMPLATE.format(project_name=project_name))

    # Create project-local virtual environment with pip.
    venv_path = root / ".venv"
    venv.EnvBuilder(with_pip=True).create(str(venv_path))
    # Some Windows path redirects can move the actual location; guarantee expected folder exists.
    venv_path.mkdir(parents=True, exist_ok=True)

    location = "current folder" if init_in_current_folder else f"'{project_name}'"
    print(f"✅ Project '{project_name}' created successfully in {location}")