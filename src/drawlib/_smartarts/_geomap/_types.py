# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Data models and preset target enumerations for drawlib.smartarts.GeoMap."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from pydantic import BaseModel, ConfigDict

from drawlib._smartarts._geomap._presets import (
    PRESET_DEFAULT_RANGES,
    Cities,
    Countries,
    World,
)

WorldPreset = World

GeoTarget = World | type[World] | Countries | Cities | str | Path | dict[str, Any]


class GeoPolygon(BaseModel):
    """A single closed polygon region with an exterior ring and optional interior holes.

    Attributes:
        exterior: Closed ring of (lon, lat) coordinate tuples forming the outer boundary.
        holes: Tuple of closed rings of (lon, lat) coordinate tuples forming interior holes.
    """

    model_config = ConfigDict(frozen=True)

    exterior: tuple[tuple[float, float], ...]
    holes: tuple[tuple[tuple[float, float], ...], ...] = ()


class GeoElement(BaseModel):
    """A single named geographical area (country, prefecture, ward, or custom region).

    Attributes:
        id: Canonical identifier returned by ``get_areas()`` (e.g. ``"Japan"``, ``"Tokyo"``, ``"Chiyoda"``).
        name: Display name in English.
        name_ja: Display name in Japanese, if available.
        aliases: Lowercase lookup aliases (ISO codes, full/short names in EN/JA).
        polygons: Tuple of ``GeoPolygon`` instances making up this area.
        center_lonlat: Representative interior ``(lon, lat)`` coordinate on the primary landmass.
        bbox: Bounding box tuple ``(min_lon, min_lat, max_lon, max_lat)``.
        properties: Original GeoJSON feature properties dictionary.
    """

    model_config = ConfigDict(frozen=True)

    id: str
    name: str
    name_ja: str = ""
    aliases: tuple[str, ...] = ()
    polygons: tuple[GeoPolygon, ...]
    center_lonlat: tuple[float, float]
    bbox: tuple[float, float, float, float]
    properties: dict[str, Any] = {}


class GeoData(BaseModel):
    """Normalized collection of geographical elements loaded from GeoJSON.

    Attributes:
        name: Dataset identifier (e.g. ``"world:all"``, ``"countries/japan"``, ``"cities/japan_tokyo"``).
        elements: Mapping from canonical element ID to ``GeoElement``.
        bbox: Overall bounding box ``(min_lon, min_lat, max_lon, max_lat)``.
        default_lon_range: Recommended default longitude viewport range ``(min_lon, max_lon)``.
        default_lat_range: Recommended default latitude viewport range ``(min_lat, max_lat)``.
    """

    model_config = ConfigDict(frozen=True)

    name: str
    elements: dict[str, GeoElement]
    bbox: tuple[float, float, float, float]
    default_lon_range: tuple[float, float] | None = None
    default_lat_range: tuple[float, float] | None = None


__all__ = [
    "PRESET_DEFAULT_RANGES",
    "Cities",
    "Countries",
    "GeoData",
    "GeoElement",
    "GeoPolygon",
    "GeoTarget",
    "World",
    "WorldPreset",
]
