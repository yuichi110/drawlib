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

import csv
import hashlib
import io
import json
import re
import shutil
import unicodedata
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

WORLD_SHORT_NAMES: dict[str, str] = {
    "United States of America": "United States",
    "People's Republic of China": "China",
    "Democratic Republic of the Congo": "DR Congo",
    "Republic of the Congo": "Congo",
    "Federated States of Micronesia": "Micronesia",
    "Saint Vincent and the Grenadines": "Saint Vincent",
    "São Tomé and Príncipe": "Sao Tome and Principe",
    "Côte d'Ivoire": "Ivory Coast",
    "Curacao": "Curacao",
    "Curaçao": "Curacao",
    "Saint Barthélemy": "Saint Barthelemy",
    " Åland": "Aland",
    "Åland": "Aland",
}

COUNTRY_DEFAULT_RANGES: dict[str, tuple[tuple[float, float], tuple[float, float]]] = {
    "japan": ((127.0, 146.0), (26.0, 46.0)),
    "united_states": ((-126.0, -66.0), (24.0, 50.0)),
    "france": ((-5.5, 10.0), (41.0, 51.5)),
    "united_kingdom": ((-8.5, 2.2), (49.8, 61.0)),
    "netherlands": ((3.2, 7.3), (50.7, 53.6)),
    "spain": ((-9.5, 4.5), (35.8, 44.0)),
    "portugal": ((-9.6, -6.1), (36.8, 42.2)),
    "norway": ((4.0, 31.5), (57.8, 71.5)),
    "denmark": ((8.0, 15.3), (54.5, 58.0)),
    "russia": ((19.0, 180.0), (41.0, 82.0)),
    "new_zealand": ((166.0, 179.0), (-47.5, -34.0)),
    "chile": ((-76.0, -66.0), (-56.0, -17.0)),
    "ecuador": ((-81.5, -75.0), (-5.2, 1.6)),
    "australia": ((112.0, 154.5), (-44.0, -10.0)),
    "south_africa": ((16.0, 33.2), (-35.0, -22.0)),
    "kiribati": ((172.0, 177.0), (-3.0, 4.0)),
    "fiji": ((176.8, 180.0), (-21.0, -16.0)),
}

HK_DISTRICTS_EN: dict[str, str] = {
    "中西区": "Central and Western",
    "湾仔区": "Wan Chai",
    "东区": "Eastern",
    "南区": "Southern",
    "油尖旺区": "Yau Tsim Mong",
    "深水埗区": "Sham Shui Po",
    "九龙城区": "Kowloon City",
    "黄大仙区": "Wong Tai Sin",
    "观塘区": "Kwun Tong",
    "荃湾区": "Tsuen Wan",
    "屯门区": "Tuen Mun",
    "元朗区": "Yuen Long",
    "北区": "North",
    "大埔区": "Tai Po",
    "西贡区": "Sai Kung",
    "沙田区": "Sha Tin",
    "葵青区": "Kwai Tsing",
    "离岛区": "Islands",
}

SHANGHAI_DISTRICTS_EN: dict[str, str] = {
    "黄浦区": "Huangpu",
    "徐汇区": "Xuhui",
    "长宁区": "Changning",
    "静安区": "Jing'an",
    "普陀区": "Putuo",
    "虹口区": "Hongkou",
    "杨浦区": "Yangpu",
    "闵行区": "Minhang",
    "宝山区": "Baoshan",
    "嘉定区": "Jiading",
    "浦东新区": "Pudong",
    "金山区": "Jinshan",
    "松江区": "Songjiang",
    "青浦区": "Qingpu",
    "奉贤区": "Fengxian",
    "崇明区": "Chongming",
}

TAIPEI_DISTRICTS_EN: dict[str, str] = {
    "松山區": "Songshan",
    "信義區": "Xinyi",
    "大安區": "Da'an",
    "中山區": "Zhongshan",
    "中正區": "Zhongzheng",
    "大同區": "Datong",
    "萬華區": "Wanhua",
    "文山區": "Wenshan",
    "南港區": "Nangang",
    "內湖區": "Neihu",
    "士林區": "Shilin",
    "北投區": "Beitou",
}


