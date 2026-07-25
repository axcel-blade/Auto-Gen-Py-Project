# Security Policy

## Supported versions

| Version | Supported |
|---------|-----------|
| 1.2.x   | Yes |
| 1.1.x   | Best effort |
| < 1.1   | No |

## Reporting a vulnerability

Please use [GitHub Security Advisories](https://github.com/axcel-blade/Auto-Gen-Py-Project/security/advisories/new) for undisclosed vulnerabilities.

Do **not** open a public issue for security-sensitive reports until a fix is available or maintainers approve disclosure.

Include:

- Affected version (for example `1.3.3`)
- Reproduction steps
- Impact assessment

## Hardening notes

- Template rendering uses Jinja2 with `StrictUndefined`
- Plugins loaded from entry points run with the same privileges as the invoking user
- Review third-party template and plugin packages before installing them
- Prefer pinning dependency versions in generated projects for production use
