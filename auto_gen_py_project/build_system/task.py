from typing import Callable, List, Optional


class Task:
    """A single build task with an optional action and dependency list."""

    def __init__(
        self,
        name: str,
        action: Optional[Callable] = None,
        depends_on: Optional[List[str]] = None,
        description: Optional[str] = None,
    ) -> None:
        self.name = name
        self.action = action
        self.depends_on: List[str] = list(depends_on or [])
        self.description: str = description or (action.__doc__ or "") if action else (description or "")

    def execute(self) -> None:
        if self.action is not None:
            self.action()

    def __repr__(self) -> str:
        return f"Task(name={self.name!r}, depends_on={self.depends_on!r})"
