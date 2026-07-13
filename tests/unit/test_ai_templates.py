"""Unit tests for AI heuristics and template registry."""

from __future__ import annotations

from auto_gen_py_project.ai import AIService, NoopAIProvider
from auto_gen_py_project.core.models import ProjectSpec, ProjectType
from auto_gen_py_project.templates import TemplateRegistry


def test_ai_recommend_fastapi():
    ai = AIService(NoopAIProvider())
    assert ai.recommend_template("a FastAPI microservice") == ProjectType.FASTAPI


def test_ai_enrich_spec():
    spec = ProjectSpec(name="X", package_name="x")
    enriched = AIService().enrich_spec(spec, "Build a Flask API for inventory")
    assert enriched.project_type == ProjectType.FLASK
    assert "Flask" in enriched.description or "inventory" in enriched.description.lower()


def test_template_registry_lists_builtins():
    registry = TemplateRegistry()
    ids = {m.id for m in registry.list()}
    assert "library" in ids
    assert "fastapi" in ids
    meta = registry.for_project_type(ProjectType.DJANGO)
    assert meta.id == "django"
