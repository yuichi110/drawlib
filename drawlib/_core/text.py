"""write docstring later"""

from typing import Literal, Optional
from matplotlib.text import Text

from drawlib._model import TextStyle, TextBackgroundStyle
from drawlib._core.util import (
    get_text_options,
    get_font_properties,
    get_bbox_dict,
)
from drawlib._util import error_handler


@error_handler
def get_text(
    x: float,
    y: float,
    text: str,
    style: Optional[TextStyle] = None,
    background: Optional[TextBackgroundStyle] = None,
    angle: Optional[float] = None,
) -> Text:
    """write docstring later"""

    options = get_text_options(style)
    fp = get_font_properties(style)
    bx = get_bbox_dict(background)

    # set default alignment
    if angle is None or angle == 0:
        angle = 0
        if "horizontalalignment" not in options:
            options["horizontalalignment"] = "left"
        if "verticalalignment" not in options:
            options["verticalalignment"] = "bottom"
    else:
        if "horizontalalignment" not in options:
            options["horizontalalignment"] = "center"
        if "verticalalignment" not in options:
            options["verticalalignment"] = "center"

    return Text(
        x=x,
        y=y,
        text=text,
        rotation=angle,
        rotation_mode="anchor",
        fontproperties=fp,
        bbox=bx,
        **options,
    )


@error_handler
def get_text_vertical(x: float, y: float, text: str) -> Text:
    """write docstring later"""
    return Text(1, 1, "hello")
