# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""GCP icon: stackdriver (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import Gcp, Icon

# ruff: noqa: E501
# fmt: off
Icon.setup()
polygon([(46.51, 52.8), (66.15, 86.57), (27.38, 86.57), (8.0, 52.8)], style=Icon.fill_style(Gcp.TECH_LIGHT))
polygon([(8.0, 47.2), (27.34, 13.43), (66.07, 13.43), (46.77, 47.2)], style=Icon.fill_style(Gcp.TECH_MID))
polygon([(92.0, 50.0), (72.62, 83.9), (53.19, 50.0), (72.62, 16.1)], style=Icon.fill_style(Gcp.TECH_MED_LIGHT))
save()
# fmt: on
