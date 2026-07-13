"""Programmatic built-in scaffold using Jinja2 strings.

Each :class:`~auto_gen_py_project.core.models.ProjectType` shares a common
file set (pyproject, tests, docs, …) and receives type-specific modules
such as FastAPI ``main.py`` or a Typer CLI entry point.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from jinja2 import Environment, StrictUndefined

from auto_gen_py_project.core.models import ProjectSpec, ProjectType
from auto_gen_py_project.utilities import write_text

_ENV = Environment(undefined=StrictUndefined, trim_blocks=True, lstrip_blocks=True, keep_trailing_newline=True)


def _r(template: str, ctx: dict[str, Any]) -> str:
    return _ENV.from_string(template).render(**ctx)


LICENSE_TEXTS = {
    "MIT": """MIT License

Copyright (c) {{ year }} {{ author }}

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
""",
    "Apache-2.0": "Apache License 2.0 — see https://www.apache.org/licenses/LICENSE-2.0\nCopyright (c) {{ year }} {{ author }}\n",
    "GPL-3.0": "GNU GPL v3 — see https://www.gnu.org/licenses/gpl-3.0.html\nCopyright (c) {{ year }} {{ author }}\n",
    "AGPL-3.0": "GNU AGPL v3 — see https://www.gnu.org/licenses/agpl-3.0.html\nCopyright (c) {{ year }} {{ author }}\n",
    "BSD-3-Clause": "BSD 3-Clause License\nCopyright (c) {{ year }} {{ author }}\n",
    "Unlicense": "This is free and unencumbered software released into the public domain.\n",
    "Proprietary": "Copyright (c) {{ year }} {{ author }}. All rights reserved.\n",
}


class BuiltinScaffold:
    """Generate a full production project for any supported ProjectType."""

    def generate(self, dest: Path, spec: ProjectSpec) -> list[Path]:
        from datetime import datetime

        ctx = spec.template_context()
        ctx["year"] = str(datetime.now().year)
        ctx["is_web"] = spec.project_type in {
            ProjectType.FASTAPI,
            ProjectType.FLASK,
            ProjectType.DJANGO,
            ProjectType.REST_API,
            ProjectType.MICROSERVICE,
        }
        ctx["is_cli"] = spec.project_type == ProjectType.CLI
        ctx["is_data"] = spec.project_type in {
            ProjectType.DATA_SCIENCE,
            ProjectType.MACHINE_LEARNING,
            ProjectType.AI,
            ProjectType.COMPUTER_VISION,
            ProjectType.JUPYTER,
        }
        written: list[Path] = []

        files: dict[str, str] = {}
        files.update(self._common(ctx, spec))
        files.update(self._type_specific(ctx, spec))

        for rel, content in files.items():
            path = dest / rel
            write_text(path, content)
            written.append(path)
        return written

    def _common(self, ctx: dict[str, Any], spec: ProjectSpec) -> dict[str, str]:
        deps = self._dependencies(spec)
        dev_deps = ["pytest>=8.0", "pytest-cov>=5.0", "ruff>=0.9", "mypy>=1.8"]
        scripts = ""
        if spec.project_type == ProjectType.CLI:
            scripts = f'\n[project.scripts]\n{ctx["project_slug"]} = "{ctx["package_name"]}.cli:main"\n'
        elif ctx["is_web"] and spec.project_type == ProjectType.FASTAPI:
            scripts = f'\n[project.scripts]\n{ctx["project_slug"]} = "{ctx["package_name"]}.main:run"\n'

        pyproject = f'''[build-system]
requires = ["setuptools>=68", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "{ctx["project_slug"]}"
version = "{ctx["version"]}"
description = "{ctx["description"]}"
readme = "README.md"
requires-python = ">={ctx["python_version"]}"
license = {{ text = "{ctx["license"]}" }}
authors = [{{ name = "{ctx["author"]}", email = "{ctx["email"]}" }}]
dependencies = {deps!r}
{scripts}
[project.optional-dependencies]
dev = {dev_deps!r}

[tool.setuptools.packages.find]
where = ["src"]

[tool.pytest.ini_options]
testpaths = ["tests"]

[tool.ruff]
line-length = 100
target-version = "py{ctx["python_version"].replace(".", "")}"

[tool.mypy]
python_version = "{ctx["python_version"]}"
strict = false
warn_return_any = true
'''

        readme = _r(
            """# {{ name }}

