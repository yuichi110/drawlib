# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Client (browsers, OS, app stores, PC/mobile OEMs, smart devices, cars, peripherals) icon provider."""

from __future__ import annotations

from drawlib._icons.png_icons._base import PngIconProvider

CLIENT_PROVIDER = PngIconProvider(
    name="client",
    package_name="icon_client",
    asset_subdir="icons/client",
)

_write = CLIENT_PROVIDER.write
