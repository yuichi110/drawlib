# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Canvas's matplotlib base shape feature implementation module."""

import math

from matplotlib.patches import (
    Arc,
    Circle,
    Ellipse,
    RegularPolygon,
    Wedge,
)

from drawlib._core.l1_core import guarded
from drawlib._core.l2_types import (
    TypeAngle,
    TypeCoordinate,
    TypeFloat,
    TypeNumVertex,
    TypePosFloat,
    TypeSize,
    TypeStr,
)
from drawlib._core.l3_styles import ShapeStyle, ShapeTextStyle
from drawlib._core.l4_canvas._base import CanvasBase
from drawlib._core.l4_canvas_utils import ShapeUtil


class CanvasPatchesFeature(CanvasBase):
    """A class for drawing various shapes using matplotlib patches on a canvas."""

    def __init__(self) -> None:
        """Initializes a CanvasPatchesFeature object.

        Initializes an instance of CanvasPatchesFeature by calling the constructor
        of its superclass, CanvasBase.
        """
        super().__init__()

    @guarded
    def arc(
        self,
        xy: TypeCoordinate,
        width: TypePosFloat,
        height: TypePosFloat,
        angle_start: TypeAngle = 0.0,
        angle_end: TypeAngle = 360.0,
        angle: TypeAngle = 0.0,
        style: ShapeStyle | TypeStr | None = None,
        text: TypeStr = "",
        textsize: TypeSize | None = None,
        textstyle: ShapeTextStyle | TypeStr | None = None,
    ) -> None:
        """Draw an arc on the canvas.

        Args:
            xy: Center coordinates tuple (x, y).
            width: Width of arc.
            height: Height of arc.
            angle_start: Starting angle in degrees.
            angle_end: Ending angle in degrees.
            angle: Rotation angle in degrees.
            style: ShapeStyle object or preset string.
            text: Text to display inside shape.
            textsize: Font size of text.
            textstyle: ShapeTextStyle object or preset string.
        """
        style, textstyle = ShapeUtil.format_styles(
            style,
            textstyle,
        )

        if textsize is not None:
            textstyle.text_size = textsize

        xy, style = ShapeUtil.apply_alignment(xy, width, height, angle, style, is_default_center=True)
        options = ShapeUtil.get_shape_options(style, default_no_line=False)
        self._artists.append(
            Arc(
                xy,
                width=width,
                height=height,
                angle=angle,
                theta1=angle_start,
                theta2=angle_end,
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

    @guarded
    def circle(
        self,
        xy: TypeCoordinate,
        radius: TypePosFloat,
        angle: TypeAngle = 0.0,
        style: ShapeStyle | TypeStr | None = None,
        text: TypeStr = "",
        textsize: TypeSize | None = None,
        textstyle: ShapeTextStyle | TypeStr | None = None,
    ) -> None:
        """Draw a circle on the canvas.

        Args:
            xy: Center coordinates tuple (x, y).
            radius: Radius of the circle.
            angle: Rotation angle in degrees.
            style: ShapeStyle object or preset string.
            text: Text to display inside shape.
            textsize: Font size of text.
            textstyle: ShapeTextStyle object or preset string.
        """
        style, textstyle = ShapeUtil.format_styles(
            style,
            textstyle,
        )

        if textsize is not None:
            textstyle.text_size = textsize

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

    @guarded
    def ellipse(
        self,
        xy: TypeCoordinate,
        width: TypePosFloat,
        height: TypePosFloat,
        angle: TypeAngle = 0.0,
        style: ShapeStyle | TypeStr | None = None,
        text: TypeStr = "",
        textsize: TypeSize | None = None,
        textstyle: ShapeTextStyle | TypeStr | None = None,
    ) -> None:
        """Draw an ellipse on the canvas.

        Args:
            xy: Center coordinates tuple (x, y).
            width: Width of the ellipse.
            height: Height of the ellipse.
            angle: Rotation angle in degrees.
            style: ShapeStyle object or preset string.
            text: Text to display inside shape.
            textsize: Font size of text.
            textstyle: ShapeTextStyle object or preset string.
        """
        style, textstyle = ShapeUtil.format_styles(
            style,
            textstyle,
        )

        if textsize is not None:
            textstyle.text_size = textsize

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

    @guarded
    def regularpolygon(
        self,
        xy: TypeCoordinate,
        num_vertex: TypeNumVertex,
        radius: TypePosFloat,
        angle: TypeAngle = 0.0,
        style: ShapeStyle | TypeStr | None = None,
        text: TypeStr = "",
        textsize: TypeSize | None = None,
        textstyle: ShapeTextStyle | TypeStr | None = None,
    ) -> None:
        """Draw a regular polygon on the canvas.

        Args:
            xy: Center coordinates tuple (x, y).
            num_vertex: Number of vertices.
            radius: Radius of polygon.
            angle: Rotation angle in degrees.
            style: ShapeStyle object or preset string.
            text: Text to display inside shape.
            textsize: Font size of text.
            textstyle: ShapeTextStyle object or preset string.
        """
        style, textstyle = ShapeUtil.format_styles(
            style,
            textstyle,
        )

        if textsize is not None:
            textstyle.text_size = textsize

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

    @guarded
    def wedge(
        self,
        xy: TypeCoordinate,
        radius: TypePosFloat,
        width: TypePosFloat | None = None,
        angle_start: TypeAngle = 0,
        angle_end: TypeAngle = 360,
        angle: TypeAngle = 0.0,
        style: ShapeStyle | TypeStr | None = None,
        text: TypeStr = "",
        textsize: TypeSize | None = None,
        textstyle: ShapeTextStyle | TypeStr | None = None,
    ) -> None:
        """Draw a wedge shape on the canvas.

        Args:
            xy: Center coordinates tuple (x, y).
            radius: Outer radius of the wedge.
            width: Width of the wedge ring (inner radius = radius - width).
            angle_start: Starting theta angle in degrees.
            angle_end: Ending theta angle in degrees.
            angle: Rotation angle in degrees.
            style: ShapeStyle object or preset string.
            text: Text to display inside shape.
            textsize: Font size of text.
            textstyle: ShapeTextStyle object or preset string.
        """
        style, textstyle = ShapeUtil.format_styles(
            style,
            textstyle,
        )

        if textsize is not None:
            textstyle.text_size = textsize

        ext_width = radius * 2
        ext_height = radius * 2
        xy, style = ShapeUtil.apply_alignment(xy, ext_width, ext_height, angle, style, is_default_center=True)
        options = ShapeUtil.get_shape_options(style)
        self._artists.append(
            Wedge(
                center=xy,
                r=radius,
                width=width,  # None makes no hole
                theta1=angle_start + angle,
                theta2=angle_end + angle,
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

    @guarded
    def donuts(
        self,
        xy: TypeCoordinate,
        radius: TypePosFloat,
        width: TypePosFloat | None = None,
        angle: TypeAngle = 0.0,
        style: ShapeStyle | TypeStr | None = None,
        text: TypeStr = "",
        textsize: TypeSize | None = None,
        textstyle: ShapeTextStyle | TypeStr | None = None,
    ) -> None:
        """Draw a donut shape on the canvas.

        Args:
            xy: Center coordinates tuple (x, y).
            radius: Outer radius of the donut.
            width: Width of the donut ring.
            angle: Rotation angle in degrees.
            style: ShapeStyle object or preset string.
            text: Text to display inside shape.
            textsize: Font size of text.
            textstyle: ShapeTextStyle object or preset string.
        """
        style, textstyle = ShapeUtil.format_styles(
            style,
            textstyle,
        )

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

    @guarded
    def fan(
        self,
        xy: TypeCoordinate,
        radius: TypePosFloat,
        angle_start: TypeAngle = 0,
        angle_end: TypeAngle = 180,
        angle: TypeAngle = 0.0,
        style: ShapeStyle | TypeStr | None = None,
        text: TypeStr = "",
        textsize: TypeSize | None = None,
        textstyle: ShapeTextStyle | TypeStr | None = None,
    ) -> None:
        """Draw a fan shape on the canvas.

        Args:
            xy: Center coordinates tuple (x, y).
            radius: Radius of the fan.
            angle_start: Starting theta angle in degrees.
            angle_end: Ending theta angle in degrees.
            angle: Rotation angle in degrees.
            style: ShapeStyle object or preset string.
            text: Text to display inside shape.
            textsize: Font size of text.
            textstyle: ShapeTextStyle object or preset string.
        """
        style, textstyle = ShapeUtil.format_styles(
            style,
            textstyle,
        )

        self.wedge(
            xy=xy,
            radius=radius,
            width=None,
            angle_start=angle_start,
            angle_end=angle_end,
            angle=angle,
            style=style,
            text=text,
            textsize=textsize,
            textstyle=textstyle,
        )
