# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Style models implementation module."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, ValidationError

from drawlib._core.l2_types import (
    Alpha,
    Angle,
    ColorType,
    Coordinate,
    Font,
    HAlign,
    IconStyle,
    LineStyle,
    PosFloat,
    Size,
    VAlign,
)


class Style(BaseModel):
    """Immutable universal style model for drawlib."""

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
        validate_assignment=True,
    )

    def __init__(self, **data: Any) -> None:  # noqa: ANN401
        try:
            super().__init__(**data)
        except ValidationError as e:
            raise ValueError(str(e)) from e

    # --- Shape Properties (rectangle, circle, polygon, etc.) ---
    shape_fill_color: ColorType | None = None
    shape_fill_alpha: Alpha | None = None
    shape_line_color: ColorType | None = None
    shape_line_width: PosFloat | None = None
    shape_line_style: LineStyle | None = None

    # --- Line / Arrow Properties (line, lines, arrow, bezier, etc.) ---
    line_color: ColorType | None = None
    line_width: PosFloat | None = None
    line_style: LineStyle | None = None
    line_alpha: Alpha | None = None
    line_arrow_head_fill: bool | None = None
    line_arrow_head_scale: PosFloat | None = None

    # --- Text Properties (text, text_vertical, embedded shape text) ---
    text_color: ColorType | None = None
    text_size: Size | None = None
    text_font: Font | None = None
    text_halign: HAlign | None = None
    text_valign: VAlign | None = None
    text_angle: Angle | None = None
    text_flip: bool | None = None
    text_xy_shift: Coordinate | None = None
    text_xy_abs_shift: Coordinate | None = None
    text_bg_fill_color: ColorType | None = None
    text_bg_fill_alpha: Alpha | None = None
    text_bg_line_color: ColorType | None = None
    text_bg_line_width: PosFloat | None = None
    text_bg_line_style: LineStyle | None = None

    # --- Icon Properties (phosphor, font_icon, gcp) ---
    icon_color: ColorType | None = None
    icon_style: IconStyle | None = None

    # --- Image Properties (image) ---
    image_tint_color: ColorType | None = None
    image_alpha: Alpha | None = None
    image_border_color: ColorType | None = None
    image_border_width: PosFloat | None = None
    image_border_style: LineStyle | None = None

    def patch(
        self,
        other: Style | None = None,
        *,
        # Shape Properties
        shape_fill_color: ColorType | None = None,
        shape_fill_alpha: Alpha | None = None,
        shape_line_color: ColorType | None = None,
        shape_line_width: PosFloat | None = None,
        shape_line_style: LineStyle | None = None,
        # Line Properties
        line_color: ColorType | None = None,
        line_width: PosFloat | None = None,
        line_style: LineStyle | None = None,
        line_alpha: Alpha | None = None,
        line_arrow_head_fill: bool | None = None,
        line_arrow_head_scale: PosFloat | None = None,
        # Text Properties
        text_color: ColorType | None = None,
        text_size: Size | None = None,
        text_font: Font | None = None,
        text_halign: HAlign | None = None,
        text_valign: VAlign | None = None,
        text_angle: Angle | None = None,
        text_flip: bool | None = None,
        text_xy_shift: Coordinate | None = None,
        text_xy_abs_shift: Coordinate | None = None,
        text_bg_fill_color: ColorType | None = None,
        text_bg_fill_alpha: Alpha | None = None,
        text_bg_line_color: ColorType | None = None,
        text_bg_line_width: PosFloat | None = None,
        text_bg_line_style: LineStyle | None = None,
        # Icon Properties
        icon_color: ColorType | None = None,
        icon_style: IconStyle | None = None,
        # Image Properties
        image_tint_color: ColorType | None = None,
        image_alpha: Alpha | None = None,
        image_border_color: ColorType | None = None,
        image_border_width: PosFloat | None = None,
        image_border_style: LineStyle | None = None,
    ) -> Style:
        """Return a new Style instance with updated attributes.

        Args:
            other: Another Style whose non-None attributes will be applied first.
            shape_fill_color: Fill color for shapes.
            shape_fill_alpha: Alpha transparency for shape fill.
            shape_line_color: Border line color for shapes.
            shape_line_width: Border line width for shapes.
            shape_line_style: Border line style for shapes.
            line_color: Stroke color for lines.
            line_width: Stroke width for lines.
            line_style: Stroke style for lines.
            line_alpha: Alpha transparency for lines.
            line_arrow_head_fill: Whether arrowhead is filled.
            line_arrow_head_scale: Arrowhead scale multiplier.
            text_color: Font color for text.
            text_size: Font size for text.
            text_font: Font family for text.
            text_halign: Horizontal alignment for text.
            text_valign: Vertical alignment for text.
            text_angle: Rotation angle for text.
            text_flip: Whether text is flipped horizontally.
            text_xy_shift: Relative XY coordinate shift.
            text_xy_abs_shift: Absolute XY coordinate shift.
            text_bg_fill_color: Background box fill color for text.
            text_bg_fill_alpha: Background box fill alpha for text.
            text_bg_line_color: Background box border line color for text.
            text_bg_line_width: Background box border line width for text.
            text_bg_line_style: Background box border line style for text.
            icon_color: Color for icons.
            icon_style: Icon style variant.
            image_tint_color: Tint color for images.
            image_alpha: Alpha transparency for images.
            image_border_color: Border line color for images.
            image_border_width: Border line width for images.
            image_border_style: Border line style for images.

        Returns:
            Style: New Style instance with updated attributes.
        """
        updates: dict[str, Any] = {}
        if other is not None:
            updates.update({k: v for k, v in other.model_dump().items() if v is not None})
        updates.update(
            {
                k: v
                for k, v in locals().items()
                if k not in {"self", "other", "updates"} and v is not None
            }
        )
        merged = {**self.__dict__, **updates}
        return Style.model_validate(merged)
