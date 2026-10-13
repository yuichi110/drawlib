# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

import pytest

from drawlib._core.l3_colors import (
    Color,
    ColorUtils,
    get_intermediate_color,
    get_intermediate_colors,
)
from drawlib.styles import (
    get_intermediate_color as styles_get_intermediate_color,
)
from drawlib.styles import (
    get_intermediate_colors as styles_get_intermediate_colors,
)


class TestColorUtils:
    """Unit tests for the ColorUtils static helper class."""

    def test_get_mplot_rgba(self) -> None:
        """Verifies get_mplot_rgba converts 0~255 RGB/RGBA to 0.0~1.0 RGBA with correct alpha handling."""
        # 1. RGB conversion (default alpha 1.0)
        assert ColorUtils.get_mplot_rgba((255, 127, 0)) == (1.0, 0.49804, 0.0, 1.0)

        # 2. RGBA conversion (preserving original alpha)
        assert ColorUtils.get_mplot_rgba((0, 255, 127, 0.5)) == (0.0, 1.0, 0.49804, 0.5)

        # 3. Alpha override
        assert ColorUtils.get_mplot_rgba((255, 127, 0), alpha=0.75) == (1.0, 0.49804, 0.0, 0.75)
        assert ColorUtils.get_mplot_rgba((0, 255, 127, 0.5), alpha=0.8) == (0.0, 1.0, 0.49804, 0.8)

    def test_get_hexrgb(self) -> None:
        """Verifies get_hexrgb converts RGB/RGBA to 6-digit hex format and enforces boundaries."""
        # Valid RGB conversion
        assert ColorUtils.get_hexrgb((255, 127, 0)) == "#ff7f00"
        assert ColorUtils.get_hexrgb((0, 0, 0)) == "#000000"

        # Boundary checks: RGB out of 0~255 range
        with pytest.raises(ValueError):
            ColorUtils.get_hexrgb((256, 127, 0))

        with pytest.raises(ValueError):
            ColorUtils.get_hexrgb((-1, 127, 0))

        with pytest.raises(ValueError):
            ColorUtils.get_hexrgb((255, 255, 300))

    def test_get_rgba_from_hex(self) -> None:
        """Verifies get_rgba_from_hex parses various hex formats.

        Parses short, long, and alpha formats, and raises ValueError on invalid formats.
        """
        # 1. Short format (#RGB)
        assert ColorUtils.get_rgba_from_hex("#f80") == (255, 136, 0, 1.0)
        assert ColorUtils.get_rgba_from_hex("f80") == (255, 136, 0, 1.0)

        # 2. Full format (#RRGGBB)
        assert ColorUtils.get_rgba_from_hex("#ff7f00") == (255, 127, 0, 1.0)
        assert ColorUtils.get_rgba_from_hex("00ff7f") == (0, 255, 127, 1.0)

        # 3. Full format with alpha (#RRGGBBAA)
        assert ColorUtils.get_rgba_from_hex("#ff7f0080") == (255, 127, 0, 128.0)

        # 4. Invalid formats
        with pytest.raises(ValueError):
            ColorUtils.get_rgba_from_hex("#ff")

        with pytest.raises(ValueError):
            ColorUtils.get_rgba_from_hex("#ff7f00aa11")

    def test_instantiation_raises_type_error(self) -> None:
        """Verifies that instantiating ColorUtils directly raises a TypeError."""
        with pytest.raises(TypeError):
            ColorUtils()

    def test_get_intermediate_color(self) -> None:
        """Verifies get_intermediate_color returns the exact 50% midpoint Color."""
        mid = get_intermediate_color(Color(0, 100, 200), Color(100, 200, 0))
        assert isinstance(mid, Color)
        assert mid == Color(50, 150, 100)

        # Accepts hex strings and tuples as well
        mid2 = styles_get_intermediate_color("#000000", (200, 100, 50, 0.5))
        assert mid2 == Color(100, 50, 25, alpha=0.75)

    def test_get_intermediate_colors(self) -> None:
        """Verifies get_intermediate_colors generates evenly spaced colors with or without ends."""
        c1 = Color(0, 0, 0, alpha=0.0)
        c2 = Color(100, 200, 40, alpha=1.0)

        mids = get_intermediate_colors(c1, c2, num=3)
        assert len(mids) == 3
        assert mids[0] == Color(25, 50, 10, alpha=0.25)
        assert mids[1] == Color(50, 100, 20, alpha=0.5)
        assert mids[2] == Color(75, 150, 30, alpha=0.75)

        with_ends = styles_get_intermediate_colors(c1, c2, num=3, include_ends=True)
        assert len(with_ends) == 5
        assert with_ends[0] == c1
        assert with_ends[1:4] == mids
        assert with_ends[4] == c2

        with pytest.raises(ValueError, match="num must be >= 1"):
            get_intermediate_colors(c1, c2, num=0)

    def test_luminance_black_and_white(self) -> None:
        """Verifies get_luminance calculates WCAG relative luminance for white and black."""
        lum_white = ColorUtils.get_luminance((255, 255, 255))
        assert pytest.approx(lum_white, abs=1e-3) == 1.0

        lum_black = ColorUtils.get_luminance((0, 0, 0))
        assert pytest.approx(lum_black, abs=1e-3) == 0.0

    def test_contrast_text_transparent_background(self) -> None:
        """Verifies get_contrast_text_color falls back to dark text on transparent backgrounds."""
        assert ColorUtils.get_contrast_text_color(None) == (40, 40, 40, 1.0)
        assert ColorUtils.get_contrast_text_color((255, 255, 255, 0.0)) == (40, 40, 40, 1.0)
        assert ColorUtils.get_contrast_text_color((255, 255, 255, 0.1)) == (40, 40, 40, 1.0)

    def test_contrast_text_bright_and_dark_backgrounds(self) -> None:
        """Verifies get_contrast_text_color selects dark or light text based on background luminance."""
        assert ColorUtils.get_contrast_text_color((255, 255, 255)) == (40, 40, 40, 1.0)
        assert ColorUtils.get_contrast_text_color((0, 0, 0)) == (255, 255, 255, 1.0)
        assert ColorUtils.get_contrast_text_color((20, 30, 80)) == (255, 255, 255, 1.0)
        assert ColorUtils.get_contrast_text_color((255, 255, 0)) == (40, 40, 40, 1.0)

    def test_contrast_text_custom_colors_and_threshold(self) -> None:
        """Verifies get_contrast_text_color respects custom dark_color and light_color."""
        res = ColorUtils.get_contrast_text_color(
            (0, 0, 0),
            dark_color=(10, 10, 10, 1.0),
            light_color=(240, 240, 240, 1.0),
        )
        assert res == (240, 240, 240, 1.0)
