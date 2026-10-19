# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Security concept icon: pam_bastion."""

from drawlib.canvas import save
from drawlib.shapes import polygon, rectangle
from drawlib.utils import Icon

Icon.setup()

w_shape = 2.0
w_line = 2.0

# 1. Main fortress wall (y=16..70, tucked under battlements at y=64..84)
rectangle(
    (50.0, 43.0),
    width=64.0,
    height=54.0,
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w_shape, shape_r=6.0),
)

# 2. Top castle battlements (y=64..84)
battlement_pts = [
    (16.0, 64.0),
    (16.0, 84.0),
    (32.0, 84.0),
    (32.0, 74.0),
    (42.0, 74.0),
    (42.0, 84.0),
    (58.0, 84.0),
    (58.0, 74.0),
    (68.0, 74.0),
    (68.0, 84.0),
    (84.0, 84.0),
    (84.0, 64.0),
]
polygon(battlement_pts, style=Icon.no_border_fill(Icon.PASTEL_BLUE))
Icon.draw_round_polyline(battlement_pts, width_units=w_shape, color=Icon.DARK, closed=True)

# 3. Inner SSH terminal screen
rectangle(
    (50.0, 40.0),
    width=48.0,
    height=32.0,
    style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=w_shape, shape_r=4.5),
)

# 4. Terminal prompt `>_`
Icon.draw_round_polyline(
    [(35.0, 46.5), (44.0, 40.0), (35.0, 33.5)],
    width_units=w_line,
    color=Icon.DARK,
)
Icon.draw_round_segment((49.0, 33.5), (62.0, 33.5), width_units=w_line, color=Icon.DARK)

save()
