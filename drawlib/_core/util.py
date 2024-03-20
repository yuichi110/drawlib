from typing import Optional, Dict, Any
from matplotlib.font_manager import FontProperties
from matplotlib.text import Text

from drawlib._model import TextStyle, LineStyle, ShapeStyle, TextBoxStyle


def get_shape_text(
    x: float,
    y: float,
    text: str,
    angle: Optional[float] = None,
    style: Optional[TextStyle] = None,
) -> Text:
    # only check color. ignore alignment
    options = get_text_options(style)
    if "horizontalalignment" in options:
        del options["horizontalalignment"]
    if "verticalalignment" in options:
        del options["verticalalignment"]

    return Text(
        x,
        y,
        text,
        rotation=angle,
        rotation_mode="anchor",
        horizontalalignment="center",
        verticalalignment="center",
        fontproperties=get_font_properties(style),
        **options,
    )


def get_text_options(
    style: Optional[TextStyle],
) -> Dict[str, Any]:
    if style is None:
        return {}

    options = {
        "color": style.color,
        "horizontalalignment": style.halign,
        "verticalalignment": style.valign,
    }
    # delete value None keys
    return {key: value for key, value in options.items() if value is not None}


def get_font_properties(
    style: Optional[TextStyle],
) -> Optional[FontProperties]:
    if style is None:
        return None

    return FontProperties(
        size=style.size,
        family=style.font_family,
        style=style.font_style,
        variant=style.font_variant,
        weight=style.font_weight,
        stretch=style.font_stretch,
        fname=style.font_file,
        math_fontfamily=style.font_math_fontfamily,
    )


def get_line_options(
    style: Optional[LineStyle] = None,
) -> Dict[str, Any]:
    if style is None:
        return {}

    options = {
        "linewidth": style.width,
        "linestyle": style.style,
        "color": style.color,
        "alpha": style.alpha,
    }
    # delete value None keys
    return {key: value for key, value in options.items() if value is not None}


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
    # delete value None keys
    return {key: value for key, value in options.items() if value is not None}


def get_bbox_dict(self, style: Optional[TextBoxStyle] = None) -> Dict[str, Any]:
    if style is None:
        return {}

    return {}
