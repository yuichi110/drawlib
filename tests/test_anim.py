# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Tests for drawlib.anim module supporting APNG and Animated WebP."""

from __future__ import annotations

import os
from pathlib import Path

import pytest
from PIL import Image

from drawlib.anim import Animation
from drawlib.canvas import canvas, clear, save, setup
from drawlib.shapes import circle, rectangle
from drawlib.styles import Styles


class TestAnimation:
    """Unit tests for Animation class and animation lifecycle."""

    def test_init_defaults(self) -> None:
        """Test Animation default initialization parameters and registration."""
        clear()
        anim = Animation()
        assert anim.fps == 10.0
        assert anim.frame_rate == 10.0
        assert anim._loop == 0
        assert canvas._active_animation is anim

    def test_init_custom_params(self) -> None:
        """Test Animation with custom fps, frame_rate, and loop count."""
        clear()
        anim1 = Animation(fps=5.0, loop=3)
        assert anim1.fps == 5.0
        assert anim1._default_duration_ms == 200

        anim2 = Animation(frame_rate=20.0)
        assert anim2.fps == 20.0
        assert anim2._default_duration_ms == 50

    def test_init_invalid_fps(self) -> None:
        """Test that non-positive fps raises ValueError."""
        clear()
        with pytest.raises(ValueError, match="FPS / frame_rate must be positive"):
            Animation(fps=0)
        with pytest.raises(ValueError, match="FPS / frame_rate must be positive"):
            Animation(frame_rate=-1)

    def test_context_manager_frames(self) -> None:
        """Test defining multiple frames via context manager."""
        clear()
        setup(width=100, height=50)
        anim = Animation(fps=10.0)  # 100ms default

        with anim.frame():
            circle((20, 25), radius=5, style=Styles.Primary)

        with anim.frame(duration=0.5):  # 500ms
            circle((50, 25), radius=5, style=Styles.Secondary)

        assert len(anim._frames) == 2
        assert anim._durations == [100, 500]

    def test_nested_frame_raises(self) -> None:
        """Test that nested with anim.frame() raises RuntimeError."""
        clear()
        anim = Animation()
        with pytest.raises(RuntimeError, match=r"Nested anim\.frame\(\) context is not allowed"):
            with anim.frame():
                with anim.frame():
                    pass

    def test_add_frame_imperative(self) -> None:
        """Test add_frame method for imperative frame definition."""
        clear()
        setup(width=100, height=50)
        anim = Animation(fps=4.0)  # 250ms default

        circle((20, 25), radius=5, style=Styles.Primary)
        anim.add_frame()

        circle((50, 25), radius=5, style=Styles.Primary)
        anim.add_frame(duration=1.0)  # 1000ms

        assert len(anim._frames) == 2
        assert anim._durations == [250, 1000]

    def test_accumulate_mode(self) -> None:
        """Test clear=False preserves existing canvas elements across frames."""
        clear()
        setup(width=100, height=50)
        anim = Animation()

        with anim.frame(clear=True):
            rectangle((10, 10), 10, 10, style=Styles.Primary)
        assert len(anim._frames) == 1

        with anim.frame(clear=False):
            rectangle((30, 10), 10, 10, style=Styles.Secondary)
            # Frame 2 contains both rectangles
            assert len(canvas._artists) == 2

        with anim.frame(clear=True):
            rectangle((50, 10), 10, 10, style=Styles.Accent)
            # Frame 3 was cleared on enter, contains only 1 rectangle
            assert len(canvas._artists) == 1

        assert len(anim._frames) == 3

    def test_save_apng(self, tmp_path: Path) -> None:
        """Test saving APNG animation via unified canvas.save()."""
        clear()
        setup(width=100, height=50)
        anim = Animation(fps=10.0, loop=0)

        for x in [20, 50, 80]:
            with anim.frame():
                circle((x, 25), radius=5, style=Styles.Primary)

        out_path = str(tmp_path / "test_anim.png")
        save(out_path)

        assert os.path.exists(out_path)
        assert canvas._active_animation is None

        with Image.open(out_path) as im:
            assert im.format == "PNG"
            assert getattr(im, "is_animated", False) is True
            assert getattr(im, "n_frames", 1) == 3

    def test_save_webp(self, tmp_path: Path) -> None:
        """Test saving Animated WebP via unified canvas.save()."""
        clear()
        setup(width=100, height=50)
        anim = Animation(fps=10.0, loop=0)

        for x in [20, 50, 80]:
            with anim.frame():
                circle((x, 25), radius=5, style=Styles.Primary)

        out_path = str(tmp_path / "test_anim.webp")
        save(out_path)

        assert os.path.exists(out_path)
        assert canvas._active_animation is None

        with Image.open(out_path) as im:
            assert im.format == "WEBP"
            assert getattr(im, "is_animated", False) is True
            assert getattr(im, "n_frames", 1) == 3

    def test_save_format_override(self, tmp_path: Path) -> None:
        """Test saving with explicit format override."""
        clear()
        setup(width=100, height=50)
        anim = Animation(fps=10.0)

        with anim.frame():
            circle((50, 25), radius=5, style=Styles.Primary)

        out_path = str(tmp_path / "output_no_ext")
        save(out_path, format="webp")

        with Image.open(out_path) as im:
            assert im.format == "WEBP"

    def test_save_without_frames_raises(self, tmp_path: Path) -> None:
        """Test that calling save() without any captured frames raises ValueError."""
        clear()
        _anim = Animation()
        out_path = str(tmp_path / "empty_anim.png")
        with pytest.raises(ValueError, match="Cannot save animation: No frames have been captured"):
            save(out_path)

    def test_save_unsupported_format_raises(self, tmp_path: Path) -> None:
        """Test that unsupported animation format raises ValueError."""
        clear()
        setup(width=100, height=50)
        anim = Animation()
        with anim.frame():
            circle((50, 25), radius=5, style=Styles.Primary)

        out_path = str(tmp_path / "test.jpg")
        with pytest.raises(ValueError, match="Unsupported animation format 'jpg'"):
            save(out_path)

    def test_clear_resets_active_animation(self) -> None:
        """Test that canvas.clear() resets _active_animation."""
        clear()
        _anim = Animation()
        assert canvas._active_animation is not None
        clear()
        assert canvas._active_animation is None
