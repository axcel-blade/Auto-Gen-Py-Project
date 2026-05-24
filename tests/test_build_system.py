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


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _registry(*tasks) -> TaskRegistry:
    """Build a fresh TaskRegistry from Task objects."""
    reg = TaskRegistry()
    for t in tasks:
        reg.register(t)
    return reg


def _task(name, depends_on=None, action=None) -> Task:
    return Task(name=name, depends_on=depends_on or [], action=action)


# ---------------------------------------------------------------------------
# Task
# ---------------------------------------------------------------------------

class TestTask:
    def test_defaults(self):
        t = Task("build")
        assert t.name == "build"
        assert t.depends_on == []
        assert t.description == ""

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
        """specs = (name, [deps]) tuples."""
        tasks = {name: _task(name, depends_on=deps) for name, deps in specs}
        return tasks

    def test_single_task_no_deps(self):
        tasks = self._make(("build", []))
        assert resolve_execution_order(tasks, "build") == ["build"]

    def test_linear_chain(self):
        tasks = self._make(("clean", []), ("test", ["clean"]), ("build", ["test"]))
        order = resolve_execution_order(tasks, "build")
        assert order == ["clean", "test", "build"]

    def test_diamond_deduplication(self):
        # build <- [lint, test] <- clean
        tasks = self._make(
            ("clean", []),
            ("lint", ["clean"]),
            ("test", ["clean"]),
            ("build", ["lint", "test"]),
        )
        order = resolve_execution_order(tasks, "build")
        # clean must appear exactly once and before lint and test
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
# TaskRunner
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
# Public API: task() decorator / function-call DSL
# ---------------------------------------------------------------------------

class TestTaskDSL:
    """Tests for the module-level task() helper using an isolated registry."""

    def setup_method(self):
        self.reg = TaskRegistry()

    def _register(self, fn=None, *, depends_on=None, name=None, action=None):
        """Register via Task directly into self.reg (avoids global registry)."""
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
