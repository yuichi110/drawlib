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

from typing import Any, ClassVar, Literal

from pydantic import BaseModel, ConfigDict, ValidationError

from drawlib._core.l2_types import (
    Alpha,
    Angle,
    Coordinate,
    Font,
    HAlign,
    IconStyle,
    LineStyle,
    PosFloat,
    Size,
    VAlign,
)
from drawlib._core.l3_colors import Color, ColorType
from drawlib._core.l3_fonts import Font as FontEnum

SupportType = Literal["shape", "line", "text", "icon", "image"]
ALL_SUPPORTS: frozenset[SupportType] = frozenset({"shape", "line", "text", "icon", "image"})


def _infer_supports(data: dict[str, Any]) -> frozenset[SupportType]:
    """Infer supported targets based on populated attributes in data.

    Only targets whose mandatory attributes are all provided will be included.

    Args:
        data: Attribute dictionary for Style.

    Returns:
        frozenset[SupportType]: Inferred set of supported targets.
    """
    supports: set[SupportType] = set()
    if (
        data.get("shape_fill_color") is not None
        and data.get("shape_line_color") is not None
        and data.get("shape_line_width") is not None
    ):
        supports.add("shape")
    if data.get("line_color") is not None and data.get("line_width") is not None:
        supports.add("line")
    if (
        data.get("text_color") is not None
        and data.get("text_size") is not None
        and data.get("text_font") is not None
    ):
        supports.add("text")
    if data.get("icon_color") is not None:
        supports.add("icon")
    if any(k.startswith("image_") and data.get(k) is not None for k in data):
        supports.add("image")
    return frozenset(supports)


