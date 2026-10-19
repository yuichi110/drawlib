# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Data concept icon: cdc_stream."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import Icon

Icon.setup()
w = Icon.ORIG_STROKE
Icon.draw_cylinder_tier(
    30.0, 22.0, 36.0, 52.0, 8.0, body_color=Icon.PASTEL_BLUE, top_color=Icon.PASTEL_BLUE_LIGHT, border_units=w
)
# Streaming chevrons / change events
for idx, (x0, col) in enumerate(((52.0, Icon.PASTEL_GREEN), (68.0, Icon.WHITE), (80.0, Icon.PASTEL_GREEN))):
    pts = [(x0, 66.0), (x0 + 10.0, 50.0), (x0, 34.0), (x0 - 6.0, 34.0), (x0 + 4.0, 50.0), (x0 - 6.0, 66.0)]
    polygon(pts, style=Icon.fill_style(col, border_color=Icon.DARK, border_units=w))
save()
