# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Color definition module."""

from typing import Final

from drawlib.v0_2.private.types import StaticContainer, TypeColorRGB, TypeColorRGBA


class ColorsBase(StaticContainer):
    """Base class for color-related classes, providing common attributes."""

    Transparent: Final[TypeColorRGBA] = (0, 0, 0, 0.0)


class Colors(ColorsBase):
    """Class representing the 16 basic web colors along with a transparent color."""

    Aqua: Final[TypeColorRGB] = (0, 255, 255)
    Black: Final[TypeColorRGB] = (0, 0, 0)
    Blue: Final[TypeColorRGB] = (0, 0, 255)
    Fuchsia: Final[TypeColorRGB] = (255, 0, 255)
    Gray: Final[TypeColorRGB] = (128, 128, 128)
    Green: Final[TypeColorRGB] = (0, 128, 0)
    Lime: Final[TypeColorRGB] = (0, 255, 0)
    Maroon: Final[TypeColorRGB] = (128, 0, 0)
    Navy: Final[TypeColorRGB] = (0, 0, 128)
    Olive: Final[TypeColorRGB] = (128, 128, 0)
    Purple: Final[TypeColorRGB] = (128, 0, 128)
    Red: Final[TypeColorRGB] = (255, 0, 0)
    Silver: Final[TypeColorRGB] = (192, 192, 192)
    Teal: Final[TypeColorRGB] = (0, 128, 128)
    White: Final[TypeColorRGB] = (255, 255, 255)
    Yellow: Final[TypeColorRGB] = (255, 255, 0)


