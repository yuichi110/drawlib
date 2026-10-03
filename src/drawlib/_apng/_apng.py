# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Animated PNG (APNG) animation generator implementation module."""

from __future__ import annotations

import os
from collections.abc import Generator
from contextlib import contextmanager

from PIL import Image
from pydantic import validate_call

from drawlib._core.l2_types import PosInt
from drawlib._core.l4_canvas import canvas


class Apng:
    """Animated PNG (APNG) animation generator for drawlib.

    This class manages animation frames and coordinates with drawlib canvas
    to output animated PNG files.
    """

    @validate_call
    def __init__(
        self,
        fps: float | None = None,
        frame_rate: float | None = None,
        loop: PosInt = 0,
    ) -> None:
        """Initialize an Apng animation instance.

        Args:
            fps: Playback frame rate in frames per second (e.g. 10.0 means 10 fps). Defaults to 10.0.
            frame_rate: Alias for `fps`. If both are specified, `fps` takes precedence.
            loop: Number of playback loops. 0 means infinite loop. Defaults to 0.

        Raises:
            ValueError: If fps or frame_rate is non-positive.
        """
        eff_fps = fps if fps is not None else (frame_rate if frame_rate is not None else 10.0)
        if eff_fps <= 0:
            raise ValueError(f"FPS / frame_rate must be positive, got {eff_fps}.")

        self._fps: float = float(eff_fps)
        self._default_duration_ms: int = max(1, round(1000.0 / self._fps))
        self._loop: int = loop
        self._frames: list[Image.Image] = []
        self._durations: list[int] = []
        self._in_frame_context: bool = False
        canvas._active_animation = self

    @property
    def fps(self) -> float:
        """Get the animation frame rate in frames per second."""
        return self._fps

    @property
    def frame_rate(self) -> float:
        """Get the animation frame rate in frames per second (alias for fps)."""
        return self._fps

    @contextmanager
    def frame(
        self,
        duration: float | None = None,
        clear: bool = True,
    ) -> Generator[None, None, None]:
        """Context manager to define and capture a single animation frame.

        Args:
            duration: Display duration for this specific frame in seconds.
                If None, uses 1 / fps.
            clear: Whether to clear existing canvas shapes before drawing this frame.
                Defaults to True. If False, keeps existing shapes from the previous frame
                (cumulative / step-by-step mode).

        Yields:
            None

        Raises:
            RuntimeError: If nested inside another `with anim.frame()` block.
            ValueError: If duration is non-positive.
        """
        if self._in_frame_context:
            raise RuntimeError("Nested anim.frame() context is not allowed.")
        if duration is not None and duration <= 0:
            raise ValueError(f"Frame duration must be positive, got {duration}.")

        self._in_frame_context = True
        if clear:
            canvas._clear_artists()

        try:
            yield
        finally:
            self._in_frame_context = False
            dimage = canvas.get_dimage()
            self._frames.append(dimage.get_pil_image())
            eff_duration_ms = (
                max(1, round(duration * 1000.0))
                if duration is not None
                else self._default_duration_ms
            )
            self._durations.append(eff_duration_ms)

    @validate_call
    def add_frame(
        self,
        duration: float | None = None,
        clear: bool = True,
    ) -> None:
        """Capture the current canvas state as an animation frame.

        Args:
            duration: Display duration for this frame in seconds.
                If None, uses 1 / fps.
            clear: Whether to clear canvas shapes after capturing this frame.
                Defaults to True.

        Raises:
            ValueError: If duration is non-positive.
        """
        if duration is not None and duration <= 0:
            raise ValueError(f"Frame duration must be positive, got {duration}.")

        dimage = canvas.get_dimage()
        self._frames.append(dimage.get_pil_image())
        eff_duration_ms = (
            max(1, round(duration * 1000.0))
            if duration is not None
            else self._default_duration_ms
        )
        self._durations.append(eff_duration_ms)
        if clear:
            canvas._clear_artists()

    def _save(self, file_path: str) -> None:
        """Internal save method called by canvas.save().

        Args:
            file_path: Destination file path.

        Raises:
            ValueError: If no frames have been captured.
        """
        if not self._frames:
            raise ValueError(
                "Cannot save APNG: No frames have been captured. Use 'with anim.frame():' or 'anim.add_frame()'."
            )

        directory = os.path.dirname(file_path)
        if directory:
            os.makedirs(directory, exist_ok=True)

        first_frame = self._frames[0]
        append_frames = self._frames[1:]
        first_frame.save(
            file_path,
            save_all=True,
            append_images=append_frames,
            duration=self._durations,
            loop=self._loop,
            format="PNG",
            compress_level=9,
            optimize=True,
        )
