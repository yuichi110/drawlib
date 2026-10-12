# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Unit and integration tests for Canvas cloud and brace shapes in drawlib.shapes."""

from typing import cast

import pytest
from pydantic import ValidationError

from drawlib._core.l2_types import BraceDirection, BraceSymbol, CloudVariant
from drawlib.canvas import canvas, clear
from drawlib.fonts import Font
from drawlib.shapes import brace, cloud
from drawlib.styles import Colors, Style, Styles


class TestCanvasCloudAndBrace:
    """Tests for cloud and brace drawing features in CanvasShapeBasicFeature."""

    def setup_method(self) -> None:
        """Reset canvas before each test."""
        clear()

    def test_imports_and_availability(self) -> None:
        """Verify cloud and brace functions are exported and callable."""
        assert callable(cloud)
        assert callable(brace)
        assert hasattr(canvas, "cloud")
        assert hasattr(canvas, "brace")

    def test_cloud_all_variants_and_options(self) -> None:
        """Test cloud drawing across all variants, bump_ratio, rotation, and text."""
        variants: tuple[CloudVariant, ...] = (
            "standard",
            "flat",
            "flat_bottom",
            "fluffy",
            "dense",
            "simple",
            "minimal",
        )
        for v in variants:
            cloud((50, 50), width=30, height=20, variant=v, style=Styles.PrimaryNeutral)
        assert len(canvas._artists) == len(variants)

        # Custom bump_ratio, angle, and embedded text
        clear()
        tstyle = Style(text_color=Colors.Black, text_size=11, text_font=Font.SANSSERIF_BOLD)
        cloud(
            (50, 50),
            width=40,
            height=24,
            variant="fluffy",
            bump_ratio=0.25,
            style=Styles.PrimaryDashed.patch(angle=15.0),
            text="VPC Cloud",
            text_style=tstyle,
        )
        assert len(canvas._artists) == 2

    def test_cloud_validation_errors(self) -> None:
        """Test cloud parameter validation errors."""
        with pytest.raises(ValidationError):
            cloud((50, 50), width=30, height=20, variant=cast(CloudVariant, "invalid"), style=Styles.Neutral)

        with pytest.raises(ValueError, match="width and height must be positive"):
            cloud((50, 50), width=0, height=20, style=Styles.Neutral)

        with pytest.raises(ValueError, match="bump_ratio must be strictly between"):
            cloud((50, 50), width=30, height=20, bump_ratio=0.0, style=Styles.Neutral)

        with pytest.raises(ValueError, match="bump_ratio must be strictly between"):
            cloud((50, 50), width=30, height=20, bump_ratio=1.0, style=Styles.Neutral)

    def test_brace_all_symbols_directions_and_styles(self) -> None:
        """Test brace across all symbols, directions, line_width, shape_r, and ratios."""
        symbols: tuple[BraceSymbol, ...] = (
            "{",
            "}",
            "{}",
            "curly",
            "[",
            "]",
            "[]",
            "square",
            "(",
            ")",
            "()",
            "round",
        )
        for sym in symbols:
            brace((50, 50), width=6, height=24, symbol=sym, style=Styles.PrimaryBold)
        assert len(canvas._artists) == len(symbols)

        # Directions, tip_ratio, tip_position_ratio, shape_r, and text
        clear()
        directions: tuple[BraceDirection, ...] = ("left", "right", "top", "bottom")
        for d in directions:
            brace(
                (50, 50),
                width=20,
                height=20,
                symbol="{",
                direction=d,
                tip_ratio=0.65,
                tip_position_ratio=0.35,
                style=Styles.Secondary.patch(line_width=3.0, angle=10.0),
                text="Group",
            )
        assert len(canvas._artists) == 8  # 4 PathPatches + 4 Text artists

        # Square bracket with shape_r and line-only Style / Flat Style
        clear()
        line_only_style = Style(line_color=Colors.Black, line_width=2.5)
        brace((30, 50), width=6, height=20, symbol="[", style=line_only_style.patch(shape_r=1.5))
        brace((70, 50), width=6, height=20, symbol="]", style=Styles.PrimaryFlat)
        assert len(canvas._artists) == 2

    def test_brace_validation_errors(self) -> None:
        """Test brace parameter validation errors."""
        with pytest.raises(ValidationError):
            brace((50, 50), width=6, height=20, symbol=cast(BraceSymbol, "<"), style=Styles.Primary)

        with pytest.raises(ValidationError):
            brace((50, 50), width=6, height=20, direction=cast(BraceDirection, "diagonal"), style=Styles.Primary)

        with pytest.raises(ValueError, match="width and height must be positive"):
            brace((50, 50), width=0, height=20, style=Styles.Primary)

        with pytest.raises(ValueError, match="tip_ratio must be strictly between"):
            brace((50, 50), width=6, height=20, tip_ratio=0.0, style=Styles.Primary)

        with pytest.raises(ValueError, match="tip_position_ratio must be strictly between"):
            brace((50, 50), width=6, height=20, tip_position_ratio=1.0, style=Styles.Primary)
