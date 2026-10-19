# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original concept icon: workflow_orchestrator."""

from drawlib.canvas import save
from drawlib.shapes import circle, polygon, rectangle
from drawlib.utils import Icon

Icon.setup()

w = Icon.ORIG_STROKE

Icon.draw_round_segment((24.0, 74.0), (76.0, 74.0), width_units=w, color=Icon.DARK)
Icon.draw_round_polyline(
    [(50.0, 74.0), (50.0, 26.0), (76.0, 26.0)],
    width_units=w,
    color=Icon.DARK,
    corner_r=6.0,
)

circle(
    (24.0, 74.0),
    radius=9.0,
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w),
)

polygon(
    [(50.0, 86.0), (62.0, 74.0), (50.0, 62.0), (38.0, 74.0)],
    style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=w, shape_r=2.5),
)

rectangle(
    (76.0, 74.0),
    width=18.0,
    height=18.0,
    style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=w, shape_r=4.0),
)

rectangle(
    (76.0, 26.0),
    width=18.0,
    height=18.0,
    style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=w, shape_r=4.0),
)

save()
