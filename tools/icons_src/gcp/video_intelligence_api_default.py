# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""GCP icon: video_intelligence_api (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import Gcp, Icon

# ruff: noqa: E501
# fmt: off
Icon.setup()
polygon([(68.17, 79.41), (44.98, 79.41), (51.16, 69.62), (59.77, 69.62), (59.77, 64.04), (47.5, 64.04), (37.71, 79.41), (8.0, 79.41), (8.0, 61.22), (16.36, 61.22), (21.66, 71.01), (32.46, 71.01), (36.07, 65.42), (25.27, 65.42), (19.98, 55.63), (8.0, 55.63), (8.0, 44.75), (19.98, 44.75), (25.27, 34.62), (36.07, 34.62), (32.46, 28.99), (21.66, 28.99), (16.36, 38.82), (8.0, 38.82), (8.0, 20.59), (37.71, 20.59), (47.5, 36.01), (59.77, 36.01), (59.77, 30.42), (51.16, 30.42), (44.98, 20.59), (68.17, 20.59), (68.17, 47.23), (41.24, 47.23), (37.75, 41.6), (30.02, 41.6), (35.31, 50.0), (30.02, 58.4), (37.75, 58.4), (41.11, 52.82), (68.17, 52.82)], style=Icon.fill_style(Gcp.TECH_MED_LIGHT))
polygon([(92.0, 74.79), (75.19, 62.56), (75.19, 36.93), (92.0, 24.54)], style=Icon.fill_style(Gcp.TECH_MID))
save()
# fmt: on
