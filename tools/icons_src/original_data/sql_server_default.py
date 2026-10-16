# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Data concept icon: sql_server."""

import math

from drawlib.canvas import save
from drawlib.shapes import circle, polygon
from drawlib.styles import Colors
from drawlib.utils import (
    DARK,
    WHITE,
    draw_cylinder_tier,
    draw_round_polyline,
    fill_style,
    no_border_fill,
    setup_icon,
)

setup_icon()

w = 1.9
cx = 50.0
width = 68.0
ry = 7.2
body_h = 15.0


def _draw_tier_accent_band(y_bot: float) -> None:
    """Draw a recessed curved Colors.Red3 band and two WHITE LEDs on a cylinder tier."""
    # Curved horizontal band on right-front side of cylinder (angles 262..342 deg)
    y_b0 = y_bot + 4.8
    y_b1 = y_bot + 10.2
    w_half = width / 2.0
    steps = 16
    band_pts: list[tuple[float, float]] = []
    for i in range(steps + 1):
        ang = math.radians(262.0 + (342.0 - 262.0) * (i / steps))
        band_pts.append((cx + w_half * math.cos(ang), y_b0 + ry * math.sin(ang)))
    for i in range(steps + 1):
        ang = math.radians(342.0 - (342.0 - 262.0) * (i / steps))
        band_pts.append((cx + w_half * math.cos(ang), y_b1 + ry * math.sin(ang)))

    polygon(band_pts, style=no_border_fill(Colors.Red3))
    draw_round_polyline(band_pts, width_units=1.5, color=DARK, closed=True)

    # Two status LED dots on left-front side following the cylinder curve
    for deg in (218.0, 238.0):
        ang = math.radians(deg)
        lx = cx + w_half * math.cos(ang)
        ly = y_bot + 7.5 + ry * math.sin(ang)
        circle(
            (lx, ly),
            radius=2.5,
            style=fill_style(WHITE, border_color=DARK, border_units=1.5),
        )


# Draw 3 stacked enterprise SQL database cylinder tiers from bottom to top
tier_y_bottoms = [18.2, 42.5, 66.8]

for y_bot in tier_y_bottoms:
    draw_cylinder_tier(
        cx=cx,
        y_bottom=y_bot,
        width=width,
        body_h=body_h,
        ry=ry,
        body_color=Colors.Gray3,
        top_color=Colors.Gray2,
        border_color=DARK,
        border_units=w,
        draw_top_cap=True,
    )
    _draw_tier_accent_band(y_bot)

save()
