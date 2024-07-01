# Copyright (c) 2024 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.


"""Class Dimage implementation module."""

from __future__ import annotations

import os
from typing import Dict, List, Tuple, Union, cast

from PIL import (
    Image,
    ImageChops,
    ImageEnhance,
    ImageFilter,
    ImageOps,
)

from drawlib.v0_2.private.util import (
    error_handler,
    get_script_relative_path,
)
from drawlib.v0_2.private.validators.color import validate_color

list_ = list


class DimageCache:
    """A class for managing a cache of Dimage objects."""

    def __init__(self) -> None:
        """Initialize an empty Dimage cache."""
        self._cache: Dict[str, Dimage] = {}

    def has(self, name: str) -> bool:
        """Check whether a Dimage cache with the given name exists.

        Args:
            name (str): The name of the cache.

        Returns:
            bool: True if the cache exists, False otherwise.
        """
        return name in self._cache

    def set(self, name: str, image: Union[str, Dimage, Image.Image]) -> None:
        """Set a copied Dimage cache with the provided name key.

        This method creates a copy of the original object and sets the copied one in the cache.
        It means you can modify the original object after caching without affecting the cached object.

        Args:
            name (str): The key under which to cache the Dimage.
            image (Union[str, Dimage, Image.Image]): The image to cache, either as a file path,
                a Dimage object, or a PIL Image.

        Returns:
            None
        """
        self._cache[name] = Dimage(image=image, copy=True)

    def list(self) -> List[str]:
        """List all cached Dimage names.

        Returns:
            list[str]: A list of all cached Dimage names.
        """
        return list_(self._cache.keys())

    def get(self, name: str) -> Dimage:
        """Get a copied Dimage cache by name (key).

        This method returns a copy of the cached Dimage object, allowing modifications
        without affecting the original cached object.

        Args:
            name (str): The key of the cached Dimage to retrieve.

        Returns:
            Dimage: A copy of the original cached Dimage object.

        Raises:
            ValueError: If the specified Dimage cache does not exist.
        """
        if not self.has(name):
            raise ValueError(f'Dimage "{name}" is not cached.')
        return self._cache[name].copy()

    def delete(self, name: str) -> None:
        """Delete a Dimage cache if it exists.

        Args:
            name (str): The key of the Dimage cache to delete.

        Returns:
            None
        """
        if self.has(name):
            del self._cache[name]


