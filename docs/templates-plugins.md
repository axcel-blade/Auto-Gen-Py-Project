# Templates and plugins

Applies to **auto-gen-py-project** v1.2.2.

## Built-in templates

Each built-in id under `auto_gen_py_project/templates/<id>/template.json` maps to a `ProjectType` and is rendered by the built-in scaffold engine when no Jinja `template/` tree is present.

## Jinja templates

```text
my-template/
  template.json
  template/
    README.md.j2
    src/{{ package_name }}/__init__.py.j2
```

```json
{
  "id": "my-template",
  "name": "My Template",
  "description": "Custom layout",
  "project_types": ["library"],
  "version": "1.0.0"
}
```

> Note: the `version` field in `template.json` is the **template schema/version**, not the package version.

## Plugin API

```python
from pathlib import Path
from auto_gen_py_project.plugins import Plugin, PluginManager

class MyPlugin(Plugin):
    name = "my"
    version = "1.0.0"

    def apply(self, manager: PluginManager) -> None:
        # Register additional template directories discovered at runtime.
        manager.register_template_root(Path(__file__).parent / "templates")

    def on_after_generate(self, spec, dest: Path) -> None:
        print("generated", dest)
```

Entry point group: `auto_gen_py_project.plugins`.
