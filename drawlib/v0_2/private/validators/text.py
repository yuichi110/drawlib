# Copyright (c) 2024 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Validate text data."""

from typing import Union

from drawlib.v0_2.private.core.fonts import FontBase, FontFile


def validate_font(name: str, value: Union[FontBase, FontFile]) -> None:
    """Validate font.

    Args:
        name (str): Name of the argument or attribute being validated.
        value (Union[FontBase, FontFile]): Font object to validate.

    Raises:
        ValueError: If value is not an instance of FontBase or FontFile.

    """
    message = f'Arg/Attr "{name} must be "instance of FontFile" or "member of Font classes". But "{value}" is given.'

    if isinstance(value, FontBase):
        ...
    elif isinstance(value, FontFile):
        ...
    else:
        raise ValueError(message)