def _to_ascii(text: str) -> str:
    """Strip diacritics and convert text to plain ASCII."""
    norm = unicodedata.normalize("NFKD", text)
    return "".join(c for c in norm if not unicodedata.combining(c))


def to_pascal_identifier(name: str) -> str:
    """Convert an English country/region name into a valid PascalCase Python identifier."""
    ascii_str = _to_ascii(name).replace("&", " And ")
    words = re.findall(r"[A-Za-z0-9]+", ascii_str)
    ident = "".join(w[0].upper() + w[1:] for w in words if w)
    return f"_{ident}" if ident and ident[0].isdigit() else (ident or "Unknown")


def to_snake_slug(name: str) -> str:
    """Convert an English country/region name into a lowercase snake_case filename slug."""
    ascii_str = _to_ascii(name).replace("&", " and ")
    words = re.findall(r"[A-Za-z0-9]+", ascii_str.lower())
    return "_".join(words) or "unknown"


# Hiragana -> Hepburn Romaji conversion for Japanese municipalities
_KANA_DIGRAPHS: dict[str, str] = {
    "きゃ": "kya", "きゅ": "kyu", "きょ": "kyo",
    "しゃ": "sha", "しゅ": "shu", "しょ": "sho",
    "ちゃ": "cha", "ちゅ": "chu", "ちょ": "cho",
    "にゃ": "nya", "にゅ": "nyu", "にょ": "nyo",
    "ひゃ": "hya", "ひゅ": "hyu", "ひょ": "hyo",
    "みゃ": "mya", "みゅ": "myu", "みょ": "myo",
    "りゃ": "rya", "りゅ": "ryu", "りょ": "ryo",
    "ぎゃ": "gya", "ぎゅ": "gyu", "ぎょ": "gyo",
    "じゃ": "ja", "じゅ": "ju", "じょ": "jo",
    "びゃ": "bya", "びゅ": "byu", "びょ": "byo",
    "ぴゃ": "pya", "ぴゅ": "pyu", "ぴょ": "pyo",
}

_KANA_MONOGRAPHS: dict[str, str] = {
    "あ": "a", "い": "i", "う": "u", "え": "e", "お": "o",
    "か": "ka", "き": "ki", "く": "ku", "け": "ke", "こ": "ko",
    "さ": "sa", "し": "shi", "す": "su", "せ": "se", "そ": "so",
    "た": "ta", "ち": "chi", "つ": "tsu", "て": "te", "と": "to",
    "な": "na", "に": "ni", "ぬ": "nu", "ね": "ne", "の": "no",
    "は": "ha", "ひ": "hi", "ふ": "fu", "へ": "he", "ほ": "ho",
    "ま": "ma", "み": "mi", "む": "mu", "め": "me", "も": "mo",
    "や": "ya", "ゆ": "yu", "よ": "yo",
    "ら": "ra", "り": "ri", "る": "ru", "れ": "re", "ろ": "ro",
    "わ": "wa", "ゐ": "i", "ゑ": "e", "を": "o", "ん": "n",
    "が": "ga", "ぎ": "gi", "ぐ": "gu", "げ": "ge", "ご": "go",
    "ざ": "za", "じ": "ji", "ず": "zu", "ぜ": "ze", "ぞ": "zo",
    "だ": "da", "ぢ": "ji", "づ": "zu", "で": "de", "ど": "do",
    "ば": "ba", "び": "bi", "ぶ": "bu", "べ": "be", "ぼ": "bo",
    "ぱ": "pa", "ぴ": "pi", "ぷ": "pu", "ぺ": "pe", "ぽ": "po",
    "ぁ": "a", "ぃ": "i", "ぅ": "u", "ぇ": "e", "ぉ": "o",
    "ー": "",
}


def _kana_to_romaji(kana: str) -> str:
    """Convert hiragana string into Hepburn romaji (compressing long o/u vowels)."""
    out: list[str] = []
    i = 0
    n = len(kana)
    while i < n:
        if kana[i] == "っ":
            if i + 1 < n:
                nxt = _KANA_DIGRAPHS.get(kana[i + 1 : i + 3]) or _KANA_MONOGRAPHS.get(kana[i + 1], "")
                if nxt:
                    out.append("t" if nxt.startswith("ch") else nxt[0])
            i += 1
            continue
        if i + 1 < n and kana[i : i + 2] in _KANA_DIGRAPHS:
            rom = _KANA_DIGRAPHS[kana[i : i + 2]]
            i += 2
        else:
            rom = _KANA_MONOGRAPHS.get(kana[i], kana[i])
            i += 1
        out.append(rom)

    joined = "".join(out)
    # Standardize long vowels in Japanese place names (e.g. kyouto -> kyoto, oosaka -> osaka, chuou -> chuo)
    joined = re.sub(r"ou", "o", joined)
    joined = re.sub(r"oo", "o", joined)
    joined = re.sub(r"uu", "u", joined)
    return joined.capitalize()


