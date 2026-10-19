# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Cisco network icon: optical transport (classic 3D default variant)."""

from drawlib.canvas import save
from drawlib.shapes import circle
from drawlib.utils import Cisco, Icon

Icon.setup()

# 3D optical shelf box (x in [10, 88], y in [20, 78])
x0, y0 = 10.0, 20.0
w_front, h_front = 64.0, 44.0
dx, dy = 14.0, 14.0

Cisco.draw_3d_box(x0, y0, w_front, h_front, dx, dy)

# Top-face oblique transport arrows aligned with 45-degree depth slope
Cisco.draw_arrow(
    (25.0, 66.5),
    (35.0, 76.5),
    shaft_w=2.8,
    head_len=5.2,
    head_w=7.2,
    color=Icon.WHITE,
)
Cisco.draw_arrow(
    (49.0, 66.5),
    (59.0, 76.5),
    shaft_w=2.8,
    head_len=5.2,
    head_w=7.2,
    color=Icon.WHITE,
)

# Front-face optical ring + horizontal bidirectional wavelength arrows (center=(42.0, 42.0))
cx, cy = 42.0, 42.0
r_ring = 13.5

# Inner wavelength lines inside the optical ring
for y_wave in (46.5, 42.0, 37.5):
    Icon.draw_round_segment(
        (cx - 11.0, y_wave),
        (cx + 11.0, y_wave),
        width_units=1.6,
        color=Cisco.LIGHT_BLUE,
    )

# Optical ring on front face
circle(
    (cx, cy),
    radius=r_ring,
    style=Icon.fill_style("#00000000", border_color=Icon.WHITE, border_units=2.6),
)

# Bidirectional horizontal wavelength arrows flanking the optical ring
for y_arrow in (46.5, 37.5):
    Cisco.draw_arrow(
        (cx - 12.0, y_arrow),
        (14.5, y_arrow),
        shaft_w=3.0,
        head_len=5.8,
        head_w=7.6,
        color=Icon.WHITE,
    )
    Cisco.draw_arrow(
        (cx + 12.0, y_arrow),
        (69.5, y_arrow),
        shaft_w=3.0,
        head_len=5.8,
        head_w=7.6,
        color=Icon.WHITE,
    )

save()
