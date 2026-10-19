# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Network concept icon: wireless_router."""

import math

from drawlib.canvas import save
from drawlib.shapes import arc, circle, rectangle
from drawlib.utils import Cisco, Icon

Icon.setup()

w = Icon.ORIG_STROKE

# Two vertical antennas
for ant_x in (30.0, 70.0):
    Icon.draw_round_segment((ant_x, 48.0), (ant_x, 78.0), width_units=3.2, color=Icon.DARK)

# Lower router chassis
rectangle(
    (50.0, 31.0),
    width=76.0,
    height=34.0,
    style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=w, shape_r=8.0),
)

# Inner WHITE panel
rectangle(
    (50.0, 31.0),
    width=62.0,
    height=22.0,
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=2.0, shape_r=4.5),
)

# 4 compact routing arrows (left/right inward, top/bottom outward)
Cisco.draw_arrow((28.5, 31.0), (44.0, 31.0), shaft_w=2.2, head_len=4.6, head_w=6.0, color=Icon.DARK)
Cisco.draw_arrow((71.5, 31.0), (56.0, 31.0), shaft_w=2.2, head_len=4.6, head_w=6.0, color=Icon.DARK)
Cisco.draw_arrow((50.0, 33.5), (50.0, 39.8), shaft_w=2.0, head_len=3.4, head_w=5.0, color=Icon.DARK)
Cisco.draw_arrow((50.0, 28.5), (50.0, 22.2), shaft_w=2.0, head_len=3.4, head_w=5.0, color=Icon.DARK)

# Small PASTEL_GREEN center dot inside panel
circle(
    (50.0, 31.0),
    radius=3.0,
    style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=1.8),
)

# PASTEL_GREEN antenna tips
for ant_x in (30.0, 70.0):
    circle(
        (ant_x, 79.0),
        radius=4.2,
        style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=2.0),
    )

# Radio wave arcs around antenna tips (y=72..86)
arc_w = 2.2
for ant_x in (30.0, 70.0):
    for diam in (18.0, 27.0):
        r = diam / 2.0
        for ang_start, ang_end in [(-32.0, 32.0), (148.0, 212.0)]:
            arc(
                (ant_x, 79.0),
                width=diam,
                height=diam,
                angle_start=ang_start,
                angle_end=ang_end,
                style=Icon.stroke_style(Icon.DARK, width_units=arc_w),
            )
            for ang_deg in (ang_start, ang_end):
                rad = math.radians(ang_deg)
                Icon.draw_cap(
                    (ant_x + r * math.cos(rad), 79.0 + r * math.sin(rad)),
                    width_units=arc_w,
                    color=Icon.DARK,
                )

save()
