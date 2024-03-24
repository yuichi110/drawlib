"""write docstring later"""

from dataclasses import dataclass
import os
from typing import (
    Union,
    Optional,
    List,
    Tuple,
    Dict,
    Any,
    Literal,
)
from drawlib._util import get_script_relative_path


@dataclass
class TextStyle:
    """write docstring later"""

    color: Union[float, str, Tuple[float, float, float], None] = None
    size: Union[float, str, None] = None
    halign: Optional[Literal["left", "center", "right"]] = None
    valign: Optional[Literal["bottom", "center", "top"]] = None
    font_family: Optional[str] = None
    font_file: Optional[str] = None
    font_style: Optional[Literal["normal", "italic", "oblique"]] = None
    font_variant: Optional[Literal["normal", "small-caps"]] = None
    font_weight: Union[int, str, None] = None
    font_stretch: Union[int, str, None] = None
    font_math_fontfamily: Optional[str] = None

    @property
    def font_file(self):
        return self._font_file

    @font_file.setter
    def font_file(self, value):
        path = get_script_relative_path(value)
        if not os.path.exists(path):
            raise FileNotFoundError('font file "{path}" does not exist.')
        self._font_file = path


@dataclass
class LineStyle:
    """write docstring later"""

    width: Optional[float] = None
    color: Union[float, str, Tuple[float, float, float], None] = None
    style: Optional[Literal["solid", "dashed", "dotted", "dashdot"]] = None
    alpha: Optional[float] = None


@dataclass
class ShapeStyle:
    """write docstring later"""

    color: Union[float, str, Tuple[float, float, float], None] = None
    lwidth: Optional[float] = 0.1
    lcolor: Union[float, str, Tuple[float, float, float], None] = None
    lstyle: Optional[
        Literal[
            "solid",
            "dashed",
            "dotted",
            "dashdot",
        ]
    ] = None
    fcolor: Union[float, str, Tuple[float, float, float], None] = None
    alpha: Optional[float] = None


@dataclass
class TextBackgroundStyle:
    """write docstring later"""

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
    ]
    lwidth: Optional[float] = 0.1
    lcolor: Union[float, str, Tuple[float, float, float], None] = None
    lstyle: Optional[
        Literal[
            "solid",
            "dashed",
            "dotted",
            "dashdot",
        ]
    ] = None
    fcolor: Union[float, str, Tuple[float, float, float], None] = None
    alpha: Optional[float] = None
    pad: Optional[float] = 0.3
    rounding_size: Optional[float] = None
    tooth_size: Optional[float] = None
