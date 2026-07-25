# Cookbook

Practical recipes for **auto-gen-py-project** v1.3.4.

## FastAPI service with Docker

```bash
auto-gen-py-project new InventoryAPI -t fastapi --docker --path ./inventory-api
```

## Plain init (creates root folder)

```bash
auto_gen_py_project init
# → ./my-project/

auto_gen_py_project init --name cool-lib
# → ./cool-lib/
```

## Flag --init (files in current / specific folder)

```bash
cd my-existing-folder
auto_gen_py_project --init --force
# or
auto_gen_py_project --init --path ./my-existing-folder --force
```

## Template from a short description

```bash
auto-gen-py-project new Shop --describe "Flask storefront with pytest"
```

## uv lockfile on scaffold

```bash
auto-gen-py-project new App -t library -m uv --lock --no-git
```

## Example FastAPI plugin template

```bash
pip install -e ./examples/auto-gen-py-project-fastapi
auto-gen-py-project new Shop -t fastapi-extended --no-git
```

## Programmatic generation

```python
from pathlib import Path
from auto_gen_py_project.core.generator import ProjectGenerator
from auto_gen_py_project.core.models import ProjectSpec, ProjectType

ProjectGenerator().generate(
    ProjectSpec(name="Batch", package_name="batch", project_type=ProjectType.AUTOMATION, use_git=False),
    Path("batch-out"),
)
```
