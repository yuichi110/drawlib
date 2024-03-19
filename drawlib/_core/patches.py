from typing import Final, Union, Optional, List, Tuple, Dict, Any, Literal
from matplotlib.text import Text
from matplotlib.patches import Arc, Circle, Rectangle, FancyBboxPatch

from drawlib._model import FontStyle
from drawlib._core.util import get_shape_text


def get_arc(
    x: float,
    y: float,
    width: float,
    height: float,
    angle: float = 0,
) -> Arc:
    return Arc((x, y), width, height, angle)


def get_arrow(self): ...


def get_arrow_fancy(self): ...


def get_circle(
    x: float,
    y: float,
    radius: float,
    angle: Optional[float] = None,
    text: Optional[str] = None,
    font: Optional[FontStyle] = None,
) -> Tuple[Circle, Optional[Text]]:
    circle = Circle((x, y), radius, color="red")
    if text:
        return circle, get_shape_text(x, y, text, angle, font)

    return circle, None


def get_ellipse(self): ...


def get_polygon(self): ...


def get_polygon_circle(self): ...


def get_polygon_regular(self): ...


def get_rectangle(
    x: float,
    y: float,
    width: float,
    height: float,
    angle: Optional[float] = None,
    text: Optional[str] = None,
    font: Optional[FontStyle] = None,
) -> Tuple[Rectangle, Optional[Text]]:
    if angle is None:
        angle = 0

    rectangle = Rectangle(
        (x, y),
        width,
        height,
        angle=angle,
        rotation_point="center",
        color="red",
    )

    if text:
        center_x = x + width / 2
        center_y = y + height / 2
        t = get_shape_text(center_x, center_y, text, angle, font)
        return rectangle, t

    return rectangle, None


def get_rectangle_rounded(
    x: float,
    y: float,
    width: float,
    height: float,
    rtype: Optional[Literal["round", "round4", "sawtooth", "roundtooth"]] = None,
    pad: Optional[float] = None,
    text: Optional[str] = None,
    font: Optional[FontStyle] = None,
) -> Tuple[FancyBboxPatch, Optional[Text]]:
    if rtype is None:
        rtype = "round"
    if pad is None:
        pad = 0.3
    boxstyle = f"{rtype},pad={pad}"

    rectangle = FancyBboxPatch(
        (x + pad, y + pad),
        width - pad * 2,
        height - pad * 2,
        boxstyle=boxstyle,
        color="red",
    )

    if text:
        center_x = x + width / 2
        center_y = y + height / 2
        t = get_shape_text(center_x, center_y, text, font=font)
        return rectangle, t

    return rectangle, None


def get_wedge(self): ...
