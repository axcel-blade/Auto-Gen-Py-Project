from typing import Dict
from .task import Task
from .exceptions import TaskNotFoundError


class TaskRegistry:
    """Holds all registered tasks for a build session."""

    def __init__(self) -> None:
        self._tasks: Dict[str, Task] = {}

    def register(self, task: Task) -> None:
        self._tasks[task.name] = task

    def get(self, name: str) -> Task:
        if name not in self._tasks:
            available = list(self._tasks.keys())
            raise TaskNotFoundError(
                f"Task '{name}' not found. Available tasks: {available}"
            )
        return self._tasks[name]

    def all_tasks(self) -> Dict[str, Task]:
        return dict(self._tasks)

    def clear(self) -> None:
        self._tasks.clear()


# Module-level registry shared across a build session.
_registry = TaskRegistry()
