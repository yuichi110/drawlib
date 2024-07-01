# Copyright (c) 2024 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Validate coordinate data."""

from typing import List, Tuple, Union


def validate_halign(name: str, value: str) -> None:
    """Validate horizontal alignment value.

    Args:
        name (str): Name of the argument or attribute being validated.
        value (str): Horizontal alignment value to validate.

    Raises:
        ValueError: If value is not one of ["left", "center", "right"].

    """
    supported = ["left", "center", "right"]
    if value not in supported:
        raise ValueError(f'Arg/Attr {name} must be one of {supported}. But "{value}" is given.')


def validate_valign(name: str, value: str) -> None:
    """Validate vertical alignment value.

    Args:
        name (str): Name of the argument or attribute being validated.
        value (str): Vertical alignment value to validate.

    Raises:
        ValueError: If value is not one of ["bottom", "center", "top"].

    """
    supported = ["bottom", "center", "top"]
    if value not in supported:
        raise ValueError(f'Arg/Attr {name} must be one of {supported}. But "{value}" is given.')


def validate_xy(arg_name: str, value: Tuple[float, float]) -> None:
    """Validate xy coordinate tuple.

    Args:
        arg_name (str): Name of the argument or attribute being validated.
        value (Tuple[float, float]): Coordinate tuple to validate.

    Raises:
        ValueError: If value is not a tuple of length 2 containing floats or integers.

    """
    message = f'Arg/Attr "{arg_name}" must be (int/float, int/float) format. But "{value}" is given.'

    if not isinstance(value, tuple):
        raise ValueError(message)
    if len(value) != 2:
        raise ValueError(message)

    x, y = value
    for c in [x, y]:
        if not isinstance(c, (float, int)):
            raise ValueError(message)


def validate_xys(arg_name: str, value: List[Tuple[float, float]]) -> None:
    """Validate list of xy coordinate tuples.

    Args:
        arg_name (str): Name of the argument or attribute being validated.
        value (List[Tuple[float, float]]): List of coordinate tuples to validate.

    Raises:
        ValueError: If value is not a list of tuples, or if any tuple does not contain exactly two floats or integers.

    """
    message = f'Arg/Attr "{arg_name}" must be list[tuple[int|float, int|float]] format. But "{value}" is given.'

    if not isinstance(value, list):
        raise ValueError(message)

    for e in value:
        if not isinstance(e, tuple):
            raise ValueError(message)
        if len(e) != 2:
            raise ValueError(message)

        x, y = e
        for c in [x, y]:
            if not isinstance(c, (float, int)):
                raise ValueError(message)


def validate_path_points(  # noqa: C901
    arg_name: str,
    value: List[
        Union[
            Tuple[float, float],
            Tuple[Tuple[float, float], Tuple[float, float]],
            Tuple[Tuple[float, float], Tuple[float, float], Tuple[float, float]],
        ]
    ],
) -> None:
    """Validate path points for complex shapes.

    Args:
        arg_name (str): Name of the argument or attribute being validated.
        value: (
            List[Tuple[float, float] |
                Tuple[Tuple[float, float], Tuple[float, float]] |
                Tuple[Tuple[float, float], Tuple[float, float], Tuple[float, float]]
            ]):
            List of path points to validate.

    Raises:
        ValueError: If value is not a list of tuples conforming to specified formats.

    """
    message = f'Arg/Attr "{arg_name}" must be list[tuple[int|float, ..., int|float]] format. But "{value}" is given.'

    if not isinstance(value, list):
        raise ValueError()

    for path_point in value:
        if not isinstance(path_point, tuple):
            raise ValueError(message)
        if len(path_point) not in {2, 3}:
            raise ValueError(message)

        if isinstance(path_point[0], tuple):
            for p in path_point:
                if not isinstance(p, tuple):
                    raise ValueError(message)

                if not isinstance(p[0], (float, int)):
                    raise ValueError(message)
                if not isinstance(p[1], (float, int)):
                    raise ValueError(message)

        else:
            if not isinstance(path_point[0], (float, int)):
                raise ValueError(message)
            if not isinstance(path_point[1], (float, int)):
                raise ValueError(message)


def validate_angle(arg_name: str, value: Union[int, float]) -> None:
    """Validate angle value.

    Args:
        arg_name (str): Name of the argument or attribute being validated.
        value (Union[int, float]): Angle value to validate.

    Raises:
        ValueError: If value is not an int or float within the range [0, 360].

    """
    message = f'Arg/Attr "{arg_name}" must be int/float 0~360. But "{value}" is given.'

    if not isinstance(value, (float, int)):
        raise ValueError(message)

    if not 0 <= value <= 360:
        raise ValueError(message)


def validate_angle_max90(arg_name: str, value: Union[int, float]) -> None:
    """Validate angle value limited to 0~90 degrees.

    Args:
        arg_name (str): Name of the argument or attribute being validated.
        value (Union[int, float]): Angle value to validate.

    Raises:
        ValueError: If value is not an int or float within the range [0, 90].

    """
    message = f'Arg/Attr "{arg_name}" must be int/float 0~90. But "{value}" is given.'

    if not isinstance(value, (float, int)):
        raise ValueError(message)

    if not 0 <= value <= 90:
        raise ValueError(message)
