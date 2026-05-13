# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Helper script for generating icon phosphor codes.

This code generate codes for writing fonticon functions.
They are created at "output_codes" directory.
Please move them to appropriate code location of drawlib package.
"""

import os
import urllib.request
from typing import Dict

from utils import cd_to_project_root

#
# Phosphor
#

PHOSPHOR_URL_BASE = "https://raw.githubusercontent.com/yuichi110/drawlib_assets/main/assets/v0_2/fonticons/phosphor/"
ASSETS_URL_BASE = "https://raw.githubusercontent.com/yuichi110/drawlib_assets/main/assets/v0_2/fonticons/"
OUTPUT_DIR = "output_codes"
OUTPUT_FILE = "phosphor.py"

PHOSPHOR_HEAD = '''
# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Phosphor icon functions."""

from __future__ import annotations

import os
from enum import Enum
from typing import Optional, Tuple, Union
from urllib.parse import urljoin

import drawlib.assets.v0_2.fonticons
from drawlib.v0_2 import ASSET_VERSION
from drawlib.v0_2.private.core.fonts import FontMetadata
from drawlib.v0_2.private.core.fonts_resource import FontResource
from drawlib.v0_2.private.core.model import IconStyle
from drawlib.v0_2.private.core.theme import dtheme
from drawlib.v0_2.private.download import download_if_not_exist
from drawlib.v0_2.private.icons.util import icon
from drawlib.v0_2.private.types import TypeAngle, TypeCoordinate, TypePosFloat, TypeStr
from drawlib.v0_2.private.util import guarded


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


def _get_font_metadata(font: _Fonts | str) -> FontMetadata:
    """Resolve full metadata for a given Phosphor font style.

    Args:
        font (_Fonts | str): The font style (e.g., 'thin', 'light', 'regular', 'bold', 'fill').

    Returns:
        FontMetadata: Resolved metadata including absolute path and URL.

    Raises:
        ValueError: If the font style is not found in _FONT_RESOURCE.

    """
    resource = _FONT_RESOURCE.get(font)
    if not resource:
        raise ValueError(f"Font {font} not found in _FONT_RESOURCE.")

    paths = [p for p in resource.path.split("/") if p]

    # Construct the local font path
    dir_path = os.path.dirname(drawlib.assets.v0_2.fonticons.__file__)
    abs_path = os.path.join(dir_path, *paths)

    # Construct the URL
    url = urljoin(
        f"https://raw.githubusercontent.com/yuichi110/drawlib_assets/main/assets/{ASSET_VERSION}/fonticons/",
        "/".join(paths),
    )

    return FontMetadata(
        path=resource.path,
        abs_path=abs_path,
        url=url,
        md5=resource.md5,
    )


def _write(
    xy: TypeCoordinate,
    width: TypePosFloat,
    code: str,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draw a Phosphor icon at the specified position with given parameters.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon center.
        width: Width of the icon.
        code: Identifier or code of the icon.
        angle: Angle of rotation (default is 0.0).
        style: Style of the icon as an IconStyle object, string, or None.
            Defaults to None, which uses the default style.

    Raises:
        ValueError: If an unsupported style type is passed to 'style'.

    """
    # None -> IconStyle
    if style is None:
        style_obj = dtheme.iconstyles.get().copy()
    # str -> IconStyle
    elif isinstance(style, str):
        style_obj = dtheme.iconstyles.get(style).copy()
    # IconStyle
    else:
        style_obj = style.copy()

    # set IconStyle.style if it is None
    if style_obj.style is None:
        style_obj.style = _DEFAULT_STYLE

    # validate IconStyle.style
    if style_obj.style not in _Fonts:
        raise ValueError(f'icon_phosphor does not support style "{style_obj.style}".')

    # set icon file path
    font_metadata = _get_font_metadata(style_obj.style)

    # download if not exist
    download_if_not_exist(
        file_path=font_metadata.abs_path,
        download_url=font_metadata.url,
        md5_hash=font_metadata.md5,
    )

    # draw phosphor icon with generic function
    icon(
        xy=xy,
        width=width,
        code=code,
        file=font_metadata.abs_path,
        angle=angle,
        style=style_obj,
    )


#
# Auto generated code from here ###
#
'''

PHOSPHOR_TEMPLATE = '''
@guarded
def {function_name}(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an {icon_name}.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\\u{icon_code}", angle=angle, style=style)
'''


class IconCodeGeneratorPhosphor:
    """Code generator."""

    def __init__(self) -> None:
        """Init."""
        self._bold_dict: Dict[str, str] = {}
        self._duotone_dict: Dict[str, str] = {}
        self._fill_dict: Dict[str, str] = {}
        self._light_dict: Dict[str, str] = {}
        self._regular_dict: Dict[str, str] = {}
        self._thin_dict: Dict[str, str] = {}

    def run(self) -> None:
        """Generate code."""
        self._load(self._thin_dict, PHOSPHOR_URL_BASE + "thin.css")
        self._load(self._light_dict, PHOSPHOR_URL_BASE + "light.css")
        self._load(self._regular_dict, PHOSPHOR_URL_BASE + "regular.css")
        self._load(self._bold_dict, PHOSPHOR_URL_BASE + "bold.css")
        self._load(self._fill_dict, PHOSPHOR_URL_BASE + "fill.css")

        # check whether code points are exactly same
        # at version 2.1, all code points are same.
        if self._regular_dict != self._thin_dict:
            raise ValueError("regular and thin dicts are not same.")
        if self._regular_dict != self._light_dict:
            raise ValueError("regular and light dicts are not same.")
        if self._regular_dict != self._bold_dict:
            raise ValueError("regular and bold dicts are not same.")
        if self._regular_dict != self._fill_dict:
            raise ValueError("regular and fill dicts are not same.")

        self._write()

    @staticmethod
    def _load(font_dict: Dict, font_css_url: str) -> None:
        with urllib.request.urlopen(font_css_url) as response:  # noqa: S310
            text = response.read().decode("utf-8")
        lines = text.splitlines()

        key = ""
        for line in lines:
            line = line.strip()

            if line.startswith(".ph") and line.endswith(":before {"):
                # key line
                words = line.split(".")
                key = words[2][3:-9]

            elif key:
                words = line.split(":")
                value = words[1].strip()[2:-2]
                font_dict[key] = value
                key = ""

    def _write(self) -> None:
        # add head
        code_chunks = [PHOSPHOR_HEAD.strip()]

        # add functions
        for icon_name, icon_code in self._regular_dict.items():
            function_name = icon_name.replace("-", "_")
            function_text = PHOSPHOR_TEMPLATE.format(
                function_name=function_name,
                icon_name=icon_name,
                icon_code=icon_code,
            )
            code_chunks.append(function_text.strip())

        # combine them with 2 new lines
        code_text = "\n\n\n".join(code_chunks)

        # write to file
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        with open(os.path.join(OUTPUT_DIR, OUTPUT_FILE), mode="w", encoding="utf8") as fout:
            fout.write(code_text)
            fout.write("\n")  # last new line


if __name__ == "__main__":
    cd_to_project_root()
    IconCodeGeneratorPhosphor().run()
