# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

# type: ignore

"""Unit tests for the color definitions module in l3_styles."""

import pytest

from drawlib.v0_2.private.l2_models import StaticContainer
from drawlib.v0_2.private.l3_styles._colors import (
    Colors,
    Colors140,
    ColorsBase,
    ColorsThemeDefault,
    ColorsThemeEssentials,
    ColorsThemeMonochrome,
)


class TestColors:
    """Test cases for Colors and color container classes."""

    def test_colors_classes(self):
        """Test all color container classes subclass StaticContainer."""
        classes: list[type[StaticContainer]] = [
            ColorsBase,
            Colors,
            Colors140,
            ColorsThemeEssentials,
            ColorsThemeDefault,
            ColorsThemeMonochrome,
        ]
        for cls in classes:
            assert issubclass(cls, StaticContainer)

    def test_colors_static_container_instantiation_raises(self):
        """Test that instantiating any color container class raises TypeError."""
        classes: list[type[StaticContainer]] = [
            ColorsBase,
            Colors,
            Colors140,
            ColorsThemeEssentials,
            ColorsThemeDefault,
            ColorsThemeMonochrome,
        ]
        for cls in classes:
            with pytest.raises(TypeError, match="cannot be instantiated"):
                cls()

    def test_color_values(self):
        """Test specific color constant tuple values."""
        assert ColorsBase.Transparent == (0, 0, 0, 0.0)
        assert Colors.Red == (255, 0, 0)
        assert Colors.Black == (0, 0, 0)
        assert Colors.White == (255, 255, 255)

    def test_colors_attributes(self):
        """Test that all color attributes are valid RGB or RGBA tuples."""
        classes: list[type[StaticContainer]] = [
            ColorsBase,
            Colors,
            Colors140,
            ColorsThemeEssentials,
            ColorsThemeDefault,
            ColorsThemeMonochrome,
        ]
        for cls in classes:
            # Get all public attributes that are color tuples
            for attr_name in dir(cls):
                if attr_name.startswith("_"):
                    continue
                val = getattr(cls, attr_name)
                # Ensure it is a tuple representing RGB or RGBA
                assert isinstance(val, tuple)
                assert len(val) in {3, 4}
                for item in val[:3]:
                    assert isinstance(item, int)
                    assert 0 <= item <= 255
                if len(val) == 4:
                    assert isinstance(val[3], float)
                    assert 0.0 <= val[3] <= 1.0
