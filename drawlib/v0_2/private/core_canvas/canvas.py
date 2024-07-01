# Copyright (c) 2024 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.


"""Canvas implementation module."""

import os
from typing import Literal, Optional

from matplotlib import pyplot

import drawlib.v0_2.private.validators.args as validator
from drawlib.v0_2.private.core.theme import dtheme
from drawlib.v0_2.private.core.util import ColorUtil
from drawlib.v0_2.private.core_canvas.image import CanvasImageFeature
from drawlib.v0_2.private.core_canvas.line import CanvasLineFeature
from drawlib.v0_2.private.core_canvas.original_arrow import CanvasOriginalArrowFeature
from drawlib.v0_2.private.core_canvas.original_polygon import CanvasOriginalPolygonFeature
from drawlib.v0_2.private.core_canvas.patches import CanvasPatchesFeature
from drawlib.v0_2.private.core_canvas.text import CanvasTextFeature
from drawlib.v0_2.private.util import (
    error_handler,
    get_script_path,
    get_script_relative_path,
)


class Canvas(
    CanvasImageFeature,
    CanvasLineFeature,
    CanvasOriginalPolygonFeature,
    CanvasOriginalArrowFeature,
    CanvasPatchesFeature,
    CanvasTextFeature,
):
    """Drawlib's canvas class.

    This class provides functionality to draw various shapes, images, lines,
    text, and apply patches on a matplotlib canvas. It supports saving the
    canvas to various image formats.
    """

    def __init__(self) -> None:
        """Initializes a Canvas object.

        Initializes an instance of Canvas by calling the constructors of its
        superclass features: CanvasImageFeature, CanvasLineFeature,
        CanvasOriginalPolygonFeature, CanvasOriginalArrowFeature,
        CanvasPatchesFeature, and CanvasTextFeature.
        """
        super().__init__()

    @error_handler
    def save(
        self,
        file: Optional[str] = None,
        format: Optional[Literal["jpg", "png", "webp", "pdf"]] = None,
    ) -> None:
        """Save canvas illustration to file.

        Args:
            file (optional): File path to save the image. Default is "<script-name>.png".
            format (optional): Image format to save. Default is "png".

        Returns:
            None

        Notes:
            If no arguments are provided, the canvas is saved as "<scriptfilename>.png"
            in the script's directory. For example, calling save() in a script "mydir/image1.py"
            will generate "mydir/image1.png".
        """
        validator.validate_canvas_args(locals())

        file_path = self._get_save_file_path(file, format)
        self._set_background()
        zorder = self._draw_items()
        self._remove_margin()
        self._create_parent_directory(file_path)

        # save normal image
        if self._grid_only:
            # does not save normal image
            ...
        else:
            pyplot.savefig(file_path)
            if not self._grid:
                self._remove_artists_from_ax()  # remove drawing items
                return

        temp_artists = self._artists
        self._artists = []
        self._draw_grid(zorder)

        # save grid image
        if self._grid_only:
            pyplot.savefig(file_path)
        else:
            name, extension = os.path.splitext(file_path)
            grid_image_file_path = f"{name}_grid{extension}"
            pyplot.savefig(grid_image_file_path)

        self._remove_artists_from_ax()  # remove grid
        self._artists = temp_artists
        self._remove_artists_from_ax()  # remove drawing items

    def _remove_artists_from_ax(self) -> None:
        """Remove all artists from the axis.

        This method iterates over the list of artists stored in the instance
        and removes each one from the axis. This is typically used to clear
        the current plot by removing all plot elements that were previously
        added.

        Returns:
            None
        """
        for artist in self._artists:
            artist.remove()

    @staticmethod
    def _get_save_file_path(file: Optional[str], format: Optional[str]) -> str:
        """Get the file path for saving the canvas.

        Args:
            file (str): File path to save the image.
            format (str): Image format to save.

        Returns:
            str: File path to save the canvas.
        """
        if file is None:
            script_path = get_script_path()
            parent_dir = os.path.dirname(script_path)
            name = os.path.basename(script_path)
            name_without_ext = os.path.splitext(name)[0]
            ext = "png" if format is None else format
            file_path = f"{os.path.join(parent_dir, name_without_ext)}.{ext}"

        else:
            file_path = get_script_relative_path(file)

        return file_path

    def _set_background(self) -> None:
        """Set the background color and alpha of the canvas."""
        has_color_alpha = False
        if self._background_color is not None:
            background_color = self._background_color
            if len(background_color) == 4:
                has_color_alpha = True
        else:
            background_color = dtheme.backgroundcolors.get()

        if self._background_alpha is not None:
            background_alpha = self._background_alpha
        elif has_color_alpha:
            # set user specified alpha in color as alpha-value
            background_alpha = background_color[3]  # type: ignore
        else:
            _, _, _, alpha = dtheme.backgroundcolors.get()
            background_alpha = alpha

        mplot_rgba = ColorUtil.get_mplot_rgba(background_color, background_alpha)
        self._fig.patch.set_facecolor(mplot_rgba)
        self._ax.patch.set_alpha(0)

    def _draw_items(self) -> int:
        """Draw all the items (shapes, lines, text, etc.) on the canvas.

        Returns:
            int: Z-order of the last drawn item.
        """
        zorder = 0
        for artist in self._artists:
            artist.zorder = zorder
            zorder += 1
            self._ax.add_artist(artist)
        return zorder

    def _remove_margin(self) -> None:
        """Remove the margins from the canvas."""
        self._fig.tight_layout()
        self._fig.subplots_adjust(left=0, right=1, bottom=0, top=1)

    @staticmethod
    def _create_parent_directory(file_path: str) -> None:
        """Create the parent directory for the save file path.

        Args:
            file_path (str): File path to save the image.
        """
        directory = os.path.dirname(file_path)
        os.makedirs(name=directory, exist_ok=True)

    def _draw_grid(self, zorder: int) -> None:
        """Draw grid lines on the canvas.

        Args:
            zorder (int): Z-order of the grid lines.
        """
        center_x = self._width / 2
        center_y = self._height / 2

        # get pitchs
        if self._grid_xpitch is None:
            xpitch = self._width / 10
        else:
            xpitch = self._grid_xpitch

        if self._grid_ypitch is None:
            ypitch = self._height / 10
        else:
            ypitch = self._grid_ypitch

        # create vertical grid lines
        i = 1
        while True:
            x = i * xpitch
            if x >= self._width:
                break
            if x != center_x:
                self.line((x, 0), (x, self._height), style=self._grid_style)
            i += 1

        # create horizontal lines
        i = 1
        while True:
            y = i * ypitch
            if y >= self._height:
                break
            if y != center_y:
                self.line((0, y), (self._width, y), style=self._grid_style)
            i += 1

        # create center grid lines
        self.line((center_x, 0), (center_x, self._height), style=self._grid_centerstyle)
        self.line((0, center_y), (self._width, center_y), style=self._grid_centerstyle)

        # draw grid lines
        for artist in self._artists:
            artist.zorder = zorder
            zorder += 1
            self._ax.add_artist(artist)


