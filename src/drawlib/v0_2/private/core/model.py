# Copyright (c) 2024 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Style models implementation module."""

from __future__ import annotations

from typing import Annotated, Any, TypeVar

from pydantic import BaseModel, ConfigDict, InstanceOf, ValidationError, model_validator

from drawlib.v0_2.private.core.fonts import FontBase, FontFile, FontSourceCode
from drawlib.v0_2.private.types import (
    TypeAlpha,
    TypeAngle,
    TypeColorTuple,
    TypeCoordinate,
    TypeFont,
    TypeHAlign,
    TypeIconStyle,
    TypeLineStyle,
    TypePosFloat,
    TypeSize,
    TypeVAlign,
)
from drawlib.v0_2.private.util import error_handler

T = TypeVar("T", bound="_StyleModel")


class _StyleModel(BaseModel):
    """Base class for all style models."""

    model_config = ConfigDict(
        extra="forbid",
        validate_assignment=True,
        arbitrary_types_allowed=True,
        ignored_types=(FontBase, FontFile),
    )

    def __init__(self, **data: Any) -> None:
        try:
            super().__init__(**data)
        except ValidationError as e:
            raise ValueError(str(e)) from e

    @error_handler
    def copy(self: T) -> T:
        """Create and return a deep copy of the style object."""
        return self.model_copy(deep=True)

    @error_handler
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
        if not isinstance(style, self.__class__):
            raise ValueError(f'Arg "style" requires {self.__class__.__name__}. But "{type(style)}" is given.')

        # We avoid model_dump() because it converts nested dataclasses (like FontFile) to dicts.
        # Using __dict__ preserves the original object instances.
        update_data = {k: v for k, v in style.__dict__.items() if v is not None}
        return self.model_copy(update=update_data)


class IconStyle(_StyleModel):
    """Represents the styling attributes for icons in drawlib.

    Attributes:
        style (Literal["thin", "light", "regular", "bold", "fill"] | None):
            The visual style of the icon. Defaults to "regular".
        color (tuple[int, int, int] | tuple[int, int, int, float] | None):
            The color of the icon in RGB or RGBA format.
            If None, the default theme color is used.
        alpha (float | None): The transparency of the icon (0.0 to 1.0).
        halign (Literal["left", "center", "right"] | None):
            The horizontal alignment of the icon.
        valign (Literal["bottom", "center", "top"] | None):
            The vertical alignment of the icon.

    Methods:
        copy(): Create and return a deep copy of the style object.
        merge(style): Merge the provided style with this object's style.
            The provided `style` takes precedence; `None` attributes are
            filled by this instance's values.
    """

    style: TypeIconStyle | None = None
    color: TypeColorTuple | None = None
    alpha: TypeAlpha | None = None
    halign: TypeHAlign | None = None
    valign: TypeVAlign | None = None


class ImageStyle(_StyleModel):
    """Represents the styling attributes for images in drawlib.

    Attributes:
        halign (Literal["left", "center", "right"] | None):
            The horizontal alignment of the image.
        valign (Literal["bottom", "center", "top"] | None):
            The vertical alignment of the image.
        lwidth (float | None):
            The width of the outline (line) around the image.
        lstyle (Literal["solid", "dashed", "dotted", "dashdot"] | None):
            The style of the outline (line) around the image.
        lcolor (tuple[int, int, int] | tuple[int, int, int, float] | None):
            The color of the outline (line) around the image.
        fcolor (tuple[int, int, int] | tuple[int, int, int, float] | None):
            The fill color of the image.
        alpha (float | None):
            The transparency of the image.

    Methods:
        copy(): Create and return a deep copy of the style object.
        merge(style): Merge the provided style with this object's style.
            The provided `style` takes precedence; `None` attributes are
            filled by this instance's values.
    """

    halign: TypeHAlign | None = None
    valign: TypeVAlign | None = None
    lwidth: TypePosFloat | None = None
    lstyle: TypeLineStyle | None = None
    lcolor: TypeColorTuple | None = None
    fcolor: TypeColorTuple | None = None
    alpha: TypeAlpha | None = None


