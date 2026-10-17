# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Code concept icon: sdk_library."""

import math

from drawlib.canvas import save
from drawlib.shapes import polygon, rectangle
from drawlib.utils import (
    DARK,
    PASTEL_BLUE,
    PASTEL_BLUE_LIGHT,
    PASTEL_GREEN,
    WHITE,
    draw_round_polyline,
    draw_round_segment,
    fill_style,
    no_border_fill,
    setup_icon,
)

setup_icon()

w_shape = 1.8


def _arc_points(
    cx: float, cy: float, r: float, deg_start: float, deg_end: float, steps: int = 12
) -> list[tuple[float, float]]:
    return [
        (
            cx + r * math.cos(math.radians(deg_start + (deg_end - deg_start) * (i / steps))),
            cy + r * math.sin(math.radians(deg_start + (deg_end - deg_start) * (i / steps))),
        )
        for i in range(steps + 1)
    ]


# 1. Bottom two modular horizontal book/layer slabs
slabs = [
    # (cx, cy, width, height, fill_color)
    (43.0, 22.0, 58.0, 16.0, WHITE),
    (43.0, 42.0, 58.0, 16.0, PASTEL_BLUE_LIGHT),
]
for cx, cy, sw, sh, col in slabs:
    rectangle(
        (cx, cy),
        width=sw,
        height=sh,
        style=fill_style(col, border_color=DARK, border_units=w_shape, shape_r=4.0),
    )
    draw_round_segment(
        (24.0, cy - sh / 2.0),
        (24.0, cy + sh / 2.0),
        width_units=w_shape,
        color=DARK,
    )

# 2. Top PASTEL_BLUE slab (x=14..60, y=54..70, rounded on left, flat on right at x=60 to interlock cleanly)
r_s = 4.0
top_slab_pts: list[tuple[float, float]] = [
    *_arc_points(14.0 + r_s, 54.0 + r_s, r_s, 180.0, 270.0, 6),
    (60.0, 54.0),
    (60.0, 70.0),
    *_arc_points(14.0 + r_s, 70.0 - r_s, r_s, 90.0, 180.0, 6),
]
polygon(top_slab_pts, style=no_border_fill(PASTEL_BLUE))
draw_round_polyline(top_slab_pts, width_units=w_shape, color=DARK, closed=True)
draw_round_segment((24.0, 54.0), (24.0, 70.0), width_units=w_shape, color=DARK)

# 3. Interlocking PASTEL_GREEN puzzle piece / connector block on top-right
# Main body x=60..86, y=54..80, flat bottom-left corner at (60, 54) flush with top slab!
x0, y0, x1, y1 = 60.0, 54.0, 86.0, 80.0
r_c = 4.0

puzzle_pts: list[tuple[float, float]] = [
    (x0, y0),
    # Bottom-right corner
    *_arc_points(x1 - r_c, y0 + r_c, r_c, 270.0, 360.0, 6),
    # Top-right corner
    *_arc_points(x1 - r_c, y1 - r_c, r_c, 0.0, 90.0, 6),
    # Top puzzle tab bulb (center (73.0, 83.6), r=4.8, angles -48..228)
    (76.2, y1),
    *_arc_points(73.0, 83.6, 4.8, -48.0, 228.0, 16),
    (69.8, y1),
    # Top-left corner
    *_arc_points(x0 + r_c, y1 - r_c, r_c, 90.0, 180.0, 6),
    # Upper part of left edge down to left tab neck
    (x0, 65.2),
    # Left puzzle tab bulb interlocking into PASTEL_BLUE top slab
    *_arc_points(56.4, 62.0, 4.8, 42.0, 318.0, 16),
    (x0, 58.8),
]

polygon(puzzle_pts, style=no_border_fill(PASTEL_GREEN))
draw_round_polyline(puzzle_pts, width_units=w_shape, color=DARK, closed=True)

save()
