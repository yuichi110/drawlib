# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Normalize raw GeoJSON maps from tools/original_assets/maps into clean drawlib GeoJSON assets."""

from __future__ import annotations

import hashlib
import json
import shutil
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

Point2D = tuple[float, float]
Ring2D = list[Point2D]
Polygon2D = list[Ring2D]

JAPAN_REGIONS_BY_CODE: dict[int, tuple[str, str]] = {
    1: ("Hokkaido", "北海道"),
    **{c: ("Tohoku", "東北") for c in range(2, 8)},
    **{c: ("Kanto", "関東") for c in range(8, 15)},
    **{c: ("Chubu", "中部") for c in range(15, 24)},
    **{c: ("Kansai", "関西") for c in range(24, 31)},
    **{c: ("Chugoku", "中国") for c in range(31, 36)},
    **{c: ("Shikoku", "四国") for c in range(36, 40)},
    **{c: ("Kyushu", "九州・沖縄") for c in range(40, 48)},
}

TOKYO_AREA_MAPPING: dict[str, tuple[str, str]] = {
    "Tokubu": ("23wards", "23区"),
    "Tama": ("tama", "多摩地域"),
    "Toushobu": ("islands", "島嶼部"),
}


def _rdp(points: list[Point2D], epsilon: float) -> list[Point2D]:
    """Simplify a 2D polyline using iterative Ramer-Douglas-Peucker."""
    if len(points) <= 2 or epsilon <= 0.0:
        return points

    stack: list[tuple[int, int]] = [(0, len(points) - 1)]
    keep = [False] * len(points)
    keep[0] = True
    keep[-1] = True
    eps_sq = epsilon * epsilon

    while stack:
        s, e = stack.pop()
        if e - s <= 1:
            continue
        x1, y1 = points[s]
        x2, y2 = points[e]
        dx, dy = x2 - x1, y2 - y1
        mag_sq = dx * dx + dy * dy
        max_d = -1.0
        idx = -1
        for i in range(s + 1, e):
            px, py = points[i]
            if mag_sq == 0.0:
                d = (px - x1) ** 2 + (py - y1) ** 2
            else:
                t = max(0.0, min(1.0, ((px - x1) * dx + (py - y1) * dy) / mag_sq))
                d = (px - (x1 + t * dx)) ** 2 + (py - (y1 + t * dy)) ** 2
            if d > max_d:
                max_d = d
                idx = i
        if max_d > eps_sq and idx != -1:
            keep[idx] = True
            stack.append((s, idx))
            stack.append((idx, e))

    return [pt for pt, k in zip(points, keep, strict=True) if k]


def _ring_signed_area(ring: Ring2D) -> float:
    """Compute signed planar area of a closed 2D ring."""
    area = 0.0
    for i in range(len(ring) - 1):
        x1, y1 = ring[i]
        x2, y2 = ring[i + 1]
        area += x1 * y2 - x2 * y1
    return area * 0.5


def _ring_area(ring: Ring2D) -> float:
    """Compute unsigned planar area of a closed 2D ring."""
    return abs(_ring_signed_area(ring))


def _ring_interior_center(ring: Ring2D, decimals: int = 4) -> list[float]:
    """Compute an interior representative coordinate [lon, lat] for a closed ring."""
    signed_a = _ring_signed_area(ring)
    if abs(signed_a) < 1e-12:
        xs = [p[0] for p in ring]
        ys = [p[1] for p in ring]
        return [round((min(xs) + max(xs)) / 2, decimals), round((min(ys) + max(ys)) / 2, decimals)]

    cx, cy = 0.0, 0.0
    for i in range(len(ring) - 1):
        x1, y1 = ring[i]
        x2, y2 = ring[i + 1]
        cross = x1 * y2 - x2 * y1
        cx += (x1 + x2) * cross
        cy += (y1 + y2) * cross
    cx /= 6.0 * signed_a
    cy /= 6.0 * signed_a

    # Intersect horizontal scanline y = cy to ensure point lies strictly inside land
    xs_int: list[float] = []
    for i in range(len(ring) - 1):
        x1, y1 = ring[i]
        x2, y2 = ring[i + 1]
        if (y1 <= cy < y2) or (y2 <= cy < y1):
            x_int = x1 + (cy - y1) * (x2 - x1) / (y2 - y1)
            xs_int.append(x_int)
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

    return [round(cx, decimals), round(cy, decimals)]