def _load_localgov_kana_map(csv_path: Path) -> dict[str, tuple[str, str]]:
    """Load JIS 5-digit municipality code -> (kanji_name, kana_name) from localgovjp-utf8.csv."""
    raw = csv_path.read_text(encoding="utf-8-sig")
    reader = csv.DictReader(io.StringIO(raw))
    mapping: dict[str, tuple[str, str]] = {}
    for row in reader:
        lgcode = (row.get("lgcode") or "").strip()
        if len(lgcode) >= 5:
            mapping[lgcode[:5]] = ((row.get("city") or "").strip(), (row.get("citykana") or "").strip())
    return mapping


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
    if name_en.strip().lower() == "hokkai do":
        return "Hokkaido"
    for suffix in (
        " To",
        " Fu",
        " Ken",
        " Ku",
        " Shi",
        " Machi",
        " Mura",
        "-to",
        "-fu",
        "-ken",
        "-ku",
        "-shi",
        "-gu",
    ):
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
        adm0_a3 = str(p.get("ADM0_A3") or p.get("GU_A3") or "")
        iso_a3 = str(p.get("ISO_A3") or "")
        if not iso_a3 or iso_a3 == "-99":
            eh_a3 = str(p.get("ISO_A3_EH") or "")
            iso_a3 = eh_a3 if eh_a3 == adm0_a3 else adm0_a3
        iso_a2 = str(p.get("ISO_A2") or "")
        if not iso_a2 or iso_a2 == "-99":
            eh_a3 = str(p.get("ISO_A3_EH") or "")
            iso_a2 = str(p.get("ISO_A2_EH") or "") if eh_a3 == adm0_a3 else ""

        name_full = str(p.get("NAME_EN") or p.get("NAME") or p.get("ADMIN") or adm0_a3)
        name_en = WORLD_SHORT_NAMES.get(name_full, name_full)
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

        feature_id = adm0_a3 if adm0_a3 and adm0_a3 != "-99" else name_en
        out_features.append(
            {
                "type": "Feature",
                "id": feature_id,
                "properties": {
                    "id": feature_id,
                    "iso_a2": iso_a2 if iso_a2 != "-99" else "",
                    "iso_a3": iso_a3 if iso_a3 != "-99" else "",
                    "name": name_en,
                    "name_full": name_full,
                    "name_ja": name_ja,
                    "region": region,
                    "subregion": subregion,
                    "center_lonlat": center_lonlat,
                },
                "geometry": _polygons_to_geojson_geometry(polys),
            }
        )

    out_features.sort(key=lambda f: str(f["properties"]["name"]))
    return {"type": "FeatureCollection", "features": out_features}


def normalize_japan_geojson(raw_data: dict[str, Any]) -> dict[str, Any]:
    """Normalize Japan 47 prefectures into clean countries/japan.geojson."""
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


