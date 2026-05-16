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
from drawlib.v0_2.private.l1_core import guarded
from drawlib.v0_2.private.l2_types import (
    TypeAngle,
    TypeCoordinate,
    TypePosFloat,
    TypeStr,
)
from drawlib.v0_2.private.l3_external import download_if_not_exist
from drawlib.v0_2.private.l3_fonts import FontMetadata, FontResource
from drawlib.v0_2.private.l3_styles import IconStyle
from drawlib.v0_2.private.l4_theme import dtheme
from drawlib.v0_2.private.l6_icons._icon import icon


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


@guarded
def acorn(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an acorn.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ueb9a", angle=angle, style=style)


@guarded
def address_book(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an address-book.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue6f8", angle=angle, style=style)


@guarded
def address_book_tabs(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an address-book-tabs.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uee4e", angle=angle, style=style)


@guarded
def air_traffic_control(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an air-traffic-control.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uecd8", angle=angle, style=style)


@guarded
def airplane(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an airplane.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue002", angle=angle, style=style)


@guarded
def airplane_in_flight(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an airplane-in-flight.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue4fe", angle=angle, style=style)


@guarded
def airplane_landing(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an airplane-landing.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue502", angle=angle, style=style)


@guarded
def airplane_takeoff(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an airplane-takeoff.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue504", angle=angle, style=style)


@guarded
def airplane_taxiing(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an airplane-taxiing.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue500", angle=angle, style=style)


@guarded
def airplane_tilt(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an airplane-tilt.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue5d6", angle=angle, style=style)


@guarded
def airplay(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an airplay.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue004", angle=angle, style=style)


@guarded
def alarm(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an alarm.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue006", angle=angle, style=style)


@guarded
def alien(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an alien.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue8a6", angle=angle, style=style)


@guarded
def align_bottom(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an align-bottom.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue506", angle=angle, style=style)


@guarded
def align_bottom_simple(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an align-bottom-simple.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ueb0c", angle=angle, style=style)


@guarded
def align_center_horizontal(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an align-center-horizontal.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue50a", angle=angle, style=style)


@guarded
def align_center_horizontal_simple(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an align-center-horizontal-simple.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ueb0e", angle=angle, style=style)


@guarded
def align_center_vertical(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an align-center-vertical.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue50c", angle=angle, style=style)


@guarded
def align_center_vertical_simple(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an align-center-vertical-simple.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ueb10", angle=angle, style=style)


@guarded
def align_left(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an align-left.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue50e", angle=angle, style=style)


@guarded
def align_left_simple(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an align-left-simple.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ueaee", angle=angle, style=style)


@guarded
def align_right(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an align-right.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue510", angle=angle, style=style)


@guarded
def align_right_simple(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an align-right-simple.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ueb12", angle=angle, style=style)


@guarded
def align_top(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an align-top.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue512", angle=angle, style=style)


@guarded
def align_top_simple(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an align-top-simple.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ueb14", angle=angle, style=style)


@guarded
def amazon_logo(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an amazon-logo.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue96c", angle=angle, style=style)


@guarded
def ambulance(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an ambulance.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue572", angle=angle, style=style)


@guarded
def anchor(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an anchor.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue514", angle=angle, style=style)


@guarded
def anchor_simple(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an anchor-simple.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue5d8", angle=angle, style=style)


@guarded
def android_logo(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an android-logo.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue008", angle=angle, style=style)


@guarded
def angle(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an angle.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue7bc", angle=angle, style=style)


@guarded
def angular_logo(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an angular-logo.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ueb80", angle=angle, style=style)


@guarded
def aperture(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an aperture.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue00a", angle=angle, style=style)


@guarded
def app_store_logo(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an app-store-logo.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue974", angle=angle, style=style)


@guarded
def app_window(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an app-window.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue5da", angle=angle, style=style)


@guarded
def apple_logo(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an apple-logo.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue516", angle=angle, style=style)


@guarded
def apple_podcasts_logo(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an apple-podcasts-logo.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ueb96", angle=angle, style=style)


@guarded
def approximate_equals(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an approximate-equals.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uedaa", angle=angle, style=style)


@guarded
def archive(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an archive.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue00c", angle=angle, style=style)


@guarded
def armchair(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an armchair.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue012", angle=angle, style=style)


@guarded
def arrow_arc_left(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an arrow-arc-left.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue014", angle=angle, style=style)


@guarded
def arrow_arc_right(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an arrow-arc-right.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue016", angle=angle, style=style)


@guarded
def arrow_bend_double_up_left(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an arrow-bend-double-up-left.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue03a", angle=angle, style=style)


@guarded
def arrow_bend_double_up_right(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an arrow-bend-double-up-right.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue03c", angle=angle, style=style)


@guarded
def arrow_bend_down_left(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an arrow-bend-down-left.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue018", angle=angle, style=style)


@guarded
def arrow_bend_down_right(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an arrow-bend-down-right.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue01a", angle=angle, style=style)


@guarded
def arrow_bend_left_down(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an arrow-bend-left-down.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue01c", angle=angle, style=style)


@guarded
def arrow_bend_left_up(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an arrow-bend-left-up.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue01e", angle=angle, style=style)


@guarded
def arrow_bend_right_down(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an arrow-bend-right-down.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue020", angle=angle, style=style)


@guarded
def arrow_bend_right_up(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an arrow-bend-right-up.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue022", angle=angle, style=style)


@guarded
def arrow_bend_up_left(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an arrow-bend-up-left.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue024", angle=angle, style=style)


@guarded
def arrow_bend_up_right(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an arrow-bend-up-right.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue026", angle=angle, style=style)


@guarded
def arrow_circle_down(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an arrow-circle-down.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue028", angle=angle, style=style)


@guarded
def arrow_circle_down_left(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an arrow-circle-down-left.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue02a", angle=angle, style=style)


@guarded
def arrow_circle_down_right(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an arrow-circle-down-right.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue02c", angle=angle, style=style)


@guarded
def arrow_circle_left(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an arrow-circle-left.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue05a", angle=angle, style=style)


@guarded
def arrow_circle_right(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an arrow-circle-right.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue02e", angle=angle, style=style)


@guarded
def arrow_circle_up(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an arrow-circle-up.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue030", angle=angle, style=style)


@guarded
def arrow_circle_up_left(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an arrow-circle-up-left.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue032", angle=angle, style=style)


@guarded
def arrow_circle_up_right(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an arrow-circle-up-right.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue034", angle=angle, style=style)


@guarded
def arrow_clockwise(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an arrow-clockwise.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue036", angle=angle, style=style)


@guarded
def arrow_counter_clockwise(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an arrow-counter-clockwise.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue038", angle=angle, style=style)


@guarded
def arrow_down(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an arrow-down.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue03e", angle=angle, style=style)


@guarded
def arrow_down_left(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an arrow-down-left.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue040", angle=angle, style=style)


@guarded
def arrow_down_right(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an arrow-down-right.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue042", angle=angle, style=style)


@guarded
def arrow_elbow_down_left(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an arrow-elbow-down-left.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue044", angle=angle, style=style)


@guarded
def arrow_elbow_down_right(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an arrow-elbow-down-right.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue046", angle=angle, style=style)


@guarded
def arrow_elbow_left(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an arrow-elbow-left.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue048", angle=angle, style=style)


@guarded
def arrow_elbow_left_down(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an arrow-elbow-left-down.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue04a", angle=angle, style=style)


@guarded
def arrow_elbow_left_up(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an arrow-elbow-left-up.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue04c", angle=angle, style=style)


@guarded
def arrow_elbow_right(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an arrow-elbow-right.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue04e", angle=angle, style=style)


@guarded
def arrow_elbow_right_down(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an arrow-elbow-right-down.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue050", angle=angle, style=style)


@guarded
def arrow_elbow_right_up(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an arrow-elbow-right-up.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue052", angle=angle, style=style)


@guarded
def arrow_elbow_up_left(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an arrow-elbow-up-left.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue054", angle=angle, style=style)


@guarded
def arrow_elbow_up_right(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an arrow-elbow-up-right.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue056", angle=angle, style=style)


@guarded
def arrow_fat_down(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an arrow-fat-down.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue518", angle=angle, style=style)


@guarded
def arrow_fat_left(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an arrow-fat-left.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue51a", angle=angle, style=style)


@guarded
def arrow_fat_line_down(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an arrow-fat-line-down.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue51c", angle=angle, style=style)


@guarded
def arrow_fat_line_left(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an arrow-fat-line-left.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue51e", angle=angle, style=style)


@guarded
def arrow_fat_line_right(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an arrow-fat-line-right.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue520", angle=angle, style=style)


@guarded
def arrow_fat_line_up(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an arrow-fat-line-up.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue522", angle=angle, style=style)


@guarded
def arrow_fat_lines_down(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an arrow-fat-lines-down.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue524", angle=angle, style=style)


@guarded
def arrow_fat_lines_left(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an arrow-fat-lines-left.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue526", angle=angle, style=style)


@guarded
def arrow_fat_lines_right(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an arrow-fat-lines-right.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue528", angle=angle, style=style)


@guarded
def arrow_fat_lines_up(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an arrow-fat-lines-up.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue52a", angle=angle, style=style)


@guarded
def arrow_fat_right(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an arrow-fat-right.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue52c", angle=angle, style=style)


@guarded
def arrow_fat_up(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an arrow-fat-up.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue52e", angle=angle, style=style)


@guarded
def arrow_left(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an arrow-left.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue058", angle=angle, style=style)


@guarded
def arrow_line_down(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an arrow-line-down.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue05c", angle=angle, style=style)


@guarded
def arrow_line_down_left(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an arrow-line-down-left.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue05e", angle=angle, style=style)


@guarded
def arrow_line_down_right(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an arrow-line-down-right.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue060", angle=angle, style=style)


@guarded
def arrow_line_left(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an arrow-line-left.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue062", angle=angle, style=style)


@guarded
def arrow_line_right(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an arrow-line-right.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue064", angle=angle, style=style)


@guarded
def arrow_line_up(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an arrow-line-up.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue066", angle=angle, style=style)


@guarded
def arrow_line_up_left(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an arrow-line-up-left.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue068", angle=angle, style=style)


@guarded
def arrow_line_up_right(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an arrow-line-up-right.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue06a", angle=angle, style=style)


@guarded
def arrow_right(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an arrow-right.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue06c", angle=angle, style=style)


@guarded
def arrow_square_down(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an arrow-square-down.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue06e", angle=angle, style=style)


@guarded
def arrow_square_down_left(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an arrow-square-down-left.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue070", angle=angle, style=style)


@guarded
def arrow_square_down_right(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an arrow-square-down-right.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue072", angle=angle, style=style)


@guarded
def arrow_square_in(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an arrow-square-in.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue5dc", angle=angle, style=style)


@guarded
def arrow_square_left(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an arrow-square-left.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue074", angle=angle, style=style)


@guarded
def arrow_square_out(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an arrow-square-out.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue5de", angle=angle, style=style)


@guarded
def arrow_square_right(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an arrow-square-right.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue076", angle=angle, style=style)


@guarded
def arrow_square_up(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an arrow-square-up.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue078", angle=angle, style=style)


@guarded
def arrow_square_up_left(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an arrow-square-up-left.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue07a", angle=angle, style=style)


@guarded
def arrow_square_up_right(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an arrow-square-up-right.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue07c", angle=angle, style=style)


@guarded
def arrow_u_down_left(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an arrow-u-down-left.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue07e", angle=angle, style=style)


@guarded
def arrow_u_down_right(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an arrow-u-down-right.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue080", angle=angle, style=style)


@guarded
def arrow_u_left_down(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an arrow-u-left-down.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue082", angle=angle, style=style)


@guarded
def arrow_u_left_up(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an arrow-u-left-up.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue084", angle=angle, style=style)


@guarded
def arrow_u_right_down(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an arrow-u-right-down.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue086", angle=angle, style=style)


@guarded
def arrow_u_right_up(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an arrow-u-right-up.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue088", angle=angle, style=style)


@guarded
def arrow_u_up_left(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an arrow-u-up-left.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue08a", angle=angle, style=style)


@guarded
def arrow_u_up_right(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an arrow-u-up-right.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue08c", angle=angle, style=style)


@guarded
def arrow_up(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an arrow-up.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue08e", angle=angle, style=style)


@guarded
def arrow_up_left(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an arrow-up-left.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue090", angle=angle, style=style)


@guarded
def arrow_up_right(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an arrow-up-right.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue092", angle=angle, style=style)


@guarded
def arrows_clockwise(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an arrows-clockwise.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue094", angle=angle, style=style)


@guarded
def arrows_counter_clockwise(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an arrows-counter-clockwise.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue096", angle=angle, style=style)


@guarded
def arrows_down_up(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an arrows-down-up.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue098", angle=angle, style=style)


@guarded
def arrows_horizontal(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an arrows-horizontal.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ueb06", angle=angle, style=style)


@guarded
def arrows_in(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an arrows-in.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue09a", angle=angle, style=style)


@guarded
def arrows_in_cardinal(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an arrows-in-cardinal.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue09c", angle=angle, style=style)


@guarded
def arrows_in_line_horizontal(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an arrows-in-line-horizontal.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue530", angle=angle, style=style)


@guarded
def arrows_in_line_vertical(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an arrows-in-line-vertical.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue532", angle=angle, style=style)


@guarded
def arrows_in_simple(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an arrows-in-simple.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue09e", angle=angle, style=style)


@guarded
def arrows_left_right(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an arrows-left-right.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue0a0", angle=angle, style=style)


@guarded
def arrows_merge(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an arrows-merge.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ued3e", angle=angle, style=style)


@guarded
def arrows_out(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an arrows-out.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue0a2", angle=angle, style=style)


@guarded
def arrows_out_cardinal(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an arrows-out-cardinal.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue0a4", angle=angle, style=style)


@guarded
def arrows_out_line_horizontal(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an arrows-out-line-horizontal.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue534", angle=angle, style=style)


@guarded
def arrows_out_line_vertical(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an arrows-out-line-vertical.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue536", angle=angle, style=style)


@guarded
def arrows_out_simple(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an arrows-out-simple.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue0a6", angle=angle, style=style)


@guarded
def arrows_split(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an arrows-split.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ued3c", angle=angle, style=style)


@guarded
def arrows_vertical(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an arrows-vertical.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ueb04", angle=angle, style=style)


@guarded
def article(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an article.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue0a8", angle=angle, style=style)


@guarded
def article_medium(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an article-medium.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue5e0", angle=angle, style=style)


@guarded
def article_ny_times(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an article-ny-times.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue5e2", angle=angle, style=style)


@guarded
def asclepius(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an asclepius.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uee34", angle=angle, style=style)


@guarded
def caduceus(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an caduceus.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uee34", angle=angle, style=style)


@guarded
def asterisk(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an asterisk.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue0aa", angle=angle, style=style)


@guarded
def asterisk_simple(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an asterisk-simple.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue832", angle=angle, style=style)


@guarded
def at(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an at.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue0ac", angle=angle, style=style)


@guarded
def atom(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an atom.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue5e4", angle=angle, style=style)


@guarded
def avocado(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an avocado.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uee04", angle=angle, style=style)


@guarded
def axe(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an axe.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue9fc", angle=angle, style=style)


@guarded
def baby(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an baby.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue774", angle=angle, style=style)


@guarded
def baby_carriage(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an baby-carriage.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue818", angle=angle, style=style)


@guarded
def backpack(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an backpack.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue922", angle=angle, style=style)


@guarded
def backspace(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an backspace.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue0ae", angle=angle, style=style)


@guarded
def bag(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an bag.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue0b0", angle=angle, style=style)


@guarded
def bag_simple(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an bag-simple.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue5e6", angle=angle, style=style)


@guarded
def balloon(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an balloon.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue76c", angle=angle, style=style)


@guarded
def bandaids(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an bandaids.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue0b2", angle=angle, style=style)


@guarded
def bank(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an bank.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue0b4", angle=angle, style=style)


@guarded
def barbell(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an barbell.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue0b6", angle=angle, style=style)


@guarded
def barcode(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an barcode.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue0b8", angle=angle, style=style)


@guarded
def barn(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an barn.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uec72", angle=angle, style=style)


@guarded
def barricade(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an barricade.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue948", angle=angle, style=style)


@guarded
def baseball(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an baseball.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue71a", angle=angle, style=style)


@guarded
def baseball_cap(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an baseball-cap.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uea28", angle=angle, style=style)


@guarded
def baseball_helmet(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an baseball-helmet.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uee4a", angle=angle, style=style)


@guarded
def basket(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an basket.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue964", angle=angle, style=style)


@guarded
def basketball(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an basketball.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue724", angle=angle, style=style)


@guarded
def bathtub(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an bathtub.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue81e", angle=angle, style=style)


@guarded
def battery_charging(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an battery-charging.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue0ba", angle=angle, style=style)


@guarded
def battery_charging_vertical(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an battery-charging-vertical.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue0bc", angle=angle, style=style)


@guarded
def battery_empty(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an battery-empty.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue0be", angle=angle, style=style)


@guarded
def battery_full(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an battery-full.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue0c0", angle=angle, style=style)


@guarded
def battery_high(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an battery-high.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue0c2", angle=angle, style=style)


@guarded
def battery_low(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an battery-low.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue0c4", angle=angle, style=style)


@guarded
def battery_medium(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an battery-medium.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue0c6", angle=angle, style=style)


@guarded
def battery_plus(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an battery-plus.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue808", angle=angle, style=style)


@guarded
def battery_plus_vertical(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an battery-plus-vertical.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uec50", angle=angle, style=style)


@guarded
def battery_vertical_empty(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an battery-vertical-empty.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue7c6", angle=angle, style=style)


@guarded
def battery_vertical_full(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an battery-vertical-full.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue7c4", angle=angle, style=style)


@guarded
def battery_vertical_high(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an battery-vertical-high.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue7c2", angle=angle, style=style)


@guarded
def battery_vertical_low(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an battery-vertical-low.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue7be", angle=angle, style=style)


@guarded
def battery_vertical_medium(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an battery-vertical-medium.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue7c0", angle=angle, style=style)


@guarded
def battery_warning(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an battery-warning.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue0c8", angle=angle, style=style)


@guarded
def battery_warning_vertical(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an battery-warning-vertical.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue0ca", angle=angle, style=style)


@guarded
def beach_ball(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an beach-ball.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ued24", angle=angle, style=style)


@guarded
def beanie(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an beanie.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uea2a", angle=angle, style=style)


@guarded
def bed(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an bed.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue0cc", angle=angle, style=style)


@guarded
def beer_bottle(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an beer-bottle.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue7b0", angle=angle, style=style)


@guarded
def beer_stein(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an beer-stein.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ueb62", angle=angle, style=style)


@guarded
def behance_logo(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an behance-logo.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue7f4", angle=angle, style=style)


@guarded
def bell(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an bell.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue0ce", angle=angle, style=style)


@guarded
def bell_ringing(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an bell-ringing.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue5e8", angle=angle, style=style)


@guarded
def bell_simple(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an bell-simple.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue0d0", angle=angle, style=style)


@guarded
def bell_simple_ringing(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an bell-simple-ringing.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue5ea", angle=angle, style=style)


@guarded
def bell_simple_slash(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an bell-simple-slash.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue0d2", angle=angle, style=style)


@guarded
def bell_simple_z(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an bell-simple-z.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue5ec", angle=angle, style=style)


@guarded
def bell_slash(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an bell-slash.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue0d4", angle=angle, style=style)


@guarded
def bell_z(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an bell-z.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue5ee", angle=angle, style=style)


@guarded
def belt(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an belt.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uea2c", angle=angle, style=style)


@guarded
def bezier_curve(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an bezier-curve.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ueb00", angle=angle, style=style)


@guarded
def bicycle(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an bicycle.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue0d6", angle=angle, style=style)


@guarded
def binary(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an binary.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uee60", angle=angle, style=style)


@guarded
def binoculars(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an binoculars.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uea64", angle=angle, style=style)


@guarded
def biohazard(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an biohazard.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue9e0", angle=angle, style=style)


@guarded
def bird(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an bird.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue72c", angle=angle, style=style)


@guarded
def blueprint(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an blueprint.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ueda0", angle=angle, style=style)


@guarded
def bluetooth(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an bluetooth.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue0da", angle=angle, style=style)


@guarded
def bluetooth_connected(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an bluetooth-connected.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue0dc", angle=angle, style=style)


@guarded
def bluetooth_slash(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an bluetooth-slash.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue0de", angle=angle, style=style)


@guarded
def bluetooth_x(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an bluetooth-x.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue0e0", angle=angle, style=style)


@guarded
def boat(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an boat.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue786", angle=angle, style=style)


@guarded
def bomb(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an bomb.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uee0a", angle=angle, style=style)


@guarded
def bone(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an bone.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue7f2", angle=angle, style=style)


@guarded
def book(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an book.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue0e2", angle=angle, style=style)


@guarded
def book_bookmark(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an book-bookmark.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue0e4", angle=angle, style=style)


@guarded
def book_open(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an book-open.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue0e6", angle=angle, style=style)


@guarded
def book_open_text(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an book-open-text.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue8f2", angle=angle, style=style)


@guarded
def book_open_user(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an book-open-user.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uede0", angle=angle, style=style)


@guarded
def bookmark(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an bookmark.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue0e8", angle=angle, style=style)


@guarded
def bookmark_simple(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an bookmark-simple.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue0ea", angle=angle, style=style)


@guarded
def bookmarks(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an bookmarks.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue0ec", angle=angle, style=style)


@guarded
def bookmarks_simple(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an bookmarks-simple.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue5f0", angle=angle, style=style)


@guarded
def books(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an books.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue758", angle=angle, style=style)


@guarded
def boot(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an boot.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uecca", angle=angle, style=style)


@guarded
def boules(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an boules.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue722", angle=angle, style=style)


@guarded
def bounding_box(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an bounding-box.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue6ce", angle=angle, style=style)


@guarded
def bowl_food(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an bowl-food.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ueaa4", angle=angle, style=style)


@guarded
def bowl_steam(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an bowl-steam.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue8e4", angle=angle, style=style)


@guarded
def bowling_ball(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an bowling-ball.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uea34", angle=angle, style=style)


@guarded
def box_arrow_down(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an box-arrow-down.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue00e", angle=angle, style=style)


@guarded
def archive_box(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an archive-box.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue00e", angle=angle, style=style)


@guarded
def box_arrow_up(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an box-arrow-up.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uee54", angle=angle, style=style)


@guarded
def boxing_glove(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an boxing-glove.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uea36", angle=angle, style=style)


@guarded
def brackets_angle(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an brackets-angle.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue862", angle=angle, style=style)


@guarded
def brackets_curly(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an brackets-curly.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue860", angle=angle, style=style)


@guarded
def brackets_round(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an brackets-round.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue864", angle=angle, style=style)


@guarded
def brackets_square(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an brackets-square.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue85e", angle=angle, style=style)


@guarded
def brain(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an brain.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue74e", angle=angle, style=style)


@guarded
def brandy(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an brandy.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue6b4", angle=angle, style=style)


@guarded
def bread(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an bread.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue81c", angle=angle, style=style)


@guarded
def bridge(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an bridge.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uea68", angle=angle, style=style)


@guarded
def briefcase(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an briefcase.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue0ee", angle=angle, style=style)


@guarded
def briefcase_metal(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an briefcase-metal.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue5f2", angle=angle, style=style)


@guarded
def broadcast(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an broadcast.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue0f2", angle=angle, style=style)


@guarded
def broom(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an broom.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uec54", angle=angle, style=style)


@guarded
def browser(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an browser.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue0f4", angle=angle, style=style)


@guarded
def browsers(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an browsers.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue0f6", angle=angle, style=style)


@guarded
def bug(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an bug.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue5f4", angle=angle, style=style)


@guarded
def bug_beetle(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an bug-beetle.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue5f6", angle=angle, style=style)


@guarded
def bug_droid(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an bug-droid.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue5f8", angle=angle, style=style)


@guarded
def building(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an building.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue100", angle=angle, style=style)


@guarded
def building_apartment(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an building-apartment.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue0fe", angle=angle, style=style)


@guarded
def building_office(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an building-office.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue0ff", angle=angle, style=style)


@guarded
def buildings(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an buildings.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue102", angle=angle, style=style)


@guarded
def bulldozer(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an bulldozer.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uec6c", angle=angle, style=style)


@guarded
def bus(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an bus.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue106", angle=angle, style=style)


@guarded
def butterfly(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an butterfly.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uea6e", angle=angle, style=style)


@guarded
def cable_car(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an cable-car.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue49c", angle=angle, style=style)


@guarded
def cactus(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an cactus.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue918", angle=angle, style=style)


@guarded
def cake(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an cake.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue780", angle=angle, style=style)


@guarded
def calculator(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an calculator.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue538", angle=angle, style=style)


@guarded
def calendar(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an calendar.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue108", angle=angle, style=style)


@guarded
def calendar_blank(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an calendar-blank.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue10a", angle=angle, style=style)


@guarded
def calendar_check(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an calendar-check.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue712", angle=angle, style=style)


@guarded
def calendar_dot(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an calendar-dot.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue7b2", angle=angle, style=style)


@guarded
def calendar_dots(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an calendar-dots.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue7b4", angle=angle, style=style)


@guarded
def calendar_heart(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an calendar-heart.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue8b0", angle=angle, style=style)


@guarded
def calendar_minus(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an calendar-minus.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uea14", angle=angle, style=style)


@guarded
def calendar_plus(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an calendar-plus.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue714", angle=angle, style=style)


@guarded
def calendar_slash(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an calendar-slash.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uea12", angle=angle, style=style)


@guarded
def calendar_star(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an calendar-star.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue8b2", angle=angle, style=style)


@guarded
def calendar_x(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an calendar-x.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue10c", angle=angle, style=style)


@guarded
def call_bell(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an call-bell.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue7de", angle=angle, style=style)


@guarded
def camera(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an camera.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue10e", angle=angle, style=style)


@guarded
def camera_plus(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an camera-plus.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uec58", angle=angle, style=style)


@guarded
def camera_rotate(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an camera-rotate.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue7a4", angle=angle, style=style)


@guarded
def camera_slash(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an camera-slash.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue110", angle=angle, style=style)


@guarded
def campfire(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an campfire.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue9d8", angle=angle, style=style)


@guarded
def car(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an car.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue112", angle=angle, style=style)


@guarded
def car_battery(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an car-battery.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uee30", angle=angle, style=style)


@guarded
def car_profile(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an car-profile.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue8cc", angle=angle, style=style)


@guarded
def car_simple(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an car-simple.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue114", angle=angle, style=style)


@guarded
def cardholder(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an cardholder.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue5fa", angle=angle, style=style)


@guarded
def cards(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an cards.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue0f8", angle=angle, style=style)


@guarded
def cards_three(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an cards-three.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uee50", angle=angle, style=style)


@guarded
def caret_circle_double_down(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an caret-circle-double-down.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue116", angle=angle, style=style)


@guarded
def caret_circle_double_left(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an caret-circle-double-left.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue118", angle=angle, style=style)


@guarded
def caret_circle_double_right(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an caret-circle-double-right.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue11a", angle=angle, style=style)


@guarded
def caret_circle_double_up(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an caret-circle-double-up.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue11c", angle=angle, style=style)


@guarded
def caret_circle_down(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an caret-circle-down.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue11e", angle=angle, style=style)


@guarded
def caret_circle_left(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an caret-circle-left.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue120", angle=angle, style=style)


@guarded
def caret_circle_right(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an caret-circle-right.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue122", angle=angle, style=style)


@guarded
def caret_circle_up(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an caret-circle-up.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue124", angle=angle, style=style)


@guarded
def caret_circle_up_down(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an caret-circle-up-down.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue13e", angle=angle, style=style)


@guarded
def caret_double_down(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an caret-double-down.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue126", angle=angle, style=style)


@guarded
def caret_double_left(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an caret-double-left.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue128", angle=angle, style=style)


@guarded
def caret_double_right(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an caret-double-right.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue12a", angle=angle, style=style)


@guarded
def caret_double_up(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an caret-double-up.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue12c", angle=angle, style=style)


@guarded
def caret_down(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an caret-down.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue136", angle=angle, style=style)


@guarded
def caret_left(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an caret-left.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue138", angle=angle, style=style)


@guarded
def caret_line_down(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an caret-line-down.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue134", angle=angle, style=style)


@guarded
def caret_line_left(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an caret-line-left.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue132", angle=angle, style=style)


@guarded
def caret_line_right(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an caret-line-right.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue130", angle=angle, style=style)


@guarded
def caret_line_up(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an caret-line-up.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue12e", angle=angle, style=style)


@guarded
def caret_right(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an caret-right.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue13a", angle=angle, style=style)


@guarded
def caret_up(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an caret-up.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue13c", angle=angle, style=style)


@guarded
def caret_up_down(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an caret-up-down.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue140", angle=angle, style=style)


@guarded
def carrot(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an carrot.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ued38", angle=angle, style=style)


@guarded
def cash_register(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an cash-register.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ued80", angle=angle, style=style)


@guarded
def cassette_tape(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an cassette-tape.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ued2e", angle=angle, style=style)


@guarded
def castle_turret(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an castle-turret.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue9d0", angle=angle, style=style)


@guarded
def cat(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an cat.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue748", angle=angle, style=style)


@guarded
def cell_signal_full(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an cell-signal-full.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue142", angle=angle, style=style)


@guarded
def cell_signal_high(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an cell-signal-high.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue144", angle=angle, style=style)


@guarded
def cell_signal_low(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an cell-signal-low.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue146", angle=angle, style=style)


@guarded
def cell_signal_medium(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an cell-signal-medium.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue148", angle=angle, style=style)


@guarded
def cell_signal_none(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an cell-signal-none.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue14a", angle=angle, style=style)


@guarded
def cell_signal_slash(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an cell-signal-slash.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue14c", angle=angle, style=style)


@guarded
def cell_signal_x(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an cell-signal-x.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue14e", angle=angle, style=style)


@guarded
def cell_tower(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an cell-tower.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uebaa", angle=angle, style=style)


@guarded
def certificate(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an certificate.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue766", angle=angle, style=style)


@guarded
def chair(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an chair.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue950", angle=angle, style=style)


@guarded
def chalkboard(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an chalkboard.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue5fc", angle=angle, style=style)


@guarded
def chalkboard_simple(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an chalkboard-simple.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue5fe", angle=angle, style=style)


@guarded
def chalkboard_teacher(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an chalkboard-teacher.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue600", angle=angle, style=style)


@guarded
def champagne(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an champagne.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ueaca", angle=angle, style=style)


@guarded
def charging_station(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an charging-station.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue8d0", angle=angle, style=style)


@guarded
def chart_bar(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an chart-bar.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue150", angle=angle, style=style)


@guarded
def chart_bar_horizontal(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an chart-bar-horizontal.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue152", angle=angle, style=style)


@guarded
def chart_donut(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an chart-donut.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ueaa6", angle=angle, style=style)


@guarded
def chart_line(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an chart-line.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue154", angle=angle, style=style)


@guarded
def chart_line_down(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an chart-line-down.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue8b6", angle=angle, style=style)


@guarded
def chart_line_up(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an chart-line-up.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue156", angle=angle, style=style)


@guarded
def chart_pie(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an chart-pie.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue158", angle=angle, style=style)


@guarded
def chart_pie_slice(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an chart-pie-slice.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue15a", angle=angle, style=style)


@guarded
def chart_polar(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an chart-polar.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ueaa8", angle=angle, style=style)


@guarded
def chart_scatter(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an chart-scatter.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ueaac", angle=angle, style=style)


@guarded
def chat(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an chat.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue15c", angle=angle, style=style)


@guarded
def chat_centered(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an chat-centered.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue160", angle=angle, style=style)


@guarded
def chat_centered_dots(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an chat-centered-dots.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue164", angle=angle, style=style)


@guarded
def chat_centered_slash(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an chat-centered-slash.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue162", angle=angle, style=style)


@guarded
def chat_centered_text(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an chat-centered-text.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue166", angle=angle, style=style)


@guarded
def chat_circle(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an chat-circle.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue168", angle=angle, style=style)


@guarded
def chat_circle_dots(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an chat-circle-dots.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue16c", angle=angle, style=style)


@guarded
def chat_circle_slash(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an chat-circle-slash.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue16a", angle=angle, style=style)


@guarded
def chat_circle_text(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an chat-circle-text.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue16e", angle=angle, style=style)


@guarded
def chat_dots(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an chat-dots.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue170", angle=angle, style=style)


@guarded
def chat_slash(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an chat-slash.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue15e", angle=angle, style=style)


@guarded
def chat_teardrop(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an chat-teardrop.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue172", angle=angle, style=style)


@guarded
def chat_teardrop_dots(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an chat-teardrop-dots.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue176", angle=angle, style=style)


@guarded
def chat_teardrop_slash(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an chat-teardrop-slash.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue174", angle=angle, style=style)


@guarded
def chat_teardrop_text(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an chat-teardrop-text.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue178", angle=angle, style=style)


@guarded
def chat_text(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an chat-text.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue17a", angle=angle, style=style)


@guarded
def chats(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an chats.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue17c", angle=angle, style=style)


@guarded
def chats_circle(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an chats-circle.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue17e", angle=angle, style=style)


@guarded
def chats_teardrop(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an chats-teardrop.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue180", angle=angle, style=style)


@guarded
def check(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an check.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue182", angle=angle, style=style)


@guarded
def check_circle(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an check-circle.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue184", angle=angle, style=style)


@guarded
def check_fat(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an check-fat.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ueba6", angle=angle, style=style)


@guarded
def check_square(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an check-square.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue186", angle=angle, style=style)


@guarded
def check_square_offset(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an check-square-offset.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue188", angle=angle, style=style)


@guarded
def checkerboard(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an checkerboard.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue8c4", angle=angle, style=style)


@guarded
def checks(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an checks.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue53a", angle=angle, style=style)


@guarded
def cheers(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an cheers.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uea4a", angle=angle, style=style)


@guarded
def cheese(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an cheese.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue9fe", angle=angle, style=style)


@guarded
def chef_hat(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an chef-hat.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ued8e", angle=angle, style=style)


@guarded
def cherries(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an cherries.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue830", angle=angle, style=style)


@guarded
def church(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an church.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uecea", angle=angle, style=style)


@guarded
def cigarette(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an cigarette.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ued90", angle=angle, style=style)


@guarded
def cigarette_slash(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an cigarette-slash.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ued92", angle=angle, style=style)


@guarded
def circle(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an circle.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue18a", angle=angle, style=style)


@guarded
def circle_dashed(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an circle-dashed.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue602", angle=angle, style=style)


@guarded
def circle_half(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an circle-half.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue18c", angle=angle, style=style)


@guarded
def circle_half_tilt(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an circle-half-tilt.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue18e", angle=angle, style=style)


@guarded
def circle_notch(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an circle-notch.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ueb44", angle=angle, style=style)


@guarded
def circles_four(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an circles-four.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue190", angle=angle, style=style)


@guarded
def circles_three(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an circles-three.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue192", angle=angle, style=style)


@guarded
def circles_three_plus(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an circles-three-plus.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue194", angle=angle, style=style)


@guarded
def circuitry(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an circuitry.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue9c2", angle=angle, style=style)


@guarded
def city(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an city.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uea6a", angle=angle, style=style)


@guarded
def clipboard(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an clipboard.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue196", angle=angle, style=style)


@guarded
def clipboard_text(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an clipboard-text.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue198", angle=angle, style=style)


@guarded
def clock(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an clock.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue19a", angle=angle, style=style)


@guarded
def clock_afternoon(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an clock-afternoon.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue19c", angle=angle, style=style)


@guarded
def clock_clockwise(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an clock-clockwise.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue19e", angle=angle, style=style)


@guarded
def clock_countdown(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an clock-countdown.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ued2c", angle=angle, style=style)


@guarded
def clock_counter_clockwise(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an clock-counter-clockwise.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue1a0", angle=angle, style=style)


@guarded
def clock_user(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an clock-user.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uedec", angle=angle, style=style)


@guarded
def closed_captioning(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an closed-captioning.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue1a4", angle=angle, style=style)


@guarded
def cloud(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an cloud.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue1aa", angle=angle, style=style)


@guarded
def cloud_arrow_down(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an cloud-arrow-down.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue1ac", angle=angle, style=style)


@guarded
def cloud_arrow_up(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an cloud-arrow-up.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue1ae", angle=angle, style=style)


@guarded
def cloud_check(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an cloud-check.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue1b0", angle=angle, style=style)


@guarded
def cloud_fog(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an cloud-fog.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue53c", angle=angle, style=style)


@guarded
def cloud_lightning(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an cloud-lightning.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue1b2", angle=angle, style=style)


@guarded
def cloud_moon(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an cloud-moon.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue53e", angle=angle, style=style)


@guarded
def cloud_rain(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an cloud-rain.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue1b4", angle=angle, style=style)


@guarded
def cloud_slash(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an cloud-slash.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue1b6", angle=angle, style=style)


@guarded
def cloud_snow(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an cloud-snow.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue1b8", angle=angle, style=style)


@guarded
def cloud_sun(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an cloud-sun.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue540", angle=angle, style=style)


@guarded
def cloud_warning(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an cloud-warning.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uea98", angle=angle, style=style)


@guarded
def cloud_x(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an cloud-x.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uea96", angle=angle, style=style)


@guarded
def clover(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an clover.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uedc8", angle=angle, style=style)


@guarded
def club(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an club.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue1ba", angle=angle, style=style)


@guarded
def coat_hanger(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an coat-hanger.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue7fe", angle=angle, style=style)


@guarded
def coda_logo(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an coda-logo.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue7ce", angle=angle, style=style)


@guarded
def code(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an code.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue1bc", angle=angle, style=style)


@guarded
def code_block(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an code-block.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ueafe", angle=angle, style=style)


@guarded
def code_simple(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an code-simple.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue1be", angle=angle, style=style)


@guarded
def codepen_logo(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an codepen-logo.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue978", angle=angle, style=style)


@guarded
def codesandbox_logo(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an codesandbox-logo.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uea06", angle=angle, style=style)


@guarded
def coffee(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an coffee.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue1c2", angle=angle, style=style)


@guarded
def coffee_bean(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an coffee-bean.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue1c0", angle=angle, style=style)


@guarded
def coin(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an coin.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue60e", angle=angle, style=style)


@guarded
def coin_vertical(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an coin-vertical.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ueb48", angle=angle, style=style)


@guarded
def coins(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an coins.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue78e", angle=angle, style=style)


@guarded
def columns(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an columns.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue546", angle=angle, style=style)


@guarded
def columns_plus_left(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an columns-plus-left.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue544", angle=angle, style=style)


@guarded
def columns_plus_right(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an columns-plus-right.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue542", angle=angle, style=style)


@guarded
def command(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an command.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue1c4", angle=angle, style=style)


@guarded
def compass(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an compass.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue1c8", angle=angle, style=style)


@guarded
def compass_rose(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an compass-rose.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue1c6", angle=angle, style=style)


@guarded
def compass_tool(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an compass-tool.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uea0e", angle=angle, style=style)


@guarded
def computer_tower(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an computer-tower.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue548", angle=angle, style=style)


@guarded
def confetti(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an confetti.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue81a", angle=angle, style=style)


@guarded
def contactless_payment(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an contactless-payment.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ued42", angle=angle, style=style)


@guarded
def control(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an control.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ueca6", angle=angle, style=style)


@guarded
def cookie(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an cookie.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue6ca", angle=angle, style=style)


@guarded
def cooking_pot(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an cooking-pot.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue764", angle=angle, style=style)


@guarded
def copy(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an copy.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue1ca", angle=angle, style=style)


@guarded
def copy_simple(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an copy-simple.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue1cc", angle=angle, style=style)


@guarded
def copyleft(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an copyleft.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue86a", angle=angle, style=style)


@guarded
def copyright(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an copyright.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue54a", angle=angle, style=style)


@guarded
def corners_in(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an corners-in.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue1ce", angle=angle, style=style)


@guarded
def corners_out(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an corners-out.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue1d0", angle=angle, style=style)


@guarded
def couch(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an couch.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue7f6", angle=angle, style=style)


@guarded
def court_basketball(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an court-basketball.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uee36", angle=angle, style=style)


@guarded
def cow(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an cow.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ueabe", angle=angle, style=style)


@guarded
def cowboy_hat(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an cowboy-hat.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ued12", angle=angle, style=style)


@guarded
def cpu(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an cpu.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue610", angle=angle, style=style)


@guarded
def crane(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an crane.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ued48", angle=angle, style=style)


@guarded
def crane_tower(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an crane-tower.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ued49", angle=angle, style=style)


@guarded
def credit_card(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an credit-card.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue1d2", angle=angle, style=style)


@guarded
def cricket(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an cricket.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uee12", angle=angle, style=style)


@guarded
def crop(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an crop.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue1d4", angle=angle, style=style)


@guarded
def cross(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an cross.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue8a0", angle=angle, style=style)


@guarded
def crosshair(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an crosshair.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue1d6", angle=angle, style=style)


@guarded
def crosshair_simple(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an crosshair-simple.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue1d8", angle=angle, style=style)


@guarded
def crown(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an crown.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue614", angle=angle, style=style)


@guarded
def crown_cross(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an crown-cross.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uee5e", angle=angle, style=style)


@guarded
def crown_simple(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an crown-simple.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue616", angle=angle, style=style)


@guarded
def cube(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an cube.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue1da", angle=angle, style=style)


@guarded
def cube_focus(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an cube-focus.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ued0a", angle=angle, style=style)


@guarded
def cube_transparent(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an cube-transparent.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uec7c", angle=angle, style=style)


@guarded
def currency_btc(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an currency-btc.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue618", angle=angle, style=style)


@guarded
def currency_circle_dollar(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an currency-circle-dollar.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue54c", angle=angle, style=style)


@guarded
def currency_cny(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an currency-cny.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue54e", angle=angle, style=style)


@guarded
def currency_dollar(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an currency-dollar.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue550", angle=angle, style=style)


@guarded
def currency_dollar_simple(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an currency-dollar-simple.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue552", angle=angle, style=style)


@guarded
def currency_eth(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an currency-eth.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ueada", angle=angle, style=style)


@guarded
def currency_eur(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an currency-eur.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue554", angle=angle, style=style)


@guarded
def currency_gbp(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an currency-gbp.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue556", angle=angle, style=style)


@guarded
def currency_inr(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an currency-inr.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue558", angle=angle, style=style)


@guarded
def currency_jpy(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an currency-jpy.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue55a", angle=angle, style=style)


@guarded
def currency_krw(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an currency-krw.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue55c", angle=angle, style=style)


@guarded
def currency_kzt(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an currency-kzt.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uec4c", angle=angle, style=style)


@guarded
def currency_ngn(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an currency-ngn.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ueb52", angle=angle, style=style)


@guarded
def currency_rub(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an currency-rub.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue55e", angle=angle, style=style)


@guarded
def cursor(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an cursor.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue1dc", angle=angle, style=style)


@guarded
def cursor_click(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an cursor-click.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue7c8", angle=angle, style=style)


@guarded
def cursor_text(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an cursor-text.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue7d8", angle=angle, style=style)


@guarded
def cylinder(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an cylinder.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue8fc", angle=angle, style=style)


@guarded
def database(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an database.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue1de", angle=angle, style=style)


@guarded
def desk(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an desk.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ued16", angle=angle, style=style)


@guarded
def desktop(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an desktop.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue560", angle=angle, style=style)


@guarded
def desktop_tower(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an desktop-tower.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue562", angle=angle, style=style)


@guarded
def detective(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an detective.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue83e", angle=angle, style=style)


@guarded
def dev_to_logo(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an dev-to-logo.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ued0e", angle=angle, style=style)


@guarded
def device_mobile(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an device-mobile.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue1e0", angle=angle, style=style)


@guarded
def device_mobile_camera(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an device-mobile-camera.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue1e2", angle=angle, style=style)


@guarded
def device_mobile_slash(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an device-mobile-slash.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uee46", angle=angle, style=style)


@guarded
def device_mobile_speaker(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an device-mobile-speaker.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue1e4", angle=angle, style=style)


@guarded
def device_rotate(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an device-rotate.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uedf2", angle=angle, style=style)


@guarded
def device_tablet(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an device-tablet.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue1e6", angle=angle, style=style)


@guarded
def device_tablet_camera(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an device-tablet-camera.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue1e8", angle=angle, style=style)


@guarded
def device_tablet_speaker(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an device-tablet-speaker.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue1ea", angle=angle, style=style)


@guarded
def devices(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an devices.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ueba4", angle=angle, style=style)


@guarded
def diamond(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an diamond.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue1ec", angle=angle, style=style)


@guarded
def diamonds_four(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an diamonds-four.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue8f4", angle=angle, style=style)


@guarded
def dice_five(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an dice-five.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue1ee", angle=angle, style=style)


@guarded
def dice_four(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an dice-four.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue1f0", angle=angle, style=style)


@guarded
def dice_one(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an dice-one.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue1f2", angle=angle, style=style)


@guarded
def dice_six(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an dice-six.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue1f4", angle=angle, style=style)


@guarded
def dice_three(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an dice-three.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue1f6", angle=angle, style=style)


@guarded
def dice_two(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an dice-two.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue1f8", angle=angle, style=style)


@guarded
def disc(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an disc.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue564", angle=angle, style=style)


@guarded
def disco_ball(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an disco-ball.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ued98", angle=angle, style=style)


@guarded
def discord_logo(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an discord-logo.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue61a", angle=angle, style=style)


@guarded
def divide(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an divide.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue1fa", angle=angle, style=style)


@guarded
def dna(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an dna.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue924", angle=angle, style=style)


@guarded
def dog(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an dog.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue74a", angle=angle, style=style)


@guarded
def door(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an door.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue61c", angle=angle, style=style)


@guarded
def door_open(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an door-open.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue7e6", angle=angle, style=style)


@guarded
def dot(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an dot.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uecde", angle=angle, style=style)


@guarded
def dot_outline(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an dot-outline.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uece0", angle=angle, style=style)


@guarded
def dots_nine(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an dots-nine.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue1fc", angle=angle, style=style)


@guarded
def dots_six(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an dots-six.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue794", angle=angle, style=style)


@guarded
def dots_six_vertical(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an dots-six-vertical.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ueae2", angle=angle, style=style)


@guarded
def dots_three(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an dots-three.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue1fe", angle=angle, style=style)


@guarded
def dots_three_circle(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an dots-three-circle.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue200", angle=angle, style=style)


@guarded
def dots_three_circle_vertical(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an dots-three-circle-vertical.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue202", angle=angle, style=style)


@guarded
def dots_three_outline(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an dots-three-outline.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue204", angle=angle, style=style)


@guarded
def dots_three_outline_vertical(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an dots-three-outline-vertical.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue206", angle=angle, style=style)


@guarded
def dots_three_vertical(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an dots-three-vertical.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue208", angle=angle, style=style)


@guarded
def download(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an download.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue20a", angle=angle, style=style)


@guarded
def download_simple(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an download-simple.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue20c", angle=angle, style=style)


@guarded
def dress(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an dress.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uea7e", angle=angle, style=style)


@guarded
def dresser(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an dresser.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue94e", angle=angle, style=style)


@guarded
def dribbble_logo(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an dribbble-logo.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue20e", angle=angle, style=style)


@guarded
def drone(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an drone.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ued74", angle=angle, style=style)


@guarded
def drop(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an drop.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue210", angle=angle, style=style)


@guarded
def drop_half(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an drop-half.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue566", angle=angle, style=style)


@guarded
def drop_half_bottom(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an drop-half-bottom.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ueb40", angle=angle, style=style)


@guarded
def drop_simple(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an drop-simple.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uee32", angle=angle, style=style)


@guarded
def drop_slash(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an drop-slash.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue954", angle=angle, style=style)


@guarded
def dropbox_logo(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an dropbox-logo.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue7d0", angle=angle, style=style)


@guarded
def ear(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an ear.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue70c", angle=angle, style=style)


@guarded
def ear_slash(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an ear-slash.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue70e", angle=angle, style=style)


@guarded
def egg(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an egg.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue812", angle=angle, style=style)


@guarded
def egg_crack(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an egg-crack.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ueb64", angle=angle, style=style)


@guarded
def eject(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an eject.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue212", angle=angle, style=style)


@guarded
def eject_simple(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an eject-simple.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue6ae", angle=angle, style=style)


@guarded
def elevator(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an elevator.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uecc0", angle=angle, style=style)


@guarded
def empty(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an empty.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uedbc", angle=angle, style=style)


@guarded
def engine(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an engine.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uea80", angle=angle, style=style)


@guarded
def envelope(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an envelope.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue214", angle=angle, style=style)


@guarded
def envelope_open(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an envelope-open.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue216", angle=angle, style=style)


@guarded
def envelope_simple(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an envelope-simple.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue218", angle=angle, style=style)


@guarded
def envelope_simple_open(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an envelope-simple-open.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue21a", angle=angle, style=style)


@guarded
def equalizer(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an equalizer.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uebbc", angle=angle, style=style)


@guarded
def equals(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an equals.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue21c", angle=angle, style=style)


@guarded
def eraser(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an eraser.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue21e", angle=angle, style=style)


@guarded
def escalator_down(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an escalator-down.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uecba", angle=angle, style=style)


@guarded
def escalator_up(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an escalator-up.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uecbc", angle=angle, style=style)


@guarded
def exam(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an exam.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue742", angle=angle, style=style)


@guarded
def exclamation_mark(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an exclamation-mark.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uee44", angle=angle, style=style)


@guarded
def exclude(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an exclude.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue882", angle=angle, style=style)


@guarded
def exclude_square(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an exclude-square.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue880", angle=angle, style=style)


@guarded
def export(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an export.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ueaf0", angle=angle, style=style)


@guarded
def eye(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an eye.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue220", angle=angle, style=style)


@guarded
def eye_closed(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an eye-closed.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue222", angle=angle, style=style)


@guarded
def eye_slash(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an eye-slash.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue224", angle=angle, style=style)


@guarded
def eyedropper(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an eyedropper.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue568", angle=angle, style=style)


@guarded
def eyedropper_sample(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an eyedropper-sample.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ueac4", angle=angle, style=style)


@guarded
def eyeglasses(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an eyeglasses.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue7ba", angle=angle, style=style)


@guarded
def eyes(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an eyes.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uee5c", angle=angle, style=style)


@guarded
def face_mask(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an face-mask.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue56a", angle=angle, style=style)


@guarded
def facebook_logo(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an facebook-logo.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue226", angle=angle, style=style)


@guarded
def factory(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an factory.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue760", angle=angle, style=style)


@guarded
def faders(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an faders.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue228", angle=angle, style=style)


@guarded
def faders_horizontal(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an faders-horizontal.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue22a", angle=angle, style=style)


@guarded
def fallout_shelter(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an fallout-shelter.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue9de", angle=angle, style=style)


@guarded
def fan(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an fan.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue9f2", angle=angle, style=style)


@guarded
def farm(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an farm.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uec70", angle=angle, style=style)


@guarded
def fast_forward(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an fast-forward.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue6a6", angle=angle, style=style)


@guarded
def fast_forward_circle(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an fast-forward-circle.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue22c", angle=angle, style=style)


@guarded
def feather(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an feather.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue9c0", angle=angle, style=style)


@guarded
def fediverse_logo(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an fediverse-logo.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ued66", angle=angle, style=style)


@guarded
def figma_logo(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an figma-logo.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue22e", angle=angle, style=style)


@guarded
def file(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an file.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue230", angle=angle, style=style)


@guarded
def file_archive(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an file-archive.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ueb2a", angle=angle, style=style)


@guarded
def file_arrow_down(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an file-arrow-down.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue232", angle=angle, style=style)


@guarded
def file_arrow_up(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an file-arrow-up.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue61e", angle=angle, style=style)


@guarded
def file_audio(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an file-audio.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uea20", angle=angle, style=style)


@guarded
def file_c(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an file-c.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ueb32", angle=angle, style=style)


@guarded
def file_c_sharp(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an file-c-sharp.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ueb30", angle=angle, style=style)


@guarded
def file_cloud(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an file-cloud.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue95e", angle=angle, style=style)


@guarded
def file_code(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an file-code.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue914", angle=angle, style=style)


@guarded
def file_cpp(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an file-cpp.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ueb2e", angle=angle, style=style)


@guarded
def file_css(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an file-css.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ueb34", angle=angle, style=style)


@guarded
def file_csv(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an file-csv.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ueb1c", angle=angle, style=style)


@guarded
def file_dashed(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an file-dashed.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue704", angle=angle, style=style)


@guarded
def file_dotted(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an file-dotted.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue704", angle=angle, style=style)


@guarded
def file_doc(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an file-doc.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ueb1e", angle=angle, style=style)


@guarded
def file_html(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an file-html.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ueb38", angle=angle, style=style)


@guarded
def file_image(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an file-image.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uea24", angle=angle, style=style)


@guarded
def file_ini(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an file-ini.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ueb33", angle=angle, style=style)


@guarded
def file_jpg(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an file-jpg.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ueb1a", angle=angle, style=style)


@guarded
def file_js(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an file-js.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ueb24", angle=angle, style=style)


@guarded
def file_jsx(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an file-jsx.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ueb3a", angle=angle, style=style)


@guarded
def file_lock(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an file-lock.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue95c", angle=angle, style=style)


@guarded
def file_magnifying_glass(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an file-magnifying-glass.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue238", angle=angle, style=style)


@guarded
def file_search(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an file-search.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue238", angle=angle, style=style)


@guarded
def file_md(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an file-md.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ued50", angle=angle, style=style)


@guarded
def file_minus(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an file-minus.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue234", angle=angle, style=style)


@guarded
def file_pdf(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an file-pdf.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue702", angle=angle, style=style)


@guarded
def file_plus(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an file-plus.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue236", angle=angle, style=style)


@guarded
def file_png(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an file-png.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ueb18", angle=angle, style=style)


@guarded
def file_ppt(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an file-ppt.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ueb20", angle=angle, style=style)


@guarded
def file_py(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an file-py.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ueb2c", angle=angle, style=style)


@guarded
def file_rs(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an file-rs.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ueb28", angle=angle, style=style)


@guarded
def file_sql(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an file-sql.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ued4e", angle=angle, style=style)


@guarded
def file_svg(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an file-svg.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ued08", angle=angle, style=style)


@guarded
def file_text(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an file-text.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue23a", angle=angle, style=style)


@guarded
def file_ts(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an file-ts.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ueb26", angle=angle, style=style)


@guarded
def file_tsx(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an file-tsx.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ueb3c", angle=angle, style=style)


@guarded
def file_txt(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an file-txt.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ueb35", angle=angle, style=style)


@guarded
def file_video(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an file-video.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uea22", angle=angle, style=style)


@guarded
def file_vue(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an file-vue.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ueb3e", angle=angle, style=style)


@guarded
def file_x(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an file-x.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue23c", angle=angle, style=style)


@guarded
def file_xls(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an file-xls.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ueb22", angle=angle, style=style)


@guarded
def file_zip(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an file-zip.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue958", angle=angle, style=style)


@guarded
def files(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an files.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue710", angle=angle, style=style)


@guarded
def film_reel(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an film-reel.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue8c0", angle=angle, style=style)


@guarded
def film_script(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an film-script.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ueb50", angle=angle, style=style)


@guarded
def film_slate(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an film-slate.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue8c2", angle=angle, style=style)


@guarded
def film_strip(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an film-strip.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue792", angle=angle, style=style)


@guarded
def fingerprint(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an fingerprint.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue23e", angle=angle, style=style)


@guarded
def fingerprint_simple(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an fingerprint-simple.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue240", angle=angle, style=style)


@guarded
def finn_the_human(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an finn-the-human.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue56c", angle=angle, style=style)


@guarded
def fire(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an fire.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue242", angle=angle, style=style)


@guarded
def fire_extinguisher(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an fire-extinguisher.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue9e8", angle=angle, style=style)


@guarded
def fire_simple(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an fire-simple.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue620", angle=angle, style=style)


@guarded
def fire_truck(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an fire-truck.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue574", angle=angle, style=style)


@guarded
def first_aid(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an first-aid.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue56e", angle=angle, style=style)


@guarded
def first_aid_kit(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an first-aid-kit.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue570", angle=angle, style=style)


@guarded
def fish(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an fish.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue728", angle=angle, style=style)


@guarded
def fish_simple(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an fish-simple.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue72a", angle=angle, style=style)


@guarded
def flag(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an flag.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue244", angle=angle, style=style)


@guarded
def flag_banner(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an flag-banner.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue622", angle=angle, style=style)


@guarded
def flag_banner_fold(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an flag-banner-fold.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uecf2", angle=angle, style=style)


@guarded
def flag_checkered(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an flag-checkered.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uea38", angle=angle, style=style)


@guarded
def flag_pennant(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an flag-pennant.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uecf0", angle=angle, style=style)


@guarded
def flame(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an flame.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue624", angle=angle, style=style)


@guarded
def flashlight(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an flashlight.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue246", angle=angle, style=style)


@guarded
def flask(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an flask.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue79e", angle=angle, style=style)


@guarded
def flip_horizontal(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an flip-horizontal.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ued6a", angle=angle, style=style)


@guarded
def flip_vertical(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an flip-vertical.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ued6c", angle=angle, style=style)


@guarded
def floppy_disk(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an floppy-disk.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue248", angle=angle, style=style)


@guarded
def floppy_disk_back(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an floppy-disk-back.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ueaf4", angle=angle, style=style)


@guarded
def flow_arrow(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an flow-arrow.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue6ec", angle=angle, style=style)


@guarded
def flower(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an flower.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue75e", angle=angle, style=style)


@guarded
def flower_lotus(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an flower-lotus.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue6cc", angle=angle, style=style)


@guarded
def flower_tulip(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an flower-tulip.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ueacc", angle=angle, style=style)


@guarded
def flying_saucer(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an flying-saucer.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ueb4a", angle=angle, style=style)


@guarded
def folder(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an folder.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue24a", angle=angle, style=style)


@guarded
def folder_notch(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an folder-notch.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue24a", angle=angle, style=style)


@guarded
def folder_dashed(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an folder-dashed.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue8f8", angle=angle, style=style)


@guarded
def folder_dotted(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an folder-dotted.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue8f8", angle=angle, style=style)


@guarded
def folder_lock(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an folder-lock.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uea3c", angle=angle, style=style)


@guarded
def folder_minus(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an folder-minus.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue254", angle=angle, style=style)


@guarded
def folder_notch_minus(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an folder-notch-minus.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue254", angle=angle, style=style)


@guarded
def folder_open(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an folder-open.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue256", angle=angle, style=style)


@guarded
def folder_notch_open(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an folder-notch-open.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue256", angle=angle, style=style)


@guarded
def folder_plus(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an folder-plus.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue258", angle=angle, style=style)


@guarded
def folder_notch_plus(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an folder-notch-plus.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue258", angle=angle, style=style)


@guarded
def folder_simple(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an folder-simple.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue25a", angle=angle, style=style)


@guarded
def folder_simple_dashed(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an folder-simple-dashed.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uec2a", angle=angle, style=style)


@guarded
def folder_simple_dotted(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an folder-simple-dotted.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uec2a", angle=angle, style=style)


@guarded
def folder_simple_lock(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an folder-simple-lock.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ueb5e", angle=angle, style=style)


@guarded
def folder_simple_minus(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an folder-simple-minus.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue25c", angle=angle, style=style)


@guarded
def folder_simple_plus(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an folder-simple-plus.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue25e", angle=angle, style=style)


@guarded
def folder_simple_star(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an folder-simple-star.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uec2e", angle=angle, style=style)


@guarded
def folder_simple_user(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an folder-simple-user.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ueb60", angle=angle, style=style)


@guarded
def folder_star(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an folder-star.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uea86", angle=angle, style=style)


@guarded
def folder_user(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an folder-user.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ueb46", angle=angle, style=style)


@guarded
def folders(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an folders.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue260", angle=angle, style=style)


@guarded
def football(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an football.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue718", angle=angle, style=style)


@guarded
def football_helmet(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an football-helmet.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uee4c", angle=angle, style=style)


@guarded
def footprints(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an footprints.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uea88", angle=angle, style=style)


@guarded
def fork_knife(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an fork-knife.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue262", angle=angle, style=style)


@guarded
def four_k(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an four-k.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uea5c", angle=angle, style=style)


@guarded
def frame_corners(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an frame-corners.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue626", angle=angle, style=style)


@guarded
def framer_logo(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an framer-logo.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue264", angle=angle, style=style)


@guarded
def function(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an function.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uebe4", angle=angle, style=style)


@guarded
def funnel(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an funnel.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue266", angle=angle, style=style)


@guarded
def funnel_simple(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an funnel-simple.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue268", angle=angle, style=style)


@guarded
def funnel_simple_x(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an funnel-simple-x.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue26a", angle=angle, style=style)


@guarded
def funnel_x(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an funnel-x.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue26c", angle=angle, style=style)


@guarded
def game_controller(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an game-controller.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue26e", angle=angle, style=style)


@guarded
def garage(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an garage.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uecd6", angle=angle, style=style)


@guarded
def gas_can(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an gas-can.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue8ce", angle=angle, style=style)


@guarded
def gas_pump(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an gas-pump.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue768", angle=angle, style=style)


@guarded
def gauge(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an gauge.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue628", angle=angle, style=style)


@guarded
def gavel(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an gavel.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uea32", angle=angle, style=style)


@guarded
def gear(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an gear.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue270", angle=angle, style=style)


@guarded
def gear_fine(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an gear-fine.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue87c", angle=angle, style=style)


@guarded
def gear_six(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an gear-six.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue272", angle=angle, style=style)


@guarded
def gender_female(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an gender-female.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue6e0", angle=angle, style=style)


@guarded
def gender_intersex(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an gender-intersex.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue6e6", angle=angle, style=style)


@guarded
def gender_male(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an gender-male.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue6e2", angle=angle, style=style)


@guarded
def gender_neuter(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an gender-neuter.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue6ea", angle=angle, style=style)


@guarded
def gender_nonbinary(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an gender-nonbinary.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue6e4", angle=angle, style=style)


@guarded
def gender_transgender(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an gender-transgender.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue6e8", angle=angle, style=style)


@guarded
def ghost(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an ghost.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue62a", angle=angle, style=style)


@guarded
def gif(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an gif.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue274", angle=angle, style=style)


@guarded
def gift(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an gift.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue276", angle=angle, style=style)


@guarded
def git_branch(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an git-branch.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue278", angle=angle, style=style)


@guarded
def git_commit(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an git-commit.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue27a", angle=angle, style=style)


@guarded
def git_diff(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an git-diff.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue27c", angle=angle, style=style)


@guarded
def git_fork(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an git-fork.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue27e", angle=angle, style=style)


@guarded
def git_merge(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an git-merge.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue280", angle=angle, style=style)


@guarded
def git_pull_request(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an git-pull-request.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue282", angle=angle, style=style)


@guarded
def github_logo(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an github-logo.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue576", angle=angle, style=style)


@guarded
def gitlab_logo(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an gitlab-logo.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue694", angle=angle, style=style)


@guarded
def gitlab_logo_simple(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an gitlab-logo-simple.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue696", angle=angle, style=style)


@guarded
def globe(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an globe.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue288", angle=angle, style=style)


@guarded
def globe_hemisphere_east(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an globe-hemisphere-east.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue28a", angle=angle, style=style)


@guarded
def globe_hemisphere_west(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an globe-hemisphere-west.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue28c", angle=angle, style=style)


@guarded
def globe_simple(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an globe-simple.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue28e", angle=angle, style=style)


@guarded
def globe_simple_x(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an globe-simple-x.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue284", angle=angle, style=style)


@guarded
def globe_stand(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an globe-stand.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue290", angle=angle, style=style)


@guarded
def globe_x(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an globe-x.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue286", angle=angle, style=style)


@guarded
def goggles(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an goggles.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uecb4", angle=angle, style=style)


@guarded
def golf(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an golf.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uea3e", angle=angle, style=style)


@guarded
def goodreads_logo(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an goodreads-logo.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ued10", angle=angle, style=style)


@guarded
def google_cardboard_logo(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an google-cardboard-logo.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue7b6", angle=angle, style=style)


@guarded
def google_chrome_logo(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an google-chrome-logo.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue976", angle=angle, style=style)


@guarded
def google_drive_logo(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an google-drive-logo.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue8f6", angle=angle, style=style)


@guarded
def google_logo(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an google-logo.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue292", angle=angle, style=style)


@guarded
def google_photos_logo(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an google-photos-logo.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ueb92", angle=angle, style=style)


@guarded
def google_play_logo(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an google-play-logo.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue294", angle=angle, style=style)


@guarded
def google_podcasts_logo(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an google-podcasts-logo.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ueb94", angle=angle, style=style)


@guarded
def gps(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an gps.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uedd8", angle=angle, style=style)


@guarded
def gps_fix(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an gps-fix.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uedd6", angle=angle, style=style)


@guarded
def gps_slash(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an gps-slash.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uedd4", angle=angle, style=style)


@guarded
def gradient(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an gradient.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ueb42", angle=angle, style=style)


@guarded
def graduation_cap(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an graduation-cap.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue62c", angle=angle, style=style)


@guarded
def grains(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an grains.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uec68", angle=angle, style=style)


@guarded
def grains_slash(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an grains-slash.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uec6a", angle=angle, style=style)


@guarded
def graph(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an graph.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ueb58", angle=angle, style=style)


@guarded
def graphics_card(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an graphics-card.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue612", angle=angle, style=style)


@guarded
def greater_than(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an greater-than.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uedc4", angle=angle, style=style)


@guarded
def greater_than_or_equal(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an greater-than-or-equal.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ueda2", angle=angle, style=style)


@guarded
def grid_four(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an grid-four.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue296", angle=angle, style=style)


@guarded
def grid_nine(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an grid-nine.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uec8c", angle=angle, style=style)


@guarded
def guitar(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an guitar.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uea8a", angle=angle, style=style)


@guarded
def hair_dryer(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an hair-dryer.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uea66", angle=angle, style=style)


@guarded
def hamburger(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an hamburger.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue790", angle=angle, style=style)


@guarded
def hammer(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an hammer.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue80e", angle=angle, style=style)


@guarded
def hand(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an hand.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue298", angle=angle, style=style)


@guarded
def hand_arrow_down(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an hand-arrow-down.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uea4e", angle=angle, style=style)


@guarded
def hand_arrow_up(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an hand-arrow-up.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uee5a", angle=angle, style=style)


@guarded
def hand_coins(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an hand-coins.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uea8c", angle=angle, style=style)


@guarded
def hand_deposit(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an hand-deposit.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uee82", angle=angle, style=style)


@guarded
def hand_eye(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an hand-eye.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uea4c", angle=angle, style=style)


@guarded
def hand_fist(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an hand-fist.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue57a", angle=angle, style=style)


@guarded
def hand_grabbing(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an hand-grabbing.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue57c", angle=angle, style=style)


@guarded
def hand_heart(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an hand-heart.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue810", angle=angle, style=style)


@guarded
def hand_palm(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an hand-palm.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue57e", angle=angle, style=style)


@guarded
def hand_peace(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an hand-peace.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue7cc", angle=angle, style=style)


@guarded
def hand_pointing(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an hand-pointing.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue29a", angle=angle, style=style)


@guarded
def hand_soap(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an hand-soap.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue630", angle=angle, style=style)


@guarded
def hand_swipe_left(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an hand-swipe-left.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uec94", angle=angle, style=style)


@guarded
def hand_swipe_right(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an hand-swipe-right.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uec92", angle=angle, style=style)


@guarded
def hand_tap(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an hand-tap.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uec90", angle=angle, style=style)


@guarded
def hand_waving(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an hand-waving.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue580", angle=angle, style=style)


@guarded
def hand_withdraw(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an hand-withdraw.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uee80", angle=angle, style=style)


@guarded
def handbag(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an handbag.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue29c", angle=angle, style=style)


@guarded
def handbag_simple(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an handbag-simple.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue62e", angle=angle, style=style)


@guarded
def hands_clapping(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an hands-clapping.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue6a0", angle=angle, style=style)


@guarded
def hands_praying(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an hands-praying.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uecc8", angle=angle, style=style)


@guarded
def handshake(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an handshake.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue582", angle=angle, style=style)


@guarded
def hard_drive(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an hard-drive.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue29e", angle=angle, style=style)


@guarded
def hard_drives(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an hard-drives.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue2a0", angle=angle, style=style)


@guarded
def hard_hat(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an hard-hat.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ued46", angle=angle, style=style)


@guarded
def hash(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an hash.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue2a2", angle=angle, style=style)


@guarded
def hash_straight(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an hash-straight.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue2a4", angle=angle, style=style)


@guarded
def head_circuit(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an head-circuit.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue7d4", angle=angle, style=style)


@guarded
def headlights(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an headlights.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue6fe", angle=angle, style=style)


@guarded
def headphones(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an headphones.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue2a6", angle=angle, style=style)


@guarded
def headset(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an headset.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue584", angle=angle, style=style)


@guarded
def heart(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an heart.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue2a8", angle=angle, style=style)


@guarded
def heart_break(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an heart-break.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uebe8", angle=angle, style=style)


@guarded
def heart_half(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an heart-half.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uec48", angle=angle, style=style)


@guarded
def heart_straight(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an heart-straight.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue2aa", angle=angle, style=style)


@guarded
def heart_straight_break(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an heart-straight-break.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ueb98", angle=angle, style=style)


@guarded
def heartbeat(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an heartbeat.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue2ac", angle=angle, style=style)


@guarded
def hexagon(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an hexagon.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue2ae", angle=angle, style=style)


@guarded
def high_definition(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an high-definition.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uea8e", angle=angle, style=style)


@guarded
def high_heel(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an high-heel.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue8e8", angle=angle, style=style)


@guarded
def highlighter(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an highlighter.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uec76", angle=angle, style=style)


@guarded
def highlighter_circle(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an highlighter-circle.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue632", angle=angle, style=style)


@guarded
def hockey(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an hockey.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uec86", angle=angle, style=style)


@guarded
def hoodie(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an hoodie.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uecd0", angle=angle, style=style)


@guarded
def horse(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an horse.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue2b0", angle=angle, style=style)


@guarded
def hospital(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an hospital.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue844", angle=angle, style=style)


@guarded
def hourglass(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an hourglass.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue2b2", angle=angle, style=style)


@guarded
def hourglass_high(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an hourglass-high.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue2b4", angle=angle, style=style)


@guarded
def hourglass_low(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an hourglass-low.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue2b6", angle=angle, style=style)


@guarded
def hourglass_medium(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an hourglass-medium.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue2b8", angle=angle, style=style)


@guarded
def hourglass_simple(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an hourglass-simple.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue2ba", angle=angle, style=style)


@guarded
def hourglass_simple_high(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an hourglass-simple-high.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue2bc", angle=angle, style=style)


@guarded
def hourglass_simple_low(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an hourglass-simple-low.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue2be", angle=angle, style=style)


@guarded
def hourglass_simple_medium(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an hourglass-simple-medium.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue2c0", angle=angle, style=style)


@guarded
def house(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an house.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue2c2", angle=angle, style=style)


@guarded
def house_line(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an house-line.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue2c4", angle=angle, style=style)


@guarded
def house_simple(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an house-simple.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue2c6", angle=angle, style=style)


@guarded
def hurricane(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an hurricane.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue88e", angle=angle, style=style)


@guarded
def ice_cream(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an ice-cream.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue804", angle=angle, style=style)


@guarded
def identification_badge(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an identification-badge.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue6f6", angle=angle, style=style)


@guarded
def identification_card(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an identification-card.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue2c8", angle=angle, style=style)


@guarded
def image(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an image.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue2ca", angle=angle, style=style)


@guarded
def image_broken(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an image-broken.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue7a8", angle=angle, style=style)


@guarded
def image_square(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an image-square.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue2cc", angle=angle, style=style)


@guarded
def images(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an images.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue836", angle=angle, style=style)


@guarded
def images_square(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an images-square.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue834", angle=angle, style=style)


@guarded
def infinity(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an infinity.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue634", angle=angle, style=style)


@guarded
def lemniscate(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an lemniscate.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue634", angle=angle, style=style)


@guarded
def info(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an info.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue2ce", angle=angle, style=style)


@guarded
def instagram_logo(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an instagram-logo.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue2d0", angle=angle, style=style)


@guarded
def intersect(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an intersect.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue2d2", angle=angle, style=style)


@guarded
def intersect_square(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an intersect-square.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue87a", angle=angle, style=style)


@guarded
def intersect_three(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an intersect-three.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uecc4", angle=angle, style=style)


@guarded
def intersection(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an intersection.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uedba", angle=angle, style=style)


@guarded
def invoice(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an invoice.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uee42", angle=angle, style=style)


@guarded
def island(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an island.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uee06", angle=angle, style=style)


@guarded
def jar(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an jar.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue7e0", angle=angle, style=style)


@guarded
def jar_label(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an jar-label.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue7e1", angle=angle, style=style)


@guarded
def jeep(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an jeep.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue2d4", angle=angle, style=style)


@guarded
def joystick(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an joystick.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uea5e", angle=angle, style=style)


@guarded
def kanban(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an kanban.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ueb54", angle=angle, style=style)


@guarded
def key(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an key.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue2d6", angle=angle, style=style)


@guarded
def key_return(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an key-return.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue782", angle=angle, style=style)


@guarded
def keyboard(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an keyboard.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue2d8", angle=angle, style=style)


@guarded
def keyhole(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an keyhole.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uea78", angle=angle, style=style)


@guarded
def knife(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an knife.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue636", angle=angle, style=style)


@guarded
def ladder(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an ladder.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue9e4", angle=angle, style=style)


@guarded
def ladder_simple(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an ladder-simple.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uec26", angle=angle, style=style)


@guarded
def lamp(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an lamp.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue638", angle=angle, style=style)


@guarded
def lamp_pendant(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an lamp-pendant.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uee2e", angle=angle, style=style)


@guarded
def laptop(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an laptop.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue586", angle=angle, style=style)


@guarded
def lasso(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an lasso.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uedc6", angle=angle, style=style)


@guarded
def lastfm_logo(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an lastfm-logo.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue842", angle=angle, style=style)


@guarded
def layout(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an layout.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue6d6", angle=angle, style=style)


@guarded
def leaf(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an leaf.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue2da", angle=angle, style=style)


@guarded
def lectern(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an lectern.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue95a", angle=angle, style=style)


@guarded
def lego(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an lego.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue8c6", angle=angle, style=style)


@guarded
def lego_smiley(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an lego-smiley.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue8c7", angle=angle, style=style)


@guarded
def less_than(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an less-than.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uedac", angle=angle, style=style)


@guarded
def less_than_or_equal(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an less-than-or-equal.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ueda4", angle=angle, style=style)


@guarded
def letter_circle_h(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an letter-circle-h.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uebf8", angle=angle, style=style)


@guarded
def letter_circle_p(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an letter-circle-p.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uec08", angle=angle, style=style)


@guarded
def letter_circle_v(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an letter-circle-v.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uec14", angle=angle, style=style)


@guarded
def lifebuoy(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an lifebuoy.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue63a", angle=angle, style=style)


@guarded
def lightbulb(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an lightbulb.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue2dc", angle=angle, style=style)


@guarded
def lightbulb_filament(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an lightbulb-filament.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue63c", angle=angle, style=style)


@guarded
def lighthouse(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an lighthouse.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue9f6", angle=angle, style=style)


@guarded
def lightning(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an lightning.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue2de", angle=angle, style=style)


@guarded
def lightning_a(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an lightning-a.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uea84", angle=angle, style=style)


@guarded
def lightning_slash(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an lightning-slash.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue2e0", angle=angle, style=style)


@guarded
def line_segment(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an line-segment.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue6d2", angle=angle, style=style)


@guarded
def line_segments(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an line-segments.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue6d4", angle=angle, style=style)


@guarded
def line_vertical(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an line-vertical.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ued70", angle=angle, style=style)


@guarded
def link(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an link.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue2e2", angle=angle, style=style)


@guarded
def link_break(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an link-break.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue2e4", angle=angle, style=style)


@guarded
def link_simple(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an link-simple.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue2e6", angle=angle, style=style)


@guarded
def link_simple_break(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an link-simple-break.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue2e8", angle=angle, style=style)


@guarded
def link_simple_horizontal(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an link-simple-horizontal.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue2ea", angle=angle, style=style)


@guarded
def link_simple_horizontal_break(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an link-simple-horizontal-break.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue2ec", angle=angle, style=style)


@guarded
def linkedin_logo(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an linkedin-logo.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue2ee", angle=angle, style=style)


@guarded
def linktree_logo(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an linktree-logo.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uedee", angle=angle, style=style)


@guarded
def linux_logo(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an linux-logo.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ueb02", angle=angle, style=style)


@guarded
def list(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an list.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue2f0", angle=angle, style=style)


@guarded
def list_bullets(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an list-bullets.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue2f2", angle=angle, style=style)


@guarded
def list_checks(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an list-checks.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ueadc", angle=angle, style=style)


@guarded
def list_dashes(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an list-dashes.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue2f4", angle=angle, style=style)


@guarded
def list_heart(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an list-heart.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uebde", angle=angle, style=style)


@guarded
def list_magnifying_glass(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an list-magnifying-glass.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uebe0", angle=angle, style=style)


@guarded
def list_numbers(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an list-numbers.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue2f6", angle=angle, style=style)


@guarded
def list_plus(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an list-plus.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue2f8", angle=angle, style=style)


@guarded
def list_star(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an list-star.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uebdc", angle=angle, style=style)


@guarded
def lock(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an lock.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue2fa", angle=angle, style=style)


@guarded
def lock_key(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an lock-key.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue2fe", angle=angle, style=style)


@guarded
def lock_key_open(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an lock-key-open.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue300", angle=angle, style=style)


@guarded
def lock_laminated(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an lock-laminated.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue302", angle=angle, style=style)


@guarded
def lock_laminated_open(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an lock-laminated-open.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue304", angle=angle, style=style)


@guarded
def lock_open(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an lock-open.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue306", angle=angle, style=style)


@guarded
def lock_simple(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an lock-simple.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue308", angle=angle, style=style)


@guarded
def lock_simple_open(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an lock-simple-open.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue30a", angle=angle, style=style)


@guarded
def lockers(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an lockers.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uecb8", angle=angle, style=style)


@guarded
def log(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an log.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ued82", angle=angle, style=style)


@guarded
def magic_wand(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an magic-wand.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue6b6", angle=angle, style=style)


@guarded
def magnet(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an magnet.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue680", angle=angle, style=style)


@guarded
def magnet_straight(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an magnet-straight.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue682", angle=angle, style=style)


@guarded
def magnifying_glass(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an magnifying-glass.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue30c", angle=angle, style=style)


@guarded
def magnifying_glass_minus(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an magnifying-glass-minus.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue30e", angle=angle, style=style)


@guarded
def magnifying_glass_plus(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an magnifying-glass-plus.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue310", angle=angle, style=style)


@guarded
def mailbox(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an mailbox.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uec1e", angle=angle, style=style)


@guarded
def map_pin(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an map-pin.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue316", angle=angle, style=style)


@guarded
def map_pin_area(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an map-pin-area.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uee3a", angle=angle, style=style)


@guarded
def map_pin_line(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an map-pin-line.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue318", angle=angle, style=style)


@guarded
def map_pin_plus(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an map-pin-plus.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue314", angle=angle, style=style)


@guarded
def map_pin_simple(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an map-pin-simple.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uee3e", angle=angle, style=style)


@guarded
def map_pin_simple_area(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an map-pin-simple-area.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uee3c", angle=angle, style=style)


@guarded
def map_pin_simple_line(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an map-pin-simple-line.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uee38", angle=angle, style=style)


@guarded
def map_trifold(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an map-trifold.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue31a", angle=angle, style=style)


@guarded
def markdown_logo(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an markdown-logo.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue508", angle=angle, style=style)


@guarded
def marker_circle(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an marker-circle.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue640", angle=angle, style=style)


@guarded
def martini(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an martini.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue31c", angle=angle, style=style)


@guarded
def mask_happy(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an mask-happy.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue9f4", angle=angle, style=style)


@guarded
def mask_sad(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an mask-sad.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ueb9e", angle=angle, style=style)


@guarded
def mastodon_logo(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an mastodon-logo.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ued68", angle=angle, style=style)


@guarded
def math_operations(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an math-operations.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue31e", angle=angle, style=style)


@guarded
def matrix_logo(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an matrix-logo.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ued64", angle=angle, style=style)


@guarded
def medal(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an medal.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue320", angle=angle, style=style)


@guarded
def medal_military(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an medal-military.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uecfc", angle=angle, style=style)


@guarded
def medium_logo(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an medium-logo.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue322", angle=angle, style=style)


@guarded
def megaphone(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an megaphone.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue324", angle=angle, style=style)


@guarded
def megaphone_simple(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an megaphone-simple.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue642", angle=angle, style=style)


@guarded
def member_of(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an member-of.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uedc2", angle=angle, style=style)


@guarded
def memory(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an memory.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue9c4", angle=angle, style=style)


@guarded
def messenger_logo(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an messenger-logo.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue6d8", angle=angle, style=style)


@guarded
def meta_logo(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an meta-logo.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ued02", angle=angle, style=style)


@guarded
def meteor(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an meteor.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue9ba", angle=angle, style=style)


@guarded
def metronome(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an metronome.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uec8e", angle=angle, style=style)


@guarded
def microphone(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an microphone.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue326", angle=angle, style=style)


@guarded
def microphone_slash(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an microphone-slash.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue328", angle=angle, style=style)


@guarded
def microphone_stage(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an microphone-stage.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue75c", angle=angle, style=style)


@guarded
def microscope(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an microscope.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uec7a", angle=angle, style=style)


@guarded
def microsoft_excel_logo(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an microsoft-excel-logo.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ueb6c", angle=angle, style=style)


@guarded
def microsoft_outlook_logo(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an microsoft-outlook-logo.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ueb70", angle=angle, style=style)


@guarded
def microsoft_powerpoint_logo(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an microsoft-powerpoint-logo.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ueace", angle=angle, style=style)


@guarded
def microsoft_teams_logo(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an microsoft-teams-logo.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ueb66", angle=angle, style=style)


@guarded
def microsoft_word_logo(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an microsoft-word-logo.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ueb6a", angle=angle, style=style)


@guarded
def minus(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an minus.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue32a", angle=angle, style=style)


@guarded
def minus_circle(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an minus-circle.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue32c", angle=angle, style=style)


@guarded
def minus_square(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an minus-square.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ued4c", angle=angle, style=style)


@guarded
def money(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an money.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue588", angle=angle, style=style)


@guarded
def money_wavy(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an money-wavy.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uee68", angle=angle, style=style)


@guarded
def monitor(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an monitor.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue32e", angle=angle, style=style)


@guarded
def monitor_arrow_up(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an monitor-arrow-up.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue58a", angle=angle, style=style)


@guarded
def monitor_play(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an monitor-play.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue58c", angle=angle, style=style)


@guarded
def moon(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an moon.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue330", angle=angle, style=style)


@guarded
def moon_stars(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an moon-stars.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue58e", angle=angle, style=style)


@guarded
def moped(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an moped.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue824", angle=angle, style=style)


@guarded
def moped_front(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an moped-front.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue822", angle=angle, style=style)


@guarded
def mosque(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an mosque.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uecee", angle=angle, style=style)


@guarded
def motorcycle(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an motorcycle.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue80a", angle=angle, style=style)


@guarded
def mountains(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an mountains.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue7ae", angle=angle, style=style)


@guarded
def mouse(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an mouse.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue33a", angle=angle, style=style)


@guarded
def mouse_left_click(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an mouse-left-click.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue334", angle=angle, style=style)


@guarded
def mouse_middle_click(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an mouse-middle-click.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue338", angle=angle, style=style)


@guarded
def mouse_right_click(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an mouse-right-click.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue336", angle=angle, style=style)


@guarded
def mouse_scroll(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an mouse-scroll.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue332", angle=angle, style=style)


@guarded
def mouse_simple(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an mouse-simple.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue644", angle=angle, style=style)


@guarded
def music_note(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an music-note.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue33c", angle=angle, style=style)


@guarded
def music_note_simple(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an music-note-simple.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue33e", angle=angle, style=style)


@guarded
def music_notes(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an music-notes.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue340", angle=angle, style=style)


@guarded
def music_notes_minus(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an music-notes-minus.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uee0c", angle=angle, style=style)


@guarded
def music_notes_plus(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an music-notes-plus.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ueb7c", angle=angle, style=style)


@guarded
def music_notes_simple(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an music-notes-simple.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue342", angle=angle, style=style)


@guarded
def navigation_arrow(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an navigation-arrow.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ueade", angle=angle, style=style)


@guarded
def needle(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an needle.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue82e", angle=angle, style=style)


@guarded
def network(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an network.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uedde", angle=angle, style=style)


@guarded
def network_slash(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an network-slash.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ueddc", angle=angle, style=style)


@guarded
def network_x(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an network-x.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uedda", angle=angle, style=style)


@guarded
def newspaper(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an newspaper.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue344", angle=angle, style=style)


@guarded
def newspaper_clipping(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an newspaper-clipping.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue346", angle=angle, style=style)


@guarded
def not_equals(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an not-equals.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ueda6", angle=angle, style=style)


@guarded
def not_member_of(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an not-member-of.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uedae", angle=angle, style=style)


@guarded
def not_subset_of(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an not-subset-of.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uedb0", angle=angle, style=style)


@guarded
def not_superset_of(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an not-superset-of.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uedb2", angle=angle, style=style)


@guarded
def notches(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an notches.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ued3a", angle=angle, style=style)


@guarded
def note(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an note.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue348", angle=angle, style=style)


@guarded
def note_blank(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an note-blank.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue34a", angle=angle, style=style)


@guarded
def note_pencil(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an note-pencil.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue34c", angle=angle, style=style)


@guarded
def notebook(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an notebook.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue34e", angle=angle, style=style)


@guarded
def notepad(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an notepad.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue63e", angle=angle, style=style)


@guarded
def notification(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an notification.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue6fa", angle=angle, style=style)


@guarded
def notion_logo(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an notion-logo.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue9a0", angle=angle, style=style)


@guarded
def nuclear_plant(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an nuclear-plant.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ued7c", angle=angle, style=style)


@guarded
def number_circle_eight(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an number-circle-eight.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue352", angle=angle, style=style)


@guarded
def number_circle_five(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an number-circle-five.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue358", angle=angle, style=style)


@guarded
def number_circle_four(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an number-circle-four.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue35e", angle=angle, style=style)


@guarded
def number_circle_nine(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an number-circle-nine.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue364", angle=angle, style=style)


@guarded
def number_circle_one(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an number-circle-one.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue36a", angle=angle, style=style)


@guarded
def number_circle_seven(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an number-circle-seven.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue370", angle=angle, style=style)


@guarded
def number_circle_six(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an number-circle-six.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue376", angle=angle, style=style)


@guarded
def number_circle_three(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an number-circle-three.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue37c", angle=angle, style=style)


@guarded
def number_circle_two(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an number-circle-two.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue382", angle=angle, style=style)


@guarded
def number_circle_zero(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an number-circle-zero.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue388", angle=angle, style=style)


@guarded
def number_eight(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an number-eight.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue350", angle=angle, style=style)


@guarded
def number_five(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an number-five.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue356", angle=angle, style=style)


@guarded
def number_four(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an number-four.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue35c", angle=angle, style=style)


@guarded
def number_nine(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an number-nine.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue362", angle=angle, style=style)


@guarded
def number_one(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an number-one.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue368", angle=angle, style=style)


@guarded
def number_seven(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an number-seven.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue36e", angle=angle, style=style)


@guarded
def number_six(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an number-six.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue374", angle=angle, style=style)


@guarded
def number_square_eight(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an number-square-eight.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue354", angle=angle, style=style)


@guarded
def number_square_five(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an number-square-five.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue35a", angle=angle, style=style)


@guarded
def number_square_four(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an number-square-four.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue360", angle=angle, style=style)


@guarded
def number_square_nine(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an number-square-nine.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue366", angle=angle, style=style)


@guarded
def number_square_one(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an number-square-one.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue36c", angle=angle, style=style)


@guarded
def number_square_seven(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an number-square-seven.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue372", angle=angle, style=style)


@guarded
def number_square_six(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an number-square-six.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue378", angle=angle, style=style)


@guarded
def number_square_three(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an number-square-three.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue37e", angle=angle, style=style)


@guarded
def number_square_two(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an number-square-two.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue384", angle=angle, style=style)


@guarded
def number_square_zero(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an number-square-zero.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue38a", angle=angle, style=style)


@guarded
def number_three(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an number-three.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue37a", angle=angle, style=style)


@guarded
def number_two(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an number-two.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue380", angle=angle, style=style)


@guarded
def number_zero(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an number-zero.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue386", angle=angle, style=style)


@guarded
def numpad(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an numpad.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue3c8", angle=angle, style=style)


@guarded
def nut(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an nut.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue38c", angle=angle, style=style)


@guarded
def ny_times_logo(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an ny-times-logo.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue646", angle=angle, style=style)


@guarded
def octagon(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an octagon.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue38e", angle=angle, style=style)


@guarded
def office_chair(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an office-chair.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uea46", angle=angle, style=style)


@guarded
def onigiri(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an onigiri.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uee2c", angle=angle, style=style)


@guarded
def open_ai_logo(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an open-ai-logo.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue7d2", angle=angle, style=style)


@guarded
def option(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an option.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue8a8", angle=angle, style=style)


@guarded
def orange(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an orange.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uee40", angle=angle, style=style)


@guarded
def orange_slice(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an orange-slice.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ued36", angle=angle, style=style)


@guarded
def oven(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an oven.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ued8c", angle=angle, style=style)


@guarded
def package(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an package.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue390", angle=angle, style=style)


@guarded
def paint_brush(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an paint-brush.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue6f0", angle=angle, style=style)


@guarded
def paint_brush_broad(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an paint-brush-broad.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue590", angle=angle, style=style)


@guarded
def paint_brush_household(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an paint-brush-household.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue6f2", angle=angle, style=style)


@guarded
def paint_bucket(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an paint-bucket.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue392", angle=angle, style=style)


@guarded
def paint_roller(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an paint-roller.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue6f4", angle=angle, style=style)


@guarded
def palette(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an palette.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue6c8", angle=angle, style=style)


@guarded
def panorama(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an panorama.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ueaa2", angle=angle, style=style)


@guarded
def pants(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an pants.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uec88", angle=angle, style=style)


@guarded
def paper_plane(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an paper-plane.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue394", angle=angle, style=style)


@guarded
def paper_plane_right(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an paper-plane-right.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue396", angle=angle, style=style)


@guarded
def paper_plane_tilt(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an paper-plane-tilt.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue398", angle=angle, style=style)


@guarded
def paperclip(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an paperclip.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue39a", angle=angle, style=style)


@guarded
def paperclip_horizontal(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an paperclip-horizontal.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue592", angle=angle, style=style)


@guarded
def parachute(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an parachute.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uea7c", angle=angle, style=style)


@guarded
def paragraph(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an paragraph.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue960", angle=angle, style=style)


@guarded
def parallelogram(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an parallelogram.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uecc6", angle=angle, style=style)


@guarded
def park(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an park.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uecb2", angle=angle, style=style)


@guarded
def password(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an password.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue752", angle=angle, style=style)


@guarded
def path(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an path.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue39c", angle=angle, style=style)


@guarded
def patreon_logo(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an patreon-logo.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue98a", angle=angle, style=style)


@guarded
def pause(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an pause.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue39e", angle=angle, style=style)


@guarded
def pause_circle(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an pause-circle.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue3a0", angle=angle, style=style)


@guarded
def paw_print(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an paw-print.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue648", angle=angle, style=style)


@guarded
def paypal_logo(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an paypal-logo.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue98c", angle=angle, style=style)


@guarded
def peace(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an peace.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue3a2", angle=angle, style=style)


@guarded
def pen(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an pen.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue3aa", angle=angle, style=style)


@guarded
def pen_nib(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an pen-nib.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue3ac", angle=angle, style=style)


@guarded
def pen_nib_straight(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an pen-nib-straight.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue64a", angle=angle, style=style)


@guarded
def pencil(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an pencil.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue3ae", angle=angle, style=style)


@guarded
def pencil_circle(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an pencil-circle.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue3b0", angle=angle, style=style)


@guarded
def pencil_line(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an pencil-line.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue3b2", angle=angle, style=style)


@guarded
def pencil_ruler(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an pencil-ruler.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue906", angle=angle, style=style)


@guarded
def pencil_simple(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an pencil-simple.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue3b4", angle=angle, style=style)


@guarded
def pencil_simple_line(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an pencil-simple-line.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uebc6", angle=angle, style=style)


@guarded
def pencil_simple_slash(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an pencil-simple-slash.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uecf6", angle=angle, style=style)


@guarded
def pencil_slash(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an pencil-slash.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uecf8", angle=angle, style=style)


@guarded
def pentagon(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an pentagon.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uec7e", angle=angle, style=style)


@guarded
def pentagram(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an pentagram.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uec5c", angle=angle, style=style)


@guarded
def pepper(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an pepper.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue94a", angle=angle, style=style)


@guarded
def percent(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an percent.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue3b6", angle=angle, style=style)


@guarded
def person(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an person.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue3a8", angle=angle, style=style)


@guarded
def person_arms_spread(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an person-arms-spread.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uecfe", angle=angle, style=style)


@guarded
def person_simple(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an person-simple.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue72e", angle=angle, style=style)


@guarded
def person_simple_bike(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an person-simple-bike.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue734", angle=angle, style=style)


@guarded
def person_simple_circle(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an person-simple-circle.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uee58", angle=angle, style=style)


@guarded
def person_simple_hike(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an person-simple-hike.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ued54", angle=angle, style=style)


@guarded
def person_simple_run(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an person-simple-run.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue730", angle=angle, style=style)


@guarded
def person_simple_ski(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an person-simple-ski.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue71c", angle=angle, style=style)


@guarded
def person_simple_snowboard(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an person-simple-snowboard.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue71e", angle=angle, style=style)


@guarded
def person_simple_swim(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an person-simple-swim.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue736", angle=angle, style=style)


@guarded
def person_simple_tai_chi(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an person-simple-tai-chi.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ued5c", angle=angle, style=style)


@guarded
def person_simple_throw(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an person-simple-throw.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue732", angle=angle, style=style)


@guarded
def person_simple_walk(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an person-simple-walk.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue73a", angle=angle, style=style)


@guarded
def perspective(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an perspective.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uebe6", angle=angle, style=style)


@guarded
def phone(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an phone.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue3b8", angle=angle, style=style)


@guarded
def phone_call(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an phone-call.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue3ba", angle=angle, style=style)


@guarded
def phone_disconnect(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an phone-disconnect.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue3bc", angle=angle, style=style)


@guarded
def phone_incoming(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an phone-incoming.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue3be", angle=angle, style=style)


@guarded
def phone_list(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an phone-list.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue3cc", angle=angle, style=style)


@guarded
def phone_outgoing(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an phone-outgoing.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue3c0", angle=angle, style=style)


@guarded
def phone_pause(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an phone-pause.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue3ca", angle=angle, style=style)


@guarded
def phone_plus(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an phone-plus.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uec56", angle=angle, style=style)


@guarded
def phone_slash(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an phone-slash.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue3c2", angle=angle, style=style)


@guarded
def phone_transfer(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an phone-transfer.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue3c6", angle=angle, style=style)


@guarded
def phone_x(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an phone-x.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue3c4", angle=angle, style=style)


@guarded
def phosphor_logo(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an phosphor-logo.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue3ce", angle=angle, style=style)


@guarded
def pi(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an pi.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uec80", angle=angle, style=style)


@guarded
def piano_keys(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an piano-keys.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue9c8", angle=angle, style=style)


@guarded
def picnic_table(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an picnic-table.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uee26", angle=angle, style=style)


@guarded
def picture_in_picture(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an picture-in-picture.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue64c", angle=angle, style=style)


@guarded
def piggy_bank(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an piggy-bank.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uea04", angle=angle, style=style)


@guarded
def pill(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an pill.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue700", angle=angle, style=style)


@guarded
def ping_pong(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an ping-pong.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uea42", angle=angle, style=style)


@guarded
def pint_glass(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an pint-glass.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uedd0", angle=angle, style=style)


@guarded
def pinterest_logo(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an pinterest-logo.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue64e", angle=angle, style=style)


@guarded
def pinwheel(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an pinwheel.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ueb9c", angle=angle, style=style)


@guarded
def pipe(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an pipe.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ued86", angle=angle, style=style)


@guarded
def pipe_wrench(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an pipe-wrench.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ued88", angle=angle, style=style)


@guarded
def pix_logo(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an pix-logo.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uecc2", angle=angle, style=style)


@guarded
def pizza(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an pizza.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue796", angle=angle, style=style)


@guarded
def placeholder(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an placeholder.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue650", angle=angle, style=style)


@guarded
def planet(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an planet.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue652", angle=angle, style=style)


@guarded
def plant(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an plant.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uebae", angle=angle, style=style)


@guarded
def play(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an play.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue3d0", angle=angle, style=style)


@guarded
def play_circle(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an play-circle.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue3d2", angle=angle, style=style)


@guarded
def play_pause(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an play-pause.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue8be", angle=angle, style=style)


@guarded
def playlist(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an playlist.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue6aa", angle=angle, style=style)


@guarded
def plug(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an plug.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue946", angle=angle, style=style)


@guarded
def plug_charging(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an plug-charging.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ueb5c", angle=angle, style=style)


@guarded
def plugs(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an plugs.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ueb56", angle=angle, style=style)


@guarded
def plugs_connected(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an plugs-connected.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ueb5a", angle=angle, style=style)


@guarded
def plus(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an plus.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue3d4", angle=angle, style=style)


@guarded
def plus_circle(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an plus-circle.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue3d6", angle=angle, style=style)


@guarded
def plus_minus(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an plus-minus.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue3d8", angle=angle, style=style)


@guarded
def plus_square(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an plus-square.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ued4a", angle=angle, style=style)


@guarded
def poker_chip(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an poker-chip.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue594", angle=angle, style=style)


@guarded
def police_car(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an police-car.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uec4a", angle=angle, style=style)


@guarded
def polygon(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an polygon.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue6d0", angle=angle, style=style)


@guarded
def popcorn(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an popcorn.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ueb4e", angle=angle, style=style)


@guarded
def popsicle(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an popsicle.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uebbe", angle=angle, style=style)


@guarded
def potted_plant(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an potted-plant.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uec22", angle=angle, style=style)


@guarded
def power(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an power.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue3da", angle=angle, style=style)


@guarded
def prescription(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an prescription.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue7a2", angle=angle, style=style)


@guarded
def presentation(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an presentation.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue654", angle=angle, style=style)


@guarded
def presentation_chart(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an presentation-chart.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue656", angle=angle, style=style)


@guarded
def printer(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an printer.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue3dc", angle=angle, style=style)


@guarded
def prohibit(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an prohibit.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue3de", angle=angle, style=style)


@guarded
def prohibit_inset(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an prohibit-inset.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue3e0", angle=angle, style=style)


@guarded
def projector_screen(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an projector-screen.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue658", angle=angle, style=style)


@guarded
def projector_screen_chart(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an projector-screen-chart.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue65a", angle=angle, style=style)


@guarded
def pulse(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an pulse.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue000", angle=angle, style=style)


@guarded
def activity(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an activity.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue000", angle=angle, style=style)


@guarded
def push_pin(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an push-pin.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue3e2", angle=angle, style=style)


@guarded
def push_pin_simple(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an push-pin-simple.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue65c", angle=angle, style=style)


@guarded
def push_pin_simple_slash(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an push-pin-simple-slash.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue65e", angle=angle, style=style)


@guarded
def push_pin_slash(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an push-pin-slash.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue3e4", angle=angle, style=style)


@guarded
def puzzle_piece(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an puzzle-piece.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue596", angle=angle, style=style)


@guarded
def qr_code(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an qr-code.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue3e6", angle=angle, style=style)


@guarded
def question(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an question.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue3e8", angle=angle, style=style)


@guarded
def question_mark(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an question-mark.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue3e9", angle=angle, style=style)


@guarded
def queue(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an queue.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue6ac", angle=angle, style=style)


@guarded
def quotes(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an quotes.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue660", angle=angle, style=style)


@guarded
def rabbit(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an rabbit.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ueac2", angle=angle, style=style)


@guarded
def racquet(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an racquet.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uee02", angle=angle, style=style)


@guarded
def radical(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an radical.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue3ea", angle=angle, style=style)


@guarded
def radio(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an radio.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue77e", angle=angle, style=style)


@guarded
def radio_button(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an radio-button.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ueb08", angle=angle, style=style)


@guarded
def radioactive(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an radioactive.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue9dc", angle=angle, style=style)


@guarded
def rainbow(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an rainbow.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue598", angle=angle, style=style)


@guarded
def rainbow_cloud(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an rainbow-cloud.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue59a", angle=angle, style=style)


@guarded
def ranking(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an ranking.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ued62", angle=angle, style=style)


@guarded
def read_cv_logo(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an read-cv-logo.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ued0c", angle=angle, style=style)


@guarded
def receipt(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an receipt.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue3ec", angle=angle, style=style)


@guarded
def receipt_x(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an receipt-x.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ued40", angle=angle, style=style)


@guarded
def record(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an record.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue3ee", angle=angle, style=style)


@guarded
def rectangle(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an rectangle.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue3f0", angle=angle, style=style)


@guarded
def rectangle_dashed(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an rectangle-dashed.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue3f2", angle=angle, style=style)


@guarded
def recycle(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an recycle.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue75a", angle=angle, style=style)


@guarded
def reddit_logo(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an reddit-logo.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue59c", angle=angle, style=style)


@guarded
def repeat(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an repeat.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue3f6", angle=angle, style=style)


@guarded
def repeat_once(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an repeat-once.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue3f8", angle=angle, style=style)


@guarded
def replit_logo(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an replit-logo.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ueb8a", angle=angle, style=style)


@guarded
def resize(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an resize.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ued6e", angle=angle, style=style)


@guarded
def rewind(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an rewind.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue6a8", angle=angle, style=style)


@guarded
def rewind_circle(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an rewind-circle.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue3fa", angle=angle, style=style)


@guarded
def road_horizon(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an road-horizon.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue838", angle=angle, style=style)


@guarded
def robot(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an robot.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue762", angle=angle, style=style)


@guarded
def rocket(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an rocket.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue3fc", angle=angle, style=style)


@guarded
def rocket_launch(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an rocket-launch.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue3fe", angle=angle, style=style)


@guarded
def rows(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an rows.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue5a2", angle=angle, style=style)


@guarded
def rows_plus_bottom(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an rows-plus-bottom.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue59e", angle=angle, style=style)


@guarded
def rows_plus_top(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an rows-plus-top.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue5a0", angle=angle, style=style)


@guarded
def rss(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an rss.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue400", angle=angle, style=style)


@guarded
def rss_simple(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an rss-simple.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue402", angle=angle, style=style)


@guarded
def rug(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an rug.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uea1a", angle=angle, style=style)


@guarded
def ruler(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an ruler.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue6b8", angle=angle, style=style)


@guarded
def sailboat(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an sailboat.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue78a", angle=angle, style=style)


@guarded
def scales(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an scales.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue750", angle=angle, style=style)


@guarded
def scan(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an scan.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uebb6", angle=angle, style=style)


@guarded
def scan_smiley(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an scan-smiley.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uebb4", angle=angle, style=style)


@guarded
def scissors(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an scissors.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ueae0", angle=angle, style=style)


@guarded
def scooter(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an scooter.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue820", angle=angle, style=style)


@guarded
def screencast(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an screencast.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue404", angle=angle, style=style)


@guarded
def screwdriver(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an screwdriver.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue86e", angle=angle, style=style)


@guarded
def scribble(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an scribble.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue806", angle=angle, style=style)


@guarded
def scribble_loop(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an scribble-loop.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue662", angle=angle, style=style)


@guarded
def scroll(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an scroll.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ueb7a", angle=angle, style=style)


@guarded
def seal(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an seal.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue604", angle=angle, style=style)


@guarded
def circle_wavy(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an circle-wavy.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue604", angle=angle, style=style)


@guarded
def seal_check(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an seal-check.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue606", angle=angle, style=style)


@guarded
def circle_wavy_check(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an circle-wavy-check.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue606", angle=angle, style=style)


@guarded
def seal_percent(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an seal-percent.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue60a", angle=angle, style=style)


@guarded
def seal_question(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an seal-question.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue608", angle=angle, style=style)


@guarded
def circle_wavy_question(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an circle-wavy-question.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue608", angle=angle, style=style)


@guarded
def seal_warning(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an seal-warning.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue60c", angle=angle, style=style)


@guarded
def circle_wavy_warning(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an circle-wavy-warning.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue60c", angle=angle, style=style)


@guarded
def seat(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an seat.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ueb8e", angle=angle, style=style)


@guarded
def seatbelt(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an seatbelt.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uedfe", angle=angle, style=style)


@guarded
def security_camera(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an security-camera.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ueca4", angle=angle, style=style)


@guarded
def selection(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an selection.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue69a", angle=angle, style=style)


@guarded
def selection_all(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an selection-all.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue746", angle=angle, style=style)


@guarded
def selection_background(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an selection-background.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ueaf8", angle=angle, style=style)


@guarded
def selection_foreground(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an selection-foreground.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ueaf6", angle=angle, style=style)


@guarded
def selection_inverse(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an selection-inverse.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue744", angle=angle, style=style)


@guarded
def selection_plus(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an selection-plus.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue69c", angle=angle, style=style)


@guarded
def selection_slash(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an selection-slash.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue69e", angle=angle, style=style)


@guarded
def shapes(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an shapes.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uec5e", angle=angle, style=style)


@guarded
def share(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an share.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue406", angle=angle, style=style)


@guarded
def share_fat(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an share-fat.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ued52", angle=angle, style=style)


@guarded
def share_network(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an share-network.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue408", angle=angle, style=style)


@guarded
def shield(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an shield.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue40a", angle=angle, style=style)


@guarded
def shield_check(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an shield-check.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue40c", angle=angle, style=style)


@guarded
def shield_checkered(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an shield-checkered.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue708", angle=angle, style=style)


@guarded
def shield_chevron(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an shield-chevron.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue40e", angle=angle, style=style)


@guarded
def shield_plus(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an shield-plus.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue706", angle=angle, style=style)


@guarded
def shield_slash(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an shield-slash.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue410", angle=angle, style=style)


@guarded
def shield_star(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an shield-star.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uec34", angle=angle, style=style)


@guarded
def shield_warning(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an shield-warning.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue412", angle=angle, style=style)


@guarded
def shipping_container(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an shipping-container.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue78c", angle=angle, style=style)


@guarded
def shirt_folded(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an shirt-folded.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uea92", angle=angle, style=style)


@guarded
def shooting_star(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an shooting-star.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uecfa", angle=angle, style=style)


@guarded
def shopping_bag(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an shopping-bag.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue416", angle=angle, style=style)


@guarded
def shopping_bag_open(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an shopping-bag-open.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue418", angle=angle, style=style)


@guarded
def shopping_cart(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an shopping-cart.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue41e", angle=angle, style=style)


@guarded
def shopping_cart_simple(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an shopping-cart-simple.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue420", angle=angle, style=style)


@guarded
def shovel(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an shovel.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue9e6", angle=angle, style=style)


@guarded
def shower(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an shower.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue776", angle=angle, style=style)


@guarded
def shrimp(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an shrimp.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ueab4", angle=angle, style=style)


@guarded
def shuffle(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an shuffle.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue422", angle=angle, style=style)


@guarded
def shuffle_angular(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an shuffle-angular.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue424", angle=angle, style=style)


@guarded
def shuffle_simple(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an shuffle-simple.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue426", angle=angle, style=style)


@guarded
def sidebar(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an sidebar.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ueab6", angle=angle, style=style)


@guarded
def sidebar_simple(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an sidebar-simple.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uec24", angle=angle, style=style)


@guarded
def sigma(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an sigma.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ueab8", angle=angle, style=style)


@guarded
def sign_in(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an sign-in.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue428", angle=angle, style=style)


@guarded
def sign_out(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an sign-out.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue42a", angle=angle, style=style)


@guarded
def signature(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an signature.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uebac", angle=angle, style=style)


@guarded
def signpost(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an signpost.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue89c", angle=angle, style=style)


@guarded
def sim_card(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an sim-card.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue664", angle=angle, style=style)


@guarded
def siren(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an siren.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue9b8", angle=angle, style=style)


@guarded
def sketch_logo(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an sketch-logo.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue42c", angle=angle, style=style)


@guarded
def skip_back(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an skip-back.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue5a4", angle=angle, style=style)


@guarded
def skip_back_circle(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an skip-back-circle.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue42e", angle=angle, style=style)


@guarded
def skip_forward(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an skip-forward.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue5a6", angle=angle, style=style)


@guarded
def skip_forward_circle(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an skip-forward-circle.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue430", angle=angle, style=style)


@guarded
def skull(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an skull.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue916", angle=angle, style=style)


@guarded
def skype_logo(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an skype-logo.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue8dc", angle=angle, style=style)


@guarded
def slack_logo(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an slack-logo.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue5a8", angle=angle, style=style)


@guarded
def sliders(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an sliders.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue432", angle=angle, style=style)


@guarded
def sliders_horizontal(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an sliders-horizontal.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue434", angle=angle, style=style)


@guarded
def slideshow(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an slideshow.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ued32", angle=angle, style=style)


@guarded
def smiley(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an smiley.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue436", angle=angle, style=style)


@guarded
def smiley_angry(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an smiley-angry.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uec62", angle=angle, style=style)


@guarded
def smiley_blank(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an smiley-blank.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue438", angle=angle, style=style)


@guarded
def smiley_meh(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an smiley-meh.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue43a", angle=angle, style=style)


@guarded
def smiley_melting(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an smiley-melting.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uee56", angle=angle, style=style)


@guarded
def smiley_nervous(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an smiley-nervous.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue43c", angle=angle, style=style)


@guarded
def smiley_sad(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an smiley-sad.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue43e", angle=angle, style=style)


@guarded
def smiley_sticker(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an smiley-sticker.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue440", angle=angle, style=style)


@guarded
def smiley_wink(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an smiley-wink.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue666", angle=angle, style=style)


@guarded
def smiley_x_eyes(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an smiley-x-eyes.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue442", angle=angle, style=style)


@guarded
def snapchat_logo(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an snapchat-logo.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue668", angle=angle, style=style)


@guarded
def sneaker(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an sneaker.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue80c", angle=angle, style=style)


@guarded
def sneaker_move(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an sneaker-move.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ued60", angle=angle, style=style)


@guarded
def snowflake(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an snowflake.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue5aa", angle=angle, style=style)


@guarded
def soccer_ball(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an soccer-ball.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue716", angle=angle, style=style)


@guarded
def sock(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an sock.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uecce", angle=angle, style=style)


@guarded
def solar_panel(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an solar-panel.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ued7a", angle=angle, style=style)


@guarded
def solar_roof(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an solar-roof.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ued7b", angle=angle, style=style)


@guarded
def sort_ascending(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an sort-ascending.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue444", angle=angle, style=style)


@guarded
def sort_descending(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an sort-descending.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue446", angle=angle, style=style)


@guarded
def soundcloud_logo(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an soundcloud-logo.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue8de", angle=angle, style=style)


@guarded
def spade(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an spade.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue448", angle=angle, style=style)


@guarded
def sparkle(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an sparkle.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue6a2", angle=angle, style=style)


@guarded
def speaker_hifi(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an speaker-hifi.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uea08", angle=angle, style=style)


@guarded
def speaker_high(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an speaker-high.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue44a", angle=angle, style=style)


@guarded
def speaker_low(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an speaker-low.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue44c", angle=angle, style=style)


@guarded
def speaker_none(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an speaker-none.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue44e", angle=angle, style=style)


@guarded
def speaker_simple_high(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an speaker-simple-high.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue450", angle=angle, style=style)


@guarded
def speaker_simple_low(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an speaker-simple-low.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue452", angle=angle, style=style)


@guarded
def speaker_simple_none(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an speaker-simple-none.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue454", angle=angle, style=style)


@guarded
def speaker_simple_slash(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an speaker-simple-slash.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue456", angle=angle, style=style)


@guarded
def speaker_simple_x(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an speaker-simple-x.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue458", angle=angle, style=style)


@guarded
def speaker_slash(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an speaker-slash.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue45a", angle=angle, style=style)


@guarded
def speaker_x(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an speaker-x.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue45c", angle=angle, style=style)


@guarded
def speedometer(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an speedometer.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uee74", angle=angle, style=style)


@guarded
def sphere(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an sphere.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uee66", angle=angle, style=style)


@guarded
def spinner(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an spinner.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue66a", angle=angle, style=style)


@guarded
def spinner_ball(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an spinner-ball.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uee28", angle=angle, style=style)


@guarded
def spinner_gap(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an spinner-gap.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue66c", angle=angle, style=style)


@guarded
def spiral(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an spiral.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue9fa", angle=angle, style=style)


@guarded
def split_horizontal(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an split-horizontal.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue872", angle=angle, style=style)


@guarded
def split_vertical(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an split-vertical.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue876", angle=angle, style=style)


@guarded
def spotify_logo(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an spotify-logo.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue66e", angle=angle, style=style)


@guarded
def spray_bottle(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an spray-bottle.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue7e4", angle=angle, style=style)


@guarded
def square(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an square.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue45e", angle=angle, style=style)


@guarded
def square_half(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an square-half.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue462", angle=angle, style=style)


@guarded
def square_half_bottom(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an square-half-bottom.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ueb16", angle=angle, style=style)


@guarded
def square_logo(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an square-logo.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue690", angle=angle, style=style)


@guarded
def square_split_horizontal(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an square-split-horizontal.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue870", angle=angle, style=style)


@guarded
def square_split_vertical(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an square-split-vertical.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue874", angle=angle, style=style)


@guarded
def squares_four(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an squares-four.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue464", angle=angle, style=style)


@guarded
def stack(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an stack.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue466", angle=angle, style=style)


@guarded
def stack_minus(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an stack-minus.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uedf4", angle=angle, style=style)


@guarded
def stack_overflow_logo(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an stack-overflow-logo.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ueb78", angle=angle, style=style)


@guarded
def stack_plus(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an stack-plus.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uedf6", angle=angle, style=style)


@guarded
def stack_simple(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an stack-simple.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue468", angle=angle, style=style)


@guarded
def stairs(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an stairs.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue8ec", angle=angle, style=style)


@guarded
def stamp(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an stamp.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uea48", angle=angle, style=style)


@guarded
def standard_definition(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an standard-definition.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uea90", angle=angle, style=style)


@guarded
def star(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an star.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue46a", angle=angle, style=style)


@guarded
def star_and_crescent(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an star-and-crescent.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uecf4", angle=angle, style=style)


@guarded
def star_four(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an star-four.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue6a4", angle=angle, style=style)


@guarded
def star_half(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an star-half.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue70a", angle=angle, style=style)


@guarded
def star_of_david(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an star-of-david.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue89e", angle=angle, style=style)


@guarded
def steam_logo(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an steam-logo.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uead4", angle=angle, style=style)


@guarded
def steering_wheel(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an steering-wheel.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue9ac", angle=angle, style=style)


@guarded
def steps(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an steps.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uecbe", angle=angle, style=style)


@guarded
def stethoscope(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an stethoscope.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue7ea", angle=angle, style=style)


@guarded
def sticker(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an sticker.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue5ac", angle=angle, style=style)


@guarded
def stool(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an stool.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uea44", angle=angle, style=style)


@guarded
def stop(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an stop.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue46c", angle=angle, style=style)


@guarded
def stop_circle(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an stop-circle.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue46e", angle=angle, style=style)


@guarded
def storefront(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an storefront.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue470", angle=angle, style=style)


@guarded
def strategy(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an strategy.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uea3a", angle=angle, style=style)


@guarded
def stripe_logo(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an stripe-logo.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue698", angle=angle, style=style)


@guarded
def student(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an student.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue73e", angle=angle, style=style)


@guarded
def subset_of(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an subset-of.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uedc0", angle=angle, style=style)


@guarded
def subset_proper_of(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an subset-proper-of.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uedb6", angle=angle, style=style)


@guarded
def subtitles(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an subtitles.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue1a8", angle=angle, style=style)


@guarded
def subtitles_slash(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an subtitles-slash.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue1a6", angle=angle, style=style)


@guarded
def subtract(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an subtract.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uebd6", angle=angle, style=style)


@guarded
def subtract_square(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an subtract-square.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uebd4", angle=angle, style=style)


@guarded
def subway(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an subway.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue498", angle=angle, style=style)


@guarded
def suitcase(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an suitcase.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue5ae", angle=angle, style=style)


@guarded
def suitcase_rolling(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an suitcase-rolling.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue9b0", angle=angle, style=style)


@guarded
def suitcase_simple(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an suitcase-simple.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue5b0", angle=angle, style=style)


@guarded
def sun(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an sun.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue472", angle=angle, style=style)


@guarded
def sun_dim(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an sun-dim.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue474", angle=angle, style=style)


@guarded
def sun_horizon(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an sun-horizon.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue5b6", angle=angle, style=style)


@guarded
def sunglasses(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an sunglasses.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue816", angle=angle, style=style)


@guarded
def superset_of(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an superset-of.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uedb8", angle=angle, style=style)


@guarded
def superset_proper_of(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an superset-proper-of.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uedb4", angle=angle, style=style)


@guarded
def swap(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an swap.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue83c", angle=angle, style=style)


@guarded
def swatches(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an swatches.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue5b8", angle=angle, style=style)


@guarded
def swimming_pool(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an swimming-pool.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uecb6", angle=angle, style=style)


@guarded
def sword(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an sword.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue5ba", angle=angle, style=style)


@guarded
def synagogue(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an synagogue.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uecec", angle=angle, style=style)


@guarded
def syringe(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an syringe.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue968", angle=angle, style=style)


@guarded
def t_shirt(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an t-shirt.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue670", angle=angle, style=style)


@guarded
def table(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an table.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue476", angle=angle, style=style)


@guarded
def tabs(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an tabs.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue778", angle=angle, style=style)


@guarded
def tag(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an tag.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue478", angle=angle, style=style)


@guarded
def tag_chevron(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an tag-chevron.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue672", angle=angle, style=style)


@guarded
def tag_simple(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an tag-simple.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue47a", angle=angle, style=style)


@guarded
def target(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an target.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue47c", angle=angle, style=style)


@guarded
def taxi(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an taxi.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue902", angle=angle, style=style)


@guarded
def tea_bag(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an tea-bag.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue8e6", angle=angle, style=style)


@guarded
def telegram_logo(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an telegram-logo.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue5bc", angle=angle, style=style)


@guarded
def television(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an television.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue754", angle=angle, style=style)


@guarded
def television_simple(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an television-simple.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ueae6", angle=angle, style=style)


@guarded
def tennis_ball(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an tennis-ball.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue720", angle=angle, style=style)


@guarded
def tent(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an tent.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue8ba", angle=angle, style=style)


@guarded
def terminal(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an terminal.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue47e", angle=angle, style=style)


@guarded
def terminal_window(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an terminal-window.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ueae8", angle=angle, style=style)


@guarded
def test_tube(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an test-tube.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue7a0", angle=angle, style=style)


@guarded
def text_a_underline(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an text-a-underline.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ued34", angle=angle, style=style)


@guarded
def text_aa(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an text-aa.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue6ee", angle=angle, style=style)


@guarded
def text_align_center(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an text-align-center.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue480", angle=angle, style=style)


@guarded
def text_align_justify(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an text-align-justify.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue482", angle=angle, style=style)


@guarded
def text_align_left(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an text-align-left.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue484", angle=angle, style=style)


@guarded
def text_align_right(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an text-align-right.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue486", angle=angle, style=style)


@guarded
def text_b(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an text-b.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue5be", angle=angle, style=style)


@guarded
def text_bolder(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an text-bolder.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue5be", angle=angle, style=style)


@guarded
def text_columns(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an text-columns.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uec96", angle=angle, style=style)


@guarded
def text_h(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an text-h.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue6ba", angle=angle, style=style)


@guarded
def text_h_five(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an text-h-five.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue6c4", angle=angle, style=style)


@guarded
def text_h_four(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an text-h-four.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue6c2", angle=angle, style=style)


@guarded
def text_h_one(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an text-h-one.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue6bc", angle=angle, style=style)


@guarded
def text_h_six(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an text-h-six.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue6c6", angle=angle, style=style)


@guarded
def text_h_three(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an text-h-three.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue6c0", angle=angle, style=style)


@guarded
def text_h_two(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an text-h-two.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue6be", angle=angle, style=style)


@guarded
def text_indent(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an text-indent.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uea1e", angle=angle, style=style)


@guarded
def text_italic(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an text-italic.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue5c0", angle=angle, style=style)


@guarded
def text_outdent(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an text-outdent.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uea1c", angle=angle, style=style)


@guarded
def text_strikethrough(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an text-strikethrough.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue5c2", angle=angle, style=style)


@guarded
def text_subscript(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an text-subscript.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uec98", angle=angle, style=style)


@guarded
def text_superscript(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an text-superscript.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uec9a", angle=angle, style=style)


@guarded
def text_t(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an text-t.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue48a", angle=angle, style=style)


@guarded
def text_t_slash(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an text-t-slash.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue488", angle=angle, style=style)


@guarded
def text_underline(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an text-underline.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue5c4", angle=angle, style=style)


@guarded
def textbox(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an textbox.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ueb0a", angle=angle, style=style)


@guarded
def thermometer(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an thermometer.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue5c6", angle=angle, style=style)


@guarded
def thermometer_cold(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an thermometer-cold.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue5c8", angle=angle, style=style)


@guarded
def thermometer_hot(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an thermometer-hot.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue5ca", angle=angle, style=style)


@guarded
def thermometer_simple(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an thermometer-simple.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue5cc", angle=angle, style=style)


@guarded
def threads_logo(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an threads-logo.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ued9e", angle=angle, style=style)


@guarded
def three_d(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an three-d.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uea5a", angle=angle, style=style)


@guarded
def thumbs_down(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an thumbs-down.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue48c", angle=angle, style=style)


@guarded
def thumbs_up(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an thumbs-up.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue48e", angle=angle, style=style)


@guarded
def ticket(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an ticket.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue490", angle=angle, style=style)


@guarded
def tidal_logo(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an tidal-logo.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ued1c", angle=angle, style=style)


@guarded
def tiktok_logo(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an tiktok-logo.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ueaf2", angle=angle, style=style)


@guarded
def tilde(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an tilde.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ueda8", angle=angle, style=style)


@guarded
def timer(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an timer.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue492", angle=angle, style=style)


@guarded
def tip_jar(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an tip-jar.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue7e2", angle=angle, style=style)


@guarded
def tipi(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an tipi.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ued30", angle=angle, style=style)


@guarded
def tire(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an tire.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uedd2", angle=angle, style=style)


@guarded
def toggle_left(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an toggle-left.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue674", angle=angle, style=style)


@guarded
def toggle_right(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an toggle-right.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue676", angle=angle, style=style)


@guarded
def toilet(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an toilet.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue79a", angle=angle, style=style)


@guarded
def toilet_paper(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an toilet-paper.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue79c", angle=angle, style=style)


@guarded
def toolbox(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an toolbox.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ueca0", angle=angle, style=style)


@guarded
def tooth(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an tooth.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue9cc", angle=angle, style=style)


@guarded
def tornado(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an tornado.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue88c", angle=angle, style=style)


@guarded
def tote(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an tote.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue494", angle=angle, style=style)


@guarded
def tote_simple(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an tote-simple.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue678", angle=angle, style=style)


@guarded
def towel(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an towel.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uede6", angle=angle, style=style)


@guarded
def tractor(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an tractor.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uec6e", angle=angle, style=style)


@guarded
def trademark(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an trademark.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue9f0", angle=angle, style=style)


@guarded
def trademark_registered(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an trademark-registered.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue3f4", angle=angle, style=style)


@guarded
def traffic_cone(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an traffic-cone.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue9a8", angle=angle, style=style)


@guarded
def traffic_sign(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an traffic-sign.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue67a", angle=angle, style=style)


@guarded
def traffic_signal(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an traffic-signal.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue9aa", angle=angle, style=style)


@guarded
def train(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an train.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue496", angle=angle, style=style)


@guarded
def train_regional(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an train-regional.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue49e", angle=angle, style=style)


@guarded
def train_simple(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an train-simple.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue4a0", angle=angle, style=style)


@guarded
def tram(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an tram.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue9ec", angle=angle, style=style)


@guarded
def translate(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an translate.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue4a2", angle=angle, style=style)


@guarded
def trash(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an trash.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue4a6", angle=angle, style=style)


@guarded
def trash_simple(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an trash-simple.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue4a8", angle=angle, style=style)


@guarded
def tray(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an tray.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue4aa", angle=angle, style=style)


@guarded
def tray_arrow_down(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an tray-arrow-down.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue010", angle=angle, style=style)


@guarded
def archive_tray(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an archive-tray.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue010", angle=angle, style=style)


@guarded
def tray_arrow_up(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an tray-arrow-up.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uee52", angle=angle, style=style)


@guarded
def treasure_chest(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an treasure-chest.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uede2", angle=angle, style=style)


@guarded
def tree(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an tree.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue6da", angle=angle, style=style)


@guarded
def tree_evergreen(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an tree-evergreen.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue6dc", angle=angle, style=style)


@guarded
def tree_palm(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an tree-palm.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue91a", angle=angle, style=style)


@guarded
def tree_structure(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an tree-structure.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue67c", angle=angle, style=style)


@guarded
def tree_view(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an tree-view.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uee48", angle=angle, style=style)


@guarded
def trend_down(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an trend-down.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue4ac", angle=angle, style=style)


@guarded
def trend_up(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an trend-up.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue4ae", angle=angle, style=style)


@guarded
def triangle(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an triangle.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue4b0", angle=angle, style=style)


@guarded
def triangle_dashed(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an triangle-dashed.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue4b2", angle=angle, style=style)


@guarded
def trolley(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an trolley.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue5b2", angle=angle, style=style)


@guarded
def trolley_suitcase(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an trolley-suitcase.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue5b4", angle=angle, style=style)


@guarded
def trophy(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an trophy.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue67e", angle=angle, style=style)


@guarded
def truck(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an truck.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue4b4", angle=angle, style=style)


@guarded
def truck_trailer(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an truck-trailer.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue4b6", angle=angle, style=style)


@guarded
def tumblr_logo(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an tumblr-logo.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue8d4", angle=angle, style=style)


@guarded
def twitch_logo(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an twitch-logo.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue5ce", angle=angle, style=style)


@guarded
def twitter_logo(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an twitter-logo.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue4ba", angle=angle, style=style)


@guarded
def umbrella(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an umbrella.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue684", angle=angle, style=style)


@guarded
def umbrella_simple(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an umbrella-simple.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue686", angle=angle, style=style)


@guarded
def union(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an union.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uedbe", angle=angle, style=style)


@guarded
def unite(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an unite.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue87e", angle=angle, style=style)


@guarded
def unite_square(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an unite-square.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue878", angle=angle, style=style)


@guarded
def upload(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an upload.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue4be", angle=angle, style=style)


@guarded
def upload_simple(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an upload-simple.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue4c0", angle=angle, style=style)


@guarded
def usb(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an usb.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue956", angle=angle, style=style)


@guarded
def user(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an user.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue4c2", angle=angle, style=style)


@guarded
def user_check(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an user-check.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ueafa", angle=angle, style=style)


@guarded
def user_circle(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an user-circle.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue4c4", angle=angle, style=style)


@guarded
def user_circle_check(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an user-circle-check.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uec38", angle=angle, style=style)


@guarded
def user_circle_dashed(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an user-circle-dashed.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uec36", angle=angle, style=style)


@guarded
def user_circle_gear(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an user-circle-gear.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue4c6", angle=angle, style=style)


@guarded
def user_circle_minus(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an user-circle-minus.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue4c8", angle=angle, style=style)


@guarded
def user_circle_plus(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an user-circle-plus.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue4ca", angle=angle, style=style)


@guarded
def user_focus(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an user-focus.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue6fc", angle=angle, style=style)


@guarded
def user_gear(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an user-gear.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue4cc", angle=angle, style=style)


@guarded
def user_list(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an user-list.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue73c", angle=angle, style=style)


@guarded
def user_minus(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an user-minus.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue4ce", angle=angle, style=style)


@guarded
def user_plus(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an user-plus.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue4d0", angle=angle, style=style)


@guarded
def user_rectangle(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an user-rectangle.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue4d2", angle=angle, style=style)


@guarded
def user_sound(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an user-sound.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ueca8", angle=angle, style=style)


@guarded
def user_square(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an user-square.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue4d4", angle=angle, style=style)


@guarded
def user_switch(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an user-switch.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue756", angle=angle, style=style)


@guarded
def users(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an users.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue4d6", angle=angle, style=style)


@guarded
def users_four(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an users-four.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue68c", angle=angle, style=style)


@guarded
def users_three(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an users-three.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue68e", angle=angle, style=style)


@guarded
def van(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an van.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue826", angle=angle, style=style)


@guarded
def vault(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an vault.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue76e", angle=angle, style=style)


@guarded
def vector_three(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an vector-three.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uee62", angle=angle, style=style)


@guarded
def vector_two(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an vector-two.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uee64", angle=angle, style=style)


@guarded
def vibrate(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an vibrate.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue4d8", angle=angle, style=style)


@guarded
def video(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an video.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue740", angle=angle, style=style)


@guarded
def video_camera(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an video-camera.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue4da", angle=angle, style=style)


@guarded
def video_camera_slash(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an video-camera-slash.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue4dc", angle=angle, style=style)


@guarded
def video_conference(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an video-conference.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uedce", angle=angle, style=style)


@guarded
def vignette(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an vignette.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ueba2", angle=angle, style=style)


@guarded
def vinyl_record(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an vinyl-record.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uecac", angle=angle, style=style)


@guarded
def virtual_reality(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an virtual-reality.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue7b8", angle=angle, style=style)


@guarded
def virus(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an virus.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue7d6", angle=angle, style=style)


@guarded
def visor(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an visor.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uee2a", angle=angle, style=style)


@guarded
def voicemail(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an voicemail.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue4de", angle=angle, style=style)


@guarded
def volleyball(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an volleyball.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue726", angle=angle, style=style)


@guarded
def wall(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an wall.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue688", angle=angle, style=style)


@guarded
def wallet(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an wallet.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue68a", angle=angle, style=style)


@guarded
def warehouse(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an warehouse.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uecd4", angle=angle, style=style)


@guarded
def warning(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an warning.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue4e0", angle=angle, style=style)


@guarded
def warning_circle(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an warning-circle.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue4e2", angle=angle, style=style)


@guarded
def warning_diamond(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an warning-diamond.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue7fc", angle=angle, style=style)


@guarded
def warning_octagon(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an warning-octagon.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue4e4", angle=angle, style=style)


@guarded
def washing_machine(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an washing-machine.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uede8", angle=angle, style=style)


@guarded
def watch(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an watch.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue4e6", angle=angle, style=style)


@guarded
def wave_sawtooth(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an wave-sawtooth.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uea9c", angle=angle, style=style)


@guarded
def wave_sine(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an wave-sine.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uea9a", angle=angle, style=style)


@guarded
def wave_square(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an wave-square.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uea9e", angle=angle, style=style)


@guarded
def wave_triangle(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an wave-triangle.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ueaa0", angle=angle, style=style)


@guarded
def waveform(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an waveform.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue802", angle=angle, style=style)


@guarded
def waveform_slash(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an waveform-slash.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue800", angle=angle, style=style)


@guarded
def waves(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an waves.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue6de", angle=angle, style=style)


@guarded
def webcam(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an webcam.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue9b2", angle=angle, style=style)


@guarded
def webcam_slash(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an webcam-slash.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uecdc", angle=angle, style=style)


@guarded
def webhooks_logo(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an webhooks-logo.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\uecae", angle=angle, style=style)


@guarded
def wechat_logo(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an wechat-logo.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue8d2", angle=angle, style=style)


@guarded
def whatsapp_logo(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an whatsapp-logo.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue5d0", angle=angle, style=style)


@guarded
def wheelchair(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an wheelchair.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue4e8", angle=angle, style=style)


@guarded
def wheelchair_motion(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an wheelchair-motion.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue89a", angle=angle, style=style)


@guarded
def wifi_high(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an wifi-high.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue4ea", angle=angle, style=style)


@guarded
def wifi_low(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an wifi-low.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue4ec", angle=angle, style=style)


@guarded
def wifi_medium(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an wifi-medium.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue4ee", angle=angle, style=style)


@guarded
def wifi_none(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an wifi-none.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue4f0", angle=angle, style=style)


@guarded
def wifi_slash(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an wifi-slash.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue4f2", angle=angle, style=style)


@guarded
def wifi_x(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an wifi-x.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue4f4", angle=angle, style=style)


@guarded
def wind(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an wind.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue5d2", angle=angle, style=style)


@guarded
def windmill(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an windmill.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue9f8", angle=angle, style=style)


@guarded
def windows_logo(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an windows-logo.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue692", angle=angle, style=style)


@guarded
def wine(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an wine.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue6b2", angle=angle, style=style)


@guarded
def wrench(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an wrench.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue5d4", angle=angle, style=style)


@guarded
def x(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an x.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue4f6", angle=angle, style=style)


@guarded
def x_circle(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an x-circle.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue4f8", angle=angle, style=style)


@guarded
def x_logo(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an x-logo.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue4bc", angle=angle, style=style)


@guarded
def x_square(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an x-square.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue4fa", angle=angle, style=style)


@guarded
def yarn(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an yarn.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ued9a", angle=angle, style=style)


@guarded
def yin_yang(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an yin-yang.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue92a", angle=angle, style=style)


@guarded
def youtube_logo(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: IconStyle | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an youtube-logo.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an IconStyle object, string, or None.

    """
    _write(xy=xy, width=width, code="\ue4fc", angle=angle, style=style)
