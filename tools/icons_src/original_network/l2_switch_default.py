# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Network concept icon: l2_switch."""

from drawlib.canvas import save
from drawlib.shapes import circle, rectangle
from drawlib.utils import Cisco, Icon

Icon.setup()

w = Icon.ORIG_STROKE

# Wide horizontal rack switch body
rectangle(
    (50.0, 50.0),
    width=78.0,
    height=46.0,
    style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=w, shape_r=8.0),
)

# Inner white front panel
rectangle(
    (50.0, 50.0),
    width=66.0,
    height=34.0,
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=2.0, shape_r=5.0),
)

# Two pastel green status LED dots on the left of the panel
for y_led in (55.5, 44.5):
    circle(
        (24.0, y_led),
        radius=2.8,
        style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=1.8),
    )

# 2x2 Cisco-style switching arrows with uniform y spacing (step = 6.4 around y = 50.0)
sw, hl, hw = 3.2, 6.5, 8.4
# Left column (pointing left)
Cisco.draw_arrow((53.0, 59.6), (32.0, 59.6), shaft_w=sw, head_len=hl, head_w=hw, color=Icon.DARK)
Cisco.draw_arrow((53.0, 46.8), (32.0, 46.8), shaft_w=sw, head_len=hl, head_w=hw, color=Icon.DARK)
# Right column (pointing right, interleaved with uniform y step)
Cisco.draw_arrow((56.0, 53.2), (77.0, 53.2), shaft_w=sw, head_len=hl, head_w=hw, color=Icon.DARK)
Cisco.draw_arrow((56.0, 40.4), (77.0, 40.4), shaft_w=sw, head_len=hl, head_w=hw, color=Icon.DARK)

save()