class LineStyle(_StyleModel):
    """Represents the styling attributes for lines in drawlib.

    Attributes:
        width (float | None):
            The width of the line.
        color (tuple[int, int, int] | tuple[int, int, int, float] | None):
            The color of the line.
        alpha (float | None):
            The transparency of the line.
        style (Literal["solid", "dashed", "dotted", "dashdot"] | None):
            The style of the line.
        ahfill (bool | None):
            Specifies whether the arrow heads at the ends of the line should be filled.
        ahscale (float | None):
            The scale factor applied to the size of the arrow heads.

    Methods:
        copy(): Create and return a deep copy of the style object.
        merge(style): Merge the provided style with this object's style.
            The provided `style` takes precedence; `None` attributes are
            filled by this instance's values.
    """

    width: TypePosFloat | None = None
    color: TypeColorTuple | None = None
    alpha: TypeAlpha | None = None
    style: TypeLineStyle | None = None
    ahfill: bool | None = None
    ahscale: TypePosFloat | None = None


class ShapeStyle(_StyleModel):
    """Represents the styling attributes for shapes in drawlib.

    Attributes:
        halign (Literal["left", "center", "right"] | None):
            The horizontal alignment of the shape.
        valign (Literal["bottom", "center", "top"] | None):
            The vertical alignment of the shape.
        alpha (float | None):
            The transparency of the shape.
        lwidth (float | None):
            The width of the outline of the shape.
        lcolor (tuple[int, int, int] | tuple[int, int, int, float] | None):
            The color of the outline of the shape.
        lstyle (Literal["solid", "dashed", "dotted", "dashdot"] | None):
            The style of the outline of the shape.
        fcolor (tuple[int, int, int] | tuple[int, int, int, float] | None):
            The fill color of the shape.

    Methods:
        copy(): Create and return a deep copy of the style object.
        merge(style): Merge the provided style with this object's style.
            The provided `style` takes precedence; `None` attributes are
            filled by this instance's values.
    """

    halign: TypeHAlign | None = None
    valign: TypeVAlign | None = None
    alpha: TypeAlpha | None = None
    lwidth: TypePosFloat | None = None
    lcolor: TypeColorTuple | None = None
    lstyle: TypeLineStyle | None = None
    fcolor: TypeColorTuple | None = None


class ShapeTextStyle(_StyleModel):
    """Represents the text styling attributes for shapes in drawlib.

    Attributes:
        alpha (float | None):
            The transparency of the text.
        color (tuple[int, int, int] | tuple[int, int, int, float] | None):
            The color of the text.
        size (float | Literal["small", "medium", "large"] | None):
            The size of the text.
        halign (Literal["left", "center", "right"] | None):
            The horizontal alignment of the text.
        valign (Literal["bottom", "center", "top"] | None):
            The vertical alignment of the text.
        font (FontBase | FontFile | None):
            The font type of the text.
        angle (float | None):
            The rotation angle of the text.
        flip (bool | None):
            Flip the text horizontally if True.
        xy_shift (tuple[float, float] | None):
            Shift the text horizontally and vertically.
        xy_abs_shift (tuple[float, float] | None):
            Shift the text horizontally and vertically by absolute amount.

    Methods:
        copy(): Create and return a deep copy of the style object.
        merge(style): Merge the provided style with this object's style.
            The provided `style` takes precedence; `None` attributes are
            filled by this instance's values.
    """

    alpha: TypeAlpha | None = None
    color: TypeColorTuple | None = None
    size: TypeSize | None = None
    halign: TypeHAlign | None = None
    valign: TypeVAlign | None = None
    font: TypeFont | None = None
    angle: TypeAngle | None = None
    flip: bool | None = None
    xy_shift: TypeCoordinate | None = None
    xy_abs_shift: TypeCoordinate | None = None


