# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Facility concept icon: satellite_station."""

import math

from drawlib.canvas import save
from drawlib.shapes import circle, ellipse, polygon, rectangle
from drawlib.utils import Icon

Icon.setup()

w_outer = 2.0
w_inner = 1.6


def _arc_band_polygon(
    cx: float,
    cy: float,
    r_mid: float,
    thickness: float,
    ang_start_deg: float,
    ang_end_deg: float,
) -> list[tuple[float, float]]:
    r_in = r_mid - thickness / 2.0
    r_out = r_mid + thickness / 2.0
    half_t = thickness / 2.0
    pts: list[tuple[float, float]] = []
    steps_arc = 18
    steps_cap = 8
    for i in range(steps_arc + 1):
        ang = math.radians(ang_start_deg + (ang_end_deg - ang_start_deg) * (i / steps_arc))
        pts.append((cx + r_out * math.cos(ang), cy + r_out * math.sin(ang)))
    end_rad = math.radians(ang_end_deg)
    cap_end_cx = cx + r_mid * math.cos(end_rad)
    cap_end_cy = cy + r_mid * math.sin(end_rad)
    for i in range(1, steps_cap):
        ang = end_rad + math.pi * (i / steps_cap)
        pts.append((cap_end_cx + half_t * math.cos(ang), cap_end_cy + half_t * math.sin(ang)))
    for i in range(steps_arc + 1):
        ang = math.radians(ang_end_deg - (ang_end_deg - ang_start_deg) * (i / steps_arc))
        pts.append((cx + r_in * math.cos(ang), cy + r_in * math.sin(ang)))
    start_rad = math.radians(ang_start_deg)
    cap_start_cx = cx + r_mid * math.cos(start_rad)
    cap_start_cy = cy + r_mid * math.sin(start_rad)
    for i in range(1, steps_cap):
        ang = start_rad + math.pi + math.pi * (i / steps_cap)
        pts.append((cap_start_cx + half_t * math.cos(ang), cap_start_cy + half_t * math.sin(ang)))
    return pts


# 1. Ground pedestal pad and tapered mount tower
rectangle(
    (38.0, 14.5),
    width=36.0,
    height=5.0,
    style=Icon.fill_style(Icon.PASTEL_BLUE_LIGHT, border_color=Icon.DARK, border_units=w_outer, shape_r=2.5),
)
pedestal_pts = [
    (28.0, 17.0),
    (48.0, 17.0),
    (43.5, 39.0),
    (32.5, 39.0),
]
polygon(pedestal_pts, style=Icon.no_border_fill(Icon.PASTEL_BLUE))
Icon.draw_round_polyline(pedestal_pts, width_units=w_outer, color=Icon.DARK, closed=True)

# 2. Parabolic dish bowl (PASTEL_BLUE back shell) tilted at 45 degrees toward upper-right
rim_cx, rim_cy = 49.5, 51.5
dish_r = 22.5
bowl_pts: list[tuple[float, float]] = []
for i in range(33):
    ang = math.radians(135.0 + 180.0 * (i / 32))
    bowl_pts.append((rim_cx + dish_r * math.cos(ang), rim_cy + dish_r * math.sin(ang)))
polygon(bowl_pts, style=Icon.no_border_fill(Icon.PASTEL_BLUE))
Icon.draw_round_polyline(bowl_pts, width_units=w_outer, color=Icon.DARK, closed=True)

# 3. Dish inner reflector rim (WHITE tilted ellipse)
ellipse(
    (rim_cx, rim_cy),
    width=dish_r * 2.0,
    height=13.0,
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w_outer, angle=-45.0),
)

# 4. Feed horn struts anchored cleanly to the dish rim ends (135 deg and 315 deg)
feed_cx, feed_cy = 63.0, 65.0
rim_tl = (rim_cx + dish_r * math.cos(math.radians(135.0)), rim_cy + dish_r * math.sin(math.radians(135.0)))
rim_br = (rim_cx + dish_r * math.cos(math.radians(315.0)), rim_cy + dish_r * math.sin(math.radians(315.0)))
Icon.draw_round_segment((rim_cx, rim_cy), (feed_cx, feed_cy), width_units=w_outer, color=Icon.DARK)
Icon.draw_round_segment(rim_tl, (feed_cx, feed_cy), width_units=w_inner, color=Icon.DARK)
Icon.draw_round_segment(rim_br, (feed_cx, feed_cy), width_units=w_inner, color=Icon.DARK)
circle(
    (feed_cx, feed_cy),
    radius=4.2,
    style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=w_outer),
)

# 5. Skyward PASTEL_GREEN signal beam arcs toward upper-right
for r_mid, span in ((11.5, 28.0), (20.5, 30.0)):
    beam = _arc_band_polygon(feed_cx, feed_cy, r_mid, 3.8, 45.0 - span, 45.0 + span)
    polygon(beam, style=Icon.no_border_fill(Icon.PASTEL_GREEN))
    Icon.draw_round_polyline(beam, width_units=w_inner, color=Icon.DARK, closed=True)

save()
