# Cookbook

Practical recipes for **auto-gen-py-project** v1.1.0.

## FastAPI service with Docker

```bash
auto-gen-py-project new InventoryAPI -t fastapi --docker --path ./inventory-api
```

## Library destined for PyPI

```bash
auto-gen-py-project new CoolLib -t pypi-package --no-git
```

## Heuristic “AI” template pick

```bash
auto-gen-py-project new Shop --ai "Flask storefront with pytest"
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
