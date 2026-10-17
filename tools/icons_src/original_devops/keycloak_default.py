# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original DevOps concept icon: keycloak."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.styles import Colors
from drawlib.utils import (
    DARK,
    draw_round_polyline,
    draw_round_segment,
    no_border_fill,
    setup_icon,
)

setup_icon()

w = 1.9
w_inner = 1.6


def _s(x: float, y: float) -> tuple[float, float]:
    """Scale official 100x100 coords by 0.94 around (50, 50) for comfortable safe margins."""
    return (50.0 + (x - 50.0) * 0.94, 50.0 + (y - 50.0) * 0.94)


# 1. Hexagonal nut top and bottom bands (Colors.Gray5)
# Leaving the central diamond hole completely transparent
top_nut = [_s(19.7, 68.5), _s(30.3, 86.9), _s(73.0, 86.9), _s(83.6, 68.5)]
bot_nut = [_s(19.7, 31.5), _s(83.6, 31.5), _s(73.0, 13.1), _s(30.3, 13.1)]

polygon(top_nut, style=no_border_fill(Colors.Gray5))
polygon(bot_nut, style=no_border_fill(Colors.Gray5))

# 2. Middle left and right nut plates (Colors.Gray3)
# Left plate ends at the left chevron's outer edge; right plate starts at right chevron's outer edge
mid_left = [
    _s(9.0, 50.0),
    _s(19.7, 68.5),
    _s(33.9, 68.5),
    _s(23.2, 50.0),
    _s(33.9, 31.5),
    _s(19.7, 31.5),
]
mid_right = [
    _s(69.5, 68.5),
    _s(91.0, 68.5),
    _s(91.0, 31.5),
    _s(69.5, 31.5),
    _s(80.1, 50.0),
]

polygon(mid_left, style=no_border_fill(Colors.Gray3))
polygon(mid_right, style=no_border_fill(Colors.Gray3))

# Subtle horizontal midline crease on left and right nut plates
draw_round_segment(_s(9.0, 50.0), _s(23.2, 50.0), width_units=w_inner, color=DARK)
draw_round_segment(_s(80.1, 50.0), _s(91.0, 50.0), width_units=w_inner, color=DARK)

# Outline nut plates
draw_round_polyline(top_nut, width_units=w, color=DARK, closed=True)
draw_round_polyline(bot_nut, width_units=w, color=DARK, closed=True)
draw_round_polyline(mid_left, width_units=w, color=DARK, closed=True)
draw_round_polyline(mid_right, width_units=w, color=DARK, closed=True)

# 3. Left interlocking chevron '<' (Colors.Blue3 outer ribbon + Colors.Blue2 inner facets)
left_chev_outer = [
    _s(23.2, 50.0),
    _s(37.45, 74.63),
    _s(44.55, 74.63),
    _s(30.34, 50.0),
    _s(44.55, 25.37),
    _s(37.45, 25.37),
]
left_chev_top_in = [
    _s(30.34, 50.0),
    _s(44.55, 74.63),
    _s(48.11, 68.5),
    _s(37.45, 50.0),
]
left_chev_bot_in = [
    _s(30.34, 50.0),
    _s(37.45, 50.0),
    _s(48.11, 31.5),
    _s(44.55, 25.37),
]

polygon(left_chev_outer, style=no_border_fill(Colors.Blue3))
polygon(left_chev_top_in, style=no_border_fill(Colors.Blue2))
polygon(left_chev_bot_in, style=no_border_fill(Colors.Blue2))

left_chev_full = [
    _s(23.2, 50.0),
    _s(37.45, 74.63),
    _s(44.55, 74.63),
    _s(48.11, 68.5),
    _s(37.45, 50.0),
    _s(48.11, 31.5),
    _s(44.55, 25.37),
    _s(37.45, 25.37),
]
draw_round_polyline(left_chev_full, width_units=w, color=DARK, closed=True)
draw_round_polyline(
    [_s(44.55, 74.63), _s(30.34, 50.0), _s(44.55, 25.37)],
    width_units=w_inner,
    color=DARK,
)
draw_round_segment(_s(30.34, 50.0), _s(37.45, 50.0), width_units=w_inner, color=DARK)

# 4. Right interlocking chevron '>' (Colors.Blue2 outer ribbon + Colors.Blue3 inner facets)
right_chev_outer = [
    _s(80.13, 50.0),
    _s(65.89, 74.63),
    _s(58.79, 74.63),
    _s(73.01, 50.0),
    _s(58.79, 25.37),
    _s(65.89, 25.37),
]
right_chev_top_in = [
    _s(73.01, 50.0),
    _s(58.79, 74.63),
    _s(55.25, 68.5),
    _s(65.91, 50.0),
]
right_chev_bot_in = [
    _s(73.01, 50.0),
    _s(65.91, 50.0),
    _s(55.25, 31.5),
    _s(58.79, 25.37),
]

polygon(right_chev_outer, style=no_border_fill(Colors.Blue2))
polygon(right_chev_top_in, style=no_border_fill(Colors.Blue3))
polygon(right_chev_bot_in, style=no_border_fill(Colors.Blue3))

right_chev_full = [
    _s(80.13, 50.0),
    _s(65.89, 74.63),
    _s(58.79, 74.63),
    _s(55.25, 68.5),
    _s(65.91, 50.0),
    _s(55.25, 31.5),
    _s(58.79, 25.37),
    _s(65.89, 25.37),
]
draw_round_polyline(right_chev_full, width_units=w, color=DARK, closed=True)
draw_round_polyline(
    [_s(58.79, 74.63), _s(73.01, 50.0), _s(58.79, 25.37)],
    width_units=w_inner,
    color=DARK,
)
draw_round_segment(_s(65.91, 50.0), _s(73.01, 50.0), width_units=w_inner, color=DARK)

save()
