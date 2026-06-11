# auto_gen_py_project/generator.py

import venv
from pathlib import Path

# ---------------------------------------------------------------------------
# File templates
# ---------------------------------------------------------------------------

_BUILD_PY_TEMPLATE = '''\
"""pybuild.py — pybuild task definitions for {project_name}.

Run tasks with:
  pybuild <task>              # e.g. pybuild build
  pybuild --list              # list all tasks (grouped)
  pybuild --dry-run build     # preview without executing
  pybuild --parallel build    # run independent tasks concurrently
  pybuild --continue build    # keep going after a failure
  python pybuild.py <task>    # without installing pybuild
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path

from auto_gen_py_project.build_system import task, run_task


# ---------------------------------------------------------------------------
# Verification group
# ---------------------------------------------------------------------------

@task(group="verification")
def clean():
    """Remove build artefacts (build/, dist/, __pycache__, htmlcov, .pytest_cache)."""
    for d in ("build", "dist", "__pycache__", ".pytest_cache", "htmlcov"):
        shutil.rmtree(d, ignore_errors=True)
    for p in Path(".").rglob("*.pyc"):
        p.unlink(missing_ok=True)


@task(depends_on=["clean"], group="verification")
def lint():
    """Run ruff linter (skipped gracefully if ruff is not installed)."""
    result = subprocess.run(
        [sys.executable, "-m", "ruff", "check", "src/", "tests/"],
        capture_output=True,
        text=True,
    )
    if result.returncode not in (0, 127):
        print(result.stdout)
        raise RuntimeError("Lint errors found — see output above.")
    if result.returncode == 127:
        print("  ruff not installed, skipping lint.")


@task(depends_on=["lint"], group="verification")
def typecheck():
    """Run mypy static type checker (skipped if mypy is not installed)."""
    result = subprocess.run(
        [sys.executable, "-m", "mypy", "src/", "--ignore-missing-imports"],
        capture_output=True,
        text=True,
    )
    if result.returncode == 127 or "No module named mypy" in result.stderr:
        print("  mypy not installed, skipping typecheck.")
    elif result.returncode != 0:
        print(result.stdout)
        raise RuntimeError("Type errors found — see output above.")


@task(depends_on=["lint"], group="verification")
def test():
    """Run the full test suite with pytest (JUnit XML written to build/test-results/)."""
    Path("build/test-results").mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            sys.executable, "-m", "pytest", "tests/", "-v", "--tb=short",
            "--junit-xml=build/test-results/test.xml",
        ],
        check=True,
    )


@task(depends_on=["lint"], group="verification")
def coverage():
    """Run tests with coverage — HTML report in build/reports/coverage/, XML for CI."""
    Path("build/test-results").mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            sys.executable, "-m", "pytest", "tests/",
            "--cov=src",
            "--cov-report=html:build/reports/coverage",
            "--cov-report=xml:build/reports/coverage.xml",
            "--cov-report=term-missing",
            "--junit-xml=build/test-results/test.xml",
        ],
        check=True,
    )


@task(depends_on=["lint", "test"], group="verification")
def check():
    """Run all verification tasks — lint + tests (equivalent to Gradle check)."""
    print("  All verification checks passed.")


# ---------------------------------------------------------------------------
# Build group
# ---------------------------------------------------------------------------

@task(group="build")
def assemble():
    """Package the project without running tests (equivalent to Gradle assemble)."""
    subprocess.run([sys.executable, "-m", "build"], check=True)


@task(depends_on=["test"], group="build")
def build():
    """Full build: run tests then package wheel + sdist (equivalent to Gradle build)."""
    subprocess.run([sys.executable, "-m", "build"], check=True)


@task(
    depends_on=["build"],
    group="build",
    only_if=lambda: os.environ.get("PUBLISH_ENABLED", "").lower() == "true",
)
def publish():
    """Upload dist/ to PyPI via twine (requires PUBLISH_ENABLED=true and TWINE_* env vars)."""
    subprocess.run(
        [sys.executable, "-m", "twine", "upload", "dist/*"],
        check=True,
    )


# ---------------------------------------------------------------------------
# Application group
# ---------------------------------------------------------------------------

@task(group="application")
def run():
    """Run the application entry point (src/main.py)."""
    subprocess.run([sys.executable, "src/main.py"], check=True)


# ---------------------------------------------------------------------------
# Utility group
# ---------------------------------------------------------------------------

@task(group="utility")
def lock():
    """Freeze the current environment into requirements.lock (reproducible installs)."""
    result = subprocess.run(
        [sys.executable, "-m", "pip", "freeze", "--exclude-editable"],
        capture_output=True,
        text=True,
        check=True,
    )
    Path("requirements.lock").write_text(result.stdout)
    print(f"  Wrote requirements.lock ({{len(result.stdout.splitlines())}} packages)")


@task(group="utility")
def check_env():
    """Print Python version and environment info."""
    print(f"  Python : {{sys.version}}")
    print(f"  CWD    : {{Path.cwd()}}")
    print(f"  Dist   : {{'present' if Path('dist').exists() else 'absent'}}")
    print(f"  .venv  : {{'present' if Path('.venv').exists() else 'absent'}}")


# ---------------------------------------------------------------------------
# Direct execution: python pybuild.py <task>
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "build"
    run_task(target)
'''

