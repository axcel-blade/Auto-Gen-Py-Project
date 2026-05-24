"""build.py — pybuild task definitions for auto-gen-py-project.

Run tasks with:
  pybuild <task>         # e.g. pybuild build
  pybuild --list         # list all tasks
  python build.py <task> # without installing pybuild
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
    """Remove build artefacts (build/, dist/, __pycache__, .pytest_cache)."""
    for d in ("build", "dist", "__pycache__", ".pytest_cache"):
        shutil.rmtree(d, ignore_errors=True)
    for p in Path(".").rglob("*.pyc"):
        p.unlink(missing_ok=True)


@task(depends_on=["clean"])
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


@task(depends_on=["lint"])
def test():
    """Run the full test suite with pytest."""
    subprocess.run(
        [sys.executable, "-m", "pytest", "tests/", "-v", "--tb=short"],
        check=True,
    )


@task(depends_on=["test"])
def build():
    """Build source distribution and wheel into dist/."""
    subprocess.run([sys.executable, "-m", "build"], check=True)


@task(depends_on=["build"])
def publish():
    """Upload dist/ packages to PyPI via twine (requires TWINE_* env vars or ~/.pypirc)."""
    subprocess.run(
        [sys.executable, "-m", "twine", "upload", "dist/*"],
        check=True,
    )


# ---------------------------------------------------------------------------
# Direct execution: python build.py <task>
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "build"
    run_task(target)
