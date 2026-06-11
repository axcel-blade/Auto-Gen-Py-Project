"""pybuild.py — pybuild task definitions for auto-gen-py-project.

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
        [sys.executable, "-m", "ruff", "check", "auto_gen_py_project/", "tests/"],
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
    """Run mypy static type checker (auto-disabled when mypy is not installed)."""
    result = subprocess.run(
        [sys.executable, "-m", "mypy", "auto_gen_py_project/", "--ignore-missing-imports"],
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
            sys.executable, "-m", "pytest", "tests/test_build_system.py", "-v", "--tb=short",
            "--junit-xml=build/test-results/test.xml",
        ],
        check=True,
    )


@task(depends_on=["lint"], group="verification")
def coverage():
    """Run tests with coverage — HTML report in build/reports/coverage/, XML for CI."""
    Path("build/test-results").mkdir(parents=True, exist_ok=True)
    Path("build/reports").mkdir(parents=True, exist_ok=True)
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "--version"],
        capture_output=True,
        text=True,
    )
    cov_available = subprocess.run(
        [sys.executable, "-m", "pytest", "--co", "-q", "--cov=auto_gen_py_project",
         "tests/test_build_system.py"],
        capture_output=True,
        text=True,
    ).returncode != 5  # exit 5 = no tests found
    subprocess.run(
        [
            sys.executable, "-m", "pytest", "tests/test_build_system.py",
            "--cov=auto_gen_py_project",
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
    """Package wheel + sdist without running tests (equivalent to Gradle assemble)."""
    subprocess.run([sys.executable, "-m", "build"], check=True)


@task(depends_on=["test"], group="build")
def build():
    """Full build: tests then package wheel + sdist (equivalent to Gradle build)."""
    subprocess.run([sys.executable, "-m", "build"], check=True)


@task(
    depends_on=["build"],
    group="build",
    only_if=lambda: os.environ.get("PUBLISH_ENABLED", "").lower() == "true",
)
def publish():
    """Upload dist/ packages to PyPI (requires PUBLISH_ENABLED=true and TWINE_* env vars)."""
    subprocess.run(
        [sys.executable, "-m", "twine", "upload", "dist/*"],
        check=True,
    )


# ---------------------------------------------------------------------------
# Application group
# ---------------------------------------------------------------------------

@task(group="application")
def run():
    """Run the CLI entry point (auto-gen-py-project --help)."""
    subprocess.run(
        [sys.executable, "-m", "auto_gen_py_project.cli", "--help"],
        check=True,
    )


# ---------------------------------------------------------------------------
# Utility group
# ---------------------------------------------------------------------------

@task(group="utility")
def lock():
    """Freeze the installed environment into requirements.lock (reproducible installs)."""
    result = subprocess.run(
        [sys.executable, "-m", "pip", "freeze", "--exclude-editable"],
        capture_output=True,
        text=True,
        check=True,
    )
    Path("requirements.lock").write_text(result.stdout)
    print(f"  Wrote requirements.lock ({len(result.stdout.splitlines())} packages)")


@task(group="utility")
def check_env():
    """Print Python version and key environment info."""
    print(f"  Python : {sys.version}")
    print(f"  CWD    : {Path.cwd()}")
    print(f"  Dist   : {'present' if Path('dist').exists() else 'absent'}")
    print(f"  .venv  : {'present' if Path('.venv').exists() else 'absent'}")


# ---------------------------------------------------------------------------
# Direct execution: python pybuild.py <task>
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "build"
    run_task(target)
