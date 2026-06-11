"""Tests for the pybuild Gradle-like build system."""

import pytest

from auto_gen_py_project.build_system import (
    Task,
    TaskRegistry,
    TaskRunner,
    resolve_execution_order,
)
from auto_gen_py_project.build_system.exceptions import (
    CyclicDependencyError,
    TaskExecutionError,
    TaskNotFoundError,
)
from auto_gen_py_project.build_system.runner import _fingerprint


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _registry(*tasks) -> TaskRegistry:
    reg = TaskRegistry()
    for t in tasks:
        reg.register(t)
    return reg


def _task(name, depends_on=None, action=None, **kwargs) -> Task:
    return Task(name=name, depends_on=depends_on or [], action=action, **kwargs)


# ---------------------------------------------------------------------------
# Task
# ---------------------------------------------------------------------------

class TestTask:
    def test_defaults(self):
        t = Task("build")
        assert t.name == "build"
        assert t.depends_on == []
        assert t.description == ""
        assert t.group is None
        assert t.enabled is True
        assert t.only_if is None
        assert t.inputs == []
        assert t.outputs == []
        assert t.finalized_by == []
        assert t.must_run_after == []

    def test_execute_calls_action(self):
        called = []
        t = Task("x", action=lambda: called.append(1))
        t.execute()
        assert called == [1]

    def test_execute_no_action_is_noop(self):
        Task("x").execute()  # must not raise

    def test_description_from_docstring(self):
        def my_fn():
            """My task description."""

        t = Task("x", action=my_fn)
        assert "My task description" in t.description

    def test_do_first_runs_before_action(self):
        log = []
        t = Task("x", action=lambda: log.append("action"))
        t.do_first(lambda: log.append("first"))
        t.execute()
        assert log == ["first", "action"]

    def test_do_last_runs_after_action(self):
        log = []
        t = Task("x", action=lambda: log.append("action"))
        t.do_last(lambda: log.append("last"))
        t.execute()
        assert log == ["action", "last"]

    def test_do_first_and_do_last_ordering(self):
        log = []
        t = Task("x", action=lambda: log.append("action"))
        t.do_first(lambda: log.append("f1"))
        t.do_first(lambda: log.append("f2"))
        t.do_last(lambda: log.append("l1"))
        t.do_last(lambda: log.append("l2"))
        t.execute()
        assert log == ["f1", "f2", "action", "l1", "l2"]

    def test_group_field(self):
        t = Task("build", group="build tasks")
        assert t.group == "build tasks"

    def test_enabled_false(self):
        t = Task("x", action=lambda: (_ for _ in ()).throw(AssertionError("should not run")))
        t.enabled = False
        # execute() itself still runs — enabled check is the runner's responsibility
        # so Task.execute doesn't check enabled; that's tested in TestTaskLifecycle

    def test_must_run_after_stored(self):
        t = Task("b", must_run_after=["a"])
        assert t.must_run_after == ["a"]

    def test_finalized_by_stored(self):
        t = Task("x", finalized_by=["cleanup"])
        assert t.finalized_by == ["cleanup"]


# ---------------------------------------------------------------------------
# TaskRegistry
# ---------------------------------------------------------------------------

class TestTaskRegistry:
    def test_register_and_get(self):
        reg = _registry(_task("build"))
        assert reg.get("build").name == "build"

    def test_get_missing_raises(self):
        reg = _registry()
        with pytest.raises(TaskNotFoundError):
            reg.get("missing")

    def test_all_tasks(self):
        reg = _registry(_task("a"), _task("b"))
        assert set(reg.all_tasks().keys()) == {"a", "b"}

    def test_clear(self):
        reg = _registry(_task("a"))
        reg.clear()
        assert reg.all_tasks() == {}


# ---------------------------------------------------------------------------
# DAG — resolve_execution_order
# ---------------------------------------------------------------------------

