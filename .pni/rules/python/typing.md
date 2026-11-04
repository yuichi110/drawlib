# Typing Standards (Python)

## Core Principles
1. **Mandatory Type Annotations**: All public functions and methods must have complete parameter and return type hints.
2. **Modern Syntax**: Use `from __future__ import annotations` and standard collection types (`list`, `dict`, `tuple`).
3. **Minimize `Any`**: Avoid `Any`. Use `Union`, `Optional`, `TypeVar`, or `Protocol` for generic interfaces.
4. **Static Type Checking**: Pass static type verification (e.g., Ty or Pyright) with zero errors.
