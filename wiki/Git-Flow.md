# Git Flow

This repository follows classic Git Flow.

```text
main
  └── hotfix/*
develop
  ├── feature/*
  └── release/*
```

## Rules

1. **feature/\*** — branch from `develop`, PR back to `develop`
2. **release/x.y.z** — branch from `develop` when stabilizing a release; bump version/docs; merge to `main` and `develop`
3. **hotfix/\*** — branch from `main` for urgent fixes; merge to `main` and `develop`
4. Tag releases on `main` (for example `v1.1.0`)

## Version bump checklist

- [ ] `pyproject.toml` `version`
- [ ] `auto_gen_py_project/__init__.py` `__version__`
- [ ] `CHANGELOG.md`
- [ ] README / docs version mentions
- [ ] Tests that assert the CLI version string
