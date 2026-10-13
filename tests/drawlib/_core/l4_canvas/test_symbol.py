# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Unit and integration tests for CanvasShapeSymbolFeature shapes."""

from __future__ import annotations

from typing import cast, get_args

import pytest
from pydantic import ValidationError

from drawlib._core.l2_types import MathSymbol
from drawlib.canvas import canvas, clear
from drawlib.fonts import Font
from drawlib.shapes import clock, face, gear, heart, lightning, math_symbol, moon, sun
from drawlib.styles import Colors, Style, Styles


class TestCanvasFace:
    """Tests for the face drawing feature in CanvasShapeSymbolFeature."""

    def setup_method(self) -> None:
        """Reset canvas before each test."""
        clear()

    def test_imports_and_availability(self) -> None:
        """Verify face function is exported and callable."""
        assert callable(face)
        assert hasattr(canvas, "face")

    def test_basic_face_variants(self) -> None:
        """Verify face rendering across all supported variants."""
        # 1. Default smile variant (1 outer circle + 2 eyes + 1 mouth = 4 artists)
        face((30, 50), radius=10, style=Styles.PrimaryNeutral)
        assert len(canvas._artists) == 4

        # 2. Neutral variant
        clear()
        face((30, 50), radius=10, style=Styles.Neutral, variant="neutral")
        assert len(canvas._artists) == 4

        # 3. Sad variant
        clear()
        face((30, 50), radius=10, style=Styles.WarningNeutral, variant="sad")
        assert len(canvas._artists) == 4

        # 4. Angry variant (1 outer circle + 2 eyes + 1 eyebrows + 1 mouth = 5 artists)
        clear()
        face((30, 50), radius=10, style=Styles.DangerNeutral, variant="angry")
        assert len(canvas._artists) == 5

        # 5. Surprised variant
        clear()
        face((30, 50), radius=10, style=Styles.SecondaryNeutral, variant="surprised")
        assert len(canvas._artists) == 4

        # 6. Dizzy variant (1 outer circle + 1 X-eyes path + 1 mouth = 3 artists)
        clear()
        face((30, 50), radius=10, style=Styles.WarningNeutral, variant="dizzy")
        assert len(canvas._artists) == 3

        # 7. Dead variant (1 outer circle + 1 X-eyes path + 1 mouth/tongue path = 3 artists)
        clear()
        face((30, 50), radius=10, style=Styles.DangerNeutral, variant="dead")
        assert len(canvas._artists) == 3

        # 8. Skull variant (1 skull silhouette + 2 eye sockets + 1 nasal + 1 teeth = 5 artists)
        clear()
        face((30, 50), radius=10, style=Styles.Neutral, variant="skull")
        assert len(canvas._artists) == 5

        # 9. Devil variant (1 head/horns path + 2 eyes + 1 eyebrows + 1 mouth = 5 artists)
        clear()
        face((30, 50), radius=10, style=Styles.DangerFlat, variant="devil")
        assert len(canvas._artists) == 5

    def test_face_styles_and_fallbacks(self) -> None:
        """Verify face rendering with flat, outline, and text_color fallback styles."""
        # Flat style without text_color (falls back to contrast color)
        face((30, 50), radius=10, style=Styles.PrimaryFlat)
        assert len(canvas._artists) == 4

        # Flat neutral style with text_color
        clear()
        face((30, 50), radius=10, style=Styles.PrimaryNeutralFlat)
        assert len(canvas._artists) == 4

        # Outline style (transparent fill)
        clear()
        face((30, 50), radius=10, style=Styles.PrimaryOutline)
        assert len(canvas._artists) == 4

    def test_face_with_text_and_rotation(self) -> None:
        """Verify face with embedded text and rotation angle."""
        face(
            (50, 50),
            radius=12,
            style=Styles.PrimaryNeutral.patch(angle=30.0),
            variant="smile",
            text="Actor",
            text_style=Style(text_color=Colors.Black, text_size=12, text_font=Font.SANSSERIF_BOLD),
        )
        assert len(canvas._artists) == 5  # 4 face artists + 1 text artist

    def test_face_alpha_transparency(self) -> None:
        """Verify semi-transparent face styling."""
        style = Styles.PrimaryNeutral.patch(alpha=0.5)
        face((50, 50), radius=10, style=style, variant="smile")
        assert len(canvas._artists) == 4

    def test_validation_errors(self) -> None:
        """Verify runtime parameter validation via @validate_call."""
        # Non-positive radius
        with pytest.raises((ValueError, ValidationError)):
            face((50, 50), radius=0, style=Styles.PrimaryNeutral)

        with pytest.raises((ValueError, ValidationError)):
            face((50, 50), radius=-5, style=Styles.PrimaryNeutral)

        # Invalid variant
        with pytest.raises((ValueError, ValidationError)):
            face((50, 50), radius=10, style=Styles.PrimaryNeutral, variant="invalid")  # type: ignore

        # Invalid style type
        with pytest.raises((TypeError, ValidationError)):
            face((50, 50), radius=10, style="invalid")  # type: ignore


class TestCanvasGear:
    """Tests for the gear drawing feature in CanvasShapeSymbolFeature."""

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


