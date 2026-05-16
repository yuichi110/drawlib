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
import urllib.request

from drawlib.v0_2.private.l1_core import (
    FONT_DIR_PATH,
    FONT_ICON_DIR_PATH,
    guarded,
    logger,
)


@guarded
def download_all_fonts() -> None:
    """Download all fonts."""
    raise NotImplementedError("Not implemented yet")


@guarded
def purge_font_cache() -> None:
    """Delete downloaded font file cache."""
    for dir_path in [FONT_DIR_PATH, FONT_ICON_DIR_PATH]:
        for file_name in os.listdir(dir_path):
            if file_name == "__init__.py":
                continue

            file_path = os.path.join(dir_path, file_name)
            if os.path.isfile(file_path):
                os.remove(file_path)
            else:
                shutil.rmtree(file_path)
