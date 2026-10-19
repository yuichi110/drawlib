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
from drawlib.utils import Icon

Icon.setup()

w = Icon.ORIG_STROKE

# Outer media player card
rectangle(
    (50.0, 56.0),
    width=72.0,
    height=50.0,
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w, shape_r=7.0),
)

# Inner video viewport screen
rectangle(
    (50.0, 56.0),
    width=60.0,
    height=38.0,
    style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=2.0, shape_r=4.0),
)

# Central right-pointing play triangle
play_pts = [(43.0, 65.5), (43.0, 46.5), (61.0, 56.0)]
polygon(play_pts, style=Icon.no_border_fill(Icon.PASTEL_GREEN))
Icon.draw_round_polyline(play_pts, width_units=w, color=Icon.DARK, closed=True)

# Bottom timeline scrub bar and playhead
scrub_y = 20.0
Icon.draw_round_segment((20.0, scrub_y), (80.0, scrub_y), width_units=w, color=Icon.DARK)
circle(
    (46.0, scrub_y),
    radius=5.5,
    style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=2.0),
)

save()
