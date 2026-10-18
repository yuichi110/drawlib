# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Security concept icon: hsm_kms (Hardware Security Module & Key Management)."""

import math

from drawlib.canvas import save
from drawlib.shapes import circle, polygon, rectangle
from drawlib.utils import (
    DARK,
    PASTEL_BLUE,
    PASTEL_GREEN,
    WHITE,
    draw_round_polyline,
    draw_round_segment,
    fill_style,
    no_border_fill,
    setup_icon,
)

setup_icon()

w_shape = 2.0
w_line = 2.0

# 1. 12 metallic chip pins (3 pins protruding on each of the 4 sides at 36, 50, 64)
pin_coords = (36.0, 50.0, 64.0)
for c in pin_coords:
    draw_round_segment((c, 78.0), (c, 88.0), width_units=w_line, color=DARK)
    draw_round_segment((c, 12.0), (c, 22.0), width_units=w_line, color=DARK)
    draw_round_segment((12.0, c), (22.0, c), width_units=w_line, color=DARK)
    draw_round_segment((78.0, c), (88.0, c), width_units=w_line, color=DARK)

# 2. PASTEL_BLUE square microchip package
rectangle(
    (50.0, 50.0),
    width=60.0,
    height=60.0,
    style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=w_shape, shape_r=7.0),
)

# 3. Inner WHITE silicon die square
rectangle(
    (50.0, 50.0),
    width=44.0,
    height=44.0,
    style=fill_style(WHITE, border_color=DARK, border_units=w_shape, shape_r=4.0),
)

# 4. Horizontal PASTEL_GREEN cryptographic key inside the die
bow_cx, bow_cy, bow_r = 40.0, 52.0, 9.0
y_top_shaft = 55.0
y_bot_shaft = 49.5
ang_top = math.degrees(math.asin((y_top_shaft - bow_cy) / bow_r))
ang_bot = 360.0 - math.degrees(math.asin((bow_cy - y_bot_shaft) / bow_r))

key_pts: list[tuple[float, float]] = []
steps = 36
for i in range(steps + 1):
    ang = math.radians(ang_top + (ang_bot - ang_top) * (i / steps))
    key_pts.append((bow_cx + bow_r * math.cos(ang), bow_cy + bow_r * math.sin(ang)))

key_pts.extend(
    [
        (54.0, y_bot_shaft),
        (54.0, 44.5),
        (58.0, 44.5),
        (58.0, y_bot_shaft),
        (61.5, y_bot_shaft),
        (61.5, 43.0),
        (66.0, 43.0),
        (66.0, y_top_shaft),
    ]
)

polygon(key_pts, style=no_border_fill(PASTEL_GREEN))
draw_round_polyline(key_pts, width_units=w_shape, color=DARK, closed=True)

circle(
    (bow_cx, bow_cy),
    radius=3.2,
    style=fill_style(WHITE, border_color=DARK, border_units=w_shape),
)

save()
