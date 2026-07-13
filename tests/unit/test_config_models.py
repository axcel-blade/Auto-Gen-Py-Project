"""Unit tests for models and config."""

from __future__ import annotations

from pathlib import Path

from auto_gen_py_project.config import load_preferences, save_preferences
from auto_gen_py_project.core.models import ProjectSpec, ProjectType, UserPreferences


def test_normalize_package_name():
    assert ProjectSpec.normalize_package_name("My App!") == "my_app"
    assert ProjectSpec.normalize_package_name("123abc").startswith("pkg_")


def test_template_context():
    spec = ProjectSpec(name="Demo", package_name="demo", project_type=ProjectType.CLI)
    ctx = spec.template_context()
    assert ctx["project_slug"] == "demo"
    assert ctx["project_type"] == "cli"


def test_preferences_roundtrip(tmp_path: Path):
    prefs = UserPreferences(author="Ada", email="ada@example.com")
    path = tmp_path / "auto-gen-py-project.toml"
    save_preferences(prefs, path)
    loaded, found = load_preferences(path)
    assert found == path
    assert loaded.author == "Ada"
    assert loaded.email == "ada@example.com"
