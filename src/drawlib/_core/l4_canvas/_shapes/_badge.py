# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Canvas callout, badge, and status indicator shape feature implementation module."""

from __future__ import annotations

from pydantic import validate_call

from drawlib._core.l2_types import (
    CheckmarkVariant,
    Coordinate,
    ExplosionVariant,
    ForbiddenVariant,
    PinVariant,
    PosFloat,
    Ratio,
    RibbonVariant,
    ShieldVariant,
    TagVariant,
    TailEdge,
)
from drawlib._core.l3_styles import Style
from drawlib._core.l4_canvas._shapes._badge_builders import (
    build_checkmark_path,
    build_explosion_path,
    build_forbidden_path,
    build_pin_path_and_center,
    build_ribbon_patches,
    build_shield_path,
    build_tag_path_and_center,
)
from drawlib._core.l4_canvas._shapes._polygon import CanvasShapePolygonFeature
from drawlib._core.l4_canvas._shapes._shape_utils import ShapeUtils


class CanvasShapeBadgeFeature(CanvasShapePolygonFeature):
    """Canvas callout, badge, and status indicator shape feature implementation module.

    Provides bubblespeech, pin, tag, ribbon, shield, forbidden, checkmark, and explosion shapes.
    """

    def __init__(self) -> None:
        """Initializes an instance of CanvasShapeBadgeFeature."""
        super().__init__()

    @validate_call
    def bubblespeech(
        self,
        xy: Coordinate,
        width: PosFloat,
        height: PosFloat,
        tail_edge: TailEdge,
        tail_start_ratio: Ratio,
        tail_vertex_xy: Coordinate,
        tail_end_ratio: Ratio,
        *,
        style: Style,
        text: str = "",
        text_style: Style | None = None,
    ) -> None:
        """Draw a speech bubble shape on the canvas.

        Args:
            xy: The (x, y) coordinates of the bottom-left corner of the bubble body.
            width: The width of the bubble body.
            height: The height of the bubble body.
            tail_edge: The edge ("left", "top", "right", "bottom") where the tail originates.
            tail_start_ratio: Ratio (between 0.0 and 1.0) along the edge where the tail begins.
            tail_vertex_xy: The (x, y) target coordinates pointing to the vertex of the tail.
            tail_end_ratio: Ratio (between 0.0 and 1.0) along the edge where the tail ends.
            style: The Style of the speech bubble shape (required).
            text: Optional text to display inside the bubble. Defaults to an empty string.
            text_style: Optional Style of the text.

        Raises:
            ValueError: If tail_start_ratio is greater than or equal to tail_end_ratio.
        """
        if tail_start_ratio >= tail_end_ratio:
            raise ValueError("tail_start_ratio must be smaller than tail_end_ratio.")

        x, y = xy
        xys: list[Coordinate] = [(x, y)]  # left bottom

        if tail_edge == "left":
            xys.append((x, y + height * tail_start_ratio))
            xys.append(tail_vertex_xy)
            xys.append((x, y + height * tail_end_ratio))
        xys.append((x, y + height))  # left top

        if tail_edge == "top":
            xys.append((x + width * tail_start_ratio, y + height))
            xys.append(tail_vertex_xy)
            xys.append((x + width * tail_end_ratio, y + height))
        xys.append((x + width, y + height))  # right top

        if tail_edge == "right":
            xys.append((x + width, y + height * tail_end_ratio))
            xys.append(tail_vertex_xy)
            xys.append((x + width, y + height * tail_start_ratio))
        xys.append((x + width, y))  # right bottom

        if tail_edge == "bottom":
            xys.append((x + width * tail_end_ratio, y))
            xys.append(tail_vertex_xy)
            xys.append((x + width * tail_start_ratio, y))

        self.polygon(xys=xys, style=style.patch(shape_r=0.0))

        if text:
            center_x = x + width / 2.0
            center_y = y + height / 2.0
            effective_text_style = ShapeUtils.resolve_embedded_text_style(style, text_style)
            self._artists.append(
                ShapeUtils.get_shape_text(
                    xy=(center_x, center_y),
                    text=text,
                    angle=0.0,
                    style=effective_text_style,
                )
            )

    @validate_call
    def pin(
        self,
        xy: Coordinate,
        width: PosFloat,
        height: PosFloat,
        *,
        variant: PinVariant = "pointer",
        hole_ratio: Ratio | None = None,
        style: Style,
        text: str = "",
        text_style: Style | None = None,
    ) -> None:
        """Draw a callout pointer badge or map pin shape on the canvas.

        Args:
            xy: Center coordinates tuple (x, y).
            width: Width of the pin bounding box.
            height: Height of the pin bounding box.
            variant: Pin silhouette ("pointer", "standard", "teardrop", "drop", "pin", "badge").
            hole_ratio: Optional center circular hole ratio in (0.0, 1.0).
            style: Style object (required).
            text: Text to display centered inside the pin head.
            text_style: Style object for text.
        """
        ShapeUtils.validate_hole_ratio(hole_ratio)
        style, text_style = ShapeUtils.format_styles(style, text_style)
        xy, angle, style = ShapeUtils.prepare_centered_shape(xy, width, height, style)
        path, head_xy = build_pin_path_and_center(xy, width, height, variant, hole_ratio, angle)
        ShapeUtils.append_path_and_text(
            artists=self._artists,
            path=path,
            style=style,
            text=text,
            text_style=text_style,
            text_xy=head_xy,
            angle=angle,
        )

    @validate_call
    def tag(
        self,
        xy: Coordinate,
        width: PosFloat,
        height: PosFloat,
        *,
        variant: TagVariant = "angled",
        mirror: bool = False,
        hole_ratio: Ratio | None = None,
        style: Style,
        text: str = "",
        text_style: Style | None = None,
    ) -> None:
        """Draw a perforated label tag or badge shape on the canvas.

        Args:
            xy: Center coordinates tuple (x, y).
            width: Width of the tag bounding box.
            height: Height of the tag bounding box.
            variant: Tag silhouette ("angled", "standard", "chamfered", "beveled", "rounded").
            mirror: Whether to flip the tag tip direction horizontally.
            hole_ratio: Optional circular hole size ratio in (0.0, 1.0).
            style: Style object (required).
            text: Text to display on the tag body.
            text_style: Style object for text.
        """
        ShapeUtils.validate_hole_ratio(hole_ratio)
        style, text_style = ShapeUtils.format_styles(style, text_style)
        xy, angle, style = ShapeUtils.prepare_centered_shape(xy, width, height, style)
        path, text_xy = build_tag_path_and_center(
            xy=xy,
            width=width,
            height=height,
            variant=variant,
            mirror=mirror,
            hole_ratio=hole_ratio,
            shape_r=style.shape_r,
            angle=angle,
        )
        ShapeUtils.append_path_and_text(
            artists=self._artists,
            path=path,
            style=style,
            text=text,
            text_style=text_style,
            text_xy=text_xy,
            angle=angle,
        )

    @validate_call
    def ribbon(
        self,
        xy: Coordinate,
        width: PosFloat,
        height: PosFloat,
        *,
        variant: RibbonVariant = "down",
        tail_width_ratio: Ratio | None = None,
        drop_ratio: Ratio | None = None,
        style: Style,
        text: str = "",
        text_style: Style | None = None,
    ) -> None:
        """Draw a ribbon banner shape on the canvas.

        Args:
            xy: Center coordinates tuple (x, y).
            width: Outer width of the ribbon bounding box.
            height: Outer height of the ribbon bounding box.
            variant: Ribbon variant ("down", "standard", "up", "flat", "banner").
            tail_width_ratio: Optional side tail width fraction in (0.0, 1.0).
            drop_ratio: Optional vertical step drop fraction in (0.0, 1.0).
            style: Style object (required).
            text: Text to display on the front banner panel.
            text_style: Style object for text.
        """
        ShapeUtils.validate_hole_ratio(tail_width_ratio)
        ShapeUtils.validate_hole_ratio(drop_ratio)
        style, text_style = ShapeUtils.format_styles(style, text_style)
        xy, angle, style = ShapeUtils.prepare_centered_shape(xy, width, height, style)
        patches, text_xy = build_ribbon_patches(
            xy=xy,
            width=width,
            height=height,
            variant=variant,
            tail_width_ratio=tail_width_ratio,
            drop_ratio=drop_ratio,
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
    def shield(
        self,
        xy: Coordinate,
        width: PosFloat,
        height: PosFloat,
        *,
        variant: ShieldVariant = "classic",
        style: Style,
        text: str = "",
        text_style: Style | None = None,
    ) -> None:
        """Draw a security shield shape on the canvas.

        Args:
            xy: Center coordinates tuple (x, y).
            width: Width of the shield bounding box.
            height: Height of the shield bounding box.
            variant: Shield silhouette variant ("classic", "standard", "flat", "heater", "round").
            style: Style object (required).
            text: Text to display inside shape.
            text_style: Style object for text.
        """
        style, text_style = ShapeUtils.format_styles(style, text_style)
        xy, angle, style = ShapeUtils.prepare_centered_shape(xy, width, height, style)
        path = build_shield_path(xy, width, height, variant, angle)
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
    def forbidden(
        self,
        xy: Coordinate,
        radius: PosFloat,
        *,
        variant: ForbiddenVariant = "slash",
        thickness_ratio: Ratio | None = None,
        style: Style,
        text: str = "",
        text_style: Style | None = None,
    ) -> None:
        """Draw a forbidden or no-entry mark shape on the canvas.

        Args:
            xy: Center coordinates tuple (x, y).
            radius: Outer radius of the forbidden circle.
            variant: Visual variant ("slash", "standard", "backslash", "cross", "no_entry", "minus").
            thickness_ratio: Optional ring/bar thickness ratio in (0.0, 1.0).
            style: Style object (required).
            text: Text to display inside shape.
            text_style: Style object for text.
        """
        ShapeUtils.validate_hole_ratio(thickness_ratio)
        style, text_style = ShapeUtils.format_styles(style, text_style)
        width = radius * 2.0
        xy, angle, style = ShapeUtils.prepare_centered_shape(xy, width, width, style)
        path = build_forbidden_path(xy, radius, variant, thickness_ratio, angle)
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
    def checkmark(
        self,
        xy: Coordinate,
        width: PosFloat,
        height: PosFloat | None = None,
        *,
        variant: CheckmarkVariant = "standard",
        thickness_ratio: Ratio | None = None,
        style: Style,
        text: str = "",
        text_style: Style | None = None,
    ) -> None:
        """Draw a checkmark symbol or badge shape on the canvas.

        Args:
            xy: Center coordinates tuple (x, y).
            width: Width of the checkmark bounding box.
            height: Height of the checkmark bounding box (defaults to width when None).
            variant: Checkmark variant ("standard", "check", "circle", "solid_circle").
            thickness_ratio: Optional stroke thickness ratio in (0.0, 1.0).
            style: Style object (required).
            text: Text to display inside shape.
            text_style: Style object for text.
        """
        ShapeUtils.validate_hole_ratio(thickness_ratio)
        style, text_style = ShapeUtils.format_styles(style, text_style)
        eff_h = width if height is None else height
        xy, angle, style = ShapeUtils.prepare_centered_shape(xy, width, eff_h, style)
        path = build_checkmark_path(xy, width, eff_h, variant, thickness_ratio, style.shape_r, angle)
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
    def explosion(
        self,
        xy: Coordinate,
        width: PosFloat,
        height: PosFloat,
        *,
        variant: ExplosionVariant = "standard",
        style: Style,
        text: str = "",
        text_style: Style | None = None,
    ) -> None:
        """Draw an asymmetric explosion or impact burst shape on the canvas.

        Args:
            xy: Center coordinates tuple (x, y).
            width: Width of the explosion bounding box.
            height: Height of the explosion bounding box.
            variant: Explosion silhouette ("standard", "irregular", "heavy",
                "wild", "curved", "comic").
            style: Style object (required).
            text: Text to display inside shape.
            text_style: Style object for text.
        """
        style, text_style = ShapeUtils.format_styles(style, text_style)
        xy, angle, style = ShapeUtils.prepare_centered_shape(xy, width, height, style)
        path = build_explosion_path(
            xy=xy,
            width=width,
            height=height,
            variant=variant,
            shape_r=style.shape_r,
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


__all__ = [
    "CanvasShapeBadgeFeature",
]
