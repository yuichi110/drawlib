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
import urllib.request

from drawlib._core.l1_core import logger
from drawlib._release_assets import ReleaseAssetPackage, find_package_for_resource_path


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


def download_if_not_exist(file_path: str, download_url: str, md5_hash: str) -> None:  # noqa: C901
    """Download asset if it doesn't exist locally or corrupted.

    Download an asset file from the specified URL if it does not already exist locally,
    or if its MD5 checksum does not match the provided hash.

    Args:
        file_path (str):
            Local file path where the downloaded file will be saved or already exists.
        download_url (str):
            URL from which the file should be downloaded if it doesn't exist locally.
        md5_hash (str):
            Expected MD5 checksum of the file. If the file already exists locally,
            its checksum is compared against this value to determine if a re-download is necessary.

    Returns:
        None

    Raises:
        RuntimeError: If any of the following conditions occur:
            - File download encounters an error.
            - Downloaded file is not saved properly.
            - Downloaded file's checksum does not match the expected MD5 hash.

    Notes:
        - Creates the parent directory of file_path if it does not exist.
        - Uses MD5 checksum to verify the integrity of the downloaded file.
        - Utilizes urllib.request.urlopen for downloading the file.
        - Logs download progress and errors using the 'logger' instance from drawlib._core.logging.

    """

    def is_file_exist() -> bool:
        return os.path.exists(file_path)

    def is_checksum_correct() -> bool:
        md5_hash2 = hashlib.md5()  # noqa: S324
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                md5_hash2.update(chunk)

        return md5_hash2.hexdigest().lower() == md5_hash.strip().lower()

    def download() -> None:
        try:
            with urllib.request.urlopen(download_url) as response:  # noqa: S310
                # create parent directory
                directory = os.path.dirname(file_path)
                os.makedirs(directory, exist_ok=True)

                # save file
                with open(file_path, "wb") as fout:
                    data = response.read()
                    fout.write(data)

        except Exception as e:
            raise RuntimeError(f"File download error happens. {str(e)}") from e

    # if file exist and checksum ok, do nothing
    if is_file_exist():
        if is_checksum_correct():
            return

    # Check if this asset belongs to a defined ReleaseAssetPackage
    pkg = _find_package_for_file_path(file_path)
    if pkg is not None:
        logger.info('Downloading release asset package "%s" from GitHub Releases...', pkg.name)
        pkg.download_and_extract()
        if is_file_exist():
            logger.info('Asset package "%s" downloaded and extracted successfully.', pkg.name)
            return

    # if file not exist or checksum has problem, try legacy download
    logger.info('No font on local machine. Downloading from "%s".', download_url)
    download()

    # after download, check file exist and checksum
    if not is_file_exist():
        raise RuntimeError("File download completed. But not saved. Abort.")
    if not is_checksum_correct():
        raise RuntimeError("File download completed. But checksum has problem. Abort.")
    logger.info("Download completed without troubles.")
