# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original AI concept icon: jupyter."""

from drawlib.canvas import save
from drawlib.shapes import circle, polygon
from drawlib.styles import Colors
from drawlib.utils import (
    DARK,
    draw_round_polyline,
    fill_style,
    no_border_fill,
    setup_icon,
)

setup_icon()

w = 1.9
scale = 0.945


def _sc_pt(x: float, y: float) -> tuple[float, float]:
    """Scale a point around canvas center (50.0, 50.0)."""
    return (50.0 + (x - 50.0) * scale, 50.0 + (y - 50.0) * scale)


def _sc(pts: list[tuple[float, float]]) -> list[tuple[float, float]]:
    """Scale a list of points around canvas center (50.0, 50.0)."""
    return [_sc_pt(x, y) for x, y in pts]


# 1. Top and bottom central crescents (Colors.Orange3)
bottom_crescent = _sc(
    [
        (51.13, 28.99),
        (46.38, 29.21),
        (41.83, 29.84),
        (37.53, 30.85),
        (33.51, 32.23),
        (29.82, 33.92),
        (26.50, 35.92),
        (23.60, 38.19),
        (21.16, 40.70),
        (23.13, 36.18),
        (25.76, 32.03),
        (29.00, 28.32),
        (32.76, 25.16),
        (36.95, 22.62),
        (41.49, 20.77),
        (46.25, 19.63),
        (51.13, 19.25),
        (56.02, 19.64),
        (60.78, 20.77),
        (65.32, 22.62),
        (69.51, 25.16),
        (73.27, 28.32),
        (76.51, 32.03),
        (79.14, 36.18),
        (81.10, 40.70),
        (78.66, 38.19),
        (75.76, 35.92),
        (72.44, 33.92),
        (68.75, 32.23),
        (64.73, 30.85),
        (60.42, 29.84),
        (55.87, 29.21),
    ]
)

top_crescent = _sc(
    [
        (51.12, 74.42),
        (55.87, 74.21),
        (60.41, 73.57),
        (64.72, 72.56),
        (68.74, 71.19),
        (72.43, 69.49),
        (75.75, 67.49),
        (78.65, 65.23),
        (81.08, 62.72),
        (79.12, 67.23),
        (76.49, 71.39),
        (73.25, 75.09),
        (69.49, 78.26),
        (65.30, 80.79),
        (60.76, 82.65),
        (56.00, 83.78),
        (51.12, 84.16),
        (46.23, 83.78),
        (41.47, 82.65),
        (36.94, 80.79),
        (32.75, 78.26),
        (28.98, 75.09),
        (25.74, 71.39),
        (23.11, 67.23),
        (21.15, 62.72),
        (23.59, 65.22),
        (26.49, 67.49),
        (29.81, 69.48),
        (33.50, 71.18),
        (37.52, 72.56),
        (41.83, 73.57),
        (46.38, 74.20),
    ]
)

for crescent in (bottom_crescent, top_crescent):
    polygon(crescent, style=no_border_fill(Colors.Orange3))
    draw_round_polyline(crescent, width_units=w, color=DARK, closed=True)

# 2. Three satellite moons (top-right Gray5, bottom-left Gray4, top-left Gray5)
circle(
    _sc_pt(74.49, 86.13),
    radius=4.86 * scale,
    style=fill_style(Colors.Gray5, border_color=DARK, border_units=w),
)
circle(
    _sc_pt(27.36, 15.15),
    radius=6.12 * scale,
    style=fill_style(Colors.Gray4, border_color=DARK, border_units=w),
)
circle(
    _sc_pt(22.48, 79.61),
    radius=3.60 * scale,
    style=fill_style(Colors.Gray5, border_color=DARK, border_units=w),
)

save()
