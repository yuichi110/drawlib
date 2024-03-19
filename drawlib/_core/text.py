from typing import Optional
from matplotlib.text import Text

from drawlib._model import FontStyle, TextBoxStyle
from drawlib._core.util import get_bbox_dict, get_font_properties


def get_text(
    x: float,
    y: float,
    text_: str,
    font: Optional[FontStyle] = None,
    box: Optional[TextBoxStyle] = None,
) -> Text:
    fp = get_font_properties(font)
    bx = get_bbox_dict(box)
    return Text(x, y, text_, fontproperties=fp, bbox=bx)


def get_text_vertical(x: float, y: float, s: str): ...
