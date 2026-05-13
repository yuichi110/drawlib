# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

import json

import pytest
from pydantic import BaseModel

from drawlib.v0_2.private.core.fonts import get_font_metadata
from drawlib.v0_2.private.core.fonts_enum import Font
from drawlib.v0_2.private.core.fonts_resource import FONT_RESOURCES


class MyModel(BaseModel):
    """Temporary model for testing font serialization."""

    font: Font


def test_font_serialization():
    # 1. Test value is a simple string key
    assert isinstance(Font.SANSSERIF_LIGHT.value, str)
    assert Font.SANSSERIF_LIGHT.value == "Font.SANSSERIF_LIGHT"

    # 2. Test serialization to JSON (should be the string key)
    m = MyModel(font=Font.SANSSERIF_LIGHT)
    dumped = m.model_dump(mode='json')
    print(f"JSON Dump: {dumped}")
    assert dumped == {"font": "Font.SANSSERIF_LIGHT"}

    # 3. Test deserialization back to Enum
    loaded = MyModel.model_validate(dumped)
    assert loaded.font == Font.SANSSERIF_LIGHT

    # 4. Test metadata resolution
    meta = get_font_metadata(loaded.font)
    print(f"Metadata: {meta}")
    assert meta.path == "cjk_japanese_noto_sans/light.otf"
    assert meta.abs_path.endswith("light.otf")
    assert meta.url.startswith("https://")
    assert meta.md5 == "88ce9ab7e76fed605c822b52605ac2fd"


if __name__ == "__main__":
    test_font_serialization()
    print("\nSerialization tests passed!")
