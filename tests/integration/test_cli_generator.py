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
    out = _out(result)
    assert "1.3.2" in out
    assert "Auto-Gen-Py-Project" in out


def test_cli_version_flag():
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    out = _out(result)
    assert "1.3.2" in out
    assert "Auto-Gen-Py-Project" in out


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


def test_cli_plain_init_creates_root_folder(tmp_path: Path, monkeypatch):
    """Plain `init` creates ./my-project/ with a simple library scaffold."""
    monkeypatch.chdir(tmp_path)
    result = runner.invoke(app, ["init", "--force"])
    assert result.exit_code == 0, _out(result)
    root = tmp_path / "my-project"
    assert root.is_dir()
    assert (root / "pyproject.toml").exists()
    assert (root / "src" / "my_project" / "__init__.py").exists()


def test_cli_init_named_folder(tmp_path: Path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    result = runner.invoke(app, ["init", "--name", "cool-lib", "--force"])
    assert result.exit_code == 0, _out(result)
    root = tmp_path / "cool-lib"
    assert (root / "pyproject.toml").exists(), _out(result)
    assert (root / "src" / "cool_lib" / "__init__.py").exists()


def test_cli_init_explicit_path_creates_folder(tmp_path: Path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    dest = tmp_path / "services" / "api"
    result = runner.invoke(app, ["init", str(dest), "-n", "api", "-t", "library", "--force"])
    assert result.exit_code == 0, _out(result)
    assert dest.is_dir()
    assert (dest / "pyproject.toml").exists()


def test_cli_doctor():
    result = runner.invoke(app, ["doctor"])
    assert result.exit_code == 0
    out = _out(result)
    assert "Auto-Gen-Py-Project" in out
    assert "1.3.2" in out
    assert "Windows, macOS, Linux" in out
