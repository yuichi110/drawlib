# Copyright (c) 2024 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Validate line data."""

from typing import Union


def validate_style(name: str, value: str) -> None:
    """Validate line style.

    Args:
        name (str): Name of the argument or attribute being validated.
        value (str): Line style to validate.

    Raises:
        ValueError: If value is not one of ["solid", "dashed", "dotted", "dashdot"].
    """
    supported = ["solid", "dashed", "dotted", "dashdot"]
    if value not in supported:
        raise ValueError(f'Arg/Attr "{name}" must be one of {supported}. But "{value}" is given.')


def validate_arrowhead(name: str, value: str) -> None:
    """Validate arrowhead style.

    Args:
        name (str): Name of the argument or attribute being validated.
        value (str): Arrowhead style to validate.

    Raises:
        ValueError: If value is not one of ["", "->", "<-", "<->"].
    """
    supported = ["", "->", "<-", "<->"]
    if value not in supported:
        raise ValueError(f'Arg/Attr "{name}" must be one of {supported}. But "{value}" is given.')


def validate_bend(arg_name: str, value: Union[int, float]) -> None:
    """Validate bend value for a line.

    Args:
        arg_name (str): Name of the argument or attribute being validated.
        value (Union[int, float]): Bend value to validate.

    Raises:
        ValueError: If value is not an int or float within the range (-2.0, 2.0).
    """
    message = f'Arg/Attr "{arg_name}" must be int/float -2.0~2.0. But "{value}" is given.'

    if not isinstance(value, (int, float)):
        raise ValueError(message)

    if not -2 < value < 2:
        raise ValueError(message)
