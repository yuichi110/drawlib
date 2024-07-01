# Copyright (c) 2024 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Validate image data."""

from typing import Literal


def validate_style(arg_name: str, value: Literal["thin", "light", "regular", "bold", "fill"]) -> None:
    """Validate style data.

    Args:
        arg_name (str): Name of the argument or attribute being validated.
        value (str): Value to validate as string data.

    Raises:
        ValueError: If value is not one of ["thin", "light", "regular", "bold", "fill"].

    """
    supported = ["thin", "light", "regular", "bold", "fill"]
    message = f'Arg/Attr "{arg_name}" requires one of {supported}. But "{value}" is given.'

    if value not in supported:
        raise ValueError(message)