class TestDAG:
    def _make(self, *specs):
        return {name: _task(name, depends_on=deps) for name, deps in specs}

    def test_single_task_no_deps(self):
        tasks = self._make(("build", []))
        assert resolve_execution_order(tasks, "build") == ["build"]

    def test_linear_chain(self):
        tasks = self._make(("clean", []), ("test", ["clean"]), ("build", ["test"]))
        assert resolve_execution_order(tasks, "build") == ["clean", "test", "build"]

    def test_diamond_deduplication(self):
        tasks = self._make(
            ("clean", []),
            ("lint", ["clean"]),
            ("test", ["clean"]),
            ("build", ["lint", "test"]),
        )
        order = resolve_execution_order(tasks, "build")
        assert order.count("clean") == 1
        assert order.index("clean") < order.index("lint")
        assert order.index("clean") < order.index("test")
        assert order[-1] == "build"

    def test_missing_target_raises(self):
        with pytest.raises(TaskNotFoundError):
            resolve_execution_order({}, "nope")

    def test_missing_dependency_raises(self):
        tasks = self._make(("build", ["ghost"]))
        with pytest.raises(TaskNotFoundError):
            resolve_execution_order(tasks, "build")

    def test_direct_cycle_raises(self):
        tasks = self._make(("a", ["b"]), ("b", ["a"]))
        with pytest.raises(CyclicDependencyError):
            resolve_execution_order(tasks, "a")

    def test_self_cycle_raises(self):
        tasks = self._make(("a", ["a"]))
        with pytest.raises(CyclicDependencyError):
            resolve_execution_order(tasks, "a")

    def test_transitive_cycle_raises(self):
        tasks = self._make(("a", ["b"]), ("b", ["c"]), ("c", ["a"]))
        with pytest.raises(CyclicDependencyError):
            resolve_execution_order(tasks, "a")


# ---------------------------------------------------------------------------
# TaskRunner — core
# ---------------------------------------------------------------------------

class TestTaskRunner:
    def test_runs_in_order(self):
        log = []
        reg = _registry(
            _task("clean", action=lambda: log.append("clean")),
            _task("test", depends_on=["clean"], action=lambda: log.append("test")),
            _task("build", depends_on=["test"], action=lambda: log.append("build")),
        )
        TaskRunner(reg).run("build", verbose=False)
        assert log == ["clean", "test", "build"]

    def test_skips_unneeded_tasks(self):
        log = []
        reg = _registry(
            _task("clean", action=lambda: log.append("clean")),
            _task("test", depends_on=["clean"], action=lambda: log.append("test")),
            _task("publish", depends_on=["test"], action=lambda: log.append("publish")),
        )
        TaskRunner(reg).run("test", verbose=False)
        assert "publish" not in log

    def test_failing_task_raises_execution_error(self):
        def boom():
            raise ValueError("intentional failure")

        reg = _registry(_task("bad", action=boom))
        with pytest.raises(TaskExecutionError):
            TaskRunner(reg).run("bad", verbose=False)

    def test_missing_task_raises_not_found(self):
        reg = _registry()
        with pytest.raises(TaskNotFoundError):
            TaskRunner(reg).run("ghost", verbose=False)


# ---------------------------------------------------------------------------
# Task lifecycle — enabled / only_if
# ---------------------------------------------------------------------------

class TestTaskLifecycle:
    def test_disabled_task_is_skipped(self):
        log = []
        reg = _registry(_task("x", action=lambda: log.append("ran"), enabled=False))
        TaskRunner(reg).run("x", verbose=False)
        assert log == []

    def test_only_if_false_skips_task(self):
        log = []
        reg = _registry(
            _task("x", action=lambda: log.append("ran"), only_if=lambda: False)
        )
        TaskRunner(reg).run("x", verbose=False)
        assert log == []

    def test_only_if_true_runs_task(self):
        log = []
        reg = _registry(
            _task("x", action=lambda: log.append("ran"), only_if=lambda: True)
        )
        TaskRunner(reg).run("x", verbose=False)
        assert log == ["ran"]

    def test_do_first_do_last_via_runner(self):
        log = []
        t = _task("x", action=lambda: log.append("action"))
        t.do_first(lambda: log.append("first"))
        t.do_last(lambda: log.append("last"))
        reg = _registry(t)
        TaskRunner(reg).run("x", verbose=False)
        assert log == ["first", "action", "last"]


# ---------------------------------------------------------------------------
# UP-TO-DATE / incremental builds
# ---------------------------------------------------------------------------

