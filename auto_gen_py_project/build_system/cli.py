"""pybuild — Gradle-inspired build CLI for Python projects."""

import argparse
import importlib.util
import sys
from collections import defaultdict
from pathlib import Path

from .exceptions import BuildError
from .registry import _registry
from .runner import LOG_DEBUG, LOG_INFO, LOG_NORMAL, LOG_QUIET, TaskRunner


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


def _load_properties(path: str) -> dict:
    """Parse a simple key=value properties file. Returns empty dict if absent."""
    props = {}
    p = Path(path)
    if not p.exists():
        return props
    for line in p.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" in line:
            key, _, value = line.partition("=")
            props[key.strip()] = value.strip()
    return props


def _print_task_list(tasks: dict) -> None:
    """Print tasks grouped by their group property, like Gradle's --tasks."""
    grouped: dict = defaultdict(list)
    for name, t in sorted(tasks.items()):
        grouped[t.group or "Other tasks"].append(t)

    print()
    for group in sorted(grouped.keys(), key=lambda g: (g == "Other tasks", g)):
        print(f"{group}")
        print("-" * len(group))
        for t in grouped[group]:
            dep_str = f"  <- {', '.join(t.depends_on)}" if t.depends_on else ""
            desc = t.description.splitlines()[0] if t.description else ""
            enabled_tag = "" if t.enabled else " [disabled]"
            print(f"  {t.name:<22} {desc}{dep_str}{enabled_tag}")
        print()


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="pybuild",
        description="Gradle-inspired build tool for Python projects",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
examples:
  pybuild build               run the 'build' task (and its dependencies)
  pybuild clean test          run 'clean', then 'test' in order
  pybuild --list              list all tasks defined in pybuild.py
  pybuild --dry-run build     show what would run without executing
  pybuild --parallel build    run independent tasks concurrently
  pybuild -f scripts/pybuild.py test
        """,
    )
    parser.add_argument("tasks", nargs="*", help="task(s) to execute")
    parser.add_argument("--list", "-l", action="store_true", help="list available tasks")
    parser.add_argument(
        "--file", "-f", default="pybuild.py", metavar="FILE",
        help="build file to load (default: pybuild.py)",
    )
    parser.add_argument(
        "--properties", default="pybuild.properties", metavar="FILE",
        help="properties file to load (default: pybuild.properties)",
    )

    # Execution flags
    parser.add_argument(
        "--dry-run", "-m", action="store_true",
        help="show which tasks would execute without running them",
    )
    parser.add_argument(
        "--continue", dest="continue_on_failure", action="store_true",
        help="continue executing tasks after a failure",
    )
    parser.add_argument(
        "--parallel", "-p", action="store_true",
        help="execute independent tasks concurrently",
    )
    parser.add_argument(
        "--rerun-tasks", action="store_true",
        help="force re-execution of all tasks (ignore UP-TO-DATE)",
    )

    # Log level (mutually exclusive)
    log_group = parser.add_mutually_exclusive_group()
    log_group.add_argument("--quiet", "-q", action="store_true", help="suppress build output")
    log_group.add_argument("--info", "-i", action="store_true", help="log task inputs/outputs")
    log_group.add_argument("--debug", "-d", action="store_true", help="log full debug output")

    args = parser.parse_args()

    # Determine log level
    if args.quiet:
        log_level = LOG_QUIET
    elif args.info:
        log_level = LOG_INFO
    elif args.debug:
        log_level = LOG_DEBUG
    else:
        log_level = LOG_NORMAL

    # Load optional properties file and expose via build_system.properties
    props = _load_properties(args.properties)
    if props:
        from auto_gen_py_project import build_system
        build_system.properties.update(props)
        if log_level >= LOG_INFO:
            print(f"  Loaded {len(props)} propert(ies) from {args.properties}")

    _load_build_file(args.file)

    if args.list:
        tasks = _registry.all_tasks()
        if not tasks:
            print("No tasks defined in build file.")
            return
        _print_task_list(tasks)
        return

    if not args.tasks:
        parser.print_help()
        sys.exit(1)

    runner = TaskRunner(_registry)

    for task_name in args.tasks:
        try:
            runner.run(
                task_name,
                verbose=(log_level >= LOG_NORMAL),
                dry_run=args.dry_run,
                continue_on_failure=args.continue_on_failure,
                parallel=args.parallel,
                rerun_tasks=args.rerun_tasks,
                log_level=log_level,
            )
        except BuildError as exc:
            print(f"\nBUILD FAILED\n{exc}", file=sys.stderr)
            sys.exit(1)
