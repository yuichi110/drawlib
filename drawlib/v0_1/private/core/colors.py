# Copyright (c) 2024 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Color definition module."""

from typing import Final, Tuple


class ColorsBase:
    """Base class for color-related classes, providing common attributes."""

    Transparent: Final[Tuple[int, int, int, float]] = (0, 0, 0, 0.0)


class Colors(ColorsBase):
    """Class representing the 16 basic web colors along with a transparent color."""

    Aqua: Final[Tuple[int, int, int]] = (0, 255, 255)
    Black: Final[Tuple[int, int, int]] = (0, 0, 0)
    Blue: Final[Tuple[int, int, int]] = (0, 0, 255)
    Fuchsia: Final[Tuple[int, int, int]] = (255, 0, 255)
    Gray: Final[Tuple[int, int, int]] = (128, 128, 128)
    Green: Final[Tuple[int, int, int]] = (0, 128, 0)
    Lime: Final[Tuple[int, int, int]] = (0, 255, 0)
    Maroon: Final[Tuple[int, int, int]] = (128, 0, 0)
    Navy: Final[Tuple[int, int, int]] = (0, 0, 128)
    Olive: Final[Tuple[int, int, int]] = (128, 128, 0)
    Purple: Final[Tuple[int, int, int]] = (128, 0, 128)
    Red: Final[Tuple[int, int, int]] = (255, 0, 0)
    Silver: Final[Tuple[int, int, int]] = (192, 192, 192)
    Teal: Final[Tuple[int, int, int]] = (0, 128, 128)
    White: Final[Tuple[int, int, int]] = (255, 255, 255)
    Yellow: Final[Tuple[int, int, int]] = (255, 255, 0)


