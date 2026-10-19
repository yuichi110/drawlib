# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Workspace concept icon: video_meeting."""

import math

from drawlib.canvas import save
from drawlib.shapes import circle, polygon, rectangle
from drawlib.utils import Icon

Icon.setup()

w_outer = 2.0
w_inner = 1.6


def _arc_pts(
    cx: float,
    cy: float,
    r: float,
    deg_start: float,
    deg_end: float,
    steps: int = 12,
) -> list[tuple[float, float]]:
    return [
        (
            cx + r * math.cos(math.radians(deg_start + (deg_end - deg_start) * (i / steps))),
            cy + r * math.sin(math.radians(deg_start + (deg_end - deg_start) * (i / steps))),
        )
        for i in range(steps + 1)
    ]


x0, y0, x1, y1 = 13.0, 24.0, 79.0, 81.0
y_hdr = 68.0
r_win = 5.0

# 1. WHITE video conference window body
win_pts: list[tuple[float, float]] = [
    *_arc_pts(x0 + r_win, y0 + r_win, r_win, 180.0, 270.0),
    *_arc_pts(x1 - r_win, y0 + r_win, r_win, 270.0, 360.0),
    *_arc_pts(x1 - r_win, y1 - r_win, r_win, 0.0, 90.0),
    *_arc_pts(x0 + r_win, y1 - r_win, r_win, 90.0, 180.0),
]
polygon(win_pts, style=Icon.no_border_fill(Icon.WHITE))

# 2. PASTEL_BLUE top header bar + window control dots
hdr_pts: list[tuple[float, float]] = [
    (x0, y_hdr),
    (x1, y_hdr),
    *_arc_pts(x1 - r_win, y1 - r_win, r_win, 0.0, 90.0),
    *_arc_pts(x0 + r_win, y1 - r_win, r_win, 90.0, 180.0),
]
polygon(hdr_pts, style=Icon.no_border_fill(Icon.PASTEL_BLUE))
Icon.draw_round_polyline(win_pts, width_units=w_outer, color=Icon.DARK, closed=True)
Icon.draw_round_segment((x0, y_hdr), (x1, y_hdr), width_units=w_outer, color=Icon.DARK)

for dot_x in (21.0, 27.0, 33.0):
    circle((dot_x, 74.5), radius=1.6, style=Icon.fill_style(Icon.DARK))

# 3. User silhouette inside screen (PASTEL_BLUE_LIGHT)
circle(
    (44.5, 53.5),
    radius=8.2,
    style=Icon.fill_style(Icon.PASTEL_BLUE_LIGHT, border_color=Icon.DARK, border_units=w_inner),
)

shoulder_pts: list[tuple[float, float]] = [
    (28.0, 30.0),
    (61.0, 30.0),
    *_arc_pts(44.5, 30.0, 16.5, 0.0, 180.0, 20),
]
polygon(shoulder_pts, style=Icon.no_border_fill(Icon.PASTEL_BLUE_LIGHT))
Icon.draw_round_polyline(shoulder_pts, width_units=w_inner, color=Icon.DARK, closed=True)

# 4. Video camera badge at bottom-right (PASTEL_GREEN)
lens_pts: list[tuple[float, float]] = [
    (75.0, 21.5),
    (87.0, 16.5),
    (87.0, 32.5),
    (75.0, 27.5),
]
polygon(lens_pts, style=Icon.no_border_fill(Icon.PASTEL_GREEN))
Icon.draw_round_polyline(lens_pts, width_units=w_outer, color=Icon.DARK, closed=True)

rectangle(
    (65.5, 24.5),
    width=21.0,
    height=18.0,
    style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=w_outer, shape_r=3.5),
)

circle(
    (65.5, 24.5),
    radius=3.2,
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w_inner),
)

save()
