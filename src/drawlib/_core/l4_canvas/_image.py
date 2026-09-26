# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Canvas image feature module."""

import logging
from typing import Any

import numpy
from matplotlib import offsetbox
from numpy.typing import NDArray
from PIL import Image
from pydantic import ConfigDict, validate_call

from drawlib._core.l2_models import Dimage
from drawlib._core.l2_types import (
    FilePath,
    TypeAngle,
    TypeCoordinate,
    TypeImageZoom,
    TypePosFloat,
)
from drawlib._core.l3_styles import Colors, Style
from drawlib._core.l4_canvas._base import CanvasBase
from drawlib._core.l4_canvas_utils import ImageUtil

logger = logging.getLogger(__name__)


class CanvasImageFeature(CanvasBase):
    """Canvas image feature class."""

    def __init__(self) -> None:
        """Initializes an instance of CanvasImageFeature."""
        super().__init__()

    @validate_call(config=ConfigDict(arbitrary_types_allowed=True))
    def image(  # noqa: C901
        self,
        xy: TypeCoordinate,
        width: TypePosFloat,
        image: FilePath | Image.Image | Dimage,
        angle: TypeAngle = 0.0,
        *,
        style: Style | None = None,
    ) -> None:
        """Draw an image on the canvas.

        Args:
            xy (tuple[float, float]): Coordinates of the left bottom corner of the image.
            width (float): Width of the image. Height is calculated automatically based on aspect ratio.
            image (str | Image | Dimage): Path to image file, PIL Image, or Dimage object.
                If a relative file path is provided, it is resolved relative to the caller script directory.
            angle (int | float, optional): Rotation angle in degrees (default is 0.0).
            style (Style | None, optional): Style of the image. Defaults to None.
        """
        style = ImageUtil.format_style(style)

        x, y = xy
        dimg = Dimage(image, copy=True)

        if style.image_tint_color is not None:
            dimg = dimg.fill(style.image_tint_color)

        image_width, image_height = dimg.get_image_size()
        height = image_height / image_width * width
        zoom = self.get_image_zoom_from_width(dimg, width)

        dimg, style = self._rotate_image(dimg, angle, style)
        x, y = self._shift_xy(x, y, dimg, zoom, style)

        im = self._convert_dimg_to_numpyarray(dimg)
        imagebox = offsetbox.OffsetImage(im, zoom=zoom, alpha=style.image_alpha)
        ab = offsetbox.AnnotationBbox(imagebox, (x, y), frameon=False)

        self._artists.append(ab)
        self._draw_border(xy, width, height, angle, style)

    @staticmethod
    def _rotate_image(dimg: Dimage, angle: TypeAngle, style: Style) -> tuple[Dimage, Style]:
        if angle == 0:
            return dimg, style

        has_wrong_style = False
        patch_kwargs: dict[str, Any] = {}
        if style.text_halign is not None and style.text_halign != "center":
            has_wrong_style = True
            patch_kwargs["text_halign"] = "center"
        if style.text_valign is not None and style.text_valign != "center":
            has_wrong_style = True
            patch_kwargs["text_valign"] = "center"
        if has_wrong_style:
            logger.warning("image() with angle only accepts Style alignment center.")
            style = style.patch(**patch_kwargs)

        return dimg._rotate(angle), style

    def _shift_xy(self, x: float, y: float, dimg: Dimage, zoom: TypeImageZoom, style: Style) -> TypeCoordinate:
        halign = style.text_halign if style.text_halign is not None else "center"
        valign = style.text_valign if style.text_valign is not None else "center"
        if halign == "center" and valign == "center":
            return (x, y)

        image_width, image_height = dimg.get_image_size()
        x_shift = image_width * zoom * self._width / 1440
        y_shift = image_height * zoom * self._width / 1440

        if halign == "left":
            x += x_shift
        elif halign == "center":
            ...
        elif halign == "right":
            x -= x_shift
        else:
            raise ValueError(f'halign "{halign}" is not supported.')

        if valign == "bottom":
            y += y_shift
        elif valign == "center":
            ...
        elif valign == "top":
            y -= y_shift
        else:
            raise ValueError(f'valign "{valign}" is not supported.')

        return (x, y)

    @staticmethod
    def _convert_dimg_to_numpyarray(dimg: Dimage) -> NDArray[Any]:
        pil_image = dimg.get_pil_image()
        im = numpy.array(pil_image)

        if im.ndim == 3:
            if im.shape[2] == 2:
                gray = im[:, :, 0]
                alpha = im[:, :, 1]
                rgb_array = numpy.stack((gray, gray, gray), axis=-1)
                im = numpy.concatenate((rgb_array, alpha[:, :, numpy.newaxis]), axis=-1)

        return im

    def _draw_border(
        self,
        xy: TypeCoordinate,
        width: TypePosFloat,
        height: TypePosFloat,
        angle: TypeAngle,
        style: Style,
    ) -> None:
        if style.image_border_width is None or style.image_border_width == 0:
            return

        border_color = style.image_border_color if style.image_border_color is not None else Colors.Black
        shapestyle = Style(
            text_halign=style.text_halign,
            text_valign=style.text_valign,
            shape_line_style=style.image_border_style if style.image_border_style is not None else "solid",
            shape_line_width=style.image_border_width,
            shape_line_color=border_color,
            shape_fill_color=Colors.Transparent,
            shape_fill_alpha=style.image_alpha,
        )
        self.rectangle(xy=xy, width=width, height=height, angle=angle, style=shapestyle)