class Colors140(ColorsBase):
    """Class representing the 140 basic web colors(CSS Color Module Level3) along with a transparent color."""

    AliceBlue: Final[Tuple[int, int, int]] = (240, 248, 255)
    AntiqueWhite: Final[Tuple[int, int, int]] = (250, 235, 215)
    Aqua: Final[Tuple[int, int, int]] = (0, 255, 255)
    Aquamarine: Final[Tuple[int, int, int]] = (127, 255, 212)
    Azure: Final[Tuple[int, int, int]] = (240, 255, 255)
    Beige: Final[Tuple[int, int, int]] = (245, 245, 220)
    Bisque: Final[Tuple[int, int, int]] = (255, 228, 196)
    Black: Final[Tuple[int, int, int]] = (0, 0, 0)
    BlanchedAlmond: Final[Tuple[int, int, int]] = (255, 235, 205)
    Blue: Final[Tuple[int, int, int]] = (0, 0, 255)
    BlueViolet: Final[Tuple[int, int, int]] = (138, 43, 226)
    Brown: Final[Tuple[int, int, int]] = (165, 42, 42)
    BurlyWood: Final[Tuple[int, int, int]] = (222, 184, 135)
    CadetBlue: Final[Tuple[int, int, int]] = (95, 158, 160)
    Chartreuse: Final[Tuple[int, int, int]] = (127, 255, 0)
    Chocolate: Final[Tuple[int, int, int]] = (210, 105, 30)
    Coral: Final[Tuple[int, int, int]] = (255, 127, 80)
    CornflowerBlue: Final[Tuple[int, int, int]] = (100, 149, 237)
    Cornsilk: Final[Tuple[int, int, int]] = (255, 248, 220)
    Crimson: Final[Tuple[int, int, int]] = (220, 20, 60)
    Cyan: Final[Tuple[int, int, int]] = (0, 255, 255)
    DarkBlue: Final[Tuple[int, int, int]] = (0, 0, 139)
    DarkCyan: Final[Tuple[int, int, int]] = (0, 139, 139)
    DarkGoldenRod: Final[Tuple[int, int, int]] = (184, 134, 11)
    DarkGray: Final[Tuple[int, int, int]] = (169, 169, 169)
    DarkGreen: Final[Tuple[int, int, int]] = (0, 100, 0)
    DarkKhaki: Final[Tuple[int, int, int]] = (189, 183, 107)
    DarkMagenta: Final[Tuple[int, int, int]] = (139, 0, 139)
    DarkOliveGreen: Final[Tuple[int, int, int]] = (85, 107, 47)
    DarkOrange: Final[Tuple[int, int, int]] = (255, 140, 0)
    DarkOrchid: Final[Tuple[int, int, int]] = (153, 50, 204)
    DarkRed: Final[Tuple[int, int, int]] = (139, 0, 0)
    DarkSalmon: Final[Tuple[int, int, int]] = (233, 150, 122)
    DarkSeaGreen: Final[Tuple[int, int, int]] = (143, 188, 143)
    DarkSlateBlue: Final[Tuple[int, int, int]] = (72, 61, 139)
    DarkSlateGray: Final[Tuple[int, int, int]] = (47, 79, 79)
    DarkTurquoise: Final[Tuple[int, int, int]] = (0, 206, 209)
    DarkViolet: Final[Tuple[int, int, int]] = (148, 0, 211)
    DeepPink: Final[Tuple[int, int, int]] = (255, 20, 147)
    DeepSkyBlue: Final[Tuple[int, int, int]] = (0, 191, 255)
    DimGray: Final[Tuple[int, int, int]] = (105, 105, 105)
    DodgerBlue: Final[Tuple[int, int, int]] = (30, 144, 255)
    FireBrick: Final[Tuple[int, int, int]] = (178, 34, 34)
    FloralWhite: Final[Tuple[int, int, int]] = (255, 250, 240)
    ForestGreen: Final[Tuple[int, int, int]] = (34, 139, 34)
    Fuchsia: Final[Tuple[int, int, int]] = (255, 0, 255)
    Gainsboro: Final[Tuple[int, int, int]] = (220, 220, 220)
    GhostWhite: Final[Tuple[int, int, int]] = (248, 248, 255)
    Gold: Final[Tuple[int, int, int]] = (255, 215, 0)
    GoldenRod: Final[Tuple[int, int, int]] = (218, 165, 32)
    Gray: Final[Tuple[int, int, int]] = (128, 128, 128)
    Green: Final[Tuple[int, int, int]] = (0, 128, 0)
    GreenYellow: Final[Tuple[int, int, int]] = (173, 255, 47)
    HoneyDew: Final[Tuple[int, int, int]] = (240, 255, 240)
    HotPink: Final[Tuple[int, int, int]] = (255, 105, 180)
    IndianRed: Final[Tuple[int, int, int]] = (205, 92, 92)
    Indigo: Final[Tuple[int, int, int]] = (75, 0, 130)
    Ivory: Final[Tuple[int, int, int]] = (255, 255, 240)
    Khaki: Final[Tuple[int, int, int]] = (240, 230, 140)
    Lavender: Final[Tuple[int, int, int]] = (230, 230, 250)
    LavenderBlush: Final[Tuple[int, int, int]] = (255, 240, 245)
    LawnGreen: Final[Tuple[int, int, int]] = (124, 252, 0)
    LemonChiffon: Final[Tuple[int, int, int]] = (255, 250, 205)
    LightBlue: Final[Tuple[int, int, int]] = (173, 216, 230)
    LightCoral: Final[Tuple[int, int, int]] = (240, 128, 128)
    LightCyan: Final[Tuple[int, int, int]] = (224, 255, 255)
    LightGoldenRodYellow: Final[Tuple[int, int, int]] = (250, 250, 210)
    LightGray: Final[Tuple[int, int, int]] = (211, 211, 211)
    LightGreen: Final[Tuple[int, int, int]] = (144, 238, 144)
    LightPink: Final[Tuple[int, int, int]] = (255, 182, 193)
    LightSalmon: Final[Tuple[int, int, int]] = (255, 160, 122)
    LightSeaGreen: Final[Tuple[int, int, int]] = (32, 178, 170)
    LightSkyBlue: Final[Tuple[int, int, int]] = (135, 206, 250)
    LightSlateGray: Final[Tuple[int, int, int]] = (119, 136, 153)
    LightSteelBlue: Final[Tuple[int, int, int]] = (176, 196, 222)
    LightYellow: Final[Tuple[int, int, int]] = (255, 255, 224)
    Lime: Final[Tuple[int, int, int]] = (0, 255, 0)
    LimeGreen: Final[Tuple[int, int, int]] = (50, 205, 50)
    Linen: Final[Tuple[int, int, int]] = (250, 240, 230)
    Magenta: Final[Tuple[int, int, int]] = (255, 0, 255)
    Maroon: Final[Tuple[int, int, int]] = (128, 0, 0)
    MediumAquaMarine: Final[Tuple[int, int, int]] = (102, 205, 170)
    MediumBlue: Final[Tuple[int, int, int]] = (0, 0, 205)
    MediumOrchid: Final[Tuple[int, int, int]] = (186, 85, 211)
    MediumPurple: Final[Tuple[int, int, int]] = (147, 112, 219)
    MediumSeaGreen: Final[Tuple[int, int, int]] = (60, 179, 113)
    MediumSlateBlue: Final[Tuple[int, int, int]] = (123, 104, 238)
    MediumSpringGreen: Final[Tuple[int, int, int]] = (0, 250, 154)
    MediumTurquoise: Final[Tuple[int, int, int]] = (72, 209, 204)
    MediumVioletRed: Final[Tuple[int, int, int]] = (199, 21, 133)
    MidnightBlue: Final[Tuple[int, int, int]] = (25, 25, 112)
    MintCream: Final[Tuple[int, int, int]] = (245, 255, 250)
    MistyRose: Final[Tuple[int, int, int]] = (255, 228, 225)
    Moccasin: Final[Tuple[int, int, int]] = (255, 228, 181)
    NavajoWhite: Final[Tuple[int, int, int]] = (255, 222, 173)
    Navy: Final[Tuple[int, int, int]] = (0, 0, 128)
    OldLace: Final[Tuple[int, int, int]] = (253, 245, 230)
    Olive: Final[Tuple[int, int, int]] = (128, 128, 0)
    OliveDrab: Final[Tuple[int, int, int]] = (107, 142, 35)
    Orange: Final[Tuple[int, int, int]] = (255, 165, 0)
    OrangeRed: Final[Tuple[int, int, int]] = (255, 69, 0)
    Orchid: Final[Tuple[int, int, int]] = (218, 112, 214)
    PaleGoldenRod: Final[Tuple[int, int, int]] = (238, 232, 170)
    PaleGreen: Final[Tuple[int, int, int]] = (152, 251, 152)
    PaleTurquoise: Final[Tuple[int, int, int]] = (175, 238, 238)
    PaleVioletRed: Final[Tuple[int, int, int]] = (219, 112, 147)
    PapayaWhip: Final[Tuple[int, int, int]] = (255, 239, 213)
    PeachPuff: Final[Tuple[int, int, int]] = (255, 218, 185)
    Peru: Final[Tuple[int, int, int]] = (205, 133, 63)
    Pink: Final[Tuple[int, int, int]] = (255, 192, 203)
    Plum: Final[Tuple[int, int, int]] = (221, 160, 221)
    PowderBlue: Final[Tuple[int, int, int]] = (176, 224, 230)
    Purple: Final[Tuple[int, int, int]] = (128, 0, 128)
    RebeccaPurple: Final[Tuple[int, int, int]] = (102, 51, 153)
    Red: Final[Tuple[int, int, int]] = (255, 0, 0)
    RosyBrown: Final[Tuple[int, int, int]] = (188, 143, 143)
    RoyalBlue: Final[Tuple[int, int, int]] = (65, 105, 225)
    SaddleBrown: Final[Tuple[int, int, int]] = (139, 69, 19)
    Salmon: Final[Tuple[int, int, int]] = (250, 128, 114)
    SandyBrown: Final[Tuple[int, int, int]] = (244, 164, 96)
    SeaGreen: Final[Tuple[int, int, int]] = (46, 139, 87)
    SeaShell: Final[Tuple[int, int, int]] = (255, 245, 238)
    Sienna: Final[Tuple[int, int, int]] = (160, 82, 45)
    Silver: Final[Tuple[int, int, int]] = (192, 192, 192)
    SkyBlue: Final[Tuple[int, int, int]] = (135, 206, 235)
    SlateBlue: Final[Tuple[int, int, int]] = (106, 90, 205)
    SlateGray: Final[Tuple[int, int, int]] = (112, 128, 144)
    Snow: Final[Tuple[int, int, int]] = (255, 250, 250)
    SpringGreen: Final[Tuple[int, int, int]] = (0, 255, 127)
    SteelBlue: Final[Tuple[int, int, int]] = (70, 130, 180)
    Tan: Final[Tuple[int, int, int]] = (210, 180, 140)
    Teal: Final[Tuple[int, int, int]] = (0, 128, 128)
    Thistle: Final[Tuple[int, int, int]] = (216, 191, 216)
    Tomato: Final[Tuple[int, int, int]] = (255, 99, 71)
    Turquoise: Final[Tuple[int, int, int]] = (64, 224, 208)
    Violet: Final[Tuple[int, int, int]] = (238, 130, 238)
    Wheat: Final[Tuple[int, int, int]] = (245, 222, 179)
    White: Final[Tuple[int, int, int]] = (255, 255, 255)
    WhiteSmoke: Final[Tuple[int, int, int]] = (245, 245, 245)
    Yellow: Final[Tuple[int, int, int]] = (255, 255, 0)
    YellowGreen: Final[Tuple[int, int, int]] = (154, 205, 50)


