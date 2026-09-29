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
from typing import Any, Self

from drawlib._core.l2_types import ColorType
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

    def patch(
        self,
        *,
        Canvas: ColorType | None = None,
        Primary: ColorType | None = None,
        Secondary: ColorType | None = None,
        Accent: ColorType | None = None,
        Muted: ColorType | None = None,
        Light: ColorType | None = None,
        Dark: ColorType | None = None,
        Danger: ColorType | None = None,
        Success: ColorType | None = None,
        # Neutrals
        White: ColorType | None = None,
        Gray1: ColorType | None = None,
        Gray2: ColorType | None = None,
        Gray3: ColorType | None = None,
        Gray4: ColorType | None = None,
        Gray5: ColorType | None = None,
        Gray6: ColorType | None = None,
        Gray7: ColorType | None = None,
        Gray8: ColorType | None = None,
        Black: ColorType | None = None,
        # Chromatic Tones
        CornflowerBlue1: ColorType | None = None,
        CornflowerBlue2: ColorType | None = None,
        CornflowerBlue3: ColorType | None = None,
        CornflowerBlue4: ColorType | None = None,
        CornflowerBlue5: ColorType | None = None,
        CornflowerBlue6: ColorType | None = None,
        Blue1: ColorType | None = None,
        Blue2: ColorType | None = None,
        Blue3: ColorType | None = None,
        Blue4: ColorType | None = None,
        Blue5: ColorType | None = None,
        Blue6: ColorType | None = None,
        Red1: ColorType | None = None,
        Red2: ColorType | None = None,
        Red3: ColorType | None = None,
        Red4: ColorType | None = None,
        Red5: ColorType | None = None,
        Red6: ColorType | None = None,
        RedBerry1: ColorType | None = None,
        RedBerry2: ColorType | None = None,
        RedBerry3: ColorType | None = None,
        RedBerry4: ColorType | None = None,
        RedBerry5: ColorType | None = None,
        RedBerry6: ColorType | None = None,
        Green1: ColorType | None = None,
        Green2: ColorType | None = None,
        Green3: ColorType | None = None,
        Green4: ColorType | None = None,
        Green5: ColorType | None = None,
        Green6: ColorType | None = None,
        Yellow1: ColorType | None = None,
        Yellow2: ColorType | None = None,
        Yellow3: ColorType | None = None,
        Yellow4: ColorType | None = None,
        Yellow5: ColorType | None = None,
        Yellow6: ColorType | None = None,
        Orange1: ColorType | None = None,
        Orange2: ColorType | None = None,
        Orange3: ColorType | None = None,
        Orange4: ColorType | None = None,
        Orange5: ColorType | None = None,
        Orange6: ColorType | None = None,
        Cyan1: ColorType | None = None,
        Cyan2: ColorType | None = None,
        Cyan3: ColorType | None = None,
        Cyan4: ColorType | None = None,
        Cyan5: ColorType | None = None,
        Cyan6: ColorType | None = None,
        Purple1: ColorType | None = None,
        Purple2: ColorType | None = None,
        Purple3: ColorType | None = None,
        Purple4: ColorType | None = None,
        Purple5: ColorType | None = None,
        Purple6: ColorType | None = None,
        Magenta1: ColorType | None = None,
        Magenta2: ColorType | None = None,
        Magenta3: ColorType | None = None,
        Magenta4: ColorType | None = None,
        Magenta5: ColorType | None = None,
        Magenta6: ColorType | None = None,
        # Base Primaries
        Red: ColorType | None = None,
        Green: ColorType | None = None,
        Blue: ColorType | None = None,
        Yellow: ColorType | None = None,
        Orange: ColorType | None = None,
        Cyan: ColorType | None = None,
        Purple: ColorType | None = None,
        Magenta: ColorType | None = None,
        RedBerry: ColorType | None = None,
        CornflowerBlue: ColorType | None = None,
        Pink: ColorType | None = None,
        Lime: ColorType | None = None,
        Teal: ColorType | None = None,
        Navy: ColorType | None = None,
        Olive: ColorType | None = None,
        Brown: ColorType | None = None,
        Gold: ColorType | None = None,
        Aqua: ColorType | None = None,
        GreenYellow: ColorType | None = None,
        Ivory: ColorType | None = None,
        Steel: ColorType | None = None,
        # Google Brand Colors
        GoogleBlue: ColorType | None = None,
        GoogleRed: ColorType | None = None,
        GoogleYellow: ColorType | None = None,
        GoogleGreen: ColorType | None = None,
        GoogleOrange: ColorType | None = None,
        **kwargs: Any,  # noqa: ANN401
    ) -> Self:
        """Create a new copy of preset colors with updated attributes.

        Args:
            Canvas: Canvas background color.
            Primary: Primary semantic color.
            Secondary: Secondary semantic color.
            Accent: Accent semantic color.
            Muted: Muted semantic color.
            Light: Light semantic color.
            Dark: Dark semantic color.
            Danger: Danger semantic color.
            Success: Success semantic color.
            White: White neutral color.
            Gray1: Neutral gray level 1.
            Gray2: Neutral gray level 2.
            Gray3: Neutral gray level 3.
            Gray4: Neutral gray level 4.
            Gray5: Neutral gray level 5.
            Gray6: Neutral gray level 6.
            Gray7: Neutral gray level 7.
            Gray8: Neutral gray level 8.
            Black: Black neutral color.
            CornflowerBlue1: Cornflower blue tone level 1.
            CornflowerBlue2: Cornflower blue tone level 2.
            CornflowerBlue3: Cornflower blue tone level 3.
            CornflowerBlue4: Cornflower blue tone level 4.
            CornflowerBlue5: Cornflower blue tone level 5.
            CornflowerBlue6: Cornflower blue tone level 6.
            Blue1: Blue tone level 1.
            Blue2: Blue tone level 2.
            Blue3: Blue tone level 3.
            Blue4: Blue tone level 4.
            Blue5: Blue tone level 5.
            Blue6: Blue tone level 6.
            Red1: Red tone level 1.
            Red2: Red tone level 2.
            Red3: Red tone level 3.
            Red4: Red tone level 4.
            Red5: Red tone level 5.
            Red6: Red tone level 6.
            RedBerry1: Red berry tone level 1.
            RedBerry2: Red berry tone level 2.
            RedBerry3: Red berry tone level 3.
            RedBerry4: Red berry tone level 4.
            RedBerry5: Red berry tone level 5.
            RedBerry6: Red berry tone level 6.
            Green1: Green tone level 1.
            Green2: Green tone level 2.
            Green3: Green tone level 3.
            Green4: Green tone level 4.
            Green5: Green tone level 5.
            Green6: Green tone level 6.
            Yellow1: Yellow tone level 1.
            Yellow2: Yellow tone level 2.
            Yellow3: Yellow tone level 3.
            Yellow4: Yellow tone level 4.
            Yellow5: Yellow tone level 5.
            Yellow6: Yellow tone level 6.
            Orange1: Orange tone level 1.
            Orange2: Orange tone level 2.
            Orange3: Orange tone level 3.
            Orange4: Orange tone level 4.
            Orange5: Orange tone level 5.
            Orange6: Orange tone level 6.
            Cyan1: Cyan tone level 1.
            Cyan2: Cyan tone level 2.
            Cyan3: Cyan tone level 3.
            Cyan4: Cyan tone level 4.
            Cyan5: Cyan tone level 5.
            Cyan6: Cyan tone level 6.
            Purple1: Purple tone level 1.
            Purple2: Purple tone level 2.
            Purple3: Purple tone level 3.
            Purple4: Purple tone level 4.
            Purple5: Purple tone level 5.
            Purple6: Purple tone level 6.
            Magenta1: Magenta tone level 1.
            Magenta2: Magenta tone level 2.
            Magenta3: Magenta tone level 3.
            Magenta4: Magenta tone level 4.
            Magenta5: Magenta tone level 5.
            Magenta6: Magenta tone level 6.
            Red: Base red primary color.
            Green: Base green primary color.
            Blue: Base blue primary color.
            Yellow: Base yellow primary color.
            Orange: Base orange primary color.
            Cyan: Base cyan primary color.
            Purple: Base purple primary color.
            Magenta: Base magenta primary color.
            RedBerry: Base red berry primary color.
            CornflowerBlue: Base cornflower blue primary color.
            Pink: Additional pink primary color.
            Lime: Additional lime primary color.
            Teal: Additional teal primary color.
            Navy: Additional navy primary color.
            Olive: Additional olive primary color.
            Brown: Additional brown primary color.
            Gold: Additional gold primary color.
            Aqua: Additional aqua primary color.
            GreenYellow: Additional green-yellow primary color.
            Ivory: Additional ivory primary color.
            Steel: Additional steel primary color.
            GoogleBlue: Google brand blue color.
            GoogleRed: Google brand red color.
            GoogleYellow: Google brand yellow color.
            GoogleGreen: Google brand green color.
            GoogleOrange: Google brand orange color.
            **kwargs: Additional color attributes to update.

        Returns:
            Self: New preset colors instance with updated attributes.
        """
        passed = {k: v for k, v in locals().items() if k not in {"self", "kwargs"} and v is not None}
        return super().patch(**passed, **kwargs)


__all__ = [
    "GoogleColors",
]
