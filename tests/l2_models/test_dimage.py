# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Unit tests for Dimage and DimageCache."""

import pytest
from PIL import Image

from drawlib._core.l2_models import Dimage
from drawlib._core.l2_models_._dimage import DimageCache
from drawlib._utils import dutil_canvas, dutil_color, dutil_script, dutil_settings
from drawlib.canvas import clear, config, save, show
from drawlib.colors import (
    Colors,
    Colors140,
    ColorsThemeDefault,
    ColorsThemeEssentials,
    ColorsThemeMonochrome,
)
from drawlib.fonts import (
    Font,
    FontArabic,
    FontBrahmic,
    FontChinese,
    FontFile,
    FontJapanese,
    FontKorean,
    FontMonoSpace,
    FontRoboto,
    FontSansSerif,
    FontSerif,
    FontSourceCode,
    FontThai,
)
from drawlib.icons import icon, icon_phosphor
from drawlib.images import image
from drawlib.lines import (
    line,
    line_arc,
    line_bezier1,
    line_bezier2,
    line_curved,
    lines,
    lines_bezier,
    lines_curved,
)
from drawlib.preset_styles import (
    ThemePreset,
    get_default_styles,
    get_essentials_styles,
    get_monochrome_styles,
    get_style,
    get_styles,
)
from drawlib.shapes import (
    arc,
    arrow,
    arrow_arc,
    arrow_l,
    arrow_polyline,
    arrow_u,
    chevron,
    circle,
    donuts,
    ellipse,
    fan,
    parallelogram,
    polygon,
    rectangle,
    regularpolygon,
    rhombus,
    shape,
    star,
    trapezoid,
    triangle,
    wedge,
)
from drawlib.smartarts import (
    BoxList,
    BulletPoints,
    GridLayout,
    Pyramid,
    SourceCode,
    Table,
    TreeNode,
    bubblespeech,
    dsart,
)
from drawlib.text import text, text_vertical
from drawlib.types import (
    ColorsBase,
    IconStyle,
    ImageStyle,
    LineStyle,
    ShapeStyle,
    ShapeTextStyle,
    Style,
    TextStyle,
)

IMAGE_FILE = "../assets/image.png"
FONT_FILE = "../../assets/font.ttf"
OUTPUT_DIR = "../../output_tests/l2_models/dimage/"


class TestDimageCache:
    """Test cases for DimageCache."""

    def test_cache_operations(self):
        """Test cache operations: set, get, has, list, delete."""
        pil_img = Image.new("RGBA", (1, 1), (255, 0, 0, 255))
        cache = DimageCache()

        # Empty cache checks
        assert cache.list() == []
        assert not cache.has("test_img")

        # Set cache item
        cache.set("test_img", pil_img)
        assert cache.has("test_img")
        assert cache.list() == ["test_img"]

        # Retrieve and verify cached item
        dimg = cache.get("test_img")
        assert isinstance(dimg, Dimage)
        assert dimg.get_image_size() == (1, 1)

        # Delete and verify
        cache.delete("test_img")
        assert not cache.has("test_img")
        assert cache.list() == []

        # Error case
        with pytest.raises(ValueError, match='Dimage "test_img" is not cached.'):
            cache.get("test_img")


