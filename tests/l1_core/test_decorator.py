# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Unit tests for _decorator.py module."""

import typing

import pytest
from pydantic import ValidationError

from drawlib._core.l1_core._decorator import guarded


@guarded
def sample_guarded_func(x: int, y: str) -> str:
    """Sample guarded function for testing.

    Args:
        x: An integer parameter.
        y: A string parameter.

    Returns:
        str: Formatted string of x and y.

    """
    if x < 0:
        raise ValueError("x cannot be negative")
    return f"{x}:{y}"


class TestGuarded:
    """Test cases for the guarded decorator."""

    def test_guarded_preserves_metadata(self):
        """Test that the guarded decorator preserves original function name and docstring."""
        assert sample_guarded_func.__name__ == "sample_guarded_func"
        doc = sample_guarded_func.__doc__
        assert doc is not None
        assert "Sample guarded function for testing" in doc

    def test_guarded_validation_success(self):
        """Test guarded function execution with valid parameters."""
        res = sample_guarded_func(42, "hello")
        assert res == "42:hello"

    def test_guarded_validation_failure(self):
        """Test guarded function parameter type validation via Pydantic."""
        # y should be str, but passing an incompatible type/value if it fails validation,
        # or passing incompatible types for x.
        with pytest.raises(ValidationError):
            # Passing a string that cannot be coerced to an int for x
            sample_guarded_func(typing.cast(int, "not-an-int"), "hello")

    def test_guarded_exception_propagation(self):
        """Test that exceptions raised in the function body propagate directly without suppression."""
        with pytest.raises(ValueError, match="x cannot be negative"):
            sample_guarded_func(-5, "hello")
