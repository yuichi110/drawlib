# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""GCP icon: cloud_router (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import Gcp, Icon

# ruff: noqa: E501
# fmt: off
Icon.setup()
polygon([(79.4, 41.6), (79.4, 29.0), (58.4, 50.0), (79.4, 71.0), (79.4, 58.4), (92.0, 58.4), (92.0, 41.6)], style=Icon.fill_style(Gcp.TECH_MID))
polygon([(20.6, 58.4), (8.0, 58.4), (8.0, 41.6), (20.6, 41.6), (20.6, 29.0), (41.6, 50.0), (20.6, 71.0)], style=Icon.fill_style(Gcp.TECH_MID))
polygon([(58.4, 29.0), (58.4, 41.6), (41.6, 41.6), (41.6, 29.0), (29.0, 29.0), (50.0, 8.0), (71.0, 29.0)], style=Icon.fill_style(Gcp.TECH_MID))
polygon([(58.4, 71.0), (58.4, 58.4), (41.6, 58.4), (41.6, 71.0), (29.0, 71.0), (50.0, 92.0), (71.0, 71.0)], style=Icon.fill_style(Gcp.TECH_MID))
save()
# fmt: on
