# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

import pytest

from drawlib._core.l4_canvas_utils._colors import ColorUtil


class TestColorUtil:
    """Unit tests for the ColorUtil static helper class."""

    def test_get_mplot_rgba(self) -> None:
        """Verifies get_mplot_rgba converts 0~255 RGB/RGBA to 0.0~1.0 RGBA with correct alpha handling."""
        # 1. RGB conversion (default alpha 1.0)
        assert ColorUtil.get_mplot_rgba((255, 127, 0)) == (1.0, 0.49804, 0.0, 1.0)

        # 2. RGBA conversion (preserving original alpha)
        assert ColorUtil.get_mplot_rgba((0, 255, 127, 0.5)) == (0.0, 1.0, 0.49804, 0.5)

        # 3. Alpha override
        assert ColorUtil.get_mplot_rgba((255, 127, 0), alpha=0.75) == (1.0, 0.49804, 0.0, 0.75)
        assert ColorUtil.get_mplot_rgba((0, 255, 127, 0.5), alpha=0.8) == (0.0, 1.0, 0.49804, 0.8)

    def test_get_hexrgb(self) -> None:
        """Verifies get_hexrgb converts RGB/RGBA to 6-digit hex format and enforces boundaries."""
        # Valid RGB conversion
        assert ColorUtil.get_hexrgb((255, 127, 0)) == "#ff7f00"
        assert ColorUtil.get_hexrgb((0, 0, 0)) == "#000000"

        # Boundary checks: RGB out of 0~255 range
        with pytest.raises(ValueError):
            ColorUtil.get_hexrgb((256, 127, 0))

        with pytest.raises(ValueError):
            ColorUtil.get_hexrgb((-1, 127, 0))

        with pytest.raises(ValueError):
            ColorUtil.get_hexrgb((255, 255, 300))

    def test_get_rgba_from_hex(self) -> None:
        """Verifies get_rgba_from_hex parses various hex formats.

        Parses short, long, and alpha formats, and raises ValueError on invalid formats.
        """
        # 1. Short format (#RGB)
        assert ColorUtil.get_rgba_from_hex("#f80") == (255, 136, 0, 1.0)
        assert ColorUtil.get_rgba_from_hex("f80") == (255, 136, 0, 1.0)

        # 2. Full format (#RRGGBB)
        assert ColorUtil.get_rgba_from_hex("#ff7f00") == (255, 127, 0, 1.0)
        assert ColorUtil.get_rgba_from_hex("00ff7f") == (0, 255, 127, 1.0)

        # 3. Full format with alpha (#RRGGBBAA)
        assert ColorUtil.get_rgba_from_hex("#ff7f0080") == (255, 127, 0, 128.0)

        # 4. Invalid formats
        with pytest.raises(ValueError):
            ColorUtil.get_rgba_from_hex("#ff")

        with pytest.raises(ValueError):
            ColorUtil.get_rgba_from_hex("#ff7f00aa11")
