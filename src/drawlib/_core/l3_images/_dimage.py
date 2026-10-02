# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
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
from collections import Counter
from typing import List, Literal, cast

import matplotlib.colors as mcolors
from PIL import (
    Image,
    ImageChops,
    ImageEnhance,
    ImageFilter,
    ImageOps,
)
from pydantic import ConfigDict, TypeAdapter, validate_call

from drawlib._core.l2_types import (
    Alpha,
    Angle,
    ColorRGB,
    ExistingFilePath,
    FilePath,
    ImageQuality,
    ImageResample,
    PosFloat,
    PosInt,
)
from drawlib._core.l3_colors import (
    Color,
    ColorType,
)

list_ = list
_existing_file_path_adapter: TypeAdapter[ExistingFilePath] = TypeAdapter(ExistingFilePath)


def _resolve_target_rgb(
    color: str | Color | tuple[int, int, int] | tuple[int, int, int, float],
) -> tuple[int, int, int]:
    """Resolve color input to RGB tuple.

    Args:
        color (str | Color | tuple[int, int, int] | tuple[int, int, int, float]):
            Target color representation.

    Returns:
        tuple[int, int, int]: Resolved RGB tuple.
    """
    if isinstance(color, Color):
        return (color.r, color.g, color.b)
    if isinstance(color, str):
        try:
            c = Color(color)
            return (c.r, c.g, c.b)
        except ValueError:
            try:
                rgb_float = mcolors.to_rgb(color)
                return (
                    int(round(rgb_float[0] * 255)),
                    int(round(rgb_float[1] * 255)),
                    int(round(rgb_float[2] * 255)),
                )
            except ValueError as e:
                raise ValueError(f"Invalid color specification: {color}") from e
    if isinstance(color, (tuple, list)):
        if len(color) in {3, 4}:
            return (int(color[0]), int(color[1]), int(color[2]))
    raise ValueError(f"Invalid color specification: {color}")


def _detect_corner_color(pilimg: Image.Image) -> tuple[int, int, int] | None:
    """Detect the dominant background color or transparency from image corners.

    Args:
        pilimg (Image.Image): The PIL image to inspect.

    Returns:
        tuple[int, int, int] | None: Detected RGB color tuple, or None if corners are transparent.
    """
    w, h = pilimg.size
    corners = [
        (0, 0),
        (max(0, w - 1), 0),
        (0, max(0, h - 1)),
        (max(0, w - 1), max(0, h - 1)),
    ]

    rgba_img = pilimg.convert("RGBA")
    corner_pixels = [rgba_img.getpixel(pos) for pos in corners]

    # If two or more corners are fully transparent, treat background as transparent
    transparent_count = sum(1 for p in corner_pixels if p[3] == 0)
    if transparent_count >= 2:
        return None

    # Otherwise, find the most common RGB color among non-transparent corners
    rgb_pixels = [p[:3] for p in corner_pixels if p[3] > 0]
    if not rgb_pixels:
        return None
    counter = Counter(rgb_pixels)
    most_common_rgb = counter.most_common(1)[0][0]
    return (most_common_rgb[0], most_common_rgb[1], most_common_rgb[2])


