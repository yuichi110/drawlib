# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Client vendor icon: microsoft (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import DARK, draw_round_polyline, no_border_fill, setup_icon

# ruff: noqa: E501
# fmt: off
setup_icon()

w = 2.0

panes: list[tuple[list[tuple[float, float]], str]] = [([(9.0, 91.0), (47.95, 91.0), (47.95, 52.05), (9.0, 52.05)], '#F28B82'), ([(52.05, 91.0), (91.0, 91.0), (91.0, 52.05), (52.05, 52.05)], '#81C995'), ([(9.0, 47.95), (47.95, 47.95), (47.95, 9.0), (9.0, 9.0)], '#7BAEF7'), ([(52.05, 47.95), (91.0, 47.95), (91.0, 9.0), (52.05, 9.0)], '#FDD663')]

for pts, fill_col in panes:
    polygon(pts, style=no_border_fill(fill_col))
    draw_round_polyline(pts, width_units=w, color=DARK, closed=True)

save()
# fmt: on
