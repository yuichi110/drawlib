# Copyright (c) 2024 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

# ruff: noqa: F811
# type: ignore

"""Style models implementation module."""

# !!! Caution !!!
# Please don't use external data classes such as pydantic.
# Use property for validation

from __future__ import annotations

import dataclasses
from copy import deepcopy
from typing import (
    List,
    Literal,
    Optional,
    Tuple,
    Union,
)

import drawlib.v0_1.private.validators.color as color_validator
import drawlib.v0_1.private.validators.coordinate as coordinate_validator
import drawlib.v0_1.private.validators.icon as icon_validator
import drawlib.v0_1.private.validators.line as line_validator
import drawlib.v0_1.private.validators.text as text_validator
import drawlib.v0_1.private.validators.types as types_validator
from drawlib.v0_1.private.core.fonts import (
    Font,
    FontArabic,
    FontBase,
    FontChinese,
    FontFile,
    FontJapanese,
    FontKorean,
    FontMonoSpace,
    FontRoboto,
    FontSansSerif,
    FontSerif,
    FontSourceCode,
)
from drawlib.v0_1.private.util import error_handler


@dataclasses.dataclass
class IconStyle:
    """Represents the styling attributes for icons in drawlib.

    This dataclass encapsulates various style attributes that can be applied to icons,
    including their visual style, color, transparency (alpha), horizontal alignment,
    and vertical alignment.

    Attributes:
        style (Optional[Literal['thin', 'light', 'regular', 'bold', 'fill']], optional):
            The visual style of the icon. Can be one of: 'thin', 'light', 'regular',
            'bold', or 'fill'.
        color (Union[Tuple[int, int, int], Tuple[int, int, int, float], None], optional):
            The color of the icon in RGB or RGBA format. If None, apply theme default.
        alpha (Optional[float], optional):
            The transparency of the icon, ranging from 0.0 (fully transparent) to 1.0
            (fully opaque).
        halign (Optional[Literal['left', 'center', 'right']], optional):
            The horizontal alignment of the icon within its bounding box. Can be one of:
            'left', 'center', or 'right'.
        valign (Optional[Literal['bottom', 'center', 'top']], optional):
            The vertical alignment of the icon within its bounding box. Can be one of:
            'bottom', 'center', or 'top'.

    Methods:
        copy(self) -> IconStyle:
            Creates and returns a deep copy of the IconStyle object.
    """

    style: Optional[Literal["thin", "light", "regular", "bold", "fill"]] = None
    color: Union[Tuple[int, int, int], Tuple[int, int, int, float], None] = None
    alpha: Optional[float] = None
    halign: Optional[Literal["left", "center", "right"]] = None
    valign: Optional[Literal["bottom", "center", "top"]] = None

    @error_handler
    def copy(self) -> IconStyle:
        """Create and return a deep copy of the IconStyle object."""
        return deepcopy(self)

    @error_handler
    def merge(self, style: IconStyle) -> IconStyle:
        """Merge the provided style with this object's style.

        This method takes the given `style` and merges it with the instance's
        style attributes. The `style` parameter is treated as the primary style,
        and any attributes that are `None` in the primary style will be replaced
        with the corresponding attributes from this object's style.

        Args:
            style (IconStyle): The primary style to be merged with this object's style.

        Returns:
            IconStyle: A new `IconStyle` instance with merged attributes.

        Example:
            primary_style = IconStyle(style='solid', color='blue')
            secondary_style = IconStyle(style='dotted', color=None, alpha=0.5)
            result_style = secondary_style.merge(primary_style)
            # result_style will have style='solid', color='blue', alpha=0.5
        """
        if not isinstance(style, IconStyle):
            raise ValueError(f'Arg "style" requires IconStyle. But "{type(style)}" is given.')

        style = style.copy()

        if style.style is None:
            style.style = self.style
        if style.color is None:
            style.color = self.color
        if style.alpha is None:
            style.alpha = self.alpha
        if style.halign is None:
            style.halign = self.halign
        if style.valign is None:
            style.valign = self.valign

        return style

    @property  # type: ignore[no-redef]
    @error_handler
    def style(self) -> Optional[Literal["thin", "light", "regular", "bold", "fill"]]:
        """Getter of style"""
        return getattr(self, "_style", None)

    @style.setter
    @error_handler
    def style(self, value: Optional[Literal["thin", "light", "regular", "bold", "fill"]]) -> None:
        """Setter of style"""
        if isinstance(value, property) or value is None:
            self._style = None
            return

        icon_validator.validate_style("IconStyle.style", value)
        self._style = value

    @property  # type: ignore[no-redef]
    @error_handler
    def color(self) -> Union[Tuple[int, int, int], Tuple[int, int, int, float], None]:
        """Getter of color"""
        return self._color

    @color.setter
    @error_handler
    def color(self, value: Union[Tuple[int, int, int], Tuple[int, int, int, float], None]) -> None:
        """Setter of style"""
        if isinstance(value, property) or value is None:
            self._color = None
            return

        color_validator.validate_color("IconStyle.color", value)
        self._color = value

    @property  # type: ignore[no-redef]
    @error_handler
    def alpha(self) -> Optional[float]:
        """Getter of alpha"""
        return self._alpha

    @alpha.setter
    @error_handler
    def alpha(self, value: Optional[float]) -> None:
        """Setter of alpha"""
        if isinstance(value, property) or value is None:
            self._alpha = None
            return

        color_validator.validate_alpha("IconStyle.alpha", value)
        self._alpha = value

    @property  # type: ignore[no-redef]
    @error_handler
    def halign(self) -> Optional[Literal["left", "center", "right"]]:
        """Getter of halign"""
        return self._halign

    @halign.setter
    @error_handler
    def halign(self, value: Optional[Literal["left", "center", "right"]]) -> None:
        """Setter of halign"""
        if isinstance(value, property) or value is None:
            self._halign = None
            return

        coordinate_validator.validate_halign("IconStyle.halign", value)
        self._halign = value

    @property  # type: ignore[no-redef]
    @error_handler
    def valign(self) -> Optional[Literal["bottom", "center", "top"]]:
        """Getter of valign"""
        return self._valign

    @valign.setter
    @error_handler
    def valign(self, value: Optional[Literal["bottom", "center", "top"]]) -> None:
        """Setter of valign"""
        if isinstance(value, property) or value is None:
            self._valign = None
            return

        coordinate_validator.validate_valign("IconStyle.valign", value)
        self._valign = value


