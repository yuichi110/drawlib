# Testing Standards (Python)

## Core Principles
1. **Pytest Framework**: Use `pytest` for all unit and integration tests.
2. **Coverage Target**: Maintain test coverage of 80% or higher across domain packages.
3. **Deterministic & Isolated**: Unit tests must not depend on external networks or execution order.
4. **Mirror Structure**: Test files should mirror the `src/` directory layout (e.g. `tests/pni/test_cli.py`).
