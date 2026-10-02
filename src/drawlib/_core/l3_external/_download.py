# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Download assets implementations."""

import hashlib
import os

from drawlib._core.l1_core import logger
from drawlib._core.l3_external._package import ReleaseAssetPackage
from drawlib._release_assets import find_package_for_resource_path


def _find_package_for_file_path(file_path: str) -> ReleaseAssetPackage | None:
    """Identify matching ReleaseAssetPackage for a local file path if applicable.

    Args:
        file_path: File path to inspect.

    Returns:
        ReleaseAssetPackage | None: Matching package if matched, otherwise None.
    """
    normalized = file_path.replace("\\", "/").strip("/")
    if "/fonts/" in normalized:
        sub = "fonts/" + normalized.split("/fonts/", 1)[1]
        return find_package_for_resource_path(sub)
    if "/fonticons/" in normalized:
        sub = "fonticons/" + normalized.split("/fonticons/", 1)[1]
        return find_package_for_resource_path(sub)
    if "/icons/" in normalized:
        sub = "icons/" + normalized.split("/icons/", 1)[1]
        return find_package_for_resource_path(sub)
    if (
        normalized.startswith("fonts/")
        or normalized.startswith("fonticons/")
        or normalized.startswith("icons/")
    ):
        return find_package_for_resource_path(normalized)
    return None


def download_if_not_exist(
    file_path: str,
    download_url: str = "",
    md5_hash: str = "",
) -> None:
    """Download asset package if the asset file does not exist locally.

    Args:
        file_path (str): Local file path where the asset should exist.
        download_url (str): Deprecated / optional download URL.
        md5_hash (str): Optional expected MD5 checksum of the file.

    Raises:
        FileNotFoundError: If the asset package cannot be found for the given path.
        RuntimeError: If downloading or extracting the package fails.
    """
    def is_file_exist() -> bool:
        return os.path.exists(file_path)

    def is_checksum_correct() -> bool:
        if not md5_hash:
            return True
        md5_hash2 = hashlib.md5()  # noqa: S324
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                md5_hash2.update(chunk)
        return md5_hash2.hexdigest().lower() == md5_hash.strip().lower()

    # If file exists and checksum is correct, nothing to do
    if is_file_exist() and is_checksum_correct():
        return

    # Check if this asset belongs to a defined ReleaseAssetPackage
    pkg = _find_package_for_file_path(file_path)
    if pkg is None:
        raise FileNotFoundError(
            f"Asset file '{file_path}' does not exist locally and no release asset package matches it."
        )

    logger.info('Downloading release asset package "%s" from GitHub Releases...', pkg.name)
    pkg.download_and_extract()

    if not is_file_exist():
        raise RuntimeError(f"Asset package '{pkg.name}' downloaded, but file '{file_path}' was not found.")
    logger.info('Asset package "%s" downloaded and extracted successfully.', pkg.name)
