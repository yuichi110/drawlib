# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""GCP icon: gke (Google Kubernetes Engine)."""

import math

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import GCP_TECH_LIGHT, GCP_TECH_MED_LIGHT, GCP_TECH_MID, fill_style, setup_icon

setup_icon()

cx, cy = 50.0, 50.0
r_out = 43.0
r_in = 34.4

angles_deg = [90.0, 30.0, -30.0, -90.0, -150.0, 150.0]
outer_pts = [(cx + r_out * math.cos(math.radians(a)), cy + r_out * math.sin(math.radians(a))) for a in angles_deg]
inner_pts = [(cx + r_in * math.cos(math.radians(a)), cy + r_in * math.sin(math.radians(a))) for a in angles_deg]

st_light = fill_style(GCP_TECH_LIGHT)

hex_ring_pts = outer_pts + [outer_pts[0], inner_pts[0]] + list(reversed(inner_pts[1:])) + [inner_pts[0]]
polygon(hex_ring_pts, style=st_light)

dx_top = 18.6
dy_top = dx_top * math.tan(math.radians(30.0))
y_top_btm = 52.3
y_top_peak = y_top_btm + 2.0 * dy_top
spoke_hw = 2.15
y_spoke_join = y_top_peak - spoke_hw * math.tan(math.radians(30.0))
top_piece_pts = [
    (cx, y_top_btm),
    (cx - dx_top, y_top_btm + dy_top),
    (cx - spoke_hw, y_spoke_join),
    (cx - spoke_hw, 88.0),
    (cx + spoke_hw, 88.0),
    (cx + spoke_hw, y_spoke_join),
    (cx + dx_top, y_top_btm + dy_top),
]
polygon(top_piece_pts, style=st_light)

x_hex_l, y_hex_bl = inner_pts[4]
spoke_h = 4.9
x_face_l = 30.2
x_face_in_l = 47.9
y_spoke_top_at_face = y_hex_bl + spoke_h + (x_face_l - x_hex_l) * math.tan(math.radians(30.0))
x_junc_l = 32.4
y_junc_l = y_hex_bl + (x_junc_l - x_hex_l) * math.tan(math.radians(30.0))
y_face_btm_in = y_junc_l - (x_face_in_l - x_junc_l) * math.tan(math.radians(30.0))
y_face_top_l = 59.6
y_face_top_in = y_face_top_l - (x_face_in_l - x_face_l) * math.tan(math.radians(30.0))

left_pts = [
    (x_hex_l, y_hex_bl),
    (x_hex_l, y_hex_bl + spoke_h),
    (x_face_l, y_spoke_top_at_face),
    (x_face_l, y_face_top_l),
    (x_face_in_l, y_face_top_in),
    (x_face_in_l, y_face_btm_in),
    (x_junc_l, y_junc_l),
]
polygon(left_pts, style=fill_style(GCP_TECH_MED_LIGHT))

right_pts = [(100.0 - x, y) for (x, y) in left_pts]
polygon(right_pts, style=fill_style(GCP_TECH_MID))

save()
