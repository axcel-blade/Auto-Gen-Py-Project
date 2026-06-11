import hashlib
import json
import threading
import time
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from .dag import resolve_execution_order
from .exceptions import TaskExecutionError
from .registry import TaskRegistry
from .task import Task

CACHE_FILE = Path(".pybuild-cache.json")

LOG_QUIET = 0
LOG_NORMAL = 1
LOG_INFO = 2
LOG_DEBUG = 3


# ---------------------------------------------------------------------------
# Cache helpers
# ---------------------------------------------------------------------------

def _load_cache() -> dict:
    if CACHE_FILE.exists():
        try:
            return json.loads(CACHE_FILE.read_text())
        except Exception:
            return {}
    return {}


def _save_cache(cache: dict) -> None:
    try:
        CACHE_FILE.write_text(json.dumps(cache, indent=2))
    except Exception:
        pass


def _fingerprint(task: Task) -> Optional[str]:
    """SHA-256 fingerprint of declared inputs/outputs. None when none declared."""
    if not task.inputs and not task.outputs:
        return None
    h = hashlib.sha256()
    for path in sorted(task.inputs):
        p = Path(path)
        if p.exists():
            h.update(p.read_bytes())
        else:
            h.update(b"\x00missing\x00" + path.encode())
    for path in sorted(task.outputs):
        p = Path(path)
        if p.exists():
            st = p.stat()
            h.update(f"{path}:{st.st_size}:{st.st_mtime}".encode())
        else:
            h.update(b"\x00missing\x00" + path.encode())
    return h.hexdigest()


# ---------------------------------------------------------------------------
# Ordering helpers
# ---------------------------------------------------------------------------

def _apply_must_run_after(order: List[str], tasks: Dict[str, Task]) -> List[str]:
    """Reorder plan to satisfy must_run_after constraints (ignores cycles)."""
    plan_set = set(order)
    extra: Dict[str, set] = {n: set() for n in plan_set}
    for name in plan_set:
        for before in tasks[name].must_run_after:
            if before in plan_set:
                extra[name].add(before)

    if not any(extra.values()):
        return order

    visited: set = set()
    in_progress: set = set()
    result: List[str] = []

    def visit(name: str) -> None:
        if name in visited:
            return
        if name in in_progress:
            return  # ignore cycle in must_run_after
        in_progress.add(name)
        all_deps = {d for d in tasks[name].depends_on if d in plan_set} | extra[name]
        for dep in sorted(all_deps):
            visit(dep)
        in_progress.discard(name)
        visited.add(name)
        result.append(name)

    for name in order:
        visit(name)

    return result


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------

