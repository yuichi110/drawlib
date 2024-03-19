from typing import Final, Union, Optional, List, Tuple, Dict, Any, Literal


class FontStyle:

    def __init__(
        self,
        family: Optional[str] = None,
        file: Optional[str] = None,
        size: Union[float, str, None] = None,
        style: Optional[Literal["normal", "italic", "oblique"]] = None,
        variant: Optional[Literal["normal", "small-caps"]] = None,
        weight: Union[int, str, None] = None,
        stretch: Union[int, str, None] = None,
        math_fontfamily: Optional[str] = None,
    ):
        self.family = family
        self.file = file
        self.size = size
        self.style = style
        self.variant = variant
        self.weight = weight
        self.stretch = stretch
        self.math_fontfamily = math_fontfamily


class LineStyle:

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

    def __init__(
        self,
        color: Union[float, str, Tuple[float, float, float], None] = None,
        lwidth: Optional[float] = 0.1,
        lcolor: Union[float, str, Tuple[float, float, float], None] = None,
        lstyle: Optional[Literal["solid", "dashed", "dotted", "dashdot"]] = None,
        fcolor: Union[float, str, Tuple[float, float, float], None] = None,
        alpha: Optional[float] = None,
    ):
        self.color = color
        self.lwidth = lwidth
        self.lcolor = lcolor
        self.lstyle = lstyle
        self.fcolor = fcolor
        self.alpha = alpha


class TextBoxStyle:
    BOXSTYLE_SQUARE = "square"

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
        lstyle: Optional[Literal["solid", "dashed", "dotted", "dashdot"]] = None,
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
