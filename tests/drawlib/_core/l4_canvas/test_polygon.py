# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Unit and integration tests for CanvasShapePolygonFeature shapes."""

import pytest

from drawlib.canvas import clear, save
from drawlib.shapes import (
    arrow_l,
    arrow_polyline,
    arrow_u,
    chevron,
    circle,
    ellipse,
    parallelogram,
    polygon,
    rectangle,
    regularpolygon,
    rhombus,
    star,
    trapezoid,
    triangle,
)
from drawlib.styles import Colors, Styles

# ruff: noqa: F403, F405

default_styles = Styles
OUTPUT_DIR = "../../../../output_tests/_core/l4_canvas/polygon/"


class TestCanvasPolygon:
    """Tests for the CanvasShapePolygonFeature class and custom polygon styles."""

    def test_triangle(self) -> None:
        """Verify triangle drawing with base, height, alignments, styling, top vertex shifts, and angles."""
        clear()
        styles = default_styles
        s_primary = styles.Primary
        s_white = styles.White.patch(shape_line_color=Colors.Black, shape_line_width=1.0)

        # Simple triangle
        triangle((50, 50), 30, 40, style=s_primary)

        # Style
        triangle(
            (50, 50),
            30,
            40,
            style=s_white.patch(
                shape_line_color=Colors.Red,
                shape_line_width=2,
                shape_line_style="dashdot",
                shape_fill_color=Colors.Transparent,
            ),
        )

        # Alignments
        triangle((50, 50), 30, 40, style=s_white.patch(halign="left", valign="bottom"))
        triangle((50, 50), 30, 40, style=s_white.patch(halign="center", valign="center"))
        triangle((50, 50), 30, 40, style=s_white.patch(halign="right", valign="top"))

        # Topvertex shifts
        triangle((50, 50), 30, 40, topvertex_x=0, style=s_primary)
        triangle((50, 50), 30, 40, topvertex_x=-10, style=s_primary)
        triangle((50, 50), 30, 40, topvertex_x=40, style=s_primary)

        # Text & angles
        triangle((50, 50), 30, 40, text="Hello", style=s_primary)
        triangle((50, 50), 30, 40, text="Hello", style=s_primary.patch(angle=45))

        save(f"{OUTPUT_DIR}test_triangle.png")

    def test_parallelogram(self) -> None:
        """Verify parallelogram drawing with dimensions, corner angles, alignments, and text."""
        clear()
        styles = default_styles
        s_primary = styles.Primary
        s_white = styles.White.patch(shape_line_color=Colors.Black, shape_line_width=1.0)
        s_red_text = s_primary.patch(text_color=Colors.Red)

        # Simple parallelogram
        parallelogram((50, 50), 30, 20, 60, style=s_primary)

        # Alignments
        parallelogram((50, 50), 30, 20, 60, style=s_white.patch(halign="left", valign="bottom"))
        parallelogram((50, 50), 30, 20, 60, style=s_white.patch(halign="center", valign="center"))
        parallelogram((50, 50), 30, 20, 60, style=s_white.patch(halign="right", valign="top"))

        # Text & custom text style
        parallelogram((50, 50), 30, 20, 60, text="hello", style=s_primary)
        parallelogram(
            (50, 50),
            30,
            20,
            60,
            text="hello",
            style=s_primary,
            text_style=s_red_text,
        )

        # Corner angles
        parallelogram((50, 50), 30, 20, 45, style=s_primary)
        parallelogram((50, 50), 30, 20, 75, style=s_primary)

        # Rotation angles
        parallelogram((50, 50), 30, 20, 60, text="hello", style=s_primary.patch(angle=45), text_style=s_red_text)

        save(f"{OUTPUT_DIR}test_parallelogram.png")

    def test_trapezoid(self) -> None:
        """Verify trapezoid drawing with edge widths, topedge offsets, and angles."""
        clear()
        styles = default_styles
        s_primary = styles.Primary
        s_white = styles.White.patch(shape_line_color=Colors.Black, shape_line_width=1.0)

        # Simple trapezoid
        trapezoid((50, 50), 30, 40, 20, style=s_primary)

        # Style and alignments
        trapezoid(
            (50, 50),
            30,
            40,
            20,
            style=s_white.patch(
                shape_line_color=Colors.Red,
                shape_fill_color=Colors.Transparent,
                shape_line_width=2,
                shape_line_style="dashdot",
            ),
        )
        trapezoid((50, 50), 30, 40, 20, style=s_white.patch(halign="left", valign="bottom"))
        trapezoid((50, 50), 30, 40, 20, style=s_white.patch(halign="center", valign="center"))

        # Width options
        trapezoid((50, 50), 30, 40, 60, style=s_white.patch(halign="center", valign="center"))

        # Topedge offset coordinates
        trapezoid((50, 50), 30, 40, 20, topedge_x=0, style=s_primary)
        trapezoid((50, 50), 30, 40, 20, topedge_x=5, style=s_primary)
        trapezoid((50, 50), 30, 40, 20, topedge_x=-10, style=s_primary)

        # Rotations & text
        trapezoid((50, 50), 30, 40, 20, text="Hello", style=s_primary.patch(angle=45))

        save(f"{OUTPUT_DIR}test_trapezoid.png")

    def test_rhombus(self) -> None:
        """Verify rhombus drawing with width, height, alignments, and angles."""
        clear()
        styles = default_styles
        s_primary = styles.Primary
        s_white = styles.White.patch(shape_line_color=Colors.Black, shape_line_width=1.0)

        # Simple rhombus
        rhombus((50, 50), 20, 40, style=s_primary)

        # Style and alignments
        rhombus(
            (50, 50),
            20,
            40,
            style=s_white.patch(
                shape_line_color=Colors.Red,
                shape_fill_color=Colors.Transparent,
                shape_line_width=3,
            ),
        )
        rhombus((50, 50), 20, 40, style=s_white.patch(halign="left", valign="bottom"))
        rhombus((50, 50), 20, 40, style=s_white.patch(halign="center", valign="center"))

        # Text & angles
        rhombus((50, 50), 20, 40, text="hello", style=s_primary)
        rhombus((50, 50), 20, 40, text="hello", style=s_primary.patch(angle=45))

        save(f"{OUTPUT_DIR}test_rhombus.png")

    def test_chevron(self) -> None:
        """Verify chevron drawing with corner angles, mirroring, and validation."""
        clear()
        styles = default_styles
        s_primary = styles.Primary
        s_white = styles.White.patch(shape_line_color=Colors.Black, shape_line_width=1.0)

        # Simple chevron corner angle 60
        chevron(xy=(50, 50), width=10, height=15, corner_angle=60, style=s_primary)

        # Alignments
        chevron(
            xy=(50, 50),
            width=10,
            height=15,
            corner_angle=60,
            style=s_white.patch(halign="left", valign="bottom"),
        )
        chevron(
            xy=(50, 50),
            width=10,
            height=15,
            corner_angle=60,
            style=s_white.patch(halign="center", valign="center"),
        )

        # Custom text and styling
        chevron(xy=(50, 50), width=10, height=15, corner_angle=60, text="Hello", style=s_primary)
        chevron(
            xy=(50, 50),
            width=10,
            height=15,
            corner_angle=60,
            style=s_white.patch(shape_line_color=Colors.Yellow, shape_fill_color=Colors.Blue, shape_line_width=3),
        )
        chevron(
            xy=(50, 50),
            width=10,
            height=15,
            corner_angle=60,
            text="hello",
            style=s_primary,
            text_style=s_primary.patch(text_color=Colors.Red, text_size=28),
        )

        # Mirroring and angles
        chevron(xy=(50, 50), width=10, height=15, corner_angle=60, mirror=True, style=s_primary)
        chevron(xy=(50, 50), width=10, height=15, corner_angle=60, text="chevron", style=s_primary.patch(angle=45))

        # Corner angle 30
        chevron(xy=(50, 50), width=10, height=15, corner_angle=30, style=s_primary)

        save(f"{OUTPUT_DIR}test_chevron.png")

    def test_chevron_invalid_corner_angle(self) -> None:
        """Verify that invalid chevron corner angles raise ValueError."""
        clear()
        styles = default_styles
        with pytest.raises(ValueError):
            chevron(xy=(50, 50), width=10, height=15, corner_angle=120, style=styles.Primary)

    def test_star(self) -> None:
        """Verify star drawing with vertices, outer/inner radii, and alignments."""
        clear()
        styles = default_styles
        s_primary = styles.Primary
        s_white = styles.White.patch(shape_line_color=Colors.Black, shape_line_width=1.0)

        # Vertices counts
        star((50, 50), 3, 30, 5, text="Hello", style=s_primary)
        star((50, 50), 4, 30, 15, text="Hello", style=s_primary)
        star((50, 50), 5, 30, 15, text="Hello", style=s_primary)
        star((50, 50), 8, 30, 15, text="Hello", style=s_primary)

        # Alignments
        star((50, 50), 5, 30, 15, style=s_white.patch(halign="left", valign="bottom"), text="Hello")
        star((50, 50), 5, 30, 15, style=s_white.patch(halign="center", valign="center"), text="Hello")

        # Custom styling & angles
        star(
            (50, 50),
            5,
            30,
            15,
            style=s_white.patch(
                shape_line_color=Colors.Red,
                shape_line_style="dashdot",
                shape_line_width=2,
                shape_fill_color=Colors.Transparent,
            ),
        )
        star((50, 50), 5, 30, 15, text="Hello", style=s_primary.patch(angle=45))

        save(f"{OUTPUT_DIR}test_star.png")

    def test_shape_r_scalar_and_tuple(self) -> None:
        """Verify Style.shape_r scalar and per-vertex tuple on polygons and ignore on circles."""
        clear()
        s = default_styles.Primary

        # Scalar and tuple shape_r on polygon primitives
        triangle((20, 20), 20, 20, style=s.patch(shape_r=2.0))
        triangle((20, 20), 20, 20, style=s.patch(shape_r=(0.0, 3.0, 0.0)))
        rectangle((50, 20), 20, 15, style=s.patch(shape_r=(0.0, 2.0, 2.0, 0.0)))
        parallelogram((80, 20), 20, 15, 60, style=s.patch(shape_r=(1.0, 2.0, 1.0, 2.0)))
        trapezoid((20, 50), 15, 25, 15, style=s.patch(shape_r=(1.0, 2.0, 2.0, 1.0)))
        rhombus((50, 50), 20, 20, style=s.patch(shape_r=(1.0, 2.0, 1.0, 2.0)))
        chevron((80, 50), 15, 15, 60, style=s.patch(shape_r=(1.0, 1.0, 1.0, 1.0, 1.0, 1.0)))
        regularpolygon((20, 80), radius=10, num_vertex=5, style=s.patch(shape_r=1.5))
        regularpolygon((20, 80), radius=10, num_vertex=5, style=s.patch(shape_r=(1.0, 2.0, 1.0, 2.0, 1.0)))
        star((50, 80), 4, 12, 6, style=s.patch(shape_r=1.0))
        polygon([(70, 70), (90, 70), (90, 90), (80, 95), (70, 90)], style=s.patch(shape_r=(0.0, 0.0, 2.0, 3.0, 2.0)))

        # Circular shapes ignore shape_r without raising errors
        circle((50, 50), radius=10, style=s.patch(shape_r=5.0))
        ellipse((50, 50), width=20, height=10, style=s.patch(shape_r=(1.0, 2.0, 3.0)))

    def test_shape_r_invalid_tuple_length(self) -> None:
        """Verify that mismatched shape_r tuple length raises ValueError."""
        clear()
        s = default_styles.Primary

        with pytest.raises(ValueError, match="shape_r tuple length"):
            triangle((50, 50), 20, 20, style=s.patch(shape_r=(1.0, 2.0, 3.0, 4.0)))

        with pytest.raises(ValueError, match="shape_r tuple length"):
            rectangle((50, 50), 20, 20, style=s.patch(shape_r=(1.0, 2.0, 3.0)))

        with pytest.raises(ValueError, match="shape_r tuple length"):
            chevron((50, 50), 20, 20, 60, style=s.patch(shape_r=(1.0, 2.0, 3.0, 4.0)))

        with pytest.raises(ValueError, match="shape_r tuple length"):
            regularpolygon((50, 50), radius=10, num_vertex=5, style=s.patch(shape_r=(1.0, 2.0, 3.0, 4.0)))

        with pytest.raises(ValueError, match="shape_r tuple length"):
            star((50, 50), 5, 20, 10, style=s.patch(shape_r=(1.0, 2.0, 3.0, 4.0, 5.0)))

        with pytest.raises(ValueError, match="shape_r tuple length"):
            arrow_l((50, 50), 20, 15, 2, 5, 3, style=s.patch(shape_r=(1.0, 2.0)))

        with pytest.raises(ValueError, match="shape_r tuple length"):
            arrow_u((50, 50), 20, 15, 2, 5, 3, style=s.patch(shape_r=(1.0, 2.0, 3.0)))

        with pytest.raises(ValueError, match="shape_r tuple length"):
            arrow_polyline([(10, 10), (10, 30), (30, 30), (30, 10)], 2, 5, 3, style=s.patch(shape_r=(1.0, 2.0, 3.0)))
