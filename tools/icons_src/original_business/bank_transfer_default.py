# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Business concept icon: bank_transfer."""

from drawlib.canvas import save
from drawlib.shapes import circle, polygon, rectangle
from drawlib.utils import Icon

Icon.setup()
w_outer, w_inner = 2.0, 1.6

# 1. Bank pediment roof (PASTEL_BLUE)
roof_pts = [(12.0, 64.0), (46.0, 86.0), (80.0, 64.0)]
polygon(roof_pts, style=Icon.no_border_fill(Icon.PASTEL_BLUE))
Icon.draw_round_polyline(roof_pts, width_units=w_outer, color=Icon.DARK, closed=True)
circle((46.0, 72.5), radius=4.0, style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w_inner))

# 2. Architrave and base plinth (PASTEL_BLUE_LIGHT)
rectangle(
    (46.0, 60.5),
    width=64.0,
    height=7.0,
    style=Icon.fill_style(Icon.PASTEL_BLUE_LIGHT, border_color=Icon.DARK, border_units=w_outer, shape_r=1.5),
)
rectangle(
    (46.0, 23.5),
    width=68.0,
    height=8.0,
    style=Icon.fill_style(Icon.PASTEL_BLUE_LIGHT, border_color=Icon.DARK, border_units=w_outer, shape_r=2.0),
)

# 3. Three columns (WHITE)
for cx in (24.0, 46.0, 68.0):
    rectangle(
        (cx, 42.0),
        width=10.0,
        height=30.0,
        style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w_outer),
    )

# 4. PASTEL_GREEN transfer arrows badge at bottom-right
circle(
    (75.0, 28.0), radius=14.5, style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=w_outer)
)
Icon.draw_round_segment((68.0, 32.0), (81.0, 32.0), width_units=w_inner, color=Icon.DARK)
Icon.draw_round_polyline([(77.0, 35.5), (81.5, 32.0), (77.0, 28.5)], width_units=w_inner, color=Icon.DARK)
Icon.draw_round_segment((82.0, 24.0), (69.0, 24.0), width_units=w_inner, color=Icon.DARK)
Icon.draw_round_polyline([(73.0, 27.5), (68.5, 24.0), (73.0, 20.5)], width_units=w_inner, color=Icon.DARK)
save()