_PYPROJECT_TOML_TEMPLATE = """\
[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[project]
name = "{project_name}"
version = "0.1.0"
description = "Auto generated Python project"
requires-python = ">=3.8"
dependencies = []

[project.optional-dependencies]
# Runtime extras (equivalent to Gradle runtimeOnly)
extras = []
# Development dependencies: linting, testing, type checking
dev = [
    "pytest>=7.0",
    "pytest-cov>=4.0",
    "pytest-xdist>=3.0",
    "ruff>=0.1",
    "mypy>=1.0",
    "build>=1.0",
    "twine>=5.0",
]
# Test-only dependencies (equivalent to Gradle testImplementation)
test = [
    "pytest>=7.0",
    "pytest-cov>=4.0",
    "pytest-xdist>=3.0",
]
# Lint-only dependencies (equivalent to Gradle compileOnly for static analysis)
lint = [
    "ruff>=0.1",
    "mypy>=1.0",
]

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "--tb=short"

[tool.coverage.run]
source = ["src"]
omit = ["tests/*"]

[tool.coverage.report]
show_missing = true
"""

_CI_YML_TEMPLATE = """\
name: CI

on:
  push:
    branches: [main, develop, "feature/**", "release/**", "hotfix/**"]
  pull_request:
    branches: [main, develop]

concurrency:
  group: ci-${{ github.ref }}
  cancel-in-progress: true

jobs:
  test:
    name: Test (Python ${{ matrix.python-version }})
    runs-on: ubuntu-latest
    strategy:
      fail-fast: true
      matrix:
        python-version: ["3.9", "3.11", "3.13"]

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
          cache: pip

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -e ".[dev]"

      - name: Lint
        run: python -m ruff check src/ tests/

      - name: Run tests
        run: |
          mkdir -p build/test-results
          python -m pytest tests/ -v --tb=short \\
            --junit-xml=build/test-results/test.xml

      - name: Upload test results
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: test-results-${{ matrix.python-version }}
          path: build/test-results/
          retention-days: 7

  coverage:
    name: Coverage report
    runs-on: ubuntu-latest
    needs: test

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.x"
          cache: pip

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -e ".[dev]"

      - name: Run coverage
        run: |
          mkdir -p build/reports
          python -m pytest tests/ \\
            --cov=src \\
            --cov-report=xml:build/reports/coverage.xml \\
            --cov-report=html:build/reports/coverage \\
            --cov-report=term-missing

      - name: Upload coverage report
        uses: actions/upload-artifact@v4
        with:
          name: coverage-report
          path: build/reports/
          retention-days: 14

  build-check:
    name: Build verification
    runs-on: ubuntu-latest
    needs: test

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.x"
          cache: pip

      - name: Install build tooling
        run: python -m pip install build twine

      - name: Build distributions
        run: python -m build

      - name: Verify distributions with twine
        run: python -m twine check dist/*
"""

_PYBUILD_WRAPPER_UNIX = """\
#!/usr/bin/env bash
# pybuild — project-local wrapper (equivalent to Gradle Wrapper)
# Runs pybuild using the project's .venv so the correct version is always used.
set -e
PYTHON=".venv/bin/python"
if [ ! -f "$PYTHON" ]; then
    echo "[pybuild] .venv not found. Bootstrap with:"
    echo "  python -m venv .venv && .venv/bin/pip install -e '.[dev]'"
    exit 1
fi
exec "$PYTHON" -m auto_gen_py_project.build_system.cli "$@"
"""

