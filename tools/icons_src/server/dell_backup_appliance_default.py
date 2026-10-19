# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Server icon: dell_backup_appliance_default."""

from drawlib.canvas import save
from drawlib.shapes import arc, ellipse, polygon, rectangle
from drawlib.styles import Colors
from drawlib.utils import Dell, Icon

Icon.setup()

# Left storage cylinder (outer cx=46.0, width=62.0 -> centerline width=57.2, outer y=12..88)
cx_cyl = 46.0
w_cyl = 57.2
rx_cyl = w_cyl / 2.0
ry_cyl = 8.5
cy_top = 77.1
cy_mid = 50.0
cy_bot = 22.9

# Cylinder top ellipse
ellipse(
    (cx_cyl, cy_top),
    width=w_cyl,
    height=ry_cyl * 2.0,
    style=Icon.fill_style(Colors.Transparent, border_color=Dell.BLUE, border_units=4.8),
)

# Cylinder left and right vertical walls with flat ends (smooth C1 join at bottom-left, crisp flat cut on right)
rectangle(
    (cx_cyl - rx_cyl, (cy_bot - 0.3 + cy_top + 0.3) / 2.0),
    width=4.8,
    height=(cy_top + 0.3) - (cy_bot - 0.3),
    style=Icon.no_border_fill(Dell.BLUE),
)
rectangle(
    (cx_cyl + rx_cyl, (55.5 + cy_top + 0.3) / 2.0),
    width=4.8,
    height=(cy_top + 0.3) - 55.5,
    style=Icon.no_border_fill(Dell.BLUE),
)

# Cylinder horizontal waist curves (middle and bottom, stopping cleanly left of the shield)
st_stroke = Icon.stroke_style(Dell.BLUE, width_units=4.8)
for cy_arc in (cy_mid, cy_bot):
    arc(
        (cx_cyl, cy_arc),
        width=w_cyl,
        height=ry_cyl * 2.0,
        angle_start=180.0,
        angle_end=260.0,
        style=st_stroke,
    )

# Foreground heraldic protection shield (outer cx=68.0, width=33.0 -> centerline half_w=14.1, outer y=12..50)
cx_sh = 68.0
hw_sh = 14.1
y_peak = 47.6
y_shldr = 42.1
y_waist = 31.0
y_tip = 14.4

# Left curved side from waist (53.9, 31.0) down to tip (68.0, 14.4)
left_curve: list[tuple[float, float]] = []
p0_l = (cx_sh - hw_sh, y_waist)
p1_l = (cx_sh - hw_sh, 23.6)
p2_l = (cx_sh - 9.2, 17.1)
p3_l = (cx_sh, y_tip)
for i in range(25):
    t = i / 24.0
    mt = 1.0 - t
    bx = (mt**3) * p0_l[0] + 3 * (mt**2) * t * p1_l[0] + 3 * mt * (t**2) * p2_l[0] + (t**3) * p3_l[0]
    by = (mt**3) * p0_l[1] + 3 * (mt**2) * t * p1_l[1] + 3 * mt * (t**2) * p2_l[1] + (t**3) * p3_l[1]
    left_curve.append((bx, by))

# Right curved side from tip (68.0, 14.4) up to waist (82.1, 31.0)
right_curve: list[tuple[float, float]] = []
for bx, by in reversed(left_curve[:-1]):
    right_curve.append((2.0 * cx_sh - bx, by))

shield_pts = [
    (cx_sh, y_peak),
    (cx_sh - hw_sh, y_shldr),
    *left_curve,
    *right_curve,
    (cx_sh + hw_sh, y_shldr),
]
polygon(
    shield_pts,
    style=Icon.fill_style(Colors.Transparent, border_color=Dell.BLUE, border_units=4.8, shape_r=0.8),
)

save()
