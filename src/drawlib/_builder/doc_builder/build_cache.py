# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""SQLite-backed build image cache (.drawlib/cache.db) for drawlib build commands.

Re-exported from drawlib._builder._common.cache for backwards compatibility.
"""

from __future__ import annotations

from drawlib._builder._common.cache import (
    DEFAULT_CACHE_REL_PATH,
    DEFAULT_MAX_CACHE_BYTES,
    SCHEMA_VERSION,
    BuildImageCache,
    CliImageCache,
    _hash_referenced_local_assets,
    hash_file,
    hash_text,
)

__all__ = [
    "DEFAULT_CACHE_REL_PATH",
    "DEFAULT_MAX_CACHE_BYTES",
    "SCHEMA_VERSION",
    "BuildImageCache",
    "CliImageCache",
    "_hash_referenced_local_assets",
    "hash_file",
    "hash_text",
]
