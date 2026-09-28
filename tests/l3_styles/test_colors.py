# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Unit tests for the color definitions module in l3_styles."""

import pytest
from pydantic import BaseModel, ValidationError

from drawlib._core.l2_types import Color
from drawlib.preset_colors import (
    BaseColors,
    Colors,
    Colors16,
    Colors140,
    Colors140Model,
    DefaultColors,
    GoogleColors,
    MonochromeColors,
    default_colors,
    google_colors,
    monochrome_colors,
)


class TestColors:
    """Test cases for BaseColors and color container instances."""

    def test_colors_classes(self) -> None:
        """Test all color model classes subclass BaseColors and BaseModel."""
        classes: list[type[BaseColors]] = [
            BaseColors,
            Colors16,
            Colors140Model,
            DefaultColors,
            GoogleColors,
            MonochromeColors,
        ]
        for cls in classes:
            assert issubclass(cls, BaseColors)
            assert issubclass(cls, BaseModel)

    def test_colors_instances(self) -> None:
        """Test all color singletons are instances of BaseColors."""
        instances: list[BaseColors] = [
            Colors,
            Colors140,
            default_colors,
            google_colors,
            monochrome_colors,
        ]
        for inst in instances:
            assert isinstance(inst, BaseColors)
            assert isinstance(inst, BaseModel)

    def test_immutability(self) -> None:
        """Test that modifying attributes on frozen instances raises ValidationError."""
        with pytest.raises(ValidationError):
            default_colors.Red = Color(0, 0, 0)

    def test_patch(self) -> None:
        """Test that patch() returns a new instance with updated color."""
        patched = default_colors.patch(Red=Color(10, 20, 30))
        assert patched.Red == (10, 20, 30)
        assert default_colors.Red == (255, 23, 23)
        assert isinstance(patched, DefaultColors)

    def test_dict_and_iter(self) -> None:
        """Test dictionary-like access and iteration."""
        assert default_colors["Red"] == (255, 23, 23)
        with pytest.raises(KeyError):
            _ = default_colors["NonExistent"]

        color_dict = dict(default_colors)
        assert "Red" in color_dict
        assert color_dict["Red"] == (255, 23, 23)

    def test_color_values(self) -> None:
        """Test specific color constant tuple values."""
        assert BaseColors.Transparent == (0, 0, 0, 0.0)
        assert Colors.Red == (255, 0, 0)
        assert Colors.Black == (0, 0, 0)
        assert Colors.White == (255, 255, 255)
        assert default_colors.Red == (255, 23, 23)
        assert default_colors.Gray5 == (38, 42, 50)
        assert default_colors.Blue2 == (111, 111, 239)
        assert monochrome_colors.Gray5 == (75, 75, 75)
        assert google_colors.Black == (0, 0, 0)

    def test_colors_attributes(self) -> None:
        """Test that all color attributes on instances are valid Color instances."""
        instances: list[BaseColors] = [
            Colors,
            Colors140,
            default_colors,
            google_colors,
            monochrome_colors,
        ]
        for inst in instances:
            for field_name in inst.__class__.model_fields:
                val = getattr(inst, field_name)
                if val is None:
                    if isinstance(inst, (Colors16, Colors140Model)):
                        assert field_name in {
                            "Primary",
                            "Secondary",
                            "Accent",
                            "Muted",
                            "Light",
                            "Dark",
                            "Danger",
                            "Success",
                            "Canvas",
                        }
                    else:
                        assert isinstance(inst, MonochromeColors) and field_name in {"Danger", "Success"}
                    continue
                assert isinstance(val, Color)
                assert len(val) in {3, 4}
                for item in val[:3]:
                    assert isinstance(item, int)
                    assert 0 <= item <= 255
                if len(val) == 4:
                    assert isinstance(val[3], float)
                    assert 0.0 <= val[3] <= 1.0

    def test_semantic_colors(self) -> None:
        """Test semantic color properties on palettes that define them."""
        semantic_instances: list[BaseColors] = [
            default_colors,
            google_colors,
            monochrome_colors,
        ]
        for inst in semantic_instances:
            for sem in ("Primary", "Secondary", "Accent", "Muted", "Light", "Dark", "Canvas"):
                val = getattr(inst, sem)
                assert isinstance(val, Color)
                # Lowercase property access
                lower_val = getattr(inst, sem.lower())
                assert lower_val == val
                # Dictionary item access (both cases)
                assert inst[sem] == val
                assert inst[sem.lower()] == val

        # Colors and Colors140 do not define semantic colors
        for inst in (Colors, Colors140):
            for sem in ("Primary", "Secondary", "Accent", "Muted", "Light", "Dark", "Danger", "Success", "Canvas"):
                assert getattr(inst, sem) is None
                with pytest.raises(AttributeError):
                    _ = getattr(inst, sem.lower())
                with pytest.raises(KeyError):
                    _ = inst[sem]
                with pytest.raises(KeyError):
                    _ = inst[sem.lower()]

        # Danger and Success on color palettes (excluding Monochrome)
        chromatic_instances: list[BaseColors] = [
            default_colors,
            google_colors,
        ]
        for inst in chromatic_instances:
            for sem in ("Danger", "Success"):
                val = getattr(inst, sem)
                assert isinstance(val, Color)
                lower_val = getattr(inst, sem.lower())
                assert lower_val == val
                assert inst[sem] == val
                assert inst[sem.lower()] == val

        # Monochrome intentionally leaves Danger and Success as None
        assert monochrome_colors.Danger is None
        assert monochrome_colors.Success is None
        with pytest.raises(AttributeError):
            _ = monochrome_colors.danger
        with pytest.raises(AttributeError):
            _ = monochrome_colors.success
        with pytest.raises(KeyError):
            _ = monochrome_colors["Danger"]
        with pytest.raises(KeyError):
            _ = monochrome_colors["danger"]
