# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Server concept icon: resource_pool."""

import math

from drawlib.canvas import save
from drawlib.shapes import circle, polygon
from drawlib.utils import Icon

Icon.setup()

w = Icon.ORIG_STROKE
cx, cy = 50.0, 50.0

# Outer circular pool ring border (transparent moat)
circle(
    (cx, cy),
    radius=38.0,
    style=Icon.stroke_style(Icon.DARK, width_units=w),
)

# 3-slice donut gauge chart (r=9.5..30.0) representing CPU / Memory / IOPS allocation
slices = [
    (90.0, 220.0, Icon.PASTEL_BLUE),
    (220.0, 330.0, Icon.PASTEL_BLUE_LIGHT),
    (330.0, 90.0, Icon.PASTEL_GREEN),
]
r_in, r_out = 9.5, 30.0
for ang_start, ang_end, fill_col in slices:
    span = ang_end - ang_start if ang_end > ang_start else (ang_end + 360.0) - ang_start
    steps = 28
    outer_arc = [
        (
            cx + r_out * math.cos(math.radians(ang_start + span * (i / steps))),
            cy + r_out * math.sin(math.radians(ang_start + span * (i / steps))),
        )
        for i in range(steps + 1)
    ]
    inner_arc = [
        (
            cx + r_in * math.cos(math.radians(ang_start + span * (i / steps))),
            cy + r_in * math.sin(math.radians(ang_start + span * (i / steps))),
        )
        for i in range(steps, -1, -1)
    ]
    polygon([*outer_arc, *inner_arc], style=Icon.no_border_fill(fill_col))
    Icon.draw_round_segment(inner_arc[-1], outer_arc[0], width_units=2.0, color=Icon.DARK)
    Icon.draw_round_segment(inner_arc[0], outer_arc[-1], width_units=2.0, color=Icon.DARK)

# Crisp continuous outer and inner perimeter strokes around the 3 donut slices
circle(
    (cx, cy),
    radius=r_out,
    style=Icon.stroke_style(Icon.DARK, width_units=2.0),
)
circle(
    (cx, cy),
    radius=r_in,
    style=Icon.stroke_style(Icon.DARK, width_units=2.0),
)

save()
