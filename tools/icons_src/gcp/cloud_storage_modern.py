# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""GCP icon: cloud_storage."""

from drawlib.canvas import save
from drawlib.shapes import circle, rectangle
from drawlib.utils import Gcp, Icon

Icon.setup()


def _draw_storage_unit(
    y_btm: float,
    y_top: float,
    *,
    top_right_color: str,
    btm_left_color: str,
) -> None:
    x_left = 8.0
    x_right = 92.0
    t = 7.0
    r = 3.8
    x_div0, x_div1 = 31.5, 38.5

    Gcp.draw_rounded_corner_block(
        x_left,
        y_btm,
        x_left + t,
        y_top - t + 0.5,
        r=r,
        round_bl=True,
        color=btm_left_color,
    )
    Gcp.draw_rounded_corner_block(
        x_left,
        y_btm,
        x_right - t + 0.5,
        y_btm + t,
        r=r,
        round_bl=True,
        color=btm_left_color,
    )
    rectangle(
        ((x_div0 + x_div1) / 2.0, (y_btm + y_top) / 2.0),
        width=x_div1 - x_div0,
        height=(y_top - y_btm) - 2.0 * t + 1.0,
        style=Icon.fill_style(btm_left_color),
    )

    Gcp.draw_rounded_corner_block(
        x_left,
        y_top - t,
        x_right,
        y_top,
        r=r,
        round_tl=True,
        round_tr=True,
        color=top_right_color,
    )
    Gcp.draw_rounded_corner_block(
        x_right - t,
        y_btm,
        x_right,
        y_top,
        r=r,
        round_tr=True,
        round_br=True,
        color=top_right_color,
    )

    circle(
        (68.5, (y_btm + y_top) / 2.0),
        radius=7.8,
        style=Icon.fill_style(top_right_color),
    )


_draw_storage_unit(55.0, 88.0, top_right_color=Gcp.RED, btm_left_color=Gcp.YELLOW)
_draw_storage_unit(12.0, 45.0, top_right_color=Gcp.BLUE, btm_left_color=Gcp.GREEN)

save()
