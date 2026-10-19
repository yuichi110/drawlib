# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Cisco classic 3D icon: web_security (default variant)."""

import math

from drawlib.canvas import save
from drawlib.shapes import circle, ellipse, polygon
from drawlib.utils import Cisco, Icon

Icon.setup()

x0 = 12.0
y0 = 15.0
w_front = 60.0
h_front = 52.0
dx = 16.0
dy = 14.0

Cisco.draw_3d_box(x0, y0, w_front, h_front, dx, dy)

# Crisp wireframe globe on the left-center of the front face
g_cx, g_cy = 37.5, 42.5
g_r = 16.0
gw = 1.85

circle((g_cx, g_cy), radius=g_r, style=Icon.stroke_style(Icon.WHITE, width_units=gw))
ellipse((g_cx, g_cy), width=15.0, height=g_r * 2.0, style=Icon.stroke_style(Icon.WHITE, width_units=gw))
Icon.draw_round_segment((g_cx, g_cy - g_r), (g_cx, g_cy + g_r), width_units=gw, color=Icon.WHITE)
Icon.draw_round_segment((g_cx - g_r, g_cy), (g_cx + g_r, g_cy), width_units=gw, color=Icon.WHITE)

for dy_lat in (-7.2, 7.2):
    dx_lat = math.sqrt(g_r * g_r - dy_lat * dy_lat)
    Icon.draw_round_segment(
        (g_cx - dx_lat, g_cy + dy_lat),
        (g_cx + dx_lat, g_cy + dy_lat),
        width_units=gw,
        color=Icon.WHITE,
    )

# Protective shield emblem overlapping bottom-right of globe
sh_cx = 54.5
sh_bot = 21.5
sh_top = 46.5
sh_hw = 10.5

# Blue halo behind shield to mask wireframe globe lines
halo_l = Icon.build_shield_half_points(sh_cx, sh_bot - 2.0, sh_top + 2.0, sh_hw + 2.0, side="left")
halo_r = Icon.build_shield_half_points(sh_cx, sh_bot - 2.0, sh_top + 2.0, sh_hw + 2.0, side="right")
polygon(halo_l + list(reversed(halo_r[1:-1])), style=Icon.no_border_fill(Cisco.BLUE))

# White outer shield
outer_l = Icon.build_shield_half_points(sh_cx, sh_bot, sh_top, sh_hw, side="left")
outer_r = Icon.build_shield_half_points(sh_cx, sh_bot, sh_top, sh_hw, side="right")
polygon(outer_l + list(reversed(outer_r[1:-1])), style=Icon.no_border_fill(Icon.WHITE))

# Dark blue inner shield recess + white checkmark
inner_l = Icon.build_shield_half_points(sh_cx, sh_bot + 2.8, sh_top - 2.4, sh_hw - 2.6, side="left")
inner_r = Icon.build_shield_half_points(sh_cx, sh_bot + 2.8, sh_top - 2.4, sh_hw - 2.6, side="right")
polygon(inner_l + list(reversed(inner_r[1:-1])), style=Icon.no_border_fill(Cisco.DARK_BLUE))

Icon.draw_round_polyline(
    [(50.4, 34.6), (53.4, 31.4), (59.0, 38.4)],
    width_units=2.1,
    color=Icon.WHITE,
)

save()
