# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Unit tests for TypeFont in _font.py."""

from unittest.mock import patch

from pydantic import TypeAdapter

from drawlib._core.l2_models_._font import FontBase, FontFile
from drawlib._core.l2_types_._font import TypeFont


class TestFontType:
    """Test cases for TypeFont."""

    def test_type_font_validation(self):
        """Test TypeFont validation using TypeAdapter."""
        adapter: TypeAdapter[TypeFont] = TypeAdapter(TypeFont)

        # Validate FontBase enum member
        class DummyFont(FontBase):
            ROBOTO = "roboto"

        assert adapter.validate_python(DummyFont.ROBOTO) == DummyFont.ROBOTO

        # Validate FontFile instance
        with (
            patch("drawlib._core.l2_models_._font.get_script_relative_path", return_value="/dummy/font.ttf"),
            patch("os.path.exists", return_value=True),
        ):
            font_file = FontFile("dummy/font.ttf")
            validated = adapter.validate_python(font_file)
            assert validated == font_file
            assert isinstance(validated, FontFile)
            assert validated.file == "/dummy/font.ttf"
