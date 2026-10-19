# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Business concept icon: cms."""

from drawlib.canvas import save
from drawlib.shapes import circle, rectangle
from drawlib.styles import Colors
from drawlib.utils import Gcp, Icon

Icon.setup()
w_outer, w_inner = 2.0, 1.6

# 1. Browser window (x=12..82, y=18..82)
rectangle((47.0, 50.0), width=70.0, height=64.0, style=Icon.no_border_fill(Icon.WHITE, shape_r=6.0))
Gcp.draw_rounded_corner_block(12.0, 68.0, 82.0, 82.0, r=6.0, round_tl=True, round_tr=True, color=Icon.PASTEL_BLUE)
Icon.draw_round_segment((12.0, 68.0), (82.0, 68.0), width_units=w_outer, color=Icon.DARK)
rectangle(
    (47.0, 50.0),
    width=70.0,
    height=64.0,
    style=Icon.fill_style(Colors.Transparent, border_color=Icon.DARK, border_units=w_outer, shape_r=6.0),
)
for dx in (20.0, 27.0):
    circle((dx, 75.0), radius=2.0, style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=1.2))

# 2. Modular CMS content blocks inside page
rectangle(
    (30.0, 51.0),
    width=22.0,
    height=20.0,
    style=Icon.fill_style(Icon.PASTEL_BLUE_LIGHT, border_color=Icon.DARK, border_units=w_inner, shape_r=2.5),
)
Icon.draw_round_segment((47.0, 58.0), (72.0, 58.0), width_units=w_inner, color=Icon.DARK)
Icon.draw_round_segment((47.0, 50.0), (68.0, 50.0), width_units=w_inner, color=Icon.DARK)
Icon.draw_round_segment((19.0, 34.0), (56.0, 34.0), width_units=w_inner, color=Icon.DARK)
Icon.draw_round_segment((19.0, 26.0), (48.0, 26.0), width_units=w_inner, color=Icon.DARK)

# 3. PASTEL_GREEN add-content badge at bottom-right
circle(
    (75.0, 27.0), radius=13.5, style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=w_outer)
)
Icon.draw_round_segment((69.0, 27.0), (81.0, 27.0), width_units=w_outer, color=Icon.DARK)
Icon.draw_round_segment((75.0, 21.0), (75.0, 33.0), width_units=w_outer, color=Icon.DARK)
save()
