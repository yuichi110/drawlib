# Python Modern Stack & Tooling Standards (`python/modern_stack`)

## 1. Packaging & Dependency Management
- **PEP 621 `pyproject.toml`**: Declare metadata, `requires-python` (e.g. `>=3.11`), and dependencies in `pyproject.toml`. Avoid legacy `setup.py`, `setup.cfg`, and `Pipfile`.
- **Reproducible Lockfiles**: Commit `uv.lock` or `poetry.lock` for applications and CLIs; pin minimum bounds in libraries.
- **`deptry` Hygiene**: Every runtime third-party import must be declared in `[project.dependencies]`; test/lint tools belong in dev groups, never imported in `src/`.

## 2. Import Hygiene (`isort` / Ruff `I`)
- Group imports strictly into `future` -> `stdlib` -> `third-party` -> `first-party / relative`, separated by a single blank line.
- Sort modules and `from ... import (...)` symbols deterministically (`CONSTANT_CASE` -> `PascalCase` -> `snake_case`).
- Avoid `from module import *` and avoid late imports inside functions unless breaking a documented cycle or lazy-loading heavy optional drivers.

## 3. Modern Python Syntax & Framework Choices
- Prefer `pathlib.Path` over `os.path`, f-strings over `%` / `.format()`, and PEP 585/604 generics (`list[str]`, `X | None`) when `requires-python >= 3.10` (or with `from __future__ import annotations`).
- Prefer **Pydantic v2** (`ConfigDict`, `@field_validator`, `model_dump()`) over deprecated v1 `class Config:`, `@validator`, and `.dict()`.
- For new typed HTTP/JSON microservices, prefer **FastAPI / Litestar** over untyped WSGI **Flask** routes when OpenAPI schemas and async I/O are primary goals.