def _extract_raw_polygons(geometry: dict[str, Any]) -> list[list[list[list[float]]]]:
    """Extract normalized list of raw polygons from Polygon or MultiPolygon geometry."""
    g_type = geometry.get("type")
    coords = geometry.get("coordinates", [])
    if g_type == "Polygon":
        return [coords] if coords else []
    if g_type == "MultiPolygon":
        return coords
    return []


def _clean_ring(raw_ring: list[list[float]], decimals: int) -> Ring2D:
    """Round coordinates and remove consecutive duplicate points in a ring."""
    pts: Ring2D = [(round(float(p[0]), decimals), round(float(p[1]), decimals)) for p in raw_ring]
    if not pts:
        return []
    dedup: Ring2D = [pts[0]]
    for p in pts[1:]:
        if p != dedup[-1]:
            dedup.append(p)
    if dedup[0] != dedup[-1]:
        dedup.append(dedup[0])
    return dedup if len(dedup) >= 4 else []


def _clean_feature_polygons(
    feature: dict[str, Any],
    decimals: int,
    min_island_area: float,
) -> list[Polygon2D]:
    """Clean and filter rings for a single feature, keeping at least the largest polygon."""
    raw_polys = _extract_raw_polygons(feature.get("geometry") or {})
    candidates: list[tuple[float, Polygon2D]] = []
    for poly in raw_polys:
        if not poly:
            continue
        ext = _clean_ring(poly[0], decimals)
        if not ext:
            continue
        area = _ring_area(ext)
        holes = [
            h
            for h in (_clean_ring(raw_h, decimals) for raw_h in poly[1:])
            if h and _ring_area(h) >= min_island_area
        ]
        candidates.append((area, [ext, *holes]))

    if not candidates:
        return []

    candidates.sort(key=lambda item: item[0], reverse=True)
    return [poly for idx, (area, poly) in enumerate(candidates) if idx == 0 or area >= min_island_area]


def _simplify_canonical_arc(
    arc: Ring2D,
    epsilon: float,
    arc_cache: dict[tuple[Point2D, ...], list[Point2D]],
) -> Ring2D:
    """Simplify an arc between two junctions in canonical direction with caching."""
    u, v = arc[0], arc[-1]
    rev = u > v or (u == v and len(arc) > 2 and arc[1] > arc[-2])
    canon = tuple(reversed(arc)) if rev else tuple(arc)

    if canon not in arc_cache:
        if u == v and len(canon) >= 4:
            x0, y0 = canon[0]
            far = max(
                range(1, len(canon) - 1),
                key=lambda i: (canon[i][0] - x0) ** 2 + (canon[i][1] - y0) ** 2,
            )
            s1 = _rdp(list(canon[: far + 1]), epsilon)
            s2 = _rdp(list(canon[far:]), epsilon)
            arc_cache[canon] = s1[:-1] + s2
        else:
            arc_cache[canon] = _rdp(list(canon), epsilon)

    res = arc_cache[canon]
    return list(reversed(res)) if rev else list(res)


def _simplify_ring_with_junctions(
    ring: Ring2D,
    junctions: set[Point2D],
    epsilon: float,
    arc_cache: dict[tuple[Point2D, ...], list[Point2D]],
) -> Ring2D:
    """Split a closed ring at junction points and simplify each shared arc."""
    j_indices = [i for i, pt in enumerate(ring[:-1]) if pt in junctions]
    if not j_indices:
        return _simplify_canonical_arc(ring, epsilon, arc_cache)

    start = j_indices[0]
    rot = ring[start:-1] + ring[:start] + [ring[start]]
    j_rot = [i for i, pt in enumerate(rot[:-1]) if pt in junctions] + [len(rot) - 1]
    simp_ring: Ring2D = []
    for k in range(len(j_rot) - 1):
        arc = rot[j_rot[k] : j_rot[k + 1] + 1]
        s_arc = _simplify_canonical_arc(arc, epsilon, arc_cache)
        simp_ring.extend(s_arc[1:] if simp_ring else s_arc)
    return simp_ring


