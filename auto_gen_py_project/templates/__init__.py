"""Template discovery and registry."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable, Optional

from auto_gen_py_project.core.exceptions import TemplateError
from auto_gen_py_project.core.models import ProjectType
from auto_gen_py_project.template_engine import TemplateMeta


def builtin_templates_root() -> Path:
    return Path(__file__).resolve().parent


class TemplateRegistry:
    """Indexes built-in, user, and plugin template directories."""

    def __init__(self, extra_roots: Optional[Iterable[Path]] = None) -> None:
        self._templates: dict[str, TemplateMeta] = {}
        self.discover(builtin_templates_root())
        for root in extra_roots or []:
            self.discover(root)

    def discover(self, root: Path) -> None:
        if not root.is_dir():
            return
        # root itself may be a template
        if (root / "template.json").exists() or (root / "template.yaml").exists():
            meta = TemplateMeta.load(root)
            self._templates[meta.id] = meta
            return
        for child in sorted(root.iterdir()):
            if child.is_dir() and not child.name.startswith(("_", ".")):
                if (child / "template.json").exists() or (child / "template.yaml").exists() or (
                    child / "template"
                ).is_dir():
                    meta = TemplateMeta.load(child)
                    self._templates[meta.id] = meta

    def get(self, template_id: str) -> TemplateMeta:
        if template_id not in self._templates:
            # allow project type aliases
            alias = template_id.replace("_", "-")
            if alias in self._templates:
                return self._templates[alias]
            raise TemplateError(f"Unknown template: {template_id}")
        return self._templates[template_id]

    def list(self) -> list[TemplateMeta]:
        return sorted(self._templates.values(), key=lambda m: m.id)

    def for_project_type(self, project_type: ProjectType | str) -> TemplateMeta:
        value = project_type.value if isinstance(project_type, ProjectType) else project_type
        for meta in self._templates.values():
            if value in meta.project_types or meta.id == value:
                return meta
        # fallback to generic library
        if "library" in self._templates:
            return self._templates["library"]
        raise TemplateError(f"No template for project type: {value}")
