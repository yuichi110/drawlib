# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Font download module."""

import os
import shutil

from drawlib._core.l1_core import (
    FONT_DIR_PATH,
    FONT_ICON_DIR_PATH,
    ICON_DIR_PATH,
    RULES_DIR_PATH,
    logger,
)
from drawlib._release_assets import (
    RELEASE_ASSET_PACKAGES,
    download_all_release_assets,
)


def download_all_fonts() -> None:
    """Download all fonts from GitHub Releases."""
    for pkg in RELEASE_ASSET_PACKAGES.values():
        if pkg.category == "font":
            pkg.download_and_extract()


def download_all_icons() -> None:
    """Download all icon fonts from GitHub Releases."""
    for pkg in RELEASE_ASSET_PACKAGES.values():
        if pkg.category == "icon":
            pkg.download_and_extract()


def download_all_assets() -> None:
    """Download all fonts and icons from GitHub Releases."""
    download_all_release_assets()


def purge_font_cache() -> None:
    """Delete downloaded font, icon, and rules cache."""
    for dir_path in [FONT_DIR_PATH, FONT_ICON_DIR_PATH, ICON_DIR_PATH, RULES_DIR_PATH]:
        if not os.path.exists(dir_path):
            continue

        for file_name in os.listdir(dir_path):
            if file_name == "__init__.py":
                continue

            file_path = os.path.join(dir_path, file_name)
            if os.path.isfile(file_path):
                os.remove(file_path)
            else:
                shutil.rmtree(file_path)
