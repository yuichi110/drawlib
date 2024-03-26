"""write docstring later"""

from __future__ import annotations

import os
from typing import Union, Tuple
from PIL import (
    Image,
    ImageFilter,
    ImageOps,
    ImageEnhance,
    ImageChops,
)
from drawlib._util import error_handler, get_script_relative_path


class Pimage:
    """Simplified PIL.Image wrapper"""

    @error_handler
    def __init__(
        self, image: Union[str, Image.Image, Pimage], copy: bool = False
    ):
        # create new PIL.Image instance
        if isinstance(image, str):
            image = get_script_relative_path(image)
            if not os.path.exists(image):
                raise FileNotFoundError(f'file "{image}" does not exist.')
            self._pilimg = Image.open(image)

        elif isinstance(image, Image.Image):
            if copy:
                self._pilimg = image.copy()
            else:
                self._pilimg = image

        elif isinstance(image, Pimage):
            if copy:
                self._pilimg = image._pilimg.copy()
            else:
                self._pilimg = image._pilimg

        else:
            raise ValueError(f'Pimage does not support type "{type(image)}".')

    @error_handler
    def get_pil_image(self) -> Image.Image:
        """write docstring later"""

        return self._pilimg.copy()

    @error_handler
    def copy(self) -> Pimage:
        """write docstring later"""

        return Pimage(self)

    @error_handler
    def save(self, file: str) -> None:
        """write docstring later"""

        if not isinstance(file, str):
            raise ValueError('arg "file" must be str.')

        abspath = get_script_relative_path(file)
        directory = os.path.dirname(abspath)
        os.makedirs(directory, exist_ok=True)
        self._pilimg.save(abspath, quality=95)

    @error_handler
    def rotate(self, angle: float) -> Pimage:
        """write docstring later"""

        newimg = self._pilimg.rotate(
            angle,
            resample=Image.Resampling.BICUBIC,
            expand=True,
        )
        return Pimage(newimg)

    @error_handler
    def resize(self, width: int, height: int) -> Pimage:
        """write docstring later"""

        newimg = self._pilimg.resize(
            (width, height),
            resample=Image.LANCZOS,  # pylint: disable=no-member
        )
        return Pimage(newimg)

    @error_handler
    def flip(self) -> Pimage:
        """write docstring later"""

        newimg = ImageOps.flip(self._pilimg)
        return Pimage(newimg)

    @error_handler
    def mirror(self) -> Pimage:
        """write docstring later"""

        newimg = ImageOps.mirror(self._pilimg)
        return Pimage(newimg)

    @error_handler
    def invert(self) -> Pimage:
        """write docstring later"""

        if "A" not in self._pilimg.mode:
            # has no tranceparency. use function
            newimg = ImageOps.invert(self._pilimg)
            return Pimage(newimg)

        # Invert RGB channels
        r, g, b, a = self._pilimg.split()
        r = Image.eval(r, lambda x: 255 - x)
        g = Image.eval(g, lambda x: 255 - x)
        b = Image.eval(b, lambda x: 255 - x)

        # Merge inverted RGB channels with original alpha channel
        inverted_image = Image.merge("RGBA", (r, g, b, a))
        return Pimage(inverted_image)

    @error_handler
    def grayscale(self) -> Pimage:
        """write docstring later"""

        newimg = self._pilimg.convert("LA")
        return Pimage(newimg)

    @error_handler
    def brightness(self, brightness_: float = 0.5) -> Pimage:
        """write docstring later"""

        enhancer = ImageEnhance.Brightness(self._pilimg)
        newimg = enhancer.enhance(brightness_)
        return Pimage(newimg)

    @error_handler
    def sepia(self) -> Pimage:
        """write docstring later"""

        gray = self._pilimg.convert("L")
        sepia_image = Image.merge(
            "RGB",
            (
                gray.point(lambda x: x * 240 / 255),
                gray.point(lambda x: x * 200 / 255),
                gray.point(lambda x: x * 145 / 255),
            ),
        )
        if "A" not in self._pilimg.mode:
            return Pimage(sepia_image)

        # add alpha from original
        alpha_mask = self._pilimg.split()[3]
        sepia_image.putalpha(alpha_mask)
        return Pimage(sepia_image)

    @error_handler
    def colorize(
        self,
        black: Union[str, Tuple[int, int, int]],
        white: Union[str, Tuple[int, int, int]],
    ) -> Pimage:
        """write docstring later"""

        gray = self._pilimg.convert("L")
        colorized_image = ImageOps.colorize(gray, black=black, white=white)
        if "A" not in self._pilimg.mode:
            return Pimage(colorized_image)

        # add alpha from original
        alpha_mask = self._pilimg.split()[3]
        colorized_image.putalpha(alpha_mask)
        return Pimage(colorized_image)

    @error_handler
    def posterize(self, num_colors: int = 4) -> Pimage:
        """write docstring later"""

        if "A" not in self._pilimg.mode:
            newimg = ImageOps.posterize(self._pilimg, num_colors)
            return Pimage(newimg)

        r, g, b, a = self._pilimg.split()
        r = ImageOps.posterize(r, num_colors)
        g = ImageOps.posterize(g, num_colors)
        b = ImageOps.posterize(b, num_colors)
        newimg = Image.merge("RGBA", (r, g, b, a))
        return Pimage(newimg)

    @error_handler
    def mosaic(self) -> Pimage:
        """write docstring later"""

        gimg = self._pilimg.filter(ImageFilter.GaussianBlur(4))
        newimg = gimg.resize(
            [x // 8 for x in self._pilimg.size],
        ).resize(self._pilimg.size)
        return Pimage(newimg)

    @error_handler
    def blur(self) -> Pimage:
        """write docstring later"""

        newimg = self._pilimg.filter(ImageFilter.BLUR)
        return Pimage(newimg)

    @error_handler
    def line_extraction(self) -> Pimage:
        """write docstring later"""

        gray = self._pilimg.convert("L")
        gray2 = gray.filter(ImageFilter.MaxFilter(5))
        senga_inv = ImageChops.difference(gray, gray2)
        newimg = ImageOps.invert(senga_inv)
        return Pimage(newimg)

    @error_handler
    def remove_margin(
        self,
        margin_color: Union[None, str, Tuple[int, int, int]],
    ) -> Pimage:
        """write docstring later"""

        if margin_color is None:
            if "A" not in self._pilimg.mode:
                message = "Can't remove transparent margin from RGB image."
                raise ValueError(message)
            crop = self._pilimg.split()[-1].getbbox()
            new_image = self._pilimg.crop(crop)
            return Pimage(new_image)

        raise NotImplementedError("Implement later")
