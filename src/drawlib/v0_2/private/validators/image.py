# Copyright (c) 2024 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Validate image data."""

from typing import Union

from PIL.Image import Image

from drawlib.v0_2.private.core.dimage import Dimage


def validate_image(arg_name: str, value: Union[str, Image, Dimage]) -> None:
    """Validate image data.

    Args:
        arg_name (str): Name of the argument or attribute being validated.
        value (Union[str, PIL.Image.Image, Dimage]): Value to validate as image data.

    Raises:
        ValueError: If value is not a string, PIL.Image.Image object, or Dimage object.
    """
    message = f'Arg/Attr "{arg_name}" requires str or PIL.Image.Image or ShapeTextStyle. But "{value}" is given.'

    if not isinstance(value, (str, Image, Dimage)):
        raise ValueError(message)
