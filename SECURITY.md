# Security Policy

## Supported Versions

Security fixes and dependency updates are published on the active `0.3.x` release line:

| Version | Supported |
| :--- | :--- |
| `0.3.x` (latest) | Yes |
| `< 0.3.0` | No |

---

## Trust Model: "Illustration as Code" Execution

Drawlib is a code-execution drawing library and documentation compiler (similar to Jupyter notebooks, Quarto, or Sphinx code-execution directives):

- Running `drawlib build`, `drawlib show`, or `get_dimage_from_code()` **executes Python code** contained inside ```` ```drawlib ```` Markdown fences, standalone `.py` scripts, `styles.py`, and `utils.py` with the privileges of the invoking process.
- **Only build or preview Markdown and Python sources that you trust.**
- If you need to render untrusted third-party Markdown or scripts in an automated pipeline, run Drawlib inside an isolated, unprivileged, network-disabled container (for example, using the non-root `USER drawlib` image built via `./dcli docker build --full` with `--user 10001:10001 --network=none --read-only --pids-limit=128 --memory=1g`).

---

## Reporting a Vulnerability

Please **do not** report security vulnerabilities through public GitHub issues.

Instead, report suspected vulnerabilities privately via one of the following channels:

1. **GitHub Private Vulnerability Reporting** *(Preferred)*: [Open a private security advisory](https://github.com/yuichi110/drawlib/security/advisories/new)
2. **Email**: Contact `yuichi@yuichi.com` with `[SECURITY] drawlib:` in the subject line.

Please include:
- Affected `drawlib` version and Python / OS environment
- A minimal reproduction description (for example, path traversal, HTML/XSS escaping bypass in generated docs, or archive extraction flaw)
- Expected vs. actual behavior and potential impact

We aim to acknowledge reports within **5 business days** and coordinate a fix and disclosure timeline with the reporter.
