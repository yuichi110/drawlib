# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Server concept icon: bmc."""

import math

from drawlib.canvas import save
from drawlib.shapes import rectangle
from drawlib.utils import Icon

Icon.setup()

w = Icon.ORIG_STROKE
pin_coords = (32.0, 50.0, 68.0)

# 1. Microchip pins on all 4 sides
for pos in pin_coords:
    Icon.draw_round_segment((11.0, pos), (21.0, pos), width_units=w, color=Icon.DARK)
    Icon.draw_round_segment((79.0, pos), (89.0, pos), width_units=w, color=Icon.DARK)
    Icon.draw_round_segment((pos, 11.0), (pos, 21.0), width_units=w, color=Icon.DARK)
    Icon.draw_round_segment((pos, 79.0), (pos, 89.0), width_units=w, color=Icon.DARK)

# 2. Outer white chip package
rectangle(
    (50.0, 50.0),
    width=58.0,
    height=58.0,
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w, shape_r=8.0),
)

# 3. Center-upper darker blue die frame
rectangle(
    (50.0, 56.5),
    width=38.0,
    height=29.0,
    style=Icon.fill_style(Icon.PASTEL_BLUE_DARK, border_color=Icon.DARK, border_units=w, shape_r=4.5),
)

# 4. Crisp white health/pulse line inside the blue frame
pulse_pts = [
    (36.5, 56.5),
    (43.5, 56.5),
    (47.0, 65.5),
    (52.5, 47.5),
    (56.0, 56.5),
    (63.5, 56.5),
]
Icon.draw_round_polyline(pulse_pts, width_units=2.6, color=Icon.WHITE)

# 5. "BMC" geometric vector letters in the bottom white area (y=26.5..36.5)
lw = 1.9

# 'B' (x=34.5 .. 40.8)
b_upper_loop = (
    [(34.5, 31.5), (34.5, 36.5), (38.0, 36.5)]
    + [
        (38.0 + 2.5 * math.cos(math.radians(deg)), 34.0 + 2.5 * math.sin(math.radians(deg)))
        for deg in range(75, -91, -15)
    ]
    + [(34.5, 31.5)]
)
b_lower_loop = (
    [(34.5, 31.5), (38.2, 31.5)]
    + [
        (38.2 + 2.5 * math.cos(math.radians(deg)), 29.0 + 2.5 * math.sin(math.radians(deg)))
        for deg in range(75, -91, -15)
    ]
    + [(34.5, 26.5), (34.5, 31.5)]
)
Icon.draw_round_polyline(b_upper_loop, width_units=lw, color=Icon.DARK)
Icon.draw_round_polyline(b_lower_loop, width_units=lw, color=Icon.DARK)

# 'M' (x=45.0 .. 54.0)
Icon.draw_round_polyline(
    [
        (45.0, 26.5),
        (45.0, 36.5),
        (49.5, 29.0),
        (54.0, 36.5),
        (54.0, 26.5),
    ],
    width_units=lw,
    color=Icon.DARK,
)

# 'C' (x=59.0 .. 65.5)
c_pts = [
    (62.2 + 3.2 * math.cos(math.radians(deg)), 33.3 + 3.2 * math.sin(math.radians(deg)))
    for deg in range(40, 181, 15)
] + [
    (62.2 + 3.2 * math.cos(math.radians(deg)), 29.7 + 3.2 * math.sin(math.radians(deg)))
    for deg in range(180, 321, 15)
]
Icon.draw_round_polyline(c_pts, width_units=lw, color=Icon.DARK)

save()
