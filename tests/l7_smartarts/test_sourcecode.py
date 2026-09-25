# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Unit and integration tests for SourceCode smart art rendering."""

import pytest

from drawlib.canvas import clear, save
from drawlib.fonts import FontSourceCode
from drawlib.smartarts import SourceCode

OUTPUT_DIR = "../../output_tests/l7_smartarts/sourcecode/"

code_snippet = """
import math

def example_function(x):
    return x * 2

print(example_function(5))

class Hello:
    ...
""".strip()

init_content = """
# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.
""".strip()


class TestSourceCode:
    """Tests for the SourceCode class drawing and syntax highlighting operations."""

    def test_sourcecode_default(self) -> None:
        """Verify SourceCode rendering with default style and python syntax."""
        clear()
        sc = SourceCode(
            language="python",
            style="default",
        )
        sc.draw(xy=(20, 20), width=30, code=code_snippet)
        save(f"{OUTPUT_DIR}test_sourcecode_default.png")

    @pytest.mark.image_threshold(97.0)
    def test_sourcecode_styles(self) -> None:
        """Verify SourceCode rendering with different Pygments themes and Roboto Mono font."""
        clear()
        for x, y, style in [
            (5, 5, "bw"),
            (5, 35, "sas"),
            (5, 60, "staroffice"),
            (40, 5, "xcode"),
            (40, 35, "default"),
            (40, 60, "monokai"),
            (70, 5, "lightbulb"),
            (70, 35, "github-dark"),
            (70, 60, "rrt"),
        ]:
            sc = SourceCode(
                language="python",
                style=style,  # type: ignore
                font=FontSourceCode.ROBOTO_MONO,
            )
            sc.draw(xy=(x, y), width=25, code=code_snippet)
        save(f"{OUTPUT_DIR}test_sourcecode_styles.png")

    def test_sourcecode_grayscale_styles(self) -> None:
        """Verify SourceCode rendering with grayscale Pygments themes."""
        clear()
        for x, y, style in [
            (5, 5, "algol"),
            (5, 35, "algol_nu"),
            (5, 65, "friendly_grayscale"),
        ]:
            sc = SourceCode(
                language="python",
                style=style,  # type: ignore
                font=FontSourceCode.ROBOTO_MONO,
            )
            sc.draw(xy=(x, y), width=25, code=code_snippet)
        save(f"{OUTPUT_DIR}test_sourcecode_grayscale_styles.png")

    @pytest.mark.image_threshold(97.0)
    def test_sourcecode_font_courier(self) -> None:
        """Verify SourceCode rendering with Courier font style."""
        clear()
        for x, y, style in [
            (5, 5, "bw"),
            (5, 35, "sas"),
            (5, 60, "staroffice"),
            (40, 5, "xcode"),
            (40, 35, "default"),
            (40, 60, "monokai"),
            (70, 5, "lightbulb"),
            (70, 35, "github-dark"),
            (70, 60, "rrt"),
        ]:
            sc = SourceCode(
                language="python",
                style=style,  # type: ignore
                font=FontSourceCode.COURIER,
            )
            sc.draw(xy=(x, y), width=25, code=code_snippet)
        save(f"{OUTPUT_DIR}test_sourcecode_courier.png")

    def test_sourcecode_get_text(self) -> None:
        """Verify static method get_text reads local files correctly relative to execution context."""
        text = SourceCode.get_text("__init__.py").strip()
        assert text == init_content
