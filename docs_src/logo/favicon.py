# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Drawlib rounded white-card favicon for modern browsers, tabs, and PWAs."""

from drawlib.canvas import canvas, save, setup
from drawlib.shapes import rectangle
from drawlib.styles import Colors, Style
from drawlib.utils import draw_logo_icon

# Transparent canvas so the outer corners of the rounded card remain transparent
setup(width=100, height=100, dpi=200, color=Colors.Canvas, alpha=0.0)

# Rounded white background card (squircle) with subtle border for white tab definition
card_style = Style(
    shape_fill_color=Colors.White,
    shape_line_color=Colors.Gray3,
    shape_line_width=1.0,
    shape_r=20.0,
)
rectangle((50.0, 50.0), width=96.0, height=96.0, style=card_style)

# Draw the Drawlib icon mark centered with balanced padding inside the rounded card
with canvas.transform(origin=(50.0, 50.0), scale=0.86):
    draw_logo_icon(canvas_width=100.0)

save()
