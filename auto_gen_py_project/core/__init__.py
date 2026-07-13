"""Core package exports."""

from auto_gen_py_project.core.exceptions import AutoGenError, GenerationError
from auto_gen_py_project.core.models import PackageManager, ProjectSpec, ProjectType

__all__ = [
    "AutoGenError",
    "GenerationError",
    "PackageManager",
    "ProjectSpec",
    "ProjectType",
]


def __getattr__(name: str):
    if name == "ProjectGenerator":
        from auto_gen_py_project.core.generator import ProjectGenerator

        return ProjectGenerator
    raise AttributeError(name)
