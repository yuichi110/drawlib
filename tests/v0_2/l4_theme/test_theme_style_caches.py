# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

import pytest

from drawlib.v0_2.private.l3_fonts import FontSourceCode
from drawlib.v0_2.private.l3_styles import (
    IconStyle,
    ImageStyle,
    LineStyle,
    ShapeStyle,
    ShapeTextStyle,
    TextStyle,
)
from drawlib.v0_2.private.l4_theme._theme_style_caches import (
    AbstractStyleCache,
    BackgroundColorCache,
    CircleStyleCache,
    IconStyleCache,
    ImageStyleCache,
    LineStyleCache,
    ShapeStyleCache,
    ShapeTextStyleCache,
    SourceCodeFontCache,
    TextStyleCache,
    ThemeColorCache,
)


class TestBasicCaches:
    """Unit tests for basic theme cache classes: ThemeColorCache, BackgroundColorCache, SourceCodeFontCache."""

    def test_theme_color_cache(self) -> None:
        """Verifies ThemeColorCache set, get, has, list, delete and promotion of RGB to RGBA."""
        cache = ThemeColorCache()
        assert not cache.has("red")

        # Test set and promote 3-tuple RGB to 4-tuple RGBA
        cache.set((255, 0, 0), "red")
        assert cache.has("red")
        assert cache.get("red") == (255, 0, 0, 1.0)

        # Test RGBA preservation
        cache.set((0, 255, 0, 0.5), "green")
        assert cache.get("green") == (0, 255, 0, 0.5)

        assert sorted(cache.list()) == ["green", "red"]

        # Test delete
        cache.delete("red")
        assert not cache.has("red")

        with pytest.raises(ValueError):
            cache.get("red")

        with pytest.raises(ValueError):
            cache.delete("red")

    def test_background_color_cache(self) -> None:
        """Verifies BackgroundColorCache set, get, has, list, delete and promotion of RGB to RGBA."""
        cache = BackgroundColorCache()
        assert not cache.has("bg")

        cache.set((255, 255, 255), "bg")
        assert cache.has("bg")
        assert cache.get("bg") == (255, 255, 255, 1.0)

        cache.delete("bg")
        assert not cache.has("bg")

        with pytest.raises(ValueError):
            cache.get("bg")

    def test_source_code_font_cache(self) -> None:
        """Verifies SourceCodeFontCache set, get, has, list, delete and type validation."""
        cache = SourceCodeFontCache()
        assert not cache.has("font")

        font = FontSourceCode.ROBOTO_MONO
        cache.set(font, "font")
        assert cache.has("font")
        assert cache.get("font") == font

        assert cache.list() == ["font"]

        # Invalid type should raise ValueError
        with pytest.raises(ValueError):
            cache.set("invalid_font", "font")  # type: ignore

        cache.delete("font")
        assert not cache.has("font")


class TestAbstractStyleCache:
    """Unit tests for the AbstractStyleCache interface."""

    def test_cannot_instantiate_abstract(self) -> None:
        """Verifies that AbstractStyleCache cannot be instantiated directly."""
        with pytest.raises(TypeError):
            AbstractStyleCache()


class TestStyleCaches:
    """Unit tests for concrete style caches (Icon, Image, Line, Shape, ShapeText, TextStyle)."""

    def test_concrete_caches(self) -> None:
        """Verifies standard styling caches and callback execution flow."""
        set_calls: list[str] = []
        delete_calls: list[str] = []

        def callback_set(name: str) -> None:
            set_calls.append(name)

        def callback_delete(name: str) -> None:
            delete_calls.append(name)

        # IconStyleCache
        icon_cache = IconStyleCache(callback_set, callback_delete)
        style = IconStyle(style="fill")
        icon_cache.set(style, "test")
        assert icon_cache.has("test")
        assert icon_cache.get("test").style == "fill"
        assert set_calls == ["test"]

        # Copy check (must be a deep copy/different instance)
        assert icon_cache.get("test") is not style

        # delete
        icon_cache.delete("test")
        assert not icon_cache.has("test")
        assert delete_calls == ["test"]

        with pytest.raises(ValueError):
            icon_cache.get("test")

        # Merge
        icon_cache.set(IconStyle(style="fill", color=(255, 0, 0, 1.0)), "red")
        icon_cache.merge(IconStyle(color=(0, 0, 255, 1.0)), targets=["red"])
        assert icon_cache.get("red").color == (0, 0, 255, 1.0)


class TestGeometricCaches:
    """Unit tests for specialized geometric caches with fallback mechanisms."""

    def test_geometric_fallback(self) -> None:
        """Verifies that geometric caches fallback to shapestyles or raise ValueError correctly."""
        set_calls: list[str] = []
        delete_calls: list[str] = []

        def dummy_callback(name: str) -> None:
            pass

        def set_callback(name: str) -> None:
            set_calls.append(name)

        def delete_callback(name: str) -> None:
            delete_calls.append(name)

        # Setup base ShapeStyleCache
        base_shape_cache = ShapeStyleCache(dummy_callback, dummy_callback)
        base_shape_cache.set(ShapeStyle(lwidth=5.0, lcolor=(255, 0, 0, 1.0)), "red_shape")

        # Setup specialized CircleStyleCache
        circle_cache = CircleStyleCache(
            shapestyles=base_shape_cache,
            callback_set=set_callback,
            callback_delete=delete_callback,
        )

        # Get style registered directly in circle_cache
        circle_style = ShapeStyle(lwidth=10.0)
        circle_cache.set(circle_style, "custom_circle")
        assert circle_cache.has("custom_circle")
        assert circle_cache.get("custom_circle").lwidth == 10.0

        # Get fallback style from shapestyles when use_shapestyles_if_not_exist is True
        assert not circle_cache.has("red_shape")
        fallback_style = circle_cache.get("red_shape", use_shapestyles_if_not_exist=True)
        assert fallback_style.lwidth == 5.0
        assert fallback_style.lcolor == (255, 0, 0, 1.0)

        # Expect ValueError when use_shapestyles_if_not_exist is False and style name is not registered
        with pytest.raises(ValueError):
            circle_cache.get("red_shape", use_shapestyles_if_not_exist=False)
