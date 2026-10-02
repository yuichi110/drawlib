# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Monochrome preset styles module."""

from __future__ import annotations

from typing import Any, Self

from drawlib._core.l2_types import ColorType
from drawlib._core.l3_colors import BaseColors
from drawlib._core.l3_fonts import FontSourceCode
from drawlib._core.l3_styles import BaseStyles, Style
from drawlib._preset_colors import MonochromeColors
from drawlib._preset_styles._utils import _make_variants


class MonochromeStyles(BaseStyles):
    """Monochrome preset styles with complete typing for IDE autocompletion."""

    # Black
    Black: Style
    BlackBordered: Style
    BlackBold: Style
    BlackLight: Style
    BlackFlat: Style
    BlackOutline: Style
    BlackSolid: Style
    BlackOutlineBold: Style
    BlackSolidBold: Style
    BlackOutlineLight: Style
    BlackSolidLight: Style
    BlackDashed: Style
    BlackDashedBold: Style
    BlackDashedLight: Style

    # Gray1
    Gray1: Style
    Gray1Bordered: Style
    Gray1Bold: Style
    Gray1Light: Style
    Gray1Flat: Style
    Gray1Outline: Style
    Gray1Solid: Style
    Gray1OutlineBold: Style
    Gray1SolidBold: Style
    Gray1OutlineLight: Style
    Gray1SolidLight: Style
    Gray1Dashed: Style
    Gray1DashedBold: Style
    Gray1DashedLight: Style

    # Gray2
    Gray2: Style
    Gray2Bordered: Style
    Gray2Bold: Style
    Gray2Light: Style
    Gray2Flat: Style
    Gray2Outline: Style
    Gray2Solid: Style
    Gray2OutlineBold: Style
    Gray2SolidBold: Style
    Gray2OutlineLight: Style
    Gray2SolidLight: Style
    Gray2Dashed: Style
    Gray2DashedBold: Style
    Gray2DashedLight: Style

    # Gray3
    Gray3: Style
    Gray3Bordered: Style
    Gray3Bold: Style
    Gray3Light: Style
    Gray3Flat: Style
    Gray3Outline: Style
    Gray3Solid: Style
    Gray3OutlineBold: Style
    Gray3SolidBold: Style
    Gray3OutlineLight: Style
    Gray3SolidLight: Style
    Gray3Dashed: Style
    Gray3DashedBold: Style
    Gray3DashedLight: Style

    # Gray4
    Gray4: Style
    Gray4Bordered: Style
    Gray4Bold: Style
    Gray4Light: Style
    Gray4Flat: Style
    Gray4Outline: Style
    Gray4Solid: Style
    Gray4OutlineBold: Style
    Gray4SolidBold: Style
    Gray4OutlineLight: Style
    Gray4SolidLight: Style
    Gray4Dashed: Style
    Gray4DashedBold: Style
    Gray4DashedLight: Style

    # Gray5
    Gray5: Style
    Gray5Bordered: Style
    Gray5Bold: Style
    Gray5Light: Style
    Gray5Flat: Style
    Gray5Outline: Style
    Gray5Solid: Style
    Gray5OutlineBold: Style
    Gray5SolidBold: Style
    Gray5OutlineLight: Style
    Gray5SolidLight: Style
    Gray5Dashed: Style
    Gray5DashedBold: Style
    Gray5DashedLight: Style

    # Gray6
    Gray6: Style
    Gray6Bordered: Style
    Gray6Bold: Style
    Gray6Light: Style
    Gray6Flat: Style
    Gray6Outline: Style
    Gray6Solid: Style
    Gray6OutlineBold: Style
    Gray6SolidBold: Style
    Gray6OutlineLight: Style
    Gray6SolidLight: Style
    Gray6Dashed: Style
    Gray6DashedBold: Style
    Gray6DashedLight: Style

    # Gray7
    Gray7: Style
    Gray7Bordered: Style
    Gray7Bold: Style
    Gray7Light: Style
    Gray7Flat: Style
    Gray7Outline: Style
    Gray7Solid: Style
    Gray7OutlineBold: Style
    Gray7SolidBold: Style
    Gray7OutlineLight: Style
    Gray7SolidLight: Style
    Gray7Dashed: Style
    Gray7DashedBold: Style
    Gray7DashedLight: Style

    # Gray8
    Gray8: Style
    Gray8Bordered: Style
    Gray8Bold: Style
    Gray8Light: Style
    Gray8Flat: Style
    Gray8Outline: Style
    Gray8Solid: Style
    Gray8OutlineBold: Style
    Gray8SolidBold: Style
    Gray8OutlineLight: Style
    Gray8SolidLight: Style
    Gray8Dashed: Style
    Gray8DashedBold: Style
    Gray8DashedLight: Style

    # White
    White: Style
    WhiteBordered: Style
    WhiteBold: Style
    WhiteLight: Style
    WhiteFlat: Style
    WhiteOutline: Style
    WhiteSolid: Style
    WhiteOutlineBold: Style
    WhiteSolidBold: Style
    WhiteOutlineLight: Style
    WhiteSolidLight: Style
    WhiteDashed: Style
    WhiteDashedBold: Style
    WhiteDashedLight: Style

    # Semantic Roles
    Primary: Style
    PrimaryBordered: Style
    PrimaryBold: Style
    PrimaryLight: Style
    PrimaryFlat: Style
    PrimaryOutline: Style
    PrimarySolid: Style
    PrimaryOutlineBold: Style
    PrimarySolidBold: Style
    PrimaryOutlineLight: Style
    PrimarySolidLight: Style
    PrimaryDashed: Style
    PrimaryDashedBold: Style
    PrimaryDashedLight: Style

    Secondary: Style
    SecondaryBordered: Style
    SecondaryBold: Style
    SecondaryLight: Style
    SecondaryFlat: Style
    SecondaryOutline: Style
    SecondarySolid: Style
    SecondaryOutlineBold: Style
    SecondarySolidBold: Style
    SecondaryOutlineLight: Style
    SecondarySolidLight: Style
    SecondaryDashed: Style
    SecondaryDashedBold: Style
    SecondaryDashedLight: Style

    Accent: Style
    AccentBordered: Style
    AccentBold: Style
    AccentLight: Style
    AccentFlat: Style
    AccentOutline: Style
    AccentSolid: Style
    AccentOutlineBold: Style
    AccentSolidBold: Style
    AccentOutlineLight: Style
    AccentSolidLight: Style
    AccentDashed: Style
    AccentDashedBold: Style
    AccentDashedLight: Style

    Muted: Style
    MutedBordered: Style
    MutedBold: Style
    MutedLight: Style
    MutedFlat: Style
    MutedOutline: Style
    MutedSolid: Style
    MutedOutlineBold: Style
    MutedSolidBold: Style
    MutedOutlineLight: Style
    MutedSolidLight: Style
    MutedDashed: Style
    MutedDashedBold: Style
    MutedDashedLight: Style

    Light: Style
    LightBordered: Style
    LightBold: Style
    LightLight: Style
    LightFlat: Style
    LightOutline: Style
    LightSolid: Style
    LightOutlineBold: Style
    LightSolidBold: Style
    LightOutlineLight: Style
    LightSolidLight: Style
    LightDashed: Style
    LightDashedBold: Style
    LightDashedLight: Style

    Dark: Style
    DarkBordered: Style
    DarkBold: Style
    DarkLight: Style
    DarkFlat: Style
    DarkOutline: Style
    DarkSolid: Style
    DarkOutlineBold: Style
    DarkSolidBold: Style
    DarkOutlineLight: Style
    DarkSolidLight: Style
    DarkDashed: Style
    DarkDashedBold: Style
    DarkDashedLight: Style

    Canvas: Style
    CanvasFlat: Style

    def __init__(self, **kwargs: Any) -> None:  # noqa: ANN401
        """Initialize preset styles instance.

        If called without arguments (or with partial overrides), missing fields are
        automatically populated from the registered default singleton instance for this class.
        """
        super().__init__(**kwargs)

    def patch(
        self,
        *,
        Canvas: Style | None = None,
        CanvasFlat: Style | None = None,
        BackgroundColor: ColorType | None = None,
        Width: int | None = None,
        Height: int | None = None,
        Dpi: int | None = None,
        SourcecodeFont: FontSourceCode | None = None,
        Colors: BaseColors | None = None,
        Primary: Style | None = None,
        PrimaryBordered: Style | None = None,
        PrimaryBold: Style | None = None,
        PrimaryLight: Style | None = None,
        PrimaryFlat: Style | None = None,
        PrimaryOutline: Style | None = None,
        PrimaryOutlineBold: Style | None = None,
        PrimaryOutlineLight: Style | None = None,
        PrimaryDashed: Style | None = None,
        PrimaryDashedBold: Style | None = None,
        PrimaryDashedLight: Style | None = None,
        Secondary: Style | None = None,
        SecondaryBordered: Style | None = None,
        SecondaryBold: Style | None = None,
        SecondaryLight: Style | None = None,
        SecondaryFlat: Style | None = None,
        SecondaryOutline: Style | None = None,
        SecondaryOutlineBold: Style | None = None,
        SecondaryOutlineLight: Style | None = None,
        SecondaryDashed: Style | None = None,
        SecondaryDashedBold: Style | None = None,
        SecondaryDashedLight: Style | None = None,
        Accent: Style | None = None,
        AccentBordered: Style | None = None,
        AccentBold: Style | None = None,
        AccentLight: Style | None = None,
        AccentFlat: Style | None = None,
        AccentOutline: Style | None = None,
        AccentOutlineBold: Style | None = None,
        AccentOutlineLight: Style | None = None,
        AccentDashed: Style | None = None,
        AccentDashedBold: Style | None = None,
        AccentDashedLight: Style | None = None,
        Muted: Style | None = None,
        MutedBordered: Style | None = None,
        MutedBold: Style | None = None,
        MutedLight: Style | None = None,
        MutedFlat: Style | None = None,
        MutedOutline: Style | None = None,
        MutedOutlineBold: Style | None = None,
        MutedOutlineLight: Style | None = None,
        MutedDashed: Style | None = None,
        MutedDashedBold: Style | None = None,
        MutedDashedLight: Style | None = None,
        Light: Style | None = None,
        LightBordered: Style | None = None,
        LightBold: Style | None = None,
        LightLight: Style | None = None,
        LightFlat: Style | None = None,
        LightOutline: Style | None = None,
        LightOutlineBold: Style | None = None,
        LightOutlineLight: Style | None = None,
        LightDashed: Style | None = None,
        LightDashedBold: Style | None = None,
        LightDashedLight: Style | None = None,
        Dark: Style | None = None,
        DarkBordered: Style | None = None,
        DarkBold: Style | None = None,
        DarkLight: Style | None = None,
        DarkFlat: Style | None = None,
        DarkOutline: Style | None = None,
        DarkOutlineBold: Style | None = None,
        DarkOutlineLight: Style | None = None,
        DarkDashed: Style | None = None,
        DarkDashedBold: Style | None = None,
        DarkDashedLight: Style | None = None,
        Danger: Style | None = None,
        DangerBordered: Style | None = None,
        DangerBold: Style | None = None,
        DangerLight: Style | None = None,
        DangerFlat: Style | None = None,
        DangerOutline: Style | None = None,
        DangerOutlineBold: Style | None = None,
        DangerOutlineLight: Style | None = None,
        DangerDashed: Style | None = None,
        DangerDashedBold: Style | None = None,
        DangerDashedLight: Style | None = None,
        Success: Style | None = None,
        SuccessBordered: Style | None = None,
        SuccessBold: Style | None = None,
        SuccessLight: Style | None = None,
        SuccessFlat: Style | None = None,
        SuccessOutline: Style | None = None,
        SuccessOutlineBold: Style | None = None,
        SuccessOutlineLight: Style | None = None,
        SuccessDashed: Style | None = None,
        SuccessDashedBold: Style | None = None,
        SuccessDashedLight: Style | None = None,
        Black: Style | None = None,
        BlackBordered: Style | None = None,
        BlackBold: Style | None = None,
        BlackLight: Style | None = None,
        BlackFlat: Style | None = None,
        BlackOutline: Style | None = None,
        BlackSolid: Style | None = None,
        BlackOutlineBold: Style | None = None,
        BlackSolidBold: Style | None = None,
        BlackOutlineLight: Style | None = None,
        BlackSolidLight: Style | None = None,
        BlackDashed: Style | None = None,
        BlackDashedBold: Style | None = None,
        BlackDashedLight: Style | None = None,
        Gray1: Style | None = None,
        Gray1Bordered: Style | None = None,
        Gray1Bold: Style | None = None,
        Gray1Light: Style | None = None,
        Gray1Flat: Style | None = None,
        Gray1Outline: Style | None = None,
        Gray1Solid: Style | None = None,
        Gray1OutlineBold: Style | None = None,
        Gray1SolidBold: Style | None = None,
        Gray1OutlineLight: Style | None = None,
        Gray1SolidLight: Style | None = None,
        Gray1Dashed: Style | None = None,
        Gray1DashedBold: Style | None = None,
        Gray1DashedLight: Style | None = None,
        Gray2: Style | None = None,
        Gray2Bordered: Style | None = None,
        Gray2Bold: Style | None = None,
        Gray2Light: Style | None = None,
        Gray2Flat: Style | None = None,
        Gray2Outline: Style | None = None,
        Gray2Solid: Style | None = None,
        Gray2OutlineBold: Style | None = None,
        Gray2SolidBold: Style | None = None,
        Gray2OutlineLight: Style | None = None,
        Gray2SolidLight: Style | None = None,
        Gray2Dashed: Style | None = None,
        Gray2DashedBold: Style | None = None,
        Gray2DashedLight: Style | None = None,
        Gray3: Style | None = None,
        Gray3Bordered: Style | None = None,
        Gray3Bold: Style | None = None,
        Gray3Light: Style | None = None,
        Gray3Flat: Style | None = None,
        Gray3Outline: Style | None = None,
        Gray3Solid: Style | None = None,
        Gray3OutlineBold: Style | None = None,
        Gray3SolidBold: Style | None = None,
        Gray3OutlineLight: Style | None = None,
        Gray3SolidLight: Style | None = None,
        Gray3Dashed: Style | None = None,
        Gray3DashedBold: Style | None = None,
        Gray3DashedLight: Style | None = None,
        Gray4: Style | None = None,
        Gray4Bordered: Style | None = None,
        Gray4Bold: Style | None = None,
        Gray4Light: Style | None = None,
        Gray4Flat: Style | None = None,
        Gray4Outline: Style | None = None,
        Gray4Solid: Style | None = None,
        Gray4OutlineBold: Style | None = None,
        Gray4SolidBold: Style | None = None,
        Gray4OutlineLight: Style | None = None,
        Gray4SolidLight: Style | None = None,
        Gray4Dashed: Style | None = None,
        Gray4DashedBold: Style | None = None,
        Gray4DashedLight: Style | None = None,
        Gray5: Style | None = None,
        Gray5Bordered: Style | None = None,
        Gray5Bold: Style | None = None,
        Gray5Light: Style | None = None,
        Gray5Flat: Style | None = None,
        Gray5Outline: Style | None = None,
        Gray5Solid: Style | None = None,
        Gray5OutlineBold: Style | None = None,
        Gray5SolidBold: Style | None = None,
        Gray5OutlineLight: Style | None = None,
        Gray5SolidLight: Style | None = None,
        Gray5Dashed: Style | None = None,
        Gray5DashedBold: Style | None = None,
        Gray5DashedLight: Style | None = None,
        Gray6: Style | None = None,
        Gray6Bordered: Style | None = None,
        Gray6Bold: Style | None = None,
        Gray6Light: Style | None = None,
        Gray6Flat: Style | None = None,
        Gray6Outline: Style | None = None,
        Gray6Solid: Style | None = None,
        Gray6OutlineBold: Style | None = None,
        Gray6SolidBold: Style | None = None,
        Gray6OutlineLight: Style | None = None,
        Gray6SolidLight: Style | None = None,
        Gray6Dashed: Style | None = None,
        Gray6DashedBold: Style | None = None,
        Gray6DashedLight: Style | None = None,
        Gray7: Style | None = None,
        Gray7Bordered: Style | None = None,
        Gray7Bold: Style | None = None,
        Gray7Light: Style | None = None,
        Gray7Flat: Style | None = None,
        Gray7Outline: Style | None = None,
        Gray7Solid: Style | None = None,
        Gray7OutlineBold: Style | None = None,
        Gray7SolidBold: Style | None = None,
        Gray7OutlineLight: Style | None = None,
        Gray7SolidLight: Style | None = None,
        Gray7Dashed: Style | None = None,
        Gray7DashedBold: Style | None = None,
        Gray7DashedLight: Style | None = None,
        Gray8: Style | None = None,
        Gray8Bordered: Style | None = None,
        Gray8Bold: Style | None = None,
        Gray8Light: Style | None = None,
        Gray8Flat: Style | None = None,
        Gray8Outline: Style | None = None,
        Gray8Solid: Style | None = None,
        Gray8OutlineBold: Style | None = None,
        Gray8SolidBold: Style | None = None,
        Gray8OutlineLight: Style | None = None,
        Gray8SolidLight: Style | None = None,
        Gray8Dashed: Style | None = None,
        Gray8DashedBold: Style | None = None,
        Gray8DashedLight: Style | None = None,
        White: Style | None = None,
        WhiteBordered: Style | None = None,
        WhiteBold: Style | None = None,
        WhiteLight: Style | None = None,
        WhiteFlat: Style | None = None,
        WhiteOutline: Style | None = None,
        WhiteSolid: Style | None = None,
        WhiteOutlineBold: Style | None = None,
        WhiteSolidBold: Style | None = None,
        WhiteOutlineLight: Style | None = None,
        WhiteSolidLight: Style | None = None,
        WhiteDashed: Style | None = None,
        WhiteDashedBold: Style | None = None,
        WhiteDashedLight: Style | None = None,
        **kwargs: Any,  # noqa: ANN401
    ) -> Self:
        """Create a new copy of preset styles with updated attributes.

        Args:
            **kwargs: Additional style attributes to update.

        Returns:
            Self: New preset styles instance with updated attributes.
        """
        passed = {k: v for k, v in locals().items() if k not in {"self", "kwargs"} and v is not None}
        return super().patch(**passed, **kwargs)

    def __getattribute__(self, name: str) -> Any:  # noqa: ANN401
        """Intercept attribute access to raise AttributeError for unsupported semantic roles.

        Args:
            name (str): Attribute name being accessed.

        Returns:
            Any: Attribute value if defined.

        Raises:
            AttributeError: If accessing an unsupported danger or success style.
        """
        val = super().__getattribute__(name)
        if (name.startswith("Danger") or name.startswith("Success")) and val is None:
            raise AttributeError(f"{self.__class__.__name__} has no {name} style.")
        return val


