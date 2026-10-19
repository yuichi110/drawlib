# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Code concept icon: cron_job."""

from drawlib.canvas import save
from drawlib.shapes import circle, polygon, rectangle
from drawlib.utils import Icon

Icon.setup()

b = 2.0
w_line = 2.0

cx, cy = 46.0, 54.0

# Outer PASTEL_BLUE clock bezel
circle(
    (cx, cy),
    radius=33.0,
    style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=b),
)

# Inner WHITE clock face
circle(
    (cx, cy),
    radius=26.0,
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=b),
)

# 4 cardinal tick marks
Icon.draw_round_segment((cx, 76.5), (cx, 73.0), width_units=w_line, color=Icon.DARK)
Icon.draw_round_segment((68.5, cy), (65.0, cy), width_units=w_line, color=Icon.DARK)
Icon.draw_round_segment((cx, 31.5), (cx, 35.0), width_units=w_line, color=Icon.DARK)
Icon.draw_round_segment((23.5, cy), (27.0, cy), width_units=w_line, color=Icon.DARK)

# Hour and minute hands + center pivot
Icon.draw_round_polyline(
    [(cx, 67.5), (cx, cy), (57.0, 48.0)],
    width_units=w_line,
    color=Icon.DARK,
)
circle(
    (cx, cy),
    radius=2.8,
    style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=b),
)

# Bottom-right overlapping PASTEL_GREEN rounded square badge
rectangle(
    (74.0, 26.0),
    width=26.0,
    height=26.0,
    style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=b, shape_r=5.0),
)

# WHITE play triangle inside badge
play_pts = [(69.5, 32.5), (69.5, 19.5), (81.0, 26.0)]
polygon(play_pts, style=Icon.no_border_fill(Icon.WHITE))
Icon.draw_round_polyline(play_pts, width_units=b, color=Icon.DARK, closed=True)

save()
