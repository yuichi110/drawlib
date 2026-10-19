# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Facility concept icon: warehouse."""

from drawlib.canvas import save
from drawlib.shapes import polygon, rectangle
from drawlib.utils import Icon

Icon.setup()

w_outer = 2.0
w_inner = 1.6

# 1. Main warehouse wall (WHITE gable pentagon, x=15..85, y=16..76)
wall_pts = [
    (15.0, 16.0),
    (85.0, 16.0),
    (85.0, 56.0),
    (50.0, 76.0),
    (15.0, 56.0),
]
polygon(wall_pts, style=Icon.no_border_fill(Icon.WHITE))
Icon.draw_round_polyline(wall_pts, width_units=w_outer, color=Icon.DARK, closed=True)

# 2. Wide gable roof fascia (PASTEL_BLUE, overhanging eaves x=11..89)
roof_pts = [
    (11.0, 57.5),
    (50.0, 80.0),
    (89.0, 57.5),
    (86.0, 52.0),
    (50.0, 73.0),
    (14.0, 52.0),
]
polygon(roof_pts, style=Icon.no_border_fill(Icon.PASTEL_BLUE))
Icon.draw_round_polyline(roof_pts, width_units=w_outer, color=Icon.DARK, closed=True)

# 3. Upper gable vent window (PASTEL_BLUE_LIGHT)
rectangle(
    (50.0, 62.5),
    width=18.0,
    height=5.0,
    style=Icon.fill_style(Icon.PASTEL_BLUE_LIGHT, border_color=Icon.DARK, border_units=w_inner, shape_r=1.5),
)

# 4. Open loading bay interior (PASTEL_BLUE_LIGHT, x=26..74, y=16..52)
rectangle(
    (50.0, 34.0),
    width=48.0,
    height=36.0,
    style=Icon.fill_style(Icon.PASTEL_BLUE_LIGHT, border_color=Icon.DARK, border_units=w_outer),
)

# Roll-up shutter header at top of bay (PASTEL_BLUE, y=45..52)
rectangle(
    (50.0, 48.5),
    width=48.0,
    height=7.0,
    style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=w_outer),
)
Icon.draw_round_segment((26.5, 48.5), (73.5, 48.5), width_units=w_inner, color=Icon.DARK)

# 5. Three stacked PASTEL_GREEN boxes inside open bay
boxes = [
    (39.0, 23.0, 18.0, 14.0),
    (61.0, 23.0, 18.0, 14.0),
    (50.0, 37.0, 18.0, 14.0),
]
for bx, by, bw, bh in boxes:
    rectangle(
        (bx, by),
        width=bw,
        height=bh,
        style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=w_outer, shape_r=1.2),
    )
    # White packing tape strip at top center of each box
    rectangle(
        (bx, by + bh / 2.0 - 2.5),
        width=5.0,
        height=5.0,
        style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w_inner),
    )

# 6. Ground foundation bar (PASTEL_BLUE)
rectangle(
    (50.0, 14.5),
    width=78.0,
    height=3.5,
    style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=w_outer, shape_r=1.5),
)

save()
