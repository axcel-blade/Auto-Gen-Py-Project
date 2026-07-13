"""Unit tests for scaffold and Jinja template engine."""

from __future__ import annotations

from pathlib import Path

from auto_gen_py_project.core.models import ProjectSpec, ProjectType
from auto_gen_py_project.core.scaffold import BuiltinScaffold
from auto_gen_py_project.template_engine import TemplateEngine, TemplateMeta
from auto_gen_py_project.templates import builtin_templates_root


def test_builtin_scaffold_library(tmp_path: Path):
    spec = ProjectSpec(name="Lib", package_name="lib_demo", project_type=ProjectType.LIBRARY)
    files = BuiltinScaffold().generate(tmp_path, spec)
    assert (tmp_path / "pyproject.toml").exists()
    assert (tmp_path / "src" / "lib_demo" / "core.py").exists()
    assert (tmp_path / "tests" / "test_version.py").exists()
    assert files


def test_builtin_scaffold_fastapi(tmp_path: Path):
    spec = ProjectSpec(name="API", package_name="api_demo", project_type=ProjectType.FASTAPI)
    BuiltinScaffold().generate(tmp_path, spec)
    main = (tmp_path / "src" / "api_demo" / "main.py").read_text(encoding="utf-8")
    assert "FastAPI" in main


def test_jinja_sample_template(tmp_path: Path):
    root = builtin_templates_root() / "_sample_custom"
    meta = TemplateMeta.load(root)
    assert meta.id == "sample-custom"
    engine = TemplateEngine()
    ctx = ProjectSpec(name="Samp", package_name="samp").template_context()
    written = engine.render_tree(root, tmp_path, ctx)
    assert (tmp_path / "README.md").exists()
    assert (tmp_path / "src" / "samp" / "__init__.py").exists()
    assert written
