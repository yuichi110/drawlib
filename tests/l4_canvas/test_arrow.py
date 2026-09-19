# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Unit and integration tests for CanvasOriginalArrowFeature shapes."""

import pytest

from drawlib.canvas import clear, save
from drawlib.colors import Colors
from drawlib.shapes import arrow, arrow_arc, arrow_l, arrow_polyline, arrow_u, ellipse
from drawlib.text import text
from drawlib.types import (
    ShapeStyle,
    ShapeTextStyle,
    TextStyle,
)

# ruff: noqa: F403, F405

OUTPUT_DIR = "../../output_tests/l4_canvas/arrow/"


class TestCanvasArrow:
    """Tests for the CanvasOriginalArrowFeature class and arrow drawing methods."""

    def test_arrow(self) -> None:
        """Verify standard arrow drawing with different heads, styling, and text."""
        clear()

        # Simple arrow
        text((5, 10), "simple", style=TextStyle(text_size=14, text_halign="left"))
        arrow(
            (40, 10),
            (90, 10),
            tail_width=5,
            head_width=10,
            head_length=10,
        )

        # Arrow with style
        text((5, 20), "style", style=TextStyle(text_size=14, text_halign="left"))
        arrow(
            (40, 20),
            (90, 20),
            tail_width=5,
            head_width=10,
            head_length=10,
            style=ShapeStyle(
                line_color=Colors.Red,
                fill_color=Colors.Transparent,
                line_width=5,
                line_style="dotted",
            ),
        )

        # Arrow with text & flipping/shifting options
        text((5, 30), "text", style=TextStyle(text_size=14, text_halign="left"))
        arrow(
            (40, 30),
            (90, 30),
            tail_width=5,
            head_width=10,
            head_length=10,
            text="Hello Drawlib",
        )
        text((5, 40), "text (flip)", style=TextStyle(text_size=14, text_halign="left"))
        arrow(
            (40, 40),
            (90, 40),
            tail_width=5,
            head_width=10,
            head_length=10,
            text="Hello Drawlib",
            textstyle=ShapeTextStyle(text_flip=True),
        )
        text((5, 50), "text (shift)", style=TextStyle(text_size=14, text_halign="left"))
        arrow(
            (40, 50),
            (90, 50),
            tail_width=5,
            head_width=10,
            head_length=10,
            head="->",
            text="Hello Drawlib",
            textstyle=ShapeTextStyle(text_xy_shift=(2.5, 2.5)),
        )

        # Other heads
        text((5, 60), "head <-", style=TextStyle(text_size=14, text_halign="left"))
        arrow(
            (40, 60),
            (90, 60),
            tail_width=5,
            head_width=10,
            head_length=10,
            head="<-",
        )
        text((5, 70), "head <->", style=TextStyle(text_size=14, text_halign="left"))
        arrow(
            (40, 70),
            (90, 70),
            tail_width=5,
            head_width=10,
            head_length=10,
            head="<->",
        )

        # Theme styles
        text((5, 80), "theme style", style=TextStyle(text_size=14, text_halign="left"))
        arrow(
            (40, 80),
            (90, 80),
            tail_width=5,
            head_width=10,
            head_length=10,
            head="->",
            style="blue",
            text="Hello Drawlib",
            textstyle="white",
        )
        save(f"{OUTPUT_DIR}test_arrow.png")

    def test_arrow_polyline(self) -> None:
        """Verify polyline arrow drawing, point duplicates, and head styles."""
        clear()

        # Standard polyline arrow
        arrow_polyline(
            xys=[(10, 10), (10, 30), (30, 30), (30, 10)],
            tail_width=2,
            head_length=3,
            head_width=5,
            head="->",
            r=5,
        )

        # Polyline with duplicated consecutive points
        arrow_polyline(
            xys=[(40, 10), (40, 30), (40, 30), (60, 30), (60, 10)],
            tail_width=2,
            head_length=3,
            head_width=5,
            head="->",
            r=5,
        )

        # Polyline with straight slopes (same m)
        arrow_polyline(
            xys=[(10, 40), (10, 50), (10, 60), (10, 60), (30, 60), (30, 40)],
            tail_width=2,
            head_length=3,
            head_width=5,
            head="->",
            r=5,
        )

        # Other heads
        arrow_polyline(
            xys=[(40, 40), (40, 60), (60, 60), (60, 40)],
            tail_width=2,
            head_length=3,
            head_width=5,
            head="<-",
            r=5,
        )
        arrow_polyline(
            xys=[(70, 40), (70, 60), (90, 60), (90, 40)],
            tail_width=2,
            head_length=3,
            head_width=5,
            head="<->",
            r=5,
        )

        save(f"{OUTPUT_DIR}test_arrow_polyline.png")

    def test_arrow_arc(self) -> None:
        """Verify elliptical arc arrow drawing on circles and ellipses."""
        clear()

        # On circle (quadrant 1)
        ellipse(xy=(25, 25), width=30, height=30, style="dashed")
        arrow_arc(
            xy=(25, 25),
            width=30,
            height=30,
            tail_width=5,
            head_angle=20,
            head_width=10,
            head="->",
            angle_start=45,
            angle_end=135,
        )

        # Other heads & full angles on circles (quadrant 2)
        ellipse(xy=(25, 75), width=30, height=30, style="dashed")
        arrow_arc(
            xy=(25, 75),
            width=30,
            height=30,
            tail_width=5,
            head_angle=20,
            head_width=10,
            head="<->",
            angle_start=0,
            angle_end=270,
        )

        # Ellipse (quadrant 3)
        ellipse(xy=(75, 25), width=40, height=20, style="dashed")
        arrow_arc(
            xy=(75, 25),
            width=40,
            height=20,
            tail_width=5,
            head_angle=20,
            head_width=10,
            head="->",
            angle_start=45,
            angle_end=135,
        )

        # Ellipse with 45 degrees orientation (quadrant 4)
        ellipse(xy=(75, 75), width=40, height=20, style="dashed", angle=45)
        arrow_arc(
            xy=(75, 75),
            width=40,
            height=20,
            tail_width=5,
            head_angle=20,
            head_width=10,
            head="->",
            angle_start=45,
            angle_end=135,
            angle=45,
        )

        save(f"{OUTPUT_DIR}test_arrow_arc.png")

    def test_arrow_l(self) -> None:
        """Verify L-shape arrow drawing and rotation angle options."""
        clear()

        arrow_l(
            (25, 25),
            width=20,
            height=15,
            tail_width=5,
            head_width=10,
            head_length=10,
        )

        arrow_l(
            xy=(25, 75),
            width=20,
            height=15,
            tail_width=2,
            head_length=3,
            head_width=5,
            head="->",
            r=5,
        )

        # Angles & other heads
        arrow_l(
            xy=(75, 25), width=20, height=15, tail_width=2, head_length=3, head_width=5, head="->", r=5, angle=90
        )
        arrow_l(xy=(75, 75), width=20, height=15, tail_width=2, head_length=3, head_width=5, head="<-", r=5)
        arrow_l(xy=(50, 50), width=20, height=15, tail_width=2, head_length=3, head_width=5, head="<->", r=5)

        save(f"{OUTPUT_DIR}test_arrow_l.png")

    def test_arrow_u(self) -> None:
        """Verify U-shape arrow drawing and rotation angle options."""
        clear()

        arrow_u(
            xy=(25, 25),
            width=20,
            height=15,
            tail_width=2,
            head_length=3,
            head_width=5,
            head="->",
            r=5,
        )

        # Angles & other heads
        arrow_u(
            xy=(25, 75), width=20, height=15, tail_width=2, head_length=3, head_width=5, head="->", r=5, angle=90
        )
        arrow_u(xy=(75, 25), width=20, height=15, tail_width=2, head_length=3, head_width=5, head="<-", r=5)
        arrow_u(xy=(75, 75), width=20, height=15, tail_width=2, head_length=3, head_width=5, head="<->", r=5)

        save(f"{OUTPUT_DIR}test_arrow_u.png")
