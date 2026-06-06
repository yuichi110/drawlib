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

from drawlib.v0_2.apis import (
    Colors,
    ShapeStyle,
    ShapeTextStyle,
    arrow,
    arrow_arc,
    arrow_l,
    arrow_polyline,
    arrow_u,
    clear,
    ellipse,
    save,
)

# ruff: noqa: F403, F405

OUTPUT_DIR = "../../../output_tests/v0_2/l5_canvas/arrow/"


class TestCanvasArrow:
    """Tests for the CanvasOriginalArrowFeature class and arrow drawing methods."""

    def test_arrow(self) -> None:
        """Verify standard arrow drawing with different heads, styling, and text."""
        clear()

        # Simple arrow
        arrow(
            (10, 10),
            (90, 10),
            tail_width=5,
            head_width=10,
            head_length=10,
        )

        # Arrow with style
        arrow(
            (10, 20),
            (90, 20),
            tail_width=5,
            head_width=10,
            head_length=10,
            style=ShapeStyle(
                lcolor=Colors.Red,
                fcolor=Colors.Transparent,
                lwidth=5,
                lstyle="dotted",
            ),
        )

        # Arrow with text & flipping/shifting options
        arrow(
            (10, 30),
            (90, 30),
            tail_width=5,
            head_width=10,
            head_length=10,
            text="Hello Drawlib",
        )
        arrow(
            (10, 40),
            (90, 40),
            tail_width=5,
            head_width=10,
            head_length=10,
            text="Hello Drawlib",
            textstyle=ShapeTextStyle(flip=True),
        )
        arrow(
            (10, 50),
            (90, 50),
            tail_width=5,
            head_width=10,
            head_length=10,
            head="->",
            text="Hello Drawlib",
            textstyle=ShapeTextStyle(xy_shift=(2.5, 2.5)),
        )

        # Other heads
        arrow(
            (10, 60),
            (90, 60),
            tail_width=5,
            head_width=10,
            head_length=10,
            head="<-",
        )
        arrow(
            (10, 70),
            (90, 70),
            tail_width=5,
            head_width=10,
            head_length=10,
            head="<->",
        )

        # Theme styles
        arrow(
            (10, 80),
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
            xys=[(10, 10), (10, 50), (50, 50), (50, 10)],
            tail_width=2,
            head_length=3,
            head_width=5,
            head="->",
            r=5,
        )

        # Polyline with duplicated consecutive points
        arrow_polyline(
            xys=[(10, 10), (10, 50), (10, 50), (50, 50), (50, 10)],
            tail_width=2,
            head_length=3,
            head_width=5,
            head="->",
            r=5,
        )

        # Polyline with straight slopes (same m)
        arrow_polyline(
            xys=[(10, 10), (10, 30), (10, 50), (10, 50), (50, 50), (50, 10)],
            tail_width=2,
            head_length=3,
            head_width=5,
            head="->",
            r=5,
        )

        # Other heads
        arrow_polyline(
            xys=[(10, 10), (10, 50), (50, 50), (50, 10)],
            tail_width=2,
            head_length=3,
            head_width=5,
            head="<-",
            r=5,
        )
        arrow_polyline(
            xys=[(10, 10), (10, 50), (50, 50), (50, 10)],
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

        # On circle
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

        # Other heads & full angles on circles
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

        # Ellipse
        ellipse(xy=(25, 25), width=40, height=20, style="dashed")
        arrow_arc(
            xy=(25, 25),
            width=40,
            height=20,
            tail_width=5,
            head_angle=20,
            head_width=10,
            head="->",
            angle_start=45,
            angle_end=135,
        )

        # Ellipse with 45 degrees orientation
        ellipse(xy=(25, 25), width=40, height=20, style="dashed", angle=45)
        arrow_arc(
            xy=(25, 25),
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
            (50, 25),
            width=30,
            height=20,
            tail_width=5,
            head_width=10,
            head_length=10,
        )

        arrow_l(
            xy=(50, 50),
            width=60,
            height=30,
            tail_width=2,
            head_length=3,
            head_width=5,
            head="->",
            r=5,
        )

        # Angles & other heads
        arrow_l(xy=(50, 50), width=60, height=30, tail_width=2, head_length=3, head_width=5, head="->", r=5, angle=90)
        arrow_l(xy=(50, 50), width=60, height=30, tail_width=2, head_length=3, head_width=5, head="<-", r=5)
        arrow_l(xy=(50, 50), width=60, height=30, tail_width=2, head_length=3, head_width=5, head="<->", r=5)

        save(f"{OUTPUT_DIR}test_arrow_l.png")

    def test_arrow_u(self) -> None:
        """Verify U-shape arrow drawing and rotation angle options."""
        clear()

        arrow_u(
            xy=(50, 50),
            width=60,
            height=30,
            tail_width=2,
            head_length=3,
            head_width=5,
            head="->",
            r=5,
        )

        # Angles & other heads
        arrow_u(xy=(50, 50), width=60, height=30, tail_width=2, head_length=3, head_width=5, head="->", r=5, angle=90)
        arrow_u(xy=(50, 50), width=60, height=30, tail_width=2, head_length=3, head_width=5, head="<-", r=5)
        arrow_u(xy=(50, 50), width=60, height=30, tail_width=2, head_length=3, head_width=5, head="<->", r=5)

        save(f"{OUTPUT_DIR}test_arrow_u.png")
