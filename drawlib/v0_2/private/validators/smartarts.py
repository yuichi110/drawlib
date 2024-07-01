# Copyright (c) 2024 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Validate smart art data."""


def validate_tail_edge(name: str, value: str) -> None:
    """Validate tail edge for smart art.

    Args:
        name (str): Name of the argument or attribute being validated.
        value (str): Tail edge value to validate.

    Raises:
        ValueError: If value is not one of ["left", "top", "right", "bottom"].
    """
    supported = ["left", "top", "right", "bottom"]
    message = f'Arg/Attr "{name}" must be one of {supported}. But "{value}" is given.'

    if value not in supported:
        raise ValueError(message)
