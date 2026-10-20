# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Cloud (hyperscalers, cloud companies, global hosting/VPS/edge, modern PaaS/BaaS, Japan cloud) icon provider."""

from __future__ import annotations

from drawlib._icons.png_icons._base import PngIconProvider

CLOUD_PROVIDER = PngIconProvider(
    name="cloud",
    package_name="icon_cloud",
    asset_subdir="icons/cloud",
)

_write = CLOUD_PROVIDER.write
