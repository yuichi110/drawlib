# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Security concept icon: threat_intel."""

from drawlib.canvas import save
from drawlib.shapes import circle
from drawlib.utils import Icon

Icon.setup()

w_shape = 2.0
w_line = 2.0

# Outer PASTEL_BLUE circular radar bezel
circle(
    (50.0, 50.0),
    radius=39.0,
    style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=w_shape),
)

# Inner WHITE radar screen
circle(
    (50.0, 50.0),
    radius=31.0,
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w_shape),
)

# Inner concentric PASTEL_BLUE_LIGHT ring
circle(
    (50.0, 50.0),
    radius=17.0,
    style=Icon.fill_style(Icon.PASTEL_BLUE_LIGHT, border_color=Icon.DARK, border_units=w_shape),
)

# Horizontal and vertical DARK crosshair lines across the screen
Icon.draw_round_segment((19.5, 50.0), (80.5, 50.0), width_units=w_line, color=Icon.DARK)
Icon.draw_round_segment((50.0, 19.5), (50.0, 80.5), width_units=w_line, color=Icon.DARK)

# Diagonal DARK radar sweep line from (50, 50) to screen rim
Icon.draw_round_segment((50.0, 50.0), (71.55, 71.55), width_units=w_line, color=Icon.DARK)
circle((50.0, 50.0), radius=2.4, style=Icon.fill_style(Icon.DARK))

# Prominent PASTEL_GREEN target blip circle at (65, 65) with DARK center dot
circle(
    (65.0, 65.0),
    radius=6.5,
    style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=w_shape),
)
circle((65.0, 65.0), radius=2.0, style=Icon.fill_style(Icon.DARK))

save()
