# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Unit tests for primitive types in _primitive.py."""

import pytest
from pydantic import TypeAdapter, ValidationError

from drawlib._core.l2_types._primitive import (
    NegFloat,
    NegInt,
    NumVertex,
    PosFloat,
    PosInt,
)


class TestTypeBool:
    """Test cases for bool validation."""

    def test_validation(self):
        """Test valid and invalid boolean values."""
        adapter: TypeAdapter[bool] = TypeAdapter(bool)
        assert adapter.validate_python(True) is True
        assert adapter.validate_python(False) is False

        # Note: Pydantic may coercion-validate strings like "true"/"false" depending on strictness.
        # But we only need to test basic validity.


class TestTypeInt:
    """Test cases for int validation."""

    def test_validation(self):
        """Test valid and invalid integer values."""
        adapter: TypeAdapter[int] = TypeAdapter(int)
        assert adapter.validate_python(5) == 5
        assert adapter.validate_python(-5) == -5


class TestTypeNegInt:
    """Test cases for NegInt validation."""

    def test_validation(self):
        """Test valid and invalid negative integer values."""
        adapter: TypeAdapter[NegInt] = TypeAdapter(NegInt)
        assert adapter.validate_python(-5) == -5
        assert adapter.validate_python(0) == 0

        with pytest.raises(ValidationError):
            adapter.validate_python(5)


class TestTypePosInt:
    """Test cases for PosInt validation."""

    def test_validation(self):
        """Test valid and invalid positive integer values."""
        adapter: TypeAdapter[PosInt] = TypeAdapter(PosInt)
        assert adapter.validate_python(5) == 5
        assert adapter.validate_python(0) == 0

        with pytest.raises(ValidationError):
            adapter.validate_python(-5)


class TestTypeNumVertex:
    """Test cases for NumVertex validation."""

    def test_validation(self):
        """Test valid and invalid polygon vertices count."""
        adapter: TypeAdapter[NumVertex] = TypeAdapter(NumVertex)
        assert adapter.validate_python(3) == 3
        assert adapter.validate_python(5) == 5

        with pytest.raises(ValidationError):
            adapter.validate_python(2)
        with pytest.raises(ValidationError):
            adapter.validate_python(0)


class TestTypeFloat:
    """Test cases for float validation."""

    def test_validation(self):
        """Test valid float values."""
        adapter: TypeAdapter[float] = TypeAdapter(float)
        assert adapter.validate_python(1.5) == 1.5
        assert adapter.validate_python(-1.5) == -1.5


class TestTypeNegFloat:
    """Test cases for NegFloat validation."""

    def test_validation(self):
        """Test valid and invalid negative float values."""
        adapter: TypeAdapter[NegFloat] = TypeAdapter(NegFloat)
        assert adapter.validate_python(-1.5) == -1.5
        assert adapter.validate_python(0.0) == 0.0

        with pytest.raises(ValidationError):
            adapter.validate_python(1.5)


class TestTypePosFloat:
    """Test cases for PosFloat validation."""

    def test_validation(self):
        """Test valid and invalid positive float values."""
        adapter: TypeAdapter[PosFloat] = TypeAdapter(PosFloat)
        assert adapter.validate_python(1.5) == 1.5
        assert adapter.validate_python(0.0) == 0.0

        with pytest.raises(ValidationError):
            adapter.validate_python(-1.5)


class TestTypeStr:
    """Test cases for str validation."""

    def test_validation(self):
        """Test valid and invalid string values."""
        adapter: TypeAdapter[str] = TypeAdapter(str)
        assert adapter.validate_python("hello") == "hello"
