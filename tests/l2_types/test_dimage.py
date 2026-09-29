# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Unit tests for Dimage."""

from pathlib import Path

import pytest
from PIL import Image

from drawlib._core.l2_types import Dimage
from drawlib.canvas import save
from drawlib.images import image
from drawlib.styles import Colors

IMAGE_FILE = "../assets/image.png"
FONT_FILE = "../../assets/font.ttf"
OUTPUT_DIR = "../../output_tests/l2_types/dimage/"


@pytest.mark.image_threshold(70.0)
class TestDimage:
    """Test cases for Dimage."""

    def test_file(self):
        """Test Dimage creation from file and saving."""
        img = Dimage(IMAGE_FILE)
        image((50, 50), 50, img)
        img.save(f"{OUTPUT_DIR}test_file_dimage.png")
        save(f"{OUTPUT_DIR}test_file.png")

    def test_pil_image(self):
        """Test Dimage creation from PIL Image."""
        path = (Path(__file__).parent / IMAGE_FILE).resolve()
        pil_img = Image.open(path)
        img = Dimage(pil_img)
        image((50, 50), 50, img)
        img.save(f"{OUTPUT_DIR}test_pil_image_dimage.png")
        save(f"{OUTPUT_DIR}test_pil_image.png")

    def test_resize(self):
        """Test Dimage resizing."""
        img = Dimage(IMAGE_FILE).resize(100, 200)
        image((50, 50), 50, img)
        img.save(f"{OUTPUT_DIR}test_resize_dimage.png")
        save(f"{OUTPUT_DIR}test_resize.png")

    def test_fill1(self):
        """Test Dimage fill with color."""
        img = Dimage(IMAGE_FILE).fill(Colors.Gray4)
        image((50, 50), 50, img)
        img.save(f"{OUTPUT_DIR}test_fill1_dimage.png")
        save(f"{OUTPUT_DIR}test_fill1.png")

    def test_fill2(self):
        """Test Dimage fill with alpha and color."""
        img = Dimage(IMAGE_FILE).alpha(0.3).fill(Colors.Gray4)
        image((50, 50), 50, img)
        img.save(f"{OUTPUT_DIR}test_fill2_dimage.png")
        save(f"{OUTPUT_DIR}test_fill2.png")

    def test_alpha(self):
        """Test Dimage alpha transparency adjustment."""
        img = Dimage(IMAGE_FILE).alpha(0.3)
        image((50, 50), 50, img)
        img.save(f"{OUTPUT_DIR}test_alpha_dimage.png")
        save(f"{OUTPUT_DIR}test_alpha.png")

    def test_crop(self):
        """Test Dimage cropping."""
        width, height = Dimage(IMAGE_FILE).get_image_size()
        img = Dimage(IMAGE_FILE).crop(int(width / 5), int(height / 5), int(width * 3 / 5), int(height * 3 / 5))
        image((50, 50), 50, img)
        img.save(f"{OUTPUT_DIR}test_crop_dimage.png")
        save(f"{OUTPUT_DIR}test_crop.png")

    def test_flip(self):
        """Test Dimage vertical flipping."""
        img = Dimage(IMAGE_FILE).flip()
        image((50, 50), 50, img)
        img.save(f"{OUTPUT_DIR}test_flip_dimage.png")
        save(f"{OUTPUT_DIR}test_flip.png")

    def test_mirror(self):
        """Test Dimage horizontal mirroring."""
        img = Dimage(IMAGE_FILE).mirror()
        image((50, 50), 50, img)
        img.save(f"{OUTPUT_DIR}test_mirror_dimage.png")
        save(f"{OUTPUT_DIR}test_mirror.png")

    def test_invert(self):
        """Test Dimage color inverting."""
        img = Dimage(IMAGE_FILE).invert()
        image((50, 50), 50, img)
        img.save(f"{OUTPUT_DIR}test_invert_dimage.png")
        save(f"{OUTPUT_DIR}test_invert.png")

    def test_grayscale(self):
        """Test Dimage grayscale conversion."""
        img = Dimage(IMAGE_FILE).grayscale()
        image((50, 50), 50, img)
        img.save(f"{OUTPUT_DIR}test_grayscale_dimage.png")
        save(f"{OUTPUT_DIR}test_grayscale.png")

    def test_brightness(self):
        """Test Dimage brightness adjustment."""
        img = Dimage(IMAGE_FILE).brightness(0.5)
        image((50, 50), 50, img)
        img.save(f"{OUTPUT_DIR}test_brightness_dimage.png")
        save(f"{OUTPUT_DIR}test_brightness.png")

    def test_sepia(self):
        """Test Dimage sepia effect."""
        img = Dimage(IMAGE_FILE).sepia()
        image((50, 50), 50, img)
        img.save(f"{OUTPUT_DIR}test_sepia_dimage.png")
        save(f"{OUTPUT_DIR}test_sepia.png")

    def test_colorize(self):
        """Test Dimage colorization."""
        img = Dimage(IMAGE_FILE).colorize(from_black_to=Colors.Blue, from_white_to=(255, 0, 0, 1.0))
        image((50, 50), 50, img)
        img.save(f"{OUTPUT_DIR}test_colorize_dimage.png")
        save(f"{OUTPUT_DIR}test_colorize.png")

    def test_colorize_mid(self):
        """Test Dimage colorization with mid-tones."""
        img = Dimage(IMAGE_FILE).colorize(
            from_black_to=Colors.Blue,
            from_white_to=Colors.Red,
            from_mid_to=Colors.Green,
        )
        image((50, 50), 50, img)
        img.save(f"{OUTPUT_DIR}test_colorize_mid_dimage.png")
        save(f"{OUTPUT_DIR}test_colorize_mid.png")

    def test_posterize(self):
        """Test Dimage posterizing."""
        img = Dimage(IMAGE_FILE).posterize()
        image((50, 50), 50, img)
        img.save(f"{OUTPUT_DIR}test_posterize_dimage.png")
        save(f"{OUTPUT_DIR}test_posterize.png")

    def test_mosaic_bs8(self):
        """Test Dimage mosaic block size 8."""
        img = Dimage(IMAGE_FILE).mosaic(block_size=8)
        image((50, 50), 50, img)
        img.save(f"{OUTPUT_DIR}test_mosaic_bs8_dimage.png")
        save(f"{OUTPUT_DIR}test_mosaic_bs8.png")

    def test_mosaic_bs16(self):
        """Test Dimage mosaic block size 16."""
        img = Dimage(IMAGE_FILE).mosaic(block_size=16)
        image((50, 50), 50, img)
        img.save(f"{OUTPUT_DIR}test_mosaic_bs16_dimage.png")
        save(f"{OUTPUT_DIR}test_mosaic_bs16.png")

    def test_blur(self):
        """Test Dimage blur effect."""
        img = Dimage(IMAGE_FILE).blur()
        image((50, 50), 50, img)
        img.save(f"{OUTPUT_DIR}test_blur_dimage.png")
        save(f"{OUTPUT_DIR}test_blur.png")

    def test_line_extraction(self):
        """Test Dimage edge/line extraction."""
        img = Dimage(IMAGE_FILE).line_extraction()
        image((50, 50), 50, img)
        img.save(f"{OUTPUT_DIR}test_line_extraction_dimage.png")
        save(f"{OUTPUT_DIR}test_line_extraction.png")


