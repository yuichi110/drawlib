# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Unit and integration tests for CanvasPatchesFeature shapes."""

import pytest

from drawlib.canvas import clear, save
from drawlib.colors import Colors
from drawlib.fonts import Font
from drawlib.preset_styles import get_default_styles, get_styles
from drawlib.shapes import arc, circle, donuts, ellipse, fan, regularpolygon, wedge
from drawlib.types import Style

# ruff: noqa: F403, F405

OUTPUT_DIR = "../../output_tests/l4_canvas/patches/"


class TestCanvasPatches:
    """Tests for the CanvasPatchesFeature class and basic matplotlib patch shapes."""

    def test_arc(self) -> None:
        """Verify arc drawing with dimensions, angles, alignments, and text."""
        clear()
        styles = get_default_styles()
        s_def = styles.white.patch(shape_line_color=Colors.Black, shape_line_width=1.0)

        # Simple arc
        arc((50, 50), 30, 50, style=s_def)

        # Alignments and text
        arc((50, 50), 30, 50, style=s_def.patch(text_halign="left", text_valign="bottom"), text="Hello")
        arc((50, 50), 30, 50, style=s_def.patch(text_halign="center", text_valign="center"), text="Hello")
        arc((50, 50), 30, 50, style=s_def.patch(text_halign="right", text_valign="top"), text="Hello")

        # Custom styling
        arc(
            (50, 50),
            30,
            50,
            style=s_def.patch(
                shape_line_color=Colors.Red,
                shape_line_width=5,
                shape_line_style="dashdot",
                shape_fill_color=Colors.Blue,
            ),
        )

        # Theta spans & angles
        arc((50, 50), 30, 50, angle=45, text="Hello", style=s_def)
        arc((50, 50), 30, 50, angle=45, angle_start=90, angle_end=270, style=s_def)

        save(f"{OUTPUT_DIR}test_arc.png")

    def test_circle(self) -> None:
        """Verify circle drawing with radius, alignments, custom styles, and preset styles."""
        clear()
        styles = get_default_styles()
        s_def = styles.white.patch(shape_line_color=Colors.Black, shape_line_width=1.0)
        styles_essentials = get_styles("essentials")

        # Simple circle
        circle(xy=(50, 50), radius=30, style=s_def)

        # Alignments and text
        circle(
            xy=(50, 50),
            radius=30,
            style=s_def.patch(text_halign="left", text_valign="bottom"),
            text="Hello",
            angle=45,
        )
        circle(
            xy=(50, 50),
            radius=30,
            style=s_def.patch(text_halign="center", text_valign="center"),
            text="Hello",
            angle=45,
        )
        circle(
            xy=(50, 50),
            radius=30,
            style=s_def.patch(text_halign="right", text_valign="top"),
            text="Hello",
            angle=45,
        )

        # Custom line style
        circle(
            xy=(50, 50),
            radius=30,
            style=s_def.patch(
                shape_line_color=Colors.Red,
                shape_line_width=5,
                shape_line_style="dashdot",
                shape_fill_color=Colors.Blue,
                shape_fill_alpha=0.7,
            ),
        )

        # Preset styles
        circle(xy=(25, 25), radius=20, style=styles_essentials.blue)
        circle(xy=(25, 75), radius=20, style=styles_essentials.green)

        save(f"{OUTPUT_DIR}test_circle.png")

    def test_ellipse(self) -> None:
        """Verify ellipse drawing with dimensions, alignments, styles, and angles."""
        clear()
        styles = get_default_styles()
        s_primary = styles.primary
        s_white = styles.white.patch(shape_line_color=Colors.Black, shape_line_width=1.0)

        # Simple ellipse
        ellipse(xy=(50, 50), width=40, height=20, style=s_primary)

        # Custom styling
        ellipse(
            xy=(50, 50),
            width=40,
            height=20,
            style=s_white.patch(shape_line_width=3, shape_line_color=Colors.Red, shape_line_style="dashdot"),
        )

        # Alignments and text
        ellipse(
            xy=(50, 50),
            width=40,
            height=20,
            style=s_white.patch(text_halign="left", text_valign="bottom"),
            text="Hello",
        )
        ellipse(
            xy=(50, 50),
            width=40,
            height=20,
            style=s_white.patch(text_halign="center", text_valign="center"),
            text="Hello",
        )
        ellipse(
            xy=(50, 50),
            width=40,
            height=20,
            style=s_white.patch(text_halign="right", text_valign="top"),
            text="Hello",
        )

        # Orientation angle
        ellipse(xy=(50, 50), width=40, height=20, angle=45, text="Hello", style=s_primary)

        save(f"{OUTPUT_DIR}test_ellipse.png")

    def test_regularpolygon(self) -> None:
        """Verify regular polygon vertices counts, styles, and alignments."""
        clear()
        styles = get_default_styles()
        s_primary = styles.primary
        s_white = styles.white.patch(shape_line_color=Colors.Black, shape_line_width=1.0)

        # Vertices counts
        regularpolygon(xy=(50, 50), radius=30, num_vertex=5, text="Hello", style=s_primary)
        regularpolygon(xy=(50, 50), radius=30, num_vertex=6, text="Hello", style=s_primary)
        regularpolygon(xy=(50, 50), radius=30, num_vertex=8, text="Hello", style=s_primary)

        # Custom style
        regularpolygon(
            xy=(50, 50),
            radius=30,
            num_vertex=5,
            style=s_white.patch(
                shape_line_width=3,
                shape_line_color=Colors.Red,
                shape_line_style="dashdot",
                shape_fill_color=Colors.Green,
            ),
        )

        # Alignments
        regularpolygon(
            xy=(50, 50),
            radius=30,
            num_vertex=8,
            text="Hello",
            style=s_white.patch(text_halign="left", text_valign="bottom"),
        )
        regularpolygon(
            xy=(50, 50),
            radius=30,
            num_vertex=8,
            text="Hello",
            style=s_white.patch(text_halign="center", text_valign="center"),
        )

        # Angle orientation
        regularpolygon(xy=(50, 50), radius=30, num_vertex=5, angle=45, text="Hello", style=s_primary)

        save(f"{OUTPUT_DIR}test_regularpolygon.png")

    def test_wedge(self) -> None:
        """Verify wedge segment drawing with radii, spans, styles, and alignments."""
        clear()
        styles = get_default_styles()
        s_primary = styles.primary
        s_white = styles.white.patch(shape_line_color=Colors.Black, shape_line_width=1.0)

        # Simple wedge
        wedge((50, 50), radius=30, width=10, text="Hello", style=s_primary)

        # Custom style
        wedge(
            (50, 50),
            radius=30,
            width=10,
            style=s_white.patch(
                shape_line_width=3,
                shape_line_color=Colors.Red,
                shape_line_style="dashdot",
                shape_fill_color=Colors.Green,
            ),
            text="Hello",
        )

        # Alignments
        wedge(
            (50, 50),
            radius=30,
            width=10,
            style=s_white.patch(text_halign="left", text_valign="bottom"),
            text="Hello",
        )
        wedge(
            (50, 50),
            radius=30,
            width=10,
            style=s_white.patch(text_halign="center", text_valign="center"),
            text="Hello",
        )

        # Angle spans
        wedge(
            (50, 50),
            radius=30,
            angle_start=45,
            angle_end=270,
            width=10,
            angle=120,
            text="Hello",
            style=s_primary,
        )

        save(f"{OUTPUT_DIR}test_wedge.png")

    def test_donuts(self) -> None:
        """Verify donut shape drawing with outer radius, width, styling, and text."""
        clear()
        styles = get_default_styles()
        s_primary = styles.primary
        s_white = styles.white.patch(shape_line_color=Colors.Black, shape_line_width=1.0)

        # Simple donut
        donuts((50, 50), radius=30, width=10, style=s_primary)

        # Styled donuts
        donuts(
            (50, 50),
            radius=30,
            width=10,
            style=s_white.patch(
                shape_line_width=3,
                shape_line_color=Colors.Red,
                shape_line_style="dashdot",
                shape_fill_color=Colors.Green,
            ),
            text="Hello",
        )

        # Alignments
        donuts(
            (50, 50),
            radius=30,
            width=10,
            style=s_white.patch(text_halign="left", text_valign="bottom"),
            text="Hello",
        )
        donuts(
            (50, 50),
            radius=30,
            width=10,
            style=s_white.patch(text_halign="center", text_valign="center"),
            text="Hello",
        )

        # Rotation angle
        donuts((50, 50), radius=30, width=10, angle=120, text="hungry", style=s_primary)

        save(f"{OUTPUT_DIR}test_donuts.png")

    def test_fan(self) -> None:
        """Verify fan sector drawing with radius, theta boundaries, styling, and text."""
        clear()
        styles = get_default_styles()
        s_primary = styles.primary
        s_white = styles.white.patch(shape_line_color=Colors.Black, shape_line_width=1.0)

        # Simple fan
        fan((50, 50), radius=30, angle_start=45, angle_end=90, style=s_primary)

        # Custom style
        fan(
            (50, 50),
            radius=30,
            angle_start=45,
            angle_end=90,
            style=s_white.patch(
                shape_line_width=3,
                shape_line_color=Colors.Red,
                shape_line_style="dashdot",
                shape_fill_color=Colors.Green,
            ),
            text="Hello",
        )

        # Alignments
        fan(
            (50, 50),
            radius=30,
            angle_start=45,
            angle_end=90,
            style=s_white.patch(text_halign="left", text_valign="bottom"),
            text="Hello",
        )
        fan(
            (50, 50),
            radius=30,
            angle_start=45,
            angle_end=90,
            style=s_white.patch(text_halign="center", text_valign="center"),
            text="Hello",
        )

        # Rotation angles
        fan((50, 50), radius=30, angle_start=45, angle_end=270, angle=120, text="Hello", style=s_primary)

        save(f"{OUTPUT_DIR}test_fan.png")
