# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""GCP icon: cloud_run (default 2-tone blue variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import Gcp, Icon

Icon.setup()

# 1. Left speed chevron (upper light blue, lower medium blue)
polygon(
    [(24.0, 49.8), (37.0, 49.8), (27.5, 82.5), (14.5, 89.0)],
    style=Icon.fill_style(Gcp.TECH_LIGHT),
)
polygon(
    [(24.0, 50.0), (37.0, 50.0), (27.5, 17.5), (14.5, 11.0)],
    style=Icon.fill_style(Gcp.TECH_MID),
)

# 2. Right main delta arrowhead (upper light blue, lower medium blue)
polygon(
    [(50.0, 49.8), (89.0, 49.8), (37.0, 89.0)],
    style=Icon.fill_style(Gcp.TECH_LIGHT),
)
polygon(
    [(50.0, 50.0), (89.0, 50.0), (37.0, 11.0)],
    style=Icon.fill_style(Gcp.TECH_MID),
)

save()