class TestDimageTrimAndTransparent:
    """Test cases for Dimage.trim() and Dimage.make_transparent()."""

    def test_trim_auto_solid_color(self) -> None:
        """Test trim with auto detection of solid background color."""
        # 100x100 white image with 40x40 red square in center (30..70, 30..70)
        im = Image.new("RGB", (100, 100), (255, 255, 255))
        for x in range(30, 70):
            for y in range(30, 70):
                im.putpixel((x, y), (255, 0, 0))

        dimg = Dimage(im)
        trimmed = dimg.trim()
        assert trimmed.get_image_size() == (40, 40)

    def test_trim_specific_color(self) -> None:
        """Test trim with a specific color provided as string or tuple."""
        im = Image.new("RGB", (100, 100), (0, 0, 255))
        for x in range(25, 75):
            for y in range(20, 80):
                im.putpixel((x, y), (0, 255, 0))

        dimg = Dimage(im)
        trimmed_str = dimg.trim(color="blue")
        assert trimmed_str.get_image_size() == (50, 60)

        trimmed_tuple = dimg.trim(color=(0, 0, 255))
        assert trimmed_tuple.get_image_size() == (50, 60)

    def test_trim_transparent_margin(self) -> None:
        """Test trim on RGBA image with transparent margin."""
        # 100x100 transparent image with 20x20 opaque square (40..60, 40..60)
        im = Image.new("RGBA", (100, 100), (0, 0, 0, 0))
        for x in range(40, 60):
            for y in range(40, 60):
                im.putpixel((x, y), (255, 255, 0, 255))

        dimg = Dimage(im)
        # auto should detect transparent corners
        trimmed_auto = dimg.trim(color="auto")
        assert trimmed_auto.get_image_size() == (20, 20)

        # explicit None
        trimmed_none = dimg.trim(color=None)
        assert trimmed_none.get_image_size() == (20, 20)

    def test_trim_transparent_error_on_rgb(self) -> None:
        """Test trim transparent margin on RGB image raises ValueError."""
        im = Image.new("RGB", (50, 50), (255, 255, 255))
        dimg = Dimage(im)
        with pytest.raises(ValueError, match="Cannot trim transparent margin"):
            dimg.trim(color=None)

    def test_trim_tolerance(self) -> None:
        """Test trim with color tolerance."""
        # 100x100 image with corner (255, 255, 255), margin (250, 250, 250), center (0, 0, 0)
        im = Image.new("RGB", (100, 100), (250, 250, 250))
        im.putpixel((0, 0), (255, 255, 255))
        im.putpixel((99, 0), (255, 255, 255))
        im.putpixel((0, 99), (255, 255, 255))
        im.putpixel((99, 99), (255, 255, 255))
        for x in range(40, 60):
            for y in range(40, 60):
                im.putpixel((x, y), (0, 0, 0))

        dimg = Dimage(im)
        # Without tolerance, (250, 250, 250) won't match (255, 255, 255)
        # With tolerance=10, (250, 250, 250) is treated as margin
        trimmed = dimg.trim(tolerance=10)
        assert trimmed.get_image_size() == (20, 20)

    def test_make_transparent_auto(self) -> None:
        """Test make_transparent with auto detection of background color."""
        im = Image.new("RGB", (50, 50), (255, 255, 255))
        for x in range(20, 30):
            for y in range(20, 30):
                im.putpixel((x, y), (255, 0, 0))

        dimg = Dimage(im)
        trans = dimg.make_transparent()
        pil_res = trans.get_pil_image()
        assert pil_res.mode == "RGBA"
        assert pil_res.size == (50, 50)
        # Corner should be transparent
        assert pil_res.getpixel((0, 0))[3] == 0
        # Red center should remain opaque
        assert pil_res.getpixel((25, 25)) == (255, 0, 0, 255)

    def test_make_transparent_specific_color(self) -> None:
        """Test make_transparent with specific color."""
        im = Image.new("RGB", (50, 50), (0, 0, 255))
        im.putpixel((25, 25), (0, 0, 0))

        dimg = Dimage(im)
        trans = dimg.make_transparent(color="blue")
        pil_res = trans.get_pil_image()
        assert pil_res.getpixel((0, 0))[3] == 0
        assert pil_res.getpixel((25, 25)) == (0, 0, 0, 255)

    def test_make_transparent_tolerance(self) -> None:
        """Test make_transparent with color tolerance."""
        im = Image.new("RGB", (50, 50), (250, 250, 250))
        im.putpixel((25, 25), (0, 0, 0))

        dimg = Dimage(im)
        # Target white (255, 255, 255), diff is 5
        trans_no_tol = dimg.make_transparent(color=(255, 255, 255), tolerance=0)
        assert trans_no_tol.get_pil_image().getpixel((0, 0))[3] == 255  # Not matched

        trans_with_tol = dimg.make_transparent(color=(255, 255, 255), tolerance=10)
        assert trans_with_tol.get_pil_image().getpixel((0, 0))[3] == 0  # Matched and made transparent

    def test_invalid_tolerance(self) -> None:
        """Test out-of-range tolerance raises ValueError."""
        im = Image.new("RGB", (10, 10), (255, 255, 255))
        dimg = Dimage(im)
        with pytest.raises(ValueError, match="tolerance"):
            dimg.trim(tolerance=-1)
        with pytest.raises(ValueError, match="tolerance"):
            dimg.trim(tolerance=256)
        with pytest.raises(ValueError, match="tolerance"):
            dimg.make_transparent(tolerance=-5)
