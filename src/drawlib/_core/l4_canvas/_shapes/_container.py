# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Canvas 3D container, flow, and grouping shape feature implementation module."""

from __future__ import annotations

from matplotlib.patches import PathPatch
from pydantic import validate_call

from drawlib._core.l2_types import (
    Angle,
    BraceDirection,
    BraceSymbol,
    CloudVariant,
    Coordinate,
    DocumentVariant,
    FunnelVariant,
    PosFloat,
    PosInt,
    Ratio,
)
from drawlib._core.l3_styles import Style
from drawlib._core.l4_canvas._shapes._container_builders import (
    build_brace_path,
    build_cloud_path,
    build_cube_patches,
    build_cylinder_patches,
    build_document_patches,
    build_funnel_patches,
    format_brace_styles,
    get_brace_stroke_options,
)
from drawlib._core.l4_canvas._shapes._polygon import CanvasShapePolygonFeature
from drawlib._core.l4_canvas._shapes._shape_utils import ShapeUtils


class CanvasShapeContainerFeature(CanvasShapePolygonFeature):
    """Canvas 3D container, flow, and grouping shape feature implementation module.

    Provides cylinder, cube, document, funnel, cloud, and brace shapes.
    """

    def __init__(self) -> None:
        """Initializes an instance of CanvasShapeContainerFeature."""
        super().__init__()

    @validate_call
    def cylinder(
        self,
        xy: Coordinate,
        width: PosFloat,
        height: PosFloat,
        *,
        style: Style,
        disks: PosInt = 1,
        text: str = "",
        text_style: Style | None = None,
    ) -> None:
        """Draw a 3D cylinder shape on the canvas.

        Args:
            xy: Center coordinates (x, y) of the cylinder.
            width: Width of the cylinder.
            height: Height of the cylinder.
            style: Style object (required).
            disks: Number of stacked disks (default is 1).
            text: Text to display inside shape.
            text_style: Style object for text.
        """
        style, text_style = ShapeUtils.format_styles(
            style,
            text_style,
        )
        if width <= 0 or height <= 0:
            raise ValueError(f"width and height must be positive, but got width={width}, height={height}.")
        if disks < 1:
            raise ValueError(f"disks must be >= 1, but got {disks}.")

        xy, angle, style = ShapeUtils.prepare_centered_shape(xy, width, height, style)
        patches = build_cylinder_patches(
            xy=xy,
            width=width,
            height=height,
            disks=disks,
            angle=angle,
            style=style,
        )
        ShapeUtils.append_patches_and_text(
            artists=self._artists,
            patches=patches,
            style=style,
            text=text,
            text_style=text_style,
            text_xy=xy,
            angle=angle,
        )

    @validate_call
    def cube(
        self,
        xy: Coordinate,
        width: PosFloat,
        height: PosFloat,
        *,
        depth_ratio: Ratio | None = None,
        style: Style,
        text: str = "",
        text_style: Style | None = None,
    ) -> None:
        """Draw a 3D cube or rectangular box shape on the canvas.

        Args:
            xy: Center coordinates tuple (x, y).
            width: Outer width of the cube bounding box.
            height: Outer height of the cube bounding box.
            depth_ratio: Optional 3D depth fraction in (0.0, 1.0) relative to min(width, height).
            style: Style object (required).
            text: Text to display on the front face of the cube.
            text_style: Style object for text.

        Raises:
            ValueError: If width, height, or depth_ratio are out of valid bounds.
        """
        style, text_style = ShapeUtils.format_styles(style, text_style)
        if width <= 0.0 or height <= 0.0:
            raise ValueError("width and height must be positive.")
        if depth_ratio is not None and not (0.0 < depth_ratio < 1.0):
            raise ValueError("depth_ratio must be strictly between 0.0 and 1.0.")

        xy, angle, style = ShapeUtils.prepare_centered_shape(xy, width, height, style)
        patches, text_xy = build_cube_patches(
            xy=xy,
            width=width,
            height=height,
            depth_ratio=depth_ratio,
            angle=angle,
            style=style,
        )
        ShapeUtils.append_patches_and_text(
            artists=self._artists,
            patches=patches,
            style=style,
            text=text,
            text_style=text_style,
            text_xy=text_xy,
            angle=angle,
        )

    @validate_call
    def document(
        self,
        xy: Coordinate,
        width: PosFloat,
        height: PosFloat,
        *,
        variant: DocumentVariant = "wave",
        stacked: PosInt = 1,
        wave_ratio: Ratio | None = None,
        fold_ratio: Ratio | None = None,
        style: Style,
        text: str = "",
        text_style: Style | None = None,
    ) -> None:
        """Draw a wavy-bottom or folded-corner document shape on the canvas.

        Args:
            xy: Center coordinates tuple (x, y).
            width: Outer width of the document bounding box.
            height: Outer height of the document bounding box.
            variant: Document silhouette ("wave", "standard", "folded", "page", "note",
                "double_wave", "snippet", "folded_wave", "report").
            stacked: Number of stacked document sheets (default is 1).
            wave_ratio: Optional wave amplitude ratio in (0.0, 1.0).
            fold_ratio: Optional top-right corner fold size ratio in (0.0, 1.0).
            style: Style object (required).
            text: Text to display on the front document sheet.
            text_style: Style object for text.

        Raises:
            ValueError: If dimensions, stacked count, or ratios are out of valid bounds.
        """
        style, text_style = ShapeUtils.format_styles(style, text_style)
        if width <= 0.0 or height <= 0.0:
            raise ValueError("width and height must be positive.")
        if stacked < 1:
            raise ValueError("stacked must be >= 1.")
        if wave_ratio is not None and not (0.0 < wave_ratio < 1.0):
            raise ValueError("wave_ratio must be strictly between 0.0 and 1.0.")
        if fold_ratio is not None and not (0.0 < fold_ratio < 1.0):
            raise ValueError("fold_ratio must be strictly between 0.0 and 1.0.")

        xy, angle, style = ShapeUtils.prepare_centered_shape(xy, width, height, style)
        patches, text_xy = build_document_patches(
            xy=xy,
            width=width,
            height=height,
            variant=variant,
            stacked=stacked,
            wave_ratio=wave_ratio,
            fold_ratio=fold_ratio,
            angle=angle,
            style=style,
        )
        ShapeUtils.append_patches_and_text(
            artists=self._artists,
            patches=patches,
            style=style,
            text=text,
            text_style=text_style,
            text_xy=text_xy,
            angle=angle,
        )

    @validate_call
    def funnel(
        self,
        xy: Coordinate,
        width: PosFloat,
        height: PosFloat,
        *,
        variant: FunnelVariant = "standard",
        neck_width_ratio: Ratio | None = None,
        neck_height_ratio: Ratio | None = None,
        style: Style,
        text: str = "",
        text_style: Style | None = None,
    ) -> None:
        """Draw a filter funnel shape on the canvas.

        Args:
            xy: Center coordinates tuple (x, y).
            width: Outer width of the funnel top opening.
            height: Total height of the funnel.
            variant: Funnel silhouette ("standard", "flat", "3d", "cylinder", "curved").
            neck_width_ratio: Optional bottom spout width ratio in (0.0, 1.0).
            neck_height_ratio: Optional bottom spout height ratio in (0.0, 1.0).
            style: Style object (required).
            text: Text to display inside the funnel.
            text_style: Style object for text.
        """
        ShapeUtils.validate_hole_ratio(neck_width_ratio)
        ShapeUtils.validate_hole_ratio(neck_height_ratio)
        style, text_style = ShapeUtils.format_styles(style, text_style)
        xy, angle, style = ShapeUtils.prepare_centered_shape(xy, width, height, style)
        patches, text_xy = build_funnel_patches(
            xy=xy,
            width=width,
            height=height,
            variant=variant,
            neck_width_ratio=neck_width_ratio,
            neck_height_ratio=neck_height_ratio,
            angle=angle,
            style=style,
        )
        ShapeUtils.append_patches_and_text(
            artists=self._artists,
            patches=patches,
            style=style,
            text=text,
            text_style=text_style,
            text_xy=text_xy,
            angle=angle,
        )

    @validate_call
    def cloud(
        self,
        xy: Coordinate,
        width: PosFloat,
        height: PosFloat,
        *,
        variant: CloudVariant = "standard",
        bump_ratio: Ratio | None = None,
        style: Style,
        text: str = "",
        text_style: Style | None = None,
    ) -> None:
        """Draw a cloud shape on the canvas.

        Args:
            xy: Center coordinates tuple (x, y).
            width: Width of the cloud bounding box.
            height: Height of the cloud bounding box.
            variant: Cloud silhouette variant ("standard", "flat", "fluffy", "simple").
            bump_ratio: Optional bulge depth ratio in (0.0, 1.0).
            style: Style object (required).
            text: Text to display inside shape.
            text_style: Style object for text.

        Raises:
            ValueError: If width, height, or bump_ratio are out of valid bounds.
        """
        style, text_style = ShapeUtils.format_styles(style, text_style)
        if width <= 0.0 or height <= 0.0:
            raise ValueError("width and height must be positive.")
        if bump_ratio is not None and not (0.0 < bump_ratio < 1.0):
            raise ValueError("bump_ratio must be strictly between 0.0 and 1.0.")

        xy, angle, style = ShapeUtils.prepare_centered_shape(xy, width, height, style)
        path = build_cloud_path(
            xy=xy,
            width=width,
            height=height,
            variant=variant,
            bump_ratio=bump_ratio,
            angle=angle,
        )
        ShapeUtils.append_path_and_text(
            artists=self._artists,
            path=path,
            style=style,
            text=text,
            text_style=text_style,
            text_xy=xy,
            angle=angle,
        )

    @validate_call
    def brace(
        self,
        xy: Coordinate,
        width: PosFloat,
        height: PosFloat,
        *,
        symbol: BraceSymbol = "{",
        direction: BraceDirection | None = None,
        tip_ratio: Ratio | None = None,
        tip_position_ratio: Ratio | None = None,
        style: Style,
        text: str = "",
        text_style: Style | None = None,
    ) -> None:
        """Draw a curly, square, or round brace shape on the canvas.

        Args:
            xy: Center coordinates tuple (x, y).
            width: Width of the brace bounding box.
            height: Height of the brace bounding box.
            symbol: Brace symbol ("{", "}", "{}", "curly", "[", "]", "[]", "square", "(", ")", "()", "round").
            direction: Orientation direction ("left", "right", "top", "bottom") or None.
            tip_ratio: Optional center tip depth ratio in (0.0, 1.0) for curly braces.
            tip_position_ratio: Optional center tip span position ratio in (0.0, 1.0) for curly braces.
            style: Style object (controls line_width, line_color, line_style, shape_r, and angle).
            text: Text to display inside shape.
            text_style: Style object for text.

        Raises:
            ValueError: If width, height, tip_ratio, or tip_position_ratio are out of valid bounds.
        """
        style, text_style = format_brace_styles(style, text_style)
        if width <= 0.0 or height <= 0.0:
            raise ValueError("width and height must be positive.")
        if tip_ratio is not None and not (0.0 < tip_ratio < 1.0):
            raise ValueError("tip_ratio must be strictly between 0.0 and 1.0.")
        if tip_position_ratio is not None and not (0.0 < tip_position_ratio < 1.0):
            raise ValueError("tip_position_ratio must be strictly between 0.0 and 1.0.")

        angle: Angle = style.angle if style.angle is not None else 0.0
        xy, style = ShapeUtils.apply_alignment(
            xy=xy,
            width=width,
            height=height,
            angle=angle,
            style=style,
            is_default_center=True,
        )

        shape_r_scalar = style.shape_r if isinstance(style.shape_r, (int, float)) else None
        path = build_brace_path(
            xy=xy,
            width=width,
            height=height,
            symbol=symbol,
            direction=direction,
            tip_ratio=tip_ratio,
            tip_position_ratio=tip_position_ratio,
            shape_r=shape_r_scalar,
            angle=angle,
        )
        options = get_brace_stroke_options(style)
        ShapeUtils.append_patches_and_text(
            artists=self._artists,
            patches=[PathPatch(path=path, **options)],
            style=style,
            text=text,
            text_style=text_style,
            text_xy=xy,
            angle=angle,
        )


__all__ = [
    "CanvasShapeContainerFeature",
]
