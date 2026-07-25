"""Example FastAPI plugin for auto-gen-py-project."""

from __future__ import annotations

from pathlib import Path

from auto_gen_py_project.plugins import Plugin as BasePlugin
from auto_gen_py_project.plugins import PluginManager


class Plugin(BasePlugin):
    name = "fastapi"
    version = "0.1.0"
    description = "FastAPI Extended example template plugin"

    def apply(self, manager: PluginManager) -> None:
        manager.register_template_root(Path(__file__).resolve().parent / "templates")
