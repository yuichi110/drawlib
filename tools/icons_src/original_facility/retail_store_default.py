# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Facility concept icon: retail_store."""

import math

from drawlib.canvas import save
from drawlib.shapes import circle, polygon, rectangle
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

w_outer = 2.0
w_inner = 1.6

# 1. Main storefront building wall (WHITE, x=16..84, y=16..80)
rectangle(
    (50.0, 48.0),
    width=68.0,
    height=64.0,
    style=fill_style(WHITE, border_color=DARK, border_units=w_outer),
)

# 2. Left entrance door (x=22..40, y=16..50)
rectangle(
    (31.0, 33.0),
    width=18.0,
    height=34.0,
    style=fill_style(PASTEL_BLUE_LIGHT, border_color=DARK, border_units=w_outer, shape_r=1.5),
)
# Door lower kickplate in PASTEL_BLUE
rectangle(
    (31.0, 19.5),
    width=18.0,
    height=7.0,
    style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=w_inner),
)
# Door handle
circle((36.5, 33.0), radius=1.4, style=fill_style(DARK))

# 3. Right display window (x=46..78, y=26..50)
rectangle(
    (62.0, 38.0),
    width=32.0,
    height=24.0,
    style=fill_style(PASTEL_BLUE_LIGHT, border_color=DARK, border_units=w_outer, shape_r=2.0),
)
# Window sill
rectangle(
    (62.0, 24.5),
    width=34.0,
    height=3.5,
    style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=w_inner, shape_r=1.0),
)
# Window shine lines
draw_round_segment((53.0, 32.0), (59.0, 44.0), width_units=w_inner, color=WHITE)
draw_round_segment((58.5, 31.0), (62.5, 39.0), width_units=w_inner, color=WHITE)

# 4. Striped awning (6 alternating PASTEL_BLUE / PASTEL_GREEN stripes)
# Top edge: x=16..84 at y=77.5; Bottom slope: x=12..88 at y=60.5; Scallop drop: ry=5.2
n_stripes = 6
for i in range(n_stripes):
    col = PASTEL_BLUE if i % 2 == 0 else PASTEL_GREEN
    xt0 = 16.0 + i * (68.0 / n_stripes)
    xt1 = 16.0 + (i + 1) * (68.0 / n_stripes)
    xb0 = 12.0 + i * (76.0 / n_stripes)
    xb1 = 12.0 + (i + 1) * (76.0 / n_stripes)
    cx = 0.5 * (xb0 + xb1)
    rx = 0.5 * (xb1 - xb0)
    ry = 5.2

    scallop_pts: list[tuple[float, float]] = []
    steps = 12
    for s in range(steps + 1):
        ang = math.radians(180.0 + 180.0 * (s / steps))
        scallop_pts.append((cx + rx * math.cos(ang), 60.5 + ry * math.sin(ang)))

    stripe_pts = [
        (xt0, 77.5),
        *scallop_pts,
        (xt1, 77.5),
    ]
    polygon(stripe_pts, style=no_border_fill(col))
    draw_round_polyline(stripe_pts, width_units=w_outer, color=DARK, closed=True)

# 5. Top parapet cornice bar (PASTEL_BLUE, drawn over awning top edge)
rectangle(
    (50.0, 80.5),
    width=74.0,
    height=7.0,
    style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=w_outer, shape_r=2.0),
)

# 6. Ground base plinth
rectangle(
    (50.0, 14.5),
    width=76.0,
    height=3.5,
    style=fill_style(PASTEL_BLUE_LIGHT, border_color=DARK, border_units=w_outer, shape_r=1.5),
)

save()