class TestDimage:
    """Test cases for Dimage."""

    def test_file(self):
        """Test Dimage creation from file and saving."""
        img = Dimage(IMAGE_FILE)
        image((50, 50), 50, img)
        img.save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}_dimage.png")
        save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")

    def test_pil_image(self):
        """Test Dimage creation from PIL Image."""
        path = dutil_script.get_relative_path(IMAGE_FILE)
        pil_img = Image.open(path)
        img = Dimage(pil_img)
        image((50, 50), 50, img)
        img.save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}_dimage.png")
        save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")

    def test_resize(self):
        """Test Dimage resizing."""
        img = Dimage(IMAGE_FILE).resize(100, 200)
        image((50, 50), 50, img)
        img.save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}_dimage.png")
        save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")

    def test_fill1(self):
        """Test Dimage fill with color."""
        img = Dimage(IMAGE_FILE).fill(Colors.Gray)
        image((50, 50), 50, img)
        img.save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}_dimage.png")
        save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")

    def test_fill2(self):
        """Test Dimage fill with alpha and color."""
        img = Dimage(IMAGE_FILE).alpha(0.3).fill(Colors.Gray)
        image((50, 50), 50, img)
        img.save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}_dimage.png")
        save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")

    def test_alpha(self):
        """Test Dimage alpha transparency adjustment."""
        img = Dimage(IMAGE_FILE).alpha(0.3)
        image((50, 50), 50, img)
        img.save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}_dimage.png")
        save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")

    def test_crop(self):
        """Test Dimage cropping."""
        width, height = Dimage(IMAGE_FILE).get_image_size()
        img = Dimage(IMAGE_FILE).crop(int(width / 5), int(height / 5), int(width * 3 / 5), int(height * 3 / 5))
        image((50, 50), 50, img)
        img.save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}_dimage.png")
        save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")

    def test_flip(self):
        """Test Dimage vertical flipping."""
        img = Dimage(IMAGE_FILE).flip()
        image((50, 50), 50, img)
        img.save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}_dimage.png")
        save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")

    def test_mirror(self):
        """Test Dimage horizontal mirroring."""
        img = Dimage(IMAGE_FILE).mirror()
        image((50, 50), 50, img)
        img.save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}_dimage.png")
        save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")

    def test_invert(self):
        """Test Dimage color inverting."""
        img = Dimage(IMAGE_FILE).invert()
        image((50, 50), 50, img)
        img.save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}_dimage.png")
        save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")

    def test_grayscale(self):
        """Test Dimage grayscale conversion."""
        img = Dimage(IMAGE_FILE).grayscale()
        image((50, 50), 50, img)
        img.save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}_dimage.png")
        save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")

    def test_brightness(self):
        """Test Dimage brightness adjustment."""
        img = Dimage(IMAGE_FILE).brightness(0.5)
        image((50, 50), 50, img)
        img.save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}_dimage.png")
        save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")

    def test_sepia(self):
        """Test Dimage sepia effect."""
        img = Dimage(IMAGE_FILE).sepia()
        image((50, 50), 50, img)
        img.save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}_dimage.png")
        save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")

    def test_colorize(self):
        """Test Dimage colorization."""
        img = Dimage(IMAGE_FILE).colorize(from_black_to=Colors.Blue, from_white_to=(255, 0, 0, 1.0))
        image((50, 50), 50, img)
        img.save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}_dimage.png")
        save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")

    def test_colorize_mid(self):
        """Test Dimage colorization with mid-tones."""
        img = Dimage(IMAGE_FILE).colorize(
            from_black_to=Colors.Blue,
            from_white_to=Colors.Red,
            from_mid_to=Colors.Green,
        )
        image((50, 50), 50, img)
        img.save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}_dimage.png")
        save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")

    def test_posterize(self):
        """Test Dimage posterizing."""
        img = Dimage(IMAGE_FILE).posterize()
        image((50, 50), 50, img)
        img.save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}_dimage.png")
        save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")

    def test_mosaic_bs8(self):
        """Test Dimage mosaic block size 8."""
        img = Dimage(IMAGE_FILE).mosaic(block_size=8)
        image((50, 50), 50, img)
        img.save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}_dimage.png")
        save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")

    def test_mosaic_bs16(self):
        """Test Dimage mosaic block size 16."""
        img = Dimage(IMAGE_FILE).mosaic(block_size=16)
        image((50, 50), 50, img)
        img.save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}_dimage.png")
        save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")

    def test_blur(self):
        """Test Dimage blur effect."""
        img = Dimage(IMAGE_FILE).blur()
        image((50, 50), 50, img)
        img.save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}_dimage.png")
        save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")

    def test_line_extraction(self):
        """Test Dimage edge/line extraction."""
        img = Dimage(IMAGE_FILE).line_extraction()
        image((50, 50), 50, img)
        img.save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}_dimage.png")
        save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")
