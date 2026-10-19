# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Network concept icon: zerotier."""

from drawlib.canvas import save
from drawlib.shapes import circle, rectangle
from drawlib.styles import Colors
from drawlib.utils import Icon

Icon.setup()

w = 2.0
w_glyph = 2.2
s = 80.0 / 82.0


def _sc(x: float, y: float) -> tuple[float, float]:
    return (50.0 + (x - 50.0) * s, 50.0 + (y - 50.0) * s)


# 1. Pastel yellow-orange rounded square badge
rectangle(
    (50.0, 50.0),
    width=80.0,
    height=80.0,
    style=Icon.fill_style(Colors.Orange3, border_color=Icon.DARK, border_units=w, shape_r=8.0),
)

# 2. Inner circle glyph
c_xy = _sc(50.0, 49.54)
c_r = 20.955 * s
circle(c_xy, radius=c_r, style=Icon.stroke_style(Icon.DARK, width_units=w_glyph))

# 3. Inner T-crossbar and vertical stem
t_left = _sc(18.11, 79.61)
t_right = _sc(81.89, 79.61)
stem_top = _sc(50.0, 79.61)
stem_bot = _sc(50.0, 17.20)

Icon.draw_round_segment(t_left, t_right, width_units=w_glyph, color=Icon.DARK)
Icon.draw_round_segment(stem_bot, stem_top, width_units=w_glyph, color=Icon.DARK)

save()
