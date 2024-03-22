from __future__ import annotations

import os
from typing import Literal, Union, Tuple
from PIL import (
    Image,
    ImageFilter,
    ImageOps,
    ImageEnhance,
    ImageChops,
)


class Pimage:
    """Simplified PIL.Image wrapper"""

    def __init__(self, image: Union[str, Image.Image, Pimage], copy: bool = False):
        # create new PIL.Image instance
        if isinstance(image, str):
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

    def get_pil_image(self):
        return self._pilimg.copy()

    def save(self, file: str):
        directory = os.path.dirname(file)
        os.makedirs(directory, exist_ok=True)
        self._pilimg.save(file, quality=95)

    def rotate(self, angle: float) -> Pimage:
        newimg = self._pilimg.rotate(
            angle,
            resample=Image.Resampling.BICUBIC,
            expand=True,
        )
        return Pimage(newimg)

    def resize(self, width: int, height: int) -> Pimage:
        newimg = self._pilimg.resize((width, height), resample=Image.LANCZOS)
        return Pimage(newimg)

    def flip(self) -> Pimage:
        newimg = ImageOps.flip(self._pilimg)
        return Pimage(newimg)

    def mirror(self) -> Pimage:
        newimg = ImageOps.mirror(self._pilimg)
        return Pimage(newimg)

    def invert(self) -> Pimage:
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

    def grayscale(self) -> Pimage:
        newimg = self._pilimg.convert("LA")
        return Pimage(newimg)

    def brightness(self, brightness_: float = 0.5) -> Pimage:
        enhancer = ImageEnhance.Brightness(self._pilimg)
        newimg = enhancer.enhance(brightness_)
        return Pimage(newimg)

    def sepia(self) -> Pimage:
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

    def colorize(
        self,
        black: Union[str, Tuple[int, int, int]],
        white: Union[str, Tuple[int, int, int]],
    ) -> Pimage:
        gray = self._pilimg.convert("L")
        colorized_image = ImageOps.colorize(gray, black=black, white=white)
        if "A" not in self._pilimg.mode:
            return Pimage(colorized_image)

        # add alpha from original
        alpha_mask = self._pilimg.split()[3]
        colorized_image.putalpha(alpha_mask)
        return Pimage(colorized_image)

    def posterize(self, num_colors: int = 4) -> Pimage:
        if "A" not in self._pilimg.mode:
            # has no tranceparency. use function
            newimg = ImageOps.posterize(self._pilimg, num_colors)
            return Pimage(newimg)

        r, g, b, a = self._pilimg.split()
        r = ImageOps.posterize(r, num_colors)
        # print(f"posterize {r.mode}")
        g = ImageOps.posterize(g, num_colors)
        b = ImageOps.posterize(b, num_colors)
        newimg = Image.merge("RGBA", (r, g, b, a))
        return Pimage(newimg)

    def mosaic(self) -> Pimage:
        gimg = self._pilimg.filter(ImageFilter.GaussianBlur(4))
        newimg = gimg.resize(
            [x // 8 for x in self._pilimg.size],
        ).resize(self._pilimg.size)
        return Pimage(newimg)

    def blur(self) -> Pimage:
        newimg = self._pilimg.filter(ImageFilter.BLUR)
        return Pimage(newimg)

    def line_extraction(self) -> Image.Image:
        gray = self._pilimg.convert("L")
        gray2 = gray.filter(ImageFilter.MaxFilter(5))
        senga_inv = ImageChops.difference(gray, gray2)
        newimg = ImageOps.invert(senga_inv)
        return Pimage(newimg)
