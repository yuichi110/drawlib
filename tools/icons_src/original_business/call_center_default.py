# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Business concept icon: call_center."""

import math

from drawlib.canvas import save
from drawlib.shapes import circle, polygon, rectangle
from drawlib.utils import Icon

Icon.setup()
w_outer, w_inner = 2.0, 1.6

# 1. Headband arc
band_pts = [
    (46.0 + 28.0 * math.cos(math.radians(a)), 48.0 + 28.0 * math.sin(math.radians(a))) for a in range(0, 181, 6)
]
Icon.draw_round_polyline(band_pts, width_units=2.4, color=Icon.DARK)

# 2. Central agent face/head (WHITE)
circle(
    (46.0, 48.0),
    radius=17.0,
    style=Icon.fill_style(Icon.PASTEL_BLUE_LIGHT, border_color=Icon.DARK, border_units=w_outer),
)

# 3. Left & right earcups (PASTEL_BLUE)
for ex in (18.0, 74.0):
    rectangle(
        (ex, 45.0),
        width=10.0,
        height=20.0,
        style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=w_outer, shape_r=4.0),
    )

# 4. Microphone boom to center
Icon.draw_round_polyline([(18.0, 35.0), (24.0, 22.0), (42.0, 22.0)], width_units=w_outer, color=Icon.DARK)
rectangle(
    (45.0, 22.0),
    width=10.0,
    height=6.5,
    style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=w_inner, shape_r=3.0),
)

# 5. Speech bubble badge at top-right (PASTEL_GREEN)
circle(
    (76.0, 74.0), radius=12.0, style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=w_outer)
)
Icon.draw_round_segment((71.0, 74.0), (81.0, 74.0), width_units=w_inner, color=Icon.DARK)
save()
