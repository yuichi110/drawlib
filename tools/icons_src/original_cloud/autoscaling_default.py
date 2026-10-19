# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original concept icon: autoscaling."""

from drawlib.canvas import save
from drawlib.shapes import circle, rectangle
from drawlib.utils import Icon

Icon.setup()

w = Icon.ORIG_STROKE

corners = [(20.0, 80.0), (80.0, 80.0), (20.0, 20.0), (80.0, 20.0)]
for corner in corners:
    Icon.draw_round_segment((50.0, 50.0), corner, width_units=w, color=Icon.DARK)

arrow_heads = [
    [(20.0, 66.0), (20.0, 80.0), (34.0, 80.0)],
    [(66.0, 80.0), (80.0, 80.0), (80.0, 66.0)],
    [(20.0, 34.0), (20.0, 20.0), (34.0, 20.0)],
    [(66.0, 20.0), (80.0, 20.0), (80.0, 34.0)],
]
for head in arrow_heads:
    Icon.draw_round_polyline(head, width_units=w, color=Icon.DARK)

rectangle(
    (50.0, 50.0),
    width=44.0,
    height=44.0,
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w, shape_r=6.0),
)

rectangle(
    (50.0, 50.0),
    width=24.0,
    height=24.0,
    style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=2.0, shape_r=4.0),
)

circle(
    (50.0, 50.0),
    radius=4.0,
    style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=2.0),
)

save()
