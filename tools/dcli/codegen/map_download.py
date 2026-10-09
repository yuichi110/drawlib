# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Module to download raw upstream GeoJSON map datasets into tools/original_assets/maps."""

from __future__ import annotations

import hashlib
import json
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, NamedTuple


class MapSource(NamedTuple):
    """Configuration for an upstream raw GeoJSON/TopoJSON/CSV dataset."""

    key: str
    url: str
    file_name: str
    license_name: str


MAP_SOURCES: list[MapSource] = [
    MapSource(
        key="world_110m",
        url="https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_110m_admin_0_countries.geojson",
        file_name="ne_110m_admin_0_countries.geojson",
        license_name="Public Domain (Natural Earth)",
    ),
    MapSource(
        key="world_50m",
        url="https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_50m_admin_0_countries.geojson",
        file_name="ne_50m_admin_0_countries.geojson",
        license_name="Public Domain (Natural Earth)",
    ),
    MapSource(
        key="world_admin1_10m",
        url="https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_10m_admin_1_states_provinces.geojson",
        file_name="ne_10m_admin_1_states_provinces.geojson",
        license_name="Public Domain (Natural Earth)",
    ),
    MapSource(
        key="japan",
        url="https://raw.githubusercontent.com/dataofjapan/land/master/japan.geojson",
        file_name="japan.geojson",
        license_name="National Land Numerical Information (MLIT Japan) / dataofjapan",
    ),
    MapSource(
        key="tokyo",
        url="https://raw.githubusercontent.com/dataofjapan/land/master/tokyo.geojson",
        file_name="tokyo.geojson",
        license_name="National Land Numerical Information (MLIT Japan) / dataofjapan",
    ),
    MapSource(
        key="jp_kyoto",
        url="https://raw.githubusercontent.com/smartnews-smri/japan-topography/main/data/municipality/geojson/s0010/N03-21_26_210101.json",
        file_name="jp_kyoto.json",
        license_name="National Land Numerical Information (MLIT Japan) / smartnews-smri",
    ),
    MapSource(
        key="jp_osaka",
        url="https://raw.githubusercontent.com/smartnews-smri/japan-topography/main/data/municipality/geojson/s0010/N03-21_27_210101.json",
        file_name="jp_osaka.json",
        license_name="National Land Numerical Information (MLIT Japan) / smartnews-smri",
    ),
    MapSource(
        key="jp_okinawa",
        url="https://raw.githubusercontent.com/smartnews-smri/japan-topography/main/data/municipality/geojson/s0010/N03-21_47_210101.json",
        file_name="jp_okinawa.json",
        license_name="National Land Numerical Information (MLIT Japan) / smartnews-smri",
    ),
    MapSource(
        key="jp_hokkaido",
        url="https://raw.githubusercontent.com/smartnews-smri/japan-topography/main/data/municipality/geojson/s0010/N03-21_01_210101.json",
        file_name="jp_hokkaido.json",
        license_name="National Land Numerical Information (MLIT Japan) / smartnews-smri",
    ),
    MapSource(
        key="jp_localgov_csv",
        url="https://raw.githubusercontent.com/codeforfukui/localgovjp/master/localgovjp-utf8.csv",
        file_name="localgovjp-utf8.csv",
        license_name="CC0 / Public Domain (codeforfukui/localgovjp)",
    ),
    MapSource(
        key="us_new_york",
        url="https://raw.githubusercontent.com/blackmad/neighborhoods/master/new-york-city-boroughs.geojson",
        file_name="us_new_york.geojson",
        license_name="Open Data NYC / blackmad/neighborhoods",
    ),
    MapSource(
        key="us_san_francisco",
        url="https://raw.githubusercontent.com/blackmad/neighborhoods/master/san-francisco.geojson",
        file_name="us_san_francisco.geojson",
        license_name="DataSF / blackmad/neighborhoods",
    ),
    MapSource(
        key="us_los_angeles",
        url="https://raw.githubusercontent.com/blackmad/neighborhoods/master/los-angeles.geojson",
        file_name="us_los_angeles.geojson",
        license_name="LA Times Mapping LA / blackmad/neighborhoods",
    ),
    MapSource(
        key="uk_london",
        url="https://raw.githubusercontent.com/blackmad/neighborhoods/master/london.geojson",
        file_name="uk_london.geojson",
        license_name="UK Open Government Licence / blackmad/neighborhoods",
    ),
    MapSource(
        key="fr_paris",
        url="https://raw.githubusercontent.com/blackmad/neighborhoods/master/paris.geojson",
        file_name="fr_paris.geojson",
        license_name="Open Data Paris / blackmad/neighborhoods",
    ),
    MapSource(
        key="de_berlin",
        url="https://raw.githubusercontent.com/funkeinteraktiv/Berlin-Geodaten/master/berlin_bezirke.geojson",
        file_name="de_berlin.geojson",
        license_name="Geoportal Berlin / funkeinteraktiv",
    ),
    MapSource(
        key="it_rome",
        url="https://raw.githubusercontent.com/blackmad/neighborhoods/master/rome-rioni.geojson",
        file_name="it_rome.geojson",
        license_name="Open Data Roma / blackmad/neighborhoods",
    ),
    MapSource(
        key="kr_seoul",
        url="https://raw.githubusercontent.com/southkorea/seoul-maps/master/kostat/2013/json/seoul_municipalities_geo_simple.json",
        file_name="kr_seoul.json",
        license_name="KOSTAT / southkorea/seoul-maps",
    ),
    MapSource(
        key="sg_singapore",
        url="https://raw.githubusercontent.com/yinshanyang/singapore/master/maps/2-planning-area.geojson",
        file_name="sg_singapore.geojson",
        license_name="Singapore Open Data / yinshanyang/singapore",
    ),
    MapSource(
        key="cn_hong_kong",
        url="https://geo.datav.aliyun.com/areas_v3/bound/810000_full.json",
        file_name="cn_hong_kong.json",
        license_name="DataV GeoAtlas",
    ),
    MapSource(
        key="cn_shanghai",
        url="https://geo.datav.aliyun.com/areas_v3/bound/310000_full.json",
        file_name="cn_shanghai.json",
        license_name="DataV GeoAtlas",
    ),
    MapSource(
        key="tw_towns",
        url="https://raw.githubusercontent.com/g0v/twgeojson/master/json/twTown1982.geo.json",
        file_name="tw_towns.geo.json",
        license_name="MIT / Taiwan Open Government Data (g0v/twgeojson)",
    ),
    MapSource(
        key="au_sa4",
        url="https://raw.githubusercontent.com/cartdeco/Australia-json-data/master/ABS_SA4_2011.json",
        file_name="au_sa4.topo.json",
        license_name="CC-BY ABS / cartdeco/Australia-json-data",
    ),
]


