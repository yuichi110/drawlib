# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Primitive type definitions for drawlib."""

from typing import Annotated, Any

from pydantic import Field


def _normalize_str(v: Any) -> Any:  # noqa: ANN401
    """Normalize string by stripping whitespace and converting to lowercase."""
    if isinstance(v, str):
        return v.strip().lower()
    return v


# Integers
PosInt = Annotated[int, Field(ge=0)]
NegInt = Annotated[int, Field(le=0)]
NumVertex = Annotated[int, Field(ge=3)]

PosFloat = Annotated[float, Field(ge=0.0)]
NegFloat = Annotated[float, Field(le=0.0)]
