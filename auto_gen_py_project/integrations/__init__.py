"""Optional integrations applied after template rendering."""

from __future__ import annotations

import shutil
import subprocess
import sys
import venv
from pathlib import Path
from typing import Optional

from auto_gen_py_project.core.models import PackageManager, ProjectSpec
from auto_gen_py_project.logging import get_logger
from auto_gen_py_project.utilities import ensure_dir, write_text

logger = get_logger(__name__)


def init_git(dest: Path) -> None:
    if not shutil.which("git"):
        logger.warning("git not found; skipping repository init")
        return
    if (dest / ".git").exists():
        return
    subprocess.run(["git", "init"], cwd=dest, check=False, capture_output=True)
    subprocess.run(["git", "add", "."], cwd=dest, check=False, capture_output=True)
    subprocess.run(
        ["git", "commit", "-m", "Initial commit from auto-gen-py-project"],
        cwd=dest,
        check=False,
        capture_output=True,
    )
    logger.info("Initialized git repository")


def create_virtualenv(dest: Path, name: str = ".venv") -> Path:
    path = dest / name
    if path.exists():
        return path
    venv.create(path, with_pip=True)
    logger.info("Created virtualenv at %s", path)
    return path


def install_dependencies(dest: Path, spec: ProjectSpec, venv_path: Optional[Path] = None) -> None:
    python = sys.executable
    if venv_path:
        if sys.platform == "win32":
            python = str(venv_path / "Scripts" / "python.exe")
        else:
            python = str(venv_path / "bin" / "python")

    pm = spec.package_manager
    try:
        if pm == PackageManager.UV and shutil.which("uv"):
            subprocess.check_call(["uv", "sync"], cwd=dest)
        elif pm == PackageManager.POETRY and shutil.which("poetry"):
            subprocess.check_call(["poetry", "install"], cwd=dest)
        elif pm == PackageManager.PDM and shutil.which("pdm"):
            subprocess.check_call(["pdm", "install"], cwd=dest)
        elif pm == PackageManager.HATCH and shutil.which("hatch"):
            subprocess.check_call(["hatch", "env", "create"], cwd=dest)
        else:
            req = dest / "requirements.txt"
            if req.exists():
                subprocess.check_call([python, "-m", "pip", "install", "-r", str(req)], cwd=dest)
            else:
                subprocess.check_call([python, "-m", "pip", "install", "-e", ".[dev]"], cwd=dest)
        logger.info("Installed dependencies via %s", pm.value)
    except subprocess.CalledProcessError as exc:
        logger.warning("Dependency installation failed: %s", exc)


def write_docker_files(dest: Path, spec: ProjectSpec) -> None:
    if not spec.use_docker:
        return
    write_text(
        dest / "Dockerfile",
        f"""FROM python:{spec.python_version}-slim

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

COPY pyproject.toml README.md ./
COPY src ./src
RUN pip install --no-cache-dir .

CMD ["python", "-m", "{spec.package_name}"]
""",
    )
    write_text(dest / ".dockerignore", "__pycache__\n.venv\n.git\n.pytest_cache\ndist\nbuild\n")
    if spec.use_compose:
        write_text(
            dest / "docker-compose.yml",
            f"""services:
  app:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./:/app
""",
        )
    logger.info("Wrote Docker configuration")


def write_github_actions(dest: Path, spec: ProjectSpec) -> None:
    if spec.ci_provider != "github-actions":
        return
    workflow = dest / ".github" / "workflows" / "ci.yml"
    write_text(
        workflow,
        f"""name: CI

on:
  push:
    branches: [main, master]
  pull_request:

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["{spec.python_version}"]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{{{ matrix.python-version }}}}
      - name: Install
        run: |
          python -m pip install --upgrade pip
          pip install -e ".[dev]"
      - name: Test
        run: pytest -q --cov={spec.package_name}
""",
    )
    logger.info("Wrote GitHub Actions workflow")


def write_precommit(dest: Path, spec: ProjectSpec) -> None:
    if not spec.use_precommit:
        return
    write_text(
        dest / ".pre-commit-config.yaml",
        """repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.9.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v5.0.0
    hooks:
      - id: end-of-file-fixer
      - id: trailing-whitespace
""",
    )


def write_ide_configs(dest: Path, spec: ProjectSpec) -> None:
    if spec.vscode:
        ensure_dir(dest / ".vscode")
        write_text(
            dest / ".vscode" / "settings.json",
            """{
  "python.testing.pytestEnabled": true,
  "editor.formatOnSave": true,
  "[python]": {
    "editor.defaultFormatter": "charliermarsh.ruff"
  }
}
""",
        )
        write_text(
            dest / ".vscode" / "extensions.json",
            """{
  "recommendations": [
    "ms-python.python",
    "charliermarsh.ruff"
  ]
}
""",
        )
    if spec.pycharm:
        ensure_dir(dest / ".idea")
        write_text(
            dest / ".idea" / "misc.xml",
            f"""<?xml version="1.0" encoding="UTF-8"?>
<project version="4">
  <component name="ProjectRootManager" version="2" languageLevel="JDK_17" />
</project>
""",
        )


def apply_integrations(dest: Path, spec: ProjectSpec) -> None:
    write_docker_files(dest, spec)
    write_github_actions(dest, spec)
    write_precommit(dest, spec)
    write_ide_configs(dest, spec)
    venv_path = None
    if spec.create_venv:
        venv_path = create_virtualenv(dest)
    if spec.install_deps:
        install_dependencies(dest, spec, venv_path)
    if spec.use_git:
        init_git(dest)
