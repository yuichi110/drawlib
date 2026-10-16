# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original AI concept icon: mistral."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.styles import Colors
from drawlib.utils import (
    DARK,
    draw_round_polyline,
    no_border_fill,
    setup_icon,
)

setup_icon()

w = 1.9

# 7x5 pixel-block grid (step = 11.2, width = 78.4, height = 56.0, centered at (50, 50))
s = 11.2
x0 = 50.0 - 3.5 * s  # 10.8
y0 = 50.0 - 2.5 * s  # 22.0

xs = [x0 + i * s for i in range(8)]
ys = [y0 + j * s for j in range(6)]
ov = 0.12  # Tiny vertical under-tuck to prevent anti-aliasing seams between rows

# 1. Row 4 (ys[4]..ys[5], Colors.Amber2): two top squares
row4_left = [(xs[1], ys[4] - ov), (xs[2], ys[4] - ov), (xs[2], ys[5]), (xs[1], ys[5])]
row4_right = [(xs[5], ys[4] - ov), (xs[6], ys[4] - ov), (xs[6], ys[5]), (xs[5], ys[5])]
polygon(row4_left, style=no_border_fill(Colors.Amber2))
polygon(row4_right, style=no_border_fill(Colors.Amber2))

# 2. Row 3 (ys[3]..ys[4], Colors.Amber3): two stepped 2-wide blocks
row3_left = [(xs[1], ys[3] - ov), (xs[3], ys[3] - ov), (xs[3], ys[4]), (xs[1], ys[4])]
row3_right = [(xs[4], ys[3] - ov), (xs[6], ys[3] - ov), (xs[6], ys[4]), (xs[4], ys[4])]
polygon(row3_left, style=no_border_fill(Colors.Amber3))
polygon(row3_right, style=no_border_fill(Colors.Amber3))

# 3. Row 2 (ys[2]..ys[3], Colors.Orange3): full horizontal crossbar
row2_bar = [
    (xs[1], ys[2] - ov),
    (xs[2], ys[2] - ov),
    (xs[2], ys[2]),
    (xs[3], ys[2]),
    (xs[3], ys[2] - ov),
    (xs[4], ys[2] - ov),
    (xs[4], ys[2]),
    (xs[5], ys[2]),
    (xs[5], ys[2] - ov),
    (xs[6], ys[2] - ov),
    (xs[6], ys[3]),
    (xs[1], ys[3]),
]
polygon(row2_bar, style=no_border_fill(Colors.Orange3))

# 4. Row 1 (ys[1]..ys[2], "#EC6E42"): three vertical legs
RED_ORANGE = "#EC6E42"
row1_left = [(xs[1], ys[1] - ov), (xs[2], ys[1] - ov), (xs[2], ys[2]), (xs[1], ys[2])]
row1_mid = [(xs[3], ys[1]), (xs[4], ys[1]), (xs[4], ys[2]), (xs[3], ys[2])]
row1_right = [(xs[5], ys[1] - ov), (xs[6], ys[1] - ov), (xs[6], ys[2]), (xs[5], ys[2])]
polygon(row1_left, style=no_border_fill(RED_ORANGE))
polygon(row1_mid, style=no_border_fill(RED_ORANGE))
polygon(row1_right, style=no_border_fill(RED_ORANGE))

# 5. Row 0 (ys[0]..ys[1], Colors.Red3): two wide bottom feet
row0_left = [(xs[0], ys[0]), (xs[3], ys[0]), (xs[3], ys[1]), (xs[0], ys[1])]
row0_right = [(xs[4], ys[0]), (xs[7], ys[0]), (xs[7], ys[1]), (xs[4], ys[1])]
polygon(row0_left, style=no_border_fill(Colors.Red3))
polygon(row0_right, style=no_border_fill(Colors.Red3))

# 6. United outer stepped M tower silhouette (width_units = w, no interior seams)
outer_m = [
    (xs[0], ys[0]),
    (xs[3], ys[0]),
    (xs[3], ys[1]),
    (xs[2], ys[1]),
    (xs[2], ys[2]),
    (xs[3], ys[2]),
    (xs[3], ys[1]),
    (xs[4], ys[1]),
    (xs[4], ys[2]),
    (xs[5], ys[2]),
    (xs[5], ys[1]),
    (xs[4], ys[1]),
    (xs[4], ys[0]),
    (xs[7], ys[0]),
    (xs[7], ys[1]),
    (xs[6], ys[1]),
    (xs[6], ys[5]),
    (xs[5], ys[5]),
    (xs[5], ys[4]),
    (xs[4], ys[4]),
    (xs[4], ys[3]),
    (xs[3], ys[3]),
    (xs[3], ys[4]),
    (xs[2], ys[4]),
    (xs[2], ys[5]),
    (xs[1], ys[5]),
    (xs[1], ys[1]),
    (xs[0], ys[1]),
]
draw_round_polyline(outer_m, width_units=w, color=DARK, closed=True)

save()
