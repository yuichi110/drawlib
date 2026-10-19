# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Data concept icon: influxdb."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.styles import Colors
from drawlib.utils import Icon

Icon.setup()

w = 2.0

# Outer 6-sided faceted crystal perimeter
p1 = (38.8, 89.0)  # top
p2 = (79.0, 77.0)  # upper-right
p3 = (88.5, 40.4)  # lower-right
p4 = (56.5, 11.0)  # bottom
p5 = (19.9, 22.4)  # bottom-left
p6 = (11.5, 61.4)  # upper-left

# Inner central triangle vertices
t1 = (55.9, 72.2)  # top-inner
t2 = (64.6, 34.1)  # right-inner
t3 = (26.5, 45.2)  # left-inner

# 1. Fill the 7 crystal facets
# Central triangle facet (Colors.Teal3)
polygon([t1, t2, t3], style=Icon.no_border_fill(Colors.Teal3))

# Three main broad quadrilateral side facets (Colors.Blue3, Colors.Blue4, Colors.Purple3)
polygon([p6, p1, t1, t3], style=Icon.no_border_fill(Colors.Blue3))
polygon([t1, p2, p3, t2], style=Icon.no_border_fill(Colors.Blue4))
polygon([t3, t2, p4, p5], style=Icon.no_border_fill(Colors.Purple3))

# Three angled corner bevel triangles (Colors.Teal1 top highlight + Colors.Blue2 side bevels)
polygon([p1, p2, t1], style=Icon.no_border_fill(Colors.Teal1))
polygon([t2, p3, p4], style=Icon.no_border_fill(Colors.Blue2))
polygon([p6, t3, p5], style=Icon.no_border_fill(Colors.Blue2))

# 2. Internal facet seam lines
Icon.draw_round_polyline([t1, t2, t3], width_units=1.8, color=Icon.DARK, closed=True)
for inner_pt, outer_pt in ((t1, p1), (t1, p2), (t2, p3), (t2, p4), (t3, p5), (t3, p6)):
    Icon.draw_round_segment(inner_pt, outer_pt, width_units=1.8, color=Icon.DARK)

# 3. Outer crystal border
Icon.draw_round_polyline([p1, p2, p3, p4, p5, p6], width_units=w, color=Icon.DARK, closed=True)

save()
