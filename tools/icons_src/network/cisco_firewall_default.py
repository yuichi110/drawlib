# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Cisco classic 3D icon: firewall (default variant)."""

from drawlib.canvas import save
from drawlib.utils import (
    CISCO_BORDER,
    WHITE,
    draw_cisco_3d_box,
    draw_round_polyline,
    draw_round_segment,
    setup_icon,
)

setup_icon()

x0 = 19.0
y0 = 10.0
w_front = 44.0
h_front = 66.0
dx = 18.0
dy = 14.0
x1 = x0 + w_front
y1 = y0 + h_front

draw_cisco_3d_box(x0, y0, w_front, h_front, dx, dy)

mortar_w = 1.55
num_rows = 6
row_h = h_front / num_rows

# Horizontal mortar lines across front and right-side faces
for r in range(1, num_rows):
    y_r = y0 + r * row_h
    draw_round_segment((x0, y_r), (x1, y_r), width_units=mortar_w, color=WHITE)
    draw_round_segment((x1, y_r), (x1 + dx, y_r + dy), width_units=mortar_w, color=WHITE)

# Staggered vertical mortar joints on front and right-side faces
for r in range(num_rows):
    yb = y0 + r * row_h
    yt = yb + row_h
    if r % 2 == 0:
        front_fracs = (1.0 / 3.0, 2.0 / 3.0)
        side_fracs = (0.5,)
    else:
        front_fracs = (1.0 / 6.0, 0.5, 5.0 / 6.0)
        side_fracs = (0.25, 0.75)

    for fx in front_fracs:
        vx = x0 + w_front * fx
        draw_round_segment((vx, yb), (vx, yt), width_units=mortar_w, color=WHITE)

    for fs in side_fracs:
        sx = x1 + dx * fs
        sy_b = yb + dy * fs
        sy_t = yt + dy * fs
        draw_round_segment((sx, sy_b), (sx, sy_t), width_units=mortar_w, color=WHITE)

# Top face mortar lines (continuing top row joints + mid-depth seam)
draw_round_segment(
    (x0 + dx * 0.5, y1 + dy * 0.5),
    (x1 + dx * 0.5, y1 + dy * 0.5),
    width_units=mortar_w,
    color=WHITE,
)
for fx in (1.0 / 6.0, 0.5, 5.0 / 6.0):
    tx = x0 + w_front * fx
    draw_round_segment((tx, y1), (tx + dx * 0.5, y1 + dy * 0.5), width_units=mortar_w, color=WHITE)
for fx in (1.0 / 3.0, 2.0 / 3.0):
    tx = x0 + w_front * fx
    draw_round_segment((tx + dx * 0.5, y1 + dy * 0.5), (tx + dx, y1 + dy), width_units=mortar_w, color=WHITE)

# Re-stroke outer dark contour cleanly over mortar endpoints
outer_pts = [
    (x0, y0),
    (x1, y0),
    (x1 + dx, y0 + dy),
    (x1 + dx, y1 + dy),
    (x0 + dx, y1 + dy),
    (x0, y1),
]
draw_round_polyline(outer_pts, width_units=1.8, color=CISCO_BORDER, closed=True)

save()
