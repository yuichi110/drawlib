# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Client concept icon: external_monitor."""

from drawlib.canvas import save
from drawlib.shapes import rectangle
from drawlib.utils import Icon

Icon.setup()

w = Icon.ORIG_STROKE

# Monitor stand neck and wide base
rectangle(
    (50.0, 26.5),
    width=12.0,
    height=15.0,
    style=Icon.fill_style(Icon.PASTEL_BLUE_LIGHT, border_color=Icon.DARK, border_units=w),
)
rectangle(
    (50.0, 18.0),
    width=36.0,
    height=6.5,
    style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=w, shape_r=3.0),
)

# Widescreen monitor bezel and WHITE display area
rectangle(
    (50.0, 56.5),
    width=74.0,
    height=46.0,
    style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=w, shape_r=5.5),
)
rectangle(
    (50.0, 56.5),
    width=64.0,
    height=36.0,
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=2.0, shape_r=2.5),
)

# PASTEL_GREEN desktop UI window inside screen
rectangle(
    (44.0, 57.5),
    width=38.0,
    height=23.0,
    style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=2.0, shape_r=2.5),
)
Icon.draw_round_segment((25.0, 62.5), (63.0, 62.5), width_units=2.0, color=Icon.DARK)
Icon.draw_round_segment((30.0, 55.5), (53.0, 55.5), width_units=2.0, color=Icon.DARK)
Icon.draw_round_segment((30.0, 50.5), (46.0, 50.5), width_units=2.0, color=Icon.DARK)

# Companion side panel on the right
rectangle(
    (71.5, 57.5),
    width=10.5,
    height=23.0,
    style=Icon.fill_style(Icon.PASTEL_BLUE_LIGHT, border_color=Icon.DARK, border_units=2.0, shape_r=2.0),
)

save()
