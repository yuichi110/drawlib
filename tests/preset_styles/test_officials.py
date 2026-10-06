# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

import pytest

from drawlib._preset_styles import (
    BaseStyles,
    DefaultStyles,
    GoogleStyles,
    MonochromeStyles,
)
from drawlib.canvas import save
from drawlib.icons import phosphor
from drawlib.lines import line
from drawlib.shapes import circle
from drawlib.text import text

_ds_inst = DefaultStyles.get_default_instance()
assert isinstance(_ds_inst, DefaultStyles)
default_styles = _ds_inst

_gs_inst = GoogleStyles.get_default_instance()
assert isinstance(_gs_inst, GoogleStyles)
google_styles = _gs_inst

_ms_inst = MonochromeStyles.get_default_instance()
assert isinstance(_ms_inst, MonochromeStyles)
monochrome_styles = _ms_inst

IMAGE_FILE = "../assets/image.png"
OUTPUT_DIR_DEFAULT = "../../output_tests/preset_styles/default/"
OUTPUT_DIR_MONOCHROME = "../../output_tests/preset_styles/monochrome/"


def test_official_preset_style_generators() -> None:
    """Verifies that all official preset style singletons are valid BaseStyles instances."""
    assert isinstance(default_styles, DefaultStyles)
    assert isinstance(default_styles, BaseStyles)

    assert isinstance(monochrome_styles, MonochromeStyles)
    assert isinstance(monochrome_styles, BaseStyles)

    assert isinstance(google_styles, GoogleStyles)
    assert isinstance(google_styles, BaseStyles)


def test_default_fill_official() -> None:
    """Integrated drawing test for default circle filling styles."""
    styles = default_styles
    circle((25, 25), 10, style=styles.PrimaryFlat, text="drawlib")
    circle((25, 50), 10, style=styles.Primary, text="drawlib")
    circle((25, 75), 10, style=styles.PrimaryThin, text="drawlib")
    circle((75, 25), 10, style=styles.PrimaryBold, text="drawlib")
    save(f"{OUTPUT_DIR_DEFAULT}test_fill_official.png")


@pytest.mark.image_threshold(95.0)
def test_monochrome_icon_text_thinbold() -> None:
    """Integrated drawing test for monochrome icons and text."""
    styles = monochrome_styles
    x1 = 20
    x2 = 50
    x3 = 80
    y1 = 20
    y2 = 50
    y3 = 80

    phosphor.airplane((x1, y1), width=20, style=styles.PrimaryThin)
    phosphor.airplane((x2, y1), width=20, style=styles.Primary)
    phosphor.airplane((x3, y1), width=20, style=styles.PrimaryBold)

    text((x1, y2), "Hello Drawlib1", style=styles.PrimaryThin)
    text((x2, y2), "Hello Drawlib1", style=styles.Primary)
    text((x3, y2), "Hello Drawlib1", style=styles.PrimaryBold)

    with pytest.raises(ValueError, match="Style cannot be used for icons"):
        phosphor.airplane((x2, y3), width=20, style=styles.PrimarySolid)
    with pytest.raises(ValueError, match="Style cannot be used for icons"):
        phosphor.airplane((x3, y3), width=20, style=styles.PrimaryDashed)

    save(f"{OUTPUT_DIR_MONOCHROME}test_icon_text_thinbold.png")


@pytest.mark.image_threshold(98.0)
def test_monochrome_shape_thinbold() -> None:
    """Integrated drawing test for monochrome circles with text."""
    styles = monochrome_styles
    x1 = 20
    x2 = 50
    x3 = 80
    y1 = 20
    y2 = 50
    radius = 10

    circle((x1, y1), radius, style=styles.PrimaryThin, text="drawlib")
    circle((x2, y1), radius, style=styles.Primary, text="drawlib")
    circle((x3, y1), radius, style=styles.PrimaryBold, text="drawlib")

    circle((x1, y2), radius, style=styles.PrimarySolid, text="drawlib")
    circle((x2, y2), radius, style=styles.PrimaryFlat, text="drawlib")
    circle((x3, y2), radius, style=styles.PrimaryDashed, text="drawlib")

    save(f"{OUTPUT_DIR_MONOCHROME}test_shape_thinbold.png")


def test_monochrome_line_thinbold() -> None:
    """Integrated drawing test for monochrome line styles."""
    styles = monochrome_styles
    x1 = 20
    x2 = 50
    x3 = 80
    y1 = 20
    y2 = 50

    line((x1 - 5, y1), (x1 + 5, y1), style=styles.PrimaryThin)
    line((x2 - 5, y1), (x2 + 5, y1), style=styles.Primary)
    line((x3 - 5, y1), (x3 + 5, y1), style=styles.PrimaryBold)

    line((x1 - 5, y2), (x1 + 5, y2), style=styles.PrimarySolid)
    with pytest.raises(ValueError, match="Style cannot be used for line"):
        line((x2 - 5, y2), (x2 + 5, y2), style=styles.PrimaryFlat)
    line((x3 - 5, y2), (x3 + 5, y2), style=styles.PrimaryDashed)

    save(f"{OUTPUT_DIR_MONOCHROME}test_line_thinbold.png")
