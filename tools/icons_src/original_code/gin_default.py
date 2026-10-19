# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Code icon: gin."""

import math

from drawlib.canvas import save
from drawlib.shapes import circle, ellipse, polygon
from drawlib.utils import Icon

Icon.setup()

s = 40.0 / 41.0
w_outer = 2.0
w_inner = 1.4
w_detail = 1.2

GOPHER_BLUE = "#4A9EE9"
LIQUID_TOP = "#5AD4F3"
SUBMERGED_TEAL = "#4CA6C8"
LEMON_YELLOW = "#F2D351"
LEMON_RIND = "#F2C138"
MUZZLE_GOLD = "#F1C349"
GLASS_AIR = "#EDF8FC"


def _sc(pts: list[tuple[float, float]]) -> list[tuple[float, float]]:
    return [(50.0 + (x - 50.0) * s, 50.0 + (y - 50.0) * s) for x, y in pts]


def _sc_pt(pt_xy: tuple[float, float]) -> tuple[float, float]:
    return (50.0 + (pt_xy[0] - 50.0) * s, 50.0 + (pt_xy[1] - 50.0) * s)


def _bezier(
    p0: tuple[float, float],
    p1: tuple[float, float],
    p2: tuple[float, float],
    p3: tuple[float, float],
    steps: int = 24,
) -> list[tuple[float, float]]:
    pts: list[tuple[float, float]] = []
    for i in range(steps + 1):
        t = i / steps
        mt = 1.0 - t
        bx = (mt**3) * p0[0] + 3 * (mt**2) * t * p1[0] + 3 * mt * (t**2) * p2[0] + (t**3) * p3[0]
        by = (mt**3) * p0[1] + 3 * (mt**2) * t * p1[1] + 3 * mt * (t**2) * p2[1] + (t**3) * p3[1]
        pts.append((bx, by))
    return pts


def _arc_pts(
    cx: float,
    cy: float,
    rx: float,
    ry: float,
    a0_deg: float,
    a1_deg: float,
    steps: int = 28,
) -> list[tuple[float, float]]:
    pts: list[tuple[float, float]] = []
    for i in range(steps + 1):
        ang = math.radians(a0_deg + (a1_deg - a0_deg) * (i / steps))
        pts.append((cx + rx * math.cos(ang), cy + ry * math.sin(ang)))
    return pts


# 1. Tumbler Glass Body (upper air region + lower Gopher liquid)
glass_bottom = _bezier((33.5, 12.6), (41.0, 8.2), (61.0, 8.2), (72.5, 12.8), steps=28)
glass_right_wall = [(72.5, 12.8), (79.0, 72.2)]
glass_top_back = _arc_pts(50.0, 72.8, 29.0, 3.8, 0.0, 180.0, steps=28)
glass_left_wall = [(21.0, 72.2), (33.5, 12.6)]

glass_air_poly = _sc([*glass_bottom, *glass_right_wall, *glass_top_back[1:-1], *glass_left_wall])
polygon(glass_air_poly, style=Icon.no_border_fill(GLASS_AIR))

# Liquid body inside glass (up to y ~ 62.5)
liquid_left_top = (23.2, 61.8)
liquid_right_top = (77.8, 61.5)
liquid_front_curve = _bezier(liquid_right_top, (63.0, 59.2), (38.0, 59.2), liquid_left_top, steps=24)
liquid_back_curve = _bezier(liquid_left_top, (36.0, 64.8), (64.0, 64.8), liquid_right_top, steps=24)

liquid_body_poly = _sc(
    [*glass_bottom, (72.5, 12.8), liquid_right_top, *liquid_front_curve[1:-1], liquid_left_top, (33.5, 12.6)]
)
polygon(liquid_body_poly, style=Icon.no_border_fill(GOPHER_BLUE))

liquid_surface_poly = _sc([*liquid_back_curve, *liquid_front_curve[1:-1]])
polygon(liquid_surface_poly, style=Icon.no_border_fill(LIQUID_TOP))

# 2. Submerged Lemon Wedge Shadow inside the Liquid
submerged_lemon = _sc(
    [
        (40.2, 60.4),
        *_bezier((40.2, 60.4), (36.5, 51.0), (54.0, 44.5), (68.0, 50.0), steps=18)[1:],
        *_bezier((68.0, 50.0), (74.5, 53.2), (77.0, 57.5), (77.5, 61.5), steps=12)[1:],
        *_bezier((77.5, 61.5), (65.0, 59.5), (50.0, 59.5), (40.2, 60.4), steps=14)[1:],
    ]
)
polygon(submerged_lemon, style=Icon.no_border_fill(SUBMERGED_TEAL))

# 3. Lemon Slice Wedge Perched on Upper-Right Rim
lemon_tip = (68.2, 90.8)
lemon_left_cut = (40.2, 60.4)
lemon_right_rim = (77.5, 61.5)

lemon_rind_outer = _bezier(lemon_tip, (76.8, 86.2), (80.6, 74.2), lemon_right_rim, steps=24)
lemon_bottom_cut = _bezier(lemon_right_rim, (65.0, 59.5), (50.0, 59.5), lemon_left_cut, steps=16)
lemon_diag_edge = _bezier(lemon_left_cut, (50.8, 69.5), (60.8, 80.5), lemon_tip, steps=18)

lemon_full_poly = _sc([*lemon_rind_outer, *lemon_bottom_cut[1:], *lemon_diag_edge[1:-1]])
polygon(lemon_full_poly, style=Icon.no_border_fill(LEMON_RIND))

