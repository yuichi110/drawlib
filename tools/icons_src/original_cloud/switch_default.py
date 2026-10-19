# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original concept icon: switch."""

from drawlib.canvas import save
from drawlib.shapes import rectangle
from drawlib.utils import Cisco, Icon

Icon.setup()

w = Icon.ORIG_STROKE

# Outer rounded concept badge
rectangle(
    (50.0, 50.0),
    width=78.0,
    height=46.0,
    style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=w, shape_r=8.0),
)

# Inner white switching plate
rectangle(
    (50.0, 50.0),
    width=66.0,
    height=34.0,
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=2.0, shape_r=5.0),
)

# Centered 2x2 Cisco-style switching arrows with uniform y spacing (step = 6.4 around y = 50.0)
sw, hl, hw = 3.2, 6.8, 8.6
# Left column (pointing left, x=48.0 -> 24.5)
Cisco.draw_arrow((48.0, 59.6), (24.5, 59.6), shaft_w=sw, head_len=hl, head_w=hw, color=Icon.DARK)
Cisco.draw_arrow((48.0, 46.8), (24.5, 46.8), shaft_w=sw, head_len=hl, head_w=hw, color=Icon.DARK)
# Right column (pointing right, interleaved, x=52.0 -> 75.5)
Cisco.draw_arrow((52.0, 53.2), (75.5, 53.2), shaft_w=sw, head_len=hl, head_w=hw, color=Icon.DARK)
Cisco.draw_arrow((52.0, 40.4), (75.5, 40.4), shaft_w=sw, head_len=hl, head_w=hw, color=Icon.DARK)

save()
