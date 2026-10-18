# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Server vendor icon: netapp (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import (
    DARK,
    draw_round_polyline,
    no_border_fill,
    setup_icon,
)

setup_icon()

w = 2.0
s = 0.95

_RAW_ARCH: list[tuple[float, float]] = [
    (9.0, 83.98),
    (9.0, 16.02),
    (41.18, 16.02),
    (41.18, 56.67),
    (58.76, 56.67),
    (58.76, 16.02),
    (91.0, 16.02),
    (91.0, 83.98),
]

pts = [(50.0 + (x - 50.0) * s, 50.0 + (y - 50.0) * s) for x, y in _RAW_ARCH]

polygon(pts, style=no_border_fill("#4A5568"))
draw_round_polyline(pts, width_units=w, color=DARK, closed=True)

save()
