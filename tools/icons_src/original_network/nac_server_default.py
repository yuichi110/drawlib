# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Network concept icon: nac_server."""

import math

from drawlib.canvas import save
from drawlib.shapes import circle, polygon, rectangle
from drawlib.utils import Icon

Icon.setup()

w = Icon.ORIG_STROKE

# 1. Tall server appliance chassis
rectangle(
    (44.0, 50.0),
    width=54.0,
    height=76.0,
    style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=w, shape_r=8.0),
)

# 2. Upper WHITE identity badge panel
rectangle(
    (44.0, 58.0),
    width=40.0,
    height=42.0,
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=2.0, shape_r=5.0),
)

# 3. User avatar inside badge panel (head + shoulder dome)
circle(
    (44.0, 66.0),
    radius=7.0,
    style=Icon.fill_style(Icon.PASTEL_BLUE_LIGHT, border_color=Icon.DARK, border_units=2.0),
)

dome_pts = [
    (
        44.0 + 12.0 * math.cos(math.radians(deg)),
        44.0 + 11.0 * math.sin(math.radians(deg)),
    )
    for deg in range(0, 181, 6)
]
polygon(dome_pts, style=Icon.no_border_fill(Icon.PASTEL_BLUE_LIGHT))
Icon.draw_round_polyline(dome_pts, width_units=2.0, color=Icon.DARK, closed=True)

# 4. Lower server slot line
Icon.draw_round_segment((28.0, 24.0), (52.0, 24.0), width_units=2.0, color=Icon.DARK)

# 5. Foreground bottom-right verification badge circle
circle(
    (70.0, 30.0),
    radius=15.0,
    style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=w),
)
Icon.draw_round_polyline(
    [(63.5, 29.5), (68.5, 24.5), (77.0, 35.0)],
    width_units=3.2,
    color=Icon.DARK,
)

save()