@dataclasses.dataclass
class ImageStyle:
    """Represents the styling attributes for images in drawlib.

    This dataclass encapsulates various style attributes that can be applied to images,
    including their alignment, outline width, outline style, outline color, fill color,
    and transparency.

    Attributes:
        halign (Optional[Literal['left', 'center', 'right']], optional):
            The horizontal alignment of the image within its bounding box. Can be one of:
            'left', 'center', or 'right'.
        valign (Optional[Literal['bottom', 'center', 'top']], optional):
            The vertical alignment of the image within its bounding box. Can be one of:
            'bottom', 'center', or 'top'.
        lwidth (Optional[float], optional):
            The width of the outline (line) around the image. Default is None (no outline).
        lstyle (Optional[Literal['solid', 'dashed', 'dotted', 'dashdot']], optional):
            The style of the outline (line) around the image. Can be one of:
            'solid', 'dashed', 'dotted', or 'dashdot'. Default is None (no outline).
        lcolor (Union[Tuple[int, int, int], Tuple[int, int, int, float], None], optional):
            The color of the outline (line) around the image in RGB or RGBA format.
            Default is None (no outline).
        fcolor (Union[Tuple[int, int, int], Tuple[int, int, int, float], None], optional):
            The fill color of the image in RGB or RGBA format. Default is None (no fill color).
        alpha (Optional[float], optional):
            The transparency of the image, ranging from 0.0 (fully transparent) to 1.0
            (fully opaque). Default is None (fully opaque).

    Methods:
        copy(self) -> ImageStyle:
            Creates and returns a deep copy of the ImageStyle object.
    """

    halign: Optional[Literal["left", "center", "right"]] = None
    valign: Optional[Literal["bottom", "center", "top"]] = None
    lwidth: Optional[float] = None
    lstyle: Optional[Literal["solid", "dashed", "dotted", "dashdot"]] = None
    lcolor: Union[Tuple[int, int, int], Tuple[int, int, int, float], None] = None
    fcolor: Union[Tuple[int, int, int], Tuple[int, int, int, float], None] = None
    alpha: Optional[float] = None

    @error_handler
    def copy(self) -> ImageStyle:
        """Create and return a deep copy of the ImageStyle object."""
        return deepcopy(self)

    @error_handler
    def merge(self, style: ImageStyle) -> ImageStyle:
        """Merge the provided style with this object's style.

        This method takes the given `style` and merges it with the instance's
        style attributes. The `style` parameter is treated as the primary style,
        and any attributes that are `None` in the primary style will be replaced
        with the corresponding attributes from this object's style.

        Args:
            style (ImageStyle): The primary style to be merged with this object's style.

        Returns:
            ImageStyle: A new `ImageStyle` instance with merged attributes.

        Example:
            primary_style = ImageStyle(halign='center', lcolor='red')
            secondary_style = ImageStyle(halign=None, lcolor=None, alpha=0.5)
            result_style = secondary_style.merge(primary_style)
            # result_style will have halign='center', lcolor='red', alpha=0.5
        """
        if not isinstance(style, ImageStyle):
            raise ValueError(f'Arg "style" requires ImageStyle. But "{type(style)}" is given.')

        style = style.copy()

        if style.halign is None:
            style.halign = self.halign
        if style.valign is None:
            style.valign = self.valign
        if style.lstyle is None:
            style.lstyle = self.lstyle
        if style.lcolor is None:
            style.lcolor = self.lcolor
        if style.lwidth is None:
            style.lwidth = self.lwidth
        if style.fcolor is None:
            style.fcolor = self.fcolor
        if style.alpha is None:
            style.alpha = self.alpha

        return style

    @property  # type: ignore[no-redef]
    @error_handler
    def halign(self) -> Optional[Literal["left", "center", "right"]]:
        """Getter of halign"""
        return self._halign

    @halign.setter
    @error_handler
    def halign(self, value: Optional[Literal["left", "center", "right"]]) -> None:
        """Setter of halign"""
        if isinstance(value, property) or value is None:
            self._halign = None
            return

        coordinate_validator.validate_halign("ImageStyle.halign", value)
        self._halign = value

    @property  # type: ignore[no-redef]
    @error_handler
    def valign(self) -> Optional[Literal["bottom", "center", "top"]]:
        """Getter of valign"""
        return self._valign

    @valign.setter
    @error_handler
    def valign(self, value: Optional[Literal["bottom", "center", "top"]]) -> None:
        """Setter of valign"""
        if isinstance(value, property) or value is None:
            self._valign = None
            return

        coordinate_validator.validate_valign("ImageStyle.valign", value)
        self._valign = value

    @property  # type: ignore[no-redef]
    @error_handler
    def lwidth(self) -> Optional[float]:
        """Getter of lwidth"""
        return self._lwidth

    @lwidth.setter
    @error_handler
    def lwidth(self, value: Optional[float]) -> None:
        """Setter of lwidth"""
        if isinstance(value, property) or value is None:
            self._lwidth = None
            return

        types_validator.validate_plus_float("ImageStyle.lwidth", value)
        self._lwidth = value

    @property  # type: ignore[no-redef]
    @error_handler
    def lstyle(self) -> Optional[str]:
        """Getter of lstyle"""
        return self._lstyle

    @lstyle.setter
    @error_handler
    def lstyle(self, value: Optional[str]) -> None:
        """Setter of lstyle"""
        if isinstance(value, property) or value is None:
            self._lstyle = None
            return

        line_validator.validate_style("ImageStyle.lstyle", value)
        self._lstyle = value

    @property  # type: ignore[no-redef]
    @error_handler
    def lcolor(self) -> Union[Tuple[int, int, int], Tuple[int, int, int, float], None]:
        """Getter of lcolor"""
        return self._lcolor

    @lcolor.setter
    @error_handler
    def lcolor(self, value: Union[Tuple[int, int, int], Tuple[int, int, int, float], None]) -> None:
        """Setter of lcolor"""
        if isinstance(value, property) or value is None:
            self._lcolor = None
            return

        color_validator.validate_color("ImageStyle.lcolor", value)
        self._lcolor = value

    @property  # type: ignore[no-redef]
    @error_handler
    def alpha(self) -> Optional[float]:
        """Getter of alpha"""
        return self._alpha

    @alpha.setter
    @error_handler
    def alpha(self, value: Optional[float]) -> None:
        """Setter of alpha"""
        if isinstance(value, property) or value is None:
            self._alpha = None
            return

        color_validator.validate_alpha("ImageStyle.alpha", value)
        self._alpha = value

    @property  # type: ignore[no-redef]
    @error_handler
    def fcolor(self) -> Union[Tuple[int, int, int], Tuple[int, int, int, float], None]:
        """Getter of fcolor"""
        return self._fcolor

    @fcolor.setter
    @error_handler
    def fcolor(self, value: Union[Tuple[int, int, int], Tuple[int, int, int, float], None]) -> None:
        """Setter of fcolor"""
        if isinstance(value, property) or value is None:
            self._fcolor = None
            return

        color_validator.validate_color("ImageStyle.fcolor", value)
        self._fcolor = value


