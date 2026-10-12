# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Unit and integration tests for Canvas gear shape in drawlib.shapes."""

import pytest
from pydantic import ValidationError

from drawlib.canvas import canvas, clear
from drawlib.fonts import Font
from drawlib.shapes import gear
from drawlib.styles import Colors, Style, Styles


class TestCanvasGear:
    """Tests for the gear drawing feature in CanvasShapePolygonFeature."""

    def setup_method(self) -> None:
        """Reset canvas before each test."""
        clear()

    def test_imports_and_availability(self) -> None:
        """Verify gear function is exported and callable."""
        assert callable(gear)
        assert hasattr(canvas, "gear")

    def test_basic_gear_rendering(self) -> None:
        """Verify basic gear rendering with default ratios and optional center hole."""
        # 1. Default gear without center hole
        gear((50, 50), num_teeth=8, radius_ext=20, radius_int=15, style=Styles.PrimaryFlat)
        assert len(canvas._artists) == 1

        # 2. Gear with center hole (compound PathPatch)
        clear()
        gear(
            (50, 50),
            num_teeth=12,
            radius_ext=20,
            radius_int=15,
            hole_radius=7,
            style=Styles.PrimaryNeutral,
        )
        assert len(canvas._artists) == 1

        # 3. Custom tooth_ext_ratio and tooth_int_ratio
        clear()
        gear(
            (50, 50),
            num_teeth=10,
            radius_ext=22,
            radius_int=16,
            tooth_ext_ratio=0.45,
            tooth_int_ratio=0.45,
            hole_radius=6,
            style=Styles.SecondaryNeutral,
        )
        assert len(canvas._artists) == 1

    def test_gear_with_text_and_rotation(self) -> None:
        """Verify gear with embedded text, rotation angle, and alignment."""
        gear(
            (50, 50),
            num_teeth=8,
            radius_ext=20,
            radius_int=15,
            hole_radius=8,
            style=Styles.PrimaryNeutral.patch(angle=22.5, halign="left", valign="bottom"),
            text="Worker",
            text_style=Style(text_color=Colors.Black, text_size=12, text_font=Font.SANSSERIF_BOLD),
        )
        assert len(canvas._artists) == 2  # 1 gear PathPatch + 1 text artist

    def test_gear_shape_r_rounding(self) -> None:
        """Verify gear corner rounding via style.shape_r scalar and per-vertex tuple."""
        # Scalar shape_r
        gear(
            (50, 50),
            num_teeth=6,
            radius_ext=20,
            radius_int=14,
            hole_radius=5,
            style=Styles.AccentNeutral.patch(shape_r=0.8),
        )
        assert len(canvas._artists) == 1

        # Per-vertex tuple shape_r (4 * num_teeth = 12 for num_teeth=3)
        clear()
        radii_tuple = tuple([0.5, 1.0, 1.0, 0.5] * 3)
        gear(
            (50, 50),
            num_teeth=3,
            radius_ext=20,
            radius_int=14,
            style=Styles.Primary.patch(shape_r=radii_tuple),
        )
        assert len(canvas._artists) == 1

    def test_validation_errors(self) -> None:
        """Verify runtime parameter validation via @validate_call and value checks."""
        # Invalid num_teeth (< 3)
        with pytest.raises((ValueError, ValidationError)):
            gear((50, 50), num_teeth=2, radius_ext=20, radius_int=15, style=Styles.Primary)

        # radius_int <= 0
        with pytest.raises((ValueError, ValidationError)):
            gear((50, 50), num_teeth=8, radius_ext=20, radius_int=0, style=Styles.Primary)

        # radius_ext <= radius_int
        with pytest.raises(ValueError, match="radius_ext must be bigger than radius_int"):
            gear((50, 50), num_teeth=8, radius_ext=15, radius_int=15, style=Styles.Primary)

        with pytest.raises(ValueError, match="radius_ext must be bigger than radius_int"):
            gear((50, 50), num_teeth=8, radius_ext=12, radius_int=15, style=Styles.Primary)

        # Boundary ratios (0.0 or 1.0 or out of range)
        with pytest.raises((ValueError, ValidationError)):
            gear(
                (50, 50),
                num_teeth=8,
                radius_ext=20,
                radius_int=15,
                tooth_ext_ratio=0.0,
                style=Styles.Primary,
            )

        with pytest.raises((ValueError, ValidationError)):
            gear(
                (50, 50),
                num_teeth=8,
                radius_ext=20,
                radius_int=15,
                tooth_int_ratio=1.0,
                style=Styles.Primary,
            )

        with pytest.raises((ValueError, ValidationError)):
            gear(
                (50, 50),
                num_teeth=8,
                radius_ext=20,
                radius_int=15,
                tooth_ext_ratio=1.5,
                style=Styles.Primary,
            )

        # Invalid hole_radius (<= 0 or >= radius_int)
        with pytest.raises(ValueError, match="hole_radius must be positive and smaller than radius_int"):
            gear(
                (50, 50),
                num_teeth=8,
                radius_ext=20,
                radius_int=15,
                hole_radius=0.0,
                style=Styles.Primary,
            )

        with pytest.raises(ValueError, match="hole_radius must be positive and smaller than radius_int"):
            gear(
                (50, 50),
                num_teeth=8,
                radius_ext=20,
                radius_int=15,
                hole_radius=15.0,
                style=Styles.Primary,
            )

        # Mismatched shape_r tuple length
        with pytest.raises(ValueError, match="shape_r tuple length"):
            gear(
                (50, 50),
                num_teeth=6,
                radius_ext=20,
                radius_int=15,
                style=Styles.Primary.patch(shape_r=(1.0, 2.0, 3.0)),
            )
