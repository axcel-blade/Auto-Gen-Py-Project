# auto_gen_py_project/build_system/__init__.py

from typing import Callable, Dict, List, Optional, Union

from .dag import resolve_execution_order
from .exceptions import (
    BuildError,
    CyclicDependencyError,
    TaskExecutionError,
    TaskNotFoundError,
)
from .registry import TaskRegistry, _registry
from .runner import LOG_DEBUG, LOG_INFO, LOG_NORMAL, LOG_QUIET, TaskRunner
from .task import Task

# Module-level properties dict populated from pybuild.properties
properties: Dict[str, str] = {}


def load_properties(path: str = "pybuild.properties") -> Dict[str, str]:
    """Load key=value pairs from *path* into the module-level properties dict."""
    from pathlib import Path
    p = Path(path)
    if not p.exists():
        return {}
    for line in p.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" in line:
            key, _, value = line.partition("=")
            properties[key.strip()] = value.strip()
    return dict(properties)


def task(
    name_or_func: Union[str, Callable, None] = None,
    *,
    depends_on: Optional[List[str]] = None,
    action: Optional[Callable] = None,
    description: Optional[str] = None,
    group: Optional[str] = None,
    enabled: bool = True,
    only_if: Optional[Callable[[], bool]] = None,
    inputs: Optional[List[str]] = None,
    outputs: Optional[List[str]] = None,
    finalized_by: Optional[List[str]] = None,
    must_run_after: Optional[List[str]] = None,
) -> Union[Task, Callable]:
    """Register a build task.

    Three usage styles::

        @task
        def build(): ...

        @task(depends_on=["test"], group="build")
        def build(): ...

        task("build", depends_on=["test"], action=build_fn)
    """
    def _make_task(name: str, fn: Optional[Callable]) -> Task:
        return Task(
            name=name,
            action=fn,
            depends_on=depends_on or [],
            description=description or (fn.__doc__ if fn else None),
            group=group,
            enabled=enabled,
            only_if=only_if,
            inputs=inputs,
            outputs=outputs,
            finalized_by=finalized_by or [],
            must_run_after=must_run_after or [],
        )

    # Style 1: @task — no parentheses, name_or_func is the decorated callable.
    if callable(name_or_func):
        func = name_or_func
        _registry.register(_make_task(func.__name__, func))
        return func

    # Style 3: task("name", action=...) — name_or_func is a string.
    if isinstance(name_or_func, str):
        t = _make_task(name_or_func, action)
        _registry.register(t)
        return t

    # Style 2: @task(...) — name_or_func is None, return a decorator.
    def decorator(func: Callable) -> Callable:
        _registry.register(_make_task(func.__name__, func))
        return func

    return decorator


def run_task(
    task_name: str,
    *,
    verbose: bool = True,
    dry_run: bool = False,
    continue_on_failure: bool = False,
    parallel: bool = False,
    rerun_tasks: bool = False,
    log_level: int = LOG_NORMAL,
) -> None:
    """Execute a named task and all of its transitive dependencies."""
    TaskRunner(_registry).run(
        task_name,
        verbose=verbose,
        dry_run=dry_run,
        continue_on_failure=continue_on_failure,
        parallel=parallel,
        rerun_tasks=rerun_tasks,
        log_level=log_level,
    )


def list_tasks() -> dict:
    """Return all registered tasks keyed by name."""
    return _registry.all_tasks()


__all__ = [
    "task",
    "run_task",
    "list_tasks",
    "load_properties",
    "properties",
    "Task",
    "TaskRunner",
    "TaskRegistry",
    "BuildError",
    "CyclicDependencyError",
    "TaskNotFoundError",
    "TaskExecutionError",
    "resolve_execution_order",
    "LOG_QUIET",
    "LOG_NORMAL",
    "LOG_INFO",
    "LOG_DEBUG",
]