{{ description }}

## Requirements

- Python {{ python_version }}+

## Install

```bash
python -m pip install -e ".[dev]"
```

## Development

```bash
pytest
ruff check src tests
```

## License

{{ license }}
""",
            ctx,
        )

        gitignore = """__pycache__/
*.py[cod]
.venv/
venv/
.env
.pytest_cache/
.mypy_cache/
.ruff_cache/
.coverage
htmlcov/
dist/
build/
*.egg-info/
.idea/
.vscode/
*.ipynb_checkpoints/
"""

        editorconfig = """root = true

[*]
charset = utf-8
end_of_line = lf
insert_final_newline = true
indent_style = space
indent_size = 4

[*.{yml,yaml,json,toml,md}]
indent_size = 2
"""

        pkg_init = _r(
            '''"""{{ name }}."""

__version__ = "{{ version }}"
''',
            ctx,
        )

        test_init = ""
        test_version = _r(
            '''from {{ package_name }} import __version__


def test_version():
    assert __version__ == "{{ version }}"
''',
            ctx,
        )

        docs_index = _r("# {{ name }}\n\n{{ description }}\n", ctx)
        example = _r(
            '''"""Example usage for {{ name }}."""

from {{ package_name }} import __version__

print(f"{{ name }} v{__version__}")
''',
            ctx,
        )
        script = _r(
            """#!/usr/bin/env python
\"\"\"Developer helper scripts live here.\"\"\"
print("{{ name }} scripts")
""",
            ctx,
        )

        req_text = "\n".join(deps) + "\n"
        req_dev = "\n".join(dev_deps) + "\n"

        license_tpl = LICENSE_TEXTS.get(ctx["license"], LICENSE_TEXTS["MIT"])
        license_text = _r(license_tpl, ctx)

        files = {
            "pyproject.toml": pyproject,
            "README.md": readme,
            "LICENSE": license_text,
            ".gitignore": gitignore,
            ".editorconfig": editorconfig,
            "requirements.txt": req_text,
            "requirements-dev.txt": req_dev,
            f"src/{ctx['package_name']}/__init__.py": pkg_init,
            f"src/{ctx['package_name']}/py.typed": "",
            "tests/__init__.py": test_init,
            "tests/test_version.py": test_version,
            "docs/index.md": docs_index,
            "examples/quickstart.py": example,
            "scripts/dev.py": script,
            "assets/.gitkeep": "",
        }
        return files

    def _dependencies(self, spec: ProjectSpec) -> list[str]:
        mapping: dict[ProjectType, list[str]] = {
            ProjectType.LIBRARY: [],
            ProjectType.CLI: ["typer>=0.12", "rich>=13.7"],
            ProjectType.FASTAPI: ["fastapi>=0.110", "uvicorn[standard]>=0.27", "pydantic>=2.6"],
            ProjectType.FLASK: ["flask>=3.0"],
            ProjectType.DJANGO: ["django>=5.0"],
            ProjectType.DATA_SCIENCE: ["pandas>=2.2", "numpy>=1.26", "matplotlib>=3.8"],
            ProjectType.MACHINE_LEARNING: ["scikit-learn>=1.4", "pandas>=2.2", "numpy>=1.26"],
            ProjectType.AI: ["httpx>=0.27", "pydantic>=2.6", "rich>=13.7"],
            ProjectType.COMPUTER_VISION: ["opencv-python>=4.9", "numpy>=1.26"],
            ProjectType.REST_API: ["fastapi>=0.110", "uvicorn[standard]>=0.27"],
            ProjectType.MICROSERVICE: ["fastapi>=0.110", "uvicorn[standard]>=0.27", "httpx>=0.27"],
            ProjectType.DESKTOP: [],
            ProjectType.AUTOMATION: ["rich>=13.7"],
            ProjectType.ASYNC: ["anyio>=4.0", "httpx>=0.27"],
            ProjectType.PYPI_PACKAGE: [],
            ProjectType.JUPYTER: ["jupyter>=1.0", "pandas>=2.2", "matplotlib>=3.8"],
        }
        return list(mapping.get(spec.project_type, []))

    def _type_specific(self, ctx: dict[str, Any], spec: ProjectSpec) -> dict[str, str]:
        pkg = ctx["package_name"]
        files: dict[str, str] = {}
        t = spec.project_type

        if t == ProjectType.CLI:
            files[f"src/{pkg}/cli.py"] = _r(
                '''"""CLI entry point."""

import typer
from rich.console import Console

app = typer.Typer(help="{{ name }} CLI")
console = Console()


@app.command()
def hello(name: str = "world") -> None:
    """Say hello."""
    console.print(f"Hello, {name}!")


def main() -> None:
    app()


if __name__ == "__main__":
    main()
''',
                ctx,
            )
            files[f"src/{pkg}/__main__.py"] = f"from {pkg}.cli import main\n\nif __name__ == '__main__':\n    main()\n"

        elif t in {ProjectType.FASTAPI, ProjectType.REST_API, ProjectType.MICROSERVICE}:
            files[f"src/{pkg}/main.py"] = _r(
                '''"""{{ name }} API."""

from fastapi import FastAPI

app = FastAPI(title="{{ name }}", version="{{ version }}")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


def run() -> None:
    import uvicorn

    uvicorn.run("{{ package_name }}.main:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    run()
''',
                ctx,
            )

        elif t == ProjectType.FLASK:
            files[f"src/{pkg}/app.py"] = _r(
                '''"""{{ name }} Flask application."""

from flask import Flask, jsonify

app = Flask(__name__)


@app.get("/health")
def health():
    return jsonify({"status": "ok"})


def create_app() -> Flask:
    return app


if __name__ == "__main__":
    app.run(debug=True)
''',
                ctx,
            )

        elif t == ProjectType.DJANGO:
            files[f"src/{pkg}/manage_stub.py"] = _r(
                '''"""Django project placeholder.

