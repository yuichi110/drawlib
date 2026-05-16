# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Package for external asset downloading implementations."""

from drawlib.v0_2.private.l3_external._download import (
    download_if_not_exist,
)
from drawlib.v0_2.private.l3_external._font import (
    purge_font_cache,
)

__all__ = [
    # _download.py
    "download_if_not_exist",
    # _font.py
    "purge_font_cache",
]
