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
from drawlib.utils import Icon

# ruff: noqa: E501
# fmt: off
Icon.setup()

w = 2.0

panes: list[tuple[list[tuple[float, float]], str]] = [([(9.0, 91.0), (47.95, 91.0), (47.95, 52.05), (9.0, 52.05)], '#F26458'), ([(52.05, 91.0), (91.0, 91.0), (91.0, 52.05), (52.05, 52.05)], '#71C789'), ([(9.0, 47.95), (47.95, 47.95), (47.95, 9.0), (9.0, 9.0)], '#5797F2'), ([(52.05, 47.95), (91.0, 47.95), (91.0, 9.0), (52.05, 9.0)], '#F2C94F')]

for pts, fill_col in panes:
    polygon(pts, style=Icon.no_border_fill(fill_col))
    Icon.draw_round_polyline(pts, width_units=w, color=Icon.DARK, closed=True)

save()
# fmt: on
