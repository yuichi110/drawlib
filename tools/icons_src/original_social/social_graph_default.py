# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Social concept icon: social_graph (default variant)."""

from drawlib.canvas import save
from drawlib.lines import line
from drawlib.shapes import circle
from drawlib.styles import Colors
from drawlib.utils import Icon

w = Icon.ORIG_STROKE
Icon.setup()
nodes = [(20.0, 76.0), (80.0, 76.0), (18.0, 24.0), (82.0, 24.0)]
for nx, ny in nodes:
    line((50.0, 50.0), (nx, ny), style=Icon.stroke_style(Icon.DARK, width_units=w * 1.2))
line((20.0, 76.0), (80.0, 76.0), style=Icon.stroke_style(Icon.DARK, width_units=w * 0.9, line_style="dashed"))
line((18.0, 24.0), (82.0, 24.0), style=Icon.stroke_style(Icon.DARK, width_units=w * 0.9, line_style="dashed"))
circle((50.0, 50.0), radius=16.0, style=Icon.fill_style(Colors.Blue3, border_color=Icon.DARK, border_units=w))
circle((50.0, 54.0), radius=5.5, style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w * 0.8))
circle((50.0, 41.0), radius=8.0, style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w * 0.8))
for idx, (nx, ny) in enumerate(nodes):
    col = Colors.Green3 if idx % 2 == 0 else Colors.Blue2
    circle((nx, ny), radius=10.5, style=Icon.fill_style(col, border_color=Icon.DARK, border_units=w))
    circle((nx, ny + 2.5), radius=3.5, style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w * 0.7))
save()
