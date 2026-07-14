# API

Programmatic API for **auto-gen-py-project** v1.2.3.

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

## AIProvider

```python
from auto_gen_py_project.ai import AIProvider, AIService
from auto_gen_py_project.core.models import ProjectType

class MyAI(AIProvider):
    name = "my-ai"

    def recommend_template(self, description: str) -> ProjectType:
        ...

    def enrich_spec(self, spec, prompt: str):
        ...

    def generate_snippet(self, prompt: str, *, language: str = "python") -> str:
        ...

AIService(MyAI())
```

## Config

```python
from auto_gen_py_project.config import load_preferences, save_preferences
```
