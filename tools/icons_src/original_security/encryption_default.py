# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Security concept icon: encryption."""

import math

from drawlib.canvas import save
from drawlib.shapes import circle, rectangle
from drawlib.utils import Icon

Icon.setup()

w_shape = 2.0
w_line = 2.0

# 1. Left WHITE document card with 3 short horizontal text lines
rectangle(
    (26.0, 54.0),
    width=30.0,
    height=42.0,
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w_shape, shape_r=4.0),
)
Icon.draw_round_segment((17.0, 66.0), (35.0, 66.0), width_units=2.0, color=Icon.DARK)
Icon.draw_round_segment((17.0, 58.0), (35.0, 58.0), width_units=2.0, color=Icon.DARK)
Icon.draw_round_segment((17.0, 50.0), (29.0, 50.0), width_units=2.0, color=Icon.DARK)

# 2. Right PASTEL_BLUE cipher card with 2x3 grid of WHITE / DARK binary dots and dashes
rectangle(
    (74.0, 54.0),
    width=30.0,
    height=42.0,
    style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=w_shape, shape_r=4.0),
)
circle((67.5, 66.0), radius=2.4, style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w_shape))
Icon.draw_round_segment((74.0, 66.0), (81.0, 66.0), width_units=2.0, color=Icon.DARK)

Icon.draw_round_segment((66.0, 58.0), (73.0, 58.0), width_units=2.0, color=Icon.DARK)
circle((79.5, 58.0), radius=2.4, style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w_shape))

circle((67.5, 50.0), radius=2.4, style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w_shape))
Icon.draw_round_segment((74.0, 50.0), (81.0, 50.0), width_units=2.0, color=Icon.DARK)

# 3. Horizontal DARK arrow connecting left card to right card across the middle
Icon.draw_round_segment((41.8, 60.0), (58.0, 60.0), width_units=w_line, color=Icon.DARK)
Icon.draw_round_polyline(
    [(53.5, 64.0), (58.0, 60.0), (53.5, 56.0)],
    width_units=w_line,
    color=Icon.DARK,
)

# 4. Central overlapping PASTEL_GREEN padlock
shackle_cx, shackle_cy, shackle_r = 50.0, 45.5, 6.5
shackle_pts: list[tuple[float, float]] = [(shackle_cx - shackle_r, 42.0)]
for i in range(25):
    ang = math.radians(180.0 - 180.0 * (i / 24))
    shackle_pts.append(
        (
            shackle_cx + shackle_r * math.cos(ang),
            shackle_cy + shackle_r * math.sin(ang),
        )
    )
shackle_pts.append((shackle_cx + shackle_r, 42.0))
Icon.draw_round_polyline(shackle_pts, width_units=w_line, color=Icon.DARK)

rectangle(
    (50.0, 34.0),
    width=24.0,
    height=20.0,
    style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=w_shape, shape_r=4.0),
)
circle((50.0, 36.0), radius=2.3, style=Icon.fill_style(Icon.DARK))
Icon.draw_round_segment((50.0, 36.0), (50.0, 31.0), width_units=2.0, color=Icon.DARK)

save()
