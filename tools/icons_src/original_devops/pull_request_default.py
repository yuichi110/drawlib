# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original concept icon: pull_request."""

from drawlib.canvas import save
from drawlib.shapes import circle
from drawlib.utils import Icon

Icon.setup()

w = Icon.ORIG_STROKE

# Main vertical branch line on the left
Icon.draw_round_segment((28.0, 22.0), (28.0, 78.0), width_units=w, color=Icon.DARK)

# PR branch rising from bottom-right and curving left toward main branch
Icon.draw_round_polyline(
    [(72.0, 24.0), (72.0, 62.0), (43.0, 62.0)],
    corner_r=10.0,
    width_units=w,
    color=Icon.DARK,
)
Icon.draw_round_polyline(
    [(51.5, 69.5), (43.0, 62.0), (51.5, 54.5)],
    width_units=w,
    color=Icon.DARK,
)

# Bottom and top commit nodes on main branch
for cy in (22.0, 78.0):
    circle(
        (28.0, cy),
        radius=8.5,
        style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=w),
    )
    circle((28.0, cy), radius=3.0, style=Icon.fill_style(Icon.WHITE))

# PR branch source commit node on bottom-right
circle(
    (72.0, 24.0),
    radius=9.5,
    style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=w),
)
circle((72.0, 24.0), radius=3.2, style=Icon.fill_style(Icon.WHITE))

save()
