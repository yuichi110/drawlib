# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Unit tests for image types in _image.py."""

import pytest
from pydantic import TypeAdapter, ValidationError

from drawlib.v0_2.private.l2_types_._image import (
    TypeImageFormat,
    TypeImageQuality,
    TypeImageResample,
    TypeImageZoom,
)


class TestImageTypeFormat:
    """Test cases for TypeImageFormat validation."""

    def test_validation(self):
        """Test valid and invalid image formats."""
        adapter: TypeAdapter[TypeImageFormat] = TypeAdapter(TypeImageFormat)
        assert adapter.validate_python("png") == "png"
        assert adapter.validate_python("jpg") == "jpg"
        assert adapter.validate_python("webp") == "webp"
        assert adapter.validate_python("pdf") == "pdf"

        with pytest.raises(ValidationError):
            adapter.validate_python("gif")


class TestImageTypeZoom:
    """Test cases for TypeImageZoom validation."""

    def test_validation(self):
        """Test valid and invalid zoom factors."""
        adapter: TypeAdapter[TypeImageZoom] = TypeAdapter(TypeImageZoom)
        assert adapter.validate_python(1.0) == 1.0
        assert adapter.validate_python(0.1) == 0.1

        with pytest.raises(ValidationError):
            adapter.validate_python(0.0)
        with pytest.raises(ValidationError):
            adapter.validate_python(-0.5)


class TestImageTypeQuality:
    """Test cases for TypeImageQuality validation."""

    def test_validation(self):
        """Test valid and invalid image qualities."""
        adapter: TypeAdapter[TypeImageQuality] = TypeAdapter(TypeImageQuality)
        assert adapter.validate_python(95) == 95
        assert adapter.validate_python(0) == 0
        assert adapter.validate_python(100) == 100

        with pytest.raises(ValidationError):
            adapter.validate_python(-1)
        with pytest.raises(ValidationError):
            adapter.validate_python(101)


class TestImageTypeResample:
    """Test cases for TypeImageResample validation."""

    def test_validation(self):
        """Test valid and invalid resample options."""
        adapter: TypeAdapter[TypeImageResample] = TypeAdapter(TypeImageResample)
        for val in ["nearest", "box", "bilinear", "hamming", "bicubic", "lanczos"]:
            assert adapter.validate_python(val) == val

        with pytest.raises(ValidationError):
            adapter.validate_python("invalid")
