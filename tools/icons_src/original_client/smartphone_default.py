# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Client concept icon: smartphone."""

from drawlib.canvas import save
from drawlib.shapes import rectangle
from drawlib.utils import Icon

Icon.setup()

w = Icon.ORIG_STROKE

# Vertical phone body
rectangle(
    (50.0, 50.0),
    width=42.0,
    height=74.0,
    style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=w, shape_r=8.0),
)

# Inner WHITE screen
rectangle(
    (50.0, 50.5),
    width=33.0,
    height=55.0,
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=2.0, shape_r=3.5),
)

# Top earpiece speaker and bottom gesture bar
Icon.draw_round_segment((46.0, 82.5), (54.0, 82.5), width_units=2.0, color=Icon.DARK)
Icon.draw_round_segment((44.0, 18.0), (56.0, 18.0), width_units=2.0, color=Icon.DARK)

# App grid with prominent PASTEL_GREEN app badge
rectangle(
    (43.5, 66.0),
    width=10.5,
    height=10.5,
    style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=2.0, shape_r=2.5),
)
for ax, ay in ((56.5, 66.0), (43.5, 52.5), (56.5, 52.5)):
    rectangle(
        (ax, ay),
        width=10.5,
        height=10.5,
        style=Icon.fill_style(Icon.PASTEL_BLUE_LIGHT, border_color=Icon.DARK, border_units=2.0, shape_r=2.5),
    )

# Bottom notification lines on screen
Icon.draw_round_segment((39.0, 38.0), (61.0, 38.0), width_units=2.0, color=Icon.DARK)
Icon.draw_round_segment((39.0, 31.5), (53.0, 31.5), width_units=2.0, color=Icon.DARK)

save()
