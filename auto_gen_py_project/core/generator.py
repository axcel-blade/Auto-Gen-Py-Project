"""Project generator orchestrating templates, plugins, and integrations.

Flow:
1. Optionally enrich the :class:`ProjectSpec` via the AI facade
2. Run plugin ``before`` hooks
3. Render a Jinja template tree when present; otherwise use :class:`BuiltinScaffold`
4. Apply optional integrations (Docker, CI, git, venv, …)
5. Run plugin ``after`` hooks
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Optional

from auto_gen_py_project.core.exceptions import GenerationError
from auto_gen_py_project.core.models import ProjectSpec
from auto_gen_py_project.core.scaffold import BuiltinScaffold
from auto_gen_py_project.integrations import apply_integrations
from auto_gen_py_project.logging import get_logger
from auto_gen_py_project.plugins import PluginManager
from auto_gen_py_project.template_engine import TemplateEngine
from auto_gen_py_project.templates import TemplateRegistry

if TYPE_CHECKING:
    from auto_gen_py_project.ai import AIService

logger = get_logger(__name__)


class ProjectGenerator:
    """Generate a project from a :class:`ProjectSpec`."""

    def __init__(
        self,
        *,
        plugins: Optional[PluginManager] = None,
        ai: Optional["AIService"] = None,
        registry: Optional[TemplateRegistry] = None,
    ) -> None:
        # Lazy import avoids an import cycle with ``auto_gen_py_project.ai``.
        from auto_gen_py_project.ai import AIService as _AIService

        self.plugins = plugins or PluginManager()
        self.plugins.load_entry_points()
        self.ai = ai or _AIService()
        self.registry = registry or TemplateRegistry(self.plugins.extra_template_roots)
        self.engine = TemplateEngine()
        self.scaffold = BuiltinScaffold()

    def generate(
        self,
        spec: ProjectSpec,
        dest: Path,
        *,
        template_id: Optional[str] = None,
        force: bool = False,
        apply_ai: bool = False,
        prompt: str = "",
    ) -> Path:
        """Render ``spec`` into ``dest`` and return the destination path."""
        if apply_ai or prompt:
            spec = self.ai.enrich_spec(spec, prompt)

        dest = dest.resolve()
        if dest.exists() and any(dest.iterdir()) and not force:
            raise GenerationError(f"Destination is not empty: {dest} (use --force)")
        dest.mkdir(parents=True, exist_ok=True)

        self.plugins.run_before(spec, dest)

        template_id = template_id or spec.project_type.value
        try:
            meta = self.registry.get(template_id)
        except Exception:
            # Unknown template ids fall back to the programmatic scaffold.
            meta = None

        written: list[Path] = []
        if meta is not None and (meta.root / "template").is_dir():
            logger.info("Rendering template '%s' from %s", meta.id, meta.root)
            written = self.engine.render_tree(meta.root, dest, spec.template_context())
        else:
            logger.info("Generating built-in scaffold for %s", spec.project_type.value)
            written = self.scaffold.generate(dest, spec)

        apply_integrations(dest, spec)
        self.plugins.run_after(spec, dest)
        logger.info("Created %d files in %s", len(written), dest)
        return dest
