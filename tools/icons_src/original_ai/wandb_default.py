# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original AI concept icon: wandb."""

from drawlib.canvas import save
from drawlib.shapes import circle
from drawlib.styles import Colors
from drawlib.utils import (
    DARK,
    fill_style,
    setup_icon,
)

setup_icon()

w_dot = 1.8
scale = 0.94

dot_style = fill_style(Colors.Amber3, border_color=DARK, border_units=w_dot)

# 3x4 dotted wave grid: (x, y, radius)
raw_dots = [
    # Left column (top to bottom)
    (17.53, 85.60, 5.33),
    (17.49, 64.47, 8.47),
    (17.44, 43.36, 5.33),
    (17.49, 22.22, 8.47),
    # Middle column (top to bottom)
    (50.03, 77.68, 5.25),
    (50.08, 56.65, 5.33),
    (50.08, 35.47, 8.49),
    (50.08, 14.40, 5.33),
    # Right column (top to bottom)
    (82.62, 85.60, 5.33),
    (82.57, 64.44, 8.43),
    (82.62, 43.25, 5.33),
    (82.62, 22.18, 5.33),
]

for x, y, r in raw_dots:
    cx = 50.0 + (x - 50.0) * scale
    cy = 50.0 + (y - 50.0) * scale
    circle((cx, cy), radius=r * scale, style=dot_style)

save()
