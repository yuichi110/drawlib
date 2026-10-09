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
    """Configuration for an upstream raw GeoJSON dataset."""

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
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read()


def download_original_maps(output_dir: Path) -> dict[str, Any]:
    """Download all raw upstream GeoJSON map files into output_dir.

    Args:
        output_dir: Directory where raw GeoJSON files and manifest.json are written
            (e.g. tools/original_assets/maps).

    Returns:
        Dictionary representing the written manifest.json.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    sources_meta: dict[str, Any] = {}

    for src in MAP_SOURCES:
        print(f"[*] Downloading {src.key} from {src.url} ...")
        raw_bytes = _download_url(src.url)
        target_path = output_dir / src.file_name
        target_path.write_bytes(raw_bytes)

        obj = json.loads(raw_bytes)
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
        print(f"    -> Saved {target_path.name} ({len(raw_bytes):,} bytes, {features_count} features)")

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
