# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Public geographical map module for drawlib.

Provides the unified ``GeoMap`` component for rendering world, country, city,
and custom GeoJSON maps onto the drawlib canvas.
"""

from __future__ import annotations

from drawlib._geo import (
    Cities,
    Countries,
    GeoData,
    GeoElement,
    GeoMap,
    GeoPolygon,
    GeoTarget,
    World,
    WorldPreset,
)

__all__ = [
    "Cities",
    "Countries",
    "GeoData",
    "GeoElement",
    "GeoMap",
    "GeoPolygon",
    "GeoTarget",
    "World",
    "WorldPreset",
]
