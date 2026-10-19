# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original concept icon: git_repository."""

from drawlib.canvas import save
from drawlib.shapes import circle
from drawlib.utils import Icon

Icon.setup()

w = Icon.ORIG_STROKE

Icon.draw_round_segment((32.0, 20.0), (32.0, 80.0), width_units=w, color=Icon.DARK)
Icon.draw_round_polyline(
    [(32.0, 38.0), (68.0, 38.0), (68.0, 66.0)],
    corner_r=10.0,
    width_units=w,
    color=Icon.DARK,
)

circle(
    (32.0, 22.0),
    radius=9.5,
    style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=w),
)
circle((32.0, 22.0), radius=3.2, style=Icon.fill_style(Icon.WHITE))

circle(
    (32.0, 78.0),
    radius=9.5,
    style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=w),
)
circle((32.0, 78.0), radius=3.2, style=Icon.fill_style(Icon.WHITE))

circle(
    (68.0, 66.0),
    radius=10.5,
    style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=w),
)
circle((68.0, 66.0), radius=3.5, style=Icon.fill_style(Icon.WHITE))

save()
