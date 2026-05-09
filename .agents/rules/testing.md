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
