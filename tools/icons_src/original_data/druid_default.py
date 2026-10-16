# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Data concept icon: druid."""

import math

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.styles import Colors
from drawlib.utils import (
    DARK,
    draw_round_polyline,
    no_border_fill,
    setup_icon,
)


def _arc_points(
    cx: float,
    cy: float,
    radius: float,
    deg_start: float,
    deg_end: float,
    steps: int = 24,
) -> list[tuple[float, float]]:
    """Sample circular arc points from deg_start to deg_end inclusive."""
    pts: list[tuple[float, float]] = []
    for i in range(steps + 1):
        t = i / steps
        ang = math.radians(deg_start + (deg_end - deg_start) * t)
        pts.append((cx + radius * math.cos(ang), cy + radius * math.sin(ang)))
    return pts


def _build_d_ribbon(
    x_top_start: float,
    x_bot_start: float,
    cx_arc: float,
    cy_arc: float,
    r_center: float,
    thickness: float,
) -> list[tuple[float, float]]:
    """Build a smooth closed D-wave ribbon polygon with semicircular left end caps."""
    ht = thickness / 2.0
    r_out = r_center + ht
    r_in = r_center - ht
    pts: list[tuple[float, float]] = []

    # Outer contour (top-left -> top-right -> right outer semicircle -> bottom-left)
    pts.extend(_arc_points(cx_arc, cy_arc, r_out, 90.0, -90.0, steps=32))
    # Bottom-left semicircular end cap
    pts.extend(_arc_points(x_bot_start, cy_arc - r_center, ht, -90.0, -270.0, steps=14))
    # Inner contour (bottom-inner -> right inner semicircle -> top-inner)
    pts.extend(_arc_points(cx_arc, cy_arc, r_in, -90.0, 90.0, steps=28))
    # Top-left semicircular end cap
    pts.extend(_arc_points(x_top_start, cy_arc + r_center, ht, -90.0, -270.0, steps=14))
    return pts


def _build_capsule_dash(
    x_left: float,
    x_right: float,
    cy: float,
    thickness: float,
) -> list[tuple[float, float]]:
    """Build a closed horizontal stadium/capsule polygon."""
    ht = thickness / 2.0
    pts: list[tuple[float, float]] = []
    pts.extend(_arc_points(x_right, cy, ht, 90.0, -90.0, steps=14))
    pts.extend(_arc_points(x_left, cy, ht, -90.0, -270.0, steps=14))
    return pts


setup_icon()

w = 1.9
t = 8.4
cx_d = 56.0
cy_d = 50.0

# 1. Outer flowing D-curve (Colors.Teal3)
outer_d = _build_d_ribbon(
    x_top_start=34.0,
    x_bot_start=51.5,
    cx_arc=cx_d,
    cy_arc=cy_d,
    r_center=29.0,
    thickness=t,
)
polygon(outer_d, style=no_border_fill(Colors.Teal3))
draw_round_polyline(outer_d, width_units=w, color=DARK, closed=True)

# 2. Inner flowing D-curve (Colors.Teal2)
inner_d = _build_d_ribbon(
    x_top_start=31.0,
    x_bot_start=21.5,
    cx_arc=cx_d,
    cy_arc=cy_d,
    r_center=13.0,
    thickness=t,
)
polygon(inner_d, style=no_border_fill(Colors.Teal2))
draw_round_polyline(inner_d, width_units=w, color=DARK, closed=True)

# 3. Upper-left droplet dash (Colors.Blue3) with clear gap before inner_d
dash_top = _build_capsule_dash(x_left=13.0, x_right=17.5, cy=63.0, thickness=t)
polygon(dash_top, style=no_border_fill(Colors.Blue3))
draw_round_polyline(dash_top, width_units=w, color=DARK, closed=True)

# 4. Lower-left droplet dash (Colors.Blue3) with clear gap before outer_d
dash_bot = _build_capsule_dash(x_left=31.0, x_right=37.0, cy=21.0, thickness=t)
polygon(dash_bot, style=no_border_fill(Colors.Blue3))
draw_round_polyline(dash_bot, width_units=w, color=DARK, closed=True)

save()
