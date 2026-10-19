# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Business concept icon: approval_workflow."""

from drawlib.canvas import save
from drawlib.shapes import circle, rectangle
from drawlib.utils import Icon

Icon.setup()
w_outer, w_inner = 2.0, 1.6

# 1. Connecting vertical spine
Icon.draw_round_segment((34.0, 74.0), (34.0, 26.0), width_units=w_outer, color=Icon.DARK)

# 2. Step 1 (top, PASTEL_BLUE_LIGHT)
rectangle(
    (46.0, 74.0),
    width=56.0,
    height=16.0,
    style=Icon.fill_style(Icon.PASTEL_BLUE_LIGHT, border_color=Icon.DARK, border_units=w_outer, shape_r=4.0),
)
circle((26.0, 74.0), radius=3.5, style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w_inner))
Icon.draw_round_segment((35.0, 74.0), (64.0, 74.0), width_units=w_inner, color=Icon.DARK)

# 3. Step 2 (middle, PASTEL_BLUE)
rectangle(
    (46.0, 50.0),
    width=56.0,
    height=16.0,
    style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=w_outer, shape_r=4.0),
)
circle((26.0, 50.0), radius=3.5, style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w_inner))
Icon.draw_round_segment((35.0, 50.0), (64.0, 50.0), width_units=w_inner, color=Icon.WHITE)

# 4. Step 3 (bottom, WHITE card + PASTEL_GREEN approved check badge)
rectangle(
    (42.0, 26.0),
    width=48.0,
    height=16.0,
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w_outer, shape_r=4.0),
)
Icon.draw_round_segment((26.0, 26.0), (54.0, 26.0), width_units=w_inner, color=Icon.DARK)
circle(
    (74.0, 26.0), radius=13.5, style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=w_outer)
)
Icon.draw_round_polyline([(68.0, 26.0), (72.5, 21.5), (80.5, 31.0)], width_units=w_outer, color=Icon.DARK)
save()