def normalize_country_admin1_geojson(raw_features: list[dict[str, Any]]) -> dict[str, Any]:
    """Normalize a single country's Admin-1 state/province features into a clean FeatureCollection."""
    simplified_geoms = _topological_simplify_features(
        raw_features,
        epsilon=0.008,
        decimals=4,
        min_island_area=0.0002,
    )

    out_features: list[dict[str, Any]] = []
    seen_names: set[str] = set()
    for idx, (raw_f, polys) in enumerate(zip(raw_features, simplified_geoms, strict=True)):
        if not polys:
            continue
        p = raw_f.get("properties") or {}
        raw_name = str(p.get("name_en") or p.get("name") or p.get("gn_name") or f"Area_{idx + 1}").strip()
        name_en = _to_ascii(raw_name) if raw_name else f"Area_{idx + 1}"
        if not name_en:
            name_en = raw_name
        if name_en in seen_names:
            iso_suffix = str(p.get("iso_3166_2") or p.get("postal") or (idx + 1))
            name_en = f"{name_en} ({iso_suffix})"
        seen_names.add(name_en)

        name_ja = str(p.get("name_ja") or raw_name).strip()
        iso_code = str(p.get("iso_3166_2") or p.get("adm1_code") or "").strip()

        main_ring = _largest_exterior_ring(polys)
        center_lonlat = _ring_interior_center(main_ring, decimals=4)

        out_features.append(
            {
                "type": "Feature",
                "id": name_en,
                "properties": {
                    "id": name_en,
                    "iso_code": iso_code,
                    "name": name_en,
                    "name_full": raw_name,
                    "name_ja": name_ja,
                    "center_lonlat": center_lonlat,
                },
                "geometry": _polygons_to_geojson_geometry(polys),
            }
        )

    out_features.sort(key=lambda f: str(f["properties"]["name"]))
    return {"type": "FeatureCollection", "features": out_features}


def normalize_tokyo_geojson(raw_data: dict[str, Any]) -> dict[str, Any]:
    """Normalize Tokyo municipalities into clean cities/japan_tokyo.geojson."""
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
    seen_ids: set[str] = set()
    for raw_f, polys in zip(valid_features, simplified_geoms, strict=True):
        if not polys:
            continue
        p = raw_f.get("properties") or {}
        code = int(p["code"])
        name_full = str(p["ward_en"])
        name_en = _strip_en_suffix(name_full)
        if name_en in seen_ids:
            name_en = name_full
        seen_ids.add(name_en)
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


def _resolve_jp_municipality_romaji(
    code: str,
    n3: str,
    kana_full: str,
    seen_names: set[str],
) -> str:
    """Resolve Hepburn Romaji name for a Japanese municipality from its kana reading."""
    kana_parts = kana_full.split()
    if len(kana_parts) >= 2:
        city_kana, ward_kana = kana_parts[0], kana_parts[-1]
        for suf in ("し", "ぐん"):
            if city_kana.endswith(suf):
                city_kana = city_kana[: -len(suf)]
        for suf in ("く", "ちょう", "まち", "そん", "むら"):
            if ward_kana.endswith(suf):
                ward_kana = ward_kana[: -len(suf)]
        city_rom = _kana_to_romaji(city_kana)
        ward_rom = _kana_to_romaji(ward_kana)
        # For capital city wards (Osaka-shi, Kyoto-shi, Sapporo-shi), use ward name directly unless collision
        if n3 in {"大阪市", "京都市", "札幌市"} and ward_rom not in seen_names:
            return ward_rom
        return f"{city_rom} {ward_rom}" if city_rom != ward_rom else ward_rom

    if kana_parts:
        m_kana = kana_parts[0]
        for suf in ("し", "ちょう", "まち", "そん", "むら", "く"):
            if m_kana.endswith(suf) and len(m_kana) > len(suf):
                m_kana = m_kana[: -len(suf)]
                break
        return _kana_to_romaji(m_kana)

    return code


