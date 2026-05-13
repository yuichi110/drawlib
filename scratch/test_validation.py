from drawlib.apis import *
from drawlib.v0_2.private.core.theme_style_caches import ThemeColorCache
import pytest

def test_invalid_color():
    cache = ThemeColorCache()
    # This should raise ValueError because of @guarded + Pydantic validation of TypeColor
    try:
        cache.set(color=(300, 300, 300), name="invalid")
        print("Failed: Should have raised ValueError")
    except SystemExit:
        print("Success: Caught SystemExit (raised by guarded after ValueError)")
    except Exception as e:
        print(f"Caught unexpected exception: {type(e).__name__}: {e}")

if __name__ == "__main__":
    test_invalid_color()
