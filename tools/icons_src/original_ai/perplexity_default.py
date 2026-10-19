# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original AI concept icon: perplexity."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.styles import Colors
from drawlib.utils import Icon

Icon.setup()

cx, cy = 50.0, 50.0
scale = 0.95


def _s(pts: list[tuple[float, float]]) -> list[tuple[float, float]]:
    return [(cx + (x - cx) * scale, cy + (y - cy) * scale) for x, y in pts]


# Exact 7-ring compound polygon from official Perplexity logo (scaled by 0.95 around (50, 50))
raw_outer_frame: list[tuple[float, float]] = [
    (76.6, 91.0),
    (76.6, 66.15),
    (85.88, 66.15),
    (85.88, 30.8),
    (75.85, 30.8),
    (75.85, 9.0),
    (51.8, 30.16),
    (51.8, 9.17),
    (48.08, 9.17),
    (48.08, 30.19),
    (24.01, 9.0),
    (24.01, 31.09),
    (14.12, 31.09),
    (14.12, 66.44),
    (23.98, 66.44),
    (23.98, 91.0),
    (48.08, 68.81),
    (48.08, 90.35),
    (51.8, 90.35),
    (51.8, 68.18),
]

raw_window_panes: list[list[tuple[float, float]]] = [
    [(51.8, 60.1), (51.8, 35.09), (72.12, 17.21), (72.12, 41.66)],
    [(48.05, 60.37), (27.73, 41.93), (27.73, 17.21), (48.05, 35.09)],
    [(75.85, 34.47), (82.15, 34.47), (82.15, 62.47), (54.99, 62.47), (75.85, 43.55)],
    [(45.16, 62.76), (17.85, 62.76), (17.85, 34.77), (24.0, 34.77), (24.0, 43.57), (45.16, 62.77)],
    [(27.71, 82.54), (27.71, 66.45), (45.18, 66.45)],
    [(72.87, 82.54), (55.39, 66.45), (72.87, 66.45)],
]

outer_frame = _s(raw_outer_frame)
window_panes = [_s(pane) for pane in raw_window_panes]

# 1. Fill the crystal bar frame in unified Colors.Teal3 with transparent window pane cutouts
polygon(outer_frame, holes=window_panes, style=Icon.fill_style(Colors.Teal3))

# 3. Crisp DARK outlines along outer crystal bar perimeter and inner window pane cutouts
Icon.draw_round_polyline(outer_frame, width_units=2.0, color=Icon.DARK, closed=True)
for pane in window_panes:
    Icon.draw_round_polyline(pane, width_units=2.0, color=Icon.DARK, closed=True)

save()
