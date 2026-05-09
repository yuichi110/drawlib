# Skill: Generate Unit Tests for drawlib

This skill provides a structured procedure for an AI assistant to generate high-quality unit tests for the `drawlib` project, ensuring consistency with the project's standards and testing rules.

## 1. Goal
Automatically generate comprehensive unit tests for a given module, class, or function, focusing on property validation, state management, and functional correctness.

## 2. Procedure

### Step 1: Analyze the Target Code
- Identify public classes, methods, and functions.
- For dataclasses/models, identify all attributes and their validation logic (check the `validators` calls in setters).
- Identify edge cases (e.g., `None`, empty strings, extreme values).

### Step 2: Determine Test Location and Filename
- Following the [Architecture Guidelines](file:///.agents/rules/architecture.md), place the test in the corresponding `tests/v0_x/` subdirectory.
- Example: `src/drawlib/v0_2/private/core/model.py` -> `tests/v0_2/core/test_model.py`.

### Step 3: Prepare the Boilerplate
Include the mandatory copyright header and imports:
```python
# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
# [Standard License Header]

# ruff: noqa: F403, F405
# type: ignore

from dataclasses import asdict
import pytest
from drawlib.v0_x.apis import * # Replace x with version
```

### Step 4: Generate Test Cases

#### For Style Models (Dataclasses):
1. **`test_<class_name>_init_default`**: Verify default values using `asdict()`.
2. **`test_<class_name>_init_valid`**: Verify object creation with various valid parameters.
3. **`test_<class_name>_init_invalid`**: Verify that `ValueError` is raised for invalid inputs using `pytest.raises`.
4. **`test_<class_name>_copy`**: Verify that `copy()` creates a deep copy with identical values.
5. **`test_<class_name>_merge`**: Verify that `merge()` correctly combines two style objects, prioritizing the primary one.

#### For Functional Logic:
1. **Positive Cases**: Test standard usage.
2. **Negative Cases**: Test invalid arguments or states.
3. **Mocking**: If the function interacts with Matplotlib, mock the necessary objects.

### Step 5: Self-Review and Execution
- Ensure no `import *` lint errors are blocking execution (use `noqa`).
- Run the newly created test using:
  ```bash
  uv run pytest <path_to_test_file>
  ```
- If the test fails, analyze whether the code or the test is incorrect and fix accordingly.

## 3. Example Template for Style Model Test
```python
def test_example_style():
    # Default
    assert asdict(ExampleStyle()) == {"attr1": None, "attr2": None}
    
    # Valid
    obj = ExampleStyle(attr1="valid_value")
    assert obj.attr1 == "valid_value"
    
    # Invalid
    with pytest.raises(ValueError):
        ExampleStyle(attr1="invalid_value")
        
    # Copy
    obj_copy = obj.copy()
    assert obj_copy.attr1 == obj.attr1
    assert obj_copy is not obj
    
    # Merge
    style1 = ExampleStyle(attr1="v1")
    style2 = ExampleStyle(attr2="v2")
    merged = style1.merge(style2)
    assert merged.attr1 == "v1"
    assert merged.attr2 == "v2"
```