def normalize_jp_prefecture_municipalities(
    raw_data: dict[str, Any],
    localgov_map: dict[str, tuple[str, str]],
) -> dict[str, Any]:
    """Normalize MLIT N03 municipality GeoJSON (e.g. Kyoto, Osaka, Okinawa, Hokkaido)."""
    grouped_polys: dict[str, list[list[list[list[float]]]]] = defaultdict(list)
    grouped_props: dict[str, dict[str, Any]] = {}

    for feat in raw_data.get("features", []):
        p = feat.get("properties") or {}
        code = str(p.get("N03_007") or "").strip()
        if not code:
            continue
        grouped_props.setdefault(code, p)
        grouped_polys[code].extend(_extract_raw_polygons(feat.get("geometry") or {}))

    merged_features: list[dict[str, Any]] = [
        {
            "type": "Feature",
            "properties": grouped_props[code],
            "geometry": {"type": "MultiPolygon", "coordinates": grouped_polys[code]},
        }
        for code in sorted(grouped_polys.keys())
    ]

    simplified_geoms = _topological_simplify_features(
        merged_features,
        epsilon=0.0005,
        decimals=4,
        min_island_area=0.000005,
    )

    out_features: list[dict[str, Any]] = []
    seen_names: set[str] = set()
    for feat, polys in zip(merged_features, simplified_geoms, strict=True):
        if not polys:
            continue
        p = feat["properties"]
        code = str(p["N03_007"]).strip()
        n3 = str(p.get("N03_003") or "").strip()
        n4 = str(p.get("N03_004") or "").strip()
        full_ja = f"{n3}{n4}" if n3.endswith("市") else n4

        _, kana_full = localgov_map.get(code, (full_ja, ""))
        name_en = _resolve_jp_municipality_romaji(code, n3, kana_full, seen_names)
        if name_en in seen_names:
            name_en = f"{name_en} ({code})"
        seen_names.add(name_en)

        main_ring = _largest_exterior_ring(polys)
        center_lonlat = _ring_interior_center(main_ring, decimals=4)

        out_features.append(
            {
                "type": "Feature",
                "id": name_en,
                "properties": {
                    "id": name_en,
                    "code": int(code),
                    "name": name_en,
                    "name_full": full_ja,
                    "name_ja": full_ja,
                    "name_short_ja": _strip_jp_suffix(n4),
                    "center_lonlat": center_lonlat,
                },
                "geometry": _polygons_to_geojson_geometry(polys),
            }
        )

    return {"type": "FeatureCollection", "features": out_features}


def _decode_topojson_to_geojson(topo: dict[str, Any], obj_name: str, filter_fn: Any) -> dict[str, Any]:
    """Decode a TopoJSON object into a standard GeoJSON FeatureCollection."""
    tf = topo.get("transform") or {}
    scale = tf.get("scale", [1.0, 1.0])
    translate = tf.get("translate", [0.0, 0.0])
    raw_arcs = topo.get("arcs", [])

    decoded_arcs: list[list[list[float]]] = []
    for arc in raw_arcs:
        x, y = 0, 0
        pts: list[list[float]] = []
        for dx, dy in arc:
            x += dx
            y += dy
            pts.append([x * scale[0] + translate[0], y * scale[1] + translate[1]])
        decoded_arcs.append(pts)

    def decode_ring(arc_indices: list[int]) -> list[list[float]]:
        ring: list[list[float]] = []
        for idx in arc_indices:
            seg = decoded_arcs[idx] if idx >= 0 else list(reversed(decoded_arcs[~idx]))
            ring.extend(seg[1:] if ring else seg)
        return ring

    geoms = ((topo.get("objects") or {}).get(obj_name) or {}).get("geometries", [])
    features: list[dict[str, Any]] = []
    for g in geoms:
        props = g.get("properties") or {}
        if not filter_fn(props):
            continue
        g_type = g.get("type")
        arcs = g.get("arcs", [])
        if g_type == "Polygon":
            coords = [decode_ring(r) for r in arcs]
            geom = {"type": "Polygon", "coordinates": coords}
        elif g_type == "MultiPolygon":
            coords = [[decode_ring(r) for r in poly] for poly in arcs]
            geom = {"type": "MultiPolygon", "coordinates": coords}
        else:
            continue
        features.append({"type": "Feature", "properties": props, "geometry": geom})

    return {"type": "FeatureCollection", "features": features}


