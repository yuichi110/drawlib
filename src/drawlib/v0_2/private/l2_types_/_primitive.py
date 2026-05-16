# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Primitive type definitions for drawlib."""

from typing import Annotated

from pydantic import Field

# bool
TypeBool = Annotated[bool, Field()]

# int
TypeInt = Annotated[int, Field()]
TypeNegInt = Annotated[int, Field(le=0)]
TypePosInt = Annotated[int, Field(ge=0)]
TypeNumVertex = Annotated[int, Field(ge=3)]

# float
TypeFloat = Annotated[float, Field()]
TypeNegFloat = Annotated[float, Field(le=0)]
TypePosFloat = Annotated[float, Field(ge=0.0)]

# str
TypeStr = Annotated[str, Field()]