def _download_url(url: str) -> bytes:
    """Download raw bytes from a direct HTTP/HTTPS URL.

    Args:
        url: Target URL to download.

    Returns:
        Downloaded raw bytes.
    """
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0 (compatible; drawlib-asset-fetcher/1.0)"},
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        return resp.read()


def download_original_maps(output_dir: Path, *, force: bool = False) -> dict[str, Any]:
    """Download all raw upstream GeoJSON map files into output_dir.

    Args:
        output_dir: Directory where raw GeoJSON files and manifest.json are written
            (e.g. tools/original_assets/maps).
        force: Re-download files even if they already exist locally.

    Returns:
        Dictionary representing the written manifest.json.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    sources_meta: dict[str, Any] = {}

    for src in MAP_SOURCES:
        target_path = output_dir / src.file_name
        if target_path.exists() and not force:
            raw_bytes = target_path.read_bytes()
            print(f"[*] Using existing {src.file_name} ({len(raw_bytes):,} bytes)")
        else:
            print(f"[*] Downloading {src.key} from {src.url} ...")
            raw_bytes = _download_url(src.url)
            target_path.write_bytes(raw_bytes)
            print(f"    -> Saved {target_path.name} ({len(raw_bytes):,} bytes)")

        features_count = 0
        if src.file_name.endswith((".geojson", ".json")):
            obj = json.loads(raw_bytes)
            if obj.get("type") == "Topology":
                for o_val in (obj.get("objects") or {}).values():
                    features_count += len(o_val.get("geometries", []))
            else:
                features_count = len(obj.get("features", []))

        sha256 = hashlib.sha256(raw_bytes).hexdigest()
        sources_meta[src.key] = {
            "url": src.url,
            "file_name": src.file_name,
            "license": src.license_name,
            "sha256": sha256,
            "size_bytes": len(raw_bytes),
            "features_count": features_count,
        }

    manifest: dict[str, Any] = {
        "format_version": "1.0",
        "provider": "maps",
        "downloaded_at": datetime.now(timezone.utc).isoformat(),
        "sources": sources_meta,
    }
    manifest_path = output_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"[✓] Original map manifest saved to {manifest_path}")
    return manifest