def _create_monochrome_styles() -> MonochromeStyles:
    """Generate monochrome preset styles.

    Returns:
        MonochromeStyles: Monochrome preset styles instance.
    """
    black = MonochromeColors.Black
    gray1 = MonochromeColors.Gray1
    gray2 = MonochromeColors.Gray2
    gray3 = MonochromeColors.Gray3
    gray4 = MonochromeColors.Gray4
    gray5 = MonochromeColors.Gray5
    gray6 = MonochromeColors.Gray6
    gray7 = MonochromeColors.Gray7
    gray8 = MonochromeColors.Gray8
    white = MonochromeColors.White

    p_v = _make_variants(
        white,
        border_color=black,
        default_text_color=black,
        line_color=black,
    )
    p_v["flat"] = Style(
        supports={"shape", "icon"},
        shape_fill_color=black,
        shape_line_color=MonochromeColors.Transparent,
        shape_line_width=0.0,
        shape_line_style="solid",
        icon_color=black,
        icon_style="regular",
    )

    s_v = _make_variants(
        gray2,
        border_color=black,
        default_text_color=black,
        line_color=black,
    )

    a_v = _make_variants(
        black,
        border_color=black,
        default_text_color=white,
        line_color=black,
    )

    m_v = _make_variants(
        gray1,
        border_color=gray5,
        default_text_color=gray5,
        line_color=gray5,
    )

    l_v = _make_variants(
        white,
        border_color=gray5,
        default_text_color=gray5,
        line_color=gray5,
    )
    d_v = _make_variants(
        gray8,
        border_color=black,
        default_text_color=white,
        line_color=black,
    )

    role_variants = {
        "Primary": p_v,
        "Secondary": s_v,
        "Accent": a_v,
        "Muted": m_v,
        "Light": l_v,
        "Dark": d_v,
    }

    styles_dict: dict[str, Any] = {
        "width": 140,
        "height": 70,
        "dpi": 100,
        "colors": MonochromeColors,
        "background_color": (255, 255, 255, 1.0),
        "sourcecode_font": FontSourceCode.SOURCECODEPRO,
        "Canvas": Style(supports={"shape"}, shape_fill_color=white, shape_line_color=white, shape_line_width=0.0),
        "CanvasFlat": Style(supports={"shape"}, shape_fill_color=white, shape_line_color=white, shape_line_width=0.0),
    }

    for role_name, v in role_variants.items():
        styles_dict[role_name] = v["normal"]
        styles_dict[f"{role_name}Bordered"] = v["bordered"]
        styles_dict[f"{role_name}Bold"] = v["bold"]
        styles_dict[f"{role_name}Light"] = v["light"]
        styles_dict[f"{role_name}Flat"] = v["flat"]
        styles_dict[f"{role_name}Outline"] = v["outline"]
        styles_dict[f"{role_name}Solid"] = v["solid"]
        styles_dict[f"{role_name}OutlineBold"] = v["outline_bold"]
        styles_dict[f"{role_name}SolidBold"] = v["solid_bold"]
        styles_dict[f"{role_name}OutlineLight"] = v["outline_light"]
        styles_dict[f"{role_name}SolidLight"] = v["solid_light"]
        styles_dict[f"{role_name}Dashed"] = v["dashed"]
        styles_dict[f"{role_name}DashedBold"] = v["dashed_bold"]
        styles_dict[f"{role_name}DashedLight"] = v["dashed_light"]

    color_variants = {
        "White": _make_variants(white, border_color=black, default_text_color=black),
        "Gray1": _make_variants(gray1, border_color=gray5, default_text_color=gray5),
        "Gray2": _make_variants(gray2, border_color=gray5, default_text_color=gray5),
        "Gray3": _make_variants(gray3, border_color=gray6, default_text_color=black),
        "Gray4": _make_variants(gray4, border_color=black, default_text_color=white),
        "Gray5": _make_variants(gray5, border_color=black, default_text_color=white),
        "Gray6": _make_variants(gray6, border_color=black, default_text_color=white),
        "Gray7": _make_variants(gray7, border_color=black, default_text_color=white),
        "Gray8": _make_variants(gray8, border_color=black, default_text_color=white),
        "Black": _make_variants(black, border_color=black, default_text_color=white),
    }

    for cname, v in color_variants.items():
        styles_dict[cname] = v["normal"]
        styles_dict[f"{cname}Bordered"] = v["bordered"]
        styles_dict[f"{cname}Bold"] = v["bold"]
        styles_dict[f"{cname}Light"] = v["light"]
        styles_dict[f"{cname}Flat"] = v["flat"]
        styles_dict[f"{cname}Outline"] = v["outline"]
        styles_dict[f"{cname}Solid"] = v["solid"]
        styles_dict[f"{cname}OutlineBold"] = v["outline_bold"]
        styles_dict[f"{cname}SolidBold"] = v["solid_bold"]
        styles_dict[f"{cname}OutlineLight"] = v["outline_light"]
        styles_dict[f"{cname}SolidLight"] = v["solid_light"]
        styles_dict[f"{cname}Dashed"] = v["dashed"]
        styles_dict[f"{cname}DashedBold"] = v["dashed_bold"]
        styles_dict[f"{cname}DashedLight"] = v["dashed_light"]

    return MonochromeStyles(**styles_dict)


_monochrome_styles: MonochromeStyles = _create_monochrome_styles()
MonochromeStyles.register_default_instance(_monochrome_styles)

__all__ = [
    "MonochromeStyles",
]
