# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.


"""Canvas's original arrow feature implementation module."""

from __future__ import annotations

from matplotlib.patches import PathPatch

from drawlib._core.l1_core import validate_call
from drawlib._core.l2_types import (
    Angle,
    Angle90,
    ArrowHead,
    Coordinate,
    Coordinates,
    PosFloat,
)
from drawlib._core.l3_math import (
    get_angle,
    get_distance,
    get_rotated_points,
)
from drawlib._core.l3_styles import Style
from drawlib._core.l4_canvas._shapes._arrow_builders import (
    ArrowPolylineHelper,
    build_arrow_arc_path_points,
    build_arrow_points,
    build_arrow_polyline_points,
    build_chevron_points,
)
from drawlib._core.l4_canvas._shapes._polygon import CanvasShapePolygonFeature
from drawlib._core.l4_canvas._shapes._shape_utils import ShapeUtils


class CanvasShapeArrowFeature(CanvasShapePolygonFeature):
    """Canvas arrow shape feature implementation module.

    This class provides methods to draw single-headed and double-headed arrows
    on a canvas. The arrows can be customized with various styles for the tail,
    head, and optional text annotations.
    """

    _get_path_from_points = staticmethod(ShapeUtils.build_matplotlib_path)

    def __init__(self) -> None:
        """Initialize CanvasShapeArrowFeature."""
        super().__init__()

    @validate_call
    def arrow(
        self,
        xy1: Coordinate,
        xy2: Coordinate,
        tail_width: PosFloat,
        head_width: PosFloat,
        head_length: PosFloat,
        head: ArrowHead = "->",
        *,
        style: Style,
        text: str = "",
        text_style: Style | None = None,
    ) -> None:
        """Draw a straight arrow between two coordinates.

        Args:
            xy1: Starting point coordinates tuple (x, y).
            xy2: Ending point coordinates tuple (x, y).
            tail_width: Width of arrow tail.
            head_width: Width of arrow head.
            head_length: Length of arrow head.
            head: Arrow head type ("->", "<-", "<->").
            style: Style object.
            text: Text to display inside shape.
            text_style: Style object for text or None.
        """
        style, text_style = ShapeUtils.format_styles(
            style,
            text_style,
        )

        x1, y1 = xy1
        x2, y2 = xy2
        x, y = ((x1 + x2) / 2, (y1 + y2) / 2)
        angle = get_angle(xy1, xy2)
        style = style.patch(halign="center", valign="center", angle=angle)

        distance = get_distance(xy1, xy2)
        if distance <= 1e-9:
            return
        points = build_arrow_points(
            distance=distance,
            tail_width=tail_width,
            head_width=head_width,
            head_length=head_length,
            head=head,
        )

        self.shape(
            xy=(x, y),
            path_points=points,
            style=style,
            text=text,
            text_style=text_style,
        )

    @validate_call
    def arrow_polyline(
        self,
        xys: Coordinates,
        tail_width: PosFloat,
        head_width: PosFloat,
        head_length: PosFloat,
        head: ArrowHead = "->",
        *,
        style: Style,
    ) -> None:
        """Draw a polyline arrow along multiple coordinates.

        Args:
            xys: Sequence of coordinate tuples.
            tail_width: Width of arrow tail.
            head_width: Width of arrow head.
            head_length: Length of arrow head.
            head: Arrow head type ("->", "<-", "<->").
            style: Style object.
        """
        style, _ = ShapeUtils.format_styles(
            style,
            None,
        )
        outline_points = build_arrow_polyline_points(
            xys=xys,
            tail_width=tail_width,
            head_width=head_width,
            head_length=head_length,
            head=head,
            shape_r=style.shape_r,
        )
        self.polygon(xys=outline_points, style=style.patch(shape_r=0.0), text="", text_style=None)

    @validate_call
    def arrow_arc(
        self,
        xy: Coordinate,
        width: PosFloat,
        height: PosFloat,
        tail_width: PosFloat,
        head_width: PosFloat,
        head_angle: Angle = 10,
        head: ArrowHead = "->",
        angle_start: Angle = 0,
        angle_end: Angle = 180,
        *,
        style: Style,
    ) -> None:
        """Draw an arc-shaped arrow on the canvas.

        Args:
            xy: Center coordinate tuple (x, y).
            width: Width of arc.
            height: Height of arc.
            tail_width: Width of arrow tail.
            head_width: Width of arrow head.
            head_angle: Angular length of arrow head.
            head: Arrow head type ("->", "<-", "<->").
            angle_start: Starting angle in degrees.
            angle_end: Ending angle in degrees.
            style: Style object.
        """
        style, _ = ShapeUtils.format_styles(
            style,
            None,
        )
        angle: Angle = style.angle if style.angle is not None else 0.0

        path_points = build_arrow_arc_path_points(
            xy=xy,
            width=width,
            height=height,
            tail_width=tail_width,
            head_width=head_width,
            head_angle=head_angle,
            head=head,
            angle_start=angle_start,
            angle_end=angle_end,
            angle=angle,
        )

        path = ShapeUtils.build_matplotlib_path(path_points)
        options = ShapeUtils.get_shape_options(style)
        self._artists.append(PathPatch(path=path, **options))

    @validate_call
    def arrow_l(
        self,
        xy: Coordinate,
        width: PosFloat,
        height: PosFloat,
        tail_width: PosFloat,
        head_width: PosFloat,
        head_length: PosFloat,
        head: ArrowHead = "->",
        *,
        style: Style,
    ) -> None:
        """Draw an L-shaped arrow on the canvas.

        Args:
            xy: Center coordinate tuple (x, y).
            width: Width of L-shape.
            height: Height of L-shape.
            tail_width: Width of arrow tail.
            head_width: Width of arrow head.
            head_length: Length of arrow head.
            head: Arrow head type ("->", "<-", "<->").
            style: Style object.
        """
        style, _ = ShapeUtils.format_styles(
            style,
            None,
        )
        angle: Angle = style.angle if style.angle is not None else 0.0

        p1 = (xy[0] - width / 2, xy[1] + height / 2)
        p2 = (xy[0] - width / 2, xy[1] - height / 2)
        p3 = (xy[0] + width / 2, xy[1] - height / 2)

        xys = [p1, p2, p3]
        if angle != 0:
            xys = get_rotated_points(xys=xys, center=xy, angle=angle)

        self.arrow_polyline(
            xys=xys,
            tail_width=tail_width,
            head_width=head_width,
            head_length=head_length,
            head=head,
            style=style,
        )

    @validate_call
    def arrow_u(
        self,
        xy: Coordinate,
        width: PosFloat,
        height: PosFloat,
        tail_width: PosFloat,
        head_width: PosFloat,
        head_length: PosFloat,
        head: ArrowHead = "->",
        *,
        style: Style,
    ) -> None:
        """Draw a U-shaped arrow on the canvas.

        Args:
            xy: Center coordinate tuple (x, y).
            width: Width of U-shape.
            height: Height of U-shape.
            tail_width: Width of arrow tail.
            head_width: Width of arrow head.
            head_length: Length of arrow head.
            head: Arrow head type ("->", "<-", "<->").
            style: Style object.
        """
        style, _ = ShapeUtils.format_styles(
            style,
            None,
        )
        angle: Angle = style.angle if style.angle is not None else 0.0

        p1 = (xy[0] - width / 2, xy[1] + height / 2)
        p2 = (xy[0] - width / 2, xy[1] - height / 2)
        p3 = (xy[0] + width / 2, xy[1] - height / 2)
        p4 = (xy[0] + width / 2, xy[1] + height / 2)

        xys = [p1, p2, p3, p4]
        if angle != 0:
            xys = get_rotated_points(xys=xys, center=xy, angle=angle)

        self.arrow_polyline(
            xys=xys,
            tail_width=tail_width,
            head_width=head_width,
            head_length=head_length,
            head=head,
            style=style,
        )

    @validate_call
    def chevron(
        self,
        xy: Coordinate,
        width: PosFloat,
        height: PosFloat,
        corner_angle: Angle90,
        mirror: bool = False,
        *,
        style: Style,
        text: str = "",
        text_style: Style | None = None,
    ) -> None:
        """Draw a chevron (arrow-head block) shape on the canvas.

        Args:
            xy: Bottom-left coordinate tuple (x, y).
            width: Width of chevron.
            height: Height of chevron.
            corner_angle: Angle of the arrowhead point.
            mirror: Whether to mirror chevron horizontally.
            style: Style object.
            text: Text to display inside shape.
            text_style: Style object for text or None.
        """
        style, text_style = ShapeUtils.format_styles(
            style,
            text_style,
        )
        path_points = build_chevron_points(
            width=width,
            height=height,
            corner_angle=corner_angle,
            mirror=mirror,
            shape_r=style.shape_r,
        )

        self.shape(
            xy=xy,
            path_points=path_points,
            style=style,
            text=text,
            text_style=text_style,
        )


__all__ = [
    "ArrowPolylineHelper",
    "CanvasShapeArrowFeature",
]
