# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Cisco modern 2D icon: web_security (modern variant)."""

import math

from drawlib.canvas import save
from drawlib.shapes import circle, ellipse, polygon
from drawlib.utils import (
    CISCO_BLUE,
    WHITE,
    build_shield_half_points,
    draw_cisco_modern_badge,
    draw_round_segment,
    no_border_fill,
    setup_icon,
    stroke_style,
)

setup_icon()
draw_cisco_modern_badge()

# Wireframe globe inside badge
g_cx, g_cy = 45.5, 53.0
g_r = 21.5
gw = 2.5

circle((g_cx, g_cy), radius=g_r, style=stroke_style(WHITE, width_units=gw))
ellipse((g_cx, g_cy), width=20.5, height=g_r * 2.0, style=stroke_style(WHITE, width_units=gw))
draw_round_segment((g_cx, g_cy - g_r), (g_cx, g_cy + g_r), width_units=gw, color=WHITE)
draw_round_segment((g_cx - g_r, g_cy), (g_cx + g_r, g_cy), width_units=gw, color=WHITE)

for dy_lat in (-9.5, 9.5):
    dx_lat = math.sqrt(g_r * g_r - dy_lat * dy_lat)
    draw_round_segment(
        (g_cx - dx_lat, g_cy + dy_lat),
        (g_cx + dx_lat, g_cy + dy_lat),
        width_units=gw,
        color=WHITE,
    )

# Protective security shield overlapping lower-right (inspired by Arch_63_Web Security.png)
sh_cx = 60.5
sh_bot = 24.5
sh_top = 56.5
sh_hw = 13.5

# Blue halo behind shield to mask wireframe lines cleanly
halo_l = build_shield_half_points(sh_cx, sh_bot - 2.5, sh_top + 2.5, sh_hw + 2.5, side="left")
halo_r = build_shield_half_points(sh_cx, sh_bot - 2.5, sh_top + 2.5, sh_hw + 2.5, side="right")
polygon(halo_l + list(reversed(halo_r[1:-1])), style=no_border_fill(CISCO_BLUE))

# White outer shield
outer_l = build_shield_half_points(sh_cx, sh_bot, sh_top, sh_hw, side="left")
outer_r = build_shield_half_points(sh_cx, sh_bot, sh_top, sh_hw, side="right")
polygon(outer_l + list(reversed(outer_r[1:-1])), style=no_border_fill(WHITE))

# Blue inner shield cutout + white diagonal guard slash (matching SAFE Web Security icon)
inner_l = build_shield_half_points(sh_cx, sh_bot + 3.4, sh_top - 3.0, sh_hw - 3.3, side="left")
inner_r = build_shield_half_points(sh_cx, sh_bot + 3.4, sh_top - 3.0, sh_hw - 3.3, side="right")
polygon(inner_l + list(reversed(inner_r[1:-1])), style=no_border_fill(CISCO_BLUE))

draw_round_segment((53.5, 35.0), (67.5, 49.0), width_units=3.0, color=WHITE)

save()
