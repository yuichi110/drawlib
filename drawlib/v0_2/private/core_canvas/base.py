# Copyright (c) 2024 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Canvas's base class implementation module."""

import math
from typing import Final, List, Optional, Tuple, Union

import matplotlib.artist
import matplotlib.font_manager
import matplotlib.lines
import matplotlib.text
import PIL.Image
from matplotlib import pyplot
from matplotlib.patches import PathPatch
from matplotlib.path import Path

import drawlib.v0_2.private.validators.args as validator
from drawlib.v0_2.private.core.colors import Colors
from drawlib.v0_2.private.core.dimage import Dimage
from drawlib.v0_2.private.core.model import (
    LineStyle,
    ShapeStyle,
    ShapeTextStyle,
)
from drawlib.v0_2.private.core.theme import dtheme
from drawlib.v0_2.private.core.util import ShapeUtil
from drawlib.v0_2.private.util import (
    error_handler,
    get_center_and_size,
    minus_2points,
)


class CanvasBase:
    """Base class for Canvas and its features.

    This class is designed for diamond inheritance.

    """

    DEFAULT_WIDTH: Final[int] = 100
    DEFAULT_HEIGHT: Final[int] = 100
    DEFAULT_DPI: Final[int] = 100
    DEFAULT_GRID: Final[bool] = False
    DEFAULT_GRID_ONLY: Final[bool] = False
    DEFAULT_GRID_STYLE: Final[LineStyle] = LineStyle(width=1, color=Colors.Gray, style="dashed")
    DEFAULT_GRID_CENTERSTYLE: Final[LineStyle] = LineStyle(width=2, color=Colors.Gray, style="dashed")

    @error_handler
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
        self._background_color: Union[
            Tuple[int, int, int],
            Tuple[int, int, int, float],
            None,
        ] = None  # apply theme default later if no update
        self._background_alpha: Optional[float] = None  # apply theme default later if no update
        self._grid = self.DEFAULT_GRID
        self._grid_only = self.DEFAULT_GRID_ONLY
        self._grid_style = self.DEFAULT_GRID_STYLE
        self._grid_centerstyle = self.DEFAULT_GRID_CENTERSTYLE
        self._grid_xpitch: Optional[int] = None
        self._grid_ypitch: Optional[int] = None
        self._artists: List[matplotlib.artist.Artist] = []

        # it is decleared only for typing system
        self._fig = pyplot.figure()
        self._ax = self._fig.add_subplot(1, 1, 1)

        # initialize fig and ax
        self.config()

    @error_handler
    def clear(self) -> None:
        """Initialize drawlib Canvas state and configuration.

        Initialize drawlib Canvas.
        It will reset parameters set by `config()` and clear all drawing states.

        Returns:
            None

        Note:
            `clear()` does not reset to theme defaults.
            If you want to reset to default theme, call `config(theme="default")` after `clear()`.

        """
        pyplot.close()
        CanvasBase.__init__(self)  # noqa: PLC2801

    @error_handler
    def config(  # noqa: C901
        self,
        width: Optional[int] = None,
        height: Optional[int] = None,
        dpi: Optional[int] = None,
        background_color: Union[
            Tuple[int, int, int],
            Tuple[int, int, int, float],
            None,
        ] = None,
        background_alpha: Optional[float] = None,
        grid: Optional[bool] = None,
        grid_only: Optional[bool] = None,
        grid_style: Optional[LineStyle] = None,
        grid_centerstyle: Optional[LineStyle] = None,
        grid_xpitch: Optional[int] = None,
        grid_ypitch: Optional[int] = None,
    ) -> None:
        """Configure drawlib Canvas parameters.

        Configures drawlib canvas parameters.
        Parameters will be reset when `clear()` method is called.
        This method can be called multiple times to update configuration.

        Args:
            width (Optional[int]): Width of the canvas.
            height (Optional[int]): Height of the canvas.
            dpi (Optional[int]): Output image resolution.
            background_color (Optional[Union[Tuple[int, int, int], Tuple[int, int, int, float]]]):
                Background color.
            background_alpha (Optional[float]): Background alpha (opacity).
            grid (Optional[bool]): Show grid for checking coordinates.
            grid_only (Optional[bool]): Show grid only.
            grid_style (Optional[LineStyle]): Style of grid lines.
            grid_centerstyle (Optional[LineStyle]): Style of center grid lines.
            grid_xpitch (Optional[int]): X-axis grid pitch.
            grid_ypitch (Optional[int]): Y-axis grid pitch.

        Returns:
            None

        Raises:
            RuntimeError: If `config()` is called after drawing, which could disrupt drawing states.

        Note:
            Changing canvas parameters after drawing operations (`shape()`, `rectangle()`, etc.)
            may lead to unexpected behavior and should be avoided.
            Call `config()` again after `clear()` if you wish to reconfigure canvas settings.
        """
        # This method config() can be called repeatedly.
        # Please don't set default value in args
        # Default values should be set at __init__() and load them via calling clear().

        validator.validate_canvas_args(locals())

        if len(self._artists) != 0:
            raise RuntimeError(
                "config() must be called before drawing. "
                "Please call clear() first if you want to "
                "initialize drawing configs and states."
            )

        def config_size_dpi() -> None:
            if width is not None:
                self._width = width
            if height is not None:
                self._height = height
            if dpi is not None:
                self._dpi = dpi

            # set fig size. width is always 10
            fig_width = 10
            fig_hight = self._height * 10 / self._width
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
            if background_color is not None:
                self._background_color = background_color
            if background_alpha is not None:
                self._background_alpha = background_alpha

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

    #
    # Shape
    #

    @error_handler
    def shape(  # noqa: C901
        self,
        xy: Tuple[float, float],
        path_points: List[
            Union[
                Tuple[float, float],
                Tuple[Tuple[float, float], Tuple[float, float]],
                Tuple[Tuple[float, float], Tuple[float, float], Tuple[float, float]],
            ]
        ],
        angle: float = 0.0,
        style: Union[ShapeStyle, str, None] = None,
        text: str = "",
        textsize: Optional[float] = None,
        textstyle: Optional[ShapeTextStyle] = None,
        is_default_center: bool = False,
    ) -> None:
        """Draw basic shape on the canvas.

        Args:
            xy: Starting point of the shape.
            path_points: List of path points including control points for Bezier curves.
            angle (float, optional): Rotation angle of the shape.
            style (Union[ShapeStyle, str, None], optional): Style of the shape.
            text (str, optional): Text to display along with the shape.
            textsize (Optional[float], optional): Size of the text.
            textstyle (Optional[ShapeTextStyle], optional): Style of the text.
            is_default_center (bool, optional): Whether to place (xy) at the center of the shape.

        Raises:
            ValueError: If invalid path points are provided.
        """
        style, textstyle = ShapeUtil.format_styles(
            style,
            textstyle,
            dtheme.shapestyles.get,
            dtheme.shapetextstyles.get,
        )
        validator.validate_shape_args(locals())
        if textsize is not None:
            textstyle.size = textsize

        # helper

        def get_rotate_point(
            xy: Tuple[float, float], angle: float, move_x: float, move_y: float
        ) -> Tuple[float, float]:
            x = xy[0]
            y = xy[1]
            angle_rad = math.radians(angle)
            x_rotated = x * math.cos(angle_rad) - y * math.sin(angle_rad)
            y_rotated = x * math.sin(angle_rad) + y * math.cos(angle_rad)
            return x_rotated + move_x, y_rotated + move_y

        # shift to center (0, 0)
        points_without_cp = []
        for pp in path_points:
            if not isinstance(pp[0], tuple):
                points_without_cp.append(pp)
            else:
                points_without_cp.append(pp[0])
        center, (width, height) = get_center_and_size(points_without_cp)

        path_points2 = []
        for pp in path_points:
            # (x, y)
            if not isinstance(pp[0], tuple):
                xy1 = minus_2points(pp, center)  # type: ignore
                path_points2.append(xy1)
                continue

            # ((x1, y1), (x2, y2))
            xy1 = minus_2points(pp[0], center)  # type: ignore
            xy2 = minus_2points(pp[1], center)  # type: ignore
            if len(pp) == 2:
                path_points2.append((xy1, xy2))
                continue

            # ((x1, y1), (x2, y2), (x3, y3))
            xy3 = minus_2points(pp[2], center)
            path_points2.append((xy1, xy2, xy3))

        # alignment
        if is_default_center:
            # move to center
            x, y = xy
            x -= width / 2
            y -= height / 2
            xy = (x, y)
        ((x, y), style) = ShapeUtil.apply_alignment(
            xy,
            width,
            height,
            angle,
            style,
            is_default_center=is_default_center,
        )

        # rotate and move
        cx = x + width / 2
        cy = y + height / 2
        path_points3 = []
        for pp in path_points2:
            # (x, y)
            if not isinstance(pp[0], tuple):
                xy1 = get_rotate_point(pp, angle=angle, move_x=cx, move_y=cy)
                path_points3.append(xy1)
                continue

            # ((x1, y1), (x2, y2))
            xy1 = get_rotate_point(pp[0], angle=angle, move_x=cx, move_y=cy)
            xy2 = get_rotate_point(pp[1], angle=angle, move_x=cx, move_y=cy)
            if len(pp) == 2:
                path_points3.append((xy1, xy2))
                continue

            # ((x1, y1), (x2, y2), (x3, y3))
            xy3 = get_rotate_point(pp[2], angle=angle, move_x=cx, move_y=cy)
            path_points3.append((xy1, xy2, xy3))

        # create Path
        vertices = [path_points3[0]]
        codes = [Path.MOVETO]
        for p in path_points3[1:]:
            length = len(p)
            if length not in {2, 3}:
                raise ValueError()

            if not isinstance(p[0], tuple):
                vertices.append(p)
                codes.append(Path.LINETO)

            elif length == 2:
                vertices.extend([p[0], p[1]])
                codes.extend([Path.CURVE3] * 2)

            else:
                vertices.extend([p[0], p[1], p[2]])
                codes.extend([Path.CURVE4] * 3)

        vertices.append(path_points3[0])
        codes.append(Path.CLOSEPOLY)
        path = Path(vertices=vertices, codes=codes)

        # create PathPatch

        options = ShapeUtil.get_shape_options(style)
        self._artists.append(PathPatch(path=path, **options))

        # create Text

        if text is not None:
            self._artists.append(
                ShapeUtil.get_shape_text(
                    xy=(cx, cy),
                    text=text,
                    angle=angle,
                    style=textstyle,
                )
            )

    @error_handler
    def rectangle(
        self,
        xy: Tuple[float, float],
        width: float,
        height: float,
        r: float = 0.0,
        angle: Union[int, float] = 0.0,
        style: Union[ShapeStyle, str, None] = None,
        text: str = "",
        textsize: Optional[float] = None,
        textstyle: Union[ShapeTextStyle, str, None] = None,
    ) -> None:
        """Draw a rectangle on the canvas.

        Args:
            xy: Bottom-left corner of the rectangle.
            width: Width of the rectangle.
            height: Height of the rectangle.
            r (float, optional): Radius for rounded corners (default is 0.0).
            angle (Union[int, float], optional): Rotation angle of the rectangle.
            style (Union[ShapeStyle, str, None], optional): Style of the rectangle.
            text (str, optional): Text to display within the rectangle.
            textsize (Optional[float], optional): Size of the text.
            textstyle (Union[ShapeTextStyle, str, None], optional): Style of the text.

        Raises:
            ValueError: If invalid path points are provided.

        """
        style, textstyle = ShapeUtil.format_styles(
            style,
            textstyle,
            dtheme.rectanglestyles.get,
            dtheme.rectangletextstyles.get,
        )
        validator.validate_shape_args(locals())

        if r == 0:
            p1 = (0, 0)
            p2 = (0, height)
            p3 = (width, height)
            p4 = (width, 0)
            self.shape(
                xy=xy,
                path_points=[p1, p2, p3, p4],
                angle=angle,
                style=style,
                text=text,
                textsize=textsize,
                textstyle=textstyle,
            )
            return

        # left center
        p1 = (0, height / 2)

        # left top corner
        p2 = (0, height - r)
        p3 = ((0, height), (r, height))

        # right top corner
        p4 = (width - r, height)
        p5 = ((width, height), (width, height - r))

        # right bottom corner
        p6 = (width, r)
        p7 = ((width, 0), (width - r, 0))

        # left bottom corner
        p8 = (r, 0)
        p9 = ((0, 0), (0, r))

        self.shape(
            xy=xy,
            path_points=[p1, p2, p3, p4, p5, p6, p7, p8, p9],
            angle=angle,
            style=style,
            text=text,
            textsize=textsize,
            textstyle=textstyle,
        )

    @error_handler
    def get_image_zoom_original(
        self,
    ) -> float:
        """Get the zoom factor for displaying the original image.

        Returns:
            float: Zoom factor.
        """
        #
        # calcuration
        # 0.72 * 100 / dpi
        #

        zoom = 72 / self._dpi
        return zoom

    @error_handler
    def get_image_zoom_from_width(
        self,
        image: Union[str, PIL.Image.Image, Dimage],
        width: float,
    ) -> float:
        """Get the zoom factor to fit the image width on the canvas.

        Args:
            image (Union[str, PIL.Image.Image, Dimage]): Image data.
            width (float): Target width.

        Returns:
            float: Zoom factor.
        """
        #
        # calcuration
        # 0.72 * 10 * 100 * target_width / canvas_width / image_width
        #

        if not isinstance(image, Dimage):
            image = Dimage(image)

        image_width, _ = image.get_image_size()
        zoom = 720 * width / self._width / image_width
        return zoom

    @error_handler
    def get_charwidth_from_fontsize(
        self,
        size: float,
    ) -> float:
        """Calculate the character width based on the font size.

        This method calculates the width of a character using a given font size.
        The calculation is currently based on a magic number which may need to be
        adjusted for better accuracy in the future.

        Args:
            size (float): The font size for which to calculate the character width.

        Returns:
            float: The calculated character width.

        Notes:
            The `magic_number` used in the calculation is currently set to 460, but
            this is a placeholder and may require a more accurate calculation.

        Todo:
            - Improve the calculation of the `magic_number` for more accurate results.

        """
        magic_number = 460  # todo: requires better calcuration
        width = size * 0.72 * self._width / magic_number
        return width

    @error_handler
    def get_fontsize_from_charwidth(
        self,
        width: float,
    ) -> float:
        """Calculate the font size based on the character width.

        This method calculates the font size required to achieve a given character width.
        The calculation is currently based on a magic number which may need to be adjusted
        for better accuracy in the future.

        Args:
            width (float): The character width for which to calculate the font size.

        Returns:
            float: The calculated font size.

        Notes:
            The `magic_number` used in the calculation is currently set to 540, but
            this is a placeholder and may require a more accurate calculation.

        Todo:
            - Improve the calculation of the `magic_number` for more accurate results.
        """
        magic_number = 540  # todo: requires better calcuration
        size = magic_number * width / 0.72 / self._width
        return int(size)
