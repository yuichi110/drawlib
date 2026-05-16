# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Color utility module for canvas operations."""

from drawlib.v0_2.private.l2_models import (
    StaticContainer,
)
from drawlib.v0_2.private.l2_types import (
    TypeColor,
    TypeColorRGBA,
)


class ColorUtil(StaticContainer):
    """A utility class for color conversion operations."""

    @staticmethod
    def get_mplot_rgba(
        rgb_or_rgba: TypeColor,
        alpha: float | None = None,
    ) -> tuple[float, float, float, float]:
        """Convert 0~255 RGB/RGBA to 0.0 ~ 1.0 RGBA for matplotlib.

        drawlib prefers 0~255 RGB/RGBA.
        matplotlib uses 0.0~1.0 RGB/RGBA.

        This function provides a converter from drawlib format to matplotlib format.
        The alpha channel is handled as follows:

        1. If the `alpha` argument is provided, use it.
        2. If the original data is RGBA, use its alpha value.
        3. Set alpha to 1.0 if not provided.

        Args:
            rgb_or_rgba (Color):
                RGB or RGBA color tuple where components are in the range 0 to 255.
                If RGBA, the alpha component should be in the range 0.0 to 1.0.
            alpha (float | None): Optional alpha value to override the input alpha.

        Returns:
            tuple[float, float, float, float]: Tuple representing matplotlib's RGBA format.
        """
        r = round(rgb_or_rgba[0] / 255, 5)
        g = round(rgb_or_rgba[1] / 255, 5)
        b = round(rgb_or_rgba[2] / 255, 5)

        if alpha is not None:
            a = alpha
        elif len(rgb_or_rgba) == 3:
            a = 1.0
        else:
            a = rgb_or_rgba[3]  # type: ignore

        return (r, g, b, a)

    @staticmethod
    def get_hexrgb(
        rgb_or_rgba: TypeColor,
    ) -> str:
        """Convert RGB or RGBA tuple to hexadecimal color code.

        Args:
            rgb_or_rgba (Color):
                RGB or RGBA color tuple where components are in the range 0 to 255.
                If RGBA, the alpha component should be in the range 0.0 to 1.0.

        Returns:
            str: Hexadecimal color code in the format "#RRGGBB" or "#RRGGBBAA" (if alpha < 1.0).

        Raises:
            ValueError: If RGB values are out of range (0-255).
        """
        r = rgb_or_rgba[0]
        g = rgb_or_rgba[1]
        b = rgb_or_rgba[2]
        if not (0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255):
            raise ValueError("RGB values must be in the range 0 to 255.")
        hex_color = f"#{r:02x}{g:02x}{b:02x}"
        return hex_color

    @staticmethod
    def get_rgba_from_hex(hex_color: str) -> TypeColorRGBA:
        """Convert a hexadecimal color code to RGBA values.

        Args:
            hex_color (str): The hexadecimal color code (e.g., "#FF5733" or "#FFF").

        Returns:
            ColorRGBA: A tuple containing the RGBA values (0-255 for R, G, B and 0.0-1.0 for A).

        Raises:
            ValueError: If the hex_color format is invalid.
        """
        # Remove the '#' prefix if present
        hex_color = hex_color.lstrip("#")

        # Determine the length of the hex color code
        hex_length = len(hex_color)

        # Convert the hex code to RGB values
        if hex_length == 3:  # Short hex format (#RGB)
            r = int(hex_color[0] * 2, 16)
            g = int(hex_color[1] * 2, 16)
            b = int(hex_color[2] * 2, 16)
            a = 1.0
        elif hex_length in {6, 8}:  # Full hex format (#RRGGBB)
            r = int(hex_color[0:2], 16)
            g = int(hex_color[2:4], 16)
            b = int(hex_color[4:6], 16)
            if hex_length == 8:  # With alpha
                a = int(hex_color[6:8], 16)
            else:
                a = 1.0
        else:
            raise ValueError("Invalid hex color code format")

        return (r, g, b, a)
