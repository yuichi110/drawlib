# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Google style colors module."""

from __future__ import annotations

from drawlib._core.l2_models import Color
from drawlib._core.l3_styles import BaseColors


class GoogleColors(BaseColors):
    """Class representing colors for Google Sheets preset styles along with a transparent color."""

    # Greys / Neutrals
    Black: Color = Color(0, 0, 0)
    DarkGray4: Color = Color(67, 67, 67)
    DarkGray3: Color = Color(102, 102, 102)
    DarkGray2: Color = Color(153, 153, 153)
    DarkGray1: Color = Color(183, 183, 183)
    Gray: Color = Color(204, 204, 204)
    LightGray1: Color = Color(217, 217, 217)
    LightGray2: Color = Color(239, 239, 239)
    LightGray3: Color = Color(243, 243, 243)
    White: Color = Color(255, 255, 255)

    # Grey Aliases
    DarkGrey4: Color = DarkGray4
    DarkGrey3: Color = DarkGray3
    DarkGrey2: Color = DarkGray2
    DarkGrey1: Color = DarkGray1
    Grey: Color = Gray
    LightGrey1: Color = LightGray1
    LightGrey2: Color = LightGray2
    LightGrey3: Color = LightGray3
    LightGray: Color = LightGray1
    LightGrey: Color = LightGray1
    DarkGray: Color = DarkGray1
    DarkGrey: Color = DarkGray1

    # Red Berry
    RedBerry: Color = Color(152, 0, 0)
    LightRedBerry3: Color = Color(230, 184, 175)
    LightRedBerry2: Color = Color(221, 126, 107)
    LightRedBerry1: Color = Color(204, 65, 37)
    DarkRedBerry1: Color = Color(166, 28, 0)
    DarkRedBerry2: Color = Color(133, 32, 12)
    DarkRedBerry3: Color = Color(91, 15, 0)
    LightRedBerry: Color = LightRedBerry1
    DarkRedBerry: Color = DarkRedBerry1

    # Red
    Red: Color = Color(255, 0, 0)
    LightRed3: Color = Color(244, 204, 204)
    LightRed2: Color = Color(234, 153, 153)
    LightRed1: Color = Color(224, 102, 102)
    DarkRed1: Color = Color(204, 0, 0)
    DarkRed2: Color = Color(153, 0, 0)
    DarkRed3: Color = Color(102, 0, 0)
    LightRed: Color = LightRed1
    DarkRed: Color = DarkRed1

    # Orange
    Orange: Color = Color(255, 153, 0)
    LightOrange3: Color = Color(252, 229, 205)
    LightOrange2: Color = Color(249, 203, 156)
    LightOrange1: Color = Color(246, 178, 107)
    DarkOrange1: Color = Color(230, 145, 56)
    DarkOrange2: Color = Color(180, 95, 6)
    DarkOrange3: Color = Color(120, 63, 4)
    LightOrange: Color = LightOrange1
    DarkOrange: Color = DarkOrange1

    # Yellow
    Yellow: Color = Color(255, 255, 0)
    LightYellow3: Color = Color(255, 242, 204)
    LightYellow2: Color = Color(255, 229, 153)
    LightYellow1: Color = Color(255, 217, 102)
    DarkYellow1: Color = Color(241, 194, 50)
    DarkYellow2: Color = Color(191, 144, 0)
    DarkYellow3: Color = Color(127, 96, 0)
    LightYellow: Color = LightYellow1
    DarkYellow: Color = DarkYellow1

    # Green
    Green: Color = Color(0, 255, 0)
    LightGreen3: Color = Color(217, 234, 211)
    LightGreen2: Color = Color(182, 215, 168)
    LightGreen1: Color = Color(147, 196, 125)
    DarkGreen1: Color = Color(106, 168, 79)
    DarkGreen2: Color = Color(56, 118, 29)
    DarkGreen3: Color = Color(39, 78, 19)
    LightGreen: Color = LightGreen1
    DarkGreen: Color = DarkGreen1

    # Cyan
    Cyan: Color = Color(0, 255, 255)
    LightCyan3: Color = Color(208, 224, 227)
    LightCyan2: Color = Color(162, 196, 201)
    LightCyan1: Color = Color(118, 165, 175)
    DarkCyan1: Color = Color(69, 129, 142)
    DarkCyan2: Color = Color(19, 79, 92)
    DarkCyan3: Color = Color(12, 52, 61)
    LightCyan: Color = LightCyan1
    DarkCyan: Color = DarkCyan1

    # Cornflower Blue
    CornflowerBlue: Color = Color(74, 134, 232)
    LightCornflowerBlue3: Color = Color(201, 218, 248)
    LightCornflowerBlue2: Color = Color(164, 194, 244)
    LightCornflowerBlue1: Color = Color(109, 158, 235)
    DarkCornflowerBlue1: Color = Color(60, 120, 216)
    DarkCornflowerBlue2: Color = Color(17, 85, 204)
    DarkCornflowerBlue3: Color = Color(28, 69, 135)
    LightCornflowerBlue: Color = LightCornflowerBlue1
    DarkCornflowerBlue: Color = DarkCornflowerBlue1

    # Blue
    Blue: Color = Color(0, 0, 255)
    LightBlue3: Color = Color(207, 226, 243)
    LightBlue2: Color = Color(159, 197, 232)
    LightBlue1: Color = Color(111, 168, 220)
    DarkBlue1: Color = Color(61, 133, 198)
    DarkBlue2: Color = Color(11, 83, 148)
    DarkBlue3: Color = Color(7, 55, 99)
    LightBlue: Color = LightBlue1
    DarkBlue: Color = DarkBlue1

    # Purple
    Purple: Color = Color(153, 0, 255)
    LightPurple3: Color = Color(217, 210, 233)
    LightPurple2: Color = Color(180, 167, 214)
    LightPurple1: Color = Color(142, 124, 195)
    DarkPurple1: Color = Color(103, 78, 167)
    DarkPurple2: Color = Color(53, 28, 117)
    DarkPurple3: Color = Color(32, 18, 77)
    LightPurple: Color = LightPurple1
    DarkPurple: Color = DarkPurple1

    # Magenta
    Magenta: Color = Color(255, 0, 255)
    LightMagenta3: Color = Color(234, 209, 220)
    LightMagenta2: Color = Color(213, 166, 189)
    LightMagenta1: Color = Color(194, 123, 160)
    DarkMagenta1: Color = Color(166, 77, 121)
    DarkMagenta2: Color = Color(116, 27, 71)
    DarkMagenta3: Color = Color(76, 17, 48)
    LightMagenta: Color = LightMagenta1
    DarkMagenta: Color = DarkMagenta1


google_colors: GoogleColors = GoogleColors()

__all__ = [
    "GoogleColors",
    "google_colors",
]
