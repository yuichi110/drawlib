# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Unit and integration tests for CanvasShapeContainerFeature shapes."""

from __future__ import annotations

from typing import cast

import pytest
from pydantic import ValidationError

from drawlib._core.l2_types import BraceDirection, BraceSymbol, CloudVariant, DocumentVariant
from drawlib.canvas import canvas, clear
from drawlib.fonts import Font
from drawlib.shapes import brace, cloud, cube, cylinder, document, funnel
from drawlib.styles import Colors, Style, Styles


class TestCanvasCylinder:
    """Tests for the cylinder drawing feature in CanvasShapeContainerFeature."""

    def setup_method(self) -> None:
        """Reset canvas before each test."""
        clear()

    def test_imports_and_availability(self) -> None:
        """Verify cylinder function is exported and callable."""
        assert callable(cylinder)
        assert hasattr(canvas, "cylinder")

    def test_basic_cylinder_rendering(self) -> None:
        """Verify basic cylinder rendering across flat, bordered, and outline styles."""
        # 1. Flat style (with automatic lighter top cap)
        cylinder((30, 50), width=20, height=30, style=Styles.PrimaryFlat)
        assert len(canvas._artists) == 2  # body + top cap

        # 2. Bordered style (body + top cap + outline path)
        clear()
        cylinder((30, 50), width=20, height=30, style=Styles.Primary)
        assert len(canvas._artists) == 3  # body + top cap + outline

        # 3. Outline style (transparent fill)
        clear()
        cylinder((30, 50), width=20, height=30, style=Styles.PrimaryOutline)
        assert len(canvas._artists) == 3

    def test_multi_disk_cylinder(self) -> None:
        """Verify multi-disk cylinder rendering for database visualization."""
        # Flat multi-disk (disks=3: body + top cap + 2 divider crease patches)
        cylinder((30, 50), width=20, height=30, style=Styles.PrimaryFlat, disks=3)
        assert len(canvas._artists) == 4  # 2 base + 2 divider patches

        # Bordered multi-disk (disks=3: body + top cap + outline + 2 divider stroke patches)
        clear()
        cylinder((30, 50), width=20, height=30, style=Styles.Primary, disks=3)
        assert len(canvas._artists) == 5  # 3 base + 2 divider patches

    def test_cylinder_with_text(self) -> None:
        """Verify cylinder with centered embedded text label."""
        cylinder(
            (50, 50),
            width=24,
            height=32,
            style=Styles.PrimaryFlat,
            text="PostgreSQL",
            text_style=Style(text_color=Colors.White, text_size=12, text_font=Font.SANSSERIF_BOLD),
        )
        assert len(canvas._artists) == 3  # 2 shape patches + 1 text artist

    def test_cylinder_rotation(self) -> None:
        """Verify cylinder rendering with rotation angles."""
        # Tilted 45 degrees
        cylinder((50, 50), width=20, height=30, style=Styles.Primary.patch(angle=45.0))
        assert len(canvas._artists) == 3

        # Horizontal cylinder (90 degrees)
        clear()
        cylinder((50, 50), width=20, height=30, style=Styles.PrimaryFlat.patch(angle=90.0))
        assert len(canvas._artists) == 2

    def test_cylinder_alpha_transparency(self) -> None:
        """Verify semi-transparent cylinder styling."""
        style = Styles.PrimaryFlat.patch(alpha=0.4)
        cylinder((50, 50), width=20, height=30, style=style)
        assert len(canvas._artists) == 2

    def test_validation_errors(self) -> None:
        """Verify runtime parameter validation via @validate_call and value checks."""
        # Non-positive width
        with pytest.raises((ValueError, ValidationError)):
            cylinder((50, 50), width=0, height=30, style=Styles.PrimaryFlat)

        with pytest.raises((ValueError, ValidationError)):
            cylinder((50, 50), width=-10, height=30, style=Styles.PrimaryFlat)

        # Non-positive height
        with pytest.raises((ValueError, ValidationError)):
            cylinder((50, 50), width=20, height=0, style=Styles.PrimaryFlat)

        # Invalid disks (< 1)
        with pytest.raises((ValueError, ValidationError)):
            cylinder((50, 50), width=20, height=30, disks=0, style=Styles.PrimaryFlat)

        # Invalid style type
        with pytest.raises((TypeError, ValidationError)):
            cylinder((50, 50), width=20, height=30, style="invalid")  # type: ignore


class TestCanvasCloudAndBrace:
    """Tests for cloud and brace drawing features in CanvasShapeContainerFeature."""

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


