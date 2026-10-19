# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""GCP icon: cloud_functions."""

import math

from drawlib.canvas import save
from drawlib.shapes import circle, polygon
from drawlib.utils import Gcp, Icon

Icon.setup()

x_out = 8.0
x_in = 21.0
w = x_in - x_out
y_fold_out_top = 58.5
y_fold_in_top = y_fold_out_top + w
y_corner_out_top = y_fold_in_top + w * math.sqrt(2.0) - w
arm_len = 13.6
x_cap_in = x_in + arm_len
y_cap_in = y_fold_in_top + arm_len
cap_dx = w / math.sqrt(2.0)
x_cap_out = x_cap_in - cap_dx
y_cap_out = y_cap_in + cap_dx
y_dark_btm_top = 66.2


def _draw_bracket(mirror_x: bool) -> None:
    def tx(x: float, y: float) -> tuple[float, float]:
        return (100.0 - x if mirror_x else x, y)

    mid_pts = [
        tx(x_out, 100.0 - y_fold_out_top),
        tx(x_out, y_fold_out_top),
        tx(x_in, y_dark_btm_top + 0.8),
        tx(x_in, 100.0 - (y_dark_btm_top + 0.8)),
    ]
    polygon(mid_pts, style=Icon.fill_style(Gcp.TECH_MED_LIGHT))

    top_dark = [
        tx(x_out, y_fold_out_top),
        tx(x_in, y_fold_in_top + 0.8),
        tx(x_in, y_dark_btm_top),
    ]
    btm_dark = [(px, 100.0 - py) for (px, py) in top_dark]
    polygon(top_dark, style=Icon.fill_style(Gcp.TECH_MID))
    polygon(btm_dark, style=Icon.fill_style(Gcp.TECH_MID))

    top_arm = [
        tx(x_out, y_fold_out_top),
        tx(x_out, y_corner_out_top),
        tx(x_cap_out, y_cap_out),
        tx(x_cap_in, y_cap_in),
    ]
    btm_arm = [(px, 100.0 - py) for (px, py) in top_arm]
    polygon(top_arm, style=Icon.fill_style(Gcp.TECH_LIGHT))
    polygon(btm_arm, style=Icon.fill_style(Gcp.TECH_LIGHT))


_draw_bracket(mirror_x=False)
_draw_bracket(mirror_x=True)

st_dot = Icon.fill_style(Gcp.TECH_LIGHT)
for xc in (31.0, 50.0, 69.0):
    circle((xc, 50.0), radius=4.9, style=st_dot)

save()
