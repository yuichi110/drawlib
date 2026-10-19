# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Server icon: dell_blade_chassis_default."""

from drawlib.canvas import save
from drawlib.shapes import rectangle
from drawlib.styles import Colors
from drawlib.utils import Dell, Icon

Icon.setup()

BORDER = 4.8

# Outer modular enclosure (outer x=10..90, centerline y=15..85)
rectangle(
    (50.0, 50.0),
    width=80.0 - BORDER,
    height=70.0,
    style=Icon.fill_style(
        Colors.Transparent,
        border_color=Dell.BLUE,
        border_units=BORDER,
        shape_r=2.5,
    ),
)

# Horizontal divider beams at y=65 and y=40 (dividing into 3 horizontal bays)
for beam_y in (65.0, 40.0):
    rectangle(
        (50.0, beam_y),
        width=80.0 - BORDER,
        height=BORDER,
        style=Icon.no_border_fill(Dell.BLUE),
    )

# Middle bay (40..65): wide horizontal blade bar (x=20..80, y=52.5, height=5.0)
rectangle(
    (50.0, 52.5),
    width=60.0,
    height=5.0,
    style=Icon.no_border_fill(Dell.BLUE),
)

# Bottom bay (15..40): left module bar (x=20..36, y=27.5, height=5.0)
rectangle(
    (28.0, 27.5),
    width=16.0,
    height=5.0,
    style=Icon.no_border_fill(Dell.BLUE),
)

save()