@dataclasses.dataclass
class LineStyle:
    """Represents the styling attributes for lines in drawlib.

    This dataclass encapsulates various style attributes that can be applied to lines,
    including their width, color, transparency, style, arrow head fill, and arrow head scale.

    Attributes:
        width (Optional[float], optional):
            The width of the line. Default is None (no specific width).
        color (Union[Tuple[int, int, int], Tuple[int, int, int, float], None], optional):
            The color of the line in RGB or RGBA format. Default is None (no specific color).
        alpha (Optional[float], optional):
            The transparency of the line, ranging from 0.0 (fully transparent) to 1.0
            (fully opaque). Default is None (fully opaque).
        style (Optional[Literal['solid', 'dashed', 'dotted', 'dashdot']], optional):
            The style of the line. Can be one of: 'solid', 'dashed', 'dotted', or 'dashdot'.
            Default is None (no specific style).
        ahfill (Optional[bool], optional):
            Specifies whether the arrow heads at the ends of the line should be filled (True)
            or not (False). Default is None (no specific fill setting).
        ahscale (Optional[int], optional):
            The scale factor applied to the size of the arrow heads at the ends of the line.
            Default is None (no specific scale factor).

    Methods:
        copy(self) -> LineStyle:
            Creates and returns a deep copy of the LineStyle object.
    """

    width: Optional[float] = None
    color: Union[Tuple[int, int, int], Tuple[int, int, int, float], None] = None
    alpha: Optional[float] = None
    style: Optional[Literal["solid", "dashed", "dotted", "dashdot"]] = None
    ahfill: Optional[bool] = None
    ahscale: Optional[float] = None

    @error_handler
    def copy(self) -> LineStyle:
        """Create and return a deep copy of the LineStyle object."""
        return deepcopy(self)

    @error_handler
    def merge(self, style: LineStyle) -> LineStyle:
        """Merge the provided style with this object's style.

        This method takes the given `style` and merges it with the instance's
        style attributes. The `style` parameter is treated as the primary style,
        and any attributes that are `None` in the primary style will be replaced
        with the corresponding attributes from this object's style.

        Args:
            style (LineStyle): The primary style to be merged with this object's style.

        Returns:
            LineStyle: A new `LineStyle` instance with merged attributes.

        Example:
            primary_style = LineStyle(width=2, color='blue')
            secondary_style = LineStyle(width=None, color=None, alpha=0.5)
            result_style = secondary_style.merge(primary_style)
            # result_style will have width=2, color='blue', alpha=0.5
        """
        if not isinstance(style, LineStyle):
            raise ValueError(f'Arg "style" requires LineStyle. But "{type(style)}" is given.')

        style = style.copy()

        if style.width is None:
            style.width = self.width
        if style.color is None:
            style.color = self.color
        if style.style is None:
            style.style = self.style
        if style.alpha is None:
            style.alpha = self.alpha
        if style.ahfill is None:
            style.ahfill = self.ahfill
        if style.ahscale is None:
            style.ahscale = self.ahscale

        return style

    @property  # type: ignore[no-redef]
    @error_handler
    def width(self) -> Optional[float]:
        """Getter of lwidth"""
        return self._width

    @width.setter
    @error_handler
    def width(self, value: Optional[float]) -> None:
        """Setter of lwidth"""
        if isinstance(value, property) or value is None:
            self._width = None
            return

        types_validator.validate_plus_float("LineStyle.width", value)
        self._width = value

    @property  # type: ignore[no-redef]
    @error_handler
    def color(self) -> Union[Tuple[int, int, int], Tuple[int, int, int, float], None]:
        """Getter of color"""
        return self._color

    @color.setter
    @error_handler
    def color(self, value: Union[Tuple[int, int, int], Tuple[int, int, int, float], None]) -> None:
        """Setter of color"""
        if isinstance(value, property) or value is None:
            self._color = None
            return

        color_validator.validate_color("LineStyle.color", value)
        self._color = value

    @property  # type: ignore[no-redef]
    @error_handler
    def alpha(self) -> Optional[float]:
        """Getter of alpha"""
        return self._alpha

    @alpha.setter
    @error_handler
    def alpha(self, value: Optional[float]) -> None:
        """Setter of alpha"""
        if isinstance(value, property) or value is None:
            self._alpha = None
            return

        color_validator.validate_alpha("LineStyle.alpha", value)
        self._alpha = value

    @property  # type: ignore[no-redef]
    @error_handler
    def style(self) -> Optional[str]:
        """Getter of lstyle"""
        return self._style

    @style.setter
    @error_handler
    def style(self, value: Optional[str]) -> None:
        """Setter of lstyle"""
        if isinstance(value, property) or value is None:
            self._style = None
            return

        line_validator.validate_style("LineStyle.style", value)
        self._style = value

    @property  # type: ignore[no-redef]
    @error_handler
    def ahscale(self) -> Optional[float]:
        """Getter of arrow head scale"""
        return self._ahscale

    @ahscale.setter
    @error_handler
    def ahscale(self, value: Optional[float]) -> None:
        """Setter of hscale"""
        if isinstance(value, property) or value is None:
            self._ahscale = None
            return

        types_validator.validate_plus_float("LineStyle.ahscale", value)
        self._ahscale = value

    @property  # type: ignore[no-redef]
    @error_handler
    def ahfill(self) -> Optional[bool]:
        """Getter of arrow head fill"""
        return self._ahfill

    @ahfill.setter
    @error_handler
    def ahfill(self, value: Optional[bool]) -> None:
        """Setter of lstyle"""
        if isinstance(value, property) or value is None:
            self._ahfill = None
            return

        types_validator.validate_bool("LineStyle.ahfill", value)
        self._ahfill = value


