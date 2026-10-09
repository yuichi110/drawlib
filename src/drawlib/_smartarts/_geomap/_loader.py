# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""GeoJSON loader and normalization into GeoData models."""

from __future__ import annotations

import functools
import json
from pathlib import Path
from typing import Any, Final

from drawlib._core.l1_core import get_script_relative_path
from drawlib._core.l1_core._const import ASSETS_DIR_PATH
from drawlib._smartarts._geomap._types import (
    Cities,
    Countries,
    GeoData,
    GeoElement,
    GeoPolygon,
    GeoTarget,
    WorldPreset,
)

PRESET_DEFAULT_RANGES: Final[dict[str, tuple[tuple[float, float], tuple[float, float]]]] = {
    "world": ((-180.0, 180.0), (-60.0, 84.0)),
    "japan": ((127.0, 146.0), (26.0, 46.0)),
    "tokyo": ((138.9, 139.95), (35.5, 35.92)),
}

FALLBACK_ID_KEYS: Final[tuple[str, ...]] = (
    "name",
    "id",
    "NAME",
    "NAME_EN",
    "nam",
    "ward_en",
    "N03_004",
    "N03_001",
    "ISO_A3",
)


def _ring_signed_area(ring: tuple[tuple[float, float], ...]) -> float:
    """Compute signed planar area of a closed 2D ring."""
    area = 0.0
    for i in range(len(ring) - 1):
        x1, y1 = ring[i]
        x2, y2 = ring[i + 1]
        area += x1 * y2 - x2 * y1
    return area * 0.5


def _ring_interior_center(ring: tuple[tuple[float, float], ...]) -> tuple[float, float]:
    """Compute an interior representative coordinate (lon, lat) for a closed ring."""
    signed_a = _ring_signed_area(ring)
    if abs(signed_a) < 1e-12:
        xs = [p[0] for p in ring]
        ys = [p[1] for p in ring]
        return ((min(xs) + max(xs)) * 0.5, (min(ys) + max(ys)) * 0.5)

    cx, cy = 0.0, 0.0
    for i in range(len(ring) - 1):
        x1, y1 = ring[i]
        x2, y2 = ring[i + 1]
        cross = x1 * y2 - x2 * y1
        cx += (x1 + x2) * cross
        cy += (y1 + y2) * cross
    cx /= 6.0 * signed_a
    cy /= 6.0 * signed_a

    xs_int: list[float] = []
    for i in range(len(ring) - 1):
        x1, y1 = ring[i]
        x2, y2 = ring[i + 1]
        if (y1 <= cy < y2) or (y2 <= cy < y1):
            xs_int.append(x1 + (cy - y1) * (x2 - x1) / (y2 - y1))
    xs_int.sort()

    if len(xs_int) >= 2:
        inside = False
        best_mid = cx
        best_len = -1.0
        for k in range(0, len(xs_int) - 1, 2):
            x_l, x_r = xs_int[k], xs_int[k + 1]
            if x_l <= cx <= x_r:
                inside = True
                break
            if (x_r - x_l) > best_len:
                best_len = x_r - x_l
                best_mid = (x_l + x_r) * 0.5
        if not inside:
            cx = best_mid

    return (cx, cy)


def _normalize_ring(raw_ring: list[Any]) -> tuple[tuple[float, float], ...]:
    """Convert raw GeoJSON ring into a closed tuple of (lon, lat) float pairs."""
    if len(raw_ring) < 3:
        return ()
    pts = [(float(pt[0]), float(pt[1])) for pt in raw_ring]
    if pts[0] != pts[-1]:
        pts.append(pts[0])
    return tuple(pts) if len(pts) >= 4 else ()


def _parse_geometry_polygons(geometry: dict[str, Any] | None) -> tuple[GeoPolygon, ...]:
    """Parse GeoJSON Polygon or MultiPolygon geometry into a tuple of GeoPolygon."""
    if not geometry:
        return ()
    g_type = geometry.get("type")
    coords = geometry.get("coordinates") or []
    raw_polys: list[Any]
    if g_type == "Polygon":
        raw_polys = [coords] if coords else []
    elif g_type == "MultiPolygon":
        raw_polys = list(coords)
    else:
        return ()

    polygons: list[GeoPolygon] = []
    for raw_poly in raw_polys:
        if not raw_poly:
            continue
        ext = _normalize_ring(raw_poly[0])
        if not ext:
            continue
        holes = tuple(h for raw_h in raw_poly[1:] if (h := _normalize_ring(raw_h)))
        polygons.append(GeoPolygon(exterior=ext, holes=holes))
    return tuple(polygons)


