# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Client concept icon: barcode_scanner."""

from drawlib.canvas import save
from drawlib.shapes import polygon, rectangle
from drawlib.utils import (
    DARK,
    ORIG_STROKE,
    PASTEL_BLUE,
    PASTEL_BLUE_LIGHT,
    PASTEL_GREEN,
    WHITE,
    draw_round_segment,
    fill_style,
    setup_icon,
)

setup_icon()

w = ORIG_STROKE

# 1. Trigger button under scanner head (PASTEL_BLUE_LIGHT)
rectangle(
    (42.5, 48.0),
    width=10.0,
    height=9.0,
    style=fill_style(PASTEL_BLUE_LIGHT, border_color=DARK, border_units=2.0, shape_r=2.5),
)

# 2. Angled pistol grip handle (PASTEL_BLUE)
grip_pts = [
    (21.0, 15.0),
    (35.0, 15.0),
    (43.0, 54.0),
    (28.0, 54.0),
]
polygon(
    grip_pts,
    style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=w, shape_r=3.5),
)

# Grip texture grooves
for gy, gx in ((25.0, 26.5), (33.0, 28.2), (41.0, 29.8)):
    draw_round_segment((gx, gy), (gx + 5.5, gy), width_units=1.8, color=DARK)

# 3. Scan beam fan (PASTEL_GREEN) projecting from nose window
beam_pts = [
    (63.0, 64.0),
    (88.0, 78.0),
    (88.0, 50.0),
]
polygon(
    beam_pts,
    style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=2.0, shape_r=1.5),
)

# Vertical scan / barcode bars inside right side of beam
draw_round_segment((80.0, 58.5), (80.0, 69.5), width_units=1.8, color=DARK)
draw_round_segment((84.0, 55.5), (84.0, 72.5), width_units=2.0, color=DARK)

# 4. Scanner head housing (PASTEL_BLUE)
head_pts = [
    (16.0, 52.0),
    (63.0, 52.0),
    (65.0, 76.0),
    (21.0, 76.0),
    (14.5, 65.0),
]
polygon(
    head_pts,
    style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=w, shape_r=(3.5, 2.5, 2.5, 5.0, 4.0)),
)

# 5. Front nose window (WHITE)
window_pts = [
    (55.0, 55.5),
    (63.2, 55.5),
    (64.6, 72.5),
    (55.0, 72.5),
]
polygon(
    window_pts,
    style=fill_style(WHITE, border_color=DARK, border_units=2.0, shape_r=1.8),
)

# Side detail line on scanner head
draw_round_segment((24.0, 64.5), (47.0, 64.5), width_units=2.0, color=DARK)

save()
