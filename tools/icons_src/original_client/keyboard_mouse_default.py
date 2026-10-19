# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Client concept icon: keyboard_mouse."""

from drawlib.canvas import save
from drawlib.shapes import rectangle
from drawlib.utils import Icon

Icon.setup()

w = Icon.ORIG_STROKE

# 1. Compact wireless keyboard frame (PASTEL_BLUE)
rectangle(
    (38.0, 50.0),
    width=52.0,
    height=42.0,
    style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=w, shape_r=6.5),
)

# 2. Keyboard top and middle key rows (WHITE)
for ky in (61.0, 50.5):
    for kx in (19.6, 28.8, 38.0, 47.2, 56.4):
        rectangle(
            (kx, ky),
            width=6.8,
            height=6.8,
            style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=1.8, shape_r=1.6),
        )

# 3. Keyboard bottom row with spacebar (WHITE)
rectangle(
    (20.5, 39.5),
    width=8.6,
    height=6.8,
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=1.8, shape_r=1.6),
)
rectangle(
    (38.0, 39.5),
    width=22.0,
    height=6.8,
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=1.8, shape_r=1.6),
)
rectangle(
    (55.5, 39.5),
    width=8.6,
    height=6.8,
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=1.8, shape_r=1.6),
)

# 4. Wireless mouse body on right (WHITE)
rectangle(
    (79.5, 49.0),
    width=18.0,
    height=38.0,
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w, shape_r=9.0),
)

# Mouse button seam lines
Icon.draw_round_segment((70.8, 53.0), (88.2, 53.0), width_units=2.0, color=Icon.DARK)
Icon.draw_round_segment((79.5, 53.0), (79.5, 67.5), width_units=2.0, color=Icon.DARK)

# 5. Mouse scroll wheel (PASTEL_GREEN)
rectangle(
    (79.5, 59.0),
    width=4.8,
    height=8.5,
    style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=1.8, shape_r=2.4),
)

save()