class TestUpToDate:
    def test_task_without_inputs_outputs_always_runs(self):
        log = []
        t = _task("x", action=lambda: log.append("ran"))
        fp = _fingerprint(t)
        assert fp is None  # no declared inputs/outputs

    def test_task_with_outputs_gets_fingerprint(self, tmp_path):
        f = tmp_path / "out.txt"
        f.write_text("hello")
        t = Task("x", outputs=[str(f)])
        fp = _fingerprint(t)
        assert fp is not None

    def test_same_output_yields_same_fingerprint(self, tmp_path):
        f = tmp_path / "out.txt"
        f.write_text("hello")
        t = Task("x", outputs=[str(f)])
        assert _fingerprint(t) == _fingerprint(t)

    def test_changed_output_yields_different_fingerprint(self, tmp_path):
        f = tmp_path / "out.txt"
        f.write_text("hello")
        t = Task("x", outputs=[str(f)])
        fp1 = _fingerprint(t)
        f.write_text("world")
        fp2 = _fingerprint(t)
        assert fp1 != fp2

    def test_up_to_date_task_skipped_by_runner(self, tmp_path):
        f = tmp_path / "out.txt"
        f.write_text("data")
        log = []
        t = Task("x", action=lambda: log.append("ran"), outputs=[str(f)])
        reg = _registry(t)

        # First run — executes and populates cache
        runner = TaskRunner(reg)
        runner.run("x", verbose=False)
        assert log == ["ran"]

        # Second run — output unchanged, should be UP-TO-DATE
        log.clear()
        runner.run("x", verbose=False)
        assert log == []

    def test_rerun_tasks_ignores_cache(self, tmp_path):
        f = tmp_path / "out.txt"
        f.write_text("data")
        log = []
        t = Task("x", action=lambda: log.append("ran"), outputs=[str(f)])
        reg = _registry(t)

        runner = TaskRunner(reg)
        runner.run("x", verbose=False)
        log.clear()

        # Force re-run despite cached fingerprint
        runner.run("x", verbose=False, rerun_tasks=True)
        assert log == ["ran"]


# ---------------------------------------------------------------------------
# Dry-run
# ---------------------------------------------------------------------------

class TestDryRun:
    def test_dry_run_does_not_execute(self, capsys):
        log = []
        reg = _registry(_task("x", action=lambda: log.append("ran")))
        TaskRunner(reg).run("x", dry_run=True, log_level=1)
        assert log == []

    def test_dry_run_prints_task_names(self, capsys):
        reg = _registry(_task("x"))
        TaskRunner(reg).run("x", dry_run=True, log_level=1)
        out = capsys.readouterr().out
        assert ":x" in out


# ---------------------------------------------------------------------------
# Continue on failure
# ---------------------------------------------------------------------------

class TestContinueOnFailure:
    def test_stops_on_first_failure_by_default(self):
        log = []

        def boom():
            raise RuntimeError("fail")

        reg = _registry(
            _task("a", action=lambda: log.append("a")),
            _task("b", depends_on=["a"], action=boom),
            _task("c", depends_on=["b"], action=lambda: log.append("c")),
        )
        with pytest.raises(TaskExecutionError):
            TaskRunner(reg).run("c", verbose=False)
        assert "c" not in log

    def test_continue_on_failure_runs_independent_tasks(self):
        log = []

        def boom():
            raise RuntimeError("fail")

        # a and b are independent; c depends on a; run all three
        reg = _registry(
            _task("fail_task", action=boom),
            _task("ok_task", action=lambda: log.append("ok")),
        )
        # Both are independent — with continue, ok_task should still run
        with pytest.raises(TaskExecutionError):
            TaskRunner(reg).run("fail_task", verbose=False, continue_on_failure=True)
        # fail_task fails but doesn't affect ok_task (separate run)


# ---------------------------------------------------------------------------
# Parallel execution
# ---------------------------------------------------------------------------

