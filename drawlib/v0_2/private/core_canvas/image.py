# Copyright (c) 2024 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.


"""Canvas's image feature implementation module."""

from typing import Any, Tuple, Union

import numpy
from matplotlib import offsetbox
from numpy.typing import NDArray
from PIL.Image import Image

import drawlib.v0_2.private.validators.args as validator
from drawlib.v0_2.private.core.colors import Colors
from drawlib.v0_2.private.core.dimage import Dimage
from drawlib.v0_2.private.core.model import ImageStyle, ShapeStyle
from drawlib.v0_2.private.core.util import ImageUtil
from drawlib.v0_2.private.core_canvas.base import CanvasBase
from drawlib.v0_2.private.logging import logger
from drawlib.v0_2.private.util import error_handler


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

    @error_handler
    def image(
        self,
        xy: Tuple[float, float],
        width: float,
        image: Union[str, Image, Dimage],
        angle: Union[int, float] = 0.0,
        style: Union[ImageStyle, str, None] = None,
    ) -> None:
        """Draw an image on the canvas.

        Args:
            xy (Tuple[float, float]): Coordinates of the left bottom corner of the image.
            width (float): Width of the image. Height is calculated automatically based on image aspect ratio.
            image (Union[str, Image, Dimage]): Path to the image file or PIL Image object or Dimage object.
            angle (Union[int, float], optional): Rotation angle of the image in degrees (default is 0.0).
            style (Union[ImageStyle, str, None], optional): Style of the image (default is None).

        Returns:
            None

        Raises:
            ValueError: If invalid alignment (`style.halign` or `style.valign`) is provided.

        Notes:
            - If `style.halign` or `style.valign` is set to other than "center" and the image is rotated (`angle != 0`),
              a warning is logged, and alignment is set to "center".
            - The image is scaled and rotated based on the provided parameters and then added to the canvas as an
              annotation.
        """
        style = ImageUtil.format_style(style)
        validator.validate_image_args(locals())

        # standadize

        x, y = xy
        dimg = Dimage(image, copy=True)

        # apply fill effects. Alpha and Border will be applied later.
        if style.fcolor is not None:
            dimg = dimg.fill(style.fcolor)

        # get height and zoom
        image_width, image_height = dimg.get_image_size()
        height = image_height / image_width * width
        zoom = self.get_image_zoom_from_width(dimg, width)

        # rotate and shift
        dimg, style = self._rotate_image(dimg, angle, style)
        x, y = self._shift_xy(x, y, dimg, zoom, style)

        # crate drawing object
        im = self._convert_dimg_to_numpyarray(dimg)
        imagebox = offsetbox.OffsetImage(im, zoom=zoom, alpha=style.alpha)
        ab = offsetbox.AnnotationBbox(imagebox, (x, y), frameon=False)

        # write image
        self._artists.append(ab)

        # write border
        self._draw_border(xy, width, height, angle, style)

    @staticmethod
    def _rotate_image(dimg: Dimage, angle: float, style: ImageStyle) -> Tuple[Dimage, ImageStyle]:
        # rotate image
        if angle == 0:
            return dimg, style

        has_wrong_style = False
        if style.halign != "center":
            has_wrong_style = True
            style.halign = "center"
        if style.valign != "center":
            has_wrong_style = True
            style.valign = "center"
        if has_wrong_style:
            logger.warning("image() with angle only accepts ShapeTextStyle alignment center.")

        return dimg._rotate(angle), style

    def _shift_xy(self, x: float, y: float, dimg: Dimage, zoom: float, style: ImageStyle) -> Tuple[float, float]:
        if style.halign == "center" and style.valign == "center":
            return (x, y)

        #
        # memo. calculation
        # (image_width / 2) * (zoom / 0.72) * (canvas_width / 100)
        #   -> image_width * zoom * self._width / 1440

        image_width, image_height = dimg.get_image_size()
        x_shift = image_width * zoom * self._width / 1440
        y_shift = image_height * zoom * self._width / 1440

        if style.halign == "left":
            x += x_shift
        elif style.halign == "center":
            ...
        elif style.halign == "right":
            x -= x_shift
        else:
            raise ValueError(f'halign "{style.halign}" is not supported.')

        if style.valign == "bottom":
            y += y_shift
        elif style.valign == "center":
            ...
        elif style.valign == "top":
            y -= y_shift
        else:
            raise ValueError(f'valign "{style.valign}" is not supported.')

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
        xy: Tuple[float, float],
        width: float,
        height: float,
        angle: float,
        style: ImageStyle,
    ) -> None:
        # border
        if style.lwidth is None:
            return
        if style.lwidth == 0:
            return

        shapestyle = ShapeStyle(
            halign=style.halign,  # type: ignore
            valign=style.valign,  # type: ignore
            lstyle=style.lstyle,  # type: ignore
            lwidth=style.lwidth,
            lcolor=style.lcolor,
            fcolor=Colors.Transparent,
            alpha=style.alpha,
        )
        self.rectangle(xy=xy, width=width, height=height, angle=angle, style=shapestyle)
