# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Workspace concept icon: dropbox."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import DARK, draw_round_polyline, no_border_fill, setup_icon

setup_icon()
w = 1.9
pastel_blue = "#66A3FF"

diamonds = [
    [(30.6, 82.97), (11.2, 70.61), (30.6, 58.25), (50.0, 70.61)],
    [(69.4, 82.97), (50.0, 70.61), (69.4, 58.25), (88.8, 70.61)],
    [(11.2, 45.89), (30.6, 33.53), (50.0, 45.89), (30.6, 58.25)],
    [(69.4, 58.25), (50.0, 45.89), (69.4, 33.53), (88.8, 45.89)],
    [(30.6, 29.39), (50.0, 17.03), (69.4, 29.39), (50.0, 41.75)],
]

for pts in diamonds:
    polygon(pts, style=no_border_fill(pastel_blue))
    draw_round_polyline(pts, width_units=w, color=DARK, closed=True)

save()
