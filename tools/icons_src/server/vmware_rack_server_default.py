# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Server icon: vmware_rack_server."""

from drawlib.canvas import save
from drawlib.shapes import circle, rectangle
from drawlib.styles import Colors
from drawlib.utils import Icon, Vmware

Icon.setup()

# 3 stacked horizontal 1U rack server boxes (vvd_icons/rack-servers.svg)
for cy in (76.0, 50.0, 24.0):
    rectangle(
        (50.0, cy),
        width=80.0,
        height=20.0,
        style=Icon.fill_style(Colors.Transparent, border_color=Vmware.NAVY, border_units=4.5, shape_r=2.0),
    )

    # 4 crisp vertical vent bars on the left
    for vx in (18.0, 22.5, 27.0, 31.5):
        rectangle(
            (vx, cy),
            width=3.2,
            height=9.0,
            style=Icon.no_border_fill(Vmware.CYAN, shape_r=0.4),
        )

    # 1 circular status LED on the right
    circle(
        (80.0, cy),
        radius=2.6,
        style=Icon.no_border_fill(Vmware.GREEN),
    )

save()
