<!-- 
    Auto-generated configuration for Gemini CLI 
    derived from Antigravity rules in "./agents/rules/" 
-->

<!-- FILE_START: ./agents/rules/architecture.md -->

# Architecture Guidelines for drawlib

This document describes the project structure and architectural principles of the `drawlib` project.

## 1. Project Root Structure
- `src/drawlib/`: The main source code directory.
- `tests/`: Contains unit and integration tests.
- `tasks/`: Automation scripts and configuration for development workflows (e.g., dependency management, building).
- `pyproject.toml`: Project metadata and tool configurations (Ruff, Pyright, uv).

## 2. Versioning Strategy
`drawlib` uses a versioned directory structure to manage library evolution while maintaining backward compatibility.

- **Version Directories**: Major versions or significant API iterations are placed in directories like `src/drawlib/v0_1/`, `src/drawlib/v0_2/`, etc.
- **Latest Version**: The highest version directory (currently `v0_2`) is considered the primary development target.
- **Top-level Entry Point**: `src/drawlib/apis.py` serves as the global gateway, re-exporting all public symbols from the latest version directory.
- **Deprecation**: Older version directories are kept for backward compatibility but are eventually deprecated. New features should only be added to the latest version.

## 3. Module Hierarchy (Internal Structure)
Each version directory (e.g., `v0_2/`) follows a strict layered architecture to separate public APIs from internal implementation.

### 3.1. Public API (`apis.py`)
- Located at `src/drawlib/v0_x/apis.py`.
- This file acts as the facade for the version. It exports only the symbols intended for end-users.
- It imports from the `private/` sub-packages and flattens the hierarchy for easier user access.

### 3.2. Implementation (`private/`)
The `private/` directory contains the actual logic and is not intended to be accessed directly by users.

- **`core/`**: Foundations of the library.
    - `model.py`: Style models (ShapeStyle, LineStyle, etc.) implemented as dataclasses.
    - `colors.py`, `fonts.py`, `theme.py`: Basic visual components.
- **`core_canvas/`**: The drawing engine.
    - `canvas.py`: Manages the drawing state and Matplotlib integration.
    - Implements basic primitives (line, rectangle, circle, text, etc.).
- **`validators/`**: Dedicated validation logic for user inputs and style attributes.
- **`dutil/`**: Low-level utilities, settings, and helper functions used across the version.
- **Feature Modules**:
    - `icons/`: Icon library integration (e.g., Phosphor icons).
    - `smartarts/`: Higher-level drawing components (e.g., flowcharts, diagrams).
    - `umls/`: Specialized UML diagram support.

## 4. Dependency Rules
- **Layered Access**: Higher-level modules (like `smartarts` or `umls`) may depend on lower-level modules (`core`, `core_canvas`), but not vice versa.
- **Private Access**: Code inside `private/` should avoid importing from other versions (e.g., `v0_2` should not depend on `v0_1`).
- **Validation**: All style model attributes must be validated using the logic in `private/validators/` via property setters.

<!-- FILE_START: ./agents/rules/code-style-guide.md -->

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

<!-- FILE_START: ./agents/rules/communication.md -->

# Communication Guidelines for drawlib Development

This document defines the communication principles for AI assistants working on the `drawlib` project.

## 1. Persona and Audience
- **Assistant Persona**: You are a senior software architect and expert pair programmer.
- **Target Audience**: The developer is an expert. Avoid over-explaining basic concepts. Focus on architectural implications, performance trade-offs, and library design consistency.

## 2. Language Policy
- **Primary Language**: Use English for all technical discussions, planning, and documentation by default.
- **Japanese Usage**: Respond in Japanese **only if** the user's request or question is written in Japanese. Even when responding in Japanese, keep technical terms and code comments in English as per the code style guide.

## 3. Communication Style
- **Be Concise**: Value the developer's time. Provide direct answers and avoid unnecessary fluff or repetitive summaries.
- **Technical Depth**: Use precise technical terminology. When proposing changes, explain the "why" behind design decisions.
- **Proactive Thinking**: If you spot potential bugs, edge cases, or opportunities for refactoring while performing a task, bring them up.
- **Context Awareness**: Always consider the library's goal: "Illustration as Code." Ensure new features or changes align with this philosophy (e.g., maintainability, readability of drawing code).

## 4. Interaction Workflow
- **Planning**: For non-trivial tasks, provide a clear, step-by-step implementation plan before writing code.
- **Verification**: After implementation, summarize what was tested and how the changes were verified (e.g., "Verified with `pytest`," "Checked visual output").
- **Error Reporting**: If a command fails or a lint error occurs, provide a concise diagnosis and a proposed fix.

## 5. Recommended Best Practices for Expert Collaboration
- **Review before Execution**: When suggesting significant architectural changes, ask for the developer's design philosophy if it's not clear.
- **Performance & Scalability**: Always consider the performance of drawing operations, especially when dealing with many shapes or complex paths.
- **Backward Compatibility**: `drawlib` is a library. Always consider whether a change breaks existing user code and suggest migration paths if necessary.
- **API Ergonomics**: Prioritize the ease of use for the end-users of `drawlib`. Suggest API improvements that make drawing code more intuitive.

<!-- FILE_START: ./agents/rules/testing.md -->

# Testing Guidelines for drawlib

This document defines the standards and best practices for writing tests in the `drawlib` project.

## 1. General Principles
- **Test Framework**: Use `pytest`.
- **Target Version**: Ensure tests are written for the specific version directory (e.g., `tests/v0_2/`).
- **Isolation**: Tests should be isolated and not depend on external network or specific local file paths (unless in `tests/assets/`).
- **Reproducibility**: Use fixed seeds or constant values for any pseudo-random operations to ensure consistent results.

## 2. Test Structure and Naming
- **Directory Mirroring**: The directory structure in `tests/v0_x/` should mirror the `src/drawlib/v0_x/private/` structure where possible.
- **File Names**: All test files must be prefixed with `test_` (e.g., `test_validator.py`).
- **Function Names**: All test functions must start with `test_` (e.g., `test_icon_style()`).
- **Conftest**: Use `conftest.py` for shared fixtures within a directory or version.

## 3. Writing Tests
- **Assertions**: Use standard Python `assert` statements.
- **Exception Testing**: Use `pytest.raises(ExceptionClass)` to verify that specific errors are raised for invalid inputs.
- **Data Comparison**: For style models, use `dataclasses.asdict()` to compare the state of objects against expected dictionaries.
- **Public API usage**: In tests, it is generally acceptable to use `from drawlib.v0_x.apis import *` to simulate how a user would interact with the library. Use `# ruff: noqa: F403, F405` if necessary.

## 4. Specific Test Types
### 4.1. Model Tests
- Verify that dataclasses correctly store attributes.
- Verify that property setters correctly validate inputs and raise `ValueError` for invalid data.
- Test `copy()` and `merge()` methods for consistency and deep copying.

### 4.2. Drawing Tests (Functional)
- For functions that generate Matplotlib patches or shapes, verify that the resulting objects have the expected properties (coordinates, colors, z-order).
- Avoid checking the exact visual rendering pixel-by-pixel unless specifically required (e.g., regression testing for image output).

## 5. Mocking and Patching
- Use `unittest.mock` (or `pytest-mock` if preferred) to isolate components.
- Mock the Matplotlib backend or figure/axes objects when testing drawing logic without wanting to display a window.

## 6. Execution
- Run tests using the `task` runner to ensure the correct environment and version:
    - `task utest:v0.2:all` (Runs all tests for v0.2)
    - `task utest:docker` (Runs tests in a clean Docker environment)

