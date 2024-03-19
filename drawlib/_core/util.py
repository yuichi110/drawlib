from typing import Optional, Dict, Any
from matplotlib.font_manager import FontProperties
from matplotlib.text import Text

from drawlib._model import FontStyle, LineStyle, ShapeStyle, TextBoxStyle


def get_shape_text(
    x: float,
    y: float,
    text: str,
    angle: Optional[float] = None,
    font: Optional[FontStyle] = None,
) -> Text:
    return Text(
        x,
        y,
        text,
        rotation=angle,
        rotation_mode="anchor",
        horizontalalignment="center",
        verticalalignment="center",
        fontproperties=get_font_properties(font),
    )


def get_font_properties(
    style: Optional[FontStyle],
) -> Optional[FontProperties]:
    if style is None:
        return None

    return FontProperties(
        family=style.family,
        style=style.style,
        variant=style.variant,
        weight=style.weight,
        stretch=style.stretch,
        size=style.size,
        fname=style.file,
        math_fontfamily=style.math_fontfamily,
    )


def get_line_options(
    style: Optional[LineStyle] = None,
) -> Dict[str, Any]:
    if style is None:
        return {}

    return {
        "linewidth": style.width,
        "linestyle": style.style,
        "color": style.color,
        "alpha": style.alpha,
    }


def get_shape_options(
    style: Optional[ShapeStyle] = None,
) -> Dict[str, Any]:
    if style is None:
        return {}

    options = {
        "facecolor": style.fcolor if style.fcolor is not None else style.color,
        "edgecolor": style.lcolor if style.lcolor is not None else style.color,
        "linestyle": style.lstyle,
        "linewidth": style.lwidth,
        "alpha": style.alpha,
    }
    return {key: value for key, value in options.items() if value is not None}


def get_bbox_dict(self, style: Optional[TextBoxStyle] = None) -> Dict[str, Any]:
    if style is None:
        return {}

    return {}
