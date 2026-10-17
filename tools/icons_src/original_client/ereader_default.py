# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Client concept icon: ereader."""

from drawlib.canvas import save
from drawlib.shapes import polygon, rectangle
from drawlib.utils import (
    DARK,
    ORIG_STROKE,
    PASTEL_BLUE,
    PASTEL_GREEN,
    WHITE,
    draw_round_polyline,
    draw_round_segment,
    fill_style,
    setup_icon,
)

setup_icon()

w = ORIG_STROKE

# E-ink reader outer bezel
rectangle(
    (50.0, 50.0),
    width=54.0,
    height=70.0,
    style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=w, shape_r=6.0),
)

# Paper-like WHITE screen (shifted slightly up for classic bottom chin)
rectangle(
    (50.0, 53.5),
    width=42.0,
    height=50.0,
    style=fill_style(WHITE, border_color=DARK, border_units=2.0, shape_r=2.5),
)

# PASTEL_GREEN bookmark ribbon at top-right of screen
bookmark_pts = [
    (57.0, 78.5),
    (65.5, 78.5),
    (65.5, 60.5),
    (61.25, 64.5),
    (57.0, 60.5),
]
polygon(bookmark_pts, style=fill_style(PASTEL_GREEN))
draw_round_polyline(bookmark_pts, width_units=2.0, color=DARK, closed=True)

# Reading page text lines
draw_round_segment((34.5, 70.0), (51.5, 70.0), width_units=2.0, color=DARK)
draw_round_segment((34.5, 62.5), (51.5, 62.5), width_units=2.0, color=DARK)
draw_round_segment((34.5, 53.5), (65.0, 53.5), width_units=2.0, color=DARK)
draw_round_segment((34.5, 45.5), (65.0, 45.5), width_units=2.0, color=DARK)
draw_round_segment((34.5, 37.5), (53.0, 37.5), width_units=2.0, color=DARK)

# Bottom chin page-turn bar
draw_round_segment((43.0, 21.5), (57.0, 21.5), width_units=2.2, color=DARK)

save()