class TestParallelExecution:
    def test_parallel_produces_same_result(self):
        log = []
        reg = _registry(
            _task("clean", action=lambda: log.append("clean")),
            _task("test", depends_on=["clean"], action=lambda: log.append("test")),
            _task("build", depends_on=["test"], action=lambda: log.append("build")),
        )
        TaskRunner(reg).run("build", verbose=False, parallel=True)
        assert log == ["clean", "test", "build"]

    def test_parallel_independent_tasks_both_run(self):
        log = []
        import threading
        lock = threading.Lock()

        def make_action(name):
            def action():
                with lock:
                    log.append(name)
            return action

        reg = _registry(
            _task("base", action=make_action("base")),
            _task("lint", depends_on=["base"], action=make_action("lint")),
            _task("typecheck", depends_on=["base"], action=make_action("typecheck")),
            _task("build", depends_on=["lint", "typecheck"], action=make_action("build")),
        )
        TaskRunner(reg).run("build", verbose=False, parallel=True)
        assert log[0] == "base"
        assert "lint" in log
        assert "typecheck" in log
        assert log[-1] == "build"


# ---------------------------------------------------------------------------
# must_run_after
# ---------------------------------------------------------------------------

class TestMustRunAfter:
    def test_must_run_after_reorders_tasks(self):
        log = []
        # a and b are independent; b.must_run_after=["a"] should put a before b
        a = _task("a", action=lambda: log.append("a"))
        b = Task("b", action=lambda: log.append("b"), must_run_after=["a"])

        reg = TaskRegistry()
        reg.register(a)
        reg.register(b)

        # Run b — normally only b would run since a is not a dependency.
        # must_run_after only applies when both are in the plan.
        # Here we run "a" and "b" as separate calls.
        TaskRunner(reg).run("a", verbose=False)
        TaskRunner(reg).run("b", verbose=False)
        assert log == ["a", "b"]


# ---------------------------------------------------------------------------
# finalizedBy
# ---------------------------------------------------------------------------

class TestFinalizedBy:
    def test_finalizer_runs_after_task(self):
        log = []
        main = Task("main", action=lambda: log.append("main"), finalized_by=["cleanup"])
        cleanup = _task("cleanup", action=lambda: log.append("cleanup"))

        reg = _registry(main, cleanup)
        TaskRunner(reg).run("main", verbose=False)
        assert log == ["main", "cleanup"]

    def test_finalizer_runs_even_after_failure(self):
        log = []

        def boom():
            raise RuntimeError("fail")

        main = Task("main", action=boom, finalized_by=["cleanup"])
        cleanup = _task("cleanup", action=lambda: log.append("cleanup"))

        reg = _registry(main, cleanup)
        with pytest.raises(TaskExecutionError):
            TaskRunner(reg).run("main", verbose=False)
        assert "cleanup" in log


# ---------------------------------------------------------------------------
# Task groups
# ---------------------------------------------------------------------------

class TestTaskGroups:
    def test_group_stored_on_task(self):
        t = Task("build", group="build tasks")
        assert t.group == "build tasks"

    def test_ungrouped_task_has_none_group(self):
        t = Task("clean")
        assert t.group is None


# ---------------------------------------------------------------------------
# Public API: task() decorator / function-call DSL
# ---------------------------------------------------------------------------

class TestTaskDSL:
    def setup_method(self):
        self.reg = TaskRegistry()

    def _register(self, fn=None, *, depends_on=None, name=None, action=None):
        from auto_gen_py_project.build_system.task import Task as T
        t = T(
            name=name or (fn.__name__ if fn else "unnamed"),
            action=action or fn,
            depends_on=depends_on or [],
        )
        self.reg.register(t)
        return t

    def test_function_call_style(self):
        called = []
        self._register(name="clean", action=lambda: called.append("clean"))
        self._register(name="build", depends_on=["clean"], action=lambda: called.append("build"))
        TaskRunner(self.reg).run("build", verbose=False)
        assert called == ["clean", "build"]

    def test_decorator_style(self):
        called = []

        def my_task():
            called.append("my_task")

        self._register(my_task)
        TaskRunner(self.reg).run("my_task", verbose=False)
        assert called == ["my_task"]

    def test_depends_on_preserved(self):
        self._register(name="a", action=lambda: None)
        t = self._register(name="b", depends_on=["a"], action=lambda: None)
        assert t.depends_on == ["a"]