@dataclasses.dataclass
class ShapeStyle:
    """Represents the styling attributes for shapes in drawlib.

    This dataclass encapsulates various style attributes that can be applied to shapes,
    including horizontal and vertical alignment, transparency, line width, line color,
    line style, and fill color.

    Attributes:
        halign (Optional[Literal['left', 'center', 'right']], optional):
            The horizontal alignment of the shape. Default is None (no specific alignment).
        valign (Optional[Literal['bottom', 'center', 'top']], optional):
            The vertical alignment of the shape. Default is None (no specific alignment).
        alpha (Optional[float], optional):
            The transparency of the shape, ranging from 0.0 (fully transparent) to 1.0
            (fully opaque). Default is None (fully opaque).
        lwidth (Optional[float], optional):
            The width of the outline of the shape. Default is None (no specific width).
        lstyle (Optional[Literal['solid', 'dashed', 'dotted', 'dashdot']], optional):
            The style of the outline of the shape. Can be one of: 'solid', 'dashed', 'dotted',
            or 'dashdot'. Default is None (no specific style).
        lcolor (Union[Tuple[int, int, int], Tuple[int, int, int, float], None], optional):
            The color of the outline of the shape in RGB or RGBA format. Default is None
            (no specific color).
        fcolor (Union[Tuple[int, int, int], Tuple[int, int, int, float], None], optional):
            The fill color of the shape in RGB or RGBA format. Default is None (no specific color).

    Methods:
        copy(self) -> ShapeStyle:
            Creates and returns a deep copy of the ShapeStyle object.
    """

    halign: Optional[Literal["left", "center", "right"]] = None
    valign: Optional[Literal["bottom", "center", "top"]] = None
    alpha: Optional[float] = None
    lwidth: Optional[float] = None
    lcolor: Union[Tuple[int, int, int], Tuple[int, int, int, float], None] = None
    lstyle: Optional[Literal["solid", "dashed", "dotted", "dashdot"]] = None
    fcolor: Union[Tuple[int, int, int], Tuple[int, int, int, float], None] = None

    @error_handler
    def copy(self) -> ShapeStyle:
        """Create and return a deep copy of the ShapeStyle object."""
        return deepcopy(self)

    @error_handler
    def merge(self, style: ShapeStyle) -> ShapeStyle:
        """Merge the provided style with this object's style.

        This method takes the given `style` and merges it with the instance's
        style attributes. The `style` parameter is treated as the primary style,
        and any attributes that are `None` in the primary style will be replaced
        with the corresponding attributes from this object's style.

        Args:
            style (ShapeStyle): The primary style to be merged with this object's style.

        Returns:
            ShapeStyle: A new `ShapeStyle` instance with merged attributes.

        Example:
            primary_style = ShapeStyle(halign='center', lcolor='red')
            secondary_style = ShapeStyle(halign=None, lcolor=None, alpha=0.5)
            result_style = secondary_style.merge(primary_style)
            # result_style will have halign='center', lcolor='red', alpha=0.5
        """
        if not isinstance(style, ShapeStyle):
            raise ValueError(f'Arg "style" requires ShapeStyle. But "{type(style)}" is given.')

        style = style.copy()

        if style.halign is None:
            style.halign = self.halign
        if style.valign is None:
            style.valign = self.valign
        if style.lwidth is None:
            style.lwidth = self.lwidth
        if style.lcolor is None:
            style.lcolor = self.lcolor
        if style.lstyle is None:
            style.lstyle = self.lstyle
        if style.fcolor is None:
            style.fcolor = self.fcolor
        if style.alpha is None:
            style.alpha = self.alpha

        return style

    @property  # type: ignore[no-redef]
    @error_handler
    def halign(self) -> Optional[Literal["left", "center", "right"]]:
        """Getter of halign"""
        return self._halign

    @halign.setter
    @error_handler
    def halign(self, value: Optional[Literal["left", "center", "right"]]) -> None:
        """Setter of halign"""
        if isinstance(value, property) or value is None:
            self._halign = None
            return

        coordinate_validator.validate_halign("ShapeStyle.halign", value)
        self._halign = value

    @property  # type: ignore[no-redef]
    @error_handler
    def valign(self) -> Optional[Literal["bottom", "center", "top"]]:
        """Getter of valign"""
        return self._valign

    @valign.setter
    @error_handler
    def valign(self, value: Optional[Literal["bottom", "center", "top"]]) -> None:
        """Setter of valign"""
        if isinstance(value, property) or value is None:
            self._valign = None
            return

        coordinate_validator.validate_valign("ShapeStyle.valign", value)
        self._valign = value

    @property  # type: ignore[no-redef]
    @error_handler
    def alpha(self) -> Optional[float]:
        """Getter of alpha"""
        return self._alpha

    @alpha.setter
    @error_handler
    def alpha(self, value: Optional[float]) -> None:
        """Setter of alpha"""
        if isinstance(value, property) or value is None:
            self._alpha = None
            return

        color_validator.validate_alpha("ShapeStyle.alpha", value)
        self._alpha = value

    @property  # type: ignore[no-redef]
    @error_handler
    def lwidth(self) -> Optional[float]:
        """Getter of lwidth"""
        return self._lwidth

    @lwidth.setter
    @error_handler
    def lwidth(self, value: Optional[float]) -> None:
        """Setter of lwidth"""
        if isinstance(value, property) or value is None:
            self._lwidth = None
            return

        types_validator.validate_plus_float("ShapeStyle.lwidth", value)
        self._lwidth = value

    @property  # type: ignore[no-redef]
    @error_handler
    def lstyle(self) -> Optional[str]:
        """Getter of lstyle"""
        return self._lstyle

    @lstyle.setter
    @error_handler
    def lstyle(self, value: Optional[str]) -> None:
        """Setter of lstyle"""
        if isinstance(value, property) or value is None:
            self._lstyle = None
            return

        line_validator.validate_style("ShapeStyle.lstyle", value)
        self._lstyle = value

    @property  # type: ignore[no-redef]
    @error_handler
    def lcolor(self) -> Union[Tuple[int, int, int], Tuple[int, int, int, float], None]:
        """Getter of lcolor"""
        return self._lcolor

    @lcolor.setter
    @error_handler
    def lcolor(self, value: Union[Tuple[int, int, int], Tuple[int, int, int, float], None]) -> None:
        """Setter of lcolor"""
        if isinstance(value, property) or value is None:
            self._lcolor = None
            return

        color_validator.validate_color("ShapeStyle.lcolor", value)
        self._lcolor = value

    @property  # type: ignore[no-redef]
    @error_handler
    def fcolor(self) -> Union[Tuple[int, int, int], Tuple[int, int, int, float], None]:
        """Getter of fcolor"""
        return self._fcolor

    @fcolor.setter
    @error_handler
    def fcolor(self, value: Union[Tuple[int, int, int], Tuple[int, int, int, float], None]) -> None:
        """Setter of fcolor"""
        if isinstance(value, property) or value is None:
            self._fcolor = None
            return

        color_validator.validate_color("ShapeStyle.fcolor", value)
        self._fcolor = value


