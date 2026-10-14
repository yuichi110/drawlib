# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""GCP icon: connectivity_test (default variant)."""

from drawlib.canvas import save
from drawlib.lines import lines
from drawlib.utils import GCP_TECH_MID, setup_icon, stroke_style

# ruff: noqa: E501
# fmt: off
setup_icon()
lines([(85.37, 87.58), (14.63, 47.79), (14.63, 75.57)], style=stroke_style(GCP_TECH_MID, width_units=8.84))
lines([(14.63, 12.42), (85.37, 52.21), (85.37, 24.43)], style=stroke_style(GCP_TECH_MID, width_units=8.84))
save()
# fmt: on
