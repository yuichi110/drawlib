# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Base model for preset styles."""

from __future__ import annotations

from typing import Any, Generator, Self

from pydantic import BaseModel, ConfigDict, validate_call

from drawlib._core.l2_types import FontBase, FontFile
from drawlib._core.l3_colors import Color, ColorType
from drawlib._core.l3_fonts import FontSourceCode
from drawlib._core.l3_styles._style_models import Style


def _resolve_target_font(
    field_name: str,
    regular: FontBase | FontFile | None,
    bold: FontBase | FontFile | None,
    light: FontBase | FontFile | None,
) -> FontBase | FontFile | None:
    """Resolve target font for a specific style field based on naming convention.

    Args:
        field_name (str): Style attribute name.
        regular (FontBase | FontFile | None): Base font.
        bold (FontBase | FontFile | None): Bold font.
        light (FontBase | FontFile | None): Light font.

    Returns:
        FontBase | FontFile | None: Target font to apply.
    """
    if field_name == "Bold" or field_name.endswith("Bold"):
        return bold if bold is not None else regular
    if field_name.endswith("Light"):
        return light if light is not None else regular
    return regular


def _resolve_style_field_name(cls: type[BaseStyles], name: str, value: Any = None) -> str:  # noqa: ANN401
    """Resolve style field name matching model attributes regardless of casing or aliases.

    Args:
        cls (type[BaseStyles]): Preset style class.
        name (str): Style or attribute name.
        value (Any): Optional value to distinguish style vs color for aliases like 'canvas'.

    Returns:
        str: Resolved field name matching cls.model_fields if found, else original name.
    """
    lower = name.lower()
    if lower in {"bg_color", "background", "background_color", "backgroundcolor"}:
        return "background_color"
    if lower in {"width", "height", "dpi", "sourcecode_font", "colors"}:
        return lower
    fields = getattr(cls, "model_fields", {})
    if name in fields:
        return name
    return name


class _BaseStylesMeta(type(BaseModel)):
    """Metaclass allowing class-level attribute access for preset styles."""

    _default_instances: dict[type, BaseStyles] = {}

    def register_default_instance(cls, instance: BaseStyles) -> None:
        """Register the default singleton instance for this style class.

        Args:
            instance (BaseStyles): Default preset style instance.
        """
        _BaseStylesMeta._default_instances[cls] = instance

    def get_default_instance(cls) -> BaseStyles | None:
        """Get the registered default instance for this style class or its superclasses.

        Returns:
            BaseStyles | None: The registered instance or None if not found.
        """
        if cls in _BaseStylesMeta._default_instances:
            return _BaseStylesMeta._default_instances[cls]
        for registered_cls, inst in _BaseStylesMeta._default_instances.items():
            if issubclass(cls, registered_cls) or issubclass(registered_cls, cls):
                return inst
        return None

    def __getattribute__(cls, name: str) -> Any:  # noqa: ANN401
        val = super().__getattribute__(name)
        if isinstance(val, property):
            inst = cls.get_default_instance()
            if inst is not None and val.fget is not None:
                return val.fget(inst)
        if name in {"patch_font", "copy"}:
            inst = cls.get_default_instance()
            if inst is not None:
                return val.__get__(inst, cls)
        return val

    def __getattr__(cls, name: str) -> Any:  # noqa: ANN401
        if name.startswith("__"):
            raise AttributeError(f"type object '{cls.__name__}' has no attribute '{name}'")
        inst = cls.get_default_instance()
        if inst is not None:
            if name in cls.model_fields:
                return getattr(inst, name)
            if hasattr(inst, name):
                return getattr(inst, name)
        raise AttributeError(f"type object '{cls.__name__}' has no attribute '{name}'")

    def __getitem__(cls, key: str) -> Style:
        inst = cls.get_default_instance()
        if inst is not None:
            return inst[key]
        raise KeyError(f'Style "{key}" is not found in {cls.__name__}.')

    def __dir__(cls) -> list[str]:
        attrs = set(super().__dir__())
        for field in cls.model_fields:
            attrs.add(field)
        return sorted(attrs)


