# Copyright (c) 2024 Yuichi Ito (yuichi@yuichi.com)
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

from drawlib.v0_1.private.logging import logger


def download_if_not_exist(file_path: str, download_url: str, md5_hash: str) -> None:
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

    Raises:
        RuntimeError: If any of the following conditions occur:
            - File download encounters an error.
            - Downloaded file is not saved properly.
            - Downloaded file's checksum does not match the expected MD5 hash.

    Returns:
        None

    Notes:
        - Creates the parent directory of file_path if it does not exist.
        - Uses MD5 checksum to verify the integrity of the downloaded file.
        - Utilizes urllib.request.urlopen for downloading the file.
        - Logs download progress and errors using the 'logger' instance from drawlib.v0_1.private.logging.

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

    # if file not exist or checksum has problem, try download
    logger.info('No font on local machine. Downloading from "%s".', download_url)
    download()

    # after download, check file exist and checksum
    if not is_file_exist():
        raise RuntimeError("File download completed. But not saved. Abort.")
    if not is_checksum_correct():
        raise RuntimeError("File download completed. But checksum has problem. Abort.")
    logger.info("Download completed without troubles.")
