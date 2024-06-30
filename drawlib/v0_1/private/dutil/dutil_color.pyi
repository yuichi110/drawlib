"""
This type stub file was generated by pyright.
"""

import typing
import drawlib.v0_1.private.util

"""Color related utilities."""
@drawlib.v0_1.private.util.error_handler
def get_rgba(rgb: typing.Tuple[int, int, int], alpha: float) -> typing.Tuple[int, int, int, float]:
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
    ...

@drawlib.v0_1.private.util.error_handler
def get_rgba_from_hexcode(hexcode: str, alpha: typing.Optional[float] = ...) -> typing.Tuple[int, int, int, float]:
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
    ...

@drawlib.v0_1.private.util.error_handler
def get_rgba_from_grayscale(grayscale: float, alpha: float = ...) -> typing.Tuple[int, int, int, float]:
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
    ...

