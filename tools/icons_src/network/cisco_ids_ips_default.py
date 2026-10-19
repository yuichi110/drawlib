# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Cisco classic 3D icon: ids_ips (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import circle, polygon
from drawlib.utils import Cisco, Icon

Icon.setup()

x0 = 12.0
y0 = 15.0
w_front = 60.0
h_front = 52.0
dx = 16.0
dy = 14.0
x1 = x0 + w_front
y1 = y0 + h_front

Cisco.draw_3d_box(x0, y0, w_front, h_front, dx, dy)

# Bottom 2-row brick sensor barrier across front and side faces
mortar_w = 1.5
y_row1 = y0 + 6.5
y_row2 = y0 + 13.0
for yr in (y_row1, y_row2):
    Icon.draw_round_segment((x0, yr), (x1, yr), width_units=mortar_w, color=Icon.WHITE)
    Icon.draw_round_segment((x1, yr), (x1 + dx, yr + dy), width_units=mortar_w, color=Icon.WHITE)

for vx in (27.0, 42.0, 57.0):
    Icon.draw_round_segment((vx, y0), (vx, y_row1), width_units=mortar_w, color=Icon.WHITE)
for vx in (19.5, 34.5, 49.5, 64.5):
    Icon.draw_round_segment((vx, y_row1), (vx, y_row2), width_units=mortar_w, color=Icon.WHITE)

Icon.draw_round_segment(
    (x1 + dx * 0.5, y0 + dy * 0.5),
    (x1 + dx * 0.5, y_row1 + dy * 0.5),
    width_units=mortar_w,
    color=Icon.WHITE,
)
for fs in (0.25, 0.75):
    Icon.draw_round_segment(
        (x1 + dx * fs, y_row1 + dy * fs),
        (x1 + dx * fs, y_row2 + dy * fs),
        width_units=mortar_w,
        color=Icon.WHITE,
    )

# Re-stroke outer dark contour cleanly over brick mortar endpoints
outer_pts = [
    (x0, y0),
    (x1, y0),
    (x1 + dx, y0 + dy),
    (x1 + dx, y1 + dy),
    (x0 + dx, y1 + dy),
    (x0, y1),
]
Icon.draw_round_polyline(outer_pts, width_units=1.8, color=Cisco.BORDER, closed=True)

# Inspection ring + passing/deflected arrows + inner shield on upper front face
cx = 42.0
cy = 48.0
circle((cx, cy), radius=12.8, style=Icon.stroke_style(Icon.WHITE, width_units=2.4))

Cisco.draw_arrow((19.0, cy + 5.8), (65.0, cy + 5.8), shaft_w=2.4, head_len=5.0, head_w=6.5, color=Icon.WHITE)
Cisco.draw_arrow((65.0, cy - 5.8), (19.0, cy - 5.8), shaft_w=2.4, head_len=5.0, head_w=6.5, color=Icon.WHITE)

left_sh = Icon.build_shield_half_points(cx, cy - 4.2, cy + 4.2, 3.6, side="left")
right_sh = Icon.build_shield_half_points(cx, cy - 4.2, cy + 4.2, 3.6, side="right")
polygon(left_sh + list(reversed(right_sh[1:-1])), style=Icon.no_border_fill(Icon.WHITE))

save()
