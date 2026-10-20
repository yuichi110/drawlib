# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Code (languages, frameworks, APIs, IDEs) icon provider configuration and writer."""

from __future__ import annotations

from drawlib._icons.png_icons._base import PngIconProvider

CODE_PROVIDER = PngIconProvider(
    name="code",
    package_name="icon_code",
    asset_subdir="icons/code",
)

_write = CODE_PROVIDER.write
