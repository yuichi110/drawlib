# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original concept icon: analytics_engine."""

import math
from typing import Any

from drawlib.canvas import save
from drawlib.lines import lines
from drawlib.shapes import circle, polygon, rectangle
from drawlib.utils import Icon


def draw_gear(
    xy: tuple[float, float],
    *,
    outer_r: float = 40.0,
    inner_r: float = 31.0,
    teeth: int = 8,
    fill_color: Any = Icon.PASTEL_BLUE_LIGHT,
    border_color: Any = Icon.DARK,
    border_units: float = Icon.ORIG_STROKE,
) -> None:
    """Draw a mechanical gear polygon with smooth root arcs and rounded tooth corners."""
    cx, cy = xy
    step_deg = 360.0 / teeth
    half_root = step_deg * 0.23
    half_tip = step_deg * 0.145

    pts: list[tuple[float, float]] = []
    corner_pts: list[tuple[float, float]] = []
    arc_steps = 6

    for i in range(teeth):
        center_deg = i * step_deg
        a_root_l = math.radians(center_deg - half_root)
        a_tip_l = math.radians(center_deg - half_tip)
        a_tip_r = math.radians(center_deg + half_tip)
        a_root_r = math.radians(center_deg + half_root)

        p_rl = (cx + inner_r * math.cos(a_root_l), cy + inner_r * math.sin(a_root_l))
        p_tl = (cx + outer_r * math.cos(a_tip_l), cy + outer_r * math.sin(a_tip_l))
        p_tr = (cx + outer_r * math.cos(a_tip_r), cy + outer_r * math.sin(a_tip_r))
        p_rr = (cx + inner_r * math.cos(a_root_r), cy + inner_r * math.sin(a_root_r))

        pts.extend([p_rl, p_tl, p_tr, p_rr])
        corner_pts.extend([p_rl, p_tl, p_tr, p_rr])

        next_root_l_deg = (i + 1) * step_deg - half_root
        start_valley_deg = center_deg + half_root
        for s in range(1, arc_steps):
            ang = math.radians(start_valley_deg + (next_root_l_deg - start_valley_deg) * (s / arc_steps))
            pts.append((cx + inner_r * math.cos(ang), cy + inner_r * math.sin(ang)))

    polygon(pts, style=Icon.no_border_fill(fill_color))
    lines([*pts, pts[0]], style=Icon.stroke_style(border_color, width_units=border_units))
    for cp in corner_pts:
        Icon.draw_cap(cp, width_units=border_units, color=border_color)


Icon.setup()

w = Icon.ORIG_STROKE

# 1. Outer analytics engine gear
draw_gear(
    (50.0, 50.0),
    outer_r=39.5,
    inner_r=31.0,
    teeth=8,
    fill_color=Icon.PASTEL_BLUE_LIGHT,
    border_color=Icon.DARK,
    border_units=w,
)

# 2. Inner white dial circle
circle(
    (50.0, 50.0),
    radius=24.0,
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w),
)

# 3. Three rising bar chart columns
y_base = 34.5
bars = [
    (39.0, 10.5, Icon.PASTEL_BLUE),
    (50.0, 16.5, Icon.PASTEL_BLUE),
    (61.0, 23.5, Icon.PASTEL_GREEN),
]
for bx, bh, bcol in bars:
    rectangle(
        (bx, y_base + bh / 2.0),
        width=7.2,
        height=bh,
        style=Icon.fill_style(bcol, border_color=Icon.DARK, border_units=2.0, shape_r=1.6),
    )

# 4. Rising trend line above the bars
trend_pts = [(38.5, 51.0), (49.5, 57.5), (60.5, 64.0)]
Icon.draw_round_polyline(trend_pts, width_units=2.0, color=Icon.DARK)
circle(
    trend_pts[-1],
    radius=3.2,
    style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=2.0),
)

save()