canvas = Canvas()

# basics
clear = canvas.clear
config = canvas.config
save = canvas.save
shape = canvas.shape

# image
image = canvas.image

# line
line = canvas.line
line_curved = canvas.line_curved
line_bezier1 = canvas.line_bezier1
line_bezier2 = canvas.line_bezier2
lines = canvas.lines
lines_curved = canvas.lines_curved
lines_bezier = canvas.lines_bezier

# original
rhombus = canvas.rhombus
trapezoid = canvas.trapezoid
parallelogram = canvas.parallelogram
triangle = canvas.triangle
arrow = canvas.arrow
star = canvas.star
chevron = canvas.chevron

# patches
arc = canvas.arc
circle = canvas.circle
ellipse = canvas.ellipse
polygon = canvas.polygon
rectangle = canvas.rectangle
regularpolygon = canvas.regularpolygon
wedge = canvas.wedge
donuts = canvas.donuts
fan = canvas.fan

# text
text = canvas.text
text_vertical = canvas.text_vertical

# dutil
get_image_zoom_original = canvas.get_image_zoom_original
get_image_zoom_from_width = canvas.get_image_zoom_from_width
get_charwidth_from_fontsize = canvas.get_charwidth_from_fontsize
get_fontsize_from_charwidth = canvas.get_fontsize_from_charwidth
