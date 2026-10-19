# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Facility concept icon: headquarters."""

from drawlib.canvas import save
from drawlib.shapes import rectangle
from drawlib.utils import Icon

Icon.setup()

w_outer = 2.0
w_inner = 1.6

# 1. Flanking lower side wings (PASTEL_BLUE_LIGHT)
for wing_x in (25.0, 75.0):
    rectangle(
        (wing_x, 33.0),
        width=16.0,
        height=38.0,
        style=Icon.fill_style(Icon.PASTEL_BLUE_LIGHT, border_color=Icon.DARK, border_units=w_outer, shape_r=2.0),
    )
    for wy in (44.0, 34.0, 24.0):
        Icon.draw_round_segment((wing_x - 3.2, wy), (wing_x + 3.2, wy), width_units=w_inner, color=Icon.DARK)

# 2. Central main glass tower (PASTEL_BLUE)
rectangle(
    (50.0, 44.5),
    width=36.0,
    height=61.0,
    style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=w_outer, shape_r=2.5),
)

# 3. Upper stepped crown tier (PASTEL_BLUE_LIGHT) + rooftop spire
rectangle(
    (50.0, 79.5),
    width=22.0,
    height=9.0,
    style=Icon.fill_style(Icon.PASTEL_BLUE_LIGHT, border_color=Icon.DARK, border_units=w_outer, shape_r=2.0),
)
Icon.draw_round_segment((50.0, 84.0), (50.0, 89.0), width_units=w_outer, color=Icon.DARK)

# 4. Crisp 3x4 WHITE window grid on the central skyscraper
for wx in (40.5, 50.0, 59.5):
    for wy in (66.5, 56.5, 46.5, 36.5):
        rectangle(
            (wx, wy),
            width=6.2,
            height=6.2,
            style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w_inner, shape_r=1.2),
        )

# 5. Grand lobby doorway at bottom center (WHITE)
rectangle(
    (50.0, 20.5),
    width=12.0,
    height=13.0,
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w_inner, shape_r=1.5),
)
Icon.draw_round_segment((50.0, 14.0), (50.0, 27.0), width_units=w_inner, color=Icon.DARK)

# 6. Ground baseline
Icon.draw_round_segment((13.0, 14.0), (87.0, 14.0), width_units=w_outer, color=Icon.DARK)

save()
