# Copyright (c) 2024 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Latest API module."""

from drawlib.v0_2.private.core.colors import (
    Colors,
    Colors140,
    ColorsBase,
    ColorsThemeDefault,
    ColorsThemeEssentials,
    ColorsThemeMonochrome,
)
from drawlib.v0_2.private.core.dimage import (
    Dimage,
)
from drawlib.v0_2.private.core.fonts import (
    Font,
    FontArabic,
    FontBrahmic,
    FontChinese,
    FontFile,
    FontJapanese,
    FontKorean,
    FontMonoSpace,
    FontRoboto,
    FontSansSerif,
    FontSerif,
    FontSourceCode,
    FontThai,
)
from drawlib.v0_2.private.core.model import (
    IconStyle,
    ImageStyle,
    LineStyle,
    ShapeStyle,
    ShapeTextStyle,
    TextStyle,
)
from drawlib.v0_2.private.core.theme import (
    dtheme,
)
from drawlib.v0_2.private.core_canvas.canvas import (
    arc,
    arrow,
    arrow_arc,
    arrow_l,
    arrow_polyline,
    arrow_u,
    chevron,
    circle,
    clear,
    config,
    donuts,
    ellipse,
    fan,
    image,
    line,
    line_arc,
    line_bezier1,
    line_bezier2,
    line_curved,
    lines,
    lines_bezier,
    lines_curved,
    parallelogram,
    polygon,
    rectangle,
    regularpolygon,
    rhombus,
    save,
    shape,
    show,
    star,
    text,
    text_vertical,
    trapezoid,
    triangle,
    wedge,
)
from drawlib.v0_2.private.dutil import (
    dutil_canvas,
    dutil_color,
    dutil_script,
)
from drawlib.v0_2.private.dutil.settings import (
    dutil_settings,
)
from drawlib.v0_2.private.icons import (
    phosphor as icon_phosphor,
)
from drawlib.v0_2.private.icons.util import (
    icon,
)
from drawlib.v0_2.private.smartarts import (
    dsart,
)

__all__ = [
    # Colors
    "Colors",
    "Colors140",
    "ColorsBase",
    "ColorsThemeDefault",
    "ColorsThemeEssentials",
    "ColorsThemeMonochrome",
    # Dimage
    "Dimage",
    # Fonts
    "Font",
    "FontArabic",
    "FontBrahmic",
    "FontChinese",
    "FontFile",
    "FontJapanese",
    "FontKorean",
    "FontMonoSpace",
    "FontRoboto",
    "FontSansSerif",
    "FontSerif",
    "FontSourceCode",
    "FontThai",
    # Style models
    "IconStyle",
    "ImageStyle",
    "LineStyle",
    "ShapeStyle",
    "ShapeTextStyle",
    "TextStyle",
    # Theme
    "dtheme",
    # Canvas and Shapes
    "arc",
    "arrow",
    "arrow_arc",
    "arrow_l",
    "arrow_polyline",
    "arrow_u",
    "chevron",
    "circle",
    "clear",
    "config",
    "donuts",
    "ellipse",
    "fan",
    "image",
    "line",
    "line_arc",
    "line_bezier1",
    "line_bezier2",
    "line_curved",
    "lines",
    "lines_bezier",
    "lines_curved",
    "parallelogram",
    "polygon",
    "rectangle",
    "regularpolygon",
    "rhombus",
    "save",
    "shape",
    "show",
    "star",
    "text",
    "text_vertical",
    "trapezoid",
    "triangle",
    "wedge",
    # Utilities
    "dutil_canvas",
    "dutil_color",
    "dutil_script",
    "dutil_settings",
    # Icons
    "icon_phosphor",
    "icon",
    # Smartarts
    "dsart",
]
