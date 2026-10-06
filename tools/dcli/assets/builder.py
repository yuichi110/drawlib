# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Deterministic ZIP builder for release asset packages."""

from __future__ import annotations

from pathlib import Path

from drawlib._release_assets import ReleaseAssetPackage, create_deterministic_zip_bytes


def build_package_zip(pkg: ReleaseAssetPackage, assets_root: Path) -> bytes:
    """Build byte-reproducible ZIP archive for a release asset package.

    Args:
        pkg: Release asset package definition.
        assets_root: Root directory of release assets, e.g. release_assets/v0.3.

    Returns:
        bytes: Binary ZIP data.
    """
    src_dir = assets_root / pkg.source_rel_path
    return create_deterministic_zip_bytes(src_dir, pkg.files)
