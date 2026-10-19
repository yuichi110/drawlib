# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""GCP icon: anthos (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import Gcp, Icon

# ruff: noqa: E501
# fmt: off
Icon.setup()
polygon([(29.0, 36.7), (50.0, 73.45), (71.0, 36.7), (88.5, 19.2), (89.2, 18.5), (50.0, 86.4), (10.8, 18.5), (11.5, 19.2)], style=Icon.fill_style(Gcp.TECH_MID))
polygon([(50.0, 58.05), (11.5, 19.2), (27.6, 26.55), (50.0, 48.95), (72.4, 26.55), (88.5, 19.2)], style=Icon.fill_style(Gcp.TECH_MID))
polygon([(29.0, 19.9), (14.3, 13.6), (85.7, 13.6), (71.0, 19.9)], style=Icon.fill_style(Gcp.TECH_MID))
polygon([(88.5, 19.2), (50.0, 36.7), (11.5, 19.2), (8.0, 13.6), (14.3, 13.6), (50.0, 29.7), (85.7, 13.6), (92.0, 13.6)], style=Icon.fill_style(Gcp.TECH_MID))
save()
# fmt: on
