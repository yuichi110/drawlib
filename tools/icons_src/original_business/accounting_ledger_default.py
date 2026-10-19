# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Business concept icon: accounting_ledger."""

from drawlib.canvas import save
from drawlib.shapes import circle, rectangle
from drawlib.styles import Colors
from drawlib.utils import Gcp, Icon

Icon.setup()
w_outer, w_inner = 2.0, 1.6

# 1. Ledger book body (x=15..77, y=16..86)
rectangle((46.0, 51.0), width=62.0, height=70.0, style=Icon.no_border_fill(Icon.WHITE, shape_r=5.0))
Gcp.draw_rounded_corner_block(15.0, 16.0, 29.0, 86.0, r=5.0, round_tl=True, round_bl=True, color=Icon.PASTEL_BLUE)
Icon.draw_round_segment((29.0, 16.0), (29.0, 86.0), width_units=w_outer, color=Icon.DARK)
rectangle(
    (46.0, 51.0),
    width=62.0,
    height=70.0,
    style=Icon.fill_style(Colors.Transparent, border_color=Icon.DARK, border_units=w_outer, shape_r=5.0),
)

# 2. Ledger table grid lines
Icon.draw_round_segment((56.0, 28.0), (56.0, 76.0), width_units=w_inner, color=Icon.DARK)
for y_row in (70.0, 58.0, 46.0, 34.0):
    Icon.draw_round_segment((35.0, y_row), (69.0, y_row), width_units=w_inner, color=Icon.DARK)

# 3. PASTEL_GREEN coin badge at bottom-right
circle(
    (74.0, 27.0), radius=14.0, style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=w_outer)
)
circle((74.0, 27.0), radius=6.0, style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w_inner))
save()