class BaseStyles(BaseModel, metaclass=_BaseStylesMeta):
    """Base model for preset styles providing iteration, dictionary-like access, and autocompletion.

    Attributes:
        background_color (ColorType): Default canvas background color for this preset style.
        sourcecode_font (FontSourceCode): Default sourcecode font for this preset style.
    """

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        extra="allow",
        frozen=True,
    )

    width: int = 140
    height: int = 70
    dpi: int = 100
    background_color: ColorType = (255, 255, 255, 1.0)
    sourcecode_font: FontSourceCode = FontSourceCode.SOURCECODEPRO
    colors: Any = None

    def __init__(self, **kwargs: Any) -> None:  # noqa: ANN401
        """Initialize preset styles instance.

        If called without arguments (or with partial overrides), missing fields are
        automatically populated from the registered default singleton instance for this class.
        """
        normalized: dict[str, Any] = {}
        for k, v in kwargs.items():
            target_key = _resolve_style_field_name(self.__class__, k, v)
            if target_key == "background_color" and v is not None:
                try:
                    normalized[target_key] = v if isinstance(v, Color) else Color(v)
                except Exception:
                    normalized[target_key] = v
            else:
                normalized[target_key] = v

        default_inst = self.__class__.get_default_instance()
        if default_inst is not None:
            merged = {**default_inst.__dict__, **normalized}
            super().__init__(**merged)
        else:
            super().__init__(**normalized)

    # 4 Universal semantic roles available across all preset catalogs including monochrome (10 variants each)
    Primary: Style
    PrimaryBordered: Style | None = None
    PrimaryBold: Style | None = None
    PrimaryLight: Style | None = None
    PrimaryFlat: Style | None = None
    PrimaryOutline: Style | None = None
    PrimarySolid: Style | None = None
    PrimaryOutlineBold: Style | None = None
    PrimarySolidBold: Style | None = None
    PrimaryOutlineLight: Style | None = None
    PrimarySolidLight: Style | None = None
    PrimaryDashed: Style | None = None
    PrimaryDashedBold: Style | None = None
    PrimaryDashedLight: Style | None = None

    Secondary: Style | None = None
    SecondaryBordered: Style | None = None
    SecondaryBold: Style | None = None
    SecondaryLight: Style | None = None
    SecondaryFlat: Style | None = None
    SecondaryOutline: Style | None = None
    SecondarySolid: Style | None = None
    SecondaryOutlineBold: Style | None = None
    SecondarySolidBold: Style | None = None
    SecondaryOutlineLight: Style | None = None
    SecondarySolidLight: Style | None = None
    SecondaryDashed: Style | None = None
    SecondaryDashedBold: Style | None = None
    SecondaryDashedLight: Style | None = None

    Accent: Style | None = None
    AccentBordered: Style | None = None
    AccentBold: Style | None = None
    AccentLight: Style | None = None
    AccentFlat: Style | None = None
    AccentOutline: Style | None = None
    AccentSolid: Style | None = None
    AccentOutlineBold: Style | None = None
    AccentSolidBold: Style | None = None
    AccentOutlineLight: Style | None = None
    AccentSolidLight: Style | None = None
    AccentDashed: Style | None = None
    AccentDashedBold: Style | None = None
    AccentDashedLight: Style | None = None

    Muted: Style | None = None
    MutedBordered: Style | None = None
    MutedBold: Style | None = None
    MutedLight: Style | None = None
    MutedFlat: Style | None = None
    MutedOutline: Style | None = None
    MutedSolid: Style | None = None
    MutedOutlineBold: Style | None = None
    MutedSolidBold: Style | None = None
    MutedOutlineLight: Style | None = None
    MutedSolidLight: Style | None = None
    MutedDashed: Style | None = None
    MutedDashedBold: Style | None = None
    MutedDashedLight: Style | None = None

    # Extended semantic roles (10 variants each):
    # - danger & success: Provided for color presets (giving 6 action/status roles total; excluded in monochrome)
    # - light & dark: Surface backgrounds and high-contrast typography
    Light: Style | None = None
    LightBordered: Style | None = None
    LightBold: Style | None = None
    LightLight: Style | None = None
    LightFlat: Style | None = None
    LightOutline: Style | None = None
    LightSolid: Style | None = None
    LightOutlineBold: Style | None = None
    LightSolidBold: Style | None = None
    LightOutlineLight: Style | None = None
    LightSolidLight: Style | None = None
    LightDashed: Style | None = None
    LightDashedBold: Style | None = None
    LightDashedLight: Style | None = None

    Dark: Style | None = None
    DarkBordered: Style | None = None
    DarkBold: Style | None = None
    DarkLight: Style | None = None
    DarkFlat: Style | None = None
    DarkOutline: Style | None = None
    DarkSolid: Style | None = None
    DarkOutlineBold: Style | None = None
    DarkSolidBold: Style | None = None
    DarkOutlineLight: Style | None = None
    DarkSolidLight: Style | None = None
    DarkDashed: Style | None = None
    DarkDashedBold: Style | None = None
    DarkDashedLight: Style | None = None

    Danger: Style | None = None
    DangerBordered: Style | None = None
    DangerBold: Style | None = None
    DangerLight: Style | None = None
    DangerFlat: Style | None = None
    DangerOutline: Style | None = None
    DangerSolid: Style | None = None
    DangerOutlineBold: Style | None = None
    DangerSolidBold: Style | None = None
    DangerOutlineLight: Style | None = None
    DangerSolidLight: Style | None = None
    DangerDashed: Style | None = None
    DangerDashedBold: Style | None = None
    DangerDashedLight: Style | None = None

    Success: Style | None = None
    SuccessBordered: Style | None = None
    SuccessBold: Style | None = None
    SuccessLight: Style | None = None
    SuccessFlat: Style | None = None
    SuccessOutline: Style | None = None
    SuccessSolid: Style | None = None
    SuccessOutlineBold: Style | None = None
    SuccessSolidBold: Style | None = None
    SuccessOutlineLight: Style | None = None
    SuccessSolidLight: Style | None = None
    SuccessDashed: Style | None = None
    SuccessDashedBold: Style | None = None
    SuccessDashedLight: Style | None = None

    Canvas: Style | None = None
    CanvasFlat: Style | None = None

    def __iter__(self) -> Generator[tuple[str, Any], None, None]:
        """Yield (field_name, field_value) pairs for all fields in the preset style model.

        Returns:
            Generator[tuple[str, Any], None, None]: Generator yielding field name and value pairs.
        """
        for field_name in self.model_fields:
            try:
                val = getattr(self, field_name)
            except AttributeError:
                continue
            if val is not None:
                yield field_name, val

    def __getitem__(self, key: str) -> Any:  # noqa: ANN401
        """Allow dictionary-like item access by style name.

        Args:
            key (str): Field name or style name.

        Returns:
            Any: Value of the specified field.

        Raises:
            KeyError: If the specified key does not exist.
        """
        try:
            if hasattr(self, key):
                val = getattr(self, key)
                if val is not None:
                    return val
        except AttributeError:
            pass
        raise KeyError(f'Style "{key}" is not found in {self.__class__.__name__}.')

    def __getattr__(self, name: str) -> Any:  # noqa: ANN401
        """Allow fallback resolution for extra fields on instances."""
        if name.startswith("__"):
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")
        extra = getattr(self, "__pydantic_extra__", None)
        if extra is not None and name in extra:
            return extra[name]
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")

    def __dir__(self) -> list[str]:
        """Include style attribute names."""
        attrs = set(super().__dir__())
        for field in self.__class__.model_fields:
            attrs.add(field)
        return sorted(attrs)

    def get(self, key: str, default: Any = None) -> Any:  # noqa: ANN401
        """Safely retrieve a style or attribute with an optional default fallback.

        Args:
            key (str): Field name or style name.
            default (Any): Fallback value if field is not found. Defaults to None.

        Returns:
            Any: Field value or default fallback.
        """
        try:
            val = getattr(self, key, default)
            return default if val is None else val
        except AttributeError:
            return default

    def styles(self) -> dict[str, Style]:
        """Extract only Style objects defined on this preset as a dictionary.

        Returns:
            dict[str, Style]: Dictionary mapping style names to Style instances.
        """
        return {k: v for k, v in self if isinstance(v, Style)}

    def patch(self, **kwargs: Any) -> Self:  # noqa: ANN401
        """Create a new copy of preset styles with updated attributes.

        Args:
            **kwargs: Style attributes to update (accepts PascalCase, snake_case, or aliases).

        Returns:
            Self: New preset styles instance with updated attributes.
        """
        updates: dict[str, Any] = {}
        for k, v in kwargs.items():
            if v is not None:
                target_key = _resolve_style_field_name(self.__class__, k, v)
                if target_key == "background_color":
                    try:
                        updates[target_key] = v if isinstance(v, Color) else Color(v)
                    except Exception:
                        updates[target_key] = v
                else:
                    updates[target_key] = v
        return self.model_copy(update=updates)

    @validate_call
    def patch_font(
        self,
        regular: FontBase | FontFile | None = None,
        *,
        bold: FontBase | FontFile | None = None,
        light: FontBase | FontFile | None = None,
        sourcecode: FontSourceCode | None = None,
    ) -> Self:
        """Create a new copy of preset styles with updated font configurations.

        Args:
            regular (FontBase | FontFile | None): Default baseline font applied to all styles.
                If provided without explicit bold/light overrides, it is also applied as fallback
                for bold and light variants.
            bold (FontBase | FontFile | None): Font override for bold style variants ('Bold', '*Bold').
            light (FontBase | FontFile | None): Font override for light style variants ('Light', '*Light').
            sourcecode (FontSourceCode | None): Monospace source code font override.

        Returns:
            Self: New preset styles instance with updated font attributes.
        """
        updates: dict[str, Any] = {}

        if sourcecode is not None:
            updates["sourcecode_font"] = sourcecode

        for field_name in self.model_fields:
            try:
                val = getattr(self, field_name)
            except AttributeError:
                continue
            if not isinstance(val, Style):
                continue

            target_font = _resolve_target_font(field_name, regular, bold, light)
            if target_font is not None:
                updates[field_name] = val.patch(text_font=target_font)

        return self.model_copy(update=updates)


__all__ = [
    "BaseStyles",
]
