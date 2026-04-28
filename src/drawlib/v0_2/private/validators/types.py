# Copyright (c) 2024 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Validate primitive data types."""

from typing import Union


def validate_bool(arg_name: str, value: bool) -> None:
    """Validate boolean value.

    Args:
        arg_name (str): Name of the argument or attribute being validated.
        value (bool): Boolean value to validate.

    Raises:
        ValueError: If value is not a boolean.

    """
    message = f'Arg/Attr "{arg_name}" must be bool. But "{value}" is given.'

    if not isinstance(value, bool):
        raise ValueError(message)


def validate_plus_int(arg_name: str, value: int, is_0_ok: bool = True) -> None:
    """Validate integer value that is greater than or equal to zero.

    Args:
        arg_name (str): Name of the argument or attribute being validated.
        value (int): Integer value to validate.
        is_0_ok (bool, optional): Whether zero is an acceptable value (default is True).

    Raises:
        ValueError: If value is not an integer or does not meet the specified conditions.

    """
    if not isinstance(value, int):
        raise ValueError(f'Arg/Attr "{arg_name}" must be int >= 0. But "{value}" is given.')

    if not is_0_ok:
        if 0 >= value:
            raise ValueError(f'Arg/Attr "{arg_name}" must be int > 0. But "{value}" is given.')


def validate_plus_float(arg_name: str, value: Union[int, float], is_0_ok: bool = True) -> None:
    """
    Validate float or integer value that is greater than or equal to zero.

    Args:
        arg_name (str): Name of the argument or attribute being validated.
        value (Union[int, float]): Float or integer value to validate.
        is_0_ok (bool, optional): Whether zero is an acceptable value (default is True).

    Raises:
        ValueError: If value is not a float or integer, or does not meet the specified conditions.

    """
    if not isinstance(value, (int, float)):
        raise ValueError(f'Arg/Attr "{arg_name}" must be int/float >= 0. But "{value}" is given.')

    if not is_0_ok:
        if 0 >= value:
            raise ValueError(f'Arg/Attr "{arg_name}" must be int/float > 0. But "{value}" is given.')


def validate_float_0_to_1(name: str, value: int) -> None:
    """Validate float or integer value that is between 0.0 and 1.0.

    Args:
        name (str): Name of the argument or attribute being validated.
        value (int): Float or integer value to validate.

    Raises:
        ValueError: If value is not a float or integer, or does not meet the specified range conditions.

    """
    message = f'Arg/Attr "{name}" must be between 0.0~1.0. But "{value}" is given.'

    if not isinstance(value, (int, float)):
        raise ValueError(message)

    if not 0.0 <= value <= 1.0:
        raise ValueError(message)


def validate_plusminus_float_or_none(arg_name: str, value: Union[int, float, None]) -> None:
    """Validate integer or float value, or None.

    Args:
        arg_name (str): Name of the argument or attribute being validated.
        value (Union[int, float, None]): Integer, float, or None value to validate.

    Raises:
        ValueError: If value is not an integer, float, or None.

    """
    message = f'Arg/Attr "{arg_name}" must be int/float. But "{value}" is given.'

    if value is None:
        ...
    elif not isinstance(value, (int, float)):
        raise ValueError(message)


def validate_str(arg_name: str, value: str) -> None:
    """Validate string value.

    Args:
        arg_name (str): Name of the argument or attribute being validated.
        value (str): String value to validate.

    Raises:
        ValueError: If value is not a string.

    """
    message = f'Arg/Attr "{arg_name}" must be str. But "{value}" is given.'

    if not isinstance(value, str):
        raise ValueError(message)
