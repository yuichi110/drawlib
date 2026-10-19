# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Data concept icon: etl_pipeline."""

from drawlib.canvas import save
from drawlib.shapes import circle, polygon
from drawlib.utils import Icon

Icon.setup()
w = Icon.ORIG_STROKE
# Left source cylinder
Icon.draw_cylinder_tier(
    22.0, 32.0, 22.0, 32.0, 5.0, body_color=Icon.PASTEL_BLUE, top_color=Icon.PASTEL_BLUE_LIGHT, border_units=w
)
# Right target cylinder
Icon.draw_cylinder_tier(
    78.0, 32.0, 22.0, 32.0, 5.0, body_color=Icon.PASTEL_BLUE_LIGHT, top_color=Icon.WHITE, border_units=w
)
# Connecting pipe
Icon.draw_round_segment((33.0, 50.0), (67.0, 50.0), width_units=w * 2.2, color=Icon.DARK)
# Center Transform funnel/gear node
circle((50.0, 50.0), radius=14.0, style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=w))
tri = [(45.0, 56.0), (57.0, 50.0), (45.0, 44.0)]
polygon(tri, style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w))
save()
