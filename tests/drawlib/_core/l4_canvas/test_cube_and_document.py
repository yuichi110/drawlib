# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Unit and integration tests for Canvas cube and document shapes in drawlib.shapes."""

from typing import cast

import pytest
from pydantic import ValidationError

from drawlib._core.l2_types import DocumentVariant
from drawlib.canvas import canvas, clear
from drawlib.fonts import Font
from drawlib.shapes import cube, document
from drawlib.styles import Colors, Style, Styles


class TestCanvasCubeAndDocument:
    """Tests for cube and document drawing features in CanvasShapeBasicFeature."""

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
