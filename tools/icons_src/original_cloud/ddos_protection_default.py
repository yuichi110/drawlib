# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original concept icon: ddos_protection."""

import math

from drawlib.canvas import save
from drawlib.shapes import circle, polygon
from drawlib.utils import (
    DARK,
    ORIG_STROKE,
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

w = ORIG_STROKE

# Right-side heraldic shield (left edge at x = 62 - 22 = 40.0)
cx = 62.0
y_bot, y_top = 18.0, 82.0
half_w = 22.0

left_pts = build_shield_half_points(cx, y_bot, y_top, half_w, side="left")
right_pts = build_shield_half_points(cx, y_bot, y_top, half_w, side="right")
full_outline = left_pts + list(reversed(right_pts[1:-1]))

polygon(full_outline, style=no_border_fill(PASTEL_BLUE))
draw_round_polyline(full_outline, width_units=w, color=DARK, closed=True)

circle(
    (cx, 51.0),
    radius=9.5,
    style=fill_style(WHITE, border_color=DARK, border_units=2.2),
)
circle(
    (cx, 51.0),
    radius=4.0,
    style=fill_style(PASTEL_GREEN),
)


def _draw_arrow_head(
    tip: tuple[float, float],
    from_pt: tuple[float, float],
    *,
    head_len: float = 7.2,
    head_angle_deg: float = 36.0,
) -> None:
    """Draw a rounded open arrowhead at `tip` oriented along `from_pt -> tip`."""
    ang = math.atan2(tip[1] - from_pt[1], tip[0] - from_pt[0])
    a1 = ang + math.radians(180.0 - head_angle_deg)
    a2 = ang - math.radians(180.0 - head_angle_deg)
    p1 = (tip[0] + head_len * math.cos(a1), tip[1] + head_len * math.sin(a1))
    p2 = (tip[0] + head_len * math.cos(a2), tip[1] + head_len * math.sin(a2))
    draw_round_polyline([p1, tip, p2], width_units=w, color=DARK)


# 1. Top attack arrow hitting shield and bouncing up-left
top_hit = (35.5, 62.0)
top_tip = (20.0, 79.0)
draw_round_polyline([(12.0, 62.0), top_hit, top_tip], width_units=w, color=DARK)
_draw_arrow_head(top_tip, top_hit)

# 2. Middle incoming attack arrow approaching shield
mid_tip = (32.0, 50.0)
draw_round_segment((10.0, 50.0), mid_tip, width_units=w, color=DARK)
_draw_arrow_head(mid_tip, (10.0, 50.0))

# 3. Bottom attack arrow hitting shield and bouncing down-left
bot_hit = (36.5, 38.0)
bot_tip = (20.0, 21.0)
draw_round_polyline([(12.0, 38.0), bot_hit, bot_tip], width_units=w, color=DARK)
_draw_arrow_head(bot_tip, bot_hit)

save()
