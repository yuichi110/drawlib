# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original IT Service (GSI, Consulting, SIer, BPO, IT Staffing & Governance) icon provider."""

from __future__ import annotations

from drawlib._icons.png_icons._base import PngIconProvider

ORIGINAL_ITSERVICE_PROVIDER = PngIconProvider(
    name="original_itservice",
    package_name="icon_original_itservice",
    asset_subdir="icons/original_itservice",
)

_write = ORIGINAL_ITSERVICE_PROVIDER.write
