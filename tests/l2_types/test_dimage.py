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
from drawlib.preset_colors import Colors

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
        img = Dimage(IMAGE_FILE).fill(Colors.Gray)
        image((50, 50), 50, img)
        img.save(f"{OUTPUT_DIR}test_fill1_dimage.png")
        save(f"{OUTPUT_DIR}test_fill1.png")

    def test_fill2(self):
        """Test Dimage fill with alpha and color."""
        img = Dimage(IMAGE_FILE).alpha(0.3).fill(Colors.Gray)
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
