# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Security concept icon: secret_vault."""

import math

from drawlib.canvas import save
from drawlib.shapes import circle, rectangle
from drawlib.utils import Icon

Icon.setup()

w_shape = 2.0
w_line = 2.0

# 1. PASTEL_BLUE outer square vault frame
rectangle(
    (50.0, 50.0),
    width=76.0,
    height=76.0,
    style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=w_shape, shape_r=9.0),
)

# 2. Inner WHITE steel vault door
rectangle(
    (52.0, 50.0),
    width=56.0,
    height=58.0,
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w_shape, shape_r=5.0),
)

# 3. 2 heavy PASTEL_BLUE_LIGHT rectangular hinges on the left edge
for hy in (64.0, 36.0):
    rectangle(
        (23.0, hy),
        width=8.0,
        height=12.0,
        style=Icon.fill_style(Icon.PASTEL_BLUE_LIGHT, border_color=Icon.DARK, border_units=w_shape, shape_r=2.0),
    )

# 4. Central PASTEL_GREEN rotary combination wheel
wheel_cx, wheel_cy = 52.0, 50.0
circle(
    (wheel_cx, wheel_cy),
    radius=15.0,
    style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=w_shape),
)

# 5. 4 diagonal DARK spokes at 45, 135, 225, 315 deg extending to r=19.0 with handle caps
for deg in (45.0, 135.0, 225.0, 315.0):
    ang = math.radians(deg)
    tx = wheel_cx + 19.0 * math.cos(ang)
    ty = wheel_cy + 19.0 * math.sin(ang)
    Icon.draw_round_segment((wheel_cx, wheel_cy), (tx, ty), width_units=w_line, color=Icon.DARK)
    circle((tx, ty), radius=2.1, style=Icon.fill_style(Icon.DARK))

# 6. Center WHITE hub circle
circle(
    (wheel_cx, wheel_cy),
    radius=5.5,
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w_shape),
)

save()
