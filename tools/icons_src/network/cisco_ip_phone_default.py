# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Cisco network topology icon: IP phone (default classic 3D variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import Cisco, Icon

Icon.setup()

# ------------------------------------------------------------------------------
# 1. 3D Angled VoIP Desk Phone Base (Wedge)
#    Slope along slanted top: dx = +14.0, dy = +42.0 (dx/dy = 1/3)
# ------------------------------------------------------------------------------
base_front = [(10.0, 16.0), (74.0, 16.0), (74.0, 26.0), (10.0, 26.0)]
base_top = [(10.0, 26.0), (74.0, 26.0), (88.0, 68.0), (24.0, 68.0)]
base_side = [(74.0, 16.0), (88.0, 46.0), (88.0, 68.0), (74.0, 26.0)]

polygon(base_front, style=Icon.no_border_fill(Cisco.BLUE))
polygon(base_top, style=Icon.no_border_fill(Cisco.LIGHT_BLUE))
polygon(base_side, style=Icon.no_border_fill(Cisco.DARK_BLUE))

# White internal seams on base
Icon.draw_round_segment((10.0, 26.0), (74.0, 26.0), width_units=1.6, color=Icon.WHITE)
Icon.draw_round_segment((74.0, 16.0), (74.0, 26.0), width_units=1.6, color=Icon.WHITE)
Icon.draw_round_segment((74.0, 26.0), (88.0, 68.0), width_units=1.6, color=Icon.WHITE)

# Dark outer contour of base
base_outer = [
    (10.0, 16.0),
    (74.0, 16.0),
    (88.0, 46.0),
    (88.0, 68.0),
    (24.0, 68.0),
    (10.0, 26.0),
]
Icon.draw_round_polyline(base_outer, width_units=1.8, color=Cisco.BORDER, closed=True)

# ------------------------------------------------------------------------------
# 2. Angled LCD Screen on Upper-Right of Slanted Top
# ------------------------------------------------------------------------------
lcd_bezel = [
    (44.0, 50.0),
    (76.0, 50.0),
    (80.5, 63.5),
    (48.5, 63.5),
]
polygon(lcd_bezel, style=Icon.no_border_fill(Icon.WHITE))

lcd_screen = [
    (47.2, 52.2),
    (74.4, 52.2),
    (77.4, 61.2),
    (50.2, 61.2),
]
polygon(lcd_screen, style=Icon.no_border_fill(Cisco.BLUE))

# ------------------------------------------------------------------------------
# 3. 3x4 Keypad Buttons on Lower-Right of Slanted Top
# ------------------------------------------------------------------------------
key_w = 5.8
key_h = 2.6
key_dx = key_h / 3.0

for row_idx in range(4):
    y_r = 43.8 - row_idx * 4.4
    row_shift = (y_r - 30.6) / 3.0
    for col_idx in range(3):
        x_c = 40.5 + col_idx * 9.0 + row_shift
        key_pts = [
            (x_c, y_r),
            (x_c + key_w, y_r),
            (x_c + key_w + key_dx, y_r + key_h),
            (x_c + key_dx, y_r + key_h),
        ]
        polygon(key_pts, style=Icon.no_border_fill(Icon.WHITE))

# ------------------------------------------------------------------------------
# 4. 3D Handset Resting on Left Side of Phone
# ------------------------------------------------------------------------------
hs_front = [(12.5, 27.0), (28.5, 27.0), (28.5, 36.5), (12.5, 36.5)]
hs_top = [(12.5, 36.5), (28.5, 36.5), (43.5, 81.5), (27.5, 81.5)]
hs_side = [(28.5, 27.0), (43.5, 72.0), (43.5, 81.5), (28.5, 36.5)]

polygon(hs_front, style=Icon.no_border_fill(Cisco.BLUE))
polygon(hs_top, style=Icon.no_border_fill(Cisco.LIGHT_BLUE))
polygon(hs_side, style=Icon.no_border_fill(Cisco.DARK_BLUE))

# White internal seams on handset
Icon.draw_round_segment((12.5, 36.5), (28.5, 36.5), width_units=1.5, color=Icon.WHITE)
Icon.draw_round_segment((28.5, 27.0), (28.5, 36.5), width_units=1.5, color=Icon.WHITE)
Icon.draw_round_segment((28.5, 36.5), (43.5, 81.5), width_units=1.5, color=Icon.WHITE)

# Dark outer contour of handset
hs_outer = [
    (12.5, 27.0),
    (28.5, 27.0),
    (43.5, 72.0),
    (43.5, 81.5),
    (27.5, 81.5),
    (12.5, 36.5),
]
Icon.draw_round_polyline(hs_outer, width_units=1.8, color=Cisco.BORDER, closed=True)

save()