def normalize_generic_city_geojson(
    raw_data: dict[str, Any],
    *,
    name_key: str = "name",
    ja_key: str | None = None,
    en_map: dict[str, str] | None = None,
    strip_prefix: str | None = None,
    epsilon: float = 0.0005,
    decimals: int = 4,
) -> dict[str, Any]:
    """Normalize a city GeoJSON dataset into standard drawlib format."""
    raw_features = raw_data.get("features", [])
    simplified_geoms = _topological_simplify_features(
        raw_features,
        epsilon=epsilon,
        decimals=decimals,
        min_island_area=0.000005,
    )

    out_features: list[dict[str, Any]] = []
    seen_ids: set[str] = set()
    for idx, (raw_f, polys) in enumerate(zip(raw_features, simplified_geoms, strict=True)):
        if not polys:
            continue
        p = raw_f.get("properties") or {}
        raw_name = str(p.get(name_key) or p.get("name") or f"Area_{idx + 1}").strip()
        if en_map and raw_name in en_map:
            name_en = en_map[raw_name]
            name_ja = raw_name
        else:
            name_en = _strip_en_suffix(raw_name)
            if strip_prefix and name_en.startswith(strip_prefix):
                name_en = name_en[len(strip_prefix) :].strip()
            if name_en.isupper() and len(name_en) > 3:
                name_en = name_en.title()
            name_ja = str(p.get(ja_key) or raw_name).strip() if ja_key else raw_name

        if name_en in seen_ids:
            name_en = f"{name_en} ({idx + 1})"
        seen_ids.add(name_en)

        main_ring = _largest_exterior_ring(polys)
        center_lonlat = _ring_interior_center(main_ring, decimals=decimals)

        out_features.append(
            {
                "type": "Feature",
                "id": name_en,
                "properties": {
                    "id": name_en,
                    "name": name_en,
                    "name_full": raw_name,
                    "name_ja": name_ja,
                    "center_lonlat": center_lonlat,
                },
                "geometry": _polygons_to_geojson_geometry(polys),
            }
        )

    return {"type": "FeatureCollection", "features": out_features}


def _write_geojson(
    norm_obj: dict[str, Any],
    rel_path: str,
    dest_dir: Path,
    cache_dir: Path | None,
    files_meta: dict[str, Any],
    *,
    category: str,
    enum_name: str,
    default_lon_range: tuple[float, float] | None = None,
    default_lat_range: tuple[float, float] | None = None,
) -> None:
    """Serialize normalized GeoJSON and record entry in files_meta."""
    compact_text = json.dumps(norm_obj, ensure_ascii=False, separators=(",", ":")) + "\n"
    out_bytes = compact_text.encode("utf-8")

    target_path = dest_dir / rel_path
    target_path.parent.mkdir(parents=True, exist_ok=True)
    target_path.write_bytes(out_bytes)

    if cache_dir is not None and cache_dir.resolve() != dest_dir.resolve():
        c_path = cache_dir / rel_path
        c_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(target_path, c_path)

    sha256 = hashlib.sha256(out_bytes).hexdigest()
    features_count = len(norm_obj.get("features", []))
    files_meta[rel_path] = {
        "category": category,
        "enum_name": enum_name,
        "features_count": features_count,
        "size_bytes": len(out_bytes),
        "sha256": sha256,
        "default_lon_range": list(default_lon_range) if default_lon_range else None,
        "default_lat_range": list(default_lat_range) if default_lat_range else None,
    }


def _normalize_all_countries(
    src_dir: Path,
    dest_dir: Path,
    cache_dir: Path | None,
    w50_raw: dict[str, Any],
    files_meta: dict[str, Any],
) -> None:
    """Normalize Japan and all Natural Earth 10m Admin-1 country maps."""
    print("[*] Normalizing Countries (Japan + Natural Earth 10m Admin-1) ...")
    jp_raw = json.loads((src_dir / "japan.geojson").read_text(encoding="utf-8"))
    jp_norm = normalize_japan_geojson(jp_raw)
    _write_geojson(
        jp_norm,
        "countries/japan.geojson",
        dest_dir,
        cache_dir,
        files_meta,
        category="countries",
        enum_name="Japan",
        default_lon_range=COUNTRY_DEFAULT_RANGES["japan"][0],
        default_lat_range=COUNTRY_DEFAULT_RANGES["japan"][1],
    )

    admin1_raw = json.loads((src_dir / "ne_10m_admin_1_states_provinces.geojson").read_text(encoding="utf-8"))
    admin1_by_a3: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for feat in admin1_raw.get("features", []):
        a3 = str((feat.get("properties") or {}).get("adm0_a3") or "")
        if a3:
            admin1_by_a3[a3].append(feat)

    seen_country_enums: set[str] = {"Japan"}
    for w_feat in w50_raw.get("features", []):
        wp = w_feat.get("properties") or {}
        a3 = str(wp.get("ADM0_A3") or wp.get("GU_A3") or "")
        if not a3 or a3 in {"JPN", "ATA"}:
            continue
        ftype = str(wp.get("TYPE") or "")
        pop = float(wp.get("POP_EST") or 0)
        if ftype not in {"Sovereign country", "Country", "Sovereignty"} and pop < 100000:
            continue

        raw_c_name = str(wp.get("NAME_EN") or wp.get("NAME") or wp.get("ADMIN") or a3)
        c_name = WORLD_SHORT_NAMES.get(raw_c_name, raw_c_name)
        enum_name = to_pascal_identifier(c_name)
        if enum_name in seen_country_enums:
            continue
        seen_country_enums.add(enum_name)

        slug = to_snake_slug(c_name)
        a1_feats = admin1_by_a3.get(a3) or [w_feat]
        c_norm = normalize_country_admin1_geojson(a1_feats)
        if not c_norm.get("features"):
            c_norm = normalize_country_admin1_geojson([w_feat])

        def_ranges = COUNTRY_DEFAULT_RANGES.get(slug)
        _write_geojson(
            c_norm,
            f"countries/{slug}.geojson",
            dest_dir,
            cache_dir,
            files_meta,
            category="countries",
            enum_name=enum_name,
            default_lon_range=def_ranges[0] if def_ranges else None,
            default_lat_range=def_ranges[1] if def_ranges else None,
        )


