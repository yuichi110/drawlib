# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original DevOps concept icon: trivy."""

import math

from drawlib.canvas import save
from drawlib.shapes import circle, polygon
from drawlib.styles import Colors
from drawlib.utils import (
    DARK,
    draw_compound_polygon,
    draw_round_polyline,
    fill_style,
    no_border_fill,
    setup_icon,
)

setup_icon()

w_outer = 2.0
w_inner = 1.5
cx, cy = 50.0, 50.0


def _pill_pts(
    x1: float,
    y1: float,
    x2: float,
    y2: float,
    width: float,
    steps: int = 12,
) -> list[tuple[float, float]]:
    """Build a stadium/capsule polygon between (x1, y1) and (x2, y2)."""
    r = width / 2.0
    ang = math.atan2(y2 - y1, x2 - x1)
    pts: list[tuple[float, float]] = []
    for i in range(steps + 1):
        a = ang - math.pi / 2.0 + math.pi * (i / steps)
        pts.append((x2 + r * math.cos(a), y2 + r * math.sin(a)))
    for i in range(steps + 1):
        a = ang + math.pi / 2.0 + math.pi * (i / steps)
        pts.append((x1 + r * math.cos(a), y1 + r * math.sin(a)))
    return pts


def _hex_pt(radius: float, deg: float) -> tuple[float, float]:
    rad = math.radians(deg)
    return (cx + radius * math.cos(rad), cy + radius * math.sin(rad))


# 1. Outer hexagon vertices (pointy-top, radius 40.0)
r_out = 40.0
outer_hex = [_hex_pt(r_out, deg) for deg in (90.0, 30.0, -30.0, -90.0, -150.0, 150.0)]

# 2. Inner cutout contour (hexagon interior minus 3 inward spokes at 150, 30, -90 deg)
# Frame wall thickness = 3.2 -> inner hex radius = 40.0 - 3.2 / cos(30) = 36.3
r_in = 36.3
r_stop = 9.8
spoke_r = 1.55  # spoke half-width


def _inward_spoke_detour(deg_corner: float) -> list[tuple[float, float]]:
    """Trace from corner-(spoke_r) inward to r_stop cap and back out to corner+(spoke_r)."""
    rad = math.radians(deg_corner)
    ux, uy = math.cos(rad), math.sin(rad)
    # Normal pointing CCW around hexagon center
    nx, ny = -uy, ux
    # Distance from center along spoke where spoke edges meet inner hex edges
    # Inner hex edges at deg_corner meet at 60 deg to the spoke centerline
    d_root = r_in - spoke_r / math.tan(math.radians(60.0))
    p_enter = (cx + d_root * ux - spoke_r * nx, cy + d_root * uy - spoke_r * ny)
    p_tip_c = (cx + r_stop * ux, cy + r_stop * uy)
    p_exit = (cx + d_root * ux + spoke_r * nx, cy + d_root * uy + spoke_r * ny)

    # Semicircular cap around p_tip_c from angle (deg_corner - 90) to (deg_corner - 270)
    cap_pts: list[tuple[float, float]] = []
    steps = 12
    for i in range(steps + 1):
        a = math.radians(deg_corner - 90.0 - 180.0 * (i / steps))
        cap_pts.append((p_tip_c[0] + spoke_r * math.cos(a), p_tip_c[1] + spoke_r * math.sin(a)))
    return [p_enter, *cap_pts, p_exit]


# Build unified inner cutout ring (CCW order: 90 -> 150(spoke) -> 210 -> 270(spoke) -> 330 -> 30(spoke))
inner_cutout: list[tuple[float, float]] = [
    _hex_pt(r_in, 90.0),
    *_inward_spoke_detour(150.0),
    _hex_pt(r_in, 210.0),
    *_inward_spoke_detour(270.0),
    _hex_pt(r_in, 330.0),
    *_inward_spoke_detour(30.0),
]

draw_compound_polygon([outer_hex, inner_cutout], color=Colors.Gray6)
draw_round_polyline(outer_hex, width_units=w_outer, color=DARK, closed=True)
draw_round_polyline(inner_cutout, width_units=w_inner, color=DARK, closed=True)

# 3. Bottom-left spoke (210 deg) in Colors.Blue3
p_bl_in = _hex_pt(r_stop, 210.0)
p_bl_out = _hex_pt(r_in - 1.8, 210.0)
bl_pill = _pill_pts(p_bl_in[0], p_bl_in[1], p_bl_out[0], p_bl_out[1], width=3.1)
polygon(bl_pill, style=no_border_fill(Colors.Blue3))
draw_round_polyline(bl_pill, width_units=w_inner, color=DARK, closed=True)