@dataclasses.dataclass
class ShapeTextStyle:
    """Represents the text styling attributes for shapes in drawlib.

    This dataclass encapsulates various style attributes that can be applied to text in shapes,
    including transparency, color, size, horizontal and vertical alignment, font type,
    rotation angle, flip status, and xy shift.

    Attributes:
        alpha (Optional[float], optional):
            The transparency of the text, ranging from 0.0 (fully transparent) to 1.0
            (fully opaque). Default is None (fully opaque).
        color (Union[Tuple[int, int, int], Tuple[int, int, int, float], None], optional):
            The color of the text in RGB or RGBA format. Default is None (no specific color).
        size (Union[float, str, None], optional):
            The size of the text. It can be a float indicating the font size in points,
            a string representing relative sizes ('small', 'medium', 'large'), or None
            (default size). Default is None.
        halign (Optional[Literal['left', 'center', 'right']], optional):
            The horizontal alignment of the text. Default is None (no specific alignment).
        valign (Optional[Literal['bottom', 'center', 'top']], optional):
            The vertical alignment of the text. Default is None (no specific alignment).
        font (Union[
            Font, FontArabic, FontBase, FontSerif, FontSansSerif, FontChinese,
            FontJapanese, FontKorean, FontMonoSpace, FontRoboto, FontSourceCode,
            FontFile, None], optional):
            The font type of the text. Default is None (no specific font).
        angle (Optional[float], optional):
            The rotation angle of the text in degrees. Default is None (no rotation).
        flip (Optional[bool], optional):
            Flip the text horizontally if True. Default is None (no flipping).
        xy_shift (Optional[Tuple[float, float]], optional):
            Shift the text horizontally and vertically by the specified amount.
            Default is None (no shift).

    Methods:
        copy(self) -> ShapeTextStyle:
            Creates and returns a deep copy of the ShapeTextStyle object.
    """

    alpha: Optional[float] = None
    color: Union[Tuple[int, int, int], Tuple[int, int, int, float], None] = None
    size: Union[float, str, None] = None
    halign: Optional[Literal["left", "center", "right"]] = None
    valign: Optional[Literal["bottom", "center", "top"]] = None
    font: Union[
        Font,
        FontArabic,
        FontBase,
        FontSerif,
        FontSansSerif,
        FontChinese,
        FontJapanese,
        FontKorean,
        FontMonoSpace,
        FontRoboto,
        FontSourceCode,
        FontFile,
        None,
    ] = None
    angle: Optional[float] = None
    flip: Optional[bool] = None
    xy_shift: Optional[Tuple[float, float]] = None

    @error_handler
    def copy(self) -> ShapeTextStyle:
        """Create and return a deep copy of the ShapeTextStyle object."""
        return deepcopy(self)

    @error_handler
    def merge(self, style: ShapeTextStyle) -> ShapeTextStyle:
        """Merge the provided style with this object's style.

        This method takes the given `style` and merges it with the instance's
        style attributes. The `style` parameter is treated as the primary style,
        and any attributes that are `None` in the primary style will be replaced
        with the corresponding attributes from this object's style.

        Args:
            style (ShapeTextStyle): The primary style to be merged with this object's style.

        Returns:
            ShapeTextStyle: A new `ShapeTextStyle` instance with merged attributes.

        Example:
            primary_style = ShapeTextStyle(color='black', size=12)
            secondary_style = ShapeTextStyle(color=None, size=None, alpha=0.5)
            result_style = secondary_style.merge(primary_style)
            # result_style will have color='black', size=12, alpha=0.5
        """
        if not isinstance(style, ShapeTextStyle):
            raise ValueError(f'Arg "style" requires ShapeTextStyle. But "{type(style)}" is given.')

        style = style.copy()

        if style.color is None:
            style.color = self.color
        if style.size is None:
            style.size = self.size
        if style.halign is None:
            style.halign = self.halign
        if style.valign is None:
            style.valign = self.valign
        if style.font is None:
            style.font = self.font
        if style.alpha is None:
            style.alpha = self.alpha

        return style

    @property  # type: ignore[no-redef]
    @error_handler
    def halign(self) -> Optional[Literal["left", "center", "right"]]:
        """Getter of halign"""
        return self._halign

    @halign.setter
    @error_handler
    def halign(self, value: Optional[Literal["left", "center", "right"]]) -> None:
        """Setter of halign"""
        if isinstance(value, property) or value is None:
            self._halign = None
            return

        coordinate_validator.validate_halign("ShapeTextStyle.halign", value)
        self._halign = value

    @property  # type: ignore[no-redef]
    @error_handler
    def valign(self) -> Optional[Literal["bottom", "center", "top"]]:
        """Getter of valign"""
        return self._valign

    @valign.setter
    @error_handler
    def valign(self, value: Optional[Literal["bottom", "center", "top"]]) -> None:
        """Setter of valign"""
        if isinstance(value, property) or value is None:
            self._valign = None
            return

        coordinate_validator.validate_valign("ShapeTextStyle.valign", value)
        self._valign = value

    @property  # type: ignore[no-redef]
    @error_handler
    def color(self) -> Union[Tuple[int, int, int], Tuple[int, int, int, float], None]:
        """Getter of color"""
        return self._color

    @color.setter
    @error_handler
    def color(self, value: Union[Tuple[int, int, int], Tuple[int, int, int, float], None]) -> None:
        """Setter of color"""
        if isinstance(value, property) or value is None:
            self._color = None
            return

        color_validator.validate_color("ShapeTextStyle.color", value)
        self._color = value

    @property  # type: ignore[no-redef]
    @error_handler
    def alpha(self) -> Optional[float]:
        """Getter of alpha"""
        return self._alpha

    @alpha.setter
    @error_handler
    def alpha(self, value: Optional[float]) -> None:
        """Setter of alpha"""
        if isinstance(value, property) or value is None:
            self._alpha = None
            return

        color_validator.validate_alpha("ShapeTextStyle.alpha", value)
        self._alpha = value

    @property  # type: ignore[no-redef]
    @error_handler
    def size(self) -> Optional[float]:
        """Getter of size"""
        return self._size

    @size.setter
    @error_handler
    def size(self, value: Optional[float]) -> None:
        """Setter of size"""
        if isinstance(value, property) or value is None:
            self._size = None
            return

        types_validator.validate_plus_float("ShapeTextStyle.size", value)
        self._size = value

    @property  # type: ignore[no-redef]
    @error_handler
    def font(
        self,
    ) -> Union[
        Font,
        FontArabic,
        FontBase,
        FontSerif,
        FontSansSerif,
        FontChinese,
        FontJapanese,
        FontKorean,
        FontMonoSpace,
        FontRoboto,
        FontSourceCode,
        FontFile,
        None,
    ]:
        """Getter of font"""
        return self._font

    @font.setter
    @error_handler
    def font(
        self,
        value: Union[
            Font,
            FontArabic,
            FontBase,
            FontSerif,
            FontSansSerif,
            FontChinese,
            FontJapanese,
            FontKorean,
            FontMonoSpace,
            FontRoboto,
            FontSourceCode,
            FontFile,
            None,
        ],
    ) -> None:
        """Setter of font"""
        if isinstance(value, property) or value is None:
            self._font = None
            return

        text_validator.validate_font("ShapeTextStyle.font", value)
        self._font = value

    @property  # type: ignore[no-redef]
    @error_handler
    def angle(self) -> Optional[float]:
        """Getter of angle"""
        return self._angle

    @angle.setter
    @error_handler
    def angle(self, value: Optional[float]) -> None:
        """Setter of alpha"""
        if isinstance(value, property) or value is None:
            self._angle = None
            return

        coordinate_validator.validate_angle("ShapeTextStyle.angle", value)
        self._angle = value

    @property  # type: ignore[no-redef]
    @error_handler
    def flip(self) -> Optional[bool]:
        """Getter of flip"""
        return self._flip

    @flip.setter
    @error_handler
    def flip(self, value: Optional[bool]) -> None:
        """Setter of flip"""
        if isinstance(value, property) or value is None:
            self._flip = None
            return

        types_validator.validate_bool("ShapeTextStyle.flip", value)
        self._flip = value

    @property  # type: ignore[no-redef]
    @error_handler
    def xy_shift(self) -> Optional[Tuple[float, float]]:
        """Getter of xy_shift"""
        return self._xy_shift

    @xy_shift.setter
    @error_handler
    def xy_shift(self, value: Optional[float]) -> None:
        """Setter of xy_shift"""
        if isinstance(value, property) or value is None:
            self._xy_shift = None
            return

        coordinate_validator.validate_xy("ShapeTextStyle.xy_shift", value)
        self._xy_shift = value


