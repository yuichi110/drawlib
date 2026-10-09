# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Internal geographical map module for drawlib.smartarts."""

from __future__ import annotations

from drawlib._smartarts._geomap._geomap import GeoMap
from drawlib._smartarts._geomap._loader import load_geodata, parse_geojson_dict
from drawlib._smartarts._geomap._projection import GeoProjection, clip_ring_to_bbox
from drawlib._smartarts._geomap._types import (
    Cities,
    Countries,
    GeoData,
    GeoElement,
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
    "GeoProjection",
    "GeoTarget",
    "World",
    "WorldPreset",
    "clip_ring_to_bbox",
    "load_geodata",
    "parse_geojson_dict",
]