class Colors140(ColorsBase):
    """Class representing the 140 basic web colors(CSS Color Module Level3) along with a transparent color."""

    AliceBlue: Final[TypeColorRGB] = (240, 248, 255)
    AntiqueWhite: Final[TypeColorRGB] = (250, 235, 215)
    Aqua: Final[TypeColorRGB] = (0, 255, 255)
    Aquamarine: Final[TypeColorRGB] = (127, 255, 212)
    Azure: Final[TypeColorRGB] = (240, 255, 255)
    Beige: Final[TypeColorRGB] = (245, 245, 220)
    Bisque: Final[TypeColorRGB] = (255, 228, 196)
    Black: Final[TypeColorRGB] = (0, 0, 0)
    BlanchedAlmond: Final[TypeColorRGB] = (255, 235, 205)
    Blue: Final[TypeColorRGB] = (0, 0, 255)
    BlueViolet: Final[TypeColorRGB] = (138, 43, 226)
    Brown: Final[TypeColorRGB] = (165, 42, 42)
    BurlyWood: Final[TypeColorRGB] = (222, 184, 135)
    CadetBlue: Final[TypeColorRGB] = (95, 158, 160)
    Chartreuse: Final[TypeColorRGB] = (127, 255, 0)
    Chocolate: Final[TypeColorRGB] = (210, 105, 30)
    Coral: Final[TypeColorRGB] = (255, 127, 80)
    CornflowerBlue: Final[TypeColorRGB] = (100, 149, 237)
    Cornsilk: Final[TypeColorRGB] = (255, 248, 220)
    Crimson: Final[TypeColorRGB] = (220, 20, 60)
    Cyan: Final[TypeColorRGB] = (0, 255, 255)
    DarkBlue: Final[TypeColorRGB] = (0, 0, 139)
    DarkCyan: Final[TypeColorRGB] = (0, 139, 139)
    DarkGoldenRod: Final[TypeColorRGB] = (184, 134, 11)
    DarkGray: Final[TypeColorRGB] = (169, 169, 169)
    DarkGreen: Final[TypeColorRGB] = (0, 100, 0)
    DarkKhaki: Final[TypeColorRGB] = (189, 183, 107)
    DarkMagenta: Final[TypeColorRGB] = (139, 0, 139)
    DarkOliveGreen: Final[TypeColorRGB] = (85, 107, 47)
    DarkOrange: Final[TypeColorRGB] = (255, 140, 0)
    DarkOrchid: Final[TypeColorRGB] = (153, 50, 204)
    DarkRed: Final[TypeColorRGB] = (139, 0, 0)
    DarkSalmon: Final[TypeColorRGB] = (233, 150, 122)
    DarkSeaGreen: Final[TypeColorRGB] = (143, 188, 143)
    DarkSlateBlue: Final[TypeColorRGB] = (72, 61, 139)
    DarkSlateGray: Final[TypeColorRGB] = (47, 79, 79)
    DarkTurquoise: Final[TypeColorRGB] = (0, 206, 209)
    DarkViolet: Final[TypeColorRGB] = (148, 0, 211)
    DeepPink: Final[TypeColorRGB] = (255, 20, 147)
    DeepSkyBlue: Final[TypeColorRGB] = (0, 191, 255)
    DimGray: Final[TypeColorRGB] = (105, 105, 105)
    DodgerBlue: Final[TypeColorRGB] = (30, 144, 255)
    FireBrick: Final[TypeColorRGB] = (178, 34, 34)
    FloralWhite: Final[TypeColorRGB] = (255, 250, 240)
    ForestGreen: Final[TypeColorRGB] = (34, 139, 34)
    Fuchsia: Final[TypeColorRGB] = (255, 0, 255)
    Gainsboro: Final[TypeColorRGB] = (220, 220, 220)
    GhostWhite: Final[TypeColorRGB] = (248, 248, 255)
    Gold: Final[TypeColorRGB] = (255, 215, 0)
    GoldenRod: Final[TypeColorRGB] = (218, 165, 32)
    Gray: Final[TypeColorRGB] = (128, 128, 128)
    Green: Final[TypeColorRGB] = (0, 128, 0)
    GreenYellow: Final[TypeColorRGB] = (173, 255, 47)
    HoneyDew: Final[TypeColorRGB] = (240, 255, 240)
    HotPink: Final[TypeColorRGB] = (255, 105, 180)
    IndianRed: Final[TypeColorRGB] = (205, 92, 92)
    Indigo: Final[TypeColorRGB] = (75, 0, 130)
    Ivory: Final[TypeColorRGB] = (255, 255, 240)
    Khaki: Final[TypeColorRGB] = (240, 230, 140)
    Lavender: Final[TypeColorRGB] = (230, 230, 250)
    LavenderBlush: Final[TypeColorRGB] = (255, 240, 245)
    LawnGreen: Final[TypeColorRGB] = (124, 252, 0)
    LemonChiffon: Final[TypeColorRGB] = (255, 250, 205)
    LightBlue: Final[TypeColorRGB] = (173, 216, 230)
    LightCoral: Final[TypeColorRGB] = (240, 128, 128)
    LightCyan: Final[TypeColorRGB] = (224, 255, 255)
    LightGoldenRodYellow: Final[TypeColorRGB] = (250, 250, 210)
    LightGray: Final[TypeColorRGB] = (211, 211, 211)
    LightGreen: Final[TypeColorRGB] = (144, 238, 144)
    LightPink: Final[TypeColorRGB] = (255, 182, 193)
    LightSalmon: Final[TypeColorRGB] = (255, 160, 122)
    LightSeaGreen: Final[TypeColorRGB] = (32, 178, 170)
    LightSkyBlue: Final[TypeColorRGB] = (135, 206, 250)
    LightSlateGray: Final[TypeColorRGB] = (119, 136, 153)
    LightSteelBlue: Final[TypeColorRGB] = (176, 196, 222)
    LightYellow: Final[TypeColorRGB] = (255, 255, 224)
    Lime: Final[TypeColorRGB] = (0, 255, 0)
    LimeGreen: Final[TypeColorRGB] = (50, 205, 50)
    Linen: Final[TypeColorRGB] = (250, 240, 230)
    Magenta: Final[TypeColorRGB] = (255, 0, 255)
    Maroon: Final[TypeColorRGB] = (128, 0, 0)
    MediumAquaMarine: Final[TypeColorRGB] = (102, 205, 170)
    MediumBlue: Final[TypeColorRGB] = (0, 0, 205)
    MediumOrchid: Final[TypeColorRGB] = (186, 85, 211)
    MediumPurple: Final[TypeColorRGB] = (147, 112, 219)
    MediumSeaGreen: Final[TypeColorRGB] = (60, 179, 113)
    MediumSlateBlue: Final[TypeColorRGB] = (123, 104, 238)
    MediumSpringGreen: Final[TypeColorRGB] = (0, 250, 154)
    MediumTurquoise: Final[TypeColorRGB] = (72, 209, 204)
    MediumVioletRed: Final[TypeColorRGB] = (199, 21, 133)
    MidnightBlue: Final[TypeColorRGB] = (25, 25, 112)
    MintCream: Final[TypeColorRGB] = (245, 255, 250)
    MistyRose: Final[TypeColorRGB] = (255, 228, 225)
    Moccasin: Final[TypeColorRGB] = (255, 228, 181)
    NavajoWhite: Final[TypeColorRGB] = (255, 222, 173)
    Navy: Final[TypeColorRGB] = (0, 0, 128)
    OldLace: Final[TypeColorRGB] = (253, 245, 230)
    Olive: Final[TypeColorRGB] = (128, 128, 0)
    OliveDrab: Final[TypeColorRGB] = (107, 142, 35)
    Orange: Final[TypeColorRGB] = (255, 165, 0)
    OrangeRed: Final[TypeColorRGB] = (255, 69, 0)
    Orchid: Final[TypeColorRGB] = (218, 112, 214)
    PaleGoldenRod: Final[TypeColorRGB] = (238, 232, 170)
    PaleGreen: Final[TypeColorRGB] = (152, 251, 152)
    PaleTurquoise: Final[TypeColorRGB] = (175, 238, 238)
    PaleVioletRed: Final[TypeColorRGB] = (219, 112, 147)
    PapayaWhip: Final[TypeColorRGB] = (255, 239, 213)
    PeachPuff: Final[TypeColorRGB] = (255, 218, 185)
    Peru: Final[TypeColorRGB] = (205, 133, 63)
    Pink: Final[TypeColorRGB] = (255, 192, 203)
    Plum: Final[TypeColorRGB] = (221, 160, 221)
    PowderBlue: Final[TypeColorRGB] = (176, 224, 230)
    Purple: Final[TypeColorRGB] = (128, 0, 128)
    RebeccaPurple: Final[TypeColorRGB] = (102, 51, 153)
    Red: Final[TypeColorRGB] = (255, 0, 0)
    RosyBrown: Final[TypeColorRGB] = (188, 143, 143)
    RoyalBlue: Final[TypeColorRGB] = (65, 105, 225)
    SaddleBrown: Final[TypeColorRGB] = (139, 69, 19)
    Salmon: Final[TypeColorRGB] = (250, 128, 114)
    SandyBrown: Final[TypeColorRGB] = (244, 164, 96)
    SeaGreen: Final[TypeColorRGB] = (46, 139, 87)
    SeaShell: Final[TypeColorRGB] = (255, 245, 238)
    Sienna: Final[TypeColorRGB] = (160, 82, 45)
    Silver: Final[TypeColorRGB] = (192, 192, 192)
    SkyBlue: Final[TypeColorRGB] = (135, 206, 235)
    SlateBlue: Final[TypeColorRGB] = (106, 90, 205)
    SlateGray: Final[TypeColorRGB] = (112, 128, 144)
    Snow: Final[TypeColorRGB] = (255, 250, 250)
    SpringGreen: Final[TypeColorRGB] = (0, 255, 127)
    SteelBlue: Final[TypeColorRGB] = (70, 130, 180)
    Tan: Final[TypeColorRGB] = (210, 180, 140)
    Teal: Final[TypeColorRGB] = (0, 128, 128)
    Thistle: Final[TypeColorRGB] = (216, 191, 216)
    Tomato: Final[TypeColorRGB] = (255, 99, 71)
    Turquoise: Final[TypeColorRGB] = (64, 224, 208)
    Violet: Final[TypeColorRGB] = (238, 130, 238)
    Wheat: Final[TypeColorRGB] = (245, 222, 179)
    White: Final[TypeColorRGB] = (255, 255, 255)
    WhiteSmoke: Final[TypeColorRGB] = (245, 245, 245)
    Yellow: Final[TypeColorRGB] = (255, 255, 0)
    YellowGreen: Final[TypeColorRGB] = (154, 205, 50)