class ColorsThemeEssentials(ColorsBase):
    """Class representing essential theme colors along with a transparent color."""

    Red: Final[Tuple[int, int, int]] = (255, 23, 23)
    LightRed: Final[Tuple[int, int, int]] = (239, 95, 95)
    Green: Final[Tuple[int, int, int]] = (15, 127, 15)
    LightGreen: Final[Tuple[int, int, int]] = (79, 191, 79)
    Blue: Final[Tuple[int, int, int]] = (31, 31, 255)
    LightBlue: Final[Tuple[int, int, int]] = (111, 111, 239)
    Yellow: Final[Tuple[int, int, int]] = (239, 239, 31)
    Purple: Final[Tuple[int, int, int]] = (127, 31, 127)
    Orange: Final[Tuple[int, int, int]] = (255, 95, 31)
    Navy: Final[Tuple[int, int, int]] = (15, 15, 127)
    Pink: Final[Tuple[int, int, int]] = (239, 63, 239)
    Charcoal: Final[Tuple[int, int, int]] = (39, 39, 39)
    Graphite: Final[Tuple[int, int, int]] = (63, 63, 63)
    Gray: Final[Tuple[int, int, int]] = (127, 127, 127)
    Silver: Final[Tuple[int, int, int]] = (191, 191, 191)
    Snow: Final[Tuple[int, int, int]] = (239, 239, 239)
    Teal: Final[Tuple[int, int, int]] = (15, 127, 127)
    Olive: Final[Tuple[int, int, int]] = (127, 127, 31)
    Brown: Final[Tuple[int, int, int]] = (159, 31, 31)
    Black: Final[Tuple[int, int, int]] = (0, 0, 0)
    White: Final[Tuple[int, int, int]] = (255, 255, 255)
    Aqua: Final[Tuple[int, int, int]] = (47, 239, 239)
    GreenYellow: Final[Tuple[int, int, int]] = (127, 207, 31)
    Ivory: Final[Tuple[int, int, int]] = (239, 239, 207)
    Steel: Final[Tuple[int, int, int]] = (96, 96, 143)