def _topological_simplify_features(
    features: list[dict[str, Any]],
    epsilon: float,
    decimals: int,
    min_island_area: float,
) -> list[list[Polygon2D]]:
    """Simplify feature polygons while preserving shared boundary topology."""
    neighbors: defaultdict[Point2D, set[Point2D]] = defaultdict(set)
    cleaned_geoms = [_clean_feature_polygons(f, decimals, min_island_area) for f in features]

    for f_polys in cleaned_geoms:
        for poly in f_polys:
            for ring in poly:
                for i in range(len(ring) - 1):
                    u, v = ring[i], ring[i + 1]
                    neighbors[u].add(v)
                    neighbors[v].add(u)

    junctions: set[Point2D] = {v for v, nbs in neighbors.items() if len(nbs) != 2}
    arc_cache: dict[tuple[Point2D, ...], list[Point2D]] = {}

    out_geoms: list[list[Polygon2D]] = []
    for f_polys in cleaned_geoms:
        out_polys: list[Polygon2D] = []
        for poly in f_polys:
            out_rings = [
                simp_ring
                for ring in poly
                if len(simp_ring := _simplify_ring_with_junctions(ring, junctions, epsilon, arc_cache)) >= 4
                and _ring_area(simp_ring) > 0
            ]
            if out_rings:
                out_polys.append(out_rings)
        if not out_polys and f_polys:
            out_polys.append(f_polys[0])
        out_geoms.append(out_polys)

    return out_geoms


def _polygons_to_geojson_geometry(polys: list[Polygon2D]) -> dict[str, Any]:
    """Convert internal Polygon2D list into GeoJSON Polygon or MultiPolygon dict."""
    serializable = [[[[pt[0], pt[1]] for pt in ring] for ring in poly] for poly in polys]
    if len(serializable) == 1:
        return {"type": "Polygon", "coordinates": serializable[0]}
    return {"type": "MultiPolygon", "coordinates": serializable}


def _largest_exterior_ring(polys: list[Polygon2D]) -> Ring2D:
    """Return the exterior ring with the largest planar area."""
    return max((poly[0] for poly in polys if poly), key=_ring_area)


def _strip_jp_suffix(name_ja: str) -> str:
    """Strip administrative suffix (都/府/県/区/市/町/村) while preserving 北海道."""
    if name_ja in {"北海道", "東京都", "京都府", "大阪府"}:
        return "北海道" if name_ja == "北海道" else name_ja[:-1]
    if len(name_ja) > 2 and name_ja[-1] in {"県", "区", "市", "町", "村"}:
        return name_ja[:-1]
    return name_ja


def _strip_en_suffix(name_en: str) -> str:
    """Strip administrative suffix (To, Fu, Ken, Ku, Shi, Machi, Mura) from English name."""
    for suffix in (" To", " Fu", " Ken", " Ku", " Shi", " Machi", " Mura", "-to", "-fu", "-ken"):
        if name_en.endswith(suffix):
            return name_en[: -len(suffix)].strip()
    return name_en.strip()


