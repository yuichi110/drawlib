# Copyright (c) 2024 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Validate color data."""

from typing import Tuple, Union


def validate_alpha(name: str, value: float) -> None:
    """Validate alpha transparency value.

    Args:
        name (str): Name of the argument or attribute being validated.
        value (float): Alpha value to validate.

    Raises:
        ValueError: If value is not a float or integer, or if it is not within the range [0.0, 1.0].
    """
    message = f'Arg/Attr "{name}" must be between 0.0~1.0. But "{value}" is given.'

    if not isinstance(value, (float, int)):
        raise ValueError(message)

    if not 0.0 <= value <= 1.0:
        raise ValueError(message)


def validate_color(
    name: str,
    value: Union[Tuple[int, int, int], Tuple[int, int, int, float]],
) -> None:
    """Validate RGB or RGBA color tuple.

    Args:
        name (str): Name of the argument or attribute being validated.
        value (Union[Tuple[int, int, int], Tuple[int, int, int, float]]): Color tuple to validate.

    Raises:
        ValueError: If value is not a tuple, if its length is not 3 or 4,
                    if RGB values are not integers within [0, 255],
                    or if alpha value (if present) is not a float within [0.0, 1.0].
    """
    message = (
        f'Arg/Attr "{name}" must be (R, G, B) or (R, G, B, A). '
        f'Where RGB is int 0~255 and A is float 0.0~1.0. But "{value}" is given.'
    )

    if not isinstance(value, tuple):
        raise ValueError(message)
    if len(value) not in {3, 4}:
        raise ValueError(message)

    r = value[0]
    g = value[1]
    b = value[2]
    for c in [r, g, b]:
        if not isinstance(c, int):
            raise ValueError(message)
        if not 0 <= c <= 255:
            raise ValueError(message)
    if len(value) == 3:
        return

    a = value[3]
    if not isinstance(a, (float, int)):
        raise ValueError(message)

    if not 0.0 <= a <= 1.0:
        raise ValueError(message)
