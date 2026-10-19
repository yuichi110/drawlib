# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Server icon: vmware_storage_array_default."""

from drawlib.canvas import save
from drawlib.shapes import circle, rectangle
from drawlib.styles import Colors
from drawlib.utils import Icon, Vmware

Icon.setup()

# Back hard-drive enclosure card (x=10..66, y=42..86, clipped at middle card)
Icon.draw_round_polyline(
    [(21.0, 42.0), (10.0, 42.0), (10.0, 86.0), (66.0, 86.0), (66.0, 74.0)],
    width_units=4.4,
    color=Vmware.NAVY,
    corner_r=4.0,
)

# Middle hard-drive enclosure card (x=21..77, y=30..74, clipped at front card)
Icon.draw_round_polyline(
    [(32.0, 30.0), (21.0, 30.0), (21.0, 74.0), (77.0, 74.0), (77.0, 62.0)],
    width_units=4.4,
    color=Vmware.NAVY,
    corner_r=4.0,
)

# Front hard-drive enclosure card (x=32..90, y=16..62)
rectangle(
    (61.0, 39.0),
    width=58.0,
    height=46.0,
    style=Icon.fill_style(Colors.Transparent, border_color=Vmware.NAVY, border_units=4.4, shape_r=4.0),
)

# Circular disk platter on front card (cx=56.0, cy=39.0, outer_r=14.0, inner_r=5.0)
circle(
    (56.0, 39.0),
    radius=14.0,
    style=Icon.stroke_style(Vmware.CYAN, width_units=4.0),
)
circle(
    (56.0, 39.0),
    radius=5.0,
    style=Icon.stroke_style(Vmware.NAVY, width_units=3.6),
)

# Horizontal actuator arm extending right to (80.0, 39.0)
Icon.draw_round_segment((70.0, 39.0), (80.0, 39.0), width_units=4.0, color=Vmware.CYAN)

save()