class TextStyle(_StyleModel):
    """Represents the text style attributes for drawlib.

    Attributes:
        alpha (float | None):
            The transparency of the text.
        color (tuple[int, int, int] | tuple[int, int, int, float] | None):
            The color of the text.
        size (float | Literal["small", "medium", "large"] | None):
            The size of the text.
        halign (Literal["left", "center", "right"] | None):
            The horizontal alignment of the text.
        valign (Literal["bottom", "center", "top"] | None):
            The vertical alignment of the text.
        font (FontBase | FontFile | None):
            The font type of the text.
        bgalpha (float | None):
            The transparency of the background.
        bglcolor (tuple[int, int, int] | tuple[int, int, int, float] | None):
            The color of the background outline.
        bglstyle (Literal["solid", "dashed", "dotted", "dashdot"] | None):
            The style of the background outline.
        bglwidth (float | None):
            The width of the background outline.
        bgfcolor (tuple[int, int, int] | tuple[int, int, int, float] | None):
            The fill color of the background.

    Methods:
        copy(): Create and return a deep copy of the style object.
        merge(style): Merge the provided style with this object's style.
            The provided `style` takes precedence; `None` attributes are
            filled by this instance's values.
    """

    alpha: TypeAlpha | None = None
    color: TypeColorTuple | None = None
    size: TypeSize | None = None
    halign: TypeHAlign | None = None
    valign: TypeVAlign | None = None
    font: TypeFont | None = None

    # background
    bgalpha: TypeAlpha | None = None
    bglcolor: TypeColorTuple | None = None
    bglstyle: TypeLineStyle | None = None
    bglwidth: TypePosFloat | None = None
    bgfcolor: TypeColorTuple | None = None


class ThemeStyles(BaseModel):
    """Represents a collection of style configurations for various shapes and text in a theme."""

    model_config = ConfigDict(
        extra="forbid",
        validate_assignment=True,
    )

    # mandatory for default
    iconstyle: IconStyle | None = None
    imagestyle: ImageStyle | None = None
    linestyle: LineStyle | None = None
    shapestyle: ShapeStyle | None = None
    shapetextstyle: ShapeTextStyle | None = None
    textstyle: TextStyle | None = None

    # optional for default
    arcstyle: ShapeStyle | None = None
    arctextstyle: ShapeTextStyle | None = None
    circlestyle: ShapeStyle | None = None
    circletextstyle: ShapeTextStyle | None = None
    ellipsestyle: ShapeStyle | None = None
    ellipsetextstyle: ShapeTextStyle | None = None
    polygonstyle: ShapeStyle | None = None
    polygontextstyle: ShapeTextStyle | None = None
    rectanglestyle: ShapeStyle | None = None
    rectangletextstyle: ShapeTextStyle | None = None
    regularpolygonstyle: ShapeStyle | None = None
    regularpolygontextstyle: ShapeTextStyle | None = None
    wedgestyle: ShapeStyle | None = None
    wedgetextstyle: ShapeTextStyle | None = None
    donutsstyle: ShapeStyle | None = None
    donutstextstyle: ShapeTextStyle | None = None
    fanstyle: ShapeStyle | None = None
    fantextstyle: ShapeTextStyle | None = None

    arrowstyle: ShapeStyle | None = None
    arrowtextstyle: ShapeTextStyle | None = None
    rhombusstyle: ShapeStyle | None = None
    rhombustextstyle: ShapeTextStyle | None = None
    parallelogramstyle: ShapeStyle | None = None
    parallelogramtextstyle: ShapeTextStyle | None = None
    trapezoidstyle: ShapeStyle | None = None
    trapezoidtextstyle: ShapeTextStyle | None = None
    trianglestyle: ShapeStyle | None = None
    triangletextstyle: ShapeTextStyle | None = None
    starstyle: ShapeStyle | None = None
    startextstyle: ShapeTextStyle | None = None
    chevronstyle: ShapeStyle | None = None
    chevrontextstyle: ShapeTextStyle | None = None

    bubblespeechstyle: ShapeStyle | None = None
    bubblespeechtextstyle: ShapeTextStyle | None = None


class OfficialThemeStyle(BaseModel):
    """Represents the official style configuration for a theme."""

    model_config = ConfigDict(
        extra="forbid",
        validate_assignment=True,
        arbitrary_types_allowed=True,
        ignored_types=(FontBase, FontFile),
    )

    default_style: ThemeStyles
    named_styles: list[tuple[str, ThemeStyles]]
    theme_colors: list[tuple[str, tuple[int, int, int]]]
    backgroundcolor: TypeColorTuple
    sourcecodefont: InstanceOf[FontSourceCode] | None