def normalize_world_geojson(raw_data: dict[str, Any]) -> dict[str, Any]:
    """Normalize Natural Earth 50m countries into clean world.geojson."""
    raw_features = raw_data.get("features", [])
    simplified_geoms = _topological_simplify_features(
        raw_features,
        epsilon=0.03,
        decimals=3,
        min_island_area=0.005,
    )

    out_features: list[dict[str, Any]] = []
    for raw_f, polys in zip(raw_features, simplified_geoms, strict=True):
        if not polys:
            continue
        p = raw_f.get("properties") or {}
        iso_a3 = str(p.get("ISO_A3") or "")
        if not iso_a3 or iso_a3 == "-99":
            iso_a3 = str(p.get("ISO_A3_EH") or p.get("ADM0_A3") or p.get("GU_A3") or "")
        iso_a2 = str(p.get("ISO_A2") or "")
        if not iso_a2 or iso_a2 == "-99":
            iso_a2 = str(p.get("ISO_A2_EH") or "")

        name_en = str(p.get("NAME_EN") or p.get("NAME") or p.get("ADMIN") or iso_a3)
        name_ja = str(p.get("NAME_JA") or name_en)
        region = str(p.get("CONTINENT") or "")
        subregion = str(p.get("SUBREGION") or "")

        main_ring = _largest_exterior_ring(polys)
        center_lonlat = _ring_interior_center(main_ring, decimals=3)
        if p.get("LABEL_X") is not None and p.get("LABEL_Y") is not None:
            lx, ly = float(p["LABEL_X"]), float(p["LABEL_Y"])
            xs = [pt[0] for pt in main_ring]
            ys = [pt[1] for pt in main_ring]
            if min(xs) <= lx <= max(xs) and min(ys) <= ly <= max(ys):
                center_lonlat = [round(lx, 3), round(ly, 3)]

        feature_id = iso_a3 if iso_a3 and iso_a3 != "-99" else name_en
        out_features.append(
            {
                "type": "Feature",
                "id": feature_id,
                "properties": {
                    "id": feature_id,
                    "iso_a2": iso_a2 if iso_a2 != "-99" else "",
                    "iso_a3": iso_a3 if iso_a3 != "-99" else "",
                    "name": name_en,
                    "name_ja": name_ja,
                    "region": region,
                    "subregion": subregion,
                    "center_lonlat": center_lonlat,
                },
                "geometry": _polygons_to_geojson_geometry(polys),
            }
        )

    out_features.sort(key=lambda f: str(f["id"]))
    return {"type": "FeatureCollection", "features": out_features}


def normalize_japan_geojson(raw_data: dict[str, Any]) -> dict[str, Any]:
    """Normalize Japan 47 prefectures into clean japan.geojson."""
    raw_features = sorted(
        raw_data.get("features", []),
        key=lambda f: int((f.get("properties") or {}).get("id", 99)),
    )
    simplified_geoms = _topological_simplify_features(
        raw_features,
        epsilon=0.004,
        decimals=4,
        min_island_area=0.0001,
    )

    out_features: list[dict[str, Any]] = []
    for raw_f, polys in zip(raw_features, simplified_geoms, strict=True):
        if not polys:
            continue
        p = raw_f.get("properties") or {}
        code = int(p.get("id", 0))
        name_full = str(p.get("nam") or "")
        name_en = _strip_en_suffix(name_full)
        name_ja = str(p.get("nam_ja") or "")
        name_short_ja = _strip_jp_suffix(name_ja)
        region_en, region_ja = JAPAN_REGIONS_BY_CODE.get(code, ("Other", "その他"))

        main_ring = _largest_exterior_ring(polys)
        center_lonlat = _ring_interior_center(main_ring, decimals=4)

        out_features.append(
            {
                "type": "Feature",
                "id": name_en,
                "properties": {
                    "id": name_en,
                    "code": code,
                    "iso_code": f"JP-{code:02d}",
                    "name": name_en,
                    "name_full": name_full,
                    "name_ja": name_ja,
                    "name_short_ja": name_short_ja,
                    "region": region_en,
                    "region_ja": region_ja,
                    "center_lonlat": center_lonlat,
                },
                "geometry": _polygons_to_geojson_geometry(polys),
            }
        )

    return {"type": "FeatureCollection", "features": out_features}


