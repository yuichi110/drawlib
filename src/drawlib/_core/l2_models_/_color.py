# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Color model module for drawlib.

Provides the immutable Color class representing an RGBA color tuple with channel accessors,
patch derivation, hex conversion, and Pydantic validation integration.
"""

from __future__ import annotations

import re
from typing import Any, Sequence

from pydantic_core import core_schema

_HEX_COLOR_PATTERN = re.compile(r"^#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{4}|[0-9a-fA-F]{6}|[0-9a-fA-F]{8})$")
_HEX_NO_HASH_PATTERN = re.compile(r"^(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{4}|[0-9a-fA-F]{6}|[0-9a-fA-F]{8})$")


def _extract_rgba(
    r: int | tuple[int | float, ...] | list[int | float] | Color,
    g: int | None,
    b: int | None,
    alpha: float | None,
) -> tuple[int | float, int | float, int | float, int | float]:
    """Extract raw r, g, b, a values from inputs."""
    if isinstance(r, (tuple, list)):
        seq_len = len(r)
        if seq_len not in {3, 4}:
            raise ValueError(f"Color tuple must have length 3 (RGB) or 4 (RGBA). Given length: {seq_len}.")
        a_val = (1.0 if seq_len == 3 else r[3]) if alpha is None else alpha
        return r[0], r[1], r[2], a_val
    if isinstance(r, (int, float)):
        if g is None or b is None:
            raise ValueError("Green (g) and Blue (b) channels must be provided when Red (r) is an integer.")
        return r, g, b, 1.0 if alpha is None else alpha
    raise ValueError(f"Invalid color value: {r}")


class Color(tuple[int, int, int, float]):
    """Immutable RGBA Color tuple with channel patching and hex representation.

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

    def __new__(
        cls,
        r: int | tuple[int | float, ...] | list[int | float] | Color | str,
        g: int | None = None,
        b: int | None = None,
        alpha: float | None = None,
    ) -> Color:
        """Create a new Color instance.

        Args:
            r (int | tuple[int | float, ...] | list[int | float] | Color | str):
                Red channel integer (0-255), RGB/RGBA tuple/list, Color instance, or hex string.
            g (int | None): Green channel integer (0-255) when r is an integer.
            b (int | None): Blue channel integer (0-255) when r is an integer.
            alpha (float | None): Alpha value (0.0-1.0). Defaults to 1.0 (or original alpha if r is RGBA).

        Returns:
            Color: The new Color instance.

        Raises:
            ValueError: If channel values or sequence length are invalid.
        """
        if isinstance(r, str):
            return cls.from_hex(r, alpha=alpha)

        r_val, g_val, b_val, a_val = _extract_rgba(r, g, b, alpha)

        try:
            r_int = int(r_val)
            g_int = int(g_val)
            b_int = int(b_val)
        except (TypeError, ValueError) as err:
            msg = f"RGB channel values must be integers between 0 and 255. Got: {(r_val, g_val, b_val)}"
            raise ValueError(msg) from err

        if not (0 <= r_int <= 255 and 0 <= g_int <= 255 and 0 <= b_int <= 255):
            raise ValueError(f"RGB channel values must be between 0 and 255. Got: {(r_int, g_int, b_int)}")

        try:
            a_float = float(a_val)
        except (TypeError, ValueError) as err:
            raise ValueError(f"Alpha channel must be a float between 0.0 and 1.0. Got: {a_val}") from err

        if not (0.0 <= a_float <= 1.0):
            raise ValueError(f"Alpha channel must be between 0.0 and 1.0. Got: {a_float}")

        return super().__new__(cls, (r_int, g_int, b_int, a_float))

    def __repr__(self) -> str:
        """Return developer-friendly string representation."""
        if self.alpha == 1.0:
            return f"Color({self.r}, {self.g}, {self.b})"
        return f"Color({self.r}, {self.g}, {self.b}, alpha={self.alpha})"

    def __eq__(self, other: object) -> bool:
        """Check equality with another Color or tuple/list.

        Matches 4-tuples directly, and matches 3-tuples when alpha is 1.0.
        """
        if isinstance(other, (tuple, list)):
            if len(other) == 4:
                return (self[0], self[1], self[2], self[3]) == (other[0], other[1], other[2], other[3])
            if len(other) == 3 and self.alpha == 1.0:
                return (self[0], self[1], self[2]) == (other[0], other[1], other[2])
        return False

    def __hash__(self) -> int:
        """Return hash based on RGBA channels."""
        return hash((self[0], self[1], self[2], self[3]))

    @property
    def r(self) -> int:
        """Red channel (0-255)."""
        return self[0]

    @property
    def g(self) -> int:
        """Green channel (0-255)."""
        return self[1]

    @property
    def b(self) -> int:
        """Blue channel (0-255)."""
        return self[2]

    @property
    def alpha(self) -> float:
        """Alpha/opacity channel (0.0-1.0)."""
        return self[3]

    @property
    def a(self) -> float:
        """Alias for alpha (0.0-1.0)."""
        return self[3]

    @property
    def rgb(self) -> tuple[int, int, int]:
        """RGB 3-tuple (r, g, b)."""
        return (self[0], self[1], self[2])

    @property
    def rgba(self) -> tuple[int, int, int, float]:
        """RGBA 4-tuple (r, g, b, alpha)."""
        return (self[0], self[1], self[2], self[3])

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
            r (int | None): New red channel (0-255).
            g (int | None): New green channel (0-255).
            b (int | None): New blue channel (0-255).
            alpha (float | None): New alpha channel (0.0-1.0).

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
            hexcode (str): Hex color string.
            alpha (float | None): Optional alpha override (0.0-1.0).

        Returns:
            Color: Parsed Color instance.

        Raises:
            ValueError: If hex string is invalid.
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

        return cls(r_val, g_val, b_val, a_val)

    @classmethod
    def __get_pydantic_core_schema__(  # noqa: PLW3201
        cls,
        _source_type: Any,  # noqa: ANN401
        _handler: Any,  # noqa: ANN401
    ) -> core_schema.CoreSchema:
        """Pydantic V2 core schema integration for Color."""

        def validate_color(v: Any) -> Color:  # noqa: ANN401
            if isinstance(v, Color):
                return v
            if isinstance(v, str):
                return cls.from_hex(v)
            if isinstance(v, (tuple, list)):
                return cls(v)
            raise ValueError(f"Cannot convert {type(v)} to Color. Expected Color, hex string, or RGB/RGBA tuple.")

        return core_schema.no_info_plain_validator_function(validate_color)


__all__ = [
    "Color",
]
