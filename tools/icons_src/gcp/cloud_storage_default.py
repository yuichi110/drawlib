# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""GCP icon: cloud_storage (default 3-tone blue variant)."""

from drawlib.canvas import save
from drawlib.shapes import circle, polygon, rectangle
from drawlib.utils import Gcp, Icon

Icon.setup()


def _draw_legacy_storage_tier(y0: float, y1: float) -> None:
    ym = (y0 + y1) / 2.0
    h = y1 - y0

    # Center light-blue body
    rectangle((50.0, ym), width=67.0, height=h, style=Icon.fill_style(Gcp.TECH_LIGHT))

    # Left medium-light cap (x in [8.0, 16.5])
    rectangle((12.25, ym), width=8.5, height=h, style=Icon.fill_style(Gcp.TECH_MED_LIGHT))

    # Right two-tone cap (x in [83.5, 92.0])
    polygon([(83.5, y0), (83.5, y1), (92.0, y1)], style=Icon.fill_style(Gcp.TECH_MID))
    polygon([(83.5, y0), (92.0, y1), (92.0, y0)], style=Icon.fill_style(Gcp.TECH_MED_LIGHT))

    # White horizontal slot & right circular indicator
    rectangle((36.5, ym), width=24.0, height=4.6, style=Icon.fill_style(Icon.WHITE))
    circle((70.0, ym), radius=6.6, style=Icon.fill_style(Icon.WHITE))


_draw_legacy_storage_tier(55.0, 84.0)
_draw_legacy_storage_tier(16.0, 45.0)

save()