class ColorsThemeDefault(ColorsBase):
    """Class representing default theme colors along with a transparent color."""

    Red: Final[Tuple[int, int, int]] = ColorsThemeEssentials.LightRed
    Green: Final[Tuple[int, int, int]] = ColorsThemeEssentials.LightGreen
    Blue: Final[Tuple[int, int, int]] = ColorsThemeEssentials.LightBlue
    Black: Final[Tuple[int, int, int]] = ColorsThemeEssentials.Black
    White: Final[Tuple[int, int, int]] = ColorsThemeEssentials.White


class ColorsThemeMonochrome(ColorsBase):
    """Class representing monochrome theme colors along with a transparent color."""

    Black: Final[Tuple[int, int, int]] = ColorsThemeEssentials.Black
    Charcoal: Final[Tuple[int, int, int]] = ColorsThemeEssentials.Charcoal
    Graphite: Final[Tuple[int, int, int]] = ColorsThemeEssentials.Graphite
    Gray: Final[Tuple[int, int, int]] = ColorsThemeEssentials.Gray
    Silver: Final[Tuple[int, int, int]] = ColorsThemeEssentials.Silver
    Snow: Final[Tuple[int, int, int]] = ColorsThemeEssentials.Snow
    White: Final[Tuple[int, int, int]] = ColorsThemeEssentials.White
