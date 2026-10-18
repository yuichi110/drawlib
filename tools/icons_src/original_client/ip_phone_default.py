# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Client concept icon: ip_phone."""

from drawlib.canvas import save
from drawlib.shapes import rectangle
from drawlib.utils import (
    DARK,
    ORIG_STROKE,
    PASTEL_BLUE,
    PASTEL_GREEN,
    WHITE,
    draw_round_segment,
    fill_style,
    setup_icon,
)

setup_icon()

w = ORIG_STROKE

# 1. Desk VoIP phone base body (PASTEL_BLUE)
rectangle(
    (55.0, 48.0),
    width=62.0,
    height=64.0,
    style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=w, shape_r=9.0),
)

# 2. Handset resting on left (PASTEL_BLUE)
rectangle(
    (27.0, 50.0),
    width=19.0,
    height=72.0,
    style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=w, shape_r=8.0),
)
# Earpiece and mouthpiece speaker slots on handset
draw_round_segment((23.8, 77.0), (30.2, 77.0), width_units=2.0, color=DARK)
draw_round_segment((23.8, 23.0), (30.2, 23.0), width_units=2.0, color=DARK)

# 3. Upper right LCD screen (WHITE)
rectangle(
    (61.5, 65.5),
    width=36.0,
    height=17.0,
    style=fill_style(WHITE, border_color=DARK, border_units=2.0, shape_r=3.5),
)
# Display lines inside LCD screen
draw_round_segment((49.0, 68.0), (65.0, 68.0), width_units=1.8, color=DARK)
draw_round_segment((49.0, 63.0), (59.0, 63.0), width_units=1.8, color=DARK)

# 4. Keypad 3x3 grid (WHITE keys)
for ky in (49.0, 40.5, 32.0):
    for kx in (49.5, 61.5, 73.5):
        rectangle(
            (kx, ky),
            width=7.5,
            height=5.2,
            style=fill_style(WHITE, border_color=DARK, border_units=1.8, shape_r=1.5),
        )

# 5. Bottom call / speakerphone key (PASTEL_GREEN)
rectangle(
    (61.5, 22.0),
    width=22.0,
    height=6.2,
    style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=2.0, shape_r=3.0),
)

save()
