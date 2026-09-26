# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Google Sheets style colors module."""

from __future__ import annotations

from typing import Final

from drawlib._core.l2_types import TypeColorRGB
from drawlib._core.l3_styles import ColorsBase


class GoogleStyleColors(ColorsBase):
    """Class representing colors for Google Sheets preset styles along with a transparent color."""

    # Greys / Neutrals
    Black: Final[TypeColorRGB] = (0, 0, 0)
    DarkGray4: Final[TypeColorRGB] = (67, 67, 67)
    DarkGray3: Final[TypeColorRGB] = (102, 102, 102)
    DarkGray2: Final[TypeColorRGB] = (153, 153, 153)
    DarkGray1: Final[TypeColorRGB] = (183, 183, 183)
    Gray: Final[TypeColorRGB] = (204, 204, 204)
    LightGray1: Final[TypeColorRGB] = (217, 217, 217)
    LightGray2: Final[TypeColorRGB] = (239, 239, 239)
    LightGray3: Final[TypeColorRGB] = (243, 243, 243)
    White: Final[TypeColorRGB] = (255, 255, 255)

    # Grey Aliases
    DarkGrey4: Final[TypeColorRGB] = DarkGray4
    DarkGrey3: Final[TypeColorRGB] = DarkGray3
    DarkGrey2: Final[TypeColorRGB] = DarkGray2
    DarkGrey1: Final[TypeColorRGB] = DarkGray1
    Grey: Final[TypeColorRGB] = Gray
    LightGrey1: Final[TypeColorRGB] = LightGray1
    LightGrey2: Final[TypeColorRGB] = LightGray2
    LightGrey3: Final[TypeColorRGB] = LightGray3
    LightGray: Final[TypeColorRGB] = LightGray1
    LightGrey: Final[TypeColorRGB] = LightGray1
    DarkGray: Final[TypeColorRGB] = DarkGray1
    DarkGrey: Final[TypeColorRGB] = DarkGray1

    # Red Berry
    RedBerry: Final[TypeColorRGB] = (152, 0, 0)
    LightRedBerry3: Final[TypeColorRGB] = (230, 184, 175)
    LightRedBerry2: Final[TypeColorRGB] = (221, 126, 107)
    LightRedBerry1: Final[TypeColorRGB] = (204, 65, 37)
    DarkRedBerry1: Final[TypeColorRGB] = (166, 28, 0)
    DarkRedBerry2: Final[TypeColorRGB] = (133, 32, 12)
    DarkRedBerry3: Final[TypeColorRGB] = (91, 15, 0)
    LightRedBerry: Final[TypeColorRGB] = LightRedBerry1
    DarkRedBerry: Final[TypeColorRGB] = DarkRedBerry1

    # Red
    Red: Final[TypeColorRGB] = (255, 0, 0)
    LightRed3: Final[TypeColorRGB] = (244, 204, 204)
    LightRed2: Final[TypeColorRGB] = (234, 153, 153)
    LightRed1: Final[TypeColorRGB] = (224, 102, 102)
    DarkRed1: Final[TypeColorRGB] = (204, 0, 0)
    DarkRed2: Final[TypeColorRGB] = (153, 0, 0)
    DarkRed3: Final[TypeColorRGB] = (102, 0, 0)
    LightRed: Final[TypeColorRGB] = LightRed1
    DarkRed: Final[TypeColorRGB] = DarkRed1

    # Orange
    Orange: Final[TypeColorRGB] = (255, 153, 0)
    LightOrange3: Final[TypeColorRGB] = (252, 229, 205)
    LightOrange2: Final[TypeColorRGB] = (249, 203, 156)
    LightOrange1: Final[TypeColorRGB] = (246, 178, 107)
    DarkOrange1: Final[TypeColorRGB] = (230, 145, 56)
    DarkOrange2: Final[TypeColorRGB] = (180, 95, 6)
    DarkOrange3: Final[TypeColorRGB] = (120, 63, 4)
    LightOrange: Final[TypeColorRGB] = LightOrange1
    DarkOrange: Final[TypeColorRGB] = DarkOrange1

    # Yellow
    Yellow: Final[TypeColorRGB] = (255, 255, 0)
    LightYellow3: Final[TypeColorRGB] = (255, 242, 204)
    LightYellow2: Final[TypeColorRGB] = (255, 229, 153)
    LightYellow1: Final[TypeColorRGB] = (255, 217, 102)
    DarkYellow1: Final[TypeColorRGB] = (241, 194, 50)
    DarkYellow2: Final[TypeColorRGB] = (191, 144, 0)
    DarkYellow3: Final[TypeColorRGB] = (127, 96, 0)
    LightYellow: Final[TypeColorRGB] = LightYellow1
    DarkYellow: Final[TypeColorRGB] = DarkYellow1

    # Green
    Green: Final[TypeColorRGB] = (0, 255, 0)
    LightGreen3: Final[TypeColorRGB] = (217, 234, 211)
    LightGreen2: Final[TypeColorRGB] = (182, 215, 168)
    LightGreen1: Final[TypeColorRGB] = (147, 196, 125)
    DarkGreen1: Final[TypeColorRGB] = (106, 168, 79)
    DarkGreen2: Final[TypeColorRGB] = (56, 118, 29)
    DarkGreen3: Final[TypeColorRGB] = (39, 78, 19)
    LightGreen: Final[TypeColorRGB] = LightGreen1
    DarkGreen: Final[TypeColorRGB] = DarkGreen1

    # Cyan
    Cyan: Final[TypeColorRGB] = (0, 255, 255)
    LightCyan3: Final[TypeColorRGB] = (208, 224, 227)
    LightCyan2: Final[TypeColorRGB] = (162, 196, 201)
    LightCyan1: Final[TypeColorRGB] = (118, 165, 175)
    DarkCyan1: Final[TypeColorRGB] = (69, 129, 142)
    DarkCyan2: Final[TypeColorRGB] = (19, 79, 92)
    DarkCyan3: Final[TypeColorRGB] = (12, 52, 61)
    LightCyan: Final[TypeColorRGB] = LightCyan1
    DarkCyan: Final[TypeColorRGB] = DarkCyan1

    # Cornflower Blue
    CornflowerBlue: Final[TypeColorRGB] = (74, 134, 232)
    LightCornflowerBlue3: Final[TypeColorRGB] = (201, 218, 248)
    LightCornflowerBlue2: Final[TypeColorRGB] = (164, 194, 244)
    LightCornflowerBlue1: Final[TypeColorRGB] = (109, 158, 235)
    DarkCornflowerBlue1: Final[TypeColorRGB] = (60, 120, 216)
    DarkCornflowerBlue2: Final[TypeColorRGB] = (17, 85, 204)
    DarkCornflowerBlue3: Final[TypeColorRGB] = (28, 69, 135)
    LightCornflowerBlue: Final[TypeColorRGB] = LightCornflowerBlue1
    DarkCornflowerBlue: Final[TypeColorRGB] = DarkCornflowerBlue1

    # Blue
    Blue: Final[TypeColorRGB] = (0, 0, 255)
    LightBlue3: Final[TypeColorRGB] = (207, 226, 243)
    LightBlue2: Final[TypeColorRGB] = (159, 197, 232)
    LightBlue1: Final[TypeColorRGB] = (111, 168, 220)
    DarkBlue1: Final[TypeColorRGB] = (61, 133, 198)
    DarkBlue2: Final[TypeColorRGB] = (11, 83, 148)
    DarkBlue3: Final[TypeColorRGB] = (7, 55, 99)
    LightBlue: Final[TypeColorRGB] = LightBlue1
    DarkBlue: Final[TypeColorRGB] = DarkBlue1

    # Purple
    Purple: Final[TypeColorRGB] = (153, 0, 255)
    LightPurple3: Final[TypeColorRGB] = (217, 210, 233)
    LightPurple2: Final[TypeColorRGB] = (180, 167, 214)
    LightPurple1: Final[TypeColorRGB] = (142, 124, 195)
    DarkPurple1: Final[TypeColorRGB] = (103, 78, 167)
    DarkPurple2: Final[TypeColorRGB] = (53, 28, 117)
    DarkPurple3: Final[TypeColorRGB] = (32, 18, 77)
    LightPurple: Final[TypeColorRGB] = LightPurple1
    DarkPurple: Final[TypeColorRGB] = DarkPurple1

    # Magenta
    Magenta: Final[TypeColorRGB] = (255, 0, 255)
    LightMagenta3: Final[TypeColorRGB] = (234, 209, 220)
    LightMagenta2: Final[TypeColorRGB] = (213, 166, 189)
    LightMagenta1: Final[TypeColorRGB] = (194, 123, 160)
    DarkMagenta1: Final[TypeColorRGB] = (166, 77, 121)
    DarkMagenta2: Final[TypeColorRGB] = (116, 27, 71)
    DarkMagenta3: Final[TypeColorRGB] = (76, 17, 48)
    LightMagenta: Final[TypeColorRGB] = LightMagenta1
    DarkMagenta: Final[TypeColorRGB] = DarkMagenta1


__all__ = [
    "GoogleStyleColors",
]
