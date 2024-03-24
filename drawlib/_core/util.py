"""write docstring later"""

from typing import Optional, Dict, Any
from matplotlib.font_manager import FontProperties
from matplotlib.text import Text

from drawlib._model import (
    TextStyle,
    LineStyle,
    ShapeStyle,
    TextBackgroundStyle,
)
from drawlib._util import error_handler


@error_handler
def get_shape_text(
    x: float,
    y: float,
    text: str,
    angle: Optional[float] = None,
    style: Optional[TextStyle] = None,
) -> Text:
    """write docstring later"""

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


@error_handler
def get_text_options(
    style: Optional[TextStyle],
) -> Dict[str, Any]:
    """write docstring later"""

    if style is None:
        return {}

    options = {
        "color": style.color,
        "horizontalalignment": style.halign,
        "verticalalignment": style.valign,
    }
    # delete value None keys
    return {key: value for key, value in options.items() if value is not None}


@error_handler
def get_font_properties(
    style: Optional[TextStyle],
) -> Optional[FontProperties]:
    """write docstring later"""

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


@error_handler
def get_line_options(
    style: Optional[LineStyle] = None,
) -> Dict[str, Any]:
    """write docstring later"""

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


@error_handler
def get_shape_options(
    style: Optional[ShapeStyle] = None,
) -> Dict[str, Any]:
    """write docstring later"""

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


@error_handler
def get_bbox_dict(
    style: Optional[TextBackgroundStyle] = None,
) -> Optional[Dict[str, Any]]:
    """write docstring later"""

    if style is None:
        # {} doesn't mean no style.
        # requires returning None when no style.
        return None

    def get_boxstyle():
        boxstyle = style.boxstyle
        if boxstyle is None:
            boxstyle = "square"
        if boxstyle in ["round", "round4", "sawtooth", "roundtooth"]:
            pad = style.pad
            if pad is None:
                pad = 0.3
            boxstyle += f",pad={pad}"
        if boxstyle in ["round, round4"]:
            if style.rounding_size is not None:
                boxstyle += f",rounding_size={style.rounding_size}"
        elif boxstyle in ["sawtooth", "roundtooth"]:
            if style.tooth_size is not None:
                boxstyle += f",tooth_size={style.tooth_size}"
        return boxstyle

    bbox_dict = {
        "boxstyle": get_boxstyle(),
        "facecolor": style.fcolor if style.fcolor is not None else style.color,
        "edgecolor": style.lcolor if style.lcolor is not None else style.color,
        "linestyle": style.lstyle,
        "linewidth": style.lwidth,
        "alpha": style.alpha,
    }

    # delete value None keys
    return {key: value for key, value in bbox_dict.items() if value is not None}