class TestCanvasCubeAndDocument:
    """Tests for cube and document drawing features in CanvasShapeContainerFeature."""

    def setup_method(self) -> None:
        """Reset canvas before each test."""
        clear()

    def test_imports_and_availability(self) -> None:
        """Verify cube and document functions are exported and callable."""
        assert callable(cube)
        assert callable(document)
        assert hasattr(canvas, "cube")
        assert hasattr(canvas, "document")

    def test_cube_rendering_and_options(self) -> None:
        """Test cube drawing across depth_ratio, styles, rotation, and embedded text."""
        # Standard cube with outline (3 face fills + 1 unified stroke = 4 artists)
        cube((50, 50), width=24, height=24, style=Styles.PrimaryNeutral)
        assert len(canvas._artists) == 4

        # Flat cube without stroke + embedded text (3 face fills + 1 text = 4 artists)
        clear()
        tstyle = Style(text_color=Colors.White, text_size=11, text_font=Font.SANSSERIF_BOLD)
        cube(
            (50, 50),
            width=30,
            height=20,
            depth_ratio=0.35,
            style=Styles.PrimaryFlat.patch(angle=15.0),
            text="Block",
            text_style=tstyle,
        )
        assert len(canvas._artists) == 4

        # Transparent / wireframe cube
        clear()
        cube(
            (50, 50),
            width=20,
            height=20,
            style=Styles.PrimaryDashed.patch(shape_fill_color=None),
        )
        assert len(canvas._artists) == 4

    def test_cube_validation_errors(self) -> None:
        """Test cube parameter validation errors."""
        with pytest.raises(ValueError, match="width and height must be positive"):
            cube((50, 50), width=0, height=20, style=Styles.Neutral)

        with pytest.raises(ValueError, match="depth_ratio must be strictly between"):
            cube((50, 50), width=20, height=20, depth_ratio=0.0, style=Styles.Neutral)

        with pytest.raises(ValueError, match="depth_ratio must be strictly between"):
            cube((50, 50), width=20, height=20, depth_ratio=1.0, style=Styles.Neutral)

    def test_document_all_variants_and_stacked(self) -> None:
        """Test document across all variants, stacked sheets, ratios, rotation, and text."""
        variants: tuple[DocumentVariant, ...] = (
            "wave",
            "standard",
            "folded",
            "page",
            "note",
            "double_wave",
            "snippet",
            "folded_wave",
            "report",
        )
        for v in variants:
            document((50, 50), width=20, height=24, variant=v, style=Styles.PrimaryNeutral)
        assert len(canvas._artists) > len(variants)

        # Stacked multi-sheet document with custom ratios, rotation, and embedded text
        clear()
        document(
            (50, 50),
            width=24,
            height=28,
            variant="folded_wave",
            stacked=3,
            wave_ratio=0.18,
            fold_ratio=0.22,
            style=Styles.Secondary.patch(angle=-10.0),
            text="Logs (x3)",
        )
        # 3 sheets * (body + flap + stroke) + 1 Text = 10 artists
        assert len(canvas._artists) == 10

        # Flat multi-sheet document without explicit border stroke (auto white separator)
        clear()
        document(
            (50, 50),
            width=22,
            height=26,
            variant="wave",
            stacked=2,
            style=Styles.PrimaryFlat,
        )
        assert len(canvas._artists) == 4

    def test_document_validation_errors(self) -> None:
        """Test document parameter validation errors."""
        with pytest.raises(ValidationError):
            document(
                (50, 50),
                width=20,
                height=24,
                variant=cast(DocumentVariant, "invalid"),
                style=Styles.Neutral,
            )

        with pytest.raises(ValueError, match="width and height must be positive"):
            document((50, 50), width=0, height=24, style=Styles.Neutral)

        with pytest.raises(ValueError, match="stacked must be >= 1"):
            document((50, 50), width=20, height=24, stacked=0, style=Styles.Neutral)

        with pytest.raises(ValueError, match="wave_ratio must be strictly between"):
            document((50, 50), width=20, height=24, wave_ratio=0.0, style=Styles.Neutral)

        with pytest.raises(ValueError, match="fold_ratio must be strictly between"):
            document((50, 50), width=20, height=24, fold_ratio=1.0, style=Styles.Neutral)


class TestCanvasFunnel:
    """Tests for funnel drawing feature in CanvasShapeContainerFeature."""

    def setup_method(self) -> None:
        """Reset canvas before each test."""
        clear()

    def test_funnel_exports_variants_and_validation(self) -> None:
        """Test funnel export, variants, neck ratios, and validation errors."""
        assert callable(funnel)
        assert hasattr(canvas, "funnel")

        for fnv in ("standard", "flat", "3d", "cylinder", "curved"):
            funnel(
                (75, 50),
                width=24,
                height=22,
                variant=fnv,
                neck_width_ratio=0.3,
                neck_height_ratio=0.35,
                style=Styles.SecondaryNeutral.patch(angle=-5),
                text="Filter",
            )
        assert len(canvas._artists) >= 10

        with pytest.raises((ValueError, ValidationError)):
            funnel((50, 50), width=20, height=20, neck_width_ratio=1.0, style=Styles.Primary)
        with pytest.raises((ValueError, ValidationError)):
            funnel((50, 50), width=20, height=20, neck_height_ratio=0.0, style=Styles.Primary)
