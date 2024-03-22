from typing import Final, Union, Optional, List, Tuple, Dict, Any, Literal
from matplotlib.text import Text
from matplotlib.patches import Arc, Circle, Rectangle, FancyBboxPatch
import matplotlib as mpl
from matplotlib.axes import Axes

from drawlib._model import TextStyle, ShapeStyle
from drawlib._core.util import get_shape_options, get_shape_text


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
    style: Optional[ShapeStyle] = None,
    angle: Optional[float] = None,
    text: Optional[str] = None,
    textstyle: Optional[TextStyle] = None,
) -> Tuple[Circle, Optional[Text]]:
    circle = Circle((x, y), radius, color="red")
    if text:
        return circle, get_shape_text(x, y, text, angle, textstyle)

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
    style: Optional[ShapeStyle] = None,
    angle: Optional[float] = None,
    text: Optional[str] = None,
    textstyle: Optional[TextStyle] = None,
) -> Tuple[Rectangle, Optional[Text]]:
    if angle is None:
        angle = 0
    options = get_shape_options(style)
    rectangle = Rectangle(
        (x, y),
        width,
        height,
        angle=angle,
        rotation_point="center",
        **options,
    )

    if text:
        center_x = x + width / 2
        center_y = y + height / 2
        t = get_shape_text(center_x, center_y, text, angle, textstyle)
        return rectangle, t

    return rectangle, None


def get_rectangle_rounded(
    x: float,
    y: float,
    width: float,
    height: float,
    rtype: Optional[Literal["round", "round4", "sawtooth", "roundtooth"]] = None,
    pad: Optional[float] = None,
    style: Optional[ShapeStyle] = None,
    ax_and_angle: Optional[Tuple[Axes, float]] = None,
    text: Optional[str] = None,
    textstyle: Optional[TextStyle] = None,
) -> Tuple[FancyBboxPatch, Optional[Text]]:
    # create boxstyle
    if rtype is None:
        rtype = "round"
    if pad is None:
        pad = 0.3
    boxstyle = f"{rtype},pad={pad}"

    # create angle for text
    if ax_and_angle is None:
        angle = 0

    options = get_shape_options(style)
    rectangle = FancyBboxPatch(
        (x + pad, y + pad),
        width - pad * 2,
        height - pad * 2,
        boxstyle=boxstyle,
        **options,
    )
    if ax_and_angle is not None:
        ax = ax_and_angle[0]
        angle = ax_and_angle[1]
        cx = x + width / 2
        cy = y + height / 2
        t2 = mpl.transforms.Affine2D().rotate_deg_around(cx, cy, angle) + ax.transData
        rectangle.set_transform(t2)

    if text is not None:
        center_x = x + width / 2
        center_y = y + height / 2
        t = get_shape_text(center_x, center_y, text, angle, textstyle)
        return rectangle, t

    return rectangle, None


def get_wedge(self): ...
