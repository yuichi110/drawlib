# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Unit and integration tests for get_dimage_from_code utility."""

import os

import pytest

from drawlib.canvas import canvas, clear, config
from drawlib.images import Dimage, get_dimage_from_code, image
from drawlib.shapes import circle
from drawlib.types import Style


class TestGetDimageFromCode:
    """Tests for get_dimage_from_code multiprocessing rendering function."""

    def test_get_dimage_from_code_basic(self) -> None:
        """Verify basic code execution returns a valid Dimage instance."""
        code = """
from drawlib.canvas import config
from drawlib.shapes import circle
from drawlib.types import Style

config(width=100, height=100)
style = Style(shape_fill_color=(100, 100, 200, 1.0), shape_line_color=(0, 0, 0, 1.0), shape_line_width=1.0)
circle((50, 50), radius=30, style=style)
"""
        dimg = get_dimage_from_code(code)
        assert isinstance(dimg, Dimage)
        width, height = dimg.get_image_size()
        assert width > 0
        assert height > 0
        assert width == 1000
        assert height == 1000

    def test_get_dimage_from_code_ignores_save(self) -> None:
        """Verify save() calls inside the code snippet are intercepted and ignored."""
        target_file = os.path.normpath(os.path.join(os.path.dirname(__file__), "should_not_exist.png"))
        if os.path.exists(target_file):
            os.remove(target_file)

        code = f"""
from drawlib.canvas import config, save
from drawlib.shapes import circle
from drawlib.types import Style

config(width=50, height=50)
style = Style(shape_fill_color=(100, 100, 200, 1.0), shape_line_color=(0, 0, 0, 1.0), shape_line_width=1.0)
circle((25, 25), radius=15, style=style)
save(r"{target_file}")
"""
        dimg = get_dimage_from_code(code)
        assert isinstance(dimg, Dimage)
        assert not os.path.exists(target_file)

    def test_get_dimage_from_code_isolation(self) -> None:
        """Verify executing get_dimage_from_code leaves parent canvas state intact."""
        clear()
        config(width=200, height=100)
        shape_style = Style(
            shape_fill_color=(100, 100, 200, 1.0), shape_line_color=(0, 0, 0, 1.0), shape_line_width=1.0
        )
        circle((50, 50), radius=20, style=shape_style)

        # Execute code in subprocess with explicit imports
        code = """
from drawlib.canvas import config
from drawlib.shapes import rectangle
from drawlib.types import Style

config(width=50, height=50)
style = Style(shape_fill_color=(100, 100, 200, 1.0), shape_line_color=(0, 0, 0, 1.0), shape_line_width=1.0)
rectangle((25, 25), width=20, height=20, style=style)
"""
        sub_img = get_dimage_from_code(code)
        assert isinstance(sub_img, Dimage)

        # Parent canvas should still have width=200, height=100, and 1 artist
        assert canvas._width == 200
        assert canvas._height == 100
        assert len(canvas._artists) == 1

        # Use the generated sub_img on the parent canvas
        img_style = Style(image_border_width=0)
        image((150, 50), width=40, style=img_style, image=sub_img)
        assert len(canvas._artists) > 1

    def test_get_dimage_from_code_syntax_error(self) -> None:
        """Verify syntax or execution errors in code snippet raise RuntimeError."""
        code = "invalid python code ))(("
        with pytest.raises(RuntimeError) as exc_info:
            get_dimage_from_code(code)
        assert "SyntaxError" in str(exc_info.value)

    def test_get_dimage_from_code_timeout(self) -> None:
        """Verify timeout parameter aborts execution and raises TimeoutError."""
        code = "import time\ntime.sleep(2)\n"
        with pytest.raises(TimeoutError):
            get_dimage_from_code(code, timeout=0.2)
