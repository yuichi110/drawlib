# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Cache management utilities for drawlib fonts and icons."""

from __future__ import annotations

from typing import Any, Dict, List

from drawlib._core.utils import download_all_assets, download_all_fonts, download_all_icons, purge_font_cache
from drawlib._release_assets import RELEASE_ASSET_PACKAGES


def clear_cache() -> None:
    """Delete all locally cached font and icon asset files."""
    purge_font_cache()


def list_cache() -> List[Dict[str, Any]]:
    """Inspect all downloadable font and icon packages and their local cache status.

    Returns:
        List[Dict[str, Any]]: List of package status dicts with keys
            'name', 'category', 'cached', 'file_count', and 'size_bytes'.
    """
    results: List[Dict[str, Any]] = []
    for pkg in RELEASE_ASSET_PACKAGES.values():
        cached_files = 0
        total_bytes = 0
        local_dir = pkg.get_local_dir()
        for rel_file in pkg.files:
            file_path = local_dir / rel_file
            if file_path.is_file():
                cached_files += 1
                total_bytes += file_path.stat().st_size

        is_cached = cached_files == len(pkg.files) and len(pkg.files) > 0
        results.append({
            "name": str(pkg.name),
            "category": pkg.category,
            "cached": is_cached,
            "file_count": f"{cached_files}/{len(pkg.files)}",
            "size_bytes": total_bytes,
        })
    return results


def download_cache(
    all_assets: bool = True,
    fonts: bool = False,
    icons: bool = False,
) -> None:
    """Pre-download font and/or icon packages into the local drawlib cache.

    Args:
        all_assets (bool): Download both fonts and icons (default True if neither fonts nor icons is set).
        fonts (bool): Download font packages only.
        icons (bool): Download icon packages only.
    """
    if fonts and not icons:
        download_all_fonts()
    elif icons and not fonts:
        download_all_icons()
    elif all_assets or (fonts and icons):
        download_all_assets()
    else:
        download_all_assets()