@dataclasses.dataclass
class TextStyle:
    """Represents the text style attributes for drawlib.

    This dataclass encapsulates various style attributes that can be applied to text,
    including transparency, color, size, horizontal and vertical alignment, font type,
    and background attributes such as background transparency, color, style, and width.

    Attributes:
        alpha (Optional[float], optional):
            The transparency of the text, ranging from 0.0 (fully transparent) to 1.0
            (fully opaque). Default is None (fully opaque).
        color (Union[Tuple[int, int, int], Tuple[int, int, int, float], None], optional):
            The color of the text in RGB or RGBA format. Default is None (no specific color).
        size (Union[float, str, None], optional):
            The size of the text. It can be a float indicating the font size in points,
            a string representing relative sizes ('small', 'medium', 'large'), or None
            (default size). Default is None.
        halign (Optional[Literal['left', 'center', 'right']], optional):
            The horizontal alignment of the text. Default is None (no specific alignment).
        valign (Optional[Literal['bottom', 'center', 'top']], optional):
            The vertical alignment of the text. Default is None (no specific alignment).
        font (Union[
            Font, FontArabic, FontBase, FontSerif, FontSansSerif, FontChinese,
            FontJapanese, FontKorean, FontMonoSpace, FontRoboto, FontSourceCode,
            FontFile, None], optional):
            The font type of the text. Default is None (no specific font).

        # Background attributes
        bgalpha (Optional[float], optional):
            The transparency of the background behind the text, ranging from 0.0
            (fully transparent) to 1.0 (fully opaque). Default is None (fully opaque).
        bglcolor (Union[Tuple[int, int, int], Tuple[int, int, int, float], None], optional):
            The color of the background behind the text in RGB or RGBA format.
            Default is None (no specific color).
        bglstyle (Optional[Literal["solid", "dashed", "dotted", "dashdot"]], optional):
            The style of the background line behind the text. Default is None (no specific style).
        bglwidth (Optional[float], optional):
            The width of the background line behind the text. Default is None (no specific width).
        bgfcolor (Union[Tuple[int, int, int], Tuple[int, int, int, float], None], optional):
            The fill color of the background behind the text in RGB or RGBA format.
            Default is None (no specific color).

    Methods:
        copy(self) -> TextStyle:
            Creates and returns a deep copy of the TextStyle object.
    """

    alpha: Optional[float] = None
    color: Union[Tuple[int, int, int], Tuple[int, int, int, float], None] = None
    size: Union[float, str, None] = None
    halign: Optional[Literal["left", "center", "right"]] = None
    valign: Optional[Literal["bottom", "center", "top"]] = None
    font: Union[
        Font,
        FontArabic,
        FontBase,
        FontSerif,
        FontSansSerif,
        FontChinese,
        FontJapanese,
        FontKorean,
        FontMonoSpace,
        FontRoboto,
        FontSourceCode,
        FontFile,
        None,
    ] = None

    # background
    bgalpha: Optional[float] = None
    bglcolor: Union[Tuple[int, int, int], Tuple[int, int, int, float], None] = None
    bglstyle: Optional[Literal["solid", "dashed", "dotted", "dashdot"]] = None
    bglwidth: Optional[float] = None
    bgfcolor: Union[Tuple[int, int, int], Tuple[int, int, int, float], None] = None

    @error_handler
    def copy(self) -> TextStyle:
        """Create and return a deep copy of the TextStyle object."""
        return deepcopy(self)

    @error_handler
    def merge(self, style: TextStyle) -> TextStyle:  # noqa: C901
        """Merge the provided style with this object's style.

        This method takes the given `style` and merges it with the instance's
        style attributes. The `style` parameter is treated as the primary style,
        and any attributes that are `None` in the primary style will be replaced
        with the corresponding attributes from this object's style.

        Args:
            style (TextStyle): The primary style to be merged with this object's style.

        Returns:
            TextStyle: A new `TextStyle` instance with merged attributes.

        Example:
            primary_style = TextStyle(color='black', size=12)
            secondary_style = TextStyle(color=None, size=None, alpha=0.5)
            result_style = secondary_style.merge(primary_style)
            # result_style will have color='black', size=12, alpha=0.5

        """
        if not isinstance(style, TextStyle):
            raise ValueError(f'Arg "style" requires TextStyle. But "{type(style)}" is given.')

        style = style.copy()

        if style.color is None:
            style.color = self.color
        if style.size is None:
            style.size = self.size
        if style.halign is None:
            style.halign = self.halign
        if style.valign is None:
            style.valign = self.valign
        if style.font is None:
            style.font = self.font
        if style.alpha is None:
            style.alpha = self.alpha
        if style.bgalpha is None:
            style.bgalpha = self.bgalpha
        if style.bglcolor is None:
            style.bglcolor = self.bglcolor
        if style.bglstyle is None:
            style.bglstyle = self.bglstyle
        if style.bglwidth is None:
            style.bglwidth = self.bglwidth
        if style.bgfcolor is None:
            style.bgfcolor = self.bgfcolor

        return style

    @property  # type: ignore[no-redef]
    @error_handler
    def halign(self) -> Optional[Literal["left", "center", "right"]]:
        """Getter of halign"""
        return self._halign

    @halign.setter
    @error_handler
    def halign(self, value: Optional[Literal["left", "center", "right"]]) -> None:
        """Setter of halign"""
        if isinstance(value, property) or value is None:
            self._halign = None
            return

        coordinate_validator.validate_halign("TextStyle.halign", value)
        self._halign = value

    @property  # type: ignore[no-redef]
    @error_handler
    def valign(self) -> Optional[Literal["bottom", "center", "top"]]:
        """Getter of valign"""
        return self._valign

    @valign.setter
    @error_handler
    def valign(self, value: Optional[Literal["bottom", "center", "top"]]) -> None:
        """Setter of valign"""
        if isinstance(value, property) or value is None:
            self._valign = None
            return

        coordinate_validator.validate_valign("TextStyle.valign", value)
        self._valign = value

    @property  # type: ignore[no-redef]
    @error_handler
    def color(self) -> Union[Tuple[int, int, int], Tuple[int, int, int, float], None]:
        """Getter of color"""
        return self._color

    @color.setter
    @error_handler
    def color(self, value: Union[Tuple[int, int, int], Tuple[int, int, int, float], None]) -> None:
        """Setter of color"""
        if isinstance(value, property) or value is None:
            self._color = None
            return

        color_validator.validate_color("TextStyle.color", value)
        self._color = value

    @property  # type: ignore[no-redef]
    @error_handler
    def alpha(self) -> Optional[float]:
        """Getter of alpha"""
        return self._alpha

    @alpha.setter
    @error_handler
    def alpha(self, value: Optional[float]) -> None:
        """Setter of alpha"""
        if isinstance(value, property) or value is None:
            self._alpha = None
            return

        color_validator.validate_alpha("TextStyle.alpha", value)
        self._alpha = value

    @property  # type: ignore[no-redef]
    @error_handler
    def size(self) -> Optional[float]:
        """Getter of size"""
        return self._size

    @size.setter
    @error_handler
    def size(self, value: Optional[float]) -> None:
        """Setter of size"""
        if isinstance(value, property) or value is None:
            self._size = None
            return

        types_validator.validate_plus_float("TextStyle.size", value)
        self._size = value

    @property  # type: ignore[no-redef]
    @error_handler
    def font(
        self,
    ) -> Union[
        Font,
        FontArabic,
        FontBase,
        FontSerif,
        FontSansSerif,
        FontChinese,
        FontJapanese,
        FontKorean,
        FontMonoSpace,
        FontRoboto,
        FontSourceCode,
        FontFile,
        None,
    ]:
        """Getter of font"""
        return self._font

    @font.setter
    @error_handler
    def font(
        self,
        value: Union[
            Font,
            FontArabic,
            FontBase,
            FontSerif,
            FontSansSerif,
            FontChinese,
            FontJapanese,
            FontKorean,
            FontMonoSpace,
            FontRoboto,
            FontSourceCode,
            FontFile,
            None,
        ],
    ) -> None:
        """Setter of font"""
        if isinstance(value, property) or value is None:
            self._font = None
            return

        text_validator.validate_font("TextStyle.font", value)
        self._font = value

    @property  # type: ignore[no-redef]
    @error_handler
    def bgalpha(self) -> Optional[float]:
        """Getter of bgalpha"""
        return self._bgalpha

    @bgalpha.setter
    @error_handler
    def bgalpha(self, value: Optional[float]) -> None:
        """Setter of bgalpha"""
        if isinstance(value, property) or value is None:
            self._bgalpha = None
            return

        color_validator.validate_alpha("TextStyle.bgalpha", value)
        self._bgalpha = value

    @property  # type: ignore[no-redef]
    @error_handler
    def bglwidth(self) -> Optional[float]:
        """Getter of bglwidth"""
        return self._bglwidth

    @bglwidth.setter
    @error_handler
    def bglwidth(self, value: Optional[float]) -> None:
        """Setter of bglwidth"""
        if isinstance(value, property) or value is None:
            self._bglwidth = None
            return

        types_validator.validate_plus_float("TextStyle.bglwidth", value)
        self._bglwidth = value

    @property  # type: ignore[no-redef]
    @error_handler
    def bglstyle(self) -> Optional[str]:
        """Getter of bglstyle"""
        return self._bglstyle

    @bglstyle.setter
    @error_handler
    def bglstyle(self, value: Optional[str]) -> None:
        """Setter of bglstyle"""
        if isinstance(value, property) or value is None:
            self._bglstyle = None
            return

        line_validator.validate_style("TextStyle.bglstyle", value)
        self._bglstyle = value

    @property  # type: ignore[no-redef]
    @error_handler
    def bglcolor(self) -> Union[Tuple[int, int, int], Tuple[int, int, int, float], None]:
        """Getter of bglcolor"""
        return self._bglcolor

    @bglcolor.setter
    @error_handler
    def bglcolor(self, value: Union[Tuple[int, int, int], Tuple[int, int, int, float], None]) -> None:
        """Setter of bglcolor"""
        if isinstance(value, property) or value is None:
            self._bglcolor = None
            return

        color_validator.validate_color("TextStyle.bglcolor", value)
        self._bglcolor = value

    @property  # type: ignore[no-redef]
    @error_handler
    def bgfcolor(self) -> Union[Tuple[int, int, int], Tuple[int, int, int, float], None]:
        """Getter of bgfcolor"""
        return self._bgfcolor

    @bgfcolor.setter
    @error_handler
    def bgfcolor(self, value: Union[Tuple[int, int, int], Tuple[int, int, int, float], None]) -> None:
        """Setter of fcolor"""
        if isinstance(value, property) or value is None:
            self._bgfcolor = None
            return

        color_validator.validate_color("TextStyle.bgfcolor", value)
        self._bgfcolor = value


