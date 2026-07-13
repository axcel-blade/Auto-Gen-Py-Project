"""Integration tests for generator and CLI."""

from __future__ import annotations

from pathlib import Path

from typer.testing import CliRunner

from auto_gen_py_project.cli.app import app
from auto_gen_py_project.core.generator import ProjectGenerator
from auto_gen_py_project.core.models import ProjectSpec, ProjectType

runner = CliRunner()


def _out(result) -> str:
    return f"{result.stdout or ''}{getattr(result, 'stderr', '') or ''}{result.output or ''}"


def test_generator_creates_project(tmp_path: Path):
    dest = tmp_path / "demo"
    spec = ProjectSpec(
        name="Demo",
        package_name="demo",
        project_type=ProjectType.CLI,
        use_git=False,
        create_venv=False,
        install_deps=False,
        use_precommit=True,
        vscode=True,
    )
    path = ProjectGenerator().generate(spec, dest)
    assert (path / "pyproject.toml").exists()
    assert (path / "src" / "demo" / "cli.py").exists()
    assert (path / ".github" / "workflows" / "ci.yml").exists()
    assert (path / ".pre-commit-config.yaml").exists()
    assert (path / ".vscode" / "settings.json").exists()


def test_cli_version():
    result = runner.invoke(app, ["version"])
    assert result.exit_code == 0
    assert "1.1.0" in _out(result)


def test_cli_list_templates():
    result = runner.invoke(app, ["list-templates"])
    assert result.exit_code == 0
    text = _out(result)
    assert "library" in text
    assert "fastapi" in text


def test_cli_new(tmp_path: Path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    result = runner.invoke(
        app,
        ["new", "HelloWorld", "--template", "library", "--no-git", "--path", str(tmp_path / "hello-world")],
    )
    assert result.exit_code == 0, _out(result)
    assert (tmp_path / "hello-world" / "pyproject.toml").exists()


def test_cli_doctor():
    result = runner.invoke(app, ["doctor"])
    assert result.exit_code == 0
    assert "auto-gen-py-project" in _out(result)
