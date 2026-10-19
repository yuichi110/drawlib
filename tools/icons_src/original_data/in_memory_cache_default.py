# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Data concept icon: in_memory_cache."""

from drawlib.canvas import save
from drawlib.shapes import polygon, rectangle
from drawlib.utils import Icon

Icon.setup()
w = Icon.ORIG_STROKE
# Chip pins on all 4 sides
for pos in (32.0, 50.0, 68.0):
    Icon.draw_round_segment((12.0, pos), (24.0, pos), width_units=w * 1.5, color=Icon.DARK)
    Icon.draw_round_segment((76.0, pos), (88.0, pos), width_units=w * 1.5, color=Icon.DARK)
    Icon.draw_round_segment((pos, 12.0), (pos, 24.0), width_units=w * 1.5, color=Icon.DARK)
    Icon.draw_round_segment((pos, 76.0), (pos, 88.0), width_units=w * 1.5, color=Icon.DARK)
rectangle(
    (50.0, 50.0),
    width=56.0,
    height=56.0,
    style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=w, shape_r=8.0),
)
rectangle(
    (50.0, 50.0),
    width=42.0,
    height=42.0,
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w, shape_r=4.0),
)
# Lightning bolt in center
bolt = [(54.0, 67.0), (39.0, 50.0), (49.0, 50.0), (45.0, 33.0), (61.0, 51.0), (51.0, 51.0)]
polygon(bolt, style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=w))
save()
