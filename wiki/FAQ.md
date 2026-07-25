# FAQ

## What is auto-gen-py-project?

A CLI that scaffolds production-ready Python projects (library, CLI, FastAPI, Django, data/ML, and more). It is a template-based generator — not an AI product and it does not call LLMs.

## How do I check the installed version?

```bash
auto-gen-py-project version
```

Current docs target **1.2.5**.

## Does generation require an API key?

No. Scaffolding runs fully offline aside from optional dependency installs you choose to run.

## How do I pick a template from a description?

```bash
auto-gen-py-project new Shop --describe "FastAPI service with Docker"
```

Matching is simple keyword/heuristics against built-in project types.

## Where are user defaults stored?

TOML/YAML/JSON files named `auto-gen-py-project.*` in the project directory, `~/.config/auto-gen-py-project/`, or `$HOME`.

## How do I add a custom template?

Ship a directory with `template.json` + `template/` Jinja files, or distribute a plugin package with the `auto_gen_py_project.templates` entry point.
