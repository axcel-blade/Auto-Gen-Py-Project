from typing import Callable, List, Optional


class Task:
    """A single build task with an optional action and dependency list."""

    def __init__(
        self,
        name: str,
        action: Optional[Callable] = None,
        depends_on: Optional[List[str]] = None,
        description: Optional[str] = None,
        group: Optional[str] = None,
        enabled: bool = True,
        only_if: Optional[Callable[[], bool]] = None,
        inputs: Optional[List[str]] = None,
        outputs: Optional[List[str]] = None,
        finalized_by: Optional[List[str]] = None,
        must_run_after: Optional[List[str]] = None,
    ) -> None:
        self.name = name
        self.action = action
        self.depends_on: List[str] = list(depends_on or [])
        self.description: str = (
            description or (action.__doc__ or "") if action else (description or "")
        )
        self.group: Optional[str] = group
        self.enabled: bool = enabled
        self.only_if: Optional[Callable[[], bool]] = only_if
        self.inputs: List[str] = list(inputs or [])
        self.outputs: List[str] = list(outputs or [])
        self.finalized_by: List[str] = list(finalized_by or [])
        self.must_run_after: List[str] = list(must_run_after or [])
        self._do_first: List[Callable] = []
        self._do_last: List[Callable] = []

    def do_first(self, fn: Callable) -> None:
        """Prepend an action to run before the main task action."""
        self._do_first.append(fn)

    def do_last(self, fn: Callable) -> None:
        """Append an action to run after the main task action."""
        self._do_last.append(fn)

    def execute(self) -> None:
        for fn in self._do_first:
            fn()
        if self.action is not None:
            self.action()
        for fn in self._do_last:
            fn()

    def __repr__(self) -> str:
        return f"Task(name={self.name!r}, depends_on={self.depends_on!r})"
