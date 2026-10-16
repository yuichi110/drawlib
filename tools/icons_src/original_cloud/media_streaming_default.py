# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original concept icon: media_streaming."""

from drawlib.canvas import save
from drawlib.shapes import circle, polygon, rectangle
from drawlib.utils import (
    DARK,
    ORIG_STROKE,
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

w = ORIG_STROKE

# Outer media player card
rectangle(
    (50.0, 56.0),
    width=72.0,
    height=50.0,
    style=fill_style(WHITE, border_color=DARK, border_units=w, shape_r=7.0),
)

# Inner video viewport screen
rectangle(
    (50.0, 56.0),
    width=60.0,
    height=38.0,
    style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=2.2, shape_r=4.0),
)

# Central right-pointing play triangle
play_pts = [(43.0, 65.5), (43.0, 46.5), (61.0, 56.0)]
polygon(play_pts, style=no_border_fill(PASTEL_GREEN))
draw_round_polyline(play_pts, width_units=w, color=DARK, closed=True)

# Bottom timeline scrub bar and playhead
scrub_y = 20.0
draw_round_segment((20.0, scrub_y), (80.0, scrub_y), width_units=w, color=DARK)
circle(
    (46.0, scrub_y),
    radius=5.5,
    style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=2.4),
)

save()
