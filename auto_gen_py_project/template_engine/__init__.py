"""Jinja2 template engine with conditionals, loops, and path rendering.

Supports ``{{ variables }}`` inside file contents and path segments
(for example ``src/{{ package_name }}/__init__.py.j2``).
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable, Optional

from jinja2 import Environment, FileSystemLoader, StrictUndefined, select_autoescape

from auto_gen_py_project.core.exceptions import TemplateError
from auto_gen_py_project.utilities import ensure_dir, write_text


@dataclass
class TemplateMeta:
    """Metadata declared in ``template.json`` / ``template.yaml``."""

    id: str
    name: str
    description: str = ""
    project_types: list[str] = field(default_factory=list)
    version: str = "1.0.0"
    prompts: list[dict[str, Any]] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)
    root: Path = field(default_factory=Path)

    @classmethod
    def load(cls, root: Path) -> "TemplateMeta":
        for name in ("template.json", "template.yaml", "template.yml"):
            path = root / name
            if not path.is_file():
                continue
            text = path.read_text(encoding="utf-8-sig")
            if path.suffix == ".json":
                data = json.loads(text)
            else:
                import yaml

                data = yaml.safe_load(text) or {}
            return cls(
                id=data.get("id") or root.name,
                name=data.get("name") or root.name,
                description=data.get("description", ""),
                project_types=list(data.get("project_types") or data.get("types") or []),
                version=str(data.get("version", "1.0.0")),
                prompts=list(data.get("prompts") or []),
                tags=list(data.get("tags") or []),
                root=root,
            )
        return cls(id=root.name, name=root.name, root=root)


class TemplateEngine:
    """Render a template directory into an output project."""

    SKIP_NAMES = {"template.json", "template.yaml", "template.yml", "__pycache__"}

    def __init__(self) -> None:
        self.env = Environment(
            loader=FileSystemLoader("/"),
            undefined=StrictUndefined,
            autoescape=select_autoescape(enabled_extensions=()),
            keep_trailing_newline=True,
            trim_blocks=True,
            lstrip_blocks=True,
        )
        self.env.filters["snake"] = lambda s: str(s).lower().replace("-", "_").replace(" ", "_")
        self.env.filters["kebab"] = lambda s: str(s).lower().replace("_", "-").replace(" ", "-")
        self.env.filters["pascal"] = lambda s: "".join(
            part.capitalize() for part in str(s).replace("-", "_").split("_") if part
        )

    def render_string(self, template: str, context: dict[str, Any]) -> str:
        try:
            return self.env.from_string(template).render(**context)
        except Exception as exc:  # noqa: BLE001
            raise TemplateError(f"Failed to render template string: {exc}") from exc

    def render_path_name(self, name: str, context: dict[str, Any]) -> str:
        # Support {{ package_name }} in path segments and strip .j2 suffix
        rendered = self.render_string(name, context)
        if rendered.endswith(".j2"):
            rendered = rendered[:-3]
        return rendered

    def iter_template_files(self, root: Path) -> Iterable[Path]:
        for path in sorted(root.rglob("*")):
            if not path.is_file():
                continue
            if path.name in self.SKIP_NAMES:
                continue
            if any(part.startswith(".") and part not in {".github", ".vscode", ".editorconfig"} for part in path.relative_to(root).parts[:-1]):
                # allow .github / .vscode folders; skip other dotdirs like .git
                rel_parts = path.relative_to(root).parts
                if any(p.startswith(".") and p not in {".github", ".vscode"} for p in rel_parts[:-1]):
                    continue
            yield path

    def render_tree(self, template_root: Path, dest: Path, context: dict[str, Any]) -> list[Path]:
        """Render all files under ``template_root`` into ``dest``."""
        content_root = template_root / "hooks"
        # Prefer a nested ``{{ cookiecutter }}`` style ``template/`` folder if present
        source = template_root / "template"
        if not source.is_dir():
            source = template_root

        written: list[Path] = []
        ensure_dir(dest)
        for src in self.iter_template_files(source):
            if "hooks" in src.parts and src.parent.name == "hooks":
                continue
            rel = src.relative_to(source)
            # Render each path component
            parts = [self.render_path_name(part, context) for part in rel.parts]
            # Skip files gated by falsey filename markers like ``Dockerfile.docker``
            out_path = dest.joinpath(*parts)
            text = src.read_text(encoding="utf-8")
            if src.suffix == ".j2" or "{{" in text or "{%" in text:
                try:
                    rendered = self.render_string(text, context)
                except TemplateError:
                    raise
                except Exception as exc:  # noqa: BLE001
                    raise TemplateError(f"Failed rendering {rel}: {exc}") from exc
            else:
                rendered = text
            # Conditional file: empty render means skip
            if rendered.strip() == "" and ("{%" in text or "{#" in text):
                continue
            write_text(out_path, rendered)
            written.append(out_path)
        return written
