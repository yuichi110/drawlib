# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Unit and integration tests for Pyramid smart art."""

from drawlib.v0_2.apis import (
    clear,
    dsart,
    save,
)

OUTPUT_DIR = "../../../output_tests/v0_2/l7_smartarts/pyramid/"


class TestPyramid:
    """Tests for the Pyramid class drawing operations."""

    def test_pyramid_default(self) -> None:
        """Verify basic Pyramid drawing with default vertex order and reversed base-to-vertex order."""
        clear()
        p = dsart.Pyramid(default_style="solid")
        p.add(text="Hello")
        p.add(text="World")
        p.add(text="A")
        p.draw((10, 10), 30, 30, 2)
        p.draw((60, 10), 30, 30, 2, order="base_to_vertex")
        save(f"{OUTPUT_DIR}test_pyramid_default.png")

    def test_pyramid_align_bottom(self) -> None:
        """Verify Pyramid drawing aligned bottom."""
        clear()
        p = dsart.Pyramid(default_style="solid")
        p.add(text="Hello")
        p.add(text="World")
        p.add(text="A")
        p.draw((10, 10), 30, 30, 2, align="bottom")
        p.draw((60, 10), 30, 30, 2, align="bottom", order="base_to_vertex")
        save(f"{OUTPUT_DIR}test_pyramid_align_bottom.png")

    def test_pyramid_align_top(self) -> None:
        """Verify Pyramid drawing aligned top."""
        clear()
        p = dsart.Pyramid(default_style="solid")
        p.add(text="Hello")
        p.add(text="World")
        p.add(text="A")
        p.draw((10, 10), 30, 30, 2, align="top")
        p.draw((60, 10), 30, 30, 2, align="top", order="base_to_vertex")
        save(f"{OUTPUT_DIR}test_pyramid_align_top.png")

    def test_pyramid_align_left(self) -> None:
        """Verify Pyramid drawing aligned left."""
        clear()
        p = dsart.Pyramid(default_style="solid")
        p.add(text="Hello")
        p.add(text="World")
        p.add(text="A")
        p.draw((10, 10), 30, 30, 2, align="left")
        p.draw((60, 10), 30, 30, 2, align="left", order="base_to_vertex")
        save(f"{OUTPUT_DIR}test_pyramid_align_left.png")

    def test_pyramid_align_right(self) -> None:
        """Verify Pyramid drawing aligned right."""
        clear()
        p = dsart.Pyramid(default_style="solid")
        p.add(text="Hello")
        p.add(text="World")
        p.add(text="A")
        p.draw((10, 10), 30, 30, 2, align="right")
        p.draw((60, 10), 30, 30, 2, align="right", order="base_to_vertex")
        save(f"{OUTPUT_DIR}test_pyramid_align_right.png")
