# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Server icon: vmware_vmotion_default."""

from drawlib.canvas import save
from drawlib.shapes import rectangle
from drawlib.styles import Colors
from drawlib.utils import (
    VMWARE_CYAN,
    VMWARE_GREEN,
    VMWARE_NAVY,
    draw_round_polyline,
    draw_round_segment,
    fill_style,
    setup_icon,
)

setup_icon()

# Left source host open C-bracket (x=10..28, y=15..85, open on right middle)
draw_round_polyline(
    [
        (28.0, 70.0),
        (28.0, 85.0),
        (10.0, 85.0),
        (10.0, 15.0),
        (28.0, 15.0),
        (28.0, 30.0),
    ],
    width_units=4.8,
    color=VMWARE_NAVY,
    corner_r=3.0,
)

# Right destination host tower (x=72..90, y=15..85)
rectangle(
    (81.0, 50.0),
    width=18.0,
    height=70.0,
    style=fill_style(Colors.Transparent, border_color=VMWARE_NAVY, border_units=4.8, shape_r=3.0),
)

# Rounded VM square between hosts (x=22..48, y=37..63, open on right for arrow shaft)
draw_round_polyline(
    [
        (48.0, 56.5),
        (48.0, 63.0),
        (22.0, 63.0),
        (22.0, 37.0),
        (48.0, 37.0),
        (48.0, 43.5),
    ],
    width_units=4.4,
    color=VMWARE_CYAN,
    corner_r=4.0,
)

# Bold horizontal migration arrow moving the VM into the right host (x=38..65.5, y=50.0)
draw_round_segment((38.0, 50.0), (65.0, 50.0), width_units=4.8, color=VMWARE_GREEN)
draw_round_polyline(
    [(54.5, 61.0), (65.5, 50.0), (54.5, 39.0)],
    width_units=4.8,
    color=VMWARE_GREEN,
)

save()
