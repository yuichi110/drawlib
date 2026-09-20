# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Unit and integration tests for CanvasBase core functionality."""

import os

import pytest

from drawlib._core.l4_canvas import (
    canvas,
    get_charwidth_from_fontsize,
    get_fontsize_from_charwidth,
    get_image_zoom_from_width,
    get_image_zoom_original,
)
from drawlib._core.l4_canvas._base import CanvasBase
from drawlib.canvas import clear, config, save
from drawlib.colors import (
    Colors,
    Colors140,
)
from drawlib.shapes import polygon, rectangle, shape
from drawlib.types import (
    Style,
)

# ruff: noqa: F403, F405

OUTPUT_DIR = "../../output_tests/l4_canvas/base/"


class TestCanvasBase:
    """Tests for the CanvasBase class and its core drawing/utility methods."""

    def test_init(self) -> None:
        """Verify that CanvasBase initializes with correct default values."""
        base = CanvasBase()
        assert base.DEFAULT_WIDTH == 100
        assert base.DEFAULT_HEIGHT == 100
        assert base.DEFAULT_DPI == 100
        assert base._width == 100
        assert base._height == 100
        assert base._dpi == 100
        assert base._grid is False
        assert len(base._artists) == 0

    def test_clear(self) -> None:
        """Verify that clear() resets state and configuration of the canvas."""
        clear()
        config(width=200, height=150, dpi=150)
        assert canvas._width == 200
        assert canvas._height == 150
        assert canvas._dpi == 150

        clear()
        assert canvas._width == 100
        assert canvas._height == 100
        assert canvas._dpi == 100

    def test_config(self) -> None:
        """Verify config() configures canvas parameters correctly."""
        clear()
        config(
            width=150,
            height=120,
            dpi=120,
            background_color=Colors140.Orange,
            background_alpha=0.5,
            grid=True,
            grid_style=Style(line_width=2, text_color=Colors.Red),
        )
        assert canvas._width == 150
        assert canvas._height == 120
        assert canvas._dpi == 120
        assert canvas._background_color == Colors140.Orange
        assert canvas._background_alpha == 0.5
        assert canvas._grid is True
        assert canvas._grid_style.line_width == 2
        assert canvas._grid_style.text_color == Colors.Red

    def test_polygon(self) -> None:
        """Verify drawing a basic polygon with different styles and text."""
        clear()
        # No style
        polygon(xys=[(10, 10), (10, 50), (80, 30)])

        # With alignment and style
        polygon(
            xys=[(10, 10), (10, 50), (80, 30)],
            style=Style(text_halign="center", text_valign="center"),
        )

        # Custom line style
        polygon(
            xys=[(10, 10), (10, 50), (80, 30)],
            style=Style(line_width=3, line_color=Colors.Red, line_style="dashdot", fill_color=Colors.Green),
        )

        # With text
        polygon(xys=[(10, 10), (10, 50), (80, 30)], text="Hello Drawlib!!")

        save(f"{OUTPUT_DIR}test_polygon.png")

    def test_shape(self) -> None:
        """Verify drawing a generic shape with various path points and styles."""
        clear()
        # Draw shape with line points
        shape(
            xy=(50, 50),
            path_points=[(0, 0), (10, 0), (10, 10), (0, 10)],
            style=Style(fill_color=Colors.Blue),
            text="Shape",
        )
        save(f"{OUTPUT_DIR}test_shape.png")

    def test_rectangle(self) -> None:
        """Verify rectangle drawing with regular corners, rounded corners, alignments, and text."""
        clear()
        # Default
        rectangle((50, 50), 40, 20, text="Rectangle")

        # Alignment options
        rectangle((50, 50), 40, 20, text="Rectangle", style=Style(text_halign="left", text_valign="bottom"))
        rectangle((50, 50), 40, 20, text="Rectangle", style=Style(text_halign="center", text_valign="center"))
        rectangle((50, 50), 40, 20, text="Rectangle", style=Style(text_halign="right", text_valign="top"))

        # Different angles
        rectangle((50, 50), 40, 20, angle=45, text="Rectangle")
        rectangle((50, 50), 40, 20, angle=90, text="Rectangle")

        # Text shift options
        rectangle(
            (50, 50),
            40,
            20,
            angle=135,
            text="Rectangle",
            textstyle=Style(text_xy_shift=(10, 5), text_flip=True, text_color=Colors.Red),
        )
        rectangle(
            (50, 50),
            40,
            20,
            angle=135,
            text="Rectangle",
            textstyle=Style(text_xy_abs_shift=(10, 5), text_flip=True, text_color=Colors.Red),
        )

        # Style & rounded corner (r > 0)
        rectangle(
            (50, 50),
            40,
            20,
            r=3.0,
            angle=45,
            text="Rectangle",
            style=Style(
                line_color=Colors.Blue,
                fill_color=Colors.Yellow,
                fill_alpha=0.5,
                line_style="dashed",
                line_width=3,
            ),
        )

        # Textsize override
        rectangle(
            (50, 50),
            40,
            20,
            text="Rectangle",
            textsize=36,
        )

        save(f"{OUTPUT_DIR}test_rectangle.png")

    def test_image_zoom(self) -> None:
        """Verify image zoom calculation utilities."""
        clear()
        config(dpi=100)
        zoom = get_image_zoom_original()
        assert abs(zoom - 0.72) < 1e-5

        # Check font sizes
        assert get_charwidth_from_fontsize(12) > 0
        assert get_fontsize_from_charwidth(2) > 0
