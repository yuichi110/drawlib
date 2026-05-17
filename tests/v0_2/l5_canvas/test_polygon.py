# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Unit and integration tests for CanvasOriginalPolygonFeature shapes."""

import pytest

from drawlib.v0_2.apis import (
    Colors,
    ShapeStyle,
    ShapeTextStyle,
    chevron,
    clear,
    parallelogram,
    rhombus,
    save,
    star,
    trapezoid,
    triangle,
)

# ruff: noqa: F403, F405

OUTPUT_DIR = "../../../output_tests/v0_2/l5_canvas/polygon/"


class TestCanvasOriginalPolygon:
    """Tests for the CanvasOriginalPolygonFeature class and custom polygon styles."""

    def test_triangle(self) -> None:
        """Verify triangle drawing with base, height, alignments, styling, top vertex shifts, and angles."""
        clear()

        # Simple triangle
        triangle((50, 50), 30, 40)

        # Style
        triangle(
            (50, 50),
            30,
            40,
            style=ShapeStyle(lcolor=Colors.Red, lwidth=2, lstyle="dashdot", fcolor=Colors.Transparent),
        )

        # Alignments
        triangle((50, 50), 30, 40, style=ShapeStyle(halign="left", valign="bottom"))
        triangle((50, 50), 30, 40, style=ShapeStyle(halign="center", valign="center"))
        triangle((50, 50), 30, 40, style=ShapeStyle(halign="right", valign="top"))

        # Topvertex shifts
        triangle((50, 50), 30, 40, topvertex_x=0)
        triangle((50, 50), 30, 40, topvertex_x=-10)
        triangle((50, 50), 30, 40, topvertex_x=40)

        # Text & angles
        triangle((50, 50), 30, 40, text="Hello")
        triangle((50, 50), 30, 40, angle=45, text="Hello")

        save(f"{OUTPUT_DIR}test_triangle.png")

    def test_parallelogram(self) -> None:
        """Verify parallelogram drawing with dimensions, corner angles, alignments, and text."""
        clear()

        # Simple parallelogram
        parallelogram((50, 50), 30, 20, 60)

        # Alignments
        parallelogram((50, 50), 30, 20, 60, style=ShapeStyle(halign="left", valign="bottom"))
        parallelogram((50, 50), 30, 20, 60, style=ShapeStyle(halign="center", valign="center"))
        parallelogram((50, 50), 30, 20, 60, style=ShapeStyle(halign="right", valign="top"))

        # Text & custom text style
        parallelogram((50, 50), 30, 20, 60, text="hello")
        parallelogram(
            (50, 50),
            30,
            20,
            60,
            text="hello",
            textstyle=ShapeTextStyle(color=Colors.Red),
        )

        # Corner angles
        parallelogram((50, 50), 30, 20, 45)
        parallelogram((50, 50), 30, 20, 75)

        # Rotation angles
        parallelogram((50, 50), 30, 20, 60, angle=45, text="hello", textstyle=ShapeTextStyle(color=Colors.Red))

        save(f"{OUTPUT_DIR}test_parallelogram.png")

    def test_trapezoid(self) -> None:
        """Verify trapezoid drawing with edge widths, topedge offsets, and angles."""
        clear()

        # Simple trapezoid
        trapezoid((50, 50), 30, 40, 20)

        # Style and alignments
        trapezoid(
            (50, 50),
            30,
            40,
            20,
            style=ShapeStyle(lcolor=Colors.Red, fcolor=Colors.Transparent, lwidth=2, lstyle="dashdot"),
        )
        trapezoid((50, 50), 30, 40, 20, style=ShapeStyle(halign="left", valign="bottom"))
        trapezoid((50, 50), 30, 40, 20, style=ShapeStyle(halign="center", valign="center"))

        # Width options
        trapezoid((50, 50), 30, 40, 60, style=ShapeStyle(halign="center", valign="center"))

        # Topedge offset coordinates
        trapezoid((50, 50), 30, 40, 20, topedge_x=0)
        trapezoid((50, 50), 30, 40, 20, topedge_x=5)
        trapezoid((50, 50), 30, 40, 20, topedge_x=-10)

        # Rotations & text
        trapezoid((50, 50), 30, 40, 20, angle=45, text="Hello")

        save(f"{OUTPUT_DIR}test_trapezoid.png")

    def test_rhombus(self) -> None:
        """Verify rhombus drawing with width, height, alignments, and angles."""
        clear()

        # Simple rhombus
        rhombus((50, 50), 20, 40)

        # Style and alignments
        rhombus((50, 50), 20, 40, style=ShapeStyle(lcolor=Colors.Red, fcolor=Colors.Transparent, lwidth=3))
        rhombus((50, 50), 20, 40, style=ShapeStyle(halign="left", valign="bottom"))
        rhombus((50, 50), 20, 40, style=ShapeStyle(halign="center", valign="center"))

        # Text & angles
        rhombus((50, 50), 20, 40, text="hello")
        rhombus((50, 50), 20, 40, angle=45, text="hello")

        save(f"{OUTPUT_DIR}test_rhombus.png")

    def test_chevron(self) -> None:
        """Verify chevron drawing with corner angles, mirroring, and validation."""
        clear()

        # Simple chevron corner angle 60
        chevron(xy=(50, 50), width=10, height=15, corner_angle=60)

        # Alignments
        chevron(xy=(50, 50), width=10, height=15, corner_angle=60, style=ShapeStyle(halign="left", valign="bottom"))
        chevron(xy=(50, 50), width=10, height=15, corner_angle=60, style=ShapeStyle(halign="center", valign="center"))

        # Custom text and styling
        chevron(xy=(50, 50), width=10, height=15, corner_angle=60, text="Hello")
        chevron(
            xy=(50, 50),
            width=10,
            height=15,
            corner_angle=60,
            style=ShapeStyle(lcolor=Colors.Yellow, fcolor=Colors.Blue, lwidth=3),
        )
        chevron(
            xy=(50, 50),
            width=10,
            height=15,
            corner_angle=60,
            text="hello",
            textstyle=ShapeTextStyle(color=Colors.Red, size=28),
        )

        # Mirroring and angles
        chevron(xy=(50, 50), width=10, height=15, corner_angle=60, mirror=True)
        chevron(xy=(50, 50), width=10, height=15, corner_angle=60, angle=45, text="chevron")

        # Corner angle 30
        chevron(xy=(50, 50), width=10, height=15, corner_angle=30)

        save(f"{OUTPUT_DIR}test_chevron.png")

    def test_chevron_invalid_corner_angle(self) -> None:
        """Verify that invalid chevron corner angles raise ValueError."""
        clear()
        with pytest.raises(ValueError):
            chevron(xy=(50, 50), width=10, height=15, corner_angle=120)

    def test_star(self) -> None:
        """Verify star drawing with vertices, outer/inner radii, and alignments."""
        clear()

        # Vertices counts
        star((50, 50), 3, 30, 5, text="Hello")
        star((50, 50), 4, 30, 15, text="Hello")
        star((50, 50), 5, 30, 15, text="Hello")
        star((50, 50), 8, 30, 15, text="Hello")

        # Alignments
        star((50, 50), 5, 30, 15, style=ShapeStyle(halign="left", valign="bottom"), text="Hello")
        star((50, 50), 5, 30, 15, style=ShapeStyle(halign="center", valign="center"), text="Hello")

        # Custom styling & angles
        star(
            (50, 50),
            5,
            30,
            15,
            style=ShapeStyle(lcolor=Colors.Red, lstyle="dashdot", lwidth=2, fcolor=Colors.Transparent),
        )
        star((50, 50), 5, 30, 15, angle=45, text="Hello")

        save(f"{OUTPUT_DIR}test_star.png")
