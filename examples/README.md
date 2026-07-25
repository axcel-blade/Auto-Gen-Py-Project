# Example plugins

Installable sample plugins that register extended Jinja templates:

| Package | Template id | Install |
|---------|-------------|---------|
| `auto-gen-py-project-fastapi` | `fastapi-extended` | `pip install -e ./examples/auto-gen-py-project-fastapi` |
| `auto-gen-py-project-django` | `django-extended` | `pip install -e ./examples/auto-gen-py-project-django` |
| `auto-gen-py-project-ai` | `ai-extended` | `pip install -e ./examples/auto-gen-py-project-ai` |

Then:

```bash
auto-gen-py-project list-templates
auto-gen-py-project new Demo -t fastapi-extended
```
