# Copyright (c) 2024 Yuichi Ito (yuichi@yuichi.com)
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


def cd_to_project_root() -> None:
    """Change directory to project root."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    os.chdir("../")


#
# Phosphor
#

PHOSPHOR_URL_BASE = "https://raw.githubusercontent.com/yuichi110/drawlib_assets/main/assets/v0_2/fonticons/phosphor/"

PHOSPHOR_HEAD = '''
# Copyright (c) 2024 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Phosphor icon functions."""

import os
import typing
import urllib.parse

import drawlib.assets.v0_2.fonticons
import drawlib.v0_2.private.core.model
import drawlib.v0_2.private.core.theme
import drawlib.v0_2.private.download
import drawlib.v0_2.private.icons.util
import drawlib.v0_2.private.util


def _get_fontfile_tuple(path: str, md5_hash: str) -> typing.Tuple[str, str, str]:
    """Retrieve font file information including local path, download URL, and MD5 hash.

    Args:
        path: Relative path of the font file within the package.
        md5_hash: MD5 hash of the font file for integrity verification.

    Returns:
        Tuple[str, str, str]: Tuple containing:
            - Local file path of the font.
            - Download URL of the font.
            - MD5 hash of the font.

    """
    paths = [p for p in path.split("/") if p]

    # font path
    dir_path = os.path.dirname(drawlib.assets.v0_2.fonticons.__file__)
    font_path = os.path.join(dir_path, *paths)

    # url
    url = urllib.parse.urljoin(
        "https://raw.githubusercontent.com/yuichi110/drawlib_assets/main/assets/v0_2/fonticons/",
        "/".join(paths),
    )

    return (font_path, url, md5_hash)


def _get_font_path(style: str) -> str:
    """Retrieve the local path of the specified font style.

    Args:
        style: Style of the font ('thin', 'light', 'regular', 'bold', 'fill').

    Returns:
        str: Local file path of the font.

    """
    file_path, download_url, md5_hash = {
        "thin": _get_fontfile_tuple("phosphor/thin.ttf", "9ca0acf8bc84ec2421f96f835017f321"),
        "light": _get_fontfile_tuple("phosphor/light.ttf", "6c53da4ecc310dd5dbcfafe3d916a346"),
        "regular": _get_fontfile_tuple("phosphor/regular.ttf", "c2ecd49d10b76c3f9b9c072966cc0c3c"),
        "bold": _get_fontfile_tuple("phosphor/bold.ttf", "4f59e81563e413635c57d78338d33b92"),
        "fill": _get_fontfile_tuple("phosphor/fill.ttf", "612af00267f5e8a429531399700db66e"),
    }[style]

    # download if local cache doesn't exist
    drawlib.v0_2.private.download.download_if_not_exist(
        file_path=file_path,
        download_url=download_url,
        md5_hash=md5_hash,
    )

    return file_path


def _write(
    xy: typing.Tuple[float, float],
    width: float,
    code: str,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_2.private.core.model.IconStyle, str, None] = None,
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
    default_style = "thin"

    # None, str -> IconStyle
    if style is None:
        style = drawlib.v0_2.private.core.theme.dtheme.iconstyles.get()
    elif isinstance(style, str):
        style = drawlib.v0_2.private.core.theme.dtheme.iconstyles.get(style)
    elif isinstance(style, drawlib.v0_2.private.core.model.IconStyle):
        ...
    else:
        raise ValueError(
            f'Unsupported type "{type(style)}" is passed to arg style. '
            'Supports only IconStyle, str, None.'
        )

    # set IconStyle.Style if it is None
    if style.style is None:
        style.style = default_style

    # validate IconStyle.Style
    if style.style not in {"thin", "light", "regular", "bold", "fill"}:
        raise ValueError(f'icon_phosphor does not support style "{style.style}".')

    # set icon file path
    file = _get_font_path(style.style)

    # draw phosphor icon with generic function
    drawlib.v0_2.private.icons.util.icon(
        xy=xy,
        width=width,
        code=code,
        file=file,
        angle=angle,
        style=style,
    )


#
# Auto generated code from here ###
#
'''

PHOSPHOR_TEMPLATE = '''
@drawlib.v0_2.private.util.error_handler
def {function_name}(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_2.private.core.model.IconStyle, str, None] = None,
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
        assert self._regular_dict == self._thin_dict
        assert self._regular_dict == self._light_dict
        assert self._regular_dict == self._bold_dict
        assert self._regular_dict == self._fill_dict

        self._write()

    @staticmethod
    def _load(font_dict: Dict, font_css_url: str) -> None:
        with urllib.request.urlopen(font_css_url) as response:
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
        os.makedirs("output_codes", exist_ok=True)
        with open("output_codes/phosphor.py", mode="w", encoding="utf8") as fout:
            fout.write(code_text)
            fout.write("\n")  # last new line


if __name__ == "__main__":
    cd_to_project_root()
    IconCodeGeneratorPhosphor().run()
