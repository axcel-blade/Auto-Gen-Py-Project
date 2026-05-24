# auto_gen_py_project/build_system/__init__.py

from typing import Callable, List, Optional, Union

from .dag import resolve_execution_order
from .exceptions import (
    BuildError,
    CyclicDependencyError,
    TaskExecutionError,
    TaskNotFoundError,
)
from .registry import TaskRegistry, _registry
from .runner import TaskRunner
from .task import Task


def task(
    name_or_func: Union[str, Callable, None] = None,
    *,
    depends_on: Optional[List[str]] = None,
    action: Optional[Callable] = None,
    description: Optional[str] = None,
) -> Union[Task, Callable]:
    """Register a build task.

    Three usage styles:

    1. Bare decorator::

        @task
        def build(): ...

    2. Decorator with options::

        @task(depends_on=["test"])
        def build(): ...

    3. Function call (Gradle-style)::

        task("build", depends_on=["test"], action=build_fn)
    """
    # Style 1: @task with no parentheses — name_or_func is the decorated callable.
    if callable(name_or_func):
        func = name_or_func
        t = Task(
            name=func.__name__,
            action=func,
            depends_on=depends_on or [],
            description=description or func.__doc__,
        )
        _registry.register(t)
        return func

    # Style 3: task("name", action=..., depends_on=...) — name_or_func is a string.
    if isinstance(name_or_func, str):
        t = Task(
            name=name_or_func,
            action=action,
            depends_on=depends_on or [],
            description=description,
        )
        _registry.register(t)
        return t

    # Style 2: @task(...) — name_or_func is None, returns a decorator.
    def decorator(func: Callable) -> Callable:
        t = Task(
            name=func.__name__,
            action=func,
            depends_on=depends_on or [],
            description=description or func.__doc__,
        )
        _registry.register(t)
        return func

    return decorator


def run_task(task_name: str, *, verbose: bool = True) -> None:
    """Execute a named task and all of its transitive dependencies."""
    TaskRunner(_registry).run(task_name, verbose=verbose)


def list_tasks() -> dict:
    """Return all registered tasks keyed by name."""
    return _registry.all_tasks()


__all__ = [
    "task",
    "run_task",
    "list_tasks",
    "Task",
    "TaskRunner",
    "TaskRegistry",
    "BuildError",
    "CyclicDependencyError",
    "TaskNotFoundError",
    "TaskExecutionError",
    "resolve_execution_order",
]