class Style(BaseModel):
    """Immutable universal style model with explicit target support declaration."""

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
        validate_assignment=True,
    )

    # --- Class Constants ---
    Transparent: ClassVar[Style]

    # --- Target Declaration ---
    supports: frozenset[SupportType] = frozenset()

    def __init__(self, **data: Any) -> None:  # noqa: ANN401
        if "supports" not in data or data["supports"] is None:
            data["supports"] = _infer_supports(data)
        elif not isinstance(data["supports"], frozenset):
            data["supports"] = frozenset(data["supports"])
        try:
            super().__init__(**data)
        except ValidationError as e:
            raise ValueError(str(e)) from e

        self._validate_invariants()

    def _validate_invariants(self) -> None:
        """Validate that all targets declared in supports have required attributes populated.

        Raises:
            ValueError: If a declared target lacks mandatory attributes.
        """
        if "shape" in self.supports:
            missing = [
                k
                for k in ("shape_fill_color", "shape_line_color", "shape_line_width")
                if getattr(self, k) is None
            ]
            if missing:
                raise ValueError(
                    f"Style declares 'shape' support, but required attributes {missing} are None."
                )

        if "line" in self.supports:
            missing = [
                k
                for k in ("line_color", "line_width")
                if getattr(self, k) is None
            ]
            if missing:
                raise ValueError(
                    f"Style declares 'line' support, but required attributes {missing} are None."
                )

        if "text" in self.supports:
            missing = [
                k
                for k in ("text_color", "text_size", "text_font")
                if getattr(self, k) is None
            ]
            if missing:
                raise ValueError(
                    f"Style declares 'text' support, but required attributes {missing} are None."
                )

        if "icon" in self.supports:
            if self.icon_color is None:
                raise ValueError(
                    "Style declares 'icon' support, but required attribute 'icon_color' is None."
                )

    # --- Shape Properties (rectangle, circle, polygon, etc.) ---
    shape_fill_color: ColorType | None = None
    shape_line_color: ColorType | None = None
    shape_line_width: PosFloat | None = None
    shape_line_style: LineStyle | None = None

    # --- Line / Arrow Properties (line, lines, arrow, bezier, etc.) ---
    line_color: ColorType | None = None
    line_width: PosFloat | None = None
    line_style: LineStyle | None = None
    line_arrow_head_fill: bool | None = None
    line_arrow_head_scale: PosFloat | None = None

    # --- Text Properties (text, text_vertical, embedded shape text) ---
    text_color: ColorType | None = None
    text_size: Size | None = None
    text_font: Font | None = None
    text_flip: bool | None = None
    text_line_spacing: PosFloat | None = None
    text_bg_fill_color: ColorType | None = None
    text_bg_line_color: ColorType | None = None
    text_bg_line_width: PosFloat | None = None
    text_bg_line_style: LineStyle | None = None

    # --- Icon Properties (phosphor, font_icon, gcp) ---
    icon_color: ColorType | None = None
    icon_style: IconStyle | None = None

    # --- Image Properties (image) ---
    image_tint_color: ColorType | None = None
    image_border_color: ColorType | None = None
    image_border_width: PosFloat | None = None
    image_border_style: LineStyle | None = None

    # --- Offset & Transform Properties (halign, valign, xy_shift, xy_abs_shift, angle, alpha) ---
    halign: HAlign | None = None
    valign: VAlign | None = None
    xy_shift: Coordinate | None = None
    xy_abs_shift: Coordinate | None = None
    angle: Angle | None = None
    alpha: Alpha | None = None

    def patch(
        self,
        other: Style | None = None,
        *,
        supports: frozenset[SupportType] | set[SupportType] | list[SupportType] | None = None,
        # Shape Properties
        shape_fill_color: ColorType | None = None,
        shape_line_color: ColorType | None = None,
        shape_line_width: PosFloat | None = None,
        shape_line_style: LineStyle | None = None,
        # Line Properties
        line_color: ColorType | None = None,
        line_width: PosFloat | None = None,
        line_style: LineStyle | None = None,
        line_arrow_head_fill: bool | None = None,
        line_arrow_head_scale: PosFloat | None = None,
        # Text Properties
        text_color: ColorType | None = None,
        text_size: Size | None = None,
        text_font: Font | None = None,
        text_flip: bool | None = None,
        text_line_spacing: PosFloat | None = None,
        text_bg_fill_color: ColorType | None = None,
        text_bg_line_color: ColorType | None = None,
        text_bg_line_width: PosFloat | None = None,
        text_bg_line_style: LineStyle | None = None,
        # Icon Properties
        icon_color: ColorType | None = None,
        icon_style: IconStyle | None = None,
        # Image Properties
        image_tint_color: ColorType | None = None,
        image_border_color: ColorType | None = None,
        image_border_width: PosFloat | None = None,
        image_border_style: LineStyle | None = None,
        # Offset & Transform Properties
        halign: HAlign | None = None,
        valign: VAlign | None = None,
        xy_shift: Coordinate | None = None,
        xy_abs_shift: Coordinate | None = None,
        angle: Angle | None = None,
        alpha: Alpha | None = None,
    ) -> Style:
        """Return a new Style instance with updated attributes.

        Args:
            other: Another Style whose non-None attributes will be applied first.
            supports: Supported target declaration (shape, line, text, icon, image).
            shape_fill_color: Fill color for shapes.
            shape_line_color: Border line color for shapes.
            shape_line_width: Border line width for shapes.
            shape_line_style: Border line style for shapes.
            line_color: Stroke color for lines.
            line_width: Stroke width for lines.
            line_style: Stroke style for lines.
            line_arrow_head_fill: Whether arrowhead is filled.
            line_arrow_head_scale: Arrowhead scale multiplier.
            text_color: Font color for text.
            text_size: Font size for text.
            text_font: Font family for text.
            text_flip: Whether text is flipped horizontally.
            text_line_spacing: Line spacing multiplier for multi-line text.
            text_bg_fill_color: Background box fill color for text.
            text_bg_line_color: Background box border line color for text.
            text_bg_line_width: Background box border line width for text.
            text_bg_line_style: Background box border line style for text.
            icon_color: Color for icons.
            icon_style: Icon style variant.
            image_tint_color: Tint color for images.
            image_border_color: Border line color for images.
            image_border_width: Border line width for images.
            image_border_style: Border line style for images.
            halign: Horizontal alignment ("left", "center", "right").
            valign: Vertical alignment ("bottom", "center", "top").
            xy_shift: Relative XY coordinate shift.
            xy_abs_shift: Absolute XY coordinate shift.
            angle: Rotation angle in degrees.
            alpha: Overall opacity (0.0 = transparent, 1.0 = opaque).

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
        if supports is not None:
            merged["supports"] = frozenset(supports)
        else:
            inferred = _infer_supports(merged)
            combined = set(self.supports)
            if other is not None and other.supports:
                combined.update(other.supports)
            if combined & inferred:
                merged["supports"] = frozenset(combined & inferred)
            else:
                merged["supports"] = inferred
        return Style(**merged)

    def validate_for(self, target: SupportType) -> None:
        """Validate that this Style supports the specified drawing target.

        Args:
            target: Drawing target to validate against ('shape', 'line', 'text', 'icon', 'image').

        Raises:
            ValueError: If target is not in self.supports.
        """
        if target not in self.supports:
            raise ValueError(f"Style cannot be used for {target}. Declared supports: {set(self.supports)}.")


Style.Transparent = Style(
    supports=ALL_SUPPORTS,
    shape_fill_color=Color(0, 0, 0, 0.0),
    shape_line_color=Color(0, 0, 0, 0.0),
    shape_line_width=0.0,
    shape_line_style="solid",
    line_color=Color(0, 0, 0, 0.0),
    line_width=0.0,
    line_style="solid",
    text_color=Color(0, 0, 0, 0.0),
    text_size=12.0,
    text_font=FontEnum.SANSSERIF_REGULAR,
    icon_color=Color(0, 0, 0, 0.0),
    icon_style="regular",
    alpha=0.0,
)


__all__ = [
    "ALL_SUPPORTS",
    "Style",
    "SupportType",
]
