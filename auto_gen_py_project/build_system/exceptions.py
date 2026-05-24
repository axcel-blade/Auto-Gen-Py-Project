class BuildError(Exception):
    """Base exception for all build system errors."""


class CyclicDependencyError(BuildError):
    """Raised when a cyclic dependency is detected in the task graph."""


class TaskNotFoundError(BuildError):
    """Raised when a referenced task does not exist in the registry."""


class TaskExecutionError(BuildError):
    """Raised when a task's action raises an exception during execution."""
