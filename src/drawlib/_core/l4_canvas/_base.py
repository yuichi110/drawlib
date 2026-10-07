# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Canvas's base class implementation module."""

import contextlib
import math
from collections.abc import Generator, Iterable
from typing import Any, Final

import matplotlib
import matplotlib.artist
import matplotlib.font_manager
import matplotlib.lines
import matplotlib.text
import PIL.Image
from matplotlib import offsetbox, pyplot
from matplotlib.patches import (
    Circle,
    Ellipse,
    FancyArrowPatch,
    Patch,
    PathPatch,
    Polygon,
    RegularPolygon,
    Wedge,
)
from matplotlib.path import Path
from matplotlib.text import Text
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


def _as_any(val: object) -> Any:  # noqa: ANN401
    return val


def _transform_fancy_arrow_patch(
    artist: FancyArrowPatch,
    s: float,
    tx: float,
    ty: float,
) -> None:
    """Transform geometry of a FancyArrowPatch in place."""
    pos_a_b = _as_any(getattr(artist, "_posA_posB", None))
    if pos_a_b is not None:
        pos_a, pos_b = pos_a_b
        artist.set_positions(
            (float(pos_a[0]) * s + tx, float(pos_a[1]) * s + ty),
            (float(pos_b[0]) * s + tx, float(pos_b[1]) * s + ty),
        )
    else:
        orig_path = _as_any(getattr(artist, "_path_original", None))
        if orig_path is not None:
            new_verts = [(float(vx) * s + tx, float(vy) * s + ty) for vx, vy in _as_any(orig_path.vertices)]
            setattr(artist, "_path_original", Path(vertices=new_verts, codes=orig_path.codes))
    ms = artist.get_mutation_scale()
    if ms:
        artist.set_mutation_scale(float(ms) * s)


def _apply_patch_geometry_transform(
    artist: Patch,
    s: float,
    tx: float,
    ty: float,
) -> None:
    """Transform geometry of a Matplotlib Patch subclass in place."""
    if isinstance(artist, FancyArrowPatch):
        _transform_fancy_arrow_patch(artist, s, tx, ty)
    elif isinstance(artist, PathPatch):
        orig_path = _as_any(artist.get_path())
        new_verts = [(float(vx) * s + tx, float(vy) * s + ty) for vx, vy in _as_any(orig_path.vertices)]
        artist.set_path(Path(vertices=new_verts, codes=orig_path.codes))
    elif isinstance(artist, Polygon):
        new_verts = [(float(vx) * s + tx, float(vy) * s + ty) for vx, vy in _as_any(artist.get_xy())]
        artist.set_xy(new_verts)
    elif isinstance(artist, Circle):
        center = _as_any(artist.get_center())
        artist.set_center((float(center[0]) * s + tx, float(center[1]) * s + ty))
        artist.set_radius(float(artist.get_radius()) * s)
    elif isinstance(artist, Ellipse):
        center = _as_any(artist.get_center())
        artist.set_center((float(center[0]) * s + tx, float(center[1]) * s + ty))
        artist.set_width(float(artist.get_width()) * s)
        artist.set_height(float(artist.get_height()) * s)
    elif isinstance(artist, RegularPolygon):
        xy = _as_any(artist.xy)
        artist.xy = (float(xy[0]) * s + tx, float(xy[1]) * s + ty)
        artist.radius = float(artist.radius) * s
    elif isinstance(artist, Wedge):
        center = _as_any(artist.center)
        artist.set_center((float(center[0]) * s + tx, float(center[1]) * s + ty))
        artist.set_radius(float(artist.r) * s)
        if artist.width is not None:
            artist.set_width(float(artist.width) * s)


