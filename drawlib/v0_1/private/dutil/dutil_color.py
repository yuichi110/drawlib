# Copyright (c) 2024 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Color related utilities."""

import typing

import drawlib.v0_1.private.util
import drawlib.v0_1.private.validators.color as color_validator


@drawlib.v0_1.private.util.error_handler
def get_rgba(
    rgb: typing.Tuple[int, int, int],
    alpha: float,
) -> typing.Tuple[int, int, int, float]:
    """
    Convert an RGB color to an RGBA color by adding an alpha (transparency) channel.

    Args:
        rgb (tuple[int, int, int]): The RGB color as a tuple of three integers.
            Each integer should be in the range 0 to 255, representing the red, green,
            and blue channels respectively.
        alpha (float): The alpha (transparency) value as a float.
            Should be in the range 0.0 to 1.0, where 0.0 is fully transparent
            and 1.0 is fully opaque.

    Returns:
        tuple[int, int, int, float]: The RGBA color as a tuple of three integers
        followed by a float, representing the red, green, blue, and alpha channels
        respectively.

    """
    color_validator.validate_color("rgb", rgb)
    color_validator.validate_alpha("alpha", alpha)

    return (rgb[0], rgb[1], rgb[2], alpha)


@drawlib.v0_1.private.util.error_handler
def get_rgba_from_hexcode(
    hexcode: str,
    alpha: typing.Optional[float] = None,
) -> typing.Tuple[int, int, int, float]:
    """
    Convert a hexadecimal color code to an RGBA color tuple.

    The priority for determining the alpha (transparency) value is as follows:
    1. If an alpha value is provided as an argument, it will be used.
    2. If the hex code contains an alpha channel, it will be used.
    3. If neither of the above is true, the default alpha value of 1.0 (fully opaque) will be used.

    Args:
        hexcode (str): A string representing the color in hexadecimal format.
                        This can be an RGB format (e.g., "#00FF00") or an RGBA format (e.g., "#00FF00FF").
        alpha (float, optional): An optional alpha value to override the default or hex code alpha value.
                                    This should be a float between 0.0 (fully transparent) and 1.0 (fully opaque).

    Returns:
        Tuple[int, int, int, float]: A tuple representing the RGBA color, where the first three elements
                                        are integers (0 to 255) representing the red, green, and blue channels,
                                        and the fourth element is a float representing the alpha channel.
    """
    try:
        hex_code = hexcode.lstrip("#")
        length = len(hex_code)
        r = int(hex_code[0:2], 16)
        g = int(hex_code[2:4], 16)
        b = int(hex_code[4:6], 16)

        if length == 6:
            a = 1.0
        else:
            a = int(hex_code[6:8], 16) / 255

        if alpha is not None:
            a = alpha

    except Exception as e:
        raise ValueError("Converting hex color code failed. Please check hex format.") from e

    return (r, g, b, a)


@drawlib.v0_1.private.util.error_handler
def get_rgba_from_grayscale(
    grayscale: float,
    alpha: float = 1.0,
) -> typing.Tuple[int, int, int, float]:
    """
    Convert a grayscale value to an RGBA color tuple.

    Args:
        grayscale (float): A float representing the grayscale value.
                            Should be in the range 0.0 (black) to 1.0 (white).
        alpha (float, optional): A float representing the alpha (transparency) value.
                                    Should be in the range 0.0 (fully transparent) to 1.0 (fully opaque).
                                    Defaults to 1.0 if not provided.

    Returns:
        tuple[int, int, int, float]: A tuple representing the RGBA color, where the first three elements
                                        are integers (0 to 255) representing the red, green, and blue channels,
                                        and the fourth element is a float representing the alpha channel.
    """
    rgb = int(grayscale * 255)
    return (rgb, rgb, rgb, alpha)
