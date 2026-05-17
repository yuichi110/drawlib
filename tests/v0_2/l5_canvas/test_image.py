# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Unit and integration tests for CanvasImageFeature."""

import os

import pytest
from PIL import Image

from drawlib.v0_2.apis import (
    Colors,
    Dimage,
    ImageStyle,
    clear,
    config,
    image,
    save,
)

# ruff: noqa: F403, F405

IMAGE_FILE = os.path.normpath(os.path.join(os.path.dirname(__file__), "../../assets/image.png"))
OUTPUT_DIR = "../../../output_tests/v0_2/l5_canvas/image/"


class TestCanvasImage:
    """Tests for the CanvasImageFeature class and image rendering operations."""

    def test_file_image(self) -> None:
        """Verify image loading from a file path."""
        clear()
        image(xy=(50, 50), width=30, image=IMAGE_FILE)
        save(f"{OUTPUT_DIR}test_file.png")

    def test_pil_image(self) -> None:
        """Verify image loading from a PIL Image object."""
        clear()
        im = Image.open(IMAGE_FILE)
        image(xy=(50, 50), width=30, image=im)
        save(f"{OUTPUT_DIR}test_pil.png")

    def test_dimage_image(self) -> None:
        """Verify image loading from a Dimage object."""
        clear()
        pimg = Dimage(IMAGE_FILE)
        image(xy=(50, 50), width=30, image=pimg)
        save(f"{OUTPUT_DIR}test_pimage.png")

    def test_cache_image(self) -> None:
        """Verify image retrieval and caching in Dimage."""
        clear()
        pimg = Dimage(IMAGE_FILE)
        Dimage.cache.set("linux", pimg)
        assert Dimage.cache.list() == ["linux"]
        pimg2 = Dimage.cache.get("linux")
        image(xy=(50, 50), width=30, image=pimg2)
        save(f"{OUTPUT_DIR}test_cache.png")

    def test_image_angles(self) -> None:
        """Verify image rotation at different angles."""
        clear()
        image(xy=(50, 50), width=30, angle=45, image=IMAGE_FILE)
        image(xy=(50, 50), width=30, angle=90, image=IMAGE_FILE)
        image(xy=(50, 50), width=30, angle=135, image=IMAGE_FILE)
        save(f"{OUTPUT_DIR}test_file_angles.png")

    def test_image_border_and_alignment(self) -> None:
        """Verify drawing image borders and using different alignments."""
        clear()
        # Border
        image(
            xy=(25, 50),
            width=30,
            image=IMAGE_FILE,
            style=ImageStyle(lwidth=2),
        )

        # Left bottom alignment
        image(
            xy=(55, 25),
            width=30,
            image=IMAGE_FILE,
            style=ImageStyle(lwidth=2, halign="left", valign="bottom"),
        )
        save(f"{OUTPUT_DIR}test_file_border.png")

    def test_image_effects(self) -> None:
        """Verify image styling fills and alphas."""
        clear()
        # Gray fill
        image(
            xy=(50, 50),
            width=30,
            image=IMAGE_FILE,
            style=ImageStyle(fcolor=Colors.Gray),
        )

        # Alpha adjustment
        config(grid_only=True, background_color=Colors.Gray)
        image(
            xy=(50, 50),
            width=30,
            image=IMAGE_FILE,
            style=ImageStyle(alpha=0.1),
        )
        save(f"{OUTPUT_DIR}test_file_effects.png")

    def test_file_border_angle45(self) -> None:
        """Verify image border drawing combined with a rotation angle."""
        clear()
        image(
            xy=(50, 50),
            width=30,
            image=IMAGE_FILE,
            angle=45,
            style=ImageStyle(lwidth=2),
        )
        save(f"{OUTPUT_DIR}test_file_border_angle45.png")

    def test_invalid_alignments_raise_value_error(self) -> None:
        """Verify that invalid alignment styles raise ValueErrors."""
        clear()
        with pytest.raises(ValueError):
            # invalid halign
            image(
                xy=(50, 50),
                width=30,
                image=IMAGE_FILE,
                style=ImageStyle(halign="invalid_halign"),  # type: ignore
            )
