# FAQ

## What is auto-gen-py-project?

A CLI that scaffolds production-ready Python projects (library, CLI, FastAPI, Django, data/ML, and more). It is a template-based generator — not an AI product and it does not call LLMs.

## How do I check the installed version?

```bash
auto-gen-py-project version
auto-gen-py-project --version
```

If the command is not found (scripts folder not on `PATH` — Windows, macOS, or Linux):

```bash
python -m auto_gen_py_project version
python -m auto_gen_py_project doctor
```

## Which operating systems are supported?

**Windows, macOS, and Linux.** The same CLI works on all three. CI runs tests on Ubuntu, Windows, and macOS with Python 3.12 and 3.13.

Current docs target **1.3.5**.

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