class ColorsThemeEssentials(ColorsBase):
    """Class representing essential theme colors along with a transparent color."""

    Red: Final[TypeColorRGB] = (255, 23, 23)
    LightRed: Final[TypeColorRGB] = (239, 95, 95)
    Green: Final[TypeColorRGB] = (15, 127, 15)
    LightGreen: Final[TypeColorRGB] = (79, 191, 79)
    Blue: Final[TypeColorRGB] = (31, 31, 255)
    LightBlue: Final[TypeColorRGB] = (111, 111, 239)
    Yellow: Final[TypeColorRGB] = (239, 239, 31)
    Purple: Final[TypeColorRGB] = (127, 31, 127)
    Orange: Final[TypeColorRGB] = (255, 95, 31)
    Navy: Final[TypeColorRGB] = (15, 15, 127)
    Pink: Final[TypeColorRGB] = (239, 63, 239)
    Charcoal: Final[TypeColorRGB] = (39, 39, 39)
    Graphite: Final[TypeColorRGB] = (63, 63, 63)
    Gray: Final[TypeColorRGB] = (127, 127, 127)
    Silver: Final[TypeColorRGB] = (191, 191, 191)
    Snow: Final[TypeColorRGB] = (239, 239, 239)
    Teal: Final[TypeColorRGB] = (15, 127, 127)
    Olive: Final[TypeColorRGB] = (127, 127, 31)
    Brown: Final[TypeColorRGB] = (159, 31, 31)
    Black: Final[TypeColorRGB] = (0, 0, 0)
    White: Final[TypeColorRGB] = (255, 255, 255)
    Aqua: Final[TypeColorRGB] = (47, 239, 239)
    GreenYellow: Final[TypeColorRGB] = (127, 207, 31)
    Ivory: Final[TypeColorRGB] = (239, 239, 207)
    Steel: Final[TypeColorRGB] = (96, 96, 143)


class ColorsThemeDefault(ColorsBase):
    """Class representing default theme colors along with a transparent color."""

    Red: Final[TypeColorRGB] = ColorsThemeEssentials.LightRed
    Green: Final[TypeColorRGB] = ColorsThemeEssentials.LightGreen
    Blue: Final[TypeColorRGB] = ColorsThemeEssentials.LightBlue
    Black: Final[TypeColorRGB] = ColorsThemeEssentials.Black
    White: Final[TypeColorRGB] = ColorsThemeEssentials.White


class ColorsThemeMonochrome(ColorsBase):
    """Class representing monochrome theme colors along with a transparent color."""

    Black: Final[TypeColorRGB] = ColorsThemeEssentials.Black
    Charcoal: Final[TypeColorRGB] = ColorsThemeEssentials.Charcoal
    Graphite: Final[TypeColorRGB] = ColorsThemeEssentials.Graphite
    Gray: Final[TypeColorRGB] = ColorsThemeEssentials.Gray
    Silver: Final[TypeColorRGB] = ColorsThemeEssentials.Silver
    Snow: Final[TypeColorRGB] = ColorsThemeEssentials.Snow
    White: Final[TypeColorRGB] = ColorsThemeEssentials.White
