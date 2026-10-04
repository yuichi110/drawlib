# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Canvas's base class implementation module."""

import math
from typing import Any, Final

import matplotlib
import matplotlib.artist
import matplotlib.font_manager
import matplotlib.lines
import matplotlib.text
import PIL.Image
from matplotlib import pyplot
from pydantic import validate_call

from drawlib._core.l2_types import (
    Alpha,
    Angle,
    Coordinate,
    ImageZoom,
    PosFloat,
    PosInt,
    Size,
)
from drawlib._core.l3_colors import (
    ColorType,
)
from drawlib._core.l3_styles import (
    Style,
)

matplotlib.rcParams["svg.fonttype"] = "none"
matplotlib.rcParams["svg.hashsalt"] = "drawlib"


class CanvasBase:
    """Base class for Canvas and its features.

    This class is designed for diamond inheritance.

    """

    DEFAULT_WIDTH: Final[int] = 100
    DEFAULT_HEIGHT: Final[int] = 100
    DEFAULT_DPI: Final[int] = 100
    DEFAULT_GRID: Final[bool] = False
    DEFAULT_GRID_ONLY: Final[bool] = False
    DEFAULT_GRID_STYLE: Final[Style] = Style(line_width=1, line_color=(128, 128, 128), line_style="dashed")
    DEFAULT_GRID_CENTERSTYLE: Final[Style] = Style(line_width=2, line_color=(128, 128, 128), line_style="dashed")
    FIGURE_WIDTH_INCHES: Final[float] = 10.0
    POINTS_PER_INCH: Final[float] = 72.0

    def __init__(self) -> None:
        """Initialize Canvas instance with default parameters.

        Not only on first initialization, this method is called from `clear()`.
        Variables are updated via `config()`.

        Returns:
            None

        """
        self._width = self.DEFAULT_WIDTH
        self._height = self.DEFAULT_HEIGHT
        self._dpi = self.DEFAULT_DPI
        self._background_color: ColorType | None = None
        self._background_alpha: Alpha | None = None
        self._grid = self.DEFAULT_GRID
        self._grid_only = self.DEFAULT_GRID_ONLY
        self._grid_style = self.DEFAULT_GRID_STYLE
        self._grid_centerstyle = self.DEFAULT_GRID_CENTERSTYLE
        self._grid_xpitch: PosInt | None = None
        self._grid_ypitch: PosInt | None = None
        self._artists: list[matplotlib.artist.Artist] = []
        self._active_animation: Any | None = None

        # it is decleared only for typing system
        self._fig = pyplot.figure()
        self._ax = self._fig.add_subplot(1, 1, 1)

        # initialize fig and ax
        self.setup()

    @validate_call
    def clear(self) -> None:
        """Initialize drawlib Canvas state and configuration.

        Initialize drawlib Canvas.
        It will reset parameters set by `config()` and clear all drawing states.

        Returns:
            None

        Note:
            `clear()` resets all canvas parameters and drawing states to system defaults.

        """
        pyplot.close()
        CanvasBase.__init__(self)  # noqa: PLC2801

    @validate_call
    def setup(  # noqa: C901
        self,
        width: PosInt | None = None,
        height: PosInt | None = None,
        dpi: PosInt | None = None,
        color: ColorType | None = None,
        alpha: Alpha | None = None,
        background_color: ColorType | None = None,
        background_alpha: Alpha | None = None,
        grid: bool | None = None,
        grid_only: bool | None = None,
        grid_style: Style | None = None,
        grid_centerstyle: Style | None = None,
        grid_xpitch: PosInt | None = None,
        grid_ypitch: PosInt | None = None,
    ) -> None:
        """Configure drawlib Canvas parameters.

        Configures drawlib canvas parameters.
        Parameters will be reset when `clear()` method is called.
        This method can be called multiple times to update configuration.

        Args:
            width (int | None): Width of the canvas.
            height (int | None): Height of the canvas.
            dpi (int | None): Output image resolution.
            color (Color | tuple[int, int, int] | tuple[int, int, int, float] | str | None):
                Canvas background color.
            alpha (float | None): Canvas background alpha (opacity).
            background_color (Color | tuple[int, int, int] | tuple[int, int, int, float] | str | None):
                Canvas background color (alias for color).
            background_alpha (float | None): Canvas background alpha (alias for alpha).
            grid (bool | None): Show grid for checking coordinates.
            grid_only (bool | None): Show grid only.
            grid_style (Style | None): Style of grid lines.
            grid_centerstyle (Style | None): Style of center grid lines.
            grid_xpitch (int | None): X-axis grid pitch.
            grid_ypitch (int | None): Y-axis grid pitch.

        Returns:
            None

        Raises:
            RuntimeError: If `setup()` is called after drawing, which could disrupt drawing states.

        Note:
            Changing canvas parameters after drawing operations (`shape()`, `rectangle()`, etc.)
            may lead to unexpected behavior and should be avoided.
            Call `setup()` again after `clear()` if you wish to reconfigure canvas settings.
        """
        # This method config() can be called repeatedly.
        # Please don't set default value in args
        # Default values should be set at __init__() and load them via calling clear().

        if len(self._artists) != 0:
            self._artists = []

        def config_size_dpi() -> None:
            if width is not None:
                self._width = width
            if height is not None:
                self._height = height
            if dpi is not None:
                self._dpi = dpi

            # set fig size. width is always FIGURE_WIDTH_INCHES (10.0 inches)
            fig_width = self.FIGURE_WIDTH_INCHES
            fig_hight = self._height * self.FIGURE_WIDTH_INCHES / self._width
            self._fig = pyplot.figure(
                figsize=(fig_width, fig_hight),
                dpi=self._dpi,
            )

            # set ax size
            self._ax = self._fig.add_subplot(1, 1, 1)
            self._ax.set_xlim(0, self._width)
            self._ax.set_ylim(0, self._height)
            self._ax.set_aspect("equal")
            self._ax.axis("off")
            self._ax.margins(0, 0)

        def config_background() -> None:
            resolved_color = color if color is not None else background_color
            if resolved_color is not None:
                self._background_color = resolved_color
            resolved_alpha = alpha if alpha is not None else background_alpha
            if resolved_alpha is not None:
                self._background_alpha = resolved_alpha

        def config_grid() -> None:
            if grid_style is not None:
                self._grid = True
                self._grid_style = grid_style
                if grid_centerstyle is None:
                    self._grid_centerstyle = grid_style

            if grid_centerstyle is not None:
                self._grid = True
                self._grid_centerstyle = grid_centerstyle

            if grid_only is not None:
                self._grid_only = grid_only
                if grid_only:
                    self._grid = True

            if grid_xpitch is not None:
                self._grid_xpitch = grid_xpitch

            if grid_ypitch is not None:
                self._grid_ypitch = grid_ypitch

            if grid is not None:
                self._grid = grid

            # grid is drawn at method _render()

        pyplot.close()
        config_size_dpi()
        config_background()
        config_grid()

    def _calculate_image_zoom(
        self,
        image_width: PosFloat,
        width: PosFloat,
    ) -> ImageZoom:
        """Calculate the Matplotlib OffsetImage zoom factor for target canvas width.

        Args:
            image_width (float): Original image width in pixels.
            width (float): Target width on canvas logical coordinates.

        Returns:
            float: Zoom factor for OffsetImage.

        Notes:
            Matplotlib OffsetImage treats input image pixels as points (1/72 inch).
            Figure width is fixed to FIGURE_WIDTH_INCHES (10.0 inches), so total points across the canvas width
            is POINTS_PER_INCH * FIGURE_WIDTH_INCHES (720.0 pt).
            The target width in points is:
                target_points = total_canvas_points * (width / self._width)
            The required zoom factor is therefore:
                zoom = target_points / image_width
            Note on DPI:
                DPI scaling is handled automatically by Matplotlib's rasterizer at save/render time
                (1 pt = dpi / 72 px). Therefore, DPI must NOT be multiplied into zoom.
        """
        total_canvas_points = self.POINTS_PER_INCH * self.FIGURE_WIDTH_INCHES
        target_points = total_canvas_points * (width / self._width)
        zoom = target_points / image_width
        return zoom

    @validate_call
    def get_charwidth_from_fontsize(
        self,
        size: PosFloat,
    ) -> float:
        """Calculate the character width based on the font size.

        This method calculates the width of a character using a given font size.
        The calculation is currently based on a magic number which may need to be
        adjusted for better accuracy in the future.

        Args:
            size (float): The font size for which to calculate the character width.

        Returns:
            float: The calculated character width.
        """
        # Notes:
        #     The `magic_number` used in the calculation is currently set to 460, but
        #     this is a placeholder and may require a more accurate calculation.
        #
        # Todo:
        #     - Improve the calculation of the `magic_number` for more accurate results.

        magic_number = 460  # todo: requires better calcuration
        width = size * 0.72 * self._width / magic_number
        return width

    @validate_call
    def get_fontsize_from_charwidth(
        self,
        width: PosFloat,
    ) -> float:
        """Calculate the font size based on the character width.

        This method calculates the font size required to achieve a given character width.
        The calculation is currently based on a magic number which may need to be adjusted
        for better accuracy in the future.

        Args:
            width (float): The character width for which to calculate the font size.

        Returns:
            float: The calculated font size.
        """
        # Notes:
        #     The `magic_number` used in the calculation is currently set to 540, but
        #     this is a placeholder and may require a more accurate calculation.
        #
        # Todo:
        #     - Improve the calculation of the `magic_number` for more accurate results.
        magic_number = 540  # todo: requires better calcuration
        size = magic_number * width / 0.72 / self._width
        return int(size)


__all__ = ["CanvasBase"]