class Dimage:
    """A wrapper class for handling images with easy methods for reading, writing, and applying effects.

    This class provides simple methods for reading, writing, and applying effects to images.
    It serves as a wrapper for `PIL.Image.Image`, allowing users to get and set PIL images
    from this class. For advanced effects, users should directly use the PIL Image class.
    """

    def __init__(
        self,
        image: ExistingFilePath | Dimage | Image.Image,
        copy: bool = False,
    ) -> None:
        """Initialize a Dimage instance from a file path, PIL Image, or another Dimage.

        This constructor initializes a Dimage instance from a given image source.
        The source can be a file path, a PIL Image, or another Dimage. If `copy` is
        True, a copy of the image is made; otherwise, the original image is used.

        Args:
            image (str | Dimage | PIL.Image.Image): The source image to initialize the Dimage.
                If a relative file path is provided, it is resolved relative to the caller script directory.
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
        if isinstance(image, (str, os.PathLike)):
            image_path = _existing_file_path_adapter.validate_python(image)
            self._pilimg = Image.open(image_path)

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

    def get_pil_image(self) -> Image.Image:
        """Get a copied PIL Image.

        This method returns a copy of the PIL Image held by the Dimage instance.
        Modifications to the returned PIL Image do not affect the original Dimage.

        Returns:
            PIL.Image.Image: A copy of the PIL Image.
        """
        return self._pilimg.copy()

    def get_image_size(self) -> tuple[int, int]:
        """Get the size of the image.

        This method returns the width and height of the image as a tuple.

        Returns:
            tuple[int, int]: A tuple containing the width and height of the image.
        """
        width, height = self._pilimg.size
        return (width, height)

    def copy(self) -> Dimage:
        """Get a copied Dimage.

        This method creates and returns another Dimage instance with the same content.

        Returns:
            Dimage: A deep copied Dimage instance.
        """
        return Dimage(self)

    @validate_call
    def save(self, file: FilePath, quality: ImageQuality = 95) -> None:
        """Save the Dimage data to a file.

        This method saves the image to the specified file path. If a relative path
        is provided, it is resolved relative to the caller script directory.

        Args:
            file (str): The file path to save the image. If a relative path is provided,
                it is resolved relative to the caller script directory.
            quality (int, optional): The quality of the saved image (0-100). Defaults to 95.

        Returns:
            None
        """
        directory = os.path.dirname(file)
        if directory:
            os.makedirs(directory, exist_ok=True)
        self._pilimg.save(file, quality=quality)

    def _rotate(self, angle: Angle, resample: ImageResample = "bicubic") -> Dimage:
        """Get a new Dimage that is rotated. The original Dimage is kept unchanged.

        This method returns a new Dimage that is rotated by the specified angle.

        Args:
            angle (float): The angle to rotate the image by, between 0.0 and 360.0 degrees.
                           The pixel size can change, and new areas become transparent.
            resample (Literal["nearest", "bilinear", "bicubic", "lanczos"] | str, optional):
                The resampling method to use. Defaults to "bicubic".

        Returns:
            Dimage: A new rotated image.
        """
        resample_map = {
            "nearest": Image.Resampling.NEAREST,
            "box": Image.Resampling.BOX,
            "bilinear": Image.Resampling.BILINEAR,
            "hamming": Image.Resampling.HAMMING,
            "bicubic": Image.Resampling.BICUBIC,
            "lanczos": Image.Resampling.LANCZOS,
        }
        newimg = self._pilimg.rotate(
            angle,
            resample=resample_map[resample],
            expand=True,
        )
        return Dimage(newimg)

    def resize(self, width: PosInt, height: PosInt, resample: ImageResample = "lanczos") -> Dimage:
        """Get a new Dimage that is resized. The original Dimage is kept unchanged.

        This method returns a new Dimage that is resized to the specified width and height.

        Args:
            width (int): The new width of the image.
            height (int): The new height of the image.
            resample (Literal["nearest", "bilinear", "bicubic", "lanczos"] | str, optional):
                The resampling method to use. Defaults to "lanczos".

        Returns:
            Dimage: A new resized image.
        """
        resample_map = {
            "nearest": Image.Resampling.NEAREST,
            "box": Image.Resampling.BOX,
            "bilinear": Image.Resampling.BILINEAR,
            "hamming": Image.Resampling.HAMMING,
            "bicubic": Image.Resampling.BICUBIC,
            "lanczos": Image.Resampling.LANCZOS,
        }
        newimg = self._pilimg.resize(
            (width, height),
            resample=resample_map[resample],
        )
        return Dimage(newimg)

    def crop(self, x: PosInt, y: PosInt, width: PosInt, height: PosInt) -> Dimage:
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

    def flip(self) -> Dimage:
        """Get a new Dimage that is flipped vertically. The original Dimage is kept unchanged.

        Returns:
            Dimage: A new vertically flipped image.
        """
        newimg = ImageOps.flip(self._pilimg)
        return Dimage(newimg)

    def mirror(self) -> Dimage:
        """Get a new Dimage that is mirrored horizontally. The original Dimage is kept unchanged.

        Returns:
            Dimage: A new horizontally mirrored image.
        """
        newimg = ImageOps.mirror(self._pilimg)
        return Dimage(newimg)

    def fill(self, color: ColorType) -> Dimage:
        """Get a new Dimage with the specified color filling the transparent areas.

        Args:
            color (Color):
                   The color to fill the transparent areas with. It can be an RGB or RGBA tuple.

        Returns:
            Dimage: A new image with the transparent areas filled with the specified color.
        """
        # const
        tuple_length_has_alpha = 4
        alpha_transparent = 0
        alpha_opaque = 255

        pil_color = (color[0], color[1], color[2], 255)

        pil_image = self._pilimg.convert("RGBA")
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

    def alpha(self, alpha: Alpha) -> Dimage:
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

    def grayscale(self) -> Dimage:
        """Get a new Dimage with a grayscale effect while keeping the original Dimage unchanged.

        Returns:
            Dimage: A new Dimage with a grayscale effect.
        """
        newimg = self._pilimg.convert("LA")
        return Dimage(newimg)

    def brightness(self, brightness: PosFloat = 0.5) -> Dimage:
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

    def colorize(
        self,
        from_black_to: ColorType,
        from_white_to: ColorType,
        from_mid_to: ColorType | None = None,
    ) -> Dimage:
        """Get a new Dimage with a colorize effect while keeping the original Dimage unchanged.

        Args:
            from_black_to (Color):
                    The color to map black to.
            from_white_to (Color):
                    The color to map white to.
            from_mid_to (Color | None):
                    The color to map mid-tone to. If None, mid-tones are mapped automatically.

        Returns:
            Dimage: A new Dimage with a colorize effect.

        """
        # validate and convert
        b = from_black_to
        black = (b[0], b[1], b[2])
        w = from_white_to
        white = (w[0], w[1], w[2])
        if from_mid_to is not None:
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

    def posterize(self, num_colors: PosInt = 4) -> Dimage:
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

    def mosaic(self, block_size: PosInt = 8) -> Dimage:
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

    def blur(self) -> Dimage:
        """Get a new Dimage with a blur effect while keeping the original Dimage unchanged.

        Returns:
            Dimage: A new Dimage with a blur effect.
        """
        newimg = self._pilimg.filter(ImageFilter.BLUR)
        return Dimage(newimg)

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

    def trim(
        self,
        color: str | Color | tuple[int, int, int] | tuple[int, int, int, float] | None = "auto",
        tolerance: int = 0,
    ) -> Dimage:
        """Get a new Dimage with background margins cropped while keeping the original unchanged.

        Args:
            color (str | Color | tuple[int, int, int] | tuple[int, int, int, float] | None):
                Target background color to crop.
                - "auto": Automatically detects background color or transparency from image corners.
                - None: Crops transparent margins (requires alpha channel).
                - Color / str / tuple: Specific color to trim as margin.
            tolerance (int): Color distance tolerance (0-255). Default is 0.

        Returns:
            Dimage: A new cropped Dimage.

        Raises:
            ValueError: If tolerance is out of range, or if trimming transparent margin on image without alpha.
        """
        if not (0 <= tolerance <= 255):
            raise ValueError("Arg 'tolerance' must be between 0 and 255.")

        target_rgb: tuple[int, int, int] | None
        if color == "auto":
            target_rgb = _detect_corner_color(self._pilimg)
        elif color is None:
            target_rgb = None
        else:
            target_rgb = _resolve_target_rgb(color)

        if target_rgb is None:
            if "A" not in self._pilimg.mode:
                raise ValueError("Cannot trim transparent margin from an image without alpha channel.")
            alpha = self._pilimg.split()[-1]
            if tolerance > 0:
                alpha_mask = alpha.point(lambda p: 255 if p > tolerance else 0)
                bbox = alpha_mask.getbbox()
            else:
                bbox = alpha.getbbox()
            if bbox:
                return Dimage(self._pilimg.crop(bbox))
            return Dimage(self._pilimg)

        bg = Image.new("RGB", self._pilimg.size, target_rgb)
        diff = ImageChops.difference(self._pilimg.convert("RGB"), bg)
        r_diff, g_diff, b_diff = diff.split()
        max_diff = ImageChops.lighter(ImageChops.lighter(r_diff, g_diff), b_diff)
        content_mask = max_diff.point(lambda p: 255 if p > tolerance else 0)

        if "A" in self._pilimg.mode:
            orig_alpha = self._pilimg.split()[-1]
            alpha_mask = orig_alpha.point(lambda p: 255 if p > tolerance else 0)
            content_mask = ImageChops.darker(content_mask, alpha_mask)

        bbox = content_mask.getbbox()
        if bbox:
            return Dimage(self._pilimg.crop(bbox))
        return Dimage(self._pilimg)

    def make_transparent(
        self,
        color: str | Color | tuple[int, int, int] | tuple[int, int, int, float] | Literal["auto"] = "auto",
        tolerance: int = 0,
    ) -> Dimage:
        """Get a new Dimage with the specified background color turned transparent.

        Args:
            color (str | Color | tuple[int, int, int] | tuple[int, int, int, float] | Literal["auto"]):
                Target color to make transparent.
                - "auto": Automatically detects background color from corners.
                - Color / str / tuple: Specific color to convert to transparent.
            tolerance (int): Color distance tolerance (0-255). Default is 0.

        Returns:
            Dimage: A new Dimage in RGBA mode with background turned transparent.

        Raises:
            ValueError: If tolerance is out of range.
        """
        if not (0 <= tolerance <= 255):
            raise ValueError("Arg 'tolerance' must be between 0 and 255.")

        target_rgb: tuple[int, int, int] | None
        if color == "auto":
            target_rgb = _detect_corner_color(self._pilimg)
            if target_rgb is None:
                return Dimage(self._pilimg.convert("RGBA"))
        else:
            target_rgb = _resolve_target_rgb(color)

        rgba = self._pilimg.convert("RGBA")
        bg = Image.new("RGB", rgba.size, target_rgb)
        diff = ImageChops.difference(rgba.convert("RGB"), bg)
        r_diff, g_diff, b_diff = diff.split()
        max_diff = ImageChops.lighter(ImageChops.lighter(r_diff, g_diff), b_diff)

        mask = max_diff.point(lambda p: 0 if p <= tolerance else 255)

        orig_alpha = rgba.split()[3]
        new_alpha = ImageChops.darker(orig_alpha, mask)

        rgba.putalpha(new_alpha)
        return Dimage(rgba)