class TestCanvasMathSymbol:
    """Tests for the math_symbol drawing feature in CanvasShapeSymbolFeature."""

    def setup_method(self) -> None:
        """Reset canvas before each test."""
        clear()

    def test_imports_and_availability(self) -> None:
        """Verify math_symbol function is exported and callable."""
        assert callable(math_symbol)
        assert hasattr(canvas, "math_symbol")

    def test_math_symbol_all_symbols(self) -> None:
        """Test math_symbol drawing for all supported symbols and aliases."""
        style = Styles.PrimaryFlat
        symbols: tuple[MathSymbol, ...] = (
            "+",
            "plus",
            "-",
            "−",
            "minus",
            "*",
            "x",
            "×",
            "multiply",
            "/",
            "÷",
            "divide",
            "=",
            "equal",
            "!=",
            "≠",
            "not_equal",
        )
        for sym in symbols:
            math_symbol((50, 50), symbol=sym, width=20, style=style)
        assert len(canvas._artists) == len(symbols)
        # Also verify uppercase / whitespace normalization via BeforeValidator
        math_symbol((50, 50), symbol=cast(MathSymbol, " PLUS "), width=20, style=style)
        assert len(canvas._artists) == len(symbols) + 1
        assert len(get_args(MathSymbol)) > 0

    def test_math_symbol_options_and_rounding(self) -> None:
        """Test math_symbol with custom height, thickness_ratio, shape_r, angle, and text."""
        style = Styles.PrimaryNeutral.patch(shape_r=0.8, angle=15.0)
        tstyle = Style(text_color=Colors.Black, text_size=10, text_font=Font.SANSSERIF_BOLD)

        core_symbols: tuple[MathSymbol, ...] = ("+", "-", "×", "÷", "=", "≠")
        for sym in core_symbols:
            math_symbol(
                (50, 50),
                symbol=sym,
                width=24,
                height=18,
                thickness_ratio=0.3,
                style=style,
                text=sym,
                text_style=tstyle,
            )
        assert len(canvas._artists) == 12  # 6 PathPatches + 6 text artists

    def test_math_symbol_validation_errors(self) -> None:
        """Test math_symbol parameter validation errors."""
        style = Styles.Neutral

        # Invalid symbol
        with pytest.raises(ValidationError):
            math_symbol((50, 50), symbol=cast(MathSymbol, "?"), width=20, style=style)

        # Invalid negative width (PosFloat validation)
        with pytest.raises(ValidationError):
            math_symbol((50, 50), symbol="+", width=-5, style=style)

        # Invalid zero width (strict positivity check)
        with pytest.raises(ValueError, match="width and height must be positive"):
            math_symbol((50, 50), symbol="+", width=0, style=style)

        # Invalid thickness_ratio > 1.0
        with pytest.raises(ValidationError):
            math_symbol((50, 50), symbol="+", width=20, thickness_ratio=1.2, style=style)

        # Invalid thickness_ratio <= 0 or >= 1.0
        with pytest.raises(ValueError, match="thickness_ratio must be strictly between"):
            math_symbol((50, 50), symbol="+", width=20, thickness_ratio=0.0, style=style)

        with pytest.raises(ValueError, match="thickness_ratio must be strictly between"):
            math_symbol((50, 50), symbol="+", width=20, thickness_ratio=1.0, style=style)


class TestExpandedSymbolShapes:
    """Tests for expanded symbol shapes in CanvasShapeSymbolFeature."""

    def setup_method(self) -> None:
        """Reset canvas before each test."""
        clear()

    def test_exports(self) -> None:
        """Verify heart, sun, moon, clock, and lightning are exported."""
        for fn, name in (
            (heart, "heart"),
            (sun, "sun"),
            (moon, "moon"),
            (clock, "clock"),
            (lightning, "lightning"),
        ):
            assert callable(fn)
            assert hasattr(canvas, name)

    def test_heart_sun_moon_lightning(self) -> None:
        """Test heart, sun, moon, and lightning across all variants and validation."""
        for hv in ("standard", "classic", "broken"):
            heart(
                (20, 50),
                width=20,
                height=18,
                variant=hv,
                style=Styles.DangerNeutral.patch(angle=-15),
                text="H",
            )
        for suv in ("rays", "standard", "ring", "beams"):
            sun(
                (40, 50),
                radius=14,
                variant=suv,
                num_rays=10,
                style=Styles.WarningFlat.patch(angle=30),
                text="S",
            )
        for mv in ("crescent", "standard", "thin", "waxing", "half"):
            moon(
                (60, 50),
                width=18,
                height=22,
                variant=mv,
                mirror=True,
                style=Styles.AccentNeutral.patch(angle=10),
                text="M",
            )
        for lv in ("standard", "flat", "double", "flat_double", "angled", "slanted"):
            lightning(
                (80, 50),
                width=18,
                height=26,
                variant=lv,
                mirror=(lv == "angled"),
                style=Styles.WarningFlat.patch(shape_r=0.4, angle=15),
                text="Zap",
            )
        assert len(canvas._artists) >= 36

        with pytest.raises((ValueError, ValidationError)):
            sun((50, 50), radius=12, num_rays=2, style=Styles.Warning)

    def test_clock_all_variants(self) -> None:
        """Test clock across all variants including font-free digital 7-segment rendering."""
        tstyle = Style(text_color=Colors.Black, text_size=10, text_font=Font.SANSSERIF_BOLD)
        for cv in ("standard", "ticks", "dial", "stopwatch", "timer", "alarm", "digital"):
            clock(
                (50, 50),
                radius=14,
                variant=cv,
                hour=23,
                minute=48,
                style=Styles.PrimaryNeutral.patch(angle=15),
                text="SLA",
                text_style=tstyle,
            )
        assert len(canvas._artists) > 14

        # Digital clock covering all digits 0-9
        clear()
        clock((30, 50), radius=12, variant="digital", hour=10, minute=56, style=Styles.SecondaryFlat)
        clock((70, 50), radius=12, variant="digital", hour=47, minute=89, style=Styles.Neutral)
        assert len(canvas._artists) >= 4
