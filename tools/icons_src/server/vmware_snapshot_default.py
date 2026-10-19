# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Server icon: vmware_snapshot."""

import math

from drawlib.canvas import save
from drawlib.shapes import arc
from drawlib.utils import Icon, Vmware

Icon.setup()

# Foreground VM rounded square (x=12..68, y=30..86, open around bottom-right clock badge) (clarity/vm-line.svg)
Icon.draw_round_polyline(
    [(44.0, 30.0), (12.0, 30.0), (12.0, 86.0), (68.0, 86.0), (68.0, 56.5)],
    width_units=4.5,
    color=Vmware.NAVY,
    corner_r=5.0,
)

# Inner interlocking VMWARE_CYAN VM corner lines
Icon.draw_round_polyline(
    [(30.0, 74.0), (52.0, 74.0), (52.0, 56.0)],
    width_units=3.8,
    color=Vmware.CYAN,
    corner_r=4.0,
)
Icon.draw_round_polyline(
    [(24.0, 62.0), (24.0, 44.0), (44.0, 44.0)],
    width_units=3.8,
    color=Vmware.CYAN,
    corner_r=4.0,
)

# Overlapping bottom-right circular history/clock badge (cx=69.0, cy=31.0, r=20.0) (clarity/history-line.svg)
badge_cx, badge_cy = 69.0, 31.0
badge_r = 20.0

# Counter-clockwise circular arrow outline (from 215 deg around bottom/right/top to 162 deg)
ang_start = 215.0
ang_end = 162.0
arc(
    (badge_cx, badge_cy),
    width=badge_r * 2.0,
    height=badge_r * 2.0,
    angle_start=ang_start,
    angle_end=360.0 + ang_end,
    style=Icon.stroke_style(Vmware.CYAN, width_units=4.2),
)

# Round cap at tail of circular arrow (215 deg)
tail_x = badge_cx + badge_r * math.cos(math.radians(ang_start))
tail_y = badge_cy + badge_r * math.sin(math.radians(ang_start))
Icon.draw_cap((tail_x, tail_y), width_units=4.2, color=Vmware.CYAN)

# Top-left arrowhead at tip of circular arrow (162 deg, matching history-line.svg)
tip_x = badge_cx + badge_r * math.cos(math.radians(ang_end))
tip_y = badge_cy + badge_r * math.sin(math.radians(ang_end))
Icon.draw_round_polyline(
    [
        (tip_x, tip_y + 8.8),
        (tip_x, tip_y),
        (tip_x + 8.8, tip_y),
    ],
    width_units=4.2,
    color=Vmware.CYAN,
)

# VMWARE_GREEN clock hands at center
Icon.draw_round_polyline(
    [
        (badge_cx, badge_cy + 10.5),
        (badge_cx, badge_cy),
        (badge_cx + 7.5, badge_cy - 5.2),
    ],
    width_units=4.0,
    color=Vmware.GREEN,
)

save()
