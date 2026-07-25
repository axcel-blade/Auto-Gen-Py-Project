"""Unit tests for lockfile generation integration."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

from auto_gen_py_project.core.models import PackageManager, ProjectSpec
from auto_gen_py_project.integrations import generate_lockfile


def test_generate_lockfile_uv(tmp_path: Path):
    spec = ProjectSpec(
        name="Demo",
        package_name="demo",
        package_manager=PackageManager.UV,
        generate_lock=True,
        use_git=False,
    )
    with patch("auto_gen_py_project.integrations.shutil.which", return_value="/usr/bin/uv"):
        with patch("auto_gen_py_project.integrations.subprocess.check_call") as call:
            generate_lockfile(tmp_path, spec)
            call.assert_called_once_with(["uv", "lock"], cwd=tmp_path)


def test_generate_lockfile_poetry(tmp_path: Path):
    spec = ProjectSpec(
        name="Demo",
        package_name="demo",
        package_manager=PackageManager.POETRY,
        generate_lock=True,
        use_git=False,
    )
    with patch("auto_gen_py_project.integrations.shutil.which", return_value="/usr/bin/poetry"):
        with patch("auto_gen_py_project.integrations.subprocess.check_call") as call:
            generate_lockfile(tmp_path, spec)
            call.assert_called_once_with(["poetry", "lock"], cwd=tmp_path)


def test_generate_lockfile_skipped_when_disabled(tmp_path: Path):
    spec = ProjectSpec(
        name="Demo",
        package_name="demo",
        package_manager=PackageManager.UV,
        generate_lock=False,
        use_git=False,
    )
    with patch("auto_gen_py_project.integrations.subprocess.check_call") as call:
        generate_lockfile(tmp_path, spec)
        call.assert_not_called()


def test_generate_lockfile_skipped_without_tool(tmp_path: Path):
    spec = ProjectSpec(
        name="Demo",
        package_name="demo",
        package_manager=PackageManager.UV,
        generate_lock=True,
        use_git=False,
    )
    with patch("auto_gen_py_project.integrations.shutil.which", return_value=None):
        with patch("auto_gen_py_project.integrations.subprocess.check_call") as call:
            generate_lockfile(tmp_path, spec)
            call.assert_not_called()
