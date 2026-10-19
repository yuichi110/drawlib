# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Workspace concept icon: spreadsheet."""

import math

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import Icon

Icon.setup()

w_outer = 2.0
w_inner = 1.6


def _arc_pts(
    cx: float,
    cy: float,
    r: float,
    deg_start: float,
    deg_end: float,
    steps: int = 10,
) -> list[tuple[float, float]]:
    return [
        (
            cx + r * math.cos(math.radians(deg_start + (deg_end - deg_start) * (i / steps))),
            cy + r * math.sin(math.radians(deg_start + (deg_end - deg_start) * (i / steps))),
        )
        for i in range(steps + 1)
    ]


x0, y0, x1, y1 = 15.0, 16.0, 85.0, 84.0
x_idx = 35.0
y_hdr = 67.0
r_sheet = 5.0

# 1. Base WHITE table sheet
sheet_pts: list[tuple[float, float]] = [
    *_arc_pts(x0 + r_sheet, y0 + r_sheet, r_sheet, 180.0, 270.0),
    *_arc_pts(x1 - r_sheet, y0 + r_sheet, r_sheet, 270.0, 360.0),
    *_arc_pts(x1 - r_sheet, y1 - r_sheet, r_sheet, 0.0, 90.0),
    *_arc_pts(x0 + r_sheet, y1 - r_sheet, r_sheet, 90.0, 180.0),
]
polygon(sheet_pts, style=Icon.no_border_fill(Icon.WHITE))

# 2. Left index column (PASTEL_BLUE_LIGHT)
idx_pts: list[tuple[float, float]] = [
    *_arc_pts(x0 + r_sheet, y0 + r_sheet, r_sheet, 180.0, 270.0),
    (x_idx, y0),
    (x_idx, y_hdr),
    (x0, y_hdr),
]
polygon(idx_pts, style=Icon.no_border_fill(Icon.PASTEL_BLUE_LIGHT))

# 3. Top header bar (PASTEL_GREEN)
hdr_pts: list[tuple[float, float]] = [
    (x0, y_hdr),
    (x1, y_hdr),
    *_arc_pts(x1 - r_sheet, y1 - r_sheet, r_sheet, 0.0, 90.0),
    *_arc_pts(x0 + r_sheet, y1 - r_sheet, r_sheet, 90.0, 180.0),
]
polygon(hdr_pts, style=Icon.no_border_fill(Icon.PASTEL_GREEN))

# 4. Crisp DARK interior grid lines
Icon.draw_round_segment((x0, 50.0), (x1, 50.0), width_units=w_inner, color=Icon.DARK)
Icon.draw_round_segment((x0, 33.0), (x1, 33.0), width_units=w_inner, color=Icon.DARK)
Icon.draw_round_segment((60.0, y0), (60.0, y1), width_units=w_inner, color=Icon.DARK)

# 5. Main dividers and outer border
Icon.draw_round_segment((x_idx, y0), (x_idx, y1), width_units=w_outer, color=Icon.DARK)
Icon.draw_round_segment((x0, y_hdr), (x1, y_hdr), width_units=w_outer, color=Icon.DARK)
Icon.draw_round_polyline(sheet_pts, width_units=w_outer, color=Icon.DARK, closed=True)

save()