def _resolve_feature_id_and_name(
    feature: dict[str, Any],
    props: dict[str, Any],
    idx: int,
    id_key: str | None,
    name_key: str | None,
) -> tuple[str, str]:
    """Determine canonical element ID and display name for a GeoJSON feature."""
    elem_id = ""
    if id_key and props.get(id_key) is not None:
        elem_id = str(props[id_key]).strip()
    if not elem_id:
        for key in FALLBACK_ID_KEYS:
            val = props.get(key)
            if val is not None and str(val).strip():
                elem_id = str(val).strip()
                break
    if not elem_id and feature.get("id") is not None:
        elem_id = str(feature["id"]).strip()
    if not elem_id:
        elem_id = f"element_{idx}"

    elem_name = elem_id
    if name_key and props.get(name_key) is not None:
        elem_name = str(props[name_key]).strip()
    elif props.get("name") is not None:
        elem_name = str(props["name"]).strip()

    return elem_id, elem_name


def _collect_feature_aliases(
    elem_id: str,
    elem_name: str,
    feature: dict[str, Any],
    props: dict[str, Any],
) -> tuple[str, ...]:
    """Build lowercase alias tuple for flexible element lookup."""
    alias_set: set[str] = {elem_id.lower(), elem_name.lower()}
    if feature.get("id") is not None:
        alias_set.add(str(feature["id"]).strip().lower())

    for key in (
        "id",
        "name",
        "name_full",
        "name_ja",
        "name_short_ja",
        "iso_a2",
        "iso_a3",
        "iso_code",
        "code",
        "nam",
        "nam_ja",
        "ward_en",
        "ward_ja",
    ):
        val = props.get(key)
        if val is not None:
            s_val = str(val).strip().lower()
            if s_val:
                alias_set.add(s_val)
    return tuple(sorted(alias_set))


def _build_geo_element(
    feature: dict[str, Any],
    idx: int,
    id_key: str | None,
    name_key: str | None,
) -> GeoElement | None:
    """Convert a single GeoJSON Feature dictionary into a GeoElement."""
    polygons = _parse_geometry_polygons(feature.get("geometry"))
    if not polygons:
        return None

    props = dict(feature.get("properties") or {})
    elem_id, elem_name = _resolve_feature_id_and_name(feature, props, idx, id_key, name_key)
    name_ja = str(props.get("name_ja") or props.get("nam_ja") or props.get("ward_ja") or "")
    group = str(props.get("region") or props.get("group") or props.get("CONTINENT") or "")
    group_ja = str(props.get("region_ja") or props.get("group_ja") or props.get("area_ja") or "")

    all_lons = [pt[0] for poly in polygons for pt in poly.exterior]
    all_lats = [pt[1] for poly in polygons for pt in poly.exterior]
    bbox = (min(all_lons), min(all_lats), max(all_lons), max(all_lats))

    raw_center = props.get("center_lonlat")
    if isinstance(raw_center, (list, tuple)) and len(raw_center) >= 2:
        center_lonlat = (float(raw_center[0]), float(raw_center[1]))
    else:
        largest_ring = max((poly.exterior for poly in polygons), key=lambda r: abs(_ring_signed_area(r)))
        center_lonlat = _ring_interior_center(largest_ring)

    aliases = _collect_feature_aliases(elem_id, elem_name, feature, props)
    return GeoElement(
        id=elem_id,
        name=elem_name,
        name_ja=name_ja,
        group=group,
        group_ja=group_ja,
        aliases=aliases,
        polygons=polygons,
        center_lonlat=center_lonlat,
        bbox=bbox,
        properties=props,
    )


