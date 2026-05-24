import time
from .dag import resolve_execution_order
from .registry import TaskRegistry
from .exceptions import TaskExecutionError


class TaskRunner:
    """Executes tasks in dependency-resolved order with Gradle-style output."""

    def __init__(self, registry: TaskRegistry) -> None:
        self.registry = registry

    def run(self, task_name: str, verbose: bool = True) -> None:
        tasks = self.registry.all_tasks()
        order = resolve_execution_order(tasks, task_name)

        total = len(order)
        if verbose:
            print(f"\n> Build: {total} task(s) to execute\n")

        start_all = time.time()
        executed = 0

        for name in order:
            task = tasks[name]
            if verbose:
                print(f"> Task :{name}")
            t0 = time.time()
            try:
                task.execute()
                executed += 1
                elapsed = time.time() - t0
                if verbose:
                    print(f"  [DONE] {elapsed:.2f}s\n")
            except Exception as exc:
                print(f"  [FAILED] :{name}")
                raise TaskExecutionError(
                    f"Task ':{name}' failed: {exc}"
                ) from exc

        total_elapsed = time.time() - start_all
        if verbose:
            print(
                f"BUILD SUCCESSFUL in {total_elapsed:.2f}s\n"
                f"{total} actionable task(s): {executed} executed"
            )
