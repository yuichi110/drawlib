# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Unit tests for the font name enums in l3_fonts."""

from pydantic import BaseModel

from drawlib.v0_2.private.l2_models import FontBase
from drawlib.v0_2.private.l3_fonts._names import (
    Font,
    FontArabic,
    FontBrahmic,
    FontChinese,
    FontJapanese,
    FontKorean,
    FontMonoSpace,
    FontRoboto,
    FontSansSerif,
    FontSerif,
    FontSourceCode,
    FontThai,
)


class TestFontNames:
    """Test cases for FontBase enums and their properties."""

    def test_font_enums_subclass_font_base(self):
        """Test all defined font enums are subclasses of FontBase."""
        enums: list[type[FontBase]] = [
            Font,
            FontSansSerif,
            FontSerif,
            FontMonoSpace,
            FontRoboto,
            FontSourceCode,
            FontArabic,
            FontBrahmic,
            FontChinese,
            FontJapanese,
            FontKorean,
            FontThai,
        ]
        for enum_cls in enums:
            assert issubclass(enum_cls, FontBase)

    def test_font_enum_member_values(self):
        """Test standard enum values are strings matching their class and name."""
        assert Font.SANSSERIF_LIGHT.value == "Font.SANSSERIF_LIGHT"
        assert FontJapanese.SANSSERIF_LIGHT.value == "FontJapanese.SANSSERIF_LIGHT"

    def test_font_pydantic_serialization(self):
        """Test font enum Pydantic serialization and deserialization."""

        class MyModel(BaseModel):
            font: Font

        m = MyModel(font=Font.SANSSERIF_LIGHT)
        dumped = m.model_dump(mode="json")
        assert dumped == {"font": "Font.SANSSERIF_LIGHT"}

        loaded = MyModel.model_validate(dumped)
        assert loaded.font == Font.SANSSERIF_LIGHT
