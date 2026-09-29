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

import warnings

from drawlib._core.styles import BaseColors, Color

warnings.filterwarnings(
    "ignore",
    message=r'Field name ".*" in ".*" shadows an attribute in parent ".*"',
    category=UserWarning,
)


class GoogleColors(BaseColors):
    """Class representing colors for Google preset styles matching Google Workspace & Slides."""

    # =========================================================================
    # 1. Neutrals (Grayscale: White, Gray1-Gray8 from lightest to darkest, Black)
    # =========================================================================
    White: Color = Color(255, 255, 255)  # #FFFFFF
    Gray1: Color = Color(243, 243, 243)  # #F3F3F3 (Google Light Gray 3: 極淡背景・カード)
    Gray2: Color = Color(239, 239, 239)  # #EFEFEF (Google Light Gray 2: セクション背景)
    Gray3: Color = Color(217, 217, 217)  # #D9D9D9 (Google Light Gray 1: 境界線・枠)
    Gray4: Color = Color(204, 204, 204)  # #CCCCCC (Google Gray: 表罫線)
    Gray5: Color = Color(183, 183, 183)  # #B7B7B7 (Google Dark Gray 1: 非活性・セパレータ)
    Gray6: Color = Color(153, 153, 153)  # #999999 (Google Dark Gray 2: 副テキスト・薄アイコン)
    Gray7: Color = Color(102, 102, 102)  # #666666 (Google Dark Gray 3: サブタイトル・濃い枠)
    Gray8: Color = Color(67, 67, 67)    # #434343 (Google Dark Gray 4: 本文チャコールテキスト)
    Black: Color = Color(0, 0, 0)        # #000000

    # =========================================================================
    # 2. Main Chromatic Tones (10 Hues x 6 Levels: 1 is lightest, 6 is darkest)
    # =========================================================================
    # Cornflower Blue (Google Presentation Blue)
    CornflowerBlue1: Color = Color(201, 218, 248)  # #C9DAF8 (Light 3: 最淡パステル)
    CornflowerBlue2: Color = Color(164, 194, 244)  # #A4C2F4 (Light 2)
    CornflowerBlue3: Color = Color(109, 158, 235)  # #6D9EEB (Light 1: 標準面)
    CornflowerBlue4: Color = Color(60, 120, 216)   # #3C78D8 (Dark 1: 強調面・境界)
    CornflowerBlue5: Color = Color(17, 85, 204)    # #1155CC (Dark 2)
    CornflowerBlue6: Color = Color(28, 69, 135)    # #1C4587 (Dark 3: 最濃シェード)

    # Blue (Pure Blue base)
    Blue1: Color = Color(207, 226, 243)  # #CFE2F3
    Blue2: Color = Color(159, 197, 232)  # #9FC5E8
    Blue3: Color = Color(111, 168, 220)  # #6FA8DC
    Blue4: Color = Color(61, 133, 198)   # #3D85C6
    Blue5: Color = Color(11, 83, 148)    # #0B5394 (Google Theme Deep Blue)
    Blue6: Color = Color(7, 55, 99)      # #073763

    # Red
    Red1: Color = Color(244, 204, 204)   # #F4CCCC
    Red2: Color = Color(234, 153, 153)   # #EA9999
    Red3: Color = Color(224, 102, 102)   # #E06666
    Red4: Color = Color(204, 0, 0)       # #CC0000
    Red5: Color = Color(153, 0, 0)       # #990000
    Red6: Color = Color(102, 0, 0)       # #660000

    # Red Berry (Wine / Burgundy)
    RedBerry1: Color = Color(230, 184, 175)  # #E6B8AF
    RedBerry2: Color = Color(221, 126, 107)  # #DD7E6B
    RedBerry3: Color = Color(204, 65, 37)    # #CD4025
    RedBerry4: Color = Color(166, 28, 0)     # #A61D01
    RedBerry5: Color = Color(133, 32, 12)    # #85210D
    RedBerry6: Color = Color(91, 15, 0)      # #5B0F00

    # Green
    Green1: Color = Color(217, 234, 211)  # #D9EAD3
    Green2: Color = Color(182, 215, 168)  # #B6D7A8
    Green3: Color = Color(147, 196, 125)  # #93C47D
    Green4: Color = Color(106, 168, 79)   # #6AA84F
    Green5: Color = Color(56, 118, 29)    # #38761D
    Green6: Color = Color(39, 78, 19)     # #274E13

    # Yellow
    Yellow1: Color = Color(255, 242, 204)  # #FFF2CC
    Yellow2: Color = Color(255, 229, 153)  # #FFE599
    Yellow3: Color = Color(255, 217, 102)  # #FFD966
    Yellow4: Color = Color(241, 194, 50)   # #F1C232
    Yellow5: Color = Color(191, 144, 0)    # #BF9000
    Yellow6: Color = Color(127, 96, 0)     # #7F6000

    # Orange
    Orange1: Color = Color(252, 229, 205)  # #FCE5CD
    Orange2: Color = Color(249, 203, 156)  # #F9CB9C
    Orange3: Color = Color(246, 178, 107)  # #F6B26B
    Orange4: Color = Color(230, 145, 56)   # #E69138
    Orange5: Color = Color(180, 95, 6)     # #B45F06
    Orange6: Color = Color(120, 63, 4)     # #783F04

    # Cyan
    Cyan1: Color = Color(208, 224, 227)  # #D0E0E3
    Cyan2: Color = Color(162, 196, 201)  # #A2C4C9
    Cyan3: Color = Color(118, 165, 175)  # #76A5AF
    Cyan4: Color = Color(69, 129, 142)   # #45818E
    Cyan5: Color = Color(19, 79, 92)     # #134F5C
    Cyan6: Color = Color(12, 52, 61)     # #0C343D

    # Purple
    Purple1: Color = Color(217, 210, 233)  # #D9D2E9
    Purple2: Color = Color(180, 167, 214)  # #B4A7D6
    Purple3: Color = Color(142, 124, 195)  # #8E7CC3
    Purple4: Color = Color(103, 78, 167)   # #674EA7
    Purple5: Color = Color(53, 28, 117)    # #351C75
    Purple6: Color = Color(32, 18, 77)     # #20124D

    # Magenta
    Magenta1: Color = Color(234, 209, 220)  # #EAD1DC
    Magenta2: Color = Color(213, 166, 189)  # #D5A6BD
    Magenta3: Color = Color(194, 123, 160)  # #C27BA0
    Magenta4: Color = Color(166, 77, 121)   # #A64D79
    Magenta5: Color = Color(116, 27, 71)    # #741B47
    Magenta6: Color = Color(76, 17, 48)     # #4C1130

    # =========================================================================
    # 3. Base Primaries (Unnumbered pure hues from Row 1 + Defaults)
    # =========================================================================
    Red: Color = Color(255, 0, 0)
    Green: Color = Color(0, 255, 0)
    Blue: Color = Color(0, 0, 255)
    Yellow: Color = Color(255, 255, 0)
    Orange: Color = Color(255, 153, 0)
    Cyan: Color = Color(0, 255, 255)
    Purple: Color = Color(153, 0, 255)
    Magenta: Color = Color(255, 0, 255)
    RedBerry: Color = Color(152, 0, 0)
    CornflowerBlue: Color = Color(74, 134, 232)
    # Additional Primaries from DefaultColors
    Pink: Color = Color(255, 50, 150)
    Lime: Color = Color(100, 215, 0)
    Teal: Color = Color(15, 127, 127)
    Navy: Color = Color(15, 25, 110)
    Olive: Color = Color(127, 127, 31)
    Brown: Color = Color(145, 45, 25)
    Gold: Color = Color(218, 165, 32)
    Aqua: Color = Color(47, 239, 239)
    GreenYellow: Color = Color(127, 207, 31)
    Ivory: Color = Color(239, 239, 207)
    Steel: Color = Color(96, 96, 143)

    # =========================================================================
    # 4. Google Brand Colors (Theme header circles)
    # =========================================================================
    GoogleBlue: Color = Color(66, 133, 244)   # #4285F4 (Circle 1)
    GoogleRed: Color = Color(234, 67, 53)     # #EA4335 (Circle 7)
    GoogleYellow: Color = Color(251, 188, 4)  # #FBBC04 (Circle 10)
    GoogleGreen: Color = Color(52, 168, 83)   # #34A853 (Circle 6)
    GoogleOrange: Color = Color(255, 152, 0)  # #FF9800 (Circle 8)

    # =========================================================================
    # 5. Semantic Roles (8+1 roles)
    # =========================================================================
    Primary: Color = GoogleBlue        # #4285F4 (メイン処理・コアサービス)
    Secondary: Color = Blue5           # #0B5394 (データ層・ストレージ・キュー)
    Accent: Color = Orange4            # #E69138 (クライアント・入口・通知)
    Muted: Color = Gray3               # #D9D9D9 (VPC境界・グループコンテナ枠線)
    Light: Color = Gray1               # #F3F3F3 (白キャンバス上の淡色カード面)
    Dark: Color = Gray8                # #434343 (本文・タイトル文字・濃色枠線)
    Danger: Color = GoogleRed          # #EA4335 (エラー・停止状態)
    Success: Color = GoogleGreen       # #34A853 (正常・完了状態)
    Canvas: Color = White              # #FFFFFF (スライドキャンバス背景)


__all__ = [
    "GoogleColors",
]
