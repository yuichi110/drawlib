# Copyright (c) 2024 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Validate style data."""

from drawlib.v0_2.private.core.model import (
    IconStyle,
    ImageStyle,
    LineStyle,
    ShapeStyle,
    ShapeTextStyle,
    TextStyle,
)


def validate_iconstyle(name: str, value: IconStyle) -> None:
    """Validate icon style.

    Args:
        name (str): Name of the argument or attribute being validated.
        value (IconStyle): IconStyle object to validate.

    Raises:
        ValueError: If value is not an instance of IconStyle.
    """
    if not isinstance(value, IconStyle):
        raise ValueError(f'Arg/Attr "{name}" requires IconStyle. But "{value}" is given.')


def validate_imagestyle(name: str, value: ImageStyle) -> None:
    """Validate image style.

    Args:
        name (str): Name of the argument or attribute being validated.
        value (ImageStyle): ImageStyle object to validate.

    Raises:
        ValueError: If value is not an instance of ImageStyle.
    """
    if not isinstance(value, ImageStyle):
        raise ValueError(f'Arg/Attr "{name}" requires ImageStyle. But "{value}" is given.')


def validate_linestyle(name: str, value: LineStyle) -> None:
    """Validate line style.

    Args:
        name (str): Name of the argument or attribute being validated.
        value (LineStyle): LineStyle object to validate.

    Raises:
        ValueError: If value is not an instance of LineStyle.
    """
    if not isinstance(value, LineStyle):
        raise ValueError(f'Arg/Attr "{name}" requires LineStyle. But "{value}" is given.')


def validate_shapestyle(name: str, value: ShapeStyle) -> None:
    """Validate shape style.

    Args:
        name (str): Name of the argument or attribute being validated.
        value (ShapeStyle): ShapeStyle object to validate.

    Raises:
        ValueError: If value is not an instance of ShapeStyle.
    """
    if not isinstance(value, ShapeStyle):
        raise ValueError(f'Arg/Attr "{name}" requires ShapeStyle. But "{value}" is given.')


def validate_shapetextstyle(name: str, value: ShapeTextStyle) -> None:
    """Validate shape text style.

    Args:
        name (str): Name of the argument or attribute being validated.
        value (ShapeTextStyle): ShapeTextStyle object to validate.

    Raises:
        ValueError: If value is not an instance of ShapeTextStyle.
    """
    if not isinstance(value, ShapeTextStyle):
        raise ValueError(f'Arg/Attr "{name}" requires ShapeTextStyle. But "{value}" is given.')


def validate_textstyle(name: str, value: TextStyle) -> None:
    """Validate text style.

    Args:
        name (str): Name of the argument or attribute being validated.
        value (TextStyle): TextStyle object to validate.

    Raises:
        ValueError: If value is not an instance of TextStyle.
    """
    if not isinstance(value, TextStyle):
        raise ValueError(f'Arg/Attr "{name}" requires TextStyle. But "{value}" is given.')
