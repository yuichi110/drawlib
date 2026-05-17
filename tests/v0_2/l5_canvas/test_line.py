# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Unit and integration tests for CanvasLineFeature lines."""

import pytest

from drawlib.v0_2.apis import (
    Colors,
    LineStyle,
    circle,
    clear,
    ellipse,
    line,
    line_arc,
    line_bezier1,
    line_bezier2,
    line_curved,
    lines,
    lines_bezier,
    lines_curved,
    save,
)
from drawlib.v0_2.private.l5_canvas._line import LineArcHelper

# ruff: noqa: F403, F405

OUTPUT_DIR = "../../../output_tests/v0_2/l5_canvas/line/"


class TestCanvasLine:
    """Tests for the CanvasLineFeature class and various line rendering modes."""

    def test_line(self) -> None:
        """Verify standard straight line drawing and custom style overrides."""
        clear()

        # Simple straight line
        line((10, 10), (90, 90))

        # With line styling
        style = LineStyle(width=3, color=Colors.Red, style="dashdot", alpha=0.5)
        line((20, 80), (80, 20), style=style)

        # Arrowheads and arrow fill
        line((20, 20), (80, 80), arrowhead="->")
        line((20, 80), (80, 20), arrowhead="<->", style=LineStyle(color=Colors.Red, ahfill=True))

        # Themes
        line((10, 10), (90, 90), style="green")
        line((10, 90), (90, 10), arrowhead="->", style="red")

        # Width options
        for y, w in [(10, 2), (20, 4), (30, 8), (40, 1), (50, 0.5)]:
            line((10, y), (90, y), width=w)

        save(f"{OUTPUT_DIR}test_line.png")

    def test_line_curved(self) -> None:
        """Verify curved line drawing with bend and arrowheads."""
        clear()

        line_curved(
            (20, 20),
            (80, 80),
            bend=-0.5,
            arrowhead="->",
        )

        line_curved(
            (20, 80),
            (80, 20),
            bend=-0.5,
            style=LineStyle(style="dashed", width=2, color=Colors.Red),
        )

        # Theme line curved
        line_curved(
            (20, 20),
            (80, 80),
            bend=-0.5,
            style="green",
        )

        save(f"{OUTPUT_DIR}test_line_curved.png")

    def test_line_bezier(self) -> None:
        """Verify quadratic and cubic Bezier line drawing."""
        clear()

        style = LineStyle(width=3, color=Colors.Red, style="dotted", alpha=1)
        line_bezier1((20, 20), (50, 50), (80, 20), style=style)
        line_bezier2((20, 20), (20, 50), (80, 50), (80, 20), style=style)

        save(f"{OUTPUT_DIR}test_line_bezier.png")

    def test_line_arc(self) -> None:
        """Verify elliptical and circular arc drawing with angles and arrowheads."""
        clear()

        # On Circle
        line_arc(xy=(25, 25), width=20, height=20, angle_start=45, angle_end=135, arrowhead="->")
        line_arc(xy=(25, 75), width=20, height=20, angle_start=10, angle_end=190, arrowhead="->")
        line_arc(xy=(75, 25), width=20, height=20, angle_start=270, angle_end=135, arrowhead="->")
        line_arc(xy=(75, 75), width=20, height=20, angle_start=0, angle_end=360, arrowhead="->")

        # On Ellipse
        line_arc(xy=(25, 25), width=30, height=15, angle_start=45, angle_end=135, arrowhead="->")
        line_arc(xy=(25, 75), width=30, height=15, angle_start=10, angle_end=190, arrowhead="->")

        # Ellipse with rotated orientation angle
        line_arc(xy=(25, 25), width=30, height=15, angle_start=45, angle_end=135, arrowhead="->", angle=45)

        save(f"{OUTPUT_DIR}test_line_arc.png")

    def test_ellipse_calculations(self) -> None:
        """Verify underlying ellipse arc mathematical approximations."""
        clear()

        ellipse((50, 50), 30, 30, style="dashed")
        a, b, c, d = LineArcHelper.bezier_ellipse_arc_approximation((50, 50), 30, 30, 45, -45)
        circle(a, 1, style="black")
        circle(b, 1, style="red")
        circle(c, 1, style="green")
        circle(d, 1, style="blue")

        # Get ellipse path points calculation
        path_points = LineArcHelper.get_ellipse_path_points((50, 50), 30, 30, 180, 45)
        assert len(path_points) > 0
        save(f"{OUTPUT_DIR}test_ellipse_calculations.png")

    def test_lines(self) -> None:
        """Verify drawing multiple consecutive connected straight lines."""
        clear()
        lines(xys=[(20, 20), (40, 80), (70, 30)])
        save(f"{OUTPUT_DIR}test_lines.png")

    def test_lines_curved(self) -> None:
        """Verify drawing curved line connections along consecutive points."""
        clear()
        lines_curved(xys=[(20, 20), (40, 80), (70, 30), (90, 50)], r=5)
        save(f"{OUTPUT_DIR}test_lines_curved.png")

    def test_lines_bezier(self) -> None:
        """Verify drawing multi-point Bezier structures via lines_bezier."""
        clear()
        points = [
            ((10, 20), (20, 20)),
            (30, 20),
            ((40, 20), (40, 10)),
            ((40, 20), (50, 20)),
        ]
        lines_bezier(xy=(0, 30), path_points=points)  # type: ignore
        save(f"{OUTPUT_DIR}test_lines_bezier.png")