def _apply_artist_transform(
    artist: matplotlib.artist.Artist,
    s: float,
    tx: float,
    ty: float,
) -> None:
    """Apply similarity transform (scale s + translation (tx, ty)) to a Matplotlib artist in place."""
    if isinstance(artist, Patch):
        _apply_patch_geometry_transform(artist, s, tx, ty)
        lw = artist.get_linewidth()
        if lw:
            artist.set_linewidth(float(lw) * s)
    elif isinstance(artist, Text):
        pos = _as_any(artist.get_position())
        artist.set_position((float(pos[0]) * s + tx, float(pos[1]) * s + ty))
        artist.set_fontsize(float(artist.get_fontsize()) * s)
        bbox_patch = artist.get_bbox_patch()
        if bbox_patch is not None:
            lw = bbox_patch.get_linewidth()
            if lw:
                bbox_patch.set_linewidth(float(lw) * s)
    elif isinstance(artist, offsetbox.AnnotationBbox):
        xy = _as_any(artist.xy)
        new_xy = (float(xy[0]) * s + tx, float(xy[1]) * s + ty)
        artist.xy = new_xy
        artist.xybox = new_xy
        ob = _as_any(artist.offsetbox)
        if hasattr(ob, "get_zoom") and hasattr(ob, "set_zoom"):
            ob.set_zoom(float(ob.get_zoom()) * s)


class _TransformArtistList(list[matplotlib.artist.Artist]):
    """Artist list that transparently applies active CanvasBase spatial transforms on append/extend."""

    def __init__(self, canvas_base: "CanvasBase") -> None:
        super().__init__()
        self._canvas_base = canvas_base

    def append(self, item: matplotlib.artist.Artist) -> None:
        stack = self._canvas_base._transform_stack
        if stack:
            s, tx, ty = stack[-1]
            _apply_artist_transform(item, s, tx, ty)
        super().append(item)

    def extend(self, iterable: Iterable[matplotlib.artist.Artist]) -> None:
        stack = self._canvas_base._transform_stack
        if stack:
            s, tx, ty = stack[-1]
            items = list(iterable)
            for item in items:
                _apply_artist_transform(item, s, tx, ty)
            super().extend(items)
        else:
            super().extend(iterable)


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
        self._transform_stack: list[tuple[float, float, float]] = []
        self._artists: list[matplotlib.artist.Artist] = _TransformArtistList(self)
        self._active_animation: Any | None = None

        # it is decleared only for typing system
        self._fig = pyplot.figure()
        self._ax = self._fig.add_subplot(1, 1, 1)

        # initialize fig and ax
        self.setup()

    @contextlib.contextmanager
    def transform(
        self,
        origin: Coordinate = (0.0, 0.0),
        scale: float = 1.0,
        translate: tuple[float, float] = (0.0, 0.0),
    ) -> Generator[None, None, None]:
        """Context manager that scales and translates all artists added within its scope.

        Args:
            origin: Anchor coordinate (ox, oy) around which scaling is performed.
            scale: Proportional scale factor (> 0). Defaults to 1.0.
            translate: Additional (dx, dy) translation offset. Defaults to (0.0, 0.0).
        """
        s_loc = float(scale)
        if s_loc <= 0.0:
            raise ValueError(f"scale must be positive (> 0), but got {scale}.")
        dx, dy = float(translate[0]), float(translate[1])
        if s_loc == 1.0 and dx == 0.0 and dy == 0.0:
            yield
            return

        ox, oy = float(origin[0]), float(origin[1])
        tx_loc = ox * (1.0 - s_loc) + dx
        ty_loc = oy * (1.0 - s_loc) + dy

        if self._transform_stack:
            s_out, tx_out, ty_out = self._transform_stack[-1]
            s_comp = s_out * s_loc
            tx_comp = s_out * tx_loc + tx_out
            ty_comp = s_out * ty_loc + ty_out
        else:
            s_comp, tx_comp, ty_comp = s_loc, tx_loc, ty_loc

        self._transform_stack.append((s_comp, tx_comp, ty_comp))
        try:
            yield
        finally:
            self._transform_stack.pop()

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
            self._artists.clear()

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
