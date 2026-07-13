"""``python -m auto_gen_py_project`` entry point.

Delegates to the Typer application so module and console-script
invocations share the same CLI surface.
"""

from auto_gen_py_project.cli.app import main

if __name__ == "__main__":
    main()
