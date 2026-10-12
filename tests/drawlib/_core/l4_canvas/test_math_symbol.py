# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Unit and integration tests for Canvas math_symbol shape in drawlib.shapes."""

from typing import cast, get_args

import pytest
from pydantic import ValidationError

from drawlib._core.l2_types import MathSymbol
from drawlib.canvas import canvas, clear
from drawlib.fonts import Font
from drawlib.shapes import math_symbol
from drawlib.styles import Colors, Style, Styles


class TestCanvasMathSymbol:
    """Tests for the math_symbol drawing feature in CanvasShapePolygonFeature."""

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
