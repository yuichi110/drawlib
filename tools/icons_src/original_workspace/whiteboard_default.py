# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Workspace concept icon: whiteboard."""

from drawlib.canvas import save
from drawlib.shapes import rectangle
from drawlib.utils import (
    DARK,
    PASTEL_BLUE,
    PASTEL_BLUE_LIGHT,
    PASTEL_GREEN,
    WHITE,
    draw_round_polyline,
    draw_round_segment,
    fill_style,
    setup_icon,
)

setup_icon()

w_outer = 2.0
w_inner = 1.6

# 1. Easel legs at bottom and top board clamp
draw_round_segment((33.0, 22.0), (28.5, 13.5), width_units=w_outer, color=DARK)
draw_round_segment((67.0, 22.0), (71.5, 13.5), width_units=w_outer, color=DARK)
rectangle(
    (50.0, 85.0),
    width=14.0,
    height=4.5,
    style=fill_style(PASTEL_BLUE_LIGHT, border_color=DARK, border_units=w_outer, shape_r=1.8),
)

# 2. Outer PASTEL_BLUE_LIGHT board frame (x=13.5..86.5, y=24.0..83.5)
rectangle(
    (50.0, 53.75),
    width=73.0,
    height=59.5,
    style=fill_style(PASTEL_BLUE_LIGHT, border_color=DARK, border_units=w_outer, shape_r=4.5),
)

# 3. Inner WHITE collaborative canvas (x=18.0..82.0, y=28.5..79.0)
rectangle(
    (50.0, 53.75),
    width=64.0,
    height=50.5,
    style=fill_style(WHITE, border_color=DARK, border_units=w_inner, shape_r=2.5),
)

# 4. Bottom marker tray bar
rectangle(
    (50.0, 22.5),
    width=76.0,
    height=5.0,
    style=fill_style(PASTEL_BLUE_LIGHT, border_color=DARK, border_units=w_outer, shape_r=2.2),
)

# 5. Two square sticky notes (PASTEL_BLUE top-left, PASTEL_GREEN bottom-right)
notes = [
    (32.5, 62.5, PASTEL_BLUE),
    (66.5, 44.5, PASTEL_GREEN),
]
for nx, ny, col in notes:
    rectangle(
        (nx, ny),
        width=17.5,
        height=17.5,
        style=fill_style(col, border_color=DARK, border_units=w_inner, shape_r=2.2),
    )
    draw_round_segment((nx - 4.5, ny + 2.2), (nx + 4.5, ny + 2.2), width_units=w_inner, color=DARK)
    draw_round_segment((nx - 4.5, ny - 2.8), (nx + 1.5, ny - 2.8), width_units=w_inner, color=DARK)

# 6. Smooth curved DARK arrow from blue sticky note to green sticky note
p0 = (43.5, 63.5)
p1 = (57.0, 65.5)
p2 = (66.5, 63.0)
p3 = (66.5, 55.5)
curve_pts: list[tuple[float, float]] = []
steps = 18
for i in range(steps + 1):
    t = i / steps
    mt = 1.0 - t
    bx = (mt**3) * p0[0] + 3 * (mt**2) * t * p1[0] + 3 * mt * (t**2) * p2[0] + (t**3) * p3[0]
    by = (mt**3) * p0[1] + 3 * (mt**2) * t * p1[1] + 3 * mt * (t**2) * p2[1] + (t**3) * p3[1]
    curve_pts.append((bx, by))

draw_round_polyline(curve_pts, width_units=w_inner, color=DARK)
draw_round_polyline([(63.2, 59.2), (66.5, 55.5), (69.8, 59.2)], width_units=w_inner, color=DARK)

save()