_PYBUILD_WRAPPER_BAT = """\
@echo off
rem pybuild.bat — project-local wrapper (equivalent to Gradle Wrapper)
rem Runs pybuild using the project's .venv so the correct version is always used.
set PYTHON=.venv\\Scripts\\python.exe
if not exist "%PYTHON%" (
    echo [pybuild] .venv not found. Bootstrap with:
    echo   python -m venv .venv ^&^& .venv\\Scripts\\pip install -e ".[dev]"
    exit /b 1
)
"%PYTHON%" -m auto_gen_py_project.build_system.cli %*
"""

_CONFTEST_TEMPLATE = """\
# tests/conftest.py — shared pytest fixtures for {project_name}
import sys
from pathlib import Path

# Ensure src/ is on the import path for all tests
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
"""

_TEST_MAIN_TEMPLATE = """\
from src.main import main


def test_main_runs(capsys):
    main()
    out = capsys.readouterr().out
    assert "Hello" in out
"""

_GITIGNORE_CONTENT = """\
__pycache__/
*.pyc
*.pyo
*.pyd
.venv/
.env
dist/
build/
*.egg-info/
htmlcov/
.coverage
.coverage.*
coverage.xml
*.xml
requirements.lock
.pytest_cache/
.mypy_cache/
.ruff_cache/
"""


# ---------------------------------------------------------------------------
# Project creator
# ---------------------------------------------------------------------------

def create_project(project_name: str, init_in_current_folder: bool = False) -> None:
    """Create a new Python project with a Gradle-equivalent structure.

    Args:
        project_name: Name of the project.
        init_in_current_folder: If True, scaffold into the current directory.
    """
    root = Path(".") if init_in_current_folder else Path(project_name)

    src = root / "src"
    resources = src / "resources"
    tests = root / "tests"
    github_workflows = root / ".github" / "workflows"

    # Create directories
    for d in (src, resources, tests, github_workflows):
        d.mkdir(parents=True, exist_ok=True)

    # Source files
    (src / "__init__.py").write_text("")
    (src / "main.py").write_text(
        "def main() -> None:\n"
        "    print('Hello World!')\n"
        "\n"
        "if __name__ == '__main__':\n"
        "    main()\n"
    )

    # Resources placeholder
    (resources / ".gitkeep").write_text("")

    # Tests
    (tests / "conftest.py").write_text(
        _CONFTEST_TEMPLATE.format(project_name=project_name)
    )
    (tests / "test_main.py").write_text(_TEST_MAIN_TEMPLATE)

    # Project metadata
    (root / "README.md").write_text(
        f"# {project_name}\n\n"
        "Generated using [auto-gen-py-project](https://github.com/axcel-blade/auto-gen-py-project)\n\n"
        "## Quick start\n\n"
        "```bash\n"
        "python -m venv .venv\n"
        "# Windows\n"
        ".venv\\Scripts\\pip install -e \".[dev]\"\n"
        "# macOS / Linux\n"
        ".venv/bin/pip install -e \".[dev]\"\n\n"
        "pybuild build        # or: python pybuild.py build\n"
        "pybuild --list       # show all available tasks\n"
        "```\n"
    )

    (root / "pyproject.toml").write_text(
        _PYPROJECT_TOML_TEMPLATE.format(project_name=project_name)
    )

    (root / ".gitignore").write_text(_GITIGNORE_CONTENT)
    (root / "LICENSE").write_text("MIT License\n")

    # Wrapper scripts (Gradle Wrapper equivalent)
    unix_wrapper = root / "pybuild"
    unix_wrapper.write_text(_PYBUILD_WRAPPER_UNIX)
    try:
        unix_wrapper.chmod(0o755)
    except Exception:
        pass  # chmod may fail on Windows — that's fine

    (root / "pybuild.bat").write_text(_PYBUILD_WRAPPER_BAT)

    # Build task file
    (root / "pybuild.py").write_text(
        _BUILD_PY_TEMPLATE.format(project_name=project_name)
    )

    # GitHub Actions CI
    (github_workflows / "ci.yml").write_text(_CI_YML_TEMPLATE)

    # Virtual environment
    venv_path = root / ".venv"
    venv.EnvBuilder(with_pip=True).create(str(venv_path))
    venv_path.mkdir(parents=True, exist_ok=True)

    location = "current folder" if init_in_current_folder else f"'{project_name}'"
    print(f"Project '{project_name}' created successfully in {location}")
