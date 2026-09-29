# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Color model and types for drawlib.

Provides the immutable Color class representing an RGBA color model with channel accessors,
patch derivation, hex conversion, and Pydantic validation integration, along with associated color type definitions.
"""

from __future__ import annotations

import re
from typing import Annotated, Any

from pydantic import BaseModel, BeforeValidator, ConfigDict, Field, model_validator

_HEX_COLOR_PATTERN = re.compile(r"^#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{4}|[0-9a-fA-F]{6}|[0-9a-fA-F]{8})$")
_HEX_NO_HASH_PATTERN = re.compile(r"^(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{4}|[0-9a-fA-F]{6}|[0-9a-fA-F]{8})$")
_UNSET = object()


def _parse_hex(hexcode: str, alpha: float | None = None) -> tuple[int, int, int, float]:
    """Parse hexadecimal string into integer RGB and float alpha.

    Args:
        hexcode: Hex color string.
        alpha: Optional alpha override (0.0-1.0).

    Returns:
        tuple[int, int, int, float]: Parsed (r, g, b, alpha) values.

    Raises:
        ValueError: If hexcode format is invalid.
    """
    cleaned = hexcode.strip()
    if not (_HEX_COLOR_PATTERN.match(cleaned) or _HEX_NO_HASH_PATTERN.match(cleaned)):
        msg = f"Invalid hex color string: '{hexcode}'. Expected '#RGB', '#RGBA', '#RRGGBB', or '#RRGGBBAA'."
        raise ValueError(msg)

    raw_hex = cleaned.lstrip("#")
    if len(raw_hex) == 3:
        raw_hex = "".join(c * 2 for c in raw_hex)
    elif len(raw_hex) == 4:
        raw_hex = "".join(c * 2 for c in raw_hex[:3]) + "".join(c * 2 for c in raw_hex[3])

    r_val = int(raw_hex[0:2], 16)
    g_val = int(raw_hex[2:4], 16)
    b_val = int(raw_hex[4:6], 16)
    a_val = 1.0 if len(raw_hex) == 6 else int(raw_hex[6:8], 16) / 255.0

    if alpha is not None:
        a_val = alpha

    return r_val, g_val, b_val, a_val


def _normalize_color_input(
    data: Any,  # noqa: ANN401
    alpha: float | None = None,
) -> dict[str, Any]:  # noqa: ANN401
    """Normalize various color inputs into an RGBA dictionary for Pydantic.

    Args:
        data: Color instance, hex string, sequence of channel values, or dictionary.
        alpha: Optional alpha override (0.0-1.0).

    Returns:
        dict[str, Any]: Dictionary containing r, g, b, and alpha channels.

    Raises:
        ValueError: If input format or sequence length is invalid.
    """
    if isinstance(data, Color):
        return {"r": data.r, "g": data.g, "b": data.b, "alpha": data.alpha if alpha is None else alpha}
    if isinstance(data, str):
        r, g, b, a = _parse_hex(data, alpha=alpha)
        return {"r": r, "g": g, "b": b, "alpha": a}
    if isinstance(data, (tuple, list)):
        seq_len = len(data)
        if seq_len not in {3, 4}:
            raise ValueError(f"Color tuple must have length 3 (RGB) or 4 (RGBA). Given length: {seq_len}.")
        a_val = (1.0 if seq_len == 3 else data[3]) if alpha is None else alpha
        return {"r": data[0], "g": data[1], "b": data[2], "alpha": a_val}
    if isinstance(data, dict):
        d = dict(data)
        if alpha is not None:
            d["alpha"] = alpha
        return d
    raise ValueError(f"Invalid color value: {data}")


class Color(BaseModel):
    """Immutable RGBA Color model with channel validation, patching, and hex representation.

    Attributes:
        r (int): Red channel (0-255).
        g (int): Green channel (0-255).
        b (int): Blue channel (0-255).
        alpha (float): Alpha/opacity channel (0.0-1.0).
        a (float): Alias for alpha (0.0-1.0).
        rgb (tuple[int, int, int]): RGB 3-tuple.
        rgba (tuple[int, int, int, float]): RGBA 4-tuple.
        hex (str): Hex string representation (e.g. '#3498db' or '#3498db80').
    """

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
        validate_assignment=True,
    )

    r: int = Field(ge=0, le=255, description="Red channel (0-255)")
    g: int = Field(ge=0, le=255, description="Green channel (0-255)")
    b: int = Field(ge=0, le=255, description="Blue channel (0-255)")
    alpha: float = Field(default=1.0, ge=0.0, le=1.0, description="Alpha channel (0.0-1.0)")

    @model_validator(mode="before")
    @classmethod
    def _pre_validate(cls, data: Any) -> Any:  # noqa: ANN401
        if isinstance(data, (Color, str, tuple, list)):
            return _normalize_color_input(data)
        return data

    def __init__(
        self,
        r: int | tuple[int | float, ...] | list[int | float] | Color | str | dict[str, Any] | object = _UNSET,
        g: int | None = None,
        b: int | None = None,
        alpha: float | None = None,
        **kwargs: Any,  # noqa: ANN401
    ) -> None:
        """Create a new Color instance.

        Args:
            r: Red channel integer (0-255), RGB/RGBA tuple/list, Color instance, or hex string.
            g: Green channel integer (0-255) when r is an integer.
            b: Blue channel integer (0-255) when r is an integer.
            alpha: Alpha value (0.0-1.0). Defaults to 1.0 (or original alpha if r is RGBA).
            **kwargs: Keyword arguments for r, g, b, alpha.

        Raises:
            ValueError: If channel values or sequence length are invalid.
            ValidationError: If channel values fail validation constraints.
        """
        if r is _UNSET:
            if kwargs:
                super().__init__(**kwargs)
                return
            raise ValueError("Color channel values must be provided.")

        if g is not None or b is not None:
            if g is None or b is None:
                raise ValueError("Green (g) and Blue (b) channels must be provided when Red (r) is an integer.")
            data: dict[str, Any] = {"r": r, "g": g, "b": b}
            if alpha is not None:
                data["alpha"] = alpha
            if kwargs:
                data.update(kwargs)
            super().__init__(**data)
            return

        data = _normalize_color_input(r, alpha=alpha)
        if kwargs:
            data.update(kwargs)
        super().__init__(**data)

    def to_mplot_rgba(self) -> tuple[float, float, float, float]:
        """Return normalized RGBA tuple (0.0-1.0) for matplotlib.

        Returns:
            tuple[float, float, float, float]: Normalized RGBA tuple.
        """
        return (round(self.r / 255.0, 5), round(self.g / 255.0, 5), round(self.b / 255.0, 5), self.alpha)

    @property
    def a(self) -> float:
        """Alias for alpha (0.0-1.0)."""
        return self.alpha

    @property
    def rgb(self) -> tuple[int, int, int]:
        """RGB 3-tuple (r, g, b)."""
        return (self.r, self.g, self.b)

    @property
    def rgba(self) -> tuple[int, int, int, float]:
        """RGBA 4-tuple (r, g, b, alpha)."""
        return (self.r, self.g, self.b, self.alpha)

    @property
    def hex(self) -> str:
        """Hex string representation, e.g. '#3498db' or '#3498db80'."""
        if self.alpha == 1.0:
            return f"#{self.r:02x}{self.g:02x}{self.b:02x}"
        return f"#{self.r:02x}{self.g:02x}{self.b:02x}{int(round(self.alpha * 255)):02x}"

    def patch(
        self,
        *,
        r: int | None = None,
        g: int | None = None,
        b: int | None = None,
        alpha: float | None = None,
    ) -> Color:
        """Derive a new Color with modified channels (similar to Style.patch).

        Args:
            r: New red channel (0-255).
            g: New green channel (0-255).
            b: New blue channel (0-255).
            alpha: New alpha channel (0.0-1.0).

        Returns:
            Color: A new immutable Color instance with updated values.
        """
        return Color(
            r=self.r if r is None else r,
            g=self.g if g is None else g,
            b=self.b if b is None else b,
            alpha=self.alpha if alpha is None else alpha,
        )

    @classmethod
    def from_hex(cls, hexcode: str, alpha: float | None = None) -> Color:
        """Create a Color instance from a hexadecimal string.

        Supports '#RGB', '#RGBA', '#RRGGBB', and '#RRGGBBAA' (with or without '#').

        Args:
            hexcode: Hex color string.
            alpha: Optional alpha override (0.0-1.0).

        Returns:
            Color: Parsed Color instance.

        Raises:
            ValueError: If hex string is invalid.
        """
        r, g, b, a = _parse_hex(hexcode, alpha=alpha)
        return cls(r, g, b, a)

    def __iter__(self) -> Any:  # noqa: ANN401
        """Yield channels sequentially (r, g, b, alpha) for tuple unpacking."""
        return iter((self.r, self.g, self.b, self.alpha))

    def __len__(self) -> int:
        """Return number of channels (always 4 for RGBA)."""
        return 4

    def __getitem__(self, index: Any) -> Any:  # noqa: ANN401
        """Get channel value by sequence index or slice."""
        return (self.r, self.g, self.b, self.alpha)[index]

    def __eq__(self, other: object) -> bool:
        """Check equality with another Color or tuple/list.

        Matches 4-tuples directly, and matches 3-tuples when alpha is 1.0.
        """
        if isinstance(other, Color):
            return (self.r, self.g, self.b, self.alpha) == (other.r, other.g, other.b, other.alpha)
        if isinstance(other, (tuple, list)):
            if len(other) == 4:
                return (self.r, self.g, self.b, self.alpha) == (other[0], other[1], other[2], other[3])
            if len(other) == 3 and self.alpha == 1.0:
                return (self.r, self.g, self.b) == (other[0], other[1], other[2])
        return False

    def __hash__(self) -> int:
        """Return hash based on RGBA channels."""
        return hash((self.r, self.g, self.b, self.alpha))

    def __repr__(self) -> str:
        """Return developer-friendly string representation."""
        if self.alpha == 1.0:
            return f"Color({self.r}, {self.g}, {self.b})"
        return f"Color({self.r}, {self.g}, {self.b}, alpha={self.alpha})"


# Color type definitions
Alpha = Annotated[float, Field(ge=0.0, le=1.0)]
RGBChannel = Annotated[int, Field(ge=0, le=255)]
ColorRGB = tuple[RGBChannel, RGBChannel, RGBChannel]
ColorRGBA = tuple[RGBChannel, RGBChannel, RGBChannel, Alpha]
ColorType = Annotated[
    Color | ColorRGB | ColorRGBA | str,
    BeforeValidator(lambda v: v if isinstance(v, Color) else Color(v)),
]

__all__ = [
    "Alpha",
    "Color",
    "ColorRGB",
    "ColorRGBA",
    "ColorType",
    "RGBChannel",
]
