# Contributing to Drawlib

Thank you for your interest in contributing to **Drawlib**! Whether you are fixing a bug, improving documentation, adding icon bindings, or proposing a new high-level diagram/SmartArt component, contributions are very welcome.

---

## Quick Setup for Contributors

Drawlib targets **Python 3.11+** (primary development on Python 3.12) and uses [`uv`](https://docs.astral.sh/uv/) plus our unified developer CLI `./dcli` for all routine checks, tests, and documentation builds:

```bash
# 1. Clone your fork and install development dependencies
git clone https://github.com/yuichi110/drawlib.git
cd drawlib
uv sync

# 2. Run static analysis (Ruff lint/format, Ty type check, docstring check)
./dcli code-check all

# 3. Run unit & integration tests
./dcli test drawlib
```

For the complete developer workflow, repository layout, and AI pair-programming rules, please read the **[Developer Guide (`docs_src/README_DEV.md`)](../docs_src/README_DEV.md)** and the specification files in **[`.agents/rules/`](../.agents/rules/)**.

---

## Pull Request Checklist

Before opening a Pull Request, please verify:

1. **Code Quality**: `./dcli code-check all` passes with zero errors.
2. **Python 3.11+ Compatibility**: Library code under `src/drawlib/` maintains compatibility with Python `3.11`, `3.12`, and `3.13`.
3. **Unit Tests**: Relevant tests pass via `./dcli test target <module_or_path>` (add unit tests under `tests/drawlib/` for new functionality or bug fixes).
4. **Visual & Documentation Check *(when modifying rendering or public APIs)***:
   - Preview affected diagrams with `-g` (`uv run drawlib show ... -g`) to ensure crisp alignment and zero text clipping.
   - Keep `docs_src/site/en/` and `docs_src/site/ja/` in structural parity if updating official documentation (`./dcli docs build site --no-clean && ./dcli docs serve site --check`).

---

## Community & Security

- **Code of Conduct**: Participation in this project is governed by our [Code of Conduct](../CODE_OF_CONDUCT.md).
- **Security Vulnerabilities**: Please report suspected security issues privately following [`SECURITY.md`](../SECURITY.md) rather than opening a public issue.

---

## License

By contributing to Drawlib, you agree that your contributions will be licensed under the **Apache License, Version 2.0**.
