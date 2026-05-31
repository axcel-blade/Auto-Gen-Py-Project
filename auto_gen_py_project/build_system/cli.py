"""pybuild — Gradle-inspired build CLI for Python projects."""

import argparse
import importlib.util
import sys
from pathlib import Path

from .exceptions import BuildError
from .registry import _registry
from .runner import TaskRunner


def _load_build_file(path: str) -> None:
    build_path = Path(path).resolve()
    if not build_path.exists():
        print(f"error: build file not found: {build_path}", file=sys.stderr)
        sys.exit(1)

    build_dir = str(build_path.parent)
    if build_dir not in sys.path:
        sys.path.insert(0, build_dir)

    spec = importlib.util.spec_from_file_location("_pybuild_script", build_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="pybuild",
        description="Gradle-inspired build tool for Python projects",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
examples:
  pybuild build             run the 'build' task (and its dependencies)
  pybuild clean test        run 'clean', then 'test' in order
  pybuild --list              list all tasks defined in pybuild.py
  pybuild -f scripts/pybuild.py test
        """,
    )
    parser.add_argument("tasks", nargs="*", help="task(s) to execute")
    parser.add_argument("--list", "-l", action="store_true", help="list available tasks")
    parser.add_argument(
        "--file", "-f", default="pybuild.py", metavar="FILE",
        help="build file to load (default: pybuild.py)",
    )
    parser.add_argument("--quiet", "-q", action="store_true", help="suppress build output")
    args = parser.parse_args()

    _load_build_file(args.file)

    if args.list:
        tasks = _registry.all_tasks()
        if not tasks:
            print("No tasks defined in build file.")
            return
        print("\nAvailable tasks:")
        print("-" * 48)
        for name, t in sorted(tasks.items()):
            dep_str = f"  <- {', '.join(t.depends_on)}" if t.depends_on else ""
            desc = t.description.splitlines()[0] if t.description else ""
            print(f"  {name:<22} {desc}{dep_str}")
        return

    if not args.tasks:
        parser.print_help()
        sys.exit(1)

    runner = TaskRunner(_registry)
    verbose = not args.quiet

    for task_name in args.tasks:
        try:
            runner.run(task_name, verbose=verbose)
        except BuildError as exc:
            print(f"\nBUILD FAILED\n{exc}", file=sys.stderr)
            sys.exit(1)
