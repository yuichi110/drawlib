# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Unit tests for color type annotations in l2_types."""

import pytest
from pydantic import TypeAdapter, ValidationError

from drawlib._core.l2_types import (
    Alpha,
    ColorRGB,
    ColorRGBA,
    RGBChannel,
)


class TestColorTypeAnnotations:
    """Test cases for color type definitions in l2_types."""

    def test_type_alpha(self) -> None:
        """Test Alpha validation."""
        adapter: TypeAdapter[Alpha] = TypeAdapter(Alpha)
        assert adapter.validate_python(0.5) == 0.5
        assert adapter.validate_python(0.0) == 0.0
        assert adapter.validate_python(1.0) == 1.0
        with pytest.raises(ValidationError):
            adapter.validate_python(-0.1)
        with pytest.raises(ValidationError):
            adapter.validate_python(1.1)

    def test_type_rgb_channel(self) -> None:
        """Test RGBChannel validation."""
        adapter: TypeAdapter[RGBChannel] = TypeAdapter(RGBChannel)
        assert adapter.validate_python(0) == 0
        assert adapter.validate_python(255) == 255
        with pytest.raises(ValidationError):
            adapter.validate_python(-1)
        with pytest.raises(ValidationError):
            adapter.validate_python(256)

    def test_type_color_rgb(self) -> None:
        """Test ColorRGB validation."""
        adapter: TypeAdapter[ColorRGB] = TypeAdapter(ColorRGB)
        assert adapter.validate_python((255, 0, 128)) == (255, 0, 128)
        with pytest.raises(ValidationError):
            adapter.validate_python((255, 0, 128, 0.5))
        with pytest.raises(ValidationError):
            adapter.validate_python((256, 0, 128))

    def test_type_color_rgba(self) -> None:
        """Test ColorRGBA validation."""
        adapter: TypeAdapter[ColorRGBA] = TypeAdapter(ColorRGBA)
        assert adapter.validate_python((255, 0, 128, 0.5)) == (255, 0, 128, 0.5)
        with pytest.raises(ValidationError):
            adapter.validate_python((255, 0, 128))
        with pytest.raises(ValidationError):
            adapter.validate_python((255, 0, 128, 1.5))
