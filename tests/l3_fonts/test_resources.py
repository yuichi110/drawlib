# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Unit tests for the font resource definitions in l3_fonts."""

from drawlib._core.l2_models import FontBase, FontResource
from drawlib._core.l3_fonts._names import (
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
from drawlib._core.l3_fonts._resources import FONT_RESOURCES


class TestFontResources:
    """Test cases for FONT_RESOURCES dictionary mapping."""

    def test_font_resources_keys_exist_in_enums(self):
        """Test all keys in FONT_RESOURCES are instances of FontBase."""
        for key in FONT_RESOURCES.keys():
            assert isinstance(key, FontBase)

    def test_font_resources_values_are_valid(self):
        """Test all values in FONT_RESOURCES are valid FontResource instances."""
        for value in FONT_RESOURCES.values():
            assert isinstance(value, FontResource)
            assert isinstance(value.path, str)
            assert len(value.path) > 0
            assert isinstance(value.md5, str)
            assert len(value.md5) == 32  # MD5 hex length is 32

    def test_all_public_enum_members_have_resource(self):
        """Test every single defined font enum member has a registered resource mapping."""
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
            for member in enum_cls:
                assert member in FONT_RESOURCES
