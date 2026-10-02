# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Color utility module for canvas operations."""

from drawlib._core.l2_types import (
    Color,
    ColorRGBA,
    ColorType,
)


class ColorUtil:
    """A utility class for color conversion operations."""

    def __init__(self) -> None:
        """Raise TypeError to prevent instantiation of utility class."""
        raise TypeError(f"'{self.__class__.__name__}' is a static utility class and cannot be instantiated.")

    @staticmethod
    def get_mplot_rgba(
        rgb_or_rgba: ColorType,
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
        if isinstance(rgb_or_rgba, dict):
            rgb_or_rgba = Color(**rgb_or_rgba)

        if isinstance(rgb_or_rgba, Color):
            if alpha is not None:
                return (
                    round(rgb_or_rgba.r / 255.0, 5),
                    round(rgb_or_rgba.g / 255.0, 5),
                    round(rgb_or_rgba.b / 255.0, 5),
                    alpha,
                )
            return rgb_or_rgba.to_mplot_rgba()

        if isinstance(rgb_or_rgba, str):
            rgba = ColorUtil.get_rgba_from_hex(rgb_or_rgba)
            r = round(rgba[0] / 255, 5)
            g = round(rgba[1] / 255, 5)
            b = round(rgba[2] / 255, 5)
            a = alpha if alpha is not None else rgba[3]
            return (r, g, b, a)

        r = round(rgb_or_rgba[0] / 255, 5)
        g = round(rgb_or_rgba[1] / 255, 5)
        b = round(rgb_or_rgba[2] / 255, 5)

        if alpha is not None:
            a = alpha
        elif len(rgb_or_rgba) == 4:
            a = float(rgb_or_rgba[-1])
        else:
            a = 1.0

        return (r, g, b, a)

    @staticmethod
    def get_hexrgb(
        rgb_or_rgba: ColorType,
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
        if isinstance(rgb_or_rgba, dict):
            rgb_or_rgba = Color(**rgb_or_rgba)
        if isinstance(rgb_or_rgba, Color):
            return rgb_or_rgba.hex
        if isinstance(rgb_or_rgba, str):
            return rgb_or_rgba
        r = rgb_or_rgba[0]
        g = rgb_or_rgba[1]
        b = rgb_or_rgba[2]
        if not (0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255):
            raise ValueError("RGB values must be in the range 0 to 255.")
        hex_color = f"#{r:02x}{g:02x}{b:02x}"
        return hex_color

    @staticmethod
    def get_rgba_from_hex(hex_color: str) -> ColorRGBA:
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

    @staticmethod
    def get_luminance(
        rgb_or_rgba: ColorType,
    ) -> float:
        """Calculate relative luminance (0.0 to 1.0) using standard ITU-R BT.601 weights.

        Args:
            rgb_or_rgba: Color specification (Color instance, hex string, or RGB/RGBA tuple).

        Returns:
            float: Relative luminance value in range [0.0, 1.0].
        """
        rgba = ColorUtil.get_mplot_rgba(rgb_or_rgba)
        return 0.299 * rgba[0] + 0.587 * rgba[1] + 0.114 * rgba[2]

    @staticmethod
    def get_contrast_text_color(
        bg_color: ColorType | None,
        bg_alpha: float | None = None,
        *,
        dark_color: ColorType = (40, 40, 40, 1.0),
        light_color: ColorType = (255, 255, 255, 1.0),
        transparent_color: ColorType | None = None,
        threshold: float = 0.6,
        alpha_threshold: float = 0.3,
    ) -> ColorType:
        """Determine contrasting text color (dark or light) based on background luminance.

        Returns transparent_color (or dark_color if transparent_color is None) when the background
        is None, fully transparent, or has alpha below alpha_threshold.
        Otherwise calculates ITU-R BT.601 luminance and compares with threshold.

        Args:
            bg_color: Background color specification, or None if transparent.
            bg_alpha: Optional alpha override for the background.
            dark_color: Color to return against bright backgrounds. Defaults to (40, 40, 40, 1.0).
            light_color: Color to return against dark backgrounds. Defaults to (255, 255, 255, 1.0).
            transparent_color: Optional color to return when background is transparent.
                If None, dark_color is returned.
            threshold: Luminance threshold (0.0 to 1.0) above which dark_color is selected. Defaults to 0.6.
            alpha_threshold: Alpha threshold below which background is treated as transparent. Defaults to 0.3.

        Returns:
            ColorType: The contrasting text color.
        """
        fallback_transparent = transparent_color if transparent_color is not None else dark_color
        if bg_color is None:
            return fallback_transparent

        rgba = ColorUtil.get_mplot_rgba(bg_color, bg_alpha)
        if rgba[3] < alpha_threshold or rgba == (0.0, 0.0, 0.0, 0.0):
            return fallback_transparent

        lum = 0.299 * rgba[0] + 0.587 * rgba[1] + 0.114 * rgba[2]
        return dark_color if lum > threshold else light_color
