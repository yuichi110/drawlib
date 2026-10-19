# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original DevOps concept icon: spinnaker."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.styles import Colors
from drawlib.utils import Icon

Icon.setup()

w = 2.0
scale = 0.94


def _sc(x: float, y: float) -> tuple[float, float]:
    return (50.0 + (x - 50.0) * scale, 50.0 + (y - 50.0) * scale)


def _cubic(
    p0: tuple[float, float],
    p1: tuple[float, float],
    p2: tuple[float, float],
    p3: tuple[float, float],
    steps: int = 24,
) -> list[tuple[float, float]]:
    pts: list[tuple[float, float]] = []
    for i in range(1, steps + 1):
        t = i / steps
        mt = 1.0 - t
        pts.append(
            (
                (mt**3) * p0[0] + 3 * (mt**2) * t * p1[0] + 3 * mt * (t**2) * p2[0] + (t**3) * p3[0],
                (mt**3) * p0[1] + 3 * (mt**2) * t * p1[1] + 3 * mt * (t**2) * p2[1] + (t**3) * p3[1],
            )
        )
    return pts


def _build_sail(
    tip: tuple[float, float],
    r_c1: tuple[float, float],
    r_c2: tuple[float, float],
    knee: tuple[float, float],
    b_c1: tuple[float, float],
    b_c2: tuple[float, float],
    tail: tuple[float, float],
    l_c1: tuple[float, float],
    l_c2: tuple[float, float],
) -> list[tuple[float, float]]:
    raw = [
        tip,
        *_cubic(tip, r_c1, r_c2, knee, 18),
        *_cubic(knee, b_c1, b_c2, tail, 24),
        *_cubic(tail, l_c1, l_c2, tip, 24),
    ]
    return [_sc(x, y) for x, y in raw]


# 1. Back large sail (Colors.Blue3)
back_sail = _build_sail(
    tip=(81.92, 91.00),
    r_c1=(87.80, 68.00),
    r_c2=(89.80, 46.50),
    knee=(85.80, 37.20),
    b_c1=(75.50, 24.50),
    b_c2=(42.00, 8.20),
    tail=(11.73, 9.39),
    l_c1=(41.50, 20.50),
    l_c2=(66.50, 54.00),
)

# 2. Middle overlapping sail (Colors.Blue2)
mid_sail = _build_sail(
    tip=(75.40, 81.00),
    r_c1=(80.20, 62.50),
    r_c2=(81.60, 45.80),
    knee=(78.40, 38.60),
    b_c1=(69.80, 27.80),
    b_c2=(43.20, 15.20),
    tail=(20.40, 15.40),
    l_c1=(44.80, 26.80),
    l_c2=(63.20, 53.00),
)

# 3. Front overlapping sail (Colors.Teal3)
front_sail = _build_sail(
    tip=(69.07, 71.18),
    r_c1=(72.80, 57.50),
    r_c2=(73.20, 44.80),
    knee=(71.20, 39.91),
    b_c1=(64.50, 31.20),
    b_c2=(46.20, 21.50),
    tail=(28.82, 21.33),
    l_c1=(48.20, 32.80),
    l_c2=(60.50, 52.00),
)

for sail_pts, fill_col in (
    (back_sail, Colors.Blue3),
    (mid_sail, Colors.Blue2),
    (front_sail, Colors.Teal3),
):
    polygon(sail_pts, style=Icon.no_border_fill(fill_col))
    Icon.draw_round_polyline(sail_pts, width_units=w, color=Icon.DARK, closed=True)

save()
