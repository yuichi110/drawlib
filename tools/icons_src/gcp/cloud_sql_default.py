# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""GCP icon: cloud_sql (default 3-tone blue variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import GCP_TECH_LIGHT, GCP_TECH_MED_LIGHT, GCP_TECH_MID, fill_style, setup_icon

setup_icon()

cx = 50.0
x_l, x_r = 18.0, 82.0
dy = 16.0
band_h = 13.5

# 1. Top back walls (drawn behind front V-band)
y_top = 89.0
y_side_top = y_top - dy  # 73.0
polygon(
    [
        (x_l, y_side_top),
        (cx, y_top),
        (cx, y_top - band_h),
        (x_l, y_side_top - band_h),
    ],
    style=fill_style(GCP_TECH_MED_LIGHT),
)
polygon(
    [
        (cx, y_top),
        (x_r, y_side_top),
        (x_r, y_side_top - band_h),
        (cx, y_top - band_h),
    ],
    style=fill_style(GCP_TECH_MID),
)

# 2. Three front V-bands (top, middle, bottom)
for y_apex in (43.5, 27.0, 10.5):
    y_s = y_apex + dy
    polygon(
        [
            (x_l, y_s + band_h),
            (cx, y_apex + band_h),
            (cx, y_apex),
            (x_l, y_s),
        ],
        style=fill_style(GCP_TECH_LIGHT),
    )
    polygon(
        [
            (cx, y_apex + band_h),
            (x_r, y_s + band_h),
            (x_r, y_s),
            (cx, y_apex),
        ],
        style=fill_style(GCP_TECH_MED_LIGHT),
    )

save()
