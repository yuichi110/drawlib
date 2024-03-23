"""write docstring later"""

from typing import (
    Union,
    Optional,
    List,
    Tuple,
    Dict,
    Any,
    Literal,
)


class TextStyle:
    """write docstring later"""

    def __init__(
        self,
        color: Union[float, str, Tuple[float, float, float], None] = None,
        size: Union[float, str, None] = None,
        halign: Optional[Literal["left", "center", "right"]] = None,
        valign: Optional[Literal["bottom", "center", "top"]] = None,
        font_family: Optional[str] = None,
        font_file: Optional[str] = None,
        font_style: Optional[Literal["normal", "italic", "oblique"]] = None,
        font_variant: Optional[Literal["normal", "small-caps"]] = None,
        font_weight: Union[int, str, None] = None,
        font_stretch: Union[int, str, None] = None,
        font_math_fontfamily: Optional[str] = None,
    ):
        self.color = color
        self.size = size
        self.halign = halign
        self.valign = valign
        self.font_family = font_family
        self.font_file = font_file
        self.font_style = font_style
        self.font_variant = font_variant
        self.font_weight = font_weight
        self.font_stretch = font_stretch
        self.font_math_fontfamily = font_math_fontfamily


class LineStyle:
    """write docstring later"""

    def __init__(
        self,
        width: Optional[float] = None,
        color: Union[float, str, Tuple[float, float, float], None] = None,
        style: Optional[Literal["solid", "dashed", "dotted", "dashdot"]] = None,
        alpha: Optional[float] = None,
    ):
        self.width = width
        self.color = color
        self.style = style
        self.alpha = alpha


class ShapeStyle:
    """write docstring later"""

    def __init__(
        self,
        color: Union[float, str, Tuple[float, float, float], None] = None,
        lwidth: Optional[float] = 0.1,
        lcolor: Union[float, str, Tuple[float, float, float], None] = None,
        lstyle: Optional[
            Literal["solid", "dashed", "dotted", "dashdot"]
        ] = None,
        fcolor: Union[float, str, Tuple[float, float, float], None] = None,
        alpha: Optional[float] = None,
    ):
        self.color = color
        self.lwidth = lwidth
        self.lcolor = lcolor
        self.lstyle = lstyle
        self.fcolor = fcolor
        self.alpha = alpha


class TextBackgroundStyle:
    """write docstring later"""

    def __init__(
        self,
        boxstyle: Literal[
            "square",
            "circle",
            "ellipse",
            "larrow",
            "rarrow",
            "darrow",
            "round",
            "round4",
            "sawtooth",
            "roundtooth",
        ],
        lwidth: Optional[float] = 0.1,
        lcolor: Union[float, str, Tuple[float, float, float], None] = None,
        lstyle: Optional[
            Literal["solid", "dashed", "dotted", "dashdot"]
        ] = None,
        fcolor: Union[float, str, Tuple[float, float, float], None] = None,
        alpha: Optional[float] = None,
        pad: Optional[float] = 0.3,
        rounding_size: Optional[float] = None,
        tooth_size: Optional[float] = None,
    ):
        self.boxstyle = boxstyle
        self.lwidth = lwidth
        self.lcolor = lcolor
        self.lstyle = lstyle
        self.fcolor = fcolor
        self.alpha = alpha
        self.pad = pad
        self.rounding_size = rounding_size
        self.tooth_size = tooth_size
