# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Data concept icon: databricks."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.styles import Colors
from drawlib.utils import Icon

Icon.setup()

w = 2.0

# Isometric Databricks geometry:
# x spans [13.0, 87.0] (half-width 37.0), isometric vertical slope = 20.5 / 37.0 (~0.55405)
# Top diamond has an open gap on the top-right between the back-right arm and front-right post.

# 1. Top C-shaped diamond layer (Bar 4) with clean open top-right notch (Colors.Red3)
top_diamond_ring = [
    (75.0, 73.9),  # Outer end of top-right back arm
    (50.0, 87.8),  # Top outer peak
    (13.0, 67.3),  # Left outer corner of top diamond
    (50.0, 46.8),  # Front outer corner of Bar 4
    (81.0, 64.0),  # Right inner corner at fold
    (87.0, 67.3),  # Right outer corner of front-right post
    (81.6, 70.3),  # Top bevel of front-right post
    (50.0, 52.8),  # Front inner corner of top diamond
    (23.8, 67.3),  # Left inner corner of top diamond
    (50.0, 81.8),  # Top inner corner of top diamond
    (69.6, 70.9),  # Inner end of top-right back arm
]
polygon(top_diamond_ring, style=Icon.no_border_fill(Colors.Red3))

# 2. Middle chevron layer: Right vertical drop + Bar 3 (Colors.Orange3)
middle_layer = [
    (81.0, 64.0),
    (81.0, 58.8),  # Right inner pocket bottom-right
    (50.0, 41.6),  # Front top of Bar 3
    (13.0, 62.1),  # Left top of Bar 3
    (13.0, 56.1),  # Left bottom of Bar 3
    (50.0, 35.6),  # Front bottom of Bar 3
    (87.0, 56.1),  # Right bottom of Bar 3
    (87.0, 67.3),  # Right top of Bar 3 vertical drop
]
polygon(middle_layer, style=Icon.no_border_fill(Colors.Orange3))

# 3. Lower folded chevron layer: Left post + Bar 2 + right post + Bar 1 (Colors.Red4)
lower_layer = [
    (13.0, 56.1),
    (19.0, 52.8),
    (19.0, 47.6),
    (50.0, 30.4),
    (87.0, 50.9),
    (87.0, 33.7),
    (50.0, 13.2),
    (13.0, 33.7),
    (13.0, 39.7),
    (50.0, 19.2),
    (81.0, 36.4),
    (81.0, 41.6),
    (50.0, 24.4),
    (13.0, 44.9),
]
polygon(lower_layer, style=Icon.no_border_fill(Colors.Red4))

# 4. Crisp structural outlines (full outer perimeter of upper_layer + seam + lower_layer)
upper_outline = [
    (75.0, 73.9),
    (50.0, 87.8),
    (13.0, 67.3),
    (50.0, 46.8),
    (81.0, 64.0),
    (81.0, 58.8),
    (50.0, 41.6),
    (13.0, 62.1),
    (13.0, 56.1),
    (50.0, 35.6),
    (87.0, 56.1),
    (87.0, 67.3),
    (81.6, 70.3),
    (50.0, 52.8),
    (23.8, 67.3),
    (50.0, 81.8),
    (69.6, 70.9),
]
Icon.draw_round_polyline(lower_layer, width_units=w, color=Icon.DARK, closed=True)
Icon.draw_round_polyline(upper_outline, width_units=w, color=Icon.DARK, closed=True)
Icon.draw_round_polyline([(81.0, 64.0), (87.0, 67.3)], width_units=1.6, color=Icon.DARK)

save()
