# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original concept icon: ids_ips."""

import math

from drawlib.canvas import save
from drawlib.shapes import circle, polygon
from drawlib.utils import Cisco, Icon

Icon.setup()

w = Icon.ORIG_STROKE

# 1. Bidirectional traffic arrows passing through the central shield
# Top arrow: left -> right (--- | shield | -->)
Cisco.draw_arrow(
    (12.0, 61.0),
    (88.0, 61.0),
    shaft_w=3.4,
    head_len=7.0,
    head_w=9.2,
    color=Icon.DARK,
)
# Bottom arrow: right -> left (<-- | shield | ---)
Cisco.draw_arrow(
    (88.0, 39.0),
    (12.0, 39.0),
    shaft_w=3.4,
    head_len=7.0,
    head_w=9.2,
    color=Icon.DARK,
)

# 2. Central PASTEL_BLUE heraldic shield (matching original_cloud firewall/ddos_protection)
cx = 50.0
y_bot, y_top = 18.0, 82.0
half_w = 21.5

left_pts = Icon.build_shield_half_points(cx, y_bot, y_top, half_w, side="left")
right_pts = Icon.build_shield_half_points(cx, y_bot, y_top, half_w, side="right")
full_outline = left_pts + list(reversed(right_pts[1:-1]))

polygon(full_outline, style=Icon.no_border_fill(Icon.PASTEL_BLUE))
Icon.draw_round_polyline(full_outline, width_units=w, color=Icon.DARK, closed=True)

# 3. Bold almond eye inside the shield (WHITE sclera + PASTEL_GREEN iris + DARK pupil)
ey = 52.5
eye_a = 13.5
eye_b = 7.8
arc_r = (eye_a * eye_a + eye_b * eye_b) / (2.0 * eye_b)
half_ang = math.asin(eye_a / arc_r)
steps = 24

eye_pts: list[tuple[float, float]] = []
yc_top = ey - (arc_r - eye_b)
for i in range(steps + 1):
    ang = (math.pi / 2.0 + half_ang) - (2.0 * half_ang) * (i / steps)
    eye_pts.append((cx + arc_r * math.cos(ang), yc_top + arc_r * math.sin(ang)))
yc_bot = ey + (arc_r - eye_b)
for i in range(1, steps):
    ang = (-math.pi / 2.0 + half_ang) - (2.0 * half_ang) * (i / steps)
    eye_pts.append((cx + arc_r * math.cos(ang), yc_bot + arc_r * math.sin(ang)))

polygon(eye_pts, style=Icon.no_border_fill(Icon.WHITE))
Icon.draw_round_polyline(eye_pts, width_units=2.0, color=Icon.DARK, closed=True)

circle((cx, ey), radius=5.0, style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=2.0))
circle((cx, ey), radius=2.1, style=Icon.fill_style(Icon.DARK))

save()