def _normalize_all_cities(
    src_dir: Path,
    dest_dir: Path,
    cache_dir: Path | None,
    files_meta: dict[str, Any],
) -> None:
    """Normalize all 16 flagship global city maps and custom GeoJSON sample files."""
    print("[*] Normalizing 16 flagship Cities ...")
    localgov_map = _load_localgov_kana_map(src_dir / "localgovjp-utf8.csv")

    tokyo_raw = json.loads((src_dir / "tokyo.geojson").read_text(encoding="utf-8"))
    _write_geojson(
        normalize_tokyo_geojson(tokyo_raw),
        "cities/japan_tokyo.geojson",
        dest_dir,
        cache_dir,
        files_meta,
        category="cities",
        enum_name="Japan_Tokyo",
        default_lon_range=(138.9, 139.95),
        default_lat_range=(35.5, 35.92),
    )

    for enum_name, slug, src_file in [
        ("Japan_Osaka", "japan_osaka", "jp_osaka.json"),
        ("Japan_Kyoto", "japan_kyoto", "jp_kyoto.json"),
    ]:
        raw_jp_city = json.loads((src_dir / src_file).read_text(encoding="utf-8"))
        _write_geojson(
            normalize_jp_prefecture_municipalities(raw_jp_city, localgov_map),
            f"cities/{slug}.geojson",
            dest_dir,
            cache_dir,
            files_meta,
            category="cities",
            enum_name=enum_name,
        )

    project_root = Path(__file__).resolve().parents[3]
    docs_assets_dir = project_root / "docs" / "docs_src" / "_assets"
    if docs_assets_dir.is_dir():
        docs_geodata_dir = docs_assets_dir / "geodata"
        docs_geodata_dir.mkdir(parents=True, exist_ok=True)
        for sample_name, sample_src in [
            ("okinawa.geojson", "jp_okinawa.json"),
            ("hokkaido.geojson", "jp_hokkaido.json"),
        ]:
            sample_raw = json.loads((src_dir / sample_src).read_text(encoding="utf-8"))
            sample_norm = normalize_jp_prefecture_municipalities(sample_raw, localgov_map)
            (docs_geodata_dir / sample_name).write_text(
                json.dumps(sample_norm, ensure_ascii=False, separators=(",", ":")) + "\n",
                encoding="utf-8",
            )

    city_configs: list[tuple[str, str, str, dict[str, Any], tuple[float, float] | None, tuple[float, float] | None]] = [
        ("UnitedStates_NewYork", "united_states_new_york", "us_new_york.geojson", {"name_key": "name"}, None, None),
        (
            "UnitedStates_SanFrancisco",
            "united_states_san_francisco",
            "us_san_francisco.geojson",
            {"name_key": "name"},
            (-122.53, -122.35),
            (37.70, 37.84),
        ),
        (
            "UnitedStates_LosAngeles",
            "united_states_los_angeles",
            "us_los_angeles.geojson",
            {"name_key": "name"},
            None,
            None,
        ),
        ("UnitedKingdom_London", "united_kingdom_london", "uk_london.geojson", {"name_key": "name"}, None, None),
        ("France_Paris", "france_paris", "fr_paris.geojson", {"name_key": "name"}, None, None),
        ("Germany_Berlin", "germany_berlin", "de_berlin.geojson", {"name_key": "name"}, None, None),
        ("Italy_Rome", "italy_rome", "it_rome.geojson", {"name_key": "name"}, None, None),
        (
            "SouthKorea_Seoul",
            "south_korea_seoul",
            "kr_seoul.json",
            {"name_key": "name_eng", "ja_key": "name"},
            None,
            None,
        ),
        ("Singapore_Singapore", "singapore_singapore", "sg_singapore.geojson", {"name_key": "name"}, None, None),
        (
            "China_HongKong",
            "china_hong_kong",
            "cn_hong_kong.json",
            {"name_key": "name", "en_map": HK_DISTRICTS_EN},
            None,
            None,
        ),
        (
            "China_Shanghai",
            "china_shanghai",
            "cn_shanghai.json",
            {"name_key": "name", "en_map": SHANGHAI_DISTRICTS_EN},
            None,
            None,
        ),
    ]

    for enum_name, slug, src_file, kwargs, lon_r, lat_r in city_configs:
        raw_c = json.loads((src_dir / src_file).read_text(encoding="utf-8"))
        norm_c = normalize_generic_city_geojson(raw_c, **kwargs)
        _write_geojson(
            norm_c,
            f"cities/{slug}.geojson",
            dest_dir,
            cache_dir,
            files_meta,
            category="cities",
            enum_name=enum_name,
            default_lon_range=lon_r,
            default_lat_range=lat_r,
        )

    tw_raw = json.loads((src_dir / "tw_towns.geo.json").read_text(encoding="utf-8"))
    taipei_feats = [
        f
        for f in tw_raw.get("features", [])
        if (f.get("properties") or {}).get("COUNTYNAME") in {"台北市", "臺北市"}
    ]
    taipei_norm = normalize_generic_city_geojson(
        {"type": "FeatureCollection", "features": taipei_feats},
        name_key="TOWNNAME",
        en_map=TAIPEI_DISTRICTS_EN,
    )
    _write_geojson(
        taipei_norm,
        "cities/taiwan_taipei.geojson",
        dest_dir,
        cache_dir,
        files_meta,
        category="cities",
        enum_name="Taiwan_Taipei",
    )

    au_topo = json.loads((src_dir / "au_sa4.topo.json").read_text(encoding="utf-8"))
    sydney_raw = _decode_topojson_to_geojson(
        au_topo,
        "ABS_SA4_2011",
        lambda p: p.get("GCC_NAME11") == "Greater Sydney",
    )
    sydney_norm = normalize_generic_city_geojson(
        sydney_raw,
        name_key="SA4_NAME11",
        strip_prefix="Sydney - ",
    )
    _write_geojson(
        sydney_norm,
        "cities/australia_sydney.geojson",
        dest_dir,
        cache_dir,
        files_meta,
        category="cities",
        enum_name="Australia_Sydney",
    )


