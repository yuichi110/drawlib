# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Social concept icon: user_engagement (default variant)."""

import math

from drawlib.canvas import save
from drawlib.shapes import circle, polygon, rectangle
from drawlib.styles import Colors
from drawlib.utils import Icon

w = Icon.ORIG_STROKE
Icon.setup()
rectangle(
    (44.0, 54.0),
    width=58.0,
    height=44.0,
    style=Icon.fill_style(Colors.Blue3, border_color=Icon.DARK, border_units=w, shape_r=10.0),
)
polygon(
    [(24.0, 32.0), (18.0, 18.0), (36.0, 32.0)],
    style=Icon.fill_style(Colors.Blue3, border_color=Icon.DARK, border_units=w),
)
heart_pts = [
    (
        round(44.0 + 16.0 * (math.sin(2.0 * math.pi * i / 48) ** 3) * 0.85, 2),
        round(
            55.5
            + (
                13.0 * math.cos(2.0 * math.pi * i / 48)
                - 5.0 * math.cos(4.0 * math.pi * i / 48)
                - 2.0 * math.cos(6.0 * math.pi * i / 48)
                - math.cos(8.0 * math.pi * i / 48)
            )
            * 0.85,
            2,
        ),
    )
    for i in range(48)
]
polygon(heart_pts, style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w * 0.85))
circle((72.0, 32.0), radius=15.0, style=Icon.fill_style(Colors.Green3, border_color=Icon.DARK, border_units=w))
polygon(
    [
        (72.0, 41.0),
        (74.5, 34.5),
        (81.0, 34.5),
        (76.0, 30.5),
        (78.0, 24.0),
        (72.0, 28.0),
        (66.0, 24.0),
        (68.0, 30.5),
        (63.0, 34.5),
        (69.5, 34.5),
    ],
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w * 0.7),
)
save()
