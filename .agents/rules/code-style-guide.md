---
trigger: always_on
---

# Code Style Guide for drawlib

This document defines the coding standards and style guidelines for the `drawlib` project. All contributors must follow these rules to ensure consistency, readability, and maintainability.

## 1. General Principles
- **Target Python Version**: Python 3.10 or higher.
- **Standard Compliance**: Follow [PEP 8](https://peps.python.org/pep-0008/) unless otherwise specified here.
- **Formatting & Linting**: 
    - Use `ruff` for both linting and formatting.
    - Max line length is **120** characters.
    - Use `pyright` for static type checking.

## 2. Naming Conventions
- **Modules and Packages**: `snake_case`. Keep names short and descriptive.
- **Classes**: `PascalCase`.
- **Functions and Methods**: `snake_case`.
- **Variables and Constants**: `snake_case`. (Note: Some constants might use `UPPER_SNAKE_CASE` if they are truly global constants).
- **Private Members**: Prefix with a single underscore `_` for internal class/module attributes or methods.
- **Type Variables**: Use `PascalCase` (e.g., `T`, `ShapeT`).

## 3. Type Hinting
- **Mandatory Typing**: All public functions and methods **must** have complete type hints for arguments and return values.
- **Modern Syntax**: Use `from __future__ import annotations` to allow forward references and modern type syntax.
- **Specific Types**: Use `List`, `Tuple`, `Dict`, `Union`, `Optional`, and `Literal` from the `typing` module (or built-in types for Python 3.10+ where appropriate).
- **Avoid `Any`**: Minimize the use of `Any`. Be as specific as possible.

## 4. Documentation (Docstrings)
- **Convention**: Follow the **Google Python Style Guide** for docstrings.
- **Mandatory Docstrings**: All public modules, classes, and functions/methods must have a docstring.
- **Content**:
    - **Classes**: Document all attributes in the `Attributes` section.
    - **Functions/Methods**: Include `Args`, `Returns`, and `Raises` sections if applicable.
- **Brief vs. Detailed**: Provide a concise one-line summary followed by a more detailed explanation if the logic is complex.
- **Type Annotations in Docstrings**:
    - **For functions decorated with `@guarded`**:
        - Use explicit base Python types and `Union` / `Literal` syntax (e.g., `tuple[float, float]`, `Literal["->", "<-", "<->", "-"] | str`).
        - Do **not** use internal type aliases (e.g., `TypeCoordinate`, `TypeArrowHead`) to ensure better IDE support for end-users.
    - **For internal functions (NOT decorated with `@guarded`)**:
        - Use internal type aliases (e.g., `TypeCoordinate`, `TypeArrowHead`) to maintain consistency with the function signature.
    - **Line Length**: Docstring lines must not exceed **120** characters. Wrap long type definitions or descriptions if necessary.

## 5. Implementation Patterns
- **Data Modeling**: 
    - Use `@dataclasses.dataclass` for style and data models.
    - **Strict Rule**: Do **not** use external validation libraries like Pydantic or Marshmallow for core models.
    - **Validation**: Use `@property` and setters to implement attribute validation. Call validator functions from `drawlib.v0_2.private.validators`.
- **Error Handling**:
    - Use the `@error_handler` decorator for public-facing methods and functions to ensure consistent error reporting.
    - Raise descriptive `ValueError` or custom exceptions when validation fails.
- **Immutability/Copying**: 
    - Provide a `copy()` method (using `deepcopy`) for style objects to prevent unintended side effects from shared state.

## 6. Imports
- **Ordering**:
    1. Standard library imports.
    2. Third-party library imports.
    3. Local library imports (`drawlib`).
- **Style**:
    - Use absolute imports (e.g., `from drawlib.v0_2.private.core.fonts import Font`).
    - Avoid `import *`.
    - Group imports from the same module.

## 7. File Header
All Python source files must start with the following copyright and license header:

```python
# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.
```

## 8. Tool Configuration
Reference `pyproject.toml` for the exact configuration of linting tools:
- `[tool.ruff]` and `[tool.ruff.lint]`
- `[tool.pyright]`
