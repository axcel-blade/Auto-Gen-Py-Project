# FAQ

## What is auto-gen-py-project?

A CLI that scaffolds production-ready Python projects (library, CLI, FastAPI, Django, data/ML, and more).

## How do I check the installed version?

```bash
auto-gen-py-project version
```

Current docs target **1.2.3**.

## Does generation require an AI API key?

No. The default AI layer uses heuristics. Real LLM backends can be plugged in later via `AIProvider`.

## Where are user defaults stored?

TOML/YAML/JSON files named `auto-gen-py-project.*` in the project directory, `~/.config/auto-gen-py-project/`, or `$HOME`.

## How do I add a custom template?

Ship a directory with `template.json` + `template/` Jinja files, or distribute a plugin package with the `auto_gen_py_project.templates` entry point.
