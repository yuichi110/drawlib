# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Unit tests for Color class."""

import pytest
from pydantic import BaseModel, ValidationError

from drawlib._core.l2_models import Color


class TestColorInstantiation:
    """Test cases for Color instantiation and validation."""

    def test_init_with_rgb_integers(self) -> None:
        """Test instantiation with 3 integer arguments."""
        c = Color(255, 128, 0)
        assert c.r == 255
        assert c.g == 128
        assert c.b == 0
        assert c.alpha == 1.0
        assert c.a == 1.0
        assert len(c) == 4

    def test_init_with_rgba(self) -> None:
        """Test instantiation with 4 arguments."""
        c = Color(255, 128, 0, 0.5)
        assert c.r == 255
        assert c.g == 128
        assert c.b == 0
        assert c.alpha == 0.5
        assert c.a == 0.5

    def test_init_with_tuple_and_list(self) -> None:
        """Test instantiation with a single tuple or list."""
        c1 = Color((10, 20, 30))
        assert c1 == (10, 20, 30, 1.0)
        c2 = Color([10, 20, 30, 0.25])
        assert c2 == (10, 20, 30, 0.25)
        assert c2.alpha == 0.25

    def test_init_with_existing_color(self) -> None:
        """Test instantiation copying an existing Color."""
        orig = Color(10, 20, 30, 0.8)
        copy = Color(orig)
        assert copy == orig
        assert copy.alpha == 0.8

    def test_init_with_hex_string(self) -> None:
        """Test instantiation with a hex color string."""
        c = Color("#ff8000")
        assert c.r == 255
        assert c.g == 128
        assert c.b == 0
        assert c.alpha == 1.0

    def test_init_with_alpha_kwarg(self) -> None:
        """Test instantiation with alpha keyword argument."""
        c = Color(100, 150, 200, alpha=0.3)
        assert c.alpha == 0.3

    def test_init_invalid_values(self) -> None:
        """Test invalid channel values raise ValueError."""
        with pytest.raises(ValueError, match="between 0 and 255"):
            Color(256, 0, 0)
        with pytest.raises(ValueError, match="between 0 and 255"):
            Color(-1, 0, 0)
        with pytest.raises(ValueError, match="between 0.0 and 1.0"):
            Color(0, 0, 0, 1.5)
        with pytest.raises(ValueError, match="between 0.0 and 1.0"):
            Color(0, 0, 0, -0.1)

    def test_init_invalid_arguments(self) -> None:
        """Test invalid argument patterns raise ValueError or TypeError."""
        with pytest.raises(ValueError):
            Color(1, 2)
        with pytest.raises((ValueError, TypeError)):
            Color(1, 2, 3, 4, 5)  # ty: ignore[too-many-positional-arguments]
        with pytest.raises(ValueError):
            Color("invalid_hex")


class TestColorProperties:
    """Test properties of Color."""

    def test_channel_properties(self) -> None:
        """Test r, g, b, alpha, a properties."""
        c = Color(10, 20, 30, 0.75)
        assert c.r == 10
        assert c.g == 20
        assert c.b == 30
        assert c.alpha == 0.75
        assert c.a == 0.75

    def test_rgb_rgba_properties(self) -> None:
        """Test rgb and rgba tuple properties."""
        c = Color(10, 20, 30, 0.75)
        assert c.rgb == (10, 20, 30)
        assert c.rgba == (10, 20, 30, 0.75)

    def test_hex_property(self) -> None:
        """Test hex property for opaque and alpha colors."""
        c_opaque = Color(255, 0, 128)
        assert c_opaque.hex == "#ff0080"
        c_alpha = Color(255, 0, 128, 0.5)
        assert c_alpha.hex == "#ff008080"

    def test_repr(self) -> None:
        """Test repr of Color."""
        assert repr(Color(255, 0, 0)) == "Color(255, 0, 0)"
        assert repr(Color(255, 0, 0, 0.5)) == "Color(255, 0, 0, alpha=0.5)"


class TestColorPatch:
    """Test Color.patch() method."""

    def test_patch_alpha(self) -> None:
        """Test patching alpha channel."""
        c = Color(100, 150, 200)
        c2 = c.patch(alpha=0.5)
        assert c2 == (100, 150, 200, 0.5)
        assert c2.alpha == 0.5
        # Original is unchanged
        assert c.alpha == 1.0

    def test_patch_channels(self) -> None:
        """Test patching individual RGB channels."""
        c = Color(100, 150, 200, 0.8)
        c2 = c.patch(r=50, b=255)
        assert c2 == (50, 150, 255, 0.8)
        assert c2.alpha == 0.8

    def test_patch_all(self) -> None:
        """Test patching all channels."""
        c = Color(10, 20, 30)
        c2 = c.patch(r=1, g=2, b=3, alpha=0.1)
        assert c2 == (1, 2, 3, 0.1)

    def test_patch_invalid(self) -> None:
        """Test patching with invalid values raises ValueError."""
        c = Color(10, 20, 30)
        with pytest.raises(ValueError):
            c.patch(alpha=2.0)
        with pytest.raises(ValueError):
            c.patch(r=300)