@dataclasses.dataclass
class ThemeStyles:
    """Represents a collection of style configurations for various shapes and text in a theme.

    This dataclass provides a set of optional style configurations for different graphical
    elements and their associated text, allowing customization of visual representations
    within a theme.
    """

    # mandatory for default
    iconstyle: Optional[IconStyle] = None
    imagestyle: Optional[ImageStyle] = None
    linestyle: Optional[LineStyle] = None
    shapestyle: Optional[ShapeStyle] = None
    shapetextstyle: Optional[ShapeTextStyle] = None
    textstyle: Optional[TextStyle] = None

    # optional for default
    arcstyle: Optional[ShapeStyle] = None
    arctextstyle: Optional[ShapeTextStyle] = None
    circlestyle: Optional[ShapeStyle] = None
    circletextstyle: Optional[ShapeTextStyle] = None
    ellipsestyle: Optional[ShapeStyle] = None
    ellipsetextstyle: Optional[ShapeTextStyle] = None
    polygonstyle: Optional[ShapeStyle] = None
    polygontextstyle: Optional[ShapeTextStyle] = None
    rectanglestyle: Optional[ShapeStyle] = None
    rectangletextstyle: Optional[ShapeTextStyle] = None
    regularpolygonstyle: Optional[ShapeStyle] = None
    regularpolygontextstyle: Optional[ShapeTextStyle] = None
    wedgestyle: Optional[ShapeStyle] = None
    wedgetextstyle: Optional[ShapeTextStyle] = None
    donutsstyle: Optional[ShapeStyle] = None
    donutstextstyle: Optional[ShapeTextStyle] = None
    fanstyle: Optional[ShapeStyle] = None
    fantextstyle: Optional[ShapeTextStyle] = None

    arrowstyle: Optional[ShapeStyle] = None
    arrowtextstyle: Optional[ShapeTextStyle] = None
    rhombusstyle: Optional[ShapeStyle] = None
    rhombustextstyle: Optional[ShapeTextStyle] = None
    parallelogramstyle: Optional[ShapeStyle] = None
    parallelogramtextstyle: Optional[ShapeTextStyle] = None
    trapezoidstyle: Optional[ShapeStyle] = None
    trapezoidtextstyle: Optional[ShapeTextStyle] = None
    trianglestyle: Optional[ShapeStyle] = None
    triangletextstyle: Optional[ShapeTextStyle] = None
    starstyle: Optional[ShapeStyle] = None
    startextstyle: Optional[ShapeTextStyle] = None
    chevronstyle: Optional[ShapeStyle] = None
    chevrontextstyle: Optional[ShapeTextStyle] = None

    bubblespeechstyle: Optional[ShapeStyle] = None
    bubblespeechtextstyle: Optional[ShapeTextStyle] = None


@dataclasses.dataclass
class OfficialThemeStyle:
    """Represents the official style configuration for a theme.

    This dataclass encapsulates various style configurations and color definitions
    for a theme, including default and named styles, theme colors, background color,
    and optional source code font.
    """

    default_style: ThemeStyles
    named_styles: List[Tuple[str, ThemeStyles]]
    theme_colors: List[Tuple[str, Tuple[int, int, int]]]
    backgroundcolor: Union[Tuple[int, int, int], Tuple[int, int, int, float]]
    sourcecodefont: Optional[FontSourceCode]
