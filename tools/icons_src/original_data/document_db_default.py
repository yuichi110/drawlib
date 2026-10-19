# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Data concept icon: document_db."""

from drawlib.canvas import save
from drawlib.shapes import polygon, rectangle
from drawlib.utils import Icon

Icon.setup()
w = Icon.ORIG_STROKE
# Back sheet
rectangle(
    (44.0, 54.0),
    width=48.0,
    height=62.0,
    style=Icon.fill_style(Icon.PASTEL_BLUE_LIGHT, border_color=Icon.DARK, border_units=w, shape_r=5.0),
)
# Front document sheet with folded corner
doc_pts = [(28.0, 14.0), (76.0, 14.0), (76.0, 62.0), (62.0, 76.0), (28.0, 76.0)]
polygon(doc_pts, style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w))
fold_pts = [(62.0, 76.0), (62.0, 62.0), (76.0, 62.0)]
polygon(fold_pts, style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=w))
# JSON badge and lines inside document
rectangle(
    (52.0, 52.0),
    width=32.0,
    height=14.0,
    style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=w, shape_r=3.5),
)
for yc, x1 in ((36.0, 66.0), (28.0, 60.0), (20.0, 54.0)):
    Icon.draw_round_segment((36.0, yc), (x1, yc), width_units=w * 1.2, color=Icon.DARK)
save()
