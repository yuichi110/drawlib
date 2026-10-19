# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Cisco network topology icon: client PC (default classic 3D variant)."""

from drawlib.canvas import save
from drawlib.shapes import circle, polygon, rectangle
from drawlib.utils import Cisco, Icon

Icon.setup()

# ------------------------------------------------------------------------------
# 1. Desktop System Unit Chassis (middle tier)
# ------------------------------------------------------------------------------
Cisco.draw_3d_box(12.0, 23.0, 62.0, 14.0, 14.0, 11.0)

# Floppy / optical drive slot and status LED on front face of system unit
Icon.draw_round_segment((53.0, 30.0), (68.0, 30.0), width_units=2.3, color=Icon.WHITE)
circle((19.0, 30.0), radius=1.6, style=Icon.no_border_fill(Icon.WHITE))

# ------------------------------------------------------------------------------
# 2. 3D Monitor sitting on top of the Desktop System Unit
# ------------------------------------------------------------------------------
Cisco.draw_3d_box(22.0, 41.0, 42.0, 34.0, 12.0, 10.0)

# Rounded CRT / LCD screen bezel on monitor front face
rectangle(
    (43.0, 58.0),
    width=32.5,
    height=24.0,
    style=Icon.fill_style(Cisco.BLUE, border_color=Icon.WHITE, border_units=1.8, shape_r=3.5),
)

# ------------------------------------------------------------------------------
# 3. Angled 3D Keyboard in front of Desktop System Unit
# ------------------------------------------------------------------------------
kb_front = [(15.0, 12.0), (67.0, 12.0), (67.0, 15.5), (15.0, 15.5)]
kb_top = [(15.0, 15.5), (67.0, 15.5), (75.0, 22.5), (23.0, 22.5)]
kb_side = [(67.0, 12.0), (75.0, 19.0), (75.0, 22.5), (67.0, 15.5)]

polygon(kb_front, style=Icon.no_border_fill(Cisco.BLUE))
polygon(kb_top, style=Icon.no_border_fill(Cisco.LIGHT_BLUE))
polygon(kb_side, style=Icon.no_border_fill(Cisco.DARK_BLUE))

# White internal seams on keyboard
Icon.draw_round_segment((15.0, 15.5), (67.0, 15.5), width_units=1.4, color=Icon.WHITE)
Icon.draw_round_segment((67.0, 12.0), (67.0, 15.5), width_units=1.4, color=Icon.WHITE)
Icon.draw_round_segment((67.0, 15.5), (75.0, 22.5), width_units=1.4, color=Icon.WHITE)

# Subtle white keycap rows on keyboard top
Icon.draw_round_segment((20.5, 17.8), (68.0, 17.8), width_units=1.2, color=Icon.WHITE)
Icon.draw_round_segment((23.0, 20.0), (70.5, 20.0), width_units=1.2, color=Icon.WHITE)

# Dark outer contour of keyboard
kb_outer = [
    (15.0, 12.0),
    (67.0, 12.0),
    (75.0, 19.0),
    (75.0, 22.5),
    (23.0, 22.5),
    (15.0, 15.5),
]
Icon.draw_round_polyline(kb_outer, width_units=1.8, color=Cisco.BORDER, closed=True)

save()
