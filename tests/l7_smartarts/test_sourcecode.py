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

from drawlib.canvas import clear, save, setup
from drawlib.fonts import FontSourceCode
from drawlib.smartarts import (
    SourceCode,
    SourceCodeStyles,
    get_source_code_styles,
    sourcecode,
)
from drawlib.styles import Style

OUTPUT_DIR = "../../output_tests/l7_smartarts/sourcecode/"

code_snippet = """
import math

def example_function(x):
    return x * 2

print(example_function(5))

class Hello:
    ...
""".strip()

japanese_code = """
def greet(name: str) -> str:
    # ユーザーに対する挨拶メッセージを作成
    msg = f"こんにちは, {name}!"
    return msg

print(greet("世界"))
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

    def test_instantiation_raises(self) -> None:
        """Verify SourceCode cannot be instantiated directly."""
        with pytest.raises(TypeError, match="SourceCode cannot be instantiated directly"):
            SourceCode()

    def test_sourcecode_default(self) -> None:
        """Verify SourceCode rendering with default style and python syntax."""
        clear()
        setup(width=100, height=80)
        styles = SourceCodeStyles.get("default", font_lang="en")
        SourceCode.draw(
            xy=(10, 70),
            width=80,
            code=code_snippet,
            styles=styles,
            code_lang="python",
            show_linenum=True,
        )
        save(f"{OUTPUT_DIR}test_sourcecode_default.png")

    def test_sourcecode_themes(self) -> None:
        """Verify SourceCode rendering with different themes."""
        clear()
        setup(width=120, height=120)
        for x, y, theme in [
            (10, 110, "default"),
            (65, 110, "monochrome"),
            (10, 50, "dark"),
            (65, 50, "google"),
        ]:
            st = get_source_code_styles(theme, font_lang="en", text_size=10.0)
            SourceCode.draw(
                xy=(x, y),
                width=50,
                code=code_snippet,
                styles=st,
                code_lang="python",
                show_linenum=True,
            )
        save(f"{OUTPUT_DIR}test_sourcecode_themes.png")

    def test_sourcecode_japanese(self) -> None:
        """Verify SourceCode rendering with Japanese font_lang avoiding tofu."""
        clear()
        setup(width=100, height=70)
        styles = SourceCodeStyles.get("default", font_lang="ja", text_size=11.0)
        SourceCode.draw(
            xy=(10, 60),
            width=80,
            code=japanese_code,
            styles=styles,
            code_lang="python",
            show_linenum=True,
        )
        save(f"{OUTPUT_DIR}test_sourcecode_japanese.png")

    def test_sourcecode_patch(self) -> None:
        """Verify SourceCodeStyles patching capability."""
        clear()
        setup(width=100, height=70)
        base = SourceCodeStyles.get("default", font_lang="en")
        custom = base.patch(
            keyword=Style(text_color=(236, 72, 153), text_font=FontSourceCode.SOURCECODEPRO, text_size=11.0),
            box_style=Style(shape_fill_color=(240, 249, 255), shape_line_color=(2, 132, 199), shape_line_width=2.0),
            text_size=14.0,
        )
        assert custom.default.text_size == 14.0
        assert custom.linenum_style.text_size == 14.0
        assert custom.keyword.text_size == 14.0
        sourcecode(
            xy=(10, 60),
            width=80,
            code=code_snippet,
            styles=custom,
            code_lang="python",
            show_linenum=False,
        )
        save(f"{OUTPUT_DIR}test_sourcecode_patch.png")

    def test_sourcecode_get_text(self) -> None:
        """Verify static method get_text reads local files correctly relative to execution context."""
        text_content = SourceCode.get_text("__init__.py").strip()
        assert text_content == init_content
