# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original concept icon: organization_account."""

from drawlib.canvas import save
from drawlib.shapes import circle, rectangle
from drawlib.utils import Icon

Icon.setup()

w = Icon.ORIG_STROKE

# Orthogonal org tree lines
Icon.draw_round_segment((50.0, 67.0), (50.0, 36.0), width_units=w, color=Icon.DARK)
Icon.draw_round_polyline(
    [(22.0, 36.0), (22.0, 52.0), (78.0, 52.0), (78.0, 36.0)],
    width_units=w,
    color=Icon.DARK,
    corner_r=4.0,
)

# Top root management account card
rectangle(
    (50.0, 76.0),
    width=36.0,
    height=18.0,
    style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=w, shape_r=4.0),
)
circle(
    (39.5, 76.0),
    radius=3.5,
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=2.0),
)
Icon.draw_round_segment((47.5, 76.0), (61.5, 76.0), width_units=2.0, color=Icon.DARK)

# 3 child account/subscription cards
child_configs = [
    (22.0, Icon.PASTEL_BLUE),
    (50.0, Icon.WHITE),
    (78.0, Icon.PASTEL_BLUE),
]
for cx, fill_col in child_configs:
    rectangle(
        (cx, 26.0),
        width=22.0,
        height=20.0,
        style=Icon.fill_style(fill_col, border_color=Icon.DARK, border_units=w, shape_r=3.5),
    )
    Icon.draw_round_segment((cx - 5.5, 26.0), (cx + 5.5, 26.0), width_units=2.0, color=Icon.DARK)

save()
