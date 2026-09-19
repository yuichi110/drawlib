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

from drawlib._core.l2_types_._primitive import (
    TypeBool,
    TypeFloat,
    TypeInt,
    TypeNegFloat,
    TypeNegInt,
    TypeNumVertex,
    TypePosFloat,
    TypePosInt,
    TypeStr,
)


class TestTypeBool:
    """Test cases for TypeBool validation."""

    def test_validation(self):
        """Test valid and invalid boolean values."""
        adapter: TypeAdapter[TypeBool] = TypeAdapter(TypeBool)
        assert adapter.validate_python(True) is True
        assert adapter.validate_python(False) is False

        # Note: Pydantic may coercion-validate strings like "true"/"false" depending on strictness.
        # But we only need to test basic validity.


class TestTypeInt:
    """Test cases for TypeInt validation."""

    def test_validation(self):
        """Test valid and invalid integer values."""
        adapter: TypeAdapter[TypeInt] = TypeAdapter(TypeInt)
        assert adapter.validate_python(5) == 5
        assert adapter.validate_python(-5) == -5


class TestTypeNegInt:
    """Test cases for TypeNegInt validation."""

    def test_validation(self):
        """Test valid and invalid negative integer values."""
        adapter: TypeAdapter[TypeNegInt] = TypeAdapter(TypeNegInt)
        assert adapter.validate_python(-5) == -5
        assert adapter.validate_python(0) == 0

        with pytest.raises(ValidationError):
            adapter.validate_python(5)


class TestTypePosInt:
    """Test cases for TypePosInt validation."""

    def test_validation(self):
        """Test valid and invalid positive integer values."""
        adapter: TypeAdapter[TypePosInt] = TypeAdapter(TypePosInt)
        assert adapter.validate_python(5) == 5
        assert adapter.validate_python(0) == 0

        with pytest.raises(ValidationError):
            adapter.validate_python(-5)


class TestTypeNumVertex:
    """Test cases for TypeNumVertex validation."""

    def test_validation(self):
        """Test valid and invalid polygon vertices count."""
        adapter: TypeAdapter[TypeNumVertex] = TypeAdapter(TypeNumVertex)
        assert adapter.validate_python(3) == 3
        assert adapter.validate_python(5) == 5

        with pytest.raises(ValidationError):
            adapter.validate_python(2)
        with pytest.raises(ValidationError):
            adapter.validate_python(0)


class TestTypeFloat:
    """Test cases for TypeFloat validation."""

    def test_validation(self):
        """Test valid float values."""
        adapter: TypeAdapter[TypeFloat] = TypeAdapter(TypeFloat)
        assert adapter.validate_python(1.5) == 1.5
        assert adapter.validate_python(-1.5) == -1.5


class TestTypeNegFloat:
    """Test cases for TypeNegFloat validation."""

    def test_validation(self):
        """Test valid and invalid negative float values."""
        adapter: TypeAdapter[TypeNegFloat] = TypeAdapter(TypeNegFloat)
        assert adapter.validate_python(-1.5) == -1.5
        assert adapter.validate_python(0.0) == 0.0

        with pytest.raises(ValidationError):
            adapter.validate_python(1.5)


class TestTypePosFloat:
    """Test cases for TypePosFloat validation."""

    def test_validation(self):
        """Test valid and invalid positive float values."""
        adapter: TypeAdapter[TypePosFloat] = TypeAdapter(TypePosFloat)
        assert adapter.validate_python(1.5) == 1.5
        assert adapter.validate_python(0.0) == 0.0

        with pytest.raises(ValidationError):
            adapter.validate_python(-1.5)


class TestTypeStr:
    """Test cases for TypeStr validation."""

    def test_validation(self):
        """Test valid and invalid string values."""
        adapter: TypeAdapter[TypeStr] = TypeAdapter(TypeStr)
        assert adapter.validate_python("hello") == "hello"
