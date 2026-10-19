# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Facility concept icon: security_gate."""

from drawlib.canvas import save
from drawlib.shapes import arc, circle, rectangle
from drawlib.styles import Colors
from drawlib.utils import Gcp, Icon

Icon.setup()

w_outer = 2.0
w_inner = 1.6

# 1. Left main gate pillar (x=14..34, y=18..76)
rectangle(
    (24.0, 47.0),
    width=20.0,
    height=58.0,
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w_outer, shape_r=4.0),
)
# Left pillar top cap (PASTEL_BLUE)
Gcp.draw_rounded_corner_block(
    14.0,
    66.0,
    34.0,
    76.0,
    r=4.0,
    round_tl=True,
    round_tr=True,
    color=Icon.PASTEL_BLUE,
)
rectangle(
    (24.0, 47.0),
    width=20.0,
    height=58.0,
    style=Icon.fill_style(Colors.Transparent, border_color=Icon.DARK, border_units=w_outer, shape_r=4.0),
)
Icon.draw_round_segment((14.0, 66.0), (34.0, 66.0), width_units=w_inner, color=Icon.DARK)

# Left pillar base plate
rectangle(
    (24.0, 16.5),
    width=24.0,
    height=4.5,
    style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=w_outer, shape_r=1.5),
)

# 2. Badge sensor on left pillar (x=18..30, y=38..56)
rectangle(
    (24.0, 47.0),
    width=12.0,
    height=18.0,
    style=Icon.fill_style(Icon.PASTEL_BLUE_LIGHT, border_color=Icon.DARK, border_units=w_inner, shape_r=2.0),
)
circle(
    (24.0, 51.0),
    radius=2.8,
    style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=w_inner),
)
Icon.draw_round_segment((21.0, 43.0), (27.0, 43.0), width_units=w_inner, color=Icon.DARK)

# Wireless RFID waves above left pillar
for rad in (5.0, 8.8):
    arc(
        (24.0, 77.5),
        width=rad * 2.0,
        height=rad * 2.0,
        angle_start=45.0,
        angle_end=135.0,
        style=Icon.stroke_style(Icon.DARK, width_units=w_inner),
    )

# 3. Right catch pillar (x=72..86, y=18..64)
rectangle(
    (79.0, 41.0),
    width=14.0,
    height=46.0,
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w_outer, shape_r=3.5),
)
Gcp.draw_rounded_corner_block(
    72.0,
    55.0,
    86.0,
    64.0,
    r=3.5,
    round_tl=True,
    round_tr=True,
    color=Icon.PASTEL_BLUE,
)
rectangle(
    (79.0, 41.0),
    width=14.0,
    height=46.0,
    style=Icon.fill_style(Colors.Transparent, border_color=Icon.DARK, border_units=w_outer, shape_r=3.5),
)
Icon.draw_round_segment((72.0, 55.0), (86.0, 55.0), width_units=w_inner, color=Icon.DARK)

# Right pillar base plate & latch catch
rectangle(
    (79.0, 16.5),
    width=18.0,
    height=4.5,
    style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=w_outer, shape_r=1.5),
)
rectangle(
    (70.5, 40.0),
    width=3.5,
    height=8.0,
    style=Icon.fill_style(Icon.PASTEL_BLUE_LIGHT, border_color=Icon.DARK, border_units=w_inner, shape_r=1.0),
)

# 4. PASTEL_GREEN swing barrier wing (x=34..69, y=26..54)
for hy in (32.0, 48.0):
    rectangle(
        (35.0, hy),
        width=4.0,
        height=4.5,
        style=Icon.fill_style(Icon.PASTEL_BLUE_LIGHT, border_color=Icon.DARK, border_units=w_inner),
    )

rectangle(
    (52.0, 40.0),
    width=34.0,
    height=26.0,
    style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=w_outer, shape_r=4.0),
)

# Inner WHITE pass/stop emblem on barrier
circle(
    (52.0, 40.0),
    radius=7.5,
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w_inner),
)
Icon.draw_round_segment((48.0, 40.0), (56.0, 40.0), width_units=2.0, color=Icon.DARK)

save()
