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

from drawlib.v0_2 import ASSET_VERSION
from drawlib.v0_2.private.l1_core import FONT_DIR_PATH
from drawlib.v0_2.private.l2_models import FontBase, FontMetadata
from drawlib.v0_2.private.l3_fonts._resources import FONT_RESOURCES


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
    abs_path = os.path.join(FONT_DIR_PATH, *paths)

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
