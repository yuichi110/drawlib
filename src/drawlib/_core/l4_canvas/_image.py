# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.


"""Canvas's image feature implementation module."""

from typing import Any

import numpy
from matplotlib import offsetbox
from numpy.typing import NDArray
from PIL.Image import Image

from drawlib._core.l1_core import guarded, logger
from drawlib._core.l2_models import (
    Dimage,
)
from drawlib._core.l2_types import (
    TypeAngle,
    TypeCoordinate,
    TypeFloat,
    TypeImageZoom,
    TypePosFloat,
    TypeStr,
)
from drawlib._core.l3_styles import Colors, ImageStyle, ShapeStyle
from drawlib._core.l4_canvas._base import CanvasBase
from drawlib._core.l4_canvas_utils import ImageUtil


class CanvasImageFeature(CanvasBase):
    """A class to handle image drawing features on a canvas.

    This class provides methods to draw images with specified styles and transformations
    on a canvas.
    """

    def __init__(self) -> None:
        """Initialize the CanvasImageFeature object.

        This constructor initializes the CanvasImageFeature object by calling the constructor
        of its superclass CanvasBase.

        Args:
            None

        Returns:
            None
        """
        super().__init__()

    @guarded
    def image(
        self,
        xy: TypeCoordinate,
        width: TypePosFloat,
        image: TypeStr | Image | Dimage,
        angle: TypeAngle = 0.0,
        style: ImageStyle | TypeStr | None = None,
    ) -> None:
        """Draw an image on the canvas.

        Args:
            xy (tuple[float, float]): Coordinates of the left bottom corner of the image.
            width (float): Width of the image. Height is calculated automatically based on image aspect ratio.
            image (str | Image | Dimage): Path to the image file or PIL Image object or Dimage object.
            angle (int | float, optional): Rotation angle of the image in degrees (default is 0.0).
            style (ImageStyle | str | None, optional): Style of the image (default is None).

        Returns:
            None

        Raises:
            ValueError: If invalid alignment (`style.text_halign` or `style.text_valign`) is provided.

        Notes:
            - If `style.text_halign` or `style.text_valign` is set to other than "center" and
              the image is rotated (`angle != 0`), a warning is logged, and alignment is set to "center".
            - The image is scaled and rotated based on the provided parameters and then added to the canvas as an
              annotation.
        """
        style = ImageUtil.format_style(style)

        # standadize

        x, y = xy
        dimg = Dimage(image, copy=True)

        # apply fill effects. Alpha and Border will be applied later.
        if style.fill_color is not None:
            dimg = dimg.fill(style.fill_color)

        # get height and zoom
        image_width, image_height = dimg.get_image_size()
        height = image_height / image_width * width
        zoom = self.get_image_zoom_from_width(dimg, width)

        # rotate and shift
        dimg, style = self._rotate_image(dimg, angle, style)
        x, y = self._shift_xy(x, y, dimg, zoom, style)

        # crate drawing object
        im = self._convert_dimg_to_numpyarray(dimg)
        imagebox = offsetbox.OffsetImage(im, zoom=zoom, alpha=style.fill_alpha)
        ab = offsetbox.AnnotationBbox(imagebox, (x, y), frameon=False)

        # write image
        self._artists.append(ab)

        # write border
        self._draw_border(xy, width, height, angle, style)

    @staticmethod
    def _rotate_image(dimg: Dimage, angle: TypeAngle, style: ImageStyle) -> tuple[Dimage, ImageStyle]:
        # rotate image
        if angle == 0:
            return dimg, style

        has_wrong_style = False
        if style.text_halign != "center":
            has_wrong_style = True
            style.text_halign = "center"
        if style.text_valign != "center":
            has_wrong_style = True
            style.text_valign = "center"
        if has_wrong_style:
            logger.warning("image() with angle only accepts ShapeTextStyle alignment center.")

        return dimg._rotate(angle), style

    def _shift_xy(self, x: float, y: float, dimg: Dimage, zoom: TypeImageZoom, style: ImageStyle) -> TypeCoordinate:
        if style.text_halign == "center" and style.text_valign == "center":
            return (x, y)

        #
        # memo. calculation
        # (image_width / 2) * (zoom / 0.72) * (canvas_width / 100)
        #   -> image_width * zoom * self._width / 1440

        image_width, image_height = dimg.get_image_size()
        x_shift = image_width * zoom * self._width / 1440
        y_shift = image_height * zoom * self._width / 1440

        if style.text_halign == "left":
            x += x_shift
        elif style.text_halign == "center":
            ...
        elif style.text_halign == "right":
            x -= x_shift
        else:
            raise ValueError(f'halign "{style.text_halign}" is not supported.')

        if style.text_valign == "bottom":
            y += y_shift
        elif style.text_valign == "center":
            ...
        elif style.text_valign == "top":
            y -= y_shift
        else:
            raise ValueError(f'valign "{style.text_valign}" is not supported.')

        return (x, y)

    @staticmethod
    def _convert_dimg_to_numpyarray(dimg: Dimage) -> NDArray[Any]:
        # create image drawing object
        pil_image = dimg.get_pil_image()
        im = numpy.array(pil_image)

        # grayscale doesn't work fine on matplotlib. convert to RGBA.
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
        style: ImageStyle,
    ) -> None:
        # border
        if style.line_width is None:
            return
        if style.line_width == 0:
            return

        shapestyle = ShapeStyle(
            text_halign=style.text_halign,
            text_valign=style.text_valign,
            line_style=style.line_style,
            line_width=style.line_width,
            line_color=style.line_color,
            fill_color=Colors.Transparent,
            fill_alpha=style.fill_alpha,
        )
        self.rectangle(xy=xy, width=width, height=height, angle=angle, style=shapestyle)
