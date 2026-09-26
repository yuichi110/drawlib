# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Phosphor icon provider base configuration and writer."""

from __future__ import annotations

from enum import Enum

from drawlib._core.fonts import FontResource
from drawlib._icons.font_icons._base import FontIconProvider


class _Fonts(str, Enum):
    THIN = "thin"
    LIGHT = "light"
    REGULAR = "regular"
    BOLD = "bold"
    FILL = "fill"


_DEFAULT_STYLE = _Fonts.THIN.value

_FONT_RESOURCE: dict[str, FontResource] = {
    _Fonts.THIN: FontResource(
        path="phosphor/thin.ttf",
        md5="9ca0acf8bc84ec2421f96f835017f321",
    ),
    _Fonts.LIGHT: FontResource(
        path="phosphor/light.ttf",
        md5="6c53da4ecc310dd5dbcfafe3d916a346",
    ),
    _Fonts.REGULAR: FontResource(
        path="phosphor/regular.ttf",
        md5="c2ecd49d10b76c3f9b9c072966cc0c3c",
    ),
    _Fonts.BOLD: FontResource(
        path="phosphor/bold.ttf",
        md5="4f59e81563e413635c57d78338d33b92",
    ),
    _Fonts.FILL: FontResource(
        path="phosphor/fill.ttf",
        md5="612af00267f5e8a429531399700db66e",
    ),
}

PHOSPHOR_PROVIDER = FontIconProvider(
    name="phosphor",
    font_resources=_FONT_RESOURCE,
    default_style=_DEFAULT_STYLE,
    asset_subdir="fonticons",
)

_write = PHOSPHOR_PROVIDER.write
