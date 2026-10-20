# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Social Media, Messaging, Streaming, Tech Community & AdTech icon provider."""

from __future__ import annotations

from drawlib._icons.png_icons._base import PngIconProvider

ORIGINAL_SOCIAL_PROVIDER = PngIconProvider(
    name="original_social",
    package_name="icon_original_social",
    asset_subdir="icons/original_social",
)

_write = ORIGINAL_SOCIAL_PROVIDER.write
