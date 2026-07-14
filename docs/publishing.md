# Publishing to PyPI / TestPyPI

## Accounts

| Site | Account username | Package name |
|------|------------------|--------------|
| [TestPyPI](https://test.pypi.org/) | `axcelblade` | `auto-gen-py-project` |
| [PyPI](https://pypi.org/) | (your production account) | `auto-gen-py-project` |

GitHub repo owner (`axcel-blade`) and TestPyPI username (`axcelblade`) are different on purpose — Trusted Publisher settings must use the **GitHub** owner/repo names, while you log into TestPyPI as `axcelblade`.

## Security

- Never paste PyPI / TestPyPI API tokens into chat, issues, or commits.
- If a token was exposed, **revoke it immediately** and create a new one.
- Prefer [Trusted Publishing (OIDC)](https://docs.pypi.org/trusted-publishers/) over long-lived API tokens.
- For API-token uploads, Twine username is always `__token__` (not `axcelblade`); password is the token value.

## Why `invalid-publisher` happens

GitHub Actions successfully minted an OIDC token, but PyPI/TestPyPI found **no Trusted Publisher** matching it.

### Production PyPI (`deploy-pypi` job)

| Field | Required value |
|-------|----------------|
| Owner | `axcel-blade` |
| Repository | `Auto-Gen-Py-Project` |
| Workflow filename | `cd.yml` |
| Environment | `pypi` |
| Project / package name | `auto-gen-py-project` |

Configure at: https://pypi.org/manage/account/publishing/ (logged into production PyPI).

### TestPyPI (`deploy-test-pypi` job) — account `axcelblade`

| Field | Required value |
|-------|----------------|
| Owner | `axcel-blade` |
| Repository | `Auto-Gen-Py-Project` |
| Workflow filename | `cd.yml` |
| Environment | `test-pypi` |
| Project / package name | `auto-gen-py-project` |

Configure at: https://test.pypi.org/manage/account/publishing/ while logged in as **`axcelblade`**.

Also create GitHub Environments named `pypi` and/or `test-pypi`, and set repo variable `ENABLE_TEST_PYPI=true` to run the TestPyPI job on releases.

## GitHub Actions secrets

Add secrets under **Settings → Secrets and variables → Actions** (do not paste tokens in chat):

| Secret | Used for |
|--------|----------|
| `TEST_PYPI_API_TOKEN` | Publish to TestPyPI (`axcelblade`) on each GitHub Release |
| `PYPI_API_TOKEN` | Publish to production PyPI (skips OIDC when set) |

Also create GitHub Environments named `pypi` and `test-pypi`.

After adding `TEST_PYPI_API_TOKEN`, re-run the failed **CD** workflow on the `v1.2.2` release (Actions → CD → Re-run jobs), or publish a new release.

## Manual upload (local)

```bash
python -m pip install build twine
python -m build

# TestPyPI as axcelblade — create a fresh token in the website UI first
# Username must be __token__ when using an API token:
twine upload --repository testpypi dist/*
# or:
twine upload --repository-url https://test.pypi.org/legacy/ -u __token__ -p <TEST_PYPI_TOKEN> dist/*

# Production PyPI:
twine upload dist/*
```

Install a TestPyPI build:

```bash
python -m pip install -i https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ auto-gen-py-project
```
