# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Cisco network icon: optical transport (modern 2D variant)."""

from drawlib.canvas import save
from drawlib.shapes import circle, polygon
from drawlib.utils import Cisco, Icon

Icon.setup()
Cisco.draw_modern_badge()

cx, cy = 50.0, 50.0
r_ring = 17.5

# Parallel wavelength beams inside the optical ring
for y_beam in (56.5, 50.0, 43.5):
    Icon.draw_round_segment(
        (cx - 14.0, y_beam),
        (cx + 14.0, y_beam),
        width_units=1.8,
        color=Cisco.LIGHT_BLUE,
    )

# Subtle prism triangle inside the ring
polygon(
    [(cx, cy + 10.5), (cx - 9.5, cy - 7.5), (cx + 9.5, cy - 7.5)],
    style=Icon.fill_style("#00000000", border_color=Cisco.LIGHT_BLUE, border_units=1.8),
)

# Outer crisp white optical ring
circle(
    (cx, cy),
    radius=r_ring,
    style=Icon.fill_style("#00000000", border_color=Icon.WHITE, border_units=3.0),
)

# Bidirectional optical wavelength arrows on left and right
for y_arrow, dx_start, x_tip_l, x_tip_r in (
    (56.5, 15.8, 19.5, 80.5),
    (50.0, 17.0, 17.0, 83.0),
    (43.5, 15.8, 19.5, 80.5),
):
    Cisco.draw_arrow(
        (cx - dx_start, y_arrow),
        (x_tip_l, y_arrow),
        shaft_w=3.0,
        head_len=5.8,
        head_w=7.6,
        color=Icon.WHITE,
    )
    Cisco.draw_arrow(
        (cx + dx_start, y_arrow),
        (x_tip_r, y_arrow),
        shaft_w=3.0,
        head_len=5.8,
        head_w=7.6,
        color=Icon.WHITE,
    )

# Small center optical node dot
circle((cx, cy - 1.5), radius=2.6, style=Icon.no_border_fill(Icon.WHITE))
circle((cx, cy - 1.5), radius=1.0, style=Icon.no_border_fill(Cisco.BLUE))

save()
