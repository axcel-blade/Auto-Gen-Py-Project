"""Keyword-based template hint helpers (not an LLM / AI service).

Scaffolding never requires network calls for recommendations.
``AIService`` / ``AIProvider`` names are kept for import stability.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Optional

from auto_gen_py_project.core.models import ProjectSpec, ProjectType


class AIProvider(ABC):
    """Pluggable hint backend (keyword/heuristic today).

    Core generation never requires a provider. Implementations may recommend
    templates or refine specs; names are kept for import stability.
    """

    name: str = "noop"

    @abstractmethod
    def recommend_template(self, description: str) -> ProjectType:
        """Suggest a project type from a free-text description."""

    @abstractmethod
    def enrich_spec(self, spec: ProjectSpec, prompt: str) -> ProjectSpec:
        """Optionally refine a project specification from a prompt."""

    @abstractmethod
    def generate_snippet(self, prompt: str, *, language: str = "python") -> str:
        """Generate a code snippet (future use)."""


class NoopAIProvider(AIProvider):
    """Default provider that applies lightweight heuristics only."""

    name = "noop"

    def recommend_template(self, description: str) -> ProjectType:
        text = description.lower()
        mapping = [
            (("fastapi",), ProjectType.FASTAPI),
            (("flask",), ProjectType.FLASK),
            (("django",), ProjectType.DJANGO),
            (("jupyter", "notebook"), ProjectType.JUPYTER),
            (("vision", "opencv", "yolo"), ProjectType.COMPUTER_VISION),
            (("llm", "langchain", "openai", "ai "), ProjectType.AI),
            (("sklearn", "xgboost", "ml ", "machine learning"), ProjectType.MACHINE_LEARNING),
            (("pandas", "numpy", "data"), ProjectType.DATA_SCIENCE),
            (("microservice",), ProjectType.MICROSERVICE),
            (("rest", "api"), ProjectType.REST_API),
            (("cli", "typer", "click"), ProjectType.CLI),
            (("async", "asyncio"), ProjectType.ASYNC),
            (("desktop", "tkinter", "pyside"), ProjectType.DESKTOP),
            (("automat", "script"), ProjectType.AUTOMATION),
            (("pypi", "package", "library"), ProjectType.LIBRARY),
        ]
        for keys, ptype in mapping:
            if any(k in text for k in keys):
                return ptype
        return ProjectType.LIBRARY

    def enrich_spec(self, spec: ProjectSpec, prompt: str) -> ProjectSpec:
        if prompt and (not spec.description or spec.description.startswith("A Python")):
            spec.description = prompt.strip()[:200]
        recommended = self.recommend_template(prompt or spec.description)
        if spec.project_type == ProjectType.LIBRARY and prompt:
            spec.project_type = recommended
        return spec

    def generate_snippet(self, prompt: str, *, language: str = "python") -> str:
        return f"# TODO: implement — {prompt}\n"


class AIService:
    """Facade used by the CLI / generator for optional description hints."""

    def __init__(self, provider: Optional[AIProvider] = None) -> None:
        self.provider = provider or NoopAIProvider()

    def set_provider(self, provider: AIProvider) -> None:
        self.provider = provider

    def recommend_template(self, description: str) -> ProjectType:
        return self.provider.recommend_template(description)

    def enrich_spec(self, spec: ProjectSpec, prompt: str = "") -> ProjectSpec:
        return self.provider.enrich_spec(spec, prompt)

    def generate_snippet(self, prompt: str, **kwargs: Any) -> str:
        return self.provider.generate_snippet(prompt, **kwargs)
