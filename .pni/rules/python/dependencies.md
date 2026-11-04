# Dependency Management Standards (Python)

## Core Principles
1. **PEP 621 Standard**: Define dependencies clearly in `pyproject.toml`.
2. **Deterministic Locking**: Always commit a lockfile (`uv.lock`) for reproducible builds.
3. **Separate Dev Dependencies**: Place testing and linting tools in `[dependency-groups].dev`.
4. **Regular Auditing**: Regularly check for outdated or vulnerable packages.
