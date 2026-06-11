"""pybuild.py — pybuild task definitions for auto-gen-py-project.

Run tasks with:
  pybuild <task>           # e.g. pybuild build
  pybuild --list           # list all tasks (grouped)
  pybuild --dry-run build  # preview without executing
  pybuild --parallel build # run independent tasks concurrently
  python pybuild.py <task> # without installing pybuild
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
    """Remove build artefacts (build/, dist/, __pycache__, .pytest_cache)."""
    for d in ("build", "dist", "__pycache__", ".pytest_cache"):
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
def test():
    """Run the full test suite with pytest."""
    subprocess.run(
        [sys.executable, "-m", "pytest", "tests/", "-v", "--tb=short"],
        check=True,
    )


# ---------------------------------------------------------------------------
# Build group
# ---------------------------------------------------------------------------

@task(depends_on=["test"], group="build")
def build():
    """Build source distribution and wheel into dist/."""
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
# Utility group
# ---------------------------------------------------------------------------

@task(group="utility")
def check_env():
    """Print Python version and key environment info."""
    print(f"  Python : {sys.version}")
    print(f"  CWD    : {Path.cwd()}")
    print(f"  Dist   : {'present' if Path('dist').exists() else 'absent'}")


@task(group="utility", enabled=bool(shutil.which("mypy")))
def typecheck():
    """Run mypy static type checker (auto-disabled when mypy is not installed)."""
    subprocess.run(
        [sys.executable, "-m", "mypy", "auto_gen_py_project/", "--ignore-missing-imports"],
        check=True,
    )


# ---------------------------------------------------------------------------
# Direct execution: python pybuild.py <task>
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "build"
    run_task(target)
