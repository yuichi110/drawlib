# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Network concept icon: router."""

from drawlib.canvas import save
from drawlib.shapes import circle
from drawlib.utils import Cisco, Icon

Icon.setup()

w = Icon.ORIG_STROKE

# Outer pastel blue router disc
circle(
    (50.0, 50.0),
    radius=38.0,
    style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=w),
)

# Inner white routing plate
circle(
    (50.0, 50.0),
    radius=28.0,
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=2.0),
)

# Left and right horizontal arrows pointing inward toward center
Cisco.draw_arrow(
    (25.0, 50.0),
    (42.0, 50.0),
    shaft_w=3.2,
    head_len=6.5,
    head_w=8.5,
    color=Icon.DARK,
)
Cisco.draw_arrow(
    (75.0, 50.0),
    (58.0, 50.0),
    shaft_w=3.2,
    head_len=6.5,
    head_w=8.5,
    color=Icon.DARK,
)

# Top and bottom vertical arrows pointing outward away from center
Cisco.draw_arrow(
    (50.0, 58.0),
    (50.0, 75.0),
    shaft_w=3.2,
    head_len=6.5,
    head_w=8.5,
    color=Icon.DARK,
)
Cisco.draw_arrow(
    (50.0, 42.0),
    (50.0, 25.0),
    shaft_w=3.2,
    head_len=6.5,
    head_w=8.5,
    color=Icon.DARK,
)

# Central routing hub dot
circle(
    (50.0, 50.0),
    radius=5.2,
    style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=2.0),
)

save()
