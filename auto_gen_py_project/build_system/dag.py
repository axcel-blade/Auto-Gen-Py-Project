from typing import Dict, List
from .task import Task
from .exceptions import CyclicDependencyError, TaskNotFoundError


def resolve_execution_order(tasks: Dict[str, Task], target: str) -> List[str]:
    """Return tasks in topological order so every dependency runs before the task that needs it.

    Raises CyclicDependencyError if a cycle is detected.
    Raises TaskNotFoundError if target or any dependency is missing.
    """
    if target not in tasks:
        raise TaskNotFoundError(
            f"Task '{target}' not found. Available tasks: {list(tasks.keys())}"
        )

    visited: set = set()
    in_progress: set = set()
    order: List[str] = []

    def visit(name: str) -> None:
        if name not in tasks:
            raise TaskNotFoundError(
                f"Dependency '{name}' not found. Available tasks: {list(tasks.keys())}"
            )
        if name in in_progress:
            cycle = " -> ".join(list(in_progress) + [name])
            raise CyclicDependencyError(f"Cyclic dependency detected: {cycle}")
        if name in visited:
            return

        in_progress.add(name)
        for dep in tasks[name].depends_on:
            visit(dep)
        in_progress.discard(name)
        visited.add(name)
        order.append(name)

    visit(target)
    return order