# 4. Bottom-right spoke (330 deg) in Colors.Amber2
p_br_in = _hex_pt(r_stop, 330.0)
p_br_out = _hex_pt(r_in - 1.8, 330.0)
br_pill = _pill_pts(p_br_in[0], p_br_in[1], p_br_out[0], p_br_out[1], width=3.1)
polygon(br_pill, style=no_border_fill(Colors.Amber2))
draw_round_polyline(br_pill, width_units=w_inner, color=DARK, closed=True)

# 5. Top vertical spoke + top-right sector cyan ribs (Colors.Teal2)
# Unified branched polygon for top vertical spoke + 3 parallel ribs at -30 deg
ux_r = math.cos(math.radians(-30.0))
uy_r = math.sin(math.radians(-30.0))
nx_r, ny_r = -uy_r, ux_r  # upward-right normal to -30 deg ray
rw = 1.4  # rib half-width


def _rib_tip_cap(x_root: float, y_root: float, length: float) -> list[tuple[float, float]]:
    """Trace out along -30 deg rib of given length, around rounded tip, and back to x=51.4."""
    tcx = x_root + length * ux_r
    tcy = y_root + length * uy_r
    pts: list[tuple[float, float]] = []
    steps = 10
    for i in range(steps + 1):
        a = math.radians(60.0 - 180.0 * (i / steps))
        pts.append((tcx + rw * math.cos(a), tcy + rw * math.sin(a)))
    return pts


# Vertical spoke goes from y=59.8 to y=84.8, centered at x=50.0 (half-width 1.4)
cyan_branch: list[tuple[float, float]] = []
# Bottom cap at (50.0, 59.8)
for i in range(11):
    a = math.radians(180.0 + 180.0 * (i / 10))
    cyan_branch.append((50.0 + rw * math.cos(a), 59.8 + rw * math.sin(a)))

# Right side of vertical spoke up to Rib 3 (y_center at x=50 is 71.2)
# Line of bottom/top of rib at -30 deg: y - y0 = tan(-30) * (x - 50)
t30 = math.tan(math.radians(-30.0))
v_sec = rw / math.cos(math.radians(30.0))  # vertical offset of rib half-width (1.616)

# Rib 3 (lowest, y0=71.2, length=5.8)
y3_bot = 71.2 + t30 * (51.4 - 50.0) - v_sec
cyan_branch.append((51.4, y3_bot))
cyan_branch.extend(reversed(_rib_tip_cap(50.0, 71.2, 5.8)))
y3_top = 71.2 + t30 * (51.4 - 50.0) + v_sec
cyan_branch.append((51.4, y3_top))

# Rib 2 (middle, y0=77.8, length=13.5)
y2_bot = 77.8 + t30 * (51.4 - 50.0) - v_sec
cyan_branch.append((51.4, y2_bot))
cyan_branch.extend(reversed(_rib_tip_cap(50.0, 77.8, 13.5)))
y2_top = 77.8 + t30 * (51.4 - 50.0) + v_sec
cyan_branch.append((51.4, y2_top))

# Rib 1 (top, y0=84.4, length=24.2)
y1_bot = 84.4 + t30 * (51.4 - 50.0) - v_sec
cyan_branch.append((51.4, y1_bot))
cyan_branch.extend(reversed(_rib_tip_cap(50.0, 84.4, 24.2)))

# Top rounded corner at (50.0, 84.4)
for i in range(9):
    a = math.radians(60.0 + 120.0 * (i / 8))
    cyan_branch.append((50.0 + rw * math.cos(a), 84.4 + rw * math.sin(a)))

polygon(cyan_branch, style=no_border_fill(Colors.Teal2))
draw_round_polyline(cyan_branch, width_units=w_inner, color=DARK, closed=True)

# Detached cyan dot on Rib 2 line (y0=77.8, d=18.8)
dot_cx = 50.0 + 18.8 * ux_r
dot_cy = 77.8 + 18.8 * uy_r
circle(
    (dot_cx, dot_cy),
    radius=1.6,
    style=fill_style(Colors.Teal2, border_color=DARK, border_units=w_inner),
)

# Detached cyan short pill on Rib 3 line (y0=71.2, d from 10.2 to 13.5)
p3_a = (50.0 + 10.2 * ux_r, 71.2 + 10.2 * uy_r)
p3_b = (50.0 + 13.5 * ux_r, 71.2 + 13.5 * uy_r)
short_pill = _pill_pts(p3_a[0], p3_a[1], p3_b[0], p3_b[1], width=2.8)
polygon(short_pill, style=no_border_fill(Colors.Teal2))
draw_round_polyline(short_pill, width_units=w_inner, color=DARK, closed=True)

# 6. Center circle (Colors.Red3)
circle(
    (cx, cy),
    radius=4.8,
    style=fill_style(Colors.Red3, border_color=DARK, border_units=w_inner),
)

save()
