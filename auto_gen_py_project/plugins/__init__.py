"""Plugin API and entry-point discovery.

Third-party packages register under:

* ``auto_gen_py_project.plugins`` — :class:`Plugin` implementations
* ``auto_gen_py_project.templates`` — extra template root directories
"""

from __future__ import annotations

import importlib
from abc import ABC, abstractmethod
from importlib import metadata
from pathlib import Path
from typing import TYPE_CHECKING, Any, Callable, Optional

from auto_gen_py_project.core.exceptions import PluginError
from auto_gen_py_project.logging import get_logger

if TYPE_CHECKING:
    import typer
    from auto_gen_py_project.core.models import ProjectSpec
    from auto_gen_py_project.template_engine import TemplateMeta

logger = get_logger(__name__)

TEMPLATES_ENTRY_POINT = "auto_gen_py_project.templates"
PLUGINS_ENTRY_POINT = "auto_gen_py_project.plugins"


class Plugin(ABC):
    """Base class for third-party plugins.

    Plugins may register templates, CLI commands, hooks, and configuration.
    """

    name: str = "plugin"
    version: str = "0.1.0"
    description: str = ""

    @abstractmethod
    def apply(self, manager: "PluginManager") -> None:
        """Register contributions with the plugin manager."""

    def on_before_generate(self, spec: ProjectSpec, dest: Path) -> None:
        """Hook executed before generation."""

    def on_after_generate(self, spec: ProjectSpec, dest: Path) -> None:
        """Hook executed after generation."""


class PluginManager:
    """Discover and manage plugins + template contributions."""

    def __init__(self) -> None:
        self.plugins: list[Plugin] = []
        self.extra_template_roots: list[Path] = []
        self.cli_registrars: list[Callable[[typer.Typer], None]] = []
        self._hooks_before: list[Callable[..., None]] = []
        self._hooks_after: list[Callable[..., None]] = []

    def register_template_root(self, path: Path) -> None:
        self.extra_template_roots.append(path)

    def register_cli(self, registrar: Callable[["typer.Typer"], None]) -> None:
        self.cli_registrars.append(registrar)

    def register_before_hook(self, hook: Callable[..., None]) -> None:
        self._hooks_before.append(hook)

    def register_after_hook(self, hook: Callable[..., None]) -> None:
        self._hooks_after.append(hook)

    def load_entry_points(self) -> None:
        self._load_plugin_eps()
        self._load_template_eps()

    def _load_plugin_eps(self) -> None:
        try:
            eps = metadata.entry_points(group=PLUGINS_ENTRY_POINT)
        except Exception:  # noqa: BLE001
            return
        for ep in eps:
            try:
                obj = ep.load()
                plugin = obj() if isinstance(obj, type) else obj
                if not isinstance(plugin, Plugin):
                    raise PluginError(f"Entry point {ep.name} is not a Plugin")
                plugin.apply(self)
                self.plugins.append(plugin)
                self._hooks_before.append(plugin.on_before_generate)
                self._hooks_after.append(plugin.on_after_generate)
                logger.debug("Loaded plugin %s", plugin.name)
            except Exception as exc:  # noqa: BLE001
                logger.warning("Failed to load plugin %s: %s", ep.name, exc)

    def _load_template_eps(self) -> None:
        try:
            eps = metadata.entry_points(group=TEMPLATES_ENTRY_POINT)
        except Exception:  # noqa: BLE001
            return
        for ep in eps:
            try:
                obj = ep.load()
                path = Path(obj) if not isinstance(obj, Path) else obj
                if callable(obj) and not isinstance(obj, Path):
                    path = Path(obj())
                if path.is_dir():
                    self.register_template_root(path)
            except Exception as exc:  # noqa: BLE001
                logger.warning("Failed to load template entry point %s: %s", ep.name, exc)

    def run_before(self, spec: ProjectSpec, dest: Path) -> None:
        for hook in self._hooks_before:
            hook(spec, dest)

    def run_after(self, spec: ProjectSpec, dest: Path) -> None:
        for hook in self._hooks_after:
            hook(spec, dest)

    def attach_cli(self, app: "typer.Typer") -> None:
        for registrar in self.cli_registrars:
            registrar(app)

    def list_installed(self) -> list[dict[str, str]]:
        return [
            {"name": p.name, "version": p.version, "description": p.description}
            for p in self.plugins
        ]


def load_plugin_module(dotted: str) -> Plugin:
    """Load ``module:Class`` or ``module.Class`` style plugin reference."""
    if ":" in dotted:
        module_name, _, class_name = dotted.partition(":")
    else:
        module_name, _, class_name = dotted.rpartition(".")
    if not module_name or not class_name:
        raise PluginError(f"Invalid plugin reference: {dotted}")
    module = importlib.import_module(module_name)
    cls = getattr(module, class_name, None)
    if cls is None:
        raise PluginError(f"Plugin class not found: {dotted}")
    plugin = cls() if isinstance(cls, type) else cls
    if not isinstance(plugin, Plugin):
        raise PluginError(f"Not a Plugin instance: {dotted}")
    return plugin