Run ``django-admin startproject config .`` inside the project after install,
or expand this stub into a full Django layout.
"""

print("Install Django deps, then scaffold with django-admin.")
''',
                ctx,
            )

        elif t in {ProjectType.DATA_SCIENCE, ProjectType.MACHINE_LEARNING, ProjectType.AI, ProjectType.COMPUTER_VISION}:
            files[f"src/{pkg}/pipeline.py"] = _r(
                '''"""Core pipeline for {{ name }}."""

from __future__ import annotations


def run_pipeline() -> dict[str, str]:
    """Execute a minimal pipeline stub."""
    return {"project": "{{ name }}", "status": "ready"}
''',
                ctx,
            )
            if t == ProjectType.JUPYTER or t == ProjectType.DATA_SCIENCE:
                files["notebooks/.gitkeep"] = ""
                files["notebooks/getting_started.ipynb"] = """{
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {},
      "source": ["# Getting started\\n"]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {},
      "outputs": [],
      "source": ["print('hello from notebook')\\n"]
    }
  ],
  "metadata": {
    "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"}
  },
  "nbformat": 4,
  "nbformat_minor": 5
}
"""

        elif t == ProjectType.JUPYTER:
            files["notebooks/.gitkeep"] = ""

        elif t == ProjectType.ASYNC:
            files[f"src/{pkg}/async_app.py"] = _r(
                '''"""Async entry point for {{ name }}."""

from __future__ import annotations

import asyncio


async def main() -> None:
    print("{{ name }} async app starting")
    await asyncio.sleep(0)
    print("done")


if __name__ == "__main__":
    asyncio.run(main())
''',
                ctx,
            )

        elif t == ProjectType.DESKTOP:
            files[f"src/{pkg}/desktop.py"] = _r(
                '''"""Minimal Tkinter desktop stub for {{ name }}."""

import tkinter as tk


def main() -> None:
    root = tk.Tk()
    root.title("{{ name }}")
    tk.Label(root, text="{{ name }}").pack(padx=20, pady=20)
    root.mainloop()


if __name__ == "__main__":
    main()
''',
                ctx,
            )

        elif t == ProjectType.AUTOMATION:
            files[f"src/{pkg}/jobs.py"] = _r(
                '''"""Automation jobs for {{ name }}."""

from rich.console import Console

console = Console()


def run() -> None:
    console.print("[green]Running automation job[/]")


if __name__ == "__main__":
    run()
''',
                ctx,
            )

        else:
            # library / pypi-package
            files[f"src/{pkg}/core.py"] = _r(
                '''"""Core API for {{ name }}."""


def greet(name: str = "world") -> str:
    """Return a greeting."""
    return f"Hello, {name}!"
''',
                ctx,
            )

        return files
