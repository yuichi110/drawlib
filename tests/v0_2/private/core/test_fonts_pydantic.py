import json
from pydantic import BaseModel
from drawlib.v0_2.private.core.fonts import get_font_metadata
from drawlib.v0_2.private.core.fonts_enum import Font
from drawlib.v0_2.private.core.fonts_resource import FONT_RESOURCES
import pytest

class MyModel(BaseModel):
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