class TaskRunner:
    """Executes tasks in dependency-resolved order with Gradle-style output."""

    def __init__(self, registry: TaskRegistry) -> None:
        self.registry = registry

    def run(
        self,
        task_name: str,
        verbose: bool = True,
        dry_run: bool = False,
        continue_on_failure: bool = False,
        parallel: bool = False,
        rerun_tasks: bool = False,
        log_level: int = LOG_NORMAL,
    ) -> None:
        if not verbose:
            log_level = LOG_QUIET

        tasks = self.registry.all_tasks()
        order = resolve_execution_order(tasks, task_name)
        order = _apply_must_run_after(order, tasks)

        finalize_map: Dict[str, List[str]] = {
            name: list(tasks[name].finalized_by)
            for name in order
            if tasks[name].finalized_by
        }

        cache = {} if rerun_tasks else _load_cache()

        if dry_run:
            self._print_dry_run(order, tasks, log_level, cache)
            return

        if parallel:
            errors = self._run_parallel(
                order, tasks, cache, continue_on_failure, log_level, finalize_map
            )
        else:
            errors = self._run_sequential(
                order, tasks, cache, continue_on_failure, log_level, finalize_map
            )

        _save_cache(cache)

        if errors:
            msg = "\n".join(str(e) for e in errors)
            raise TaskExecutionError(
                f"Build failed with {len(errors)} error(s):\n{msg}"
            )

    # ------------------------------------------------------------------
    # Dry-run
    # ------------------------------------------------------------------

    def _print_dry_run(
        self,
        order: List[str],
        tasks: Dict[str, Task],
        log_level: int,
        cache: dict,
    ) -> None:
        if log_level >= LOG_NORMAL:
            print(f"\n> Task graph ({len(order)} tasks — dry run)\n")
        for name in order:
            task = tasks[name]
            fp = _fingerprint(task)
            if not task.enabled:
                status = "SKIPPED (disabled)"
            elif fp is not None and cache.get(name) == fp:
                status = "UP-TO-DATE"
            else:
                status = "would execute"
            print(f"  :{name:<22} [{status}]")

    # ------------------------------------------------------------------
    # Sequential
    # ------------------------------------------------------------------

    def _run_sequential(
        self,
        order: List[str],
        tasks: Dict[str, Task],
        cache: dict,
        continue_on_failure: bool,
        log_level: int,
        finalize_map: Dict[str, List[str]],
    ) -> List[Exception]:
        if log_level >= LOG_NORMAL:
            print(f"\n> Build: {len(order)} task(s) to execute\n")

        start_all = time.time()
        executed = up_to_date = skipped = 0
        errors: List[Exception] = []

        for name in order:
            task = tasks[name]
            status, exc = self._execute_one(name, task, cache, log_level)

            if status == "EXECUTED":
                executed += 1
                cache[name] = _fingerprint(task)
            elif status == "UP-TO-DATE":
                up_to_date += 1
            elif status == "SKIPPED":
                skipped += 1
            elif status == "FAILED":
                errors.append(exc)

            # Finalizers always run, even when the triggering task failed
            for fin in finalize_map.get(name, []):
                if fin in tasks:
                    fin_status, _ = self._execute_one(fin, tasks[fin], cache, log_level)
                    if fin_status == "EXECUTED":
                        cache[fin] = _fingerprint(tasks[fin])

            if status == "FAILED" and not continue_on_failure:
                break

        if log_level >= LOG_NORMAL:
            elapsed = time.time() - start_all
            result = "BUILD FAILED" if (errors and not continue_on_failure) else "BUILD SUCCESSFUL"
            suffix = ""
            if up_to_date:
                suffix += f", {up_to_date} up-to-date"
            if skipped:
                suffix += f", {skipped} skipped"
            print(
                f"{result} in {elapsed:.2f}s\n"
                f"{len(order)} actionable task(s): {executed} executed{suffix}"
            )

        return errors

    # ------------------------------------------------------------------
    # Parallel
    # ------------------------------------------------------------------

    def _run_parallel(
        self,
        order: List[str],
        tasks: Dict[str, Task],
        cache: dict,
        continue_on_failure: bool,
        log_level: int,
        finalize_map: Dict[str, List[str]],
    ) -> List[Exception]:
        if log_level >= LOG_NORMAL:
            print(f"\n> Build (parallel): {len(order)} task(s)\n")

        plan_set = set(order)

        # Compute level for each task (tasks at the same level are independent)
        level: Dict[str, int] = {}
        for name in order:
            plan_deps = [d for d in tasks[name].depends_on if d in plan_set]
            level[name] = (1 + max(level[d] for d in plan_deps)) if plan_deps else 0

        levels: Dict[int, List[str]] = defaultdict(list)
        for name, lv in level.items():
            levels[lv].append(name)

        lock = threading.Lock()
        errors: List[Exception] = []
        failed_tasks: set = set()
        start_all = time.time()
        executed = up_to_date = skipped = 0

        with ThreadPoolExecutor() as executor:
            for lv in sorted(levels.keys()):
                if failed_tasks and not continue_on_failure:
                    break

                batch = levels[lv]
                if log_level >= LOG_INFO:
                    print(f"  [level {lv}]: {batch}")

                # Skip tasks whose dependency failed
                runnable = []
                for name in batch:
                    if any(d in failed_tasks for d in tasks[name].depends_on if d in plan_set):
                        failed_tasks.add(name)
                        if log_level >= LOG_NORMAL:
                            print(f"> Task :{name} SKIPPED (dependency failed)")
                    else:
                        runnable.append(name)

                futures = {
                    executor.submit(self._execute_one, name, tasks[name], cache, log_level): name
                    for name in runnable
                }

                for future in as_completed(futures):
                    name = futures[future]
                    status, exc = future.result()
                    with lock:
                        if status == "EXECUTED":
                            executed += 1
                            cache[name] = _fingerprint(tasks[name])
                        elif status == "UP-TO-DATE":
                            up_to_date += 1
                        elif status == "SKIPPED":
                            skipped += 1
                        elif status == "FAILED":
                            failed_tasks.add(name)
                            errors.append(exc)

                    for fin in finalize_map.get(name, []):
                        if fin in tasks:
                            fin_status, _ = self._execute_one(fin, tasks[fin], cache, log_level)
                            if fin_status == "EXECUTED":
                                with lock:
                                    cache[fin] = _fingerprint(tasks[fin])

        if log_level >= LOG_NORMAL:
            elapsed = time.time() - start_all
            result = "BUILD FAILED" if errors and not continue_on_failure else "BUILD SUCCESSFUL"
            suffix = ""
            if up_to_date:
                suffix += f", {up_to_date} up-to-date"
            if skipped:
                suffix += f", {skipped} skipped"
            print(
                f"{result} in {elapsed:.2f}s\n"
                f"{len(order)} actionable task(s): {executed} executed{suffix}"
            )

        return errors

    # ------------------------------------------------------------------
    # Single-task execution
    # ------------------------------------------------------------------

    def _execute_one(
        self,
        name: str,
        task: Task,
        cache: dict,
        log_level: int,
    ) -> Tuple[str, Optional[Exception]]:
        if not task.enabled:
            if log_level >= LOG_NORMAL:
                print(f"> Task :{name} SKIPPED (disabled)")
            return "SKIPPED", None

        if task.only_if is not None and not task.only_if():
            if log_level >= LOG_NORMAL:
                print(f"> Task :{name} SKIPPED (condition not met)")
            return "SKIPPED", None

        fp = _fingerprint(task)
        if fp is not None and cache.get(name) == fp:
            if log_level >= LOG_NORMAL:
                print(f"> Task :{name} UP-TO-DATE")
            return "UP-TO-DATE", None

        if log_level >= LOG_NORMAL:
            print(f"> Task :{name}")
        if log_level >= LOG_INFO:
            if task.inputs:
                print(f"  inputs:  {task.inputs}")
            if task.outputs:
                print(f"  outputs: {task.outputs}")
        if log_level >= LOG_DEBUG:
            print(f"  depends_on: {task.depends_on}")

        t0 = time.time()
        try:
            task.execute()
            elapsed = time.time() - t0
            if log_level >= LOG_NORMAL:
                print(f"  [DONE] {elapsed:.2f}s\n")
            return "EXECUTED", None
        except Exception as exc:
            elapsed = time.time() - t0
            print(f"  [FAILED] :{name} ({elapsed:.2f}s)")
            err = TaskExecutionError(f"Task ':{name}' failed: {exc}")
            return "FAILED", err
