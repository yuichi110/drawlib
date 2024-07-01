# Copyright (c) 2024 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Validate shape data."""

from typing import Union


def validate_num_vertex(arg_name: str, value: int) -> None:
    """Validate number of vertices for a shape.

    Args:
        arg_name (str): Name of the argument or attribute being validated.
        value (int): Number of vertices to validate.

    Raises:
        ValueError: If value is not an integer greater than or equal to 3.
    """
    message = f'Arg/Attr "{arg_name}" must be int > 3. But "{value}" is given.'

    if not isinstance(value, int):
        raise ValueError(message)
    if value < 3:
        raise ValueError(message)


def validate_r(arg_name: str, value: Union[int, float]) -> None:
    """Validate radius value for a shape.

    Args:
        arg_name (str): Name of the argument or attribute being validated.
        value (Union[int, float]): Radius value to validate.

    Raises:
        ValueError: If value is not a non-negative integer or float.
    """
    message = f'Arg/Attr "{arg_name}" must be int|float >= 0. But "{value}" is given.'

    if not isinstance(value, (float, int)):
        raise ValueError(message)

    if value < 0:
        raise ValueError(message)


def validate_head_style(arg_name: str, value: str) -> None:
    """Validate head style for a shape.

    Args:
        arg_name (str): Name of the argument or attribute being validated.
        value (str): Head style value to validate.

    Raises:
        ValueError: If value is not one of ["->", "<-", "<->"].
    """
    message = f'Arg/Attr "{arg_name}" must be one of "->","<-","<->". But "{value}" is given.'

    if value not in {"->", "<-", "<->"}:
        raise ValueError(message)
