# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Public cache management module for drawlib.tools."""

from __future__ import annotations

from drawlib._tools.cache_manager import clear_cache, download_cache, list_cache

clear = clear_cache
purge = clear_cache
list = list_cache  # noqa: A001
download = download_cache

__all__ = [
    "clear",
    "clear_cache",
    "download",
    "download_cache",
    "list",
    "list_cache",
    "purge",
]
