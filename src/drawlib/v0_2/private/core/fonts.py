# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Font metadata resolution module."""

import os
from urllib.parse import urljoin

from pydantic import BaseModel

import drawlib.assets.v0_2.fonts
from drawlib.v0_2 import ASSET_VERSION
from drawlib.v0_2.private.core.fonts_resource import FONT_RESOURCES
from drawlib.v0_2.private.types import FontBase


class FontMetadata(BaseModel):
    """Resolved font metadata with absolute path and URL."""

    path: str
    abs_path: str
    url: str
    md5: str


def get_font_metadata(font: FontBase) -> FontMetadata:
    """Resolve full metadata for a given font enum member.

    Args:
        font (FontBase): The font enum member.

    Returns:
        FontMetadata: Resolved metadata including absolute path and URL.

    Raises:
        ValueError: If the font is not found in FONT_RESOURCES.
    """
    resource = FONT_RESOURCES.get(font)
    if not resource:
        raise ValueError(f"Font {font} not found in FONT_RESOURCES.")

    paths = [p for p in resource.path.split("/") if p]

    # Construct the local font path
    dir_path = os.path.dirname(drawlib.assets.v0_2.fonts.__file__)
    abs_path = os.path.join(dir_path, *paths)

    # Construct the URL
    url = urljoin(
        f"https://raw.githubusercontent.com/yuichi110/drawlib_assets/main/assets/{ASSET_VERSION}/fonts/",
        "/".join(paths),
    )

    return FontMetadata(
        path=resource.path,
        abs_path=abs_path,
        url=url,
        md5=resource.md5,
    )