class Dimage:
    """A wrapper class for handling images with easy methods for reading, writing, and applying effects.

    This class provides simple methods for reading, writing, and applying effects to images.
    It serves as a wrapper for `PIL.Image.Image`, allowing users to get and set PIL images
    from this class. For advanced effects, users should directly use the PIL Image class.

    Attributes:
        cache (DimageCache): A cache for storing Dimage objects.
    """

    cache = DimageCache()

    @error_handler
    def __init__(
        self,
        image: Union[str, Dimage, Image.Image],
        copy: bool = False,
    ) -> None:
        """Initialize a Dimage instance from a file path, PIL Image, or another Dimage.

        This constructor initializes a Dimage instance from a given image source.
        The source can be a file path, a PIL Image, or another Dimage. If `copy` is
        True, a copy of the image is made; otherwise, the original image is used.

        Args:
            image (str | Dimage | Image.Image): The source image to initialize the Dimage.
            copy (bool, optional): If True, a copy of the image is made. Defaults to False.

        Raises:
            FileNotFoundError: If the file path does not exist.
            ValueError: If the image type is not supported.

        Note:
            The file path is relative to the user code which calls this constructor,
            not relative to where you call Python (default path behavior). If you
            want to use the normal path behavior, convert the relative path to an
            absolute path before passing it to this class.
        """
        # create a new PIL.Image instance
        if isinstance(image, str):
            image_str = cast(str, image)  # for mypy check
            image_str = get_script_relative_path(image_str)
            if not os.path.exists(image_str):
                raise FileNotFoundError(f'file "{image_str}" does not exist.')
            self._pilimg = Image.open(image_str)

        elif isinstance(image, Image.Image):
            if copy:
                self._pilimg = image.copy()
            else:
                self._pilimg = image

        elif isinstance(image, Dimage):
            if copy:
                self._pilimg = image._pilimg.copy()
            else:
                self._pilimg = image._pilimg

        else:
            raise ValueError(f'Dimage does not support type "{type(image)}".')

    @error_handler
    def get_pil_image(self) -> Image.Image:
        """Get a copied PIL Image.

        This method returns a copy of the PIL Image held by the Dimage instance.
        Modifications to the returned PIL Image do not affect the original Dimage.

        Returns:
            PIL.Image.Image: A copy of the PIL Image.
        """
        return self._pilimg.copy()

    @error_handler
    def get_image_size(self) -> Tuple[int, int]:
        """Get the size of the image.

        This method returns the width and height of the image as a tuple.

        Returns:
            tuple[int, int]: A tuple containing the width and height of the image.
        """
        width, height = self._pilimg.size
        return (width, height)

    @error_handler
    def copy(self) -> Dimage:
        """Get a copied Dimage.

        This method creates and returns another Dimage instance with the same content.

        Returns:
            Dimage: A deep copied Dimage instance.
        """
        return Dimage(self)

    @error_handler
    def save(self, file: str) -> None:
        """Save the Dimage data to a file.

        This method saves the image to the specified file path. The path is
        relative to the script file which calls this method.

        Args:
            file (str): The file path to save the image. This path is relative to the user script file.

        Raises:
            ValueError: If the file argument is not a string.

        Returns:
            None
        """
        if not isinstance(file, str):
            raise ValueError('arg "file" must be str.')

        abspath = get_script_relative_path(file)
        directory = os.path.dirname(abspath)
        os.makedirs(directory, exist_ok=True)
        self._pilimg.save(abspath, quality=95)

    @error_handler
    def _rotate(self, angle: float) -> Dimage:
        """Get a new Dimage that is rotated. The original Dimage is kept unchanged.

        This method returns a new Dimage that is rotated by the specified angle.

        Args:
            angle (float): The angle to rotate the image by, between 0.0 and 360.0 degrees.
                           The pixel size can change, and new areas become transparent.

        Returns:
            Dimage: A new rotated image.
        """
        newimg = self._pilimg.rotate(
            angle,
            resample=Image.Resampling.BICUBIC,
            expand=True,
        )
        return Dimage(newimg)

    @error_handler
    def resize(self, width: int, height: int) -> Dimage:
        """Get a new Dimage that is resized. The original Dimage is kept unchanged.

        This method returns a new Dimage that is resized to the specified width and height.

        Args:
            width (int): The new width of the image.
            height (int): The new height of the image.

        Returns:
            Dimage: A new resized image.
        """
        newimg = self._pilimg.resize(
            (width, height),
            resample=Image.LANCZOS,
        )
        return Dimage(newimg)

    @error_handler
    def crop(self, x: int, y: int, width: int, height: int) -> Dimage:
        """Get a new Dimage that is cropped. The original Dimage is kept unchanged.

        This method returns a new Dimage that is cropped to the specified dimensions.
        Note that the origin (0, 0) is at the left bottom for this method.

        Args:
            x (int): The x-coordinate of the top-left corner of the cropping box.
            y (int): The y-coordinate of the top-left corner of the cropping box.
            width (int): The width of the cropping box.
            height (int): The height of the cropping box.

        Returns:
            Dimage: A new cropped image.
        """
        # drawlib's (0, 0) is left bottom
        # pil crop()'s (0, 0) is left top.
        # reverse y
        (_, image_height) = self.get_image_size()
        left = x
        top = image_height - (y + height)
        right = x + width
        bottom = image_height - y
        new_image = self._pilimg.crop((left, top, right, bottom))
        return Dimage(new_image)

    @error_handler
    def flip(self) -> Dimage:
        """Get a new Dimage that is flipped vertically. The original Dimage is kept unchanged.

        Returns:
            Dimage: A new vertically flipped image.
        """
        newimg = ImageOps.flip(self._pilimg)
        return Dimage(newimg)

    @error_handler
    def mirror(self) -> Dimage:
        """Get a new Dimage that is mirrored horizontally. The original Dimage is kept unchanged.

        Returns:
            Dimage: A new horizontally mirrored image.
        """
        newimg = ImageOps.mirror(self._pilimg)
        return Dimage(newimg)

    @error_handler
    def fill(self, color: Union[Tuple[int, int, int], Tuple[int, int, int, float]]) -> Dimage:
        """Get a new Dimage with the specified color filling the transparent areas.

        Args:
            color (Union[Tuple[int, int, int], Tuple[int, int, int, float]]):
                   The color to fill the transparent areas with. It can be an RGB or RGBA tuple.

        Returns:
            Dimage: A new image with the transparent areas filled with the specified color.
        """
        # const
        tuple_length_has_alpha = 4
        alpha_transparent = 0
        alpha_opaque = 255

        validate_color("from_black_to", color)
        pil_color = (color[0], color[1], color[2], 255)

        pil_image = self._pilimg
        width, height = pil_image.size
        new_image = Image.new("RGBA", (width, height))

        pixels = pil_image.load()
        new_pixels = new_image.load()

        for y in range(height):
            for x in range(width):
                if len(pixels[x, y]) != tuple_length_has_alpha:
                    new_pixels[x, y] = pixels[x, y]
                    continue

                original_alpha = pixels[x, y][3]
                if original_alpha == alpha_transparent:
                    # transparent
                    new_pixels[x, y] = pil_color
                elif original_alpha == alpha_opaque:
                    # not transparent
                    new_pixels[x, y] = pixels[x, y]
                else:
                    # little bit transparent
                    original_ratio = original_alpha / 255
                    new_ratio = 1.0 - original_ratio
                    r = int(pixels[x, y][0] * original_ratio + pil_color[0] * new_ratio)
                    g = int(pixels[x, y][1] * original_ratio + pil_color[1] * new_ratio)
                    b = int(pixels[x, y][2] * original_ratio + pil_color[2] * new_ratio)
                    new_pixels[x, y] = (r, g, b, 255)

        return Dimage(new_image)

    @error_handler
    def alpha(self, alpha: float) -> Dimage:
        """Get a new Dimage with the specified alpha transparency while keeping the original Dimage unchanged.

        This method returns a new Dimage with modified alpha transparency.
        It keeps original transparency if it is lower than provided value.

        Args:
            alpha (float): The alpha value to apply to the image,
            where 0.0 is fully transparent and 1.0 is fully opaque.

        Returns:
            Dimage: A new Dimage with the specified alpha transparency.
        """
        pil_alpha = int(alpha * 255)

        pil_image = self._pilimg
        width, height = pil_image.size
        new_image = Image.new("RGBA", (width, height))

        pixels = pil_image.load()
        new_pixels = new_image.load()

        for y in range(height):
            for x in range(width):
                r, g, b, a = pixels[x, y]
                if a < pil_alpha:
                    new_pixels[x, y] = (r, g, b, a)
                else:
                    new_pixels[x, y] = (r, g, b, pil_alpha)

        return Dimage(new_image)

    @error_handler
    def invert(self) -> Dimage:
        """Get a new Dimage with inverted colors while keeping the original Dimage unchanged.

        Returns:
            Dimage: A new Dimage with inverted colors.
        """
        if "A" not in self._pilimg.mode:
            # has no tranceparency. use function
            newimg = ImageOps.invert(self._pilimg)
            return Dimage(newimg)

        # Invert RGB channels
        r, g, b, a = self._pilimg.split()
        r = Image.eval(r, lambda x: 255 - x)
        g = Image.eval(g, lambda x: 255 - x)
        b = Image.eval(b, lambda x: 255 - x)

        # Merge inverted RGB channels with original alpha channel
        inverted_image = Image.merge("RGBA", (r, g, b, a))
        return Dimage(inverted_image)

    @error_handler
    def grayscale(self) -> Dimage:
        """Get a new Dimage with a grayscale effect while keeping the original Dimage unchanged.

        Returns:
            Dimage: A new Dimage with a grayscale effect.
        """
        newimg = self._pilimg.convert("LA")
        return Dimage(newimg)

    @error_handler
    def brightness(self, brightness: float = 0.5) -> Dimage:
        """Get a new Dimage with changed brightness while keeping the original Dimage unchanged.

        Args:
            brightness (float): The factor by which to change the brightness. A factor of 1.0 means no change,
                                less than 1.0 means darker, and greater than 1.0 means brighter.

        Returns:
            Dimage: A new Dimage with changed brightness.
        """
        enhancer = ImageEnhance.Brightness(self._pilimg)
        newimg = enhancer.enhance(brightness)
        return Dimage(newimg)

    @error_handler
    def sepia(self) -> Dimage:
        """Get a new Dimage with a sepia effect while keeping the original Dimage unchanged.

        Returns:
            Dimage: A new Dimage with a sepia effect.
        """
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
            return Dimage(sepia_image)

        # add alpha from original
        alpha_mask = self._pilimg.split()[3]
        sepia_image.putalpha(alpha_mask)
        return Dimage(sepia_image)

    @error_handler
    def colorize(
        self,
        from_black_to: Union[Tuple[int, int, int], Tuple[int, int, int, float]],
        from_white_to: Union[Tuple[int, int, int], Tuple[int, int, int, float]],
        from_mid_to: Union[Tuple[int, int, int], Tuple[int, int, int, float], None] = None,
    ) -> Dimage:
        """Get a new Dimage with a colorize effect while keeping the original Dimage unchanged.

        Args:
            from_black_to (Union[Tuple[int, int, int], Tuple[int, int, int, float]]):
                    The color to map black to.
            from_white_to (Union[Tuple[int, int, int], Tuple[int, int, int, float]]):
                    The color to map white to.
            from_mid_to (Union[Tuple[int, int, int], Tuple[int, int, int, float], None]):
                    The color to map mid-tone to. If None, mid-tones are mapped automatically.

        Returns:
            Dimage: A new Dimage with a colorize effect.

        """
        # validate and convert
        validate_color("from_black_to", from_black_to)
        validate_color("from_white_to", from_white_to)
        b = from_black_to
        black = (b[0], b[1], b[2])
        w = from_white_to
        white = (w[0], w[1], w[2])
        if from_mid_to is not None:
            validate_color("from_mid_to", from_mid_to)
            m = from_mid_to
            mid = (m[0], m[1], m[2])
        else:
            mid = None
        # colorize
        gray = self._pilimg.convert("L")
        colorized_image = ImageOps.colorize(gray, black=black, white=white, mid=mid)  # type: ignore
        if "A" not in self._pilimg.mode:
            return Dimage(colorized_image)

        # add alpha from original
        alpha_mask = self._pilimg.split()[3]
        colorized_image.putalpha(alpha_mask)
        return Dimage(colorized_image)

    @error_handler
    def posterize(self, num_colors: int = 4) -> Dimage:
        """Get a new Dimage with a posterize effect while keeping the original Dimage unchanged.

        Args:
            num_colors (int): The number of colors to use in the posterized image. Lower values mean fewer colors.

        Returns:
            Dimage: A new Dimage with a posterize effect.
        """
        if "A" not in self._pilimg.mode:
            newimg = ImageOps.posterize(self._pilimg, num_colors)
            return Dimage(newimg)

        r, g, b, a = self._pilimg.split()
        r = ImageOps.posterize(r, num_colors)
        g = ImageOps.posterize(g, num_colors)
        b = ImageOps.posterize(b, num_colors)
        newimg = Image.merge("RGBA", (r, g, b, a))
        return Dimage(newimg)

    @error_handler
    def mosaic(self, block_size: int = 8) -> Dimage:
        """Get a new Dimage with a mosaic effect while keeping the original Dimage unchanged.

        Args:
            block_size (int): The size of the mosaic blocks. Larger values mean larger mosaic blocks.

        Returns:
            Dimage: A new Dimage with a mosaic effect.
        """
        # Ensure the image is in RGBA mode
        image = self._pilimg.convert("RGBA")
        pixels = image.load()
        width, height = image.size

        # Iterate over the blocks in the image
        for y in range(0, height, block_size):
            for x in range(0, width, block_size):
                # Initialize variables to store color sums and pixel count
                r, g, b, max_a = 0, 0, 0, 0
                count = 0

                # Calculate the average color of the current block
                for j in range(y, min(y + block_size, height)):
                    for i in range(x, min(x + block_size, width)):
                        pixel = pixels[i, j]
                        r += pixel[0]
                        g += pixel[1]
                        b += pixel[2]
                        max_a = max(pixel[3], max_a)
                        count += 1

                # Compute the average color. Use max alpha value
                avg_color = (r // count, g // count, b // count, max_a)

                # Set the color of each pixel in the block to the average color
                for j in range(y, min(y + block_size, height)):
                    for i in range(x, min(x + block_size, width)):
                        pixels[i, j] = avg_color

        # change pil image to Dimage.
        return Dimage(image)

    @error_handler
    def blur(self) -> Dimage:
        """Get a new Dimage with a blur effect while keeping the original Dimage unchanged.

        Returns:
            Dimage: A new Dimage with a blur effect.
        """
        newimg = self._pilimg.filter(ImageFilter.BLUR)
        return Dimage(newimg)

    @error_handler
    def line_extraction(self) -> Dimage:
        """Get a new Dimage with a line extraction effect while keeping the original Dimage unchanged.

        Returns:
            Dimage: A new Dimage with a line extraction effect.
        """
        gray = self._pilimg.convert("L")
        gray2 = gray.filter(ImageFilter.MaxFilter(5))
        senga_inv = ImageChops.difference(gray, gray2)
        newimg = ImageOps.invert(senga_inv)
        return Dimage(newimg)

    @error_handler
    def remove_margin(
        self,
        margin_color: Union[None, str, Tuple[int, int, int]],
    ) -> Dimage:
        """Get a new Dimage with the margins removed while keeping the original Dimage unchanged.

        Args:
            margin_color (Union[None, str, Tuple[int, int, int]]):
                    The color of the margin to remove. If None, removes transparent margins.

        Returns:
            Dimage: A new Dimage with the margins removed.

        """
        if margin_color is None:
            if "A" not in self._pilimg.mode:
                message = "Can't remove transparent margin from RGB image."
                raise ValueError(message)
            crop = self._pilimg.split()[-1].getbbox()
            new_image = self._pilimg.crop(crop)
            return Dimage(new_image)

        raise NotImplementedError("Implement later")