def parse_geojson_dict(
    raw_obj: dict[str, Any],
    *,
    dataset_name: str = "custom",
    id_key: str | None = None,
    name_key: str | None = None,
) -> GeoData:
    """Parse a GeoJSON dictionary into a normalized GeoData object.

    Args:
        raw_obj: Parsed GeoJSON dictionary (FeatureCollection or single Feature).
        dataset_name: Logical dataset name.
        id_key: Optional property key to use as element identifier.
        name_key: Optional property key to use as element display name.

    Returns:
        Normalized GeoData instance.

    Raises:
        ValueError: If no valid polygon features are found in the GeoJSON data.
    """
    obj_type = raw_obj.get("type")
    if obj_type == "FeatureCollection":
        raw_features = list(raw_obj.get("features") or [])
    elif obj_type == "Feature":
        raw_features = [raw_obj]
    elif obj_type in {"Polygon", "MultiPolygon"}:
        raw_features = [{"type": "Feature", "properties": {}, "geometry": raw_obj}]
    else:
        raise ValueError(f"Unsupported GeoJSON root type: {obj_type!r}. Expected 'FeatureCollection' or 'Feature'.")

    elements: dict[str, GeoElement] = {}
    for idx, feat in enumerate(raw_features):
        elem = _build_geo_element(feat, idx, id_key, name_key)
        if elem is None:
            continue
        unique_id = elem.id
        if unique_id in elements and feat.get("id") is not None:
            unique_id = str(feat["id"])
            elem = elem.model_copy(update={"id": unique_id})
        elements[unique_id] = elem

    if not elements:
        raise ValueError(f"No valid Polygon or MultiPolygon features found in GeoJSON ({dataset_name}).")

    min_lon = min(e.bbox[0] for e in elements.values())
    min_lat = min(e.bbox[1] for e in elements.values())
    max_lon = max(e.bbox[2] for e in elements.values())
    max_lat = max(e.bbox[3] for e in elements.values())

    default_ranges = PRESET_DEFAULT_RANGES.get(dataset_name)
    default_lon_range = default_ranges[0] if default_ranges else None
    default_lat_range = default_ranges[1] if default_ranges else None

    return GeoData(
        name=dataset_name,
        elements=elements,
        bbox=(min_lon, min_lat, max_lon, max_lat),
        default_lon_range=default_lon_range,
        default_lat_range=default_lat_range,
    )


@functools.lru_cache(maxsize=16)
def _load_preset_geodata(preset_key: str) -> GeoData:
    """Load and cache a preset GeoJSON dataset from _cached_assets/maps/."""
    asset_path = Path(ASSETS_DIR_PATH) / "maps" / f"{preset_key}.geojson"
    if not asset_path.is_file():
        raise FileNotFoundError(
            f"Preset map asset '{preset_key}.geojson' not found at {asset_path}. "
            "Run './dcli codegen map' to generate cached map assets."
        )
    raw_obj = json.loads(asset_path.read_text(encoding="utf-8"))
    return parse_geojson_dict(raw_obj, dataset_name=preset_key)


def load_geodata(
    target: GeoTarget,
    *,
    id_key: str | None = None,
    name_key: str | None = None,
) -> GeoData:
    """Load GeoData from a preset enum, file path, GeoJSON dict, or __geo_interface__ object.

    Args:
        target: Preset map enum (World, Countries.Japan, Cities.Tokyo), file path, or GeoJSON dict.
        id_key: Optional property key for element IDs when loading custom GeoJSON.
        name_key: Optional property key for display names when loading custom GeoJSON.

    Returns:
        Loaded and normalized GeoData object.
    """
    if isinstance(target, (WorldPreset, Countries, Cities)):
        return _load_preset_geodata(target.value)

    if isinstance(target, dict):
        return parse_geojson_dict(target, dataset_name="custom_dict", id_key=id_key, name_key=name_key)

    geo_iface = getattr(target, "__geo_interface__", None)
    if isinstance(geo_iface, dict):
        return parse_geojson_dict(geo_iface, dataset_name="geo_interface", id_key=id_key, name_key=name_key)

    target_str = str(target).strip()
    if target_str.lower() in PRESET_DEFAULT_RANGES and not target_str.endswith((".geojson", ".json")):
        return _load_preset_geodata(target_str.lower())

    cand_path = Path(target_str)
    file_path = cand_path if cand_path.is_file() else Path(get_script_relative_path(target_str))
    if not file_path.is_file():
        raise FileNotFoundError(f"GeoJSON file not found: {target_str}")

    raw_obj = json.loads(file_path.read_text(encoding="utf-8"))
    return parse_geojson_dict(raw_obj, dataset_name=file_path.stem, id_key=id_key, name_key=name_key)


__all__ = [
    "load_geodata",
    "parse_geojson_dict",
]
