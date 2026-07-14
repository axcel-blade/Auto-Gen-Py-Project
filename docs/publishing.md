# Publishing (TestPyPI only)

Applies to package **auto-gen-py-project** v1.2.4+.

This project’s CD workflow publishes **only to TestPyPI** on GitHub Releases.

## Account

| Site | Username | Package |
|------|----------|---------|
| [TestPyPI](https://test.pypi.org/) | `axcelblade` | `auto-gen-py-project` |

## Fix: `ACTIONS_ID_TOKEN_REQUEST_TOKEN was unset`

The publish job must request an OIDC token when using Trusted Publishing:

```yaml
permissions:
  id-token: write
  contents: read
```

That is set on the `deploy-test-pypi` job in `.github/workflows/cd.yml`.

## Recommended: API token secret

1. Log into TestPyPI as **`axcelblade`**
2. Create a token at https://test.pypi.org/manage/account/token/
3. GitHub → **Settings → Secrets and variables → Actions**
   - Name: `TEST_PYPI_API_TOKEN`
   - Value: the new token (**never** paste tokens in chat/issues)
4. Create Environment **`test-pypi`** (Settings → Environments)
5. Re-run the CD workflow for the release (or publish a new patch release so the updated workflow is on the tag)

Twine / the publish action use username **`__token__`** with that secret as the password.

## Alternative: Trusted Publisher (OIDC)

On https://test.pypi.org/manage/account/publishing/ (as `axcelblade`), add:

| Field | Value |
|-------|--------|
| Owner | `axcel-blade` |
| Repository | `Auto-Gen-Py-Project` |
| Workflow filename | `cd.yml` |
| Environment | `test-pypi` |
| Project name | `auto-gen-py-project` |

Then you can omit `TEST_PYPI_API_TOKEN` (OIDC will be used).

## Security

- Never commit or paste API tokens.
- Revoke any token that was exposed in chat or logs.
- Production PyPI deploy is **disabled** in CD by design.