def normalize_tokyo_geojson(raw_data: dict[str, Any]) -> dict[str, Any]:
    """Normalize Tokyo municipalities into clean tokyo.geojson."""
    valid_features = [
        f
        for f in raw_data.get("features", [])
        if (f.get("properties") or {}).get("code") is not None
        and (f.get("properties") or {}).get("ward_en") is not None
    ]
    valid_features.sort(key=lambda f: int((f.get("properties") or {}).get("code", 0)))

    simplified_geoms = _topological_simplify_features(
        valid_features,
        epsilon=0.0005,
        decimals=4,
        min_island_area=0.000005,
    )

    out_features: list[dict[str, Any]] = []
    for raw_f, polys in zip(valid_features, simplified_geoms, strict=True):
        if not polys:
            continue
        p = raw_f.get("properties") or {}
        code = int(p["code"])
        name_full = str(p["ward_en"])
        name_en = _strip_en_suffix(name_full)
        name_ja = str(p.get("ward_ja") or "")
        name_short_ja = _strip_jp_suffix(name_ja)
        raw_area = str(p.get("area_en") or "")
        region_en, region_ja = TOKYO_AREA_MAPPING.get(raw_area, ("other", "その他"))

        main_ring = _largest_exterior_ring(polys)
        center_lonlat = _ring_interior_center(main_ring, decimals=4)

        out_features.append(
            {
                "type": "Feature",
                "id": name_en,
                "properties": {
                    "id": name_en,
                    "code": code,
                    "name": name_en,
                    "name_full": name_full,
                    "name_ja": name_ja,
                    "name_short_ja": name_short_ja,
                    "region": region_en,
                    "region_ja": region_ja,
                    "center_lonlat": center_lonlat,
                },
                "geometry": _polygons_to_geojson_geometry(polys),
            }
        )

    return {"type": "FeatureCollection", "features": out_features}


def normalize_all_maps(
    src_dir: Path,
    dest_dir: Path,
    cache_dir: Path | None = None,
) -> dict[str, Any]:
    """Normalize raw map datasets from src_dir and write clean GeoJSONs to dest_dir (and cache_dir).

    Args:
        src_dir: Source directory containing raw GeoJSONs (tools/original_assets/maps).
        dest_dir: Primary destination directory for normalized GeoJSONs.
        cache_dir: Optional secondary directory (e.g. src/drawlib/_cached_assets/maps) to sync.

    Returns:
        Manifest dictionary summarizing normalized map files.
    """
    dest_dir.mkdir(parents=True, exist_ok=True)
    if cache_dir is not None:
        cache_dir.mkdir(parents=True, exist_ok=True)

    tasks = [
        ("world.geojson", "ne_50m_admin_0_countries.geojson", normalize_world_geojson),
        ("japan.geojson", "japan.geojson", normalize_japan_geojson),
        ("tokyo.geojson", "tokyo.geojson", normalize_tokyo_geojson),
    ]

    files_meta: dict[str, Any] = {}
    for target_name, src_name, normalizer in tasks:
        src_path = src_dir / src_name
        if not src_path.exists():
            raise FileNotFoundError(f"Original map file not found: {src_path}")

        print(f"[*] Normalizing {src_name} -> {target_name} ...")
        raw_obj = json.loads(src_path.read_text(encoding="utf-8"))
        norm_obj = normalizer(raw_obj)

        compact_text = json.dumps(norm_obj, ensure_ascii=False, separators=(",", ":")) + "\n"
        out_bytes = compact_text.encode("utf-8")

        target_path = dest_dir / target_name
        target_path.write_bytes(out_bytes)
        if cache_dir is not None and cache_dir.resolve() != dest_dir.resolve():
            shutil.copy2(target_path, cache_dir / target_name)

        sha256 = hashlib.sha256(out_bytes).hexdigest()
        features_count = len(norm_obj.get("features", []))
        files_meta[target_name] = {
            "source_file": src_name,
            "features_count": features_count,
            "size_bytes": len(out_bytes),
            "sha256": sha256,
        }
        print(f"    -> Wrote {target_name} ({len(out_bytes):,} bytes, {features_count} features)")

    manifest: dict[str, Any] = {
        "format_version": "1.0",
        "provider": "maps",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "total_files": len(files_meta),
        "files": files_meta,
    }
    manifest_text = json.dumps(manifest, indent=2, ensure_ascii=False) + "\n"
    (dest_dir / "manifest.json").write_text(manifest_text, encoding="utf-8")
    if cache_dir is not None and cache_dir.resolve() != dest_dir.resolve():
        (cache_dir / "manifest.json").write_text(manifest_text, encoding="utf-8")

    print(f"[✓] Normalized {len(files_meta)} map files into {dest_dir}")
    if cache_dir is not None and cache_dir.resolve() != dest_dir.resolve():
        print(f"[✓] Synced normalized map files into {cache_dir}")
    return manifest
