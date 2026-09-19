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

from typing import Annotated, Any, TypeVar, cast

from pydantic import BaseModel, ConfigDict, InstanceOf, ValidationError, model_validator

from drawlib._core.l1_core import guarded
from drawlib._core.l2_types import (
    TypeAlpha,
    TypeAngle,
    TypeAngle90,
    TypeColor,
    TypeColorRGB,
    TypeCoordinate,
    TypeFont,
    TypeHAlign,
    TypeIconStyle,
    TypeLineStyle,
    TypePosFloat,
    TypeSize,
    TypeVAlign,
)
from drawlib._core.l3_fonts import FontSourceCode

T = TypeVar("T", bound="_StyleModel")


class _StyleModel(BaseModel):
    """Base class for all style models."""

    model_config = ConfigDict(
        extra="forbid",
        validate_assignment=True,
    )

    def __init__(self, **data: Any) -> None:  # noqa: ANN401
        try:
            super().__init__(**data)
        except ValidationError as e:
            raise ValueError(str(e)) from e

    @guarded
    def copy(self: T) -> T:
        """Create and return a deep copy of the style object."""
        return self.model_copy(deep=True)

    @guarded
    def merge(self: T, style: T) -> T:
        """Merge the provided style with this object's style.

        This method takes the given `style` and merges it with the instance's
        style attributes. The `style` parameter is treated as the primary style,
        and any attributes that are `None` in the primary style will be replaced
        with the corresponding attributes from this object's style.

        Args:
            style (T): The primary style to be merged with this object's style.

        Returns:
            T: A new instance with merged attributes.
        """
        if not isinstance(style, _StyleModel):
            raise ValueError(f'Arg "style" requires Style or _StyleModel, but "{type(style)}" is given.')

        # We avoid model_dump() because it converts nested dataclasses (like FontFile) to dicts.
        # Using __dict__ preserves the original object instances.
        update_data = {k: v for k, v in style.__dict__.items() if v is not None}
        return self.model_copy(update=update_data)


class Style(_StyleModel):
    """Universal declarative style class for all drawlib elements."""

    # --- Fill Properties ---
    fill_color: TypeColor | None = None
    fill_alpha: TypeAlpha | None = None

    # --- Line / Border Properties ---
    line_color: TypeColor | None = None
    line_width: TypePosFloat | None = None
    line_style: TypeLineStyle | None = None

    # --- Text Properties ---
    text_color: TypeColor | None = None
    text_size: TypeSize | None = None
    text_font: TypeFont | None = None
    text_halign: TypeHAlign | None = None
    text_valign: TypeVAlign | None = None
    text_angle: TypeAngle | None = None
    text_flip: bool | None = None
    text_xy_shift: TypeCoordinate | None = None
    text_xy_abs_shift: TypeCoordinate | None = None

    # --- Text Background Box Properties ---
    text_bg_fill_color: TypeColor | None = None
    text_bg_fill_alpha: TypeAlpha | None = None
    text_bg_line_color: TypeColor | None = None
    text_bg_line_width: TypePosFloat | None = None
    text_bg_line_style: TypeLineStyle | None = None

    # --- Arrowhead Properties ---
    arrow_head_fill: bool | None = None
    arrow_head_scale: TypePosFloat | None = None

    # --- Icon Properties ---
    icon_style: TypeIconStyle | None = None

    def get_fill_color(self) -> TypeColor | None:
        """Get fill color."""
        return self.fill_color

    def get_line_color(self) -> TypeColor | None:
        """Get line/border color."""
        return self.line_color

    def get_line_width(self) -> TypePosFloat | None:
        """Get line width."""
        return self.line_width

    def get_line_style(self) -> TypeLineStyle | None:
        """Get line style."""
        return self.line_style

    def get_icon_style(self) -> TypeIconStyle | None:
        """Get icon style."""
        return self.icon_style


# Type aliases for backward compatibility
IconStyle = Style
ImageStyle = Style
LineStyle = Style
ShapeStyle = Style
ShapeTextStyle = Style
TextStyle = Style