def normalize_all_maps(
    src_dir: Path,
    dest_dir: Path,
    cache_dir: Path | None = None,
) -> dict[str, Any]:
    """Normalize all raw map datasets from src_dir into dest_dir (and cache_dir)."""
    dest_dir.mkdir(parents=True, exist_ok=True)
    if cache_dir is not None:
        cache_dir.mkdir(parents=True, exist_ok=True)

    for legacy in ("world.geojson", "japan.geojson", "tokyo.geojson"):
        for d in (dest_dir, cache_dir):
            if d is not None and (d / legacy).is_file():
                (d / legacy).unlink()

    files_meta: dict[str, Any] = {}

    print("[*] Normalizing world/world.geojson ...")
    w50_raw = json.loads((src_dir / "ne_50m_admin_0_countries.geojson").read_text(encoding="utf-8"))
    world_norm = normalize_world_geojson(w50_raw)
    _write_geojson(
        world_norm,
        "world/world.geojson",
        dest_dir,
        cache_dir,
        files_meta,
        category="world",
        enum_name="All",
        default_lon_range=(-180.0, 180.0),
        default_lat_range=(-60.0, 84.0),
    )

    _normalize_all_countries(src_dir, dest_dir, cache_dir, w50_raw, files_meta)
    _normalize_all_cities(src_dir, dest_dir, cache_dir, files_meta)

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
    return manifest
