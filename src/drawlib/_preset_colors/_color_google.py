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

from drawlib._core.l2_models import Color
from drawlib._core.l3_styles import ColorsBase


class GoogleStyleColors(ColorsBase):
    """Class representing colors for Google Sheets preset styles along with a transparent color."""

    # Greys / Neutrals
    Black: Final[Color] = Color(0, 0, 0)
    DarkGray4: Final[Color] = Color(67, 67, 67)
    DarkGray3: Final[Color] = Color(102, 102, 102)
    DarkGray2: Final[Color] = Color(153, 153, 153)
    DarkGray1: Final[Color] = Color(183, 183, 183)
    Gray: Final[Color] = Color(204, 204, 204)
    LightGray1: Final[Color] = Color(217, 217, 217)
    LightGray2: Final[Color] = Color(239, 239, 239)
    LightGray3: Final[Color] = Color(243, 243, 243)
    White: Final[Color] = Color(255, 255, 255)

    # Grey Aliases
    DarkGrey4: Final[Color] = DarkGray4
    DarkGrey3: Final[Color] = DarkGray3
    DarkGrey2: Final[Color] = DarkGray2
    DarkGrey1: Final[Color] = DarkGray1
    Grey: Final[Color] = Gray
    LightGrey1: Final[Color] = LightGray1
    LightGrey2: Final[Color] = LightGray2
    LightGrey3: Final[Color] = LightGray3
    LightGray: Final[Color] = LightGray1
    LightGrey: Final[Color] = LightGray1
    DarkGray: Final[Color] = DarkGray1
    DarkGrey: Final[Color] = DarkGray1

    # Red Berry
    RedBerry: Final[Color] = Color(152, 0, 0)
    LightRedBerry3: Final[Color] = Color(230, 184, 175)
    LightRedBerry2: Final[Color] = Color(221, 126, 107)
    LightRedBerry1: Final[Color] = Color(204, 65, 37)
    DarkRedBerry1: Final[Color] = Color(166, 28, 0)
    DarkRedBerry2: Final[Color] = Color(133, 32, 12)
    DarkRedBerry3: Final[Color] = Color(91, 15, 0)
    LightRedBerry: Final[Color] = LightRedBerry1
    DarkRedBerry: Final[Color] = DarkRedBerry1

    # Red
    Red: Final[Color] = Color(255, 0, 0)
    LightRed3: Final[Color] = Color(244, 204, 204)
    LightRed2: Final[Color] = Color(234, 153, 153)
    LightRed1: Final[Color] = Color(224, 102, 102)
    DarkRed1: Final[Color] = Color(204, 0, 0)
    DarkRed2: Final[Color] = Color(153, 0, 0)
    DarkRed3: Final[Color] = Color(102, 0, 0)
    LightRed: Final[Color] = LightRed1
    DarkRed: Final[Color] = DarkRed1

    # Orange
    Orange: Final[Color] = Color(255, 153, 0)
    LightOrange3: Final[Color] = Color(252, 229, 205)
    LightOrange2: Final[Color] = Color(249, 203, 156)
    LightOrange1: Final[Color] = Color(246, 178, 107)
    DarkOrange1: Final[Color] = Color(230, 145, 56)
    DarkOrange2: Final[Color] = Color(180, 95, 6)
    DarkOrange3: Final[Color] = Color(120, 63, 4)
    LightOrange: Final[Color] = LightOrange1
    DarkOrange: Final[Color] = DarkOrange1

    # Yellow
    Yellow: Final[Color] = Color(255, 255, 0)
    LightYellow3: Final[Color] = Color(255, 242, 204)
    LightYellow2: Final[Color] = Color(255, 229, 153)
    LightYellow1: Final[Color] = Color(255, 217, 102)
    DarkYellow1: Final[Color] = Color(241, 194, 50)
    DarkYellow2: Final[Color] = Color(191, 144, 0)
    DarkYellow3: Final[Color] = Color(127, 96, 0)
    LightYellow: Final[Color] = LightYellow1
    DarkYellow: Final[Color] = DarkYellow1

    # Green
    Green: Final[Color] = Color(0, 255, 0)
    LightGreen3: Final[Color] = Color(217, 234, 211)
    LightGreen2: Final[Color] = Color(182, 215, 168)
    LightGreen1: Final[Color] = Color(147, 196, 125)
    DarkGreen1: Final[Color] = Color(106, 168, 79)
    DarkGreen2: Final[Color] = Color(56, 118, 29)
    DarkGreen3: Final[Color] = Color(39, 78, 19)
    LightGreen: Final[Color] = LightGreen1
    DarkGreen: Final[Color] = DarkGreen1

    # Cyan
    Cyan: Final[Color] = Color(0, 255, 255)
    LightCyan3: Final[Color] = Color(208, 224, 227)
    LightCyan2: Final[Color] = Color(162, 196, 201)
    LightCyan1: Final[Color] = Color(118, 165, 175)
    DarkCyan1: Final[Color] = Color(69, 129, 142)
    DarkCyan2: Final[Color] = Color(19, 79, 92)
    DarkCyan3: Final[Color] = Color(12, 52, 61)
    LightCyan: Final[Color] = LightCyan1
    DarkCyan: Final[Color] = DarkCyan1

    # Cornflower Blue
    CornflowerBlue: Final[Color] = Color(74, 134, 232)
    LightCornflowerBlue3: Final[Color] = Color(201, 218, 248)
    LightCornflowerBlue2: Final[Color] = Color(164, 194, 244)
    LightCornflowerBlue1: Final[Color] = Color(109, 158, 235)
    DarkCornflowerBlue1: Final[Color] = Color(60, 120, 216)
    DarkCornflowerBlue2: Final[Color] = Color(17, 85, 204)
    DarkCornflowerBlue3: Final[Color] = Color(28, 69, 135)
    LightCornflowerBlue: Final[Color] = LightCornflowerBlue1
    DarkCornflowerBlue: Final[Color] = DarkCornflowerBlue1

    # Blue
    Blue: Final[Color] = Color(0, 0, 255)
    LightBlue3: Final[Color] = Color(207, 226, 243)
    LightBlue2: Final[Color] = Color(159, 197, 232)
    LightBlue1: Final[Color] = Color(111, 168, 220)
    DarkBlue1: Final[Color] = Color(61, 133, 198)
    DarkBlue2: Final[Color] = Color(11, 83, 148)
    DarkBlue3: Final[Color] = Color(7, 55, 99)
    LightBlue: Final[Color] = LightBlue1
    DarkBlue: Final[Color] = DarkBlue1

    # Purple
    Purple: Final[Color] = Color(153, 0, 255)
    LightPurple3: Final[Color] = Color(217, 210, 233)
    LightPurple2: Final[Color] = Color(180, 167, 214)
    LightPurple1: Final[Color] = Color(142, 124, 195)
    DarkPurple1: Final[Color] = Color(103, 78, 167)
    DarkPurple2: Final[Color] = Color(53, 28, 117)
    DarkPurple3: Final[Color] = Color(32, 18, 77)
    LightPurple: Final[Color] = LightPurple1
    DarkPurple: Final[Color] = DarkPurple1

    # Magenta
    Magenta: Final[Color] = Color(255, 0, 255)
    LightMagenta3: Final[Color] = Color(234, 209, 220)
    LightMagenta2: Final[Color] = Color(213, 166, 189)
    LightMagenta1: Final[Color] = Color(194, 123, 160)
    DarkMagenta1: Final[Color] = Color(166, 77, 121)
    DarkMagenta2: Final[Color] = Color(116, 27, 71)
    DarkMagenta3: Final[Color] = Color(76, 17, 48)
    LightMagenta: Final[Color] = LightMagenta1
    DarkMagenta: Final[Color] = DarkMagenta1


__all__ = [
    "GoogleStyleColors",
]
