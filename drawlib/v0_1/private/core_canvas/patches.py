# Copyright (c) 2024 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Canvas's matplotlib base shape feature implementation module."""

import math
from typing import List, Optional, Tuple, Union

from matplotlib.patches import (
    Arc,
    Circle,
    Ellipse,
    Polygon,
    RegularPolygon,
    Wedge,
)

import drawlib.v0_1.private.validators.args as validator
from drawlib.v0_1.private.core.model import ShapeStyle, ShapeTextStyle
from drawlib.v0_1.private.core.theme import dtheme
from drawlib.v0_1.private.core.util import ShapeUtil
from drawlib.v0_1.private.core_canvas.base import CanvasBase
from drawlib.v0_1.private.util import error_handler, get_center_and_size


class CanvasPatchesFeature(CanvasBase):
    """A class for drawing various shapes using matplotlib patches on a canvas."""

    def __init__(self) -> None:
        """Initializes a CanvasPatchesFeature object.

        Initializes an instance of CanvasPatchesFeature by calling the constructor
        of its superclass, CanvasBase.
        """
        super().__init__()

    @error_handler
    def arc(
        self,
        xy: Tuple[float, float],
        width: float,
        height: float,
        from_angle: Union[int, float] = 0.0,
        to_angle: Union[int, float] = 360.0,
        angle: Union[int, float] = 0.0,
        style: Union[ShapeStyle, str, None] = None,
        text: str = "",
        textsize: Optional[float] = None,
        textstyle: Union[ShapeTextStyle, str, None] = None,
    ) -> None:
        """Draw an arc on the canvas.

        Args:
            xy: Center of the arc.
            width: Width of the arc.
            height: Height of the arc.
            from_angle (optional): Starting angle of the arc (default is 0.0).
            to_angle (optional): Ending angle of the arc (default is 360.0).
            angle (optional): Rotation angle of the arc.
            style (optional): Style of the arc.
            text (optional): Text shown at the center of the arc.
            textsize (optional): Font size of the text.
            textstyle (optional): Style of the text.

        Returns:
            None
        """
        style, textstyle = ShapeUtil.format_styles(
            style,
            textstyle,
            dtheme.arcstyles.get,
            dtheme.arctextstyles.get,
        )
        validator.validate_shape_args(locals())

        if textsize is not None:
            textstyle.size = textsize

        xy, style = ShapeUtil.apply_alignment(xy, width, height, angle, style, is_default_center=True)
        options = ShapeUtil.get_shape_options(style, default_no_line=False)
        self._artists.append(
            Arc(
                xy,
                width=width,
                height=height,
                angle=angle,
                theta1=from_angle,
                theta2=to_angle,
                **options,
            )
        )

        if not text:
            return
        self._artists.append(
            ShapeUtil.get_shape_text(
                xy=xy,
                text=text,
                angle=angle,
                style=textstyle,
            ),
        )

    @error_handler
    def circle(
        self,
        xy: Tuple[float, float],
        radius: float,
        angle: Union[int, float] = 0.0,
        style: Union[ShapeStyle, str, None] = None,
        text: str = "",
        textsize: Optional[float] = None,
        textstyle: Union[ShapeTextStyle, str, None] = None,
    ) -> None:
        """Draw a circle on the canvas.

        Args:
            xy: Center of the circle.
            radius: Radius of the circle.
            angle (optional): Rotation angle of the circle.
            style (optional): Style of the circle.
            text (optional): Text shown at the center of the circle.
            textsize (optional): Font size of the text.
            textstyle (optional): Style of the text.

        Returns:
            None
        """
        style, textstyle = ShapeUtil.format_styles(
            style,
            textstyle,
            dtheme.circlestyles.get,
            dtheme.circletextstyles.get,
        )
        validator.validate_shape_args(locals())

        if textsize is not None:
            textstyle.size = textsize

        width = radius * 2
        height = radius * 2
        xy, style = ShapeUtil.apply_alignment(xy, width, height, angle, style, is_default_center=True)
        options = ShapeUtil.get_shape_options(style)
        self._artists.append(
            Circle(
                xy=xy,
                radius=radius,
                **options,
            ),
        )

        if not text:
            return
        self._artists.append(
            ShapeUtil.get_shape_text(
                xy=xy,
                text=text,
                angle=angle,
                style=textstyle,
            ),
        )

    @error_handler
    def ellipse(
        self,
        xy: Tuple[float, float],
        width: float,
        height: float,
        angle: Union[int, float] = 0.0,
        style: Union[ShapeStyle, str, None] = None,
        text: str = "",
        textsize: Optional[float] = None,
        textstyle: Union[ShapeTextStyle, str, None] = None,
    ) -> None:
        """Draw an ellipse on the canvas.

        Args:
            xy: Center of the ellipse.
            width: Width of the ellipse.
            height: Height of the ellipse.
            angle (optional): Rotation angle of the ellipse.
            style (optional): Style of the ellipse.
            text (optional): Text shown at the center of the ellipse.
            textsize (optional): Font size of the text.
            textstyle (optional): Style of the text.

        Returns:
            None
        """
        style, textstyle = ShapeUtil.format_styles(
            style,
            textstyle,
            dtheme.ellipsestyles.get,
            dtheme.ellipsetextstyles.get,
        )
        validator.validate_shape_args(locals())

        if textsize is not None:
            textstyle.size = textsize

        xy, style = ShapeUtil.apply_alignment(xy, width, height, angle, style, is_default_center=True)
        options = ShapeUtil.get_shape_options(style)
        self._artists.append(
            Ellipse(
                xy=xy,
                width=width,
                height=height,
                angle=angle,
                **options,
            ),
        )

        if not text:
            return
        self._artists.append(
            ShapeUtil.get_shape_text(
                xy=xy,
                text=text,
                angle=angle,
                style=textstyle,
            ),
        )

    @error_handler
    def polygon(
        self,
        xys: List[Tuple[float, float]],
        style: Union[ShapeStyle, str, None] = None,
        text: str = "",
        textsize: Optional[float] = None,
        textstyle: Union[ShapeTextStyle, str, None] = None,
    ) -> None:
        """Draw a polygon on the canvas.

        Args:
            xys: List of vertices [(x1, y1), ...(x_n, y_n)].
            style (optional): Style of the polygon.
            text (optional): Text shown at the center of the polygon.
            textsize (optional): Font size of the text.
            textstyle (optional): Style of the text.

        Returns:
            None
        """
        style, textstyle = ShapeUtil.format_styles(
            style,
            textstyle,
            dtheme.polygonstyles.get,
            dtheme.polygontextstyles.get,
        )
        validator.validate_shape_args(locals())

        if textsize is not None:
            textstyle.size = textsize

        style.halign = None
        style.valign = None
        options = ShapeUtil.get_shape_options(style)
        self._artists.append(Polygon(xy=xys, closed=True, **options))

        if not text:
            return
        center, (_, _) = get_center_and_size(xys)
        self._artists.append(
            ShapeUtil.get_shape_text(
                center,
                text=text,
                angle=0,
                style=textstyle,
            ),
        )

    @error_handler
    def regularpolygon(
        self,
        xy: Tuple[float, float],
        radius: float,
        num_vertex: int,
        angle: Union[int, float] = 0.0,
        style: Union[ShapeStyle, str, None] = None,
        text: str = "",
        textsize: Optional[float] = None,
        textstyle: Union[ShapeTextStyle, str, None] = None,
    ) -> None:
        """Draw a regular polygon on the canvas.

        Args:
            xy: Center of the regular polygon.
            radius: Radius of the regular polygon's vertices.
            num_vertex: Number of vertices.
            angle (optional): Rotation angle of the polygon.
            style (optional): Style of the regular polygon.
            text (optional): Text shown at the center of the regular polygon.
            textsize (optional): Font size of the text.
            textstyle (optional): Style of the text.

        Returns:
            None
        """
        style, textstyle = ShapeUtil.format_styles(
            style,
            textstyle,
            dtheme.regularpolygonstyles.get,
            dtheme.regularpolygontextstyles.get,
        )
        validator.validate_shape_args(locals())

        if textsize is not None:
            textstyle.size = textsize

        width = radius * 2
        height = radius * 2
        xy, style = ShapeUtil.apply_alignment(xy, width, height, angle, style, is_default_center=True)
        options = ShapeUtil.get_shape_options(style)
        self._artists.append(
            RegularPolygon(
                xy,
                radius=radius,
                numVertices=num_vertex,
                orientation=math.radians(angle),
                **options,
            )
        )

        if not text:
            return
        self._artists.append(
            ShapeUtil.get_shape_text(
                xy=xy,
                text=text,
                angle=angle,
                style=textstyle,
            ),
        )

    @error_handler
    def wedge(
        self,
        xy: Tuple[float, float],
        radius: float,
        width: Optional[float] = None,
        from_angle: float = 0,
        to_angle: float = 360,
        angle: Union[int, float] = 0.0,
        style: Union[ShapeStyle, str, None] = None,
        text: str = "",
        textsize: Optional[float] = None,
        textstyle: Union[ShapeTextStyle, str, None] = None,
    ) -> None:
        """Draw a wedge on the canvas.

        Args:
            xy: Center of the wedge.
            radius: Radius of the wedge.
            width (optional): Length from outer to inner circumference.
                              Default is same as radius.
            from_angle (optional): Starting angle of the wedge (default is 0).
            to_angle (optional): Ending angle of the wedge (default is 360).
            angle (optional): Rotation angle of the wedge.
            style (optional): Style of the wedge.
            text (optional): Text shown at the center of the wedge.
            textsize (optional): Font size of the text.
            textstyle (optional): Style of the text.

        Returns:
            None
        """
        style, textstyle = ShapeUtil.format_styles(
            style,
            textstyle,
            dtheme.wedgestyles.get,
            dtheme.wedgetextstyles.get,
        )
        validator.validate_shape_args(locals(), argnames_accept_none=["width"])

        if textsize is not None:
            textstyle.size = textsize

        ext_width = radius * 2
        ext_height = radius * 2
        xy, style = ShapeUtil.apply_alignment(xy, ext_width, ext_height, angle, style, is_default_center=True)
        options = ShapeUtil.get_shape_options(style)
        self._artists.append(
            Wedge(
                center=xy,
                r=radius,
                width=width,  # None makes no hole
                theta1=from_angle + angle,
                theta2=to_angle + angle,
                **options,
            )
        )

        if not text:
            return
        self._artists.append(
            ShapeUtil.get_shape_text(
                xy=xy,
                text=text,
                angle=angle,
                style=textstyle,
            ),
        )

    @error_handler
    def donuts(
        self,
        xy: Tuple[float, float],
        radius: float,
        width: Optional[float] = None,
        angle: Union[int, float] = 0.0,
        style: Union[ShapeStyle, str, None] = None,
        text: str = "",
        textsize: Optional[float] = None,
        textstyle: Union[ShapeTextStyle, str, None] = None,
    ) -> None:
        """Draw a donut shape on the canvas.

        Args:
            xy: Center of the donut.
            radius: Radius of the donut.
            width (optional): Width of the donut ring (default is None).
            angle (optional): Rotation angle of the donut.
            style (optional): Style of the donut.
            text (optional): Text shown at the center of the donut.
            textsize (optional): Font size of the text.
            textstyle (optional): Style of the text.

        Returns:
            None
        """
        style, textstyle = ShapeUtil.format_styles(
            style,
            textstyle,
            dtheme.donutsstyles.get,
            dtheme.donutstextstyles.get,
        )
        validator.validate_shape_args(locals(), argnames_accept_none=["width"])

        self.wedge(
            xy=xy,
            radius=radius,
            width=width,
            angle=angle,
            style=style,
            text=text,
            textsize=textsize,
            textstyle=textstyle,
        )

    @error_handler
    def fan(
        self,
        xy: Tuple[float, float],
        radius: float,
        from_angle: float = 0,
        to_angle: float = 180,
        angle: Union[int, float] = 0.0,
        style: Union[ShapeStyle, str, None] = None,
        text: str = "",
        textsize: Optional[float] = None,
        textstyle: Union[ShapeTextStyle, str, None] = None,
    ) -> None:
        """Draw a fan shape on the canvas.

        Args:
            xy: Center of the fan.
            radius: Radius of the fan.
            from_angle (optional): Starting angle of the fan (default is 0).
            to_angle (optional): Ending angle of the fan (default is 180).
            angle (optional): Rotation angle of the fan.
            style (optional): Style of the fan.
            text (optional): Text shown at the center of the fan.
            textsize (optional): Font size of the text.
            textstyle (optional): Style of the text.

        Returns:
            None
        """
        style, textstyle = ShapeUtil.format_styles(
            style,
            textstyle,
            dtheme.fanstyles.get,
            dtheme.fantextstyles.get,
        )
        validator.validate_shape_args(locals())

        self.wedge(
            xy=xy,
            radius=radius,
            width=None,
            from_angle=from_angle,
            to_angle=to_angle,
            angle=angle,
            style=style,
            text=text,
            textsize=textsize,
            textstyle=textstyle,
        )
