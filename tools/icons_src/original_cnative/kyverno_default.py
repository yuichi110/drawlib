# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Cloud Native concept icon: kyverno."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import (
    DARK,
    ORIG_STROKE,
    PASTEL_BLUE,
    PASTEL_GREEN,
    WHITE,
    build_shield_half_points,
    draw_round_polyline,
    fill_style,
    no_border_fill,
    setup_icon,
)

setup_icon()

w = ORIG_STROKE
cx = 50.0

# 1. Outer protective shield (PASTEL_BLUE)
outer_left = build_shield_half_points(cx, 12.0, 86.0, 34.0, side="left")
outer_right = build_shield_half_points(cx, 12.0, 86.0, 34.0, side="right")
outer_outline = outer_left + list(reversed(outer_right[1:-1]))
polygon(outer_outline, style=no_border_fill(PASTEL_BLUE))
draw_round_polyline(outer_outline, width_units=w, color=DARK, closed=True)

# 2. Inner protective shield (WHITE)
inner_left = build_shield_half_points(cx, 21.0, 77.5, 24.5, side="left")
inner_right = build_shield_half_points(cx, 21.0, 77.5, 24.5, side="right")
inner_outline = inner_left + list(reversed(inner_right[1:-1]))
polygon(inner_outline, style=no_border_fill(WHITE))
draw_round_polyline(inner_outline, width_units=2.0, color=DARK, closed=True)

# 3. Central PASTEL_GREEN diamond policy badge
cy_badge = 51.5
r_badge = 14.0
diamond_pts = [
    (cx, cy_badge + r_badge),
    (cx + r_badge, cy_badge),
    (cx, cy_badge - r_badge),
    (cx - r_badge, cy_badge),
]
polygon(
    diamond_pts,
    style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=2.0, shape_r=2.5),
)

# 4. Crisp DARK checkmark inside the diamond
draw_round_polyline(
    [(44.2, 51.0), (48.4, 46.8), (56.2, 55.4)],
    width_units=2.0,
    color=DARK,
)

save()
