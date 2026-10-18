# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Security concept icon: ddos_protection."""

import math

from drawlib.canvas import save
from drawlib.shapes import circle, polygon
from drawlib.utils import (
    DARK,
    PASTEL_BLUE,
    PASTEL_BLUE_LIGHT,
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

# 1. Right-side split heraldic shield
cx = 62.0
y_bot, y_top = 16.0, 84.0
half_w = 23.0

left_pts = build_shield_half_points(cx, y_bot, y_top, half_w, side="left")
right_pts = build_shield_half_points(cx, y_bot, y_top, half_w, side="right")
full_outline = left_pts + list(reversed(right_pts[1:-1]))

polygon(left_pts, style=no_border_fill(PASTEL_BLUE))
polygon(right_pts, style=no_border_fill(PASTEL_BLUE_LIGHT))
draw_round_segment((cx, y_bot), (cx, y_top), width_units=w_shape, color=DARK)
draw_round_polyline(full_outline, width_units=w_shape, color=DARK, closed=True)

# 2. Center PASTEL_GREEN badge with WHITE checkmark
badge_cy = 51.5
circle(
    (cx, badge_cy),
    radius=9.5,
    style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=w_shape),
)
draw_round_polyline(
    [(58.0, 51.3), (61.0, 48.3), (66.2, 54.7)],
    width_units=2.0,
    color=WHITE,
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
    draw_round_polyline([p1, tip, p2], width_units=w_line, color=DARK)


# 3. Left-side incoming and bouncing attack arrows
top_hit = (34.5, 62.0)
top_tip = (19.0, 79.0)
draw_round_polyline([(11.0, 62.0), top_hit, top_tip], width_units=w_line, color=DARK)
_draw_arrow_head(top_tip, top_hit)

mid_tip = (31.0, 50.0)
draw_round_segment((10.0, 50.0), mid_tip, width_units=w_line, color=DARK)
_draw_arrow_head(mid_tip, (10.0, 50.0))

bot_hit = (35.5, 38.0)
bot_tip = (19.0, 21.0)
draw_round_polyline([(11.0, 38.0), bot_hit, bot_tip], width_units=w_line, color=DARK)
_draw_arrow_head(bot_tip, bot_hit)

save()
