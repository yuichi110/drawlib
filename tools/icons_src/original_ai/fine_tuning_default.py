# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original concept icon: fine_tuning."""

from drawlib.canvas import save
from drawlib.shapes import circle, polygon, rectangle
from drawlib.utils import Icon

Icon.setup()

w = Icon.ORIG_STROKE

# 1. Rounded parameter control card
rectangle(
    (48.0, 48.0),
    width=66.0,
    height=64.0,
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w, shape_r=9.0),
)

# 2. Three horizontal tuning slider tracks and knobs
sliders = [
    (64.0, 37.0, Icon.PASTEL_BLUE),
    (48.0, 58.0, Icon.PASTEL_GREEN),
    (32.0, 43.0, Icon.PASTEL_BLUE),
]
for sy, kx, kcol in sliders:
    Icon.draw_round_segment((25.0, sy), (70.0, sy), width_units=w, color=Icon.DARK)
    circle(
        (kx, sy),
        radius=6.2,
        style=Icon.fill_style(kcol, border_color=Icon.DARK, border_units=2.0),
    )

# 3. Top-right AI sparkle accent
sparkle_pts = Icon.build_sparkle_4pt_polygon(76.0, 76.0, outer_r=11.5, inner_r=4.0)
polygon(sparkle_pts, style=Icon.no_border_fill(Icon.PASTEL_GREEN))
Icon.draw_round_polyline(sparkle_pts, width_units=2.0, color=Icon.DARK, closed=True)

save()
