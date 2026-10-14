# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""GCP icon: stream_suite (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import GCP_TECH_MID, fill_style, setup_icon, stroke_style

# ruff: noqa: E501
# fmt: off
setup_icon()
polygon([(32.11, 78.53), (75.67, 78.53), (70.9, 71.75), (27.2, 71.75)], style=fill_style(GCP_TECH_MID))
polygon([(22.51, 64.69), (66.07, 64.69), (61.3, 57.92), (17.6, 57.92)], style=fill_style(GCP_TECH_MID))
polygon([(12.91, 50.86), (56.47, 50.86), (51.7, 44.08), (8.0, 44.08)], style=fill_style(GCP_TECH_MID))
polygon([(57.97, 27.14), (57.88, 26.02), (57.58, 24.92), (57.1, 23.9), (56.45, 22.97), (55.65, 22.17), (54.73, 21.52), (53.7, 21.04), (52.61, 20.75), (51.48, 20.65), (50.35, 20.75), (49.26, 21.04), (48.23, 21.52), (47.31, 22.17), (46.51, 22.97), (45.86, 23.9), (45.38, 24.92), (45.08, 26.02), (44.99, 27.14), (45.08, 28.27), (45.38, 29.36), (45.86, 30.39), (46.51, 31.32), (47.31, 32.12), (48.23, 32.77), (49.26, 33.25), (50.35, 33.54), (51.48, 33.64), (52.61, 33.54), (53.7, 33.25), (54.73, 32.77), (55.65, 32.12), (56.45, 31.32), (57.1, 30.39), (57.58, 29.36), (57.88, 28.27)], style=stroke_style(GCP_TECH_MID, width_units=6.78))
polygon([(53.2, 35.34), (86.36, 82.74), (92.0, 78.79), (58.83, 31.39)], style=fill_style(GCP_TECH_MID))
save()
# fmt: on
