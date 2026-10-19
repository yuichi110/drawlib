# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""GCP icon: automl_natural_language (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import Gcp, Icon

# ruff: noqa: E501
# fmt: off
Icon.setup()
polygon([(64.1, 25.58), (32.26, 25.58), (28.26, 18.67), (32.26, 11.75), (72.08, 11.75), (92.0, 46.25), (84.02, 60.08)], style=Icon.fill_style(Gcp.TECH_MID))
polygon([(27.92, 88.25), (8.0, 53.75), (15.99, 39.92), (35.9, 74.42), (67.75, 74.42), (71.74, 81.33), (67.75, 88.25)], style=Icon.fill_style(Gcp.TECH_MID))
polygon([(39.3, 56.78), (60.7, 56.78), (60.7, 62.54), (39.3, 62.54)], style=Icon.fill_style(Gcp.TECH_MID))
polygon([(39.3, 46.16), (60.7, 46.16), (60.7, 51.91), (39.3, 51.91)], style=Icon.fill_style(Gcp.TECH_MID))
polygon([(39.3, 35.47), (60.7, 35.47), (60.7, 41.22), (39.3, 41.22)], style=Icon.fill_style(Gcp.TECH_MID))
save()
# fmt: on
