# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

from typing import Literal

from pydantic import BaseModel, ConfigDict, InstanceOf

from drawlib.v0_2.private.l2_types import (
    TypeColor,
    TypeColorRGB,
)
from drawlib.v0_2.private.l3_fonts import FontSourceCode
from drawlib.v0_2.private.l3_styles import (
    IconStyle,
    ImageStyle,
    LineStyle,
    ShapeStyle,
    ShapeTextStyle,
    TextStyle,
)


class ThemeStyles(BaseModel):
    """Represents a collection of style configurations for various shapes and text in a theme."""

    model_config = ConfigDict(
        extra="forbid",
        validate_assignment=True,
    )

    # mandatory for default
    iconstyle: IconStyle | None = None
    imagestyle: ImageStyle | None = None
    linestyle: LineStyle | None = None
    shapestyle: ShapeStyle | None = None
    shapetextstyle: ShapeTextStyle | None = None
    textstyle: TextStyle | None = None

    # optional for default
    arcstyle: ShapeStyle | None = None
    arctextstyle: ShapeTextStyle | None = None
    circlestyle: ShapeStyle | None = None
    circletextstyle: ShapeTextStyle | None = None
    ellipsestyle: ShapeStyle | None = None
    ellipsetextstyle: ShapeTextStyle | None = None
    polygonstyle: ShapeStyle | None = None
    polygontextstyle: ShapeTextStyle | None = None
    rectanglestyle: ShapeStyle | None = None
    rectangletextstyle: ShapeTextStyle | None = None
    regularpolygonstyle: ShapeStyle | None = None
    regularpolygontextstyle: ShapeTextStyle | None = None
    wedgestyle: ShapeStyle | None = None
    wedgetextstyle: ShapeTextStyle | None = None
    donutsstyle: ShapeStyle | None = None
    donutstextstyle: ShapeTextStyle | None = None
    fanstyle: ShapeStyle | None = None
    fantextstyle: ShapeTextStyle | None = None

    arrowstyle: ShapeStyle | None = None
    arrowtextstyle: ShapeTextStyle | None = None
    rhombusstyle: ShapeStyle | None = None
    rhombustextstyle: ShapeTextStyle | None = None
    parallelogramstyle: ShapeStyle | None = None
    parallelogramtextstyle: ShapeTextStyle | None = None
    trapezoidstyle: ShapeStyle | None = None
    trapezoidtextstyle: ShapeTextStyle | None = None
    trianglestyle: ShapeStyle | None = None
    triangletextstyle: ShapeTextStyle | None = None
    starstyle: ShapeStyle | None = None
    startextstyle: ShapeTextStyle | None = None
    chevronstyle: ShapeStyle | None = None
    chevrontextstyle: ShapeTextStyle | None = None

    bubblespeechstyle: ShapeStyle | None = None
    bubblespeechtextstyle: ShapeTextStyle | None = None


class OfficialThemeStyle(BaseModel):
    """Represents the official style configuration for a theme."""

    model_config = ConfigDict(
        extra="forbid",
        validate_assignment=True,
    )

    default_style: ThemeStyles
    named_styles: list[tuple[str, ThemeStyles]]
    theme_colors: list[tuple[str, TypeColorRGB]]
    backgroundcolor: TypeColor
    sourcecodefont: InstanceOf[FontSourceCode] | None