class TestColorFromHex:
    """Test Color.from_hex classmethod."""

    def test_from_hex_6_digits(self) -> None:
        """Test standard 6-digit hex."""
        c = Color.from_hex("#3498db")
        assert c.r == 0x34
        assert c.g == 0x98
        assert c.b == 0xDB
        assert c.alpha == 1.0

    def test_from_hex_without_hash(self) -> None:
        """Test hex without leading hash."""
        c = Color.from_hex("3498db")
        assert c.r == 0x34
        assert c.g == 0x98
        assert c.b == 0xDB
        assert c.alpha == 1.0

    def test_from_hex_3_digits(self) -> None:
        """Test short 3-digit hex."""
        c = Color.from_hex("#f80")
        assert c.r == 0xFF
        assert c.g == 0x88
        assert c.b == 0x00
        assert c.alpha == 1.0

    def test_from_hex_8_digits(self) -> None:
        """Test 8-digit hex with alpha."""
        c = Color.from_hex("#ff000080")
        assert c.r == 255
        assert c.g == 0
        assert c.b == 0
        assert round(c.alpha, 2) == 0.5

    def test_from_hex_override_alpha(self) -> None:
        """Test overriding alpha in from_hex."""
        c = Color.from_hex("#ff0000", alpha=0.25)
        assert c.alpha == 0.25

    def test_from_hex_invalid(self) -> None:
        """Test invalid hex strings raise ValueError."""
        with pytest.raises(ValueError):
            Color.from_hex("not_a_hex")
        with pytest.raises(ValueError):
            Color.from_hex("#12345")


class TestColorEqualityAndHash:
    """Test equality and hashing of Color."""

    def test_equality_with_color(self) -> None:
        """Test equality between Color instances."""
        assert Color(255, 0, 0) == Color(255, 0, 0, 1.0)
        assert Color(255, 0, 0, 0.5) != Color(255, 0, 0, 1.0)

    def test_equality_with_3_tuple(self) -> None:
        """Test equality with 3-tuple when alpha == 1.0."""
        assert Color(255, 0, 0) == (255, 0, 0)
        assert (255, 0, 0) == Color(255, 0, 0)
        # When alpha is not 1.0, not equal to 3-tuple
        assert Color(255, 0, 0, 0.5) != (255, 0, 0)

    def test_equality_with_4_tuple(self) -> None:
        """Test equality with 4-tuple."""
        assert Color(255, 0, 0, 0.5) == (255, 0, 0, 0.5)
        assert (255, 0, 0, 0.5) == Color(255, 0, 0, 0.5)

    def test_hash_in_dict_and_set(self) -> None:
        """Test that Color can be used in sets and as dictionary keys."""
        s = {Color(255, 0, 0), Color(255, 0, 0, 1.0)}
        assert len(s) == 1
        d = {Color(255, 0, 0): "red"}
        assert d[Color(255, 0, 0, 1.0)] == "red"

    def test_tuple_unpacking(self) -> None:
        """Test tuple unpacking."""
        r, g, b, a = Color(1, 2, 3, 0.4)
        assert (r, g, b, a) == (1, 2, 3, 0.4)


class TestColorPydanticIntegration:
    """Test Pydantic integration for Color."""

    class Model(BaseModel):
        """Test model for Pydantic Color validation."""

        color: Color

    def test_pydantic_parses_color(self) -> None:
        """Test Pydantic parses existing Color."""
        m = self.Model(color=Color(255, 0, 0))
        assert isinstance(m.color, Color)
        assert m.color == (255, 0, 0)

    def test_pydantic_parses_hex(self) -> None:
        """Test Pydantic parses hex string."""
        m = self.Model.model_validate({"color": "#3498db"})
        assert isinstance(m.color, Color)
        assert m.color.hex == "#3498db"

    def test_pydantic_parses_tuple(self) -> None:
        """Test Pydantic parses RGB tuple."""
        m = self.Model.model_validate({"color": (10, 20, 30)})
        assert isinstance(m.color, Color)
        assert m.color.rgb == (10, 20, 30)

    def test_pydantic_invalid_raises(self) -> None:
        """Test Pydantic rejects invalid value."""
        with pytest.raises(ValidationError):
            self.Model.model_validate({"color": "invalid"})
