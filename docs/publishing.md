# Publishing (TestPyPI + PyPI)

Applies to package **auto-gen-py-project** v1.2.6+.

On each GitHub Release, CD publishes to **TestPyPI**, then **production PyPI**.

## Accounts

| Site | Username | Package |
|------|----------|---------|
| [TestPyPI](https://test.pypi.org/) | `axcelblade` | `auto-gen-py-project` |
| [PyPI](https://pypi.org/) | `axcelblade` | `auto-gen-py-project` |

## GitHub secrets

| Secret | Where |
|--------|--------|
| `TEST_PYPI_API_TOKEN` | TestPyPI API token |
| `PYPI_API_TOKEN` | Production PyPI API token |

Create tokens at:

- https://test.pypi.org/manage/account/token/
- https://pypi.org/manage/account/token/

Then: GitHub → **Settings → Secrets and variables → Actions**

Twine / `pypa/gh-action-pypi-publish` use username **`__token__`** with the secret as the password.

**Never** commit tokens or paste them in issues/chat. Revoke any token that was exposed.

## Environments

Create Environments (Settings → Environments):

| Environment | Purpose |
|-------------|---------|
| `test-pypi` | TestPyPI deploy job |
| `pypi` | Production PyPI deploy job |

Both jobs request `id-token: write` so Trusted Publishing (OIDC) can work when the matching API token secret is unset.

## Trusted Publisher (OIDC) — optional

### TestPyPI

https://test.pypi.org/manage/account/publishing/

| Field | Value |
|-------|--------|
| Owner | `axcel-blade` |
| Repository | `Auto-Gen-Py-Project` |
| Workflow filename | `cd.yml` |
| Environment | `test-pypi` |
| Project name | `auto-gen-py-project` |

### PyPI

https://pypi.org/manage/account/publishing/

| Field | Value |
|-------|--------|
| Owner | `axcel-blade` |
| Repository | `Auto-Gen-Py-Project` |
| Workflow filename | `cd.yml` |
| Environment | `pypi` |
| Project name | `auto-gen-py-project` |

## Security

- Never commit or paste API tokens.
- Revoke any token that was exposed in chat or logs.
- Prefer short-lived tokens scoped to project `auto-gen-py-project`.
