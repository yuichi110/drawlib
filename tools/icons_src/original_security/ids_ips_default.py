# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Security concept icon: ids_ips."""

import math

from drawlib.canvas import save
from drawlib.shapes import circle, polygon
from drawlib.utils import (
    DARK,
    PASTEL_BLUE,
    PASTEL_GREEN,
    WHITE,
    build_shield_half_points,
    draw_round_polyline,
    draw_round_segment,
    fill_style,
    no_border_fill,
    setup_icon,
)

setup_icon()

w_shape = 2.0
w_line = 2.0


def _draw_arrow_head(
    tip: tuple[float, float],
    from_pt: tuple[float, float],
    *,
    head_len: float = 6.8,
    head_angle_deg: float = 36.0,
) -> None:
    """Draw a rounded open arrowhead at `tip` oriented along `from_pt -> tip`."""
    ang = math.atan2(tip[1] - from_pt[1], tip[0] - from_pt[0])
    a1 = ang + math.radians(180.0 - head_angle_deg)
    a2 = ang - math.radians(180.0 - head_angle_deg)
    p1 = (tip[0] + head_len * math.cos(a1), tip[1] + head_len * math.sin(a1))
    p2 = (tip[0] + head_len * math.cos(a2), tip[1] + head_len * math.sin(a2))
    draw_round_polyline([p1, tip, p2], width_units=w_line, color=DARK)


# 1. Three traffic arrows: top arrow bounced (IPS), middle & bottom passing through (IDS/IPS)
y_top_arrow = 66.0
y_mid_arrow = 50.0
y_bot_arrow = 34.0

# Top arrow: comes from left, hits shield left edge, bounces up-left
hit_pt = (29.0, y_top_arrow)
bounce_tip = (15.5, 80.5)
draw_round_polyline([(10.0, y_top_arrow), hit_pt, bounce_tip], width_units=w_line, color=DARK)
_draw_arrow_head(bounce_tip, hit_pt)

# Middle arrow: passes through shield left -> right
draw_round_segment((10.0, y_mid_arrow), (90.0, y_mid_arrow), width_units=w_line, color=DARK)
_draw_arrow_head((90.0, y_mid_arrow), (10.0, y_mid_arrow))

# Bottom arrow: passes through shield right -> left
draw_round_segment((90.0, y_bot_arrow), (10.0, y_bot_arrow), width_units=w_line, color=DARK)
_draw_arrow_head((10.0, y_bot_arrow), (90.0, y_bot_arrow))

# 2. Central PASTEL_BLUE heraldic shield
cx = 52.0
y_bot, y_top = 15.0, 85.0
half_w = 23.0

left_pts = build_shield_half_points(cx, y_bot, y_top, half_w, side="left")
right_pts = build_shield_half_points(cx, y_bot, y_top, half_w, side="right")
full_outline = left_pts + list(reversed(right_pts[1:-1]))

polygon(full_outline, style=no_border_fill(PASTEL_BLUE))
draw_round_polyline(full_outline, width_units=w_shape, color=DARK, closed=True)

# 3. Almond eye inside the central shield (WHITE sclera + PASTEL_GREEN iris + DARK pupil)
ey = 52.0
eye_a = 15.0
eye_b = 8.8
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

polygon(eye_pts, style=no_border_fill(WHITE))
draw_round_polyline(eye_pts, width_units=w_shape, color=DARK, closed=True)

circle(
    (cx, ey),
    radius=6.0,
    style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=w_shape),
)
circle((cx, ey), radius=2.4, style=fill_style(DARK))

save()
