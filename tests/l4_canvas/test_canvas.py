# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Unit and integration tests for Canvas class and saving/showing logic."""

import os

import pytest
from matplotlib import pyplot

from drawlib._core.l4_canvas import canvas
from drawlib.canvas import clear, config, get_dimage, save, show
from drawlib.colors import (
    Colors,
    Colors140,
)
from drawlib.images import Dimage, image
from drawlib.shapes import circle
from drawlib.types import Style

OUTPUT_DIR = "../../output_tests/l4_canvas/canvas/"


class TestCanvas:
    """Tests for the Canvas class and global canvas state/drawing pipeline."""

    def test_save_without_filename(self) -> None:
        """Verify saving without a filename auto-infers script context name."""
        target_path = os.path.normpath(os.path.join(os.path.dirname(__file__), "test_canvas.png"))
        if os.path.exists(target_path):
            os.remove(target_path)

        clear()
        circle((50, 50), 30)
        # Saves to directory of running script with default "png" format
        save()
        # Ensure file got saved
        assert os.path.exists(target_path)
        os.remove(target_path)

    def test_save_with_format(self) -> None:
        """Verify format argument overrides default extension."""
        target_path = os.path.normpath(os.path.join(os.path.dirname(__file__), "test_canvas.webp"))
        if os.path.exists(target_path):
            os.remove(target_path)

        clear()
        circle((50, 50), 30)
        save(format="webp")
        assert os.path.exists(target_path)
        os.remove(target_path)

    def test_canvas_config_grid(self) -> None:
        """Verify canvas grid-only and standard save options work correctly."""
        clear()
        config(width=192, height=108, grid_only=True)
        save(f"{OUTPUT_DIR}test_size.png")

        clear()
        config(width=200, height=100, grid_only=True, grid_xpitch=10, grid_ypitch=50)
        save(f"{OUTPUT_DIR}test_grid_pitch.png")

        clear()
        config(grid_only=True, dpi=200)
        save(f"{OUTPUT_DIR}test_dpi.png")

        clear()
        config(
            background_color=Colors140.Orange,
            background_alpha=0.2,
            grid_only=True,
        )
        save(f"{OUTPUT_DIR}test_background.png")

        clear()
        config(
            grid_only=True,
            grid_style=Style(
                line_width=1,
                line_color=Colors.Red,
                line_style="dashed",
            ),
        )
        save(f"{OUTPUT_DIR}test_grid.png")

        clear()
        circle((50, 50), 30)
        save(f"{OUTPUT_DIR}test_nogrid.png")

        clear()
        config(grid=True)
        circle((50, 50), 30)
        save(f"{OUTPUT_DIR}test_both.png")

    def test_serial_save(self) -> None:
        """Verify multiple saves consecutively maintain isolated drawing updates."""
        clear()
        circle((25, 25), radius=10)
        save(f"{OUTPUT_DIR}test_serial_save_1.png")
        circle((25, 75), radius=10)
        save(f"{OUTPUT_DIR}test_serial_save_2.png")
        circle((75, 25), radius=10)
        save(f"{OUTPUT_DIR}test_serial_save_3.png")
        circle((75, 75), radius=10)
        save(f"{OUTPUT_DIR}test_serial_save_4.png")

    def test_serial_save_grid(self) -> None:
        """Verify consecutive saves with a grid enabled work properly."""
        clear()
        config(grid=True)
        circle((25, 25), radius=10)
        save(f"{OUTPUT_DIR}test_serial_save_grid_1.png")
        circle((25, 75), radius=10)
        save(f"{OUTPUT_DIR}test_serial_save_grid_2.png")

    def test_serial_save_gridonly(self) -> None:
        """Verify consecutive saves with only a grid enabled work properly."""
        clear()
        config(grid_only=True)
        circle((25, 25), radius=10)
        save(f"{OUTPUT_DIR}test_serial_save_gridonly_1.png")
        circle((25, 75), radius=10)
        save(f"{OUTPUT_DIR}test_serial_save_gridonly_2.png")

    def test_get_save_file_path(self) -> None:
        """Verify the private save file path resolution helper."""
        path1 = canvas._get_save_file_path("output.png", None)
        assert path1.endswith("output.png")

        path2 = canvas._get_save_file_path(None, "png")
        assert path2.endswith("test_canvas.png")

    def test_set_background(self) -> None:
        """Verify internal set_background logic with background colors and overrides."""
        clear()
        config(background_color=Colors.Green, background_alpha=0.8)
        canvas._set_background()
        assert canvas._fig.patch.get_facecolor() is not None

    def test_show(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Verify show() invokes pyplot.show without errors using monkeypatch."""
        show_called = False

        def dummy_show() -> None:
            nonlocal show_called
            show_called = True

        monkeypatch.setattr(pyplot, "show", dummy_show)

        clear()
        circle((50, 50), 10)
        show()
        assert show_called

        # Also show with grid
        show_called = False
        clear()
        config(grid=True)
        circle((50, 50), 10)
        show()
        assert show_called

    def test_get_dimage(self) -> None:
        """Verify get_dimage renders canvas illustration to a Dimage object in memory."""
        clear()
        config(width=100, height=100)
        circle((50, 50), 30)

        dimg = get_dimage()
        assert isinstance(dimg, Dimage)
        width, height = dimg.get_image_size()
        assert width > 0
        assert height > 0

        # Verify canvas.get_dimage() method works identically
        dimg2 = canvas.get_dimage()
        assert isinstance(dimg2, Dimage)
        assert dimg2.get_image_size() == (width, height)

        # Verify the returned Dimage can be drawn on a subsequent canvas and captured
        clear()
        image((50, 50), width=40, image=dimg)
        dimg_composed = get_dimage()
        assert isinstance(dimg_composed, Dimage)
        assert dimg_composed.get_image_size() == (width, height)

    def test_get_dimage_with_grid(self) -> None:
        """Verify get_dimage includes grid overlay when grid is enabled."""
        clear()
        config(width=100, height=100, grid=True)
        circle((50, 50), 30)

        dimg = get_dimage()
        assert isinstance(dimg, Dimage)
        width, height = dimg.get_image_size()
        assert width > 0
        assert height > 0