# Inner yellow pulp & white pith line
pith_outer = _bezier((67.3, 88.0), (74.2, 83.8), (77.2, 73.5), (74.8, 61.6), steps=20)
pulp_bottom = _bezier((74.8, 61.6), (64.0, 60.2), (51.0, 60.2), (42.5, 60.8), steps=14)
pulp_diag = _bezier((42.5, 60.8), (52.0, 69.5), (60.5, 79.2), (67.3, 88.0), steps=14)
lemon_pulp_poly = _sc([*pith_outer, *pulp_bottom[1:], *pulp_diag[1:-1]])
polygon(lemon_pulp_poly, style=Icon.no_border_fill(LEMON_YELLOW))

Icon.draw_round_polyline(_sc(pith_outer), width_units=1.35, color=Icon.WHITE, closed=False)
Icon.draw_round_polyline(_sc(pulp_diag), width_units=1.25, color=Icon.WHITE, closed=False)

# Lemon segment spokes in WHITE
lemon_hub = _sc_pt((57.8, 72.2))
for seg_end in [(72.2, 79.5), (74.5, 70.5), (69.5, 62.5)]:
    Icon.draw_round_segment(lemon_hub, _sc_pt(seg_end), width_units=1.25, color=Icon.WHITE)

# Outline of lemon wedge
Icon.draw_round_polyline(
    _sc([*lemon_diag_edge, *lemon_rind_outer[1:]]),
    width_units=w_outer,
    color=Icon.DARK,
    closed=False,
)
Icon.draw_round_polyline(_sc(lemon_bottom_cut), width_units=w_inner, color=Icon.DARK, closed=False)

# 4. Liquid Surface & Glass Rim Outlines
Icon.draw_round_polyline(
    _sc(_bezier(liquid_left_top, (32.0, 64.2), (42.0, 64.5), (47.5, 64.2), steps=14)),
    width_units=w_inner,
    color=Icon.DARK,
    closed=False,
)
Icon.draw_round_polyline(_sc(liquid_front_curve), width_units=w_inner, color=Icon.DARK, closed=False)

# Glass top rim front curve & left back curve
glass_rim_front = _arc_pts(50.0, 72.8, 29.0, 3.8, 180.0, 355.0, steps=28)
glass_rim_back_left = _arc_pts(50.0, 72.8, 29.0, 3.8, 63.0, 180.0, steps=20)
Icon.draw_round_polyline(_sc(glass_rim_back_left), width_units=w_outer, color=Icon.DARK, closed=False)
Icon.draw_round_polyline(_sc(glass_rim_front), width_units=w_outer, color=Icon.DARK, closed=False)

# Glass outer walls & bottom outline
glass_outer_u = _sc([(21.0, 72.2), (33.5, 12.6), *glass_bottom[1:], (79.0, 72.2)])
Icon.draw_round_polyline(glass_outer_u, width_units=w_outer, color=Icon.DARK, closed=False)

# 5. Gopher Face on the Glass Front
# Left eye
left_eye_c = _sc_pt((43.7, 34.9))
ellipse(
    left_eye_c,
    width=11.6 * s,
    height=10.4 * s,
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w_inner),
)
circle(_sc_pt((40.4, 34.6)), radius=2.15 * s, style=Icon.no_border_fill(Icon.DARK))
circle(_sc_pt((41.2, 35.4)), radius=0.55 * s, style=Icon.no_border_fill(Icon.WHITE))

# Right eye
right_eye_c = _sc_pt((60.0, 35.6))
ellipse(
    right_eye_c,
    width=11.7 * s,
    height=10.4 * s,
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w_inner),
)
circle(_sc_pt((56.7, 35.3)), radius=2.15 * s, style=Icon.no_border_fill(Icon.DARK))
circle(_sc_pt((57.6, 36.0)), radius=0.55 * s, style=Icon.no_border_fill(Icon.WHITE))

# Gopher teeth (drawn just behind the upper muzzle lip)
for tx in (51.0, 53.5):
    tooth_pts = _sc(
        [
            (tx - 1.1, 27.0),
            (tx - 1.1, 22.4),
            (tx - 0.6, 21.7),
            (tx + 0.6, 21.7),
            (tx + 1.1, 22.4),
            (tx + 1.1, 27.0),
        ]
    )
    polygon(tooth_pts, style=Icon.no_border_fill(Icon.WHITE))
    Icon.draw_round_polyline(tooth_pts, width_units=w_detail, color=Icon.DARK, closed=True)

# Gopher muzzle / snout
muzzle_c = _sc_pt((52.25, 27.1))
ellipse(
    muzzle_c,
    width=10.2 * s,
    height=4.3 * s,
    style=Icon.fill_style(MUZZLE_GOLD, border_color=Icon.DARK, border_units=w_inner),
)

# Gopher nose tip
nose_c = _sc_pt((52.25, 28.7))
ellipse(nose_c, width=5.6 * s, height=2.5 * s, style=Icon.no_border_fill(Icon.DARK))

# Subtle glass shine highlight on lower-left wall
Icon.draw_round_segment(_sc_pt((27.8, 46.0)), _sc_pt((31.2, 26.5)), width_units=1.2, color=Icon.WHITE)
Icon.draw_round_segment(_sc_pt((32.0, 22.0)), _sc_pt((33.2, 16.5)), width_units=1.2, color=Icon.WHITE)

save()
