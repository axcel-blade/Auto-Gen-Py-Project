# API

Programmatic API for **auto-gen-py-project** v1.2.5.

## ProjectGenerator

```python
from pathlib import Path
from auto_gen_py_project.core.generator import ProjectGenerator
from auto_gen_py_project.core.models import ProjectSpec, ProjectType

spec = ProjectSpec(
    name="Demo",
    package_name="demo",
    project_type=ProjectType.FASTAPI,
    use_git=False,
)
ProjectGenerator().generate(spec, Path("demo-out"))
```

## Template hints (keyword matching)

Optional helpers live under `auto_gen_py_project.ai` for historical import paths.
They use simple keyword matching — not an LLM or external AI service.

```python
from auto_gen_py_project.ai import AIService
from auto_gen_py_project.core.models import ProjectType

service = AIService()
assert service.recommend_template("FastAPI microservice") == ProjectType.FASTAPI
```

## Config

```python
from auto_gen_py_project.config import load_preferences, save_preferences
```
