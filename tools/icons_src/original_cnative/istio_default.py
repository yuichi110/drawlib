# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Cloud Native concept icon: istio."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import Icon

Icon.setup()

w = Icon.ORIG_STROKE

# Left jib sail (WHITE)
jib_pts = [
    (20.0, 29.5),
    (41.5, 33.0),
    (41.5, 70.0),
]
polygon(jib_pts, style=Icon.no_border_fill(Icon.WHITE))
Icon.draw_round_polyline(jib_pts, width_units=w, color=Icon.DARK, closed=True)

# Right main sail (PASTEL_BLUE)
main_pts = [
    (47.0, 33.0),
    (80.0, 29.5),
    (47.0, 86.5),
]
polygon(main_pts, style=Icon.no_border_fill(Icon.PASTEL_BLUE))
Icon.draw_round_polyline(main_pts, width_units=w, color=Icon.DARK, closed=True)

# Bottom tapered sailboat hull (PASTEL_GREEN)
hull_pts = [
    (20.0, 24.0),
    (80.0, 24.0),
    (44.0, 12.5),
]
polygon(hull_pts, style=Icon.no_border_fill(Icon.PASTEL_GREEN))
Icon.draw_round_polyline(hull_pts, width_units=w, color=Icon.DARK, closed=True)

save()
