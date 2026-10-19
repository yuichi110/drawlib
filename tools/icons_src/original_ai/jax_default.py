# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original AI concept icon: jax."""

import math

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.styles import Colors
from drawlib.utils import Icon

Icon.setup()

w = 2.0
w_seam = 1.45

# 60-degree isometric lattice: ix in [0..18], iy in [0..6], centered at (9, 3) -> (50.0, 50.0)
dx = 78.0 / 18.0
dy = dx * math.sqrt(3.0)


def _iso(ix: float, iy: float) -> tuple[float, float]:
    """Map integer isometric lattice coordinates (ix, iy) to canvas coordinates."""
    return (50.0 + (ix - 9.0) * dx, 50.0 + (iy - 3.0) * dy)


# 1. Letter "J" facets (Blue2 top faces, Blue3 front/right faces)
polygon([_iso(1, 2), _iso(2, 3), _iso(4, 3), _iso(3, 2)], style=Icon.no_border_fill(Colors.Blue3))
polygon([_iso(0, 1), _iso(1, 2), _iso(7, 2), _iso(6, 1)], style=Icon.no_border_fill(Colors.Blue3))
polygon([_iso(5, 2), _iso(9, 6), _iso(11, 6), _iso(7, 2)], style=Icon.no_border_fill(Colors.Blue3))
polygon([_iso(0, 1), _iso(6, 1), _iso(7, 0), _iso(1, 0)], style=Icon.no_border_fill(Colors.Blue4))
polygon([_iso(3, 2), _iso(4, 3), _iso(5, 2)], style=Icon.no_border_fill(Colors.Blue4))

# 2. Letter "A" facets (Teal2 top crossbar, Teal3 right-facing walls, Teal4 down-left undersides)
polygon([_iso(7, 2), _iso(8, 3), _iso(12, 3), _iso(11, 2)], style=Icon.no_border_fill(Colors.Teal2))
polygon([_iso(6, 1), _iso(7, 2), _iso(8, 1), _iso(7, 0)], style=Icon.no_border_fill(Colors.Teal3))
polygon([_iso(8, 3), _iso(10, 5), _iso(11, 4), _iso(10, 3)], style=Icon.no_border_fill(Colors.Teal3))
polygon([_iso(10, 5), _iso(12, 5), _iso(14, 3), _iso(12, 3)], style=Icon.no_border_fill(Colors.Teal4))
polygon([_iso(7, 2), _iso(11, 2), _iso(10, 1), _iso(8, 1)], style=Icon.no_border_fill(Colors.Teal4))
polygon([_iso(14, 1), _iso(15, 2), _iso(17, 0), _iso(15, 0)], style=Icon.no_border_fill(Colors.Teal4))

# 3. Letter "X" facets (Purple2 top/left faces, Purple3 right faces, Purple4 bottom foot)
polygon([_iso(10, 5), _iso(11, 6), _iso(13, 6), _iso(12, 5)], style=Icon.no_border_fill(Colors.Purple2))
polygon([_iso(10, 1), _iso(12, 3), _iso(14, 3), _iso(12, 1)], style=Icon.no_border_fill(Colors.Purple2))
polygon([_iso(15, 4), _iso(14, 5), _iso(15, 6), _iso(17, 6)], style=Icon.no_border_fill(Colors.Purple2))
polygon([_iso(12, 5), _iso(13, 6), _iso(18, 1), _iso(17, 0)], style=Icon.no_border_fill(Colors.Purple3))
polygon([_iso(15, 4), _iso(17, 6), _iso(18, 5), _iso(16, 3)], style=Icon.no_border_fill(Colors.Purple3))
polygon([_iso(12, 1), _iso(14, 3), _iso(15, 2), _iso(13, 0)], style=Icon.no_border_fill(Colors.Purple3))
polygon([_iso(10, 1), _iso(12, 1), _iso(13, 0), _iso(11, 0)], style=Icon.no_border_fill(Colors.Purple4))

# 4. Inner triangle hole of "A" (transparent cutout)
a_hole = [_iso(10, 3), _iso(11, 4), _iso(12, 3)]

# 5. Inner isometric fold and seam lines
seams = [
    (_iso(1, 2), _iso(3, 2)),
    (_iso(3, 2), _iso(4, 3)),
    (_iso(3, 2), _iso(5, 2)),
    (_iso(5, 2), _iso(7, 2)),
    (_iso(0, 1), _iso(6, 1)),
    (_iso(6, 1), _iso(7, 2)),
    (_iso(6, 1), _iso(7, 0)),
    (_iso(7, 2), _iso(8, 1)),
    (_iso(7, 2), _iso(11, 2)),
    (_iso(8, 3), _iso(10, 3)),
    (_iso(7, 2), _iso(10, 5)),
    (_iso(10, 5), _iso(11, 4)),
    (_iso(10, 5), _iso(11, 6)),
    (_iso(10, 5), _iso(12, 5)),
    (_iso(12, 5), _iso(13, 6)),
    (_iso(12, 5), _iso(14, 3)),
    (_iso(12, 3), _iso(14, 3)),
    (_iso(10, 1), _iso(12, 3)),
    (_iso(10, 1), _iso(12, 1)),
    (_iso(12, 1), _iso(14, 3)),
    (_iso(12, 1), _iso(13, 0)),
    (_iso(14, 1), _iso(15, 2)),
    (_iso(15, 2), _iso(17, 0)),
    (_iso(14, 3), _iso(15, 2)),
    (_iso(14, 5), _iso(15, 4)),
    (_iso(15, 4), _iso(17, 6)),
    (_iso(15, 4), _iso(16, 3)),
]
for p1, p2 in seams:
    Icon.draw_round_segment(p1, p2, width_units=w_seam, color=Icon.DARK)

# 6. Bold outer silhouette and inner "A" hole borders
Icon.draw_round_polyline(a_hole, width_units=w, color=Icon.DARK, closed=True)

outer_contour = [
    _iso(0, 1),
    _iso(2, 3),
    _iso(4, 3),
    _iso(5, 2),
    _iso(9, 6),
    _iso(13, 6),
    _iso(14, 5),
    _iso(15, 6),
    _iso(17, 6),
    _iso(18, 5),
    _iso(16, 3),
    _iso(18, 1),
    _iso(17, 0),
    _iso(15, 0),
    _iso(14, 1),
    _iso(13, 0),
    _iso(11, 0),
    _iso(10, 1),
    _iso(8, 1),
    _iso(7, 0),
    _iso(1, 0),
]
Icon.draw_round_polyline(outer_contour, width_units=w, color=Icon.DARK, closed=True)

save()
