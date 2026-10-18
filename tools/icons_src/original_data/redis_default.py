# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Data concept icon: redis."""

import math

from drawlib.canvas import save
from drawlib.shapes import ellipse, polygon
from drawlib.styles import Colors
from drawlib.utils import (
    DARK,
    WHITE,
    draw_round_polyline,
    draw_round_segment,
    fill_style,
    no_border_fill,
    setup_icon,
)


def _rounded_diamond_half(
    cx: float,
    cy: float,
    rx: float,
    ry: float,
    r_corner: float,
) -> tuple[list[tuple[float, float]], list[tuple[float, float]]]:
    """Build smooth top-half and bottom-half points for an isometric rounded diamond."""
    frac_x = r_corner / rx
    frac_y = r_corner / ry

    def _quad(
        p0: tuple[float, float],
        p1: tuple[float, float],
        p2: tuple[float, float],
        n: int = 10,
    ) -> list[tuple[float, float]]:
        return [
            (
                ((1 - t) ** 2) * p0[0] + 2 * (1 - t) * t * p1[0] + (t**2) * p2[0],
                ((1 - t) ** 2) * p0[1] + 2 * (1 - t) * t * p1[1] + (t**2) * p2[1],
            )
            for t in (i / n for i in range(n + 1))
        ]

    l_bot = (cx - rx * (1.0 - frac_x), cy - ry * frac_x)
    l_tip = (cx - rx, cy)
    l_top = (cx - rx * (1.0 - frac_x), cy + ry * frac_x)

    t_left = (cx - rx * frac_y, cy + ry * (1.0 - frac_y))
    t_tip = (cx, cy + ry)
    t_right = (cx + rx * frac_y, cy + ry * (1.0 - frac_y))

    r_top = (cx + rx * (1.0 - frac_x), cy + ry * frac_x)
    r_tip = (cx + rx, cy)
    r_bot = (cx + rx * (1.0 - frac_x), cy - ry * frac_x)

    b_right = (cx + rx * frac_y, cy - ry * (1.0 - frac_y))
    b_tip = (cx, cy - ry)
    b_left = (cx - rx * frac_y, cy - ry * (1.0 - frac_y))

    left_curve = _quad(l_bot, l_tip, l_top, 10)
    top_curve = _quad(t_left, t_tip, t_right, 12)
    right_curve = _quad(r_top, r_tip, r_bot, 10)
    bot_curve = _quad(b_right, b_tip, b_left, 12)

    mid_l = len(left_curve) // 2
    mid_r = len(right_curve) // 2

    top_half = [*left_curve[mid_l:], *top_curve, *right_curve[: mid_r + 1]]
    bot_half = [*right_curve[mid_r:], *bot_curve, *left_curve[: mid_l + 1]]
    return top_half, bot_half


def _draw_platter(cx: float, cy: float, rx: float, ry: float, th: float, r_corner: float, w_border: float) -> None:
    """Draw one 3D isometric platter tier with vertical tangent side walls."""
    top_half, bot_half = _rounded_diamond_half(cx, cy, rx, ry, r_corner)
    bot_skirt = [(x, y - th) for x, y in bot_half]

    # Side skirt polygon using exact tangent endpoints bot_half[0] and bot_half[-1]
    skirt_pts = [*bot_half, *reversed(bot_skirt)]
    polygon(skirt_pts, style=no_border_fill(Colors.Red4))
    draw_round_polyline(
        [bot_half[0], *bot_skirt, bot_half[-1]],
        width_units=w_border,
        color=DARK,
    )

    # Top diamond polygon
    full_top = [*top_half, *bot_half[1:-1]]
    polygon(full_top, style=no_border_fill(Colors.Red3))
    draw_round_polyline(full_top, width_units=w_border, color=DARK, closed=True)


setup_icon()

w = 2.0
cx = 50.0
rx = 41.0
ry = 18.2
th = 9.0
r_corner = 5.5

# 1. Three stacked isometric platter tiers (bottom to top)
for cy_tier in (37.5, 53.0, 68.5):
    _draw_platter(cx, cy_tier, rx, ry, th, r_corner, w)

# 2. Four geometric tokens on the top platter (cy = 68.5)
# (a) Left: WHITE isometric circle/ellipse
ellipse(
    (34.5, 68.5),
    width=15.0,
    height=7.8,
    style=fill_style(WHITE, border_color=DARK, border_units=1.5),
)

# (b) Top: WHITE 5-point isometric star
star_cx, star_cy = 50.0, 76.2
star_pts: list[tuple[float, float]] = []
for i in range(10):
    ang = math.radians(90.0 + i * 36.0)
    r_s = 8.8 if i % 2 == 0 else 3.9
    star_pts.append((star_cx + r_s * math.cos(ang), star_cy + r_s * 0.54 * math.sin(ang)))
polygon(star_pts, style=no_border_fill(WHITE))
draw_round_polyline(star_pts, width_units=1.5, color=DARK, closed=True)

# (c) Bottom: WHITE triangle token
tri_pts = [
    (40.5, 61.5),
    (54.5, 63.8),
    (49.5, 56.8),
]
polygon(tri_pts, style=no_border_fill(WHITE))
draw_round_polyline(tri_pts, width_units=1.5, color=DARK, closed=True)

# (d) Right: Colors.Red2 / Colors.Red4 isometric diamond/cube recess
cube_cx, cube_cy = 65.5, 68.5
crx, cry = 9.2, 4.4
c_top = (cube_cx, cube_cy + cry)
c_right = (cube_cx + crx, cube_cy)
c_bot = (cube_cx, cube_cy - cry)
c_left = (cube_cx - crx, cube_cy)
polygon([c_top, c_right, c_bot, c_left], style=no_border_fill(Colors.Red2))
polygon([c_top, c_right, c_bot], style=no_border_fill(Colors.Red4))
draw_round_segment(c_top, c_bot, width_units=1.5, color=DARK)
draw_round_polyline([c_top, c_right, c_bot, c_left], width_units=1.5, color=DARK, closed=True)

save()
