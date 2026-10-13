# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Public shapes module for drawlib.

Provides 43 shape primitives organized into 6 semantic categories:
- Basic (`rectangle`, `circle`, `ellipse`, `wedge`, `fan`, `arc`)
- Polygon (`triangle`, `parallelogram`, `trapezoid`, `rhombus`, `regularpolygon`, `star`, `plaque`, `polygon`, `shape`)
- Arrow (`arrow`, `arrow_l`, `arrow_u`, `arrow_arc`, `arrow_polyline`, `chevron`)
- Container (`cylinder`, `cube`, `document`, `funnel`, `cloud`, `brace`)
- Badge (`bubblespeech`, `pin`, `tag`, `ribbon`, `shield`, `forbidden`, `checkmark`, `explosion`)
- Symbol (`face`, `clock`, `sun`, `moon`, `heart`, `lightning`, `gear`, `math_symbol`)
"""

from __future__ import annotations

from drawlib._core.l4_canvas import (
    arc,
    arrow,
    arrow_arc,
    arrow_l,
    arrow_polyline,
    arrow_u,
    brace,
    bubblespeech,
    checkmark,
    chevron,
    circle,
    clock,
    cloud,
    cube,
    cylinder,
    document,
    ellipse,
    explosion,
    face,
    fan,
    forbidden,
    funnel,
    gear,
    heart,
    lightning,
    math_symbol,
    moon,
    parallelogram,
    pin,
    plaque,
    polygon,
    rectangle,
    regularpolygon,
    rhombus,
    ribbon,
    shape,
    shield,
    star,
    sun,
    tag,
    trapezoid,
    triangle,
    wedge,
)

__all__ = [
    "arc",
    "arrow",
    "arrow_arc",
    "arrow_l",
    "arrow_polyline",
    "arrow_u",
    "brace",
    "bubblespeech",
    "checkmark",
    "chevron",
    "circle",
    "clock",
    "cloud",
    "cube",
    "cylinder",
    "document",
    "ellipse",
    "explosion",
    "face",
    "fan",
    "forbidden",
    "funnel",
    "gear",
    "heart",
    "lightning",
    "math_symbol",
    "moon",
    "parallelogram",
    "pin",
    "plaque",
    "polygon",
    "rectangle",
    "regularpolygon",
    "rhombus",
    "ribbon",
    "shape",
    "shield",
    "star",
    "sun",
    "tag",
    "trapezoid",
    "triangle",
    "wedge",
]
