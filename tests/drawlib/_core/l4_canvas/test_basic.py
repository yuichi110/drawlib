# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Unit and integration tests for CanvasShapeBasicFeature shapes."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from drawlib.canvas import canvas, clear, save
from drawlib.shapes import arc, circle, ellipse, fan, rectangle, regularpolygon, wedge
from drawlib.styles import Colors, Styles

default_styles = Styles
OUTPUT_DIR = "../../../../output_tests/_core/l4_canvas/basic/"


class TestCanvasBasic:
    """Tests for the CanvasShapeBasicFeature class and basic patch shapes."""

    def test_arc(self) -> None:
        """Verify arc drawing with dimensions, angles, alignments, and text."""
        clear()
        styles = default_styles
        s_def = styles.White.patch(shape_line_color=Colors.Black, shape_line_width=1.0)

        # Simple arc
        arc((50, 50), 30, 50, style=s_def)

        # Alignments and text
        arc((50, 50), 30, 50, style=s_def.patch(halign="left", valign="bottom"), text="Hello")
        arc((50, 50), 30, 50, style=s_def.patch(halign="center", valign="center"), text="Hello")
        arc((50, 50), 30, 50, style=s_def.patch(halign="right", valign="top"), text="Hello")

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
        arc((50, 50), 30, 50, text="Hello", style=s_def.patch(angle=45))
        arc((50, 50), 30, 50, angle_start=90, angle_end=270, style=s_def.patch(angle=45))

        save(f"{OUTPUT_DIR}test_arc.png")

    @pytest.mark.image_threshold(98.5)
    def test_circle(self) -> None:
        """Verify circle drawing with radius, alignments, custom styles, and preset styles."""
        clear()
        styles = default_styles
        s_def = styles.White.patch(shape_line_color=Colors.Black, shape_line_width=1.0)
        styles_essentials = default_styles

        # Simple circle
        circle(xy=(50, 50), radius=30, style=s_def)

        # Alignments and text
        circle(
            xy=(50, 50),
            radius=30,
            style=s_def.patch(halign="left", valign="bottom", angle=45),
            text="Hello",
        )
        circle(
            xy=(50, 50),
            radius=30,
            style=s_def.patch(halign="center", valign="center", angle=45),
            text="Hello",
        )
        circle(
            xy=(50, 50),
            radius=30,
            style=s_def.patch(halign="right", valign="top", angle=45),
            text="Hello",
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
                alpha=0.7,
            ),
        )

        # Preset styles
        circle(xy=(25, 25), radius=20, style=styles_essentials.Blue)
        circle(xy=(25, 75), radius=20, style=styles_essentials.Green)

        save(f"{OUTPUT_DIR}test_circle.png")

    def test_ellipse(self) -> None:
        """Verify ellipse drawing with dimensions, alignments, styles, and angles."""
        clear()
        styles = default_styles
        s_primary = styles.Primary
        s_white = styles.White.patch(shape_line_color=Colors.Black, shape_line_width=1.0)

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
            style=s_white.patch(halign="left", valign="bottom"),
            text="Hello",
        )
        ellipse(
            xy=(50, 50),
            width=40,
            height=20,
            style=s_white.patch(halign="center", valign="center"),
            text="Hello",
        )
        ellipse(
            xy=(50, 50),
            width=40,
            height=20,
            style=s_white.patch(halign="right", valign="top"),
            text="Hello",
        )

        # Orientation angle
        ellipse(xy=(50, 50), width=40, height=20, text="Hello", style=s_primary.patch(angle=45))

        save(f"{OUTPUT_DIR}test_ellipse.png")

    def test_regularpolygon(self) -> None:
        """Verify regular polygon vertices counts, styles, and alignments."""
        clear()
        styles = default_styles
        s_primary = styles.Primary
        s_white = styles.White.patch(shape_line_color=Colors.Black, shape_line_width=1.0)

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
            style=s_white.patch(halign="left", valign="bottom"),
        )
        regularpolygon(
            xy=(50, 50),
            radius=30,
            num_vertex=8,
            text="Hello",
            style=s_white.patch(halign="center", valign="center"),
        )

        # Angle orientation
        regularpolygon(xy=(50, 50), radius=30, num_vertex=5, text="Hello", style=s_primary.patch(angle=45))

        save(f"{OUTPUT_DIR}test_regularpolygon.png")

    def test_wedge(self) -> None:
        """Verify wedge segment drawing with radii, spans, styles, and alignments."""
        clear()
        styles = default_styles
        s_primary = styles.Primary
        s_white = styles.White.patch(shape_line_color=Colors.Black, shape_line_width=1.0)

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
            style=s_white.patch(halign="left", valign="bottom"),
            text="Hello",
        )
        wedge(
            (50, 50),
            radius=30,
            width=10,
            style=s_white.patch(halign="center", valign="center"),
            text="Hello",
        )

        # Angle spans
        wedge(
            (50, 50),
            radius=30,
            angle_start=45,
            angle_end=270,
            width=10,
            text="Hello",
            style=s_primary.patch(angle=120),
        )

        save(f"{OUTPUT_DIR}test_wedge.png")

    def test_circle_hole_ratio(self) -> None:
        """Verify hollow circle (donut) drawing with hole_ratio, styling, and text."""
        clear()
        styles = default_styles
        s_primary = styles.Primary
        s_white = styles.White.patch(shape_line_color=Colors.Black, shape_line_width=1.0)

        # Simple hollow circle
        circle((50, 50), radius=30, hole_ratio=20 / 30, style=s_primary)

        # Styled hollow circle
        circle(
            (50, 50),
            radius=30,
            hole_ratio=20 / 30,
            style=s_white.patch(
                shape_line_width=3,
                shape_line_color=Colors.Red,
                shape_line_style="dashdot",
                shape_fill_color=Colors.Green,
            ),
            text="Hello",
        )

        # Alignments
        circle(
            (50, 50),
            radius=30,
            hole_ratio=20 / 30,
            style=s_white.patch(halign="left", valign="bottom"),
            text="Hello",
        )
        circle(
            (50, 50),
            radius=30,
            hole_ratio=20 / 30,
            style=s_white.patch(halign="center", valign="center"),
            text="Hello",
        )

        # Rotation angle
        circle((50, 50), radius=30, hole_ratio=20 / 30, text="hungry", style=s_primary.patch(angle=120))

        save(f"{OUTPUT_DIR}test_donuts.png")

    def test_fan(self) -> None:
        """Verify fan sector drawing with radius, theta boundaries, styling, and text."""
        clear()
        styles = default_styles
        s_primary = styles.Primary
        s_white = styles.White.patch(shape_line_color=Colors.Black, shape_line_width=1.0)

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
            style=s_white.patch(halign="left", valign="bottom"),
            text="Hello",
        )
        fan(
            (50, 50),
            radius=30,
            angle_start=45,
            angle_end=90,
            style=s_white.patch(halign="center", valign="center"),
            text="Hello",
        )

        # Rotation angles
        fan((50, 50), radius=30, angle_start=45, angle_end=270, text="Hello", style=s_primary.patch(angle=120))

        save(f"{OUTPUT_DIR}test_fan.png")

    def test_basic_shapes_hole_ratio(self) -> None:
        """Verify hole_ratio rendering on circle, ellipse, rectangle, and regularpolygon."""
        clear()
        circle((25, 50), radius=15, hole_ratio=0.5, style=Styles.PrimaryNeutral, text="C")
        ellipse((50, 50), width=30, height=20, hole_ratio=0.4, style=Styles.SecondaryNeutral.patch(angle=20), text="E")
        rectangle(
            (75, 50),
            width=24,
            height=18,
            hole_ratio=0.5,
            style=Styles.AccentNeutral.patch(shape_r=1.5),
            text="R",
        )
        regularpolygon(
            (50, 20),
            radius=14,
            num_vertex=6,
            hole_ratio=0.5,
            style=Styles.SuccessNeutral.patch(shape_r=1.0, angle=15),
            text="P",
        )
        assert len(canvas._artists) == 8  # 4 hollow PathPatches + 4 Text artists

    def test_basic_hole_ratio_validation_errors(self) -> None:
        """Verify hole_ratio boundary validation errors on basic shapes."""
        clear()
        for bad_ratio in (0.0, 1.0, -0.2, 1.5):
            with pytest.raises((ValueError, ValidationError)):
                circle((50, 50), radius=10, hole_ratio=bad_ratio, style=Styles.Neutral)
            with pytest.raises((ValueError, ValidationError)):
                ellipse((50, 50), width=20, height=10, hole_ratio=bad_ratio, style=Styles.Neutral)
            with pytest.raises((ValueError, ValidationError)):
                rectangle((50, 50), width=20, height=10, hole_ratio=bad_ratio, style=Styles.Neutral)
            with pytest.raises((ValueError, ValidationError)):
                regularpolygon((50, 50), radius=10, num_vertex=5, hole_ratio=bad_ratio, style=Styles.Neutral)
