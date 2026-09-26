# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""SQLite-backed build image cache (.drawlib/cache.db) for drawlib build commands."""

from __future__ import annotations

import hashlib
import os
import re
import sqlite3
import time
from typing import Optional

import matplotlib

from drawlib import LIB_VERSION

DEFAULT_CACHE_REL_PATH = os.path.join(".drawlib", "cache.db")
DEFAULT_MAX_CACHE_BYTES = 1024 * 1024 * 1024  # 1 GiB
SCHEMA_VERSION = "1"

_STRING_LITERAL_RE = re.compile(r"""['"]([^'"\n]{1,128}\.[a-zA-Z0-9]{1,8})['"]""")


def hash_text(text: str) -> str:
    """Compute SHA-256 hex digest of a UTF-8 string."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def hash_file(file_path: Optional[str]) -> str:
    """Compute SHA-256 hex digest of a file's contents, or empty string if None/missing."""
    if not file_path:
        return ""
    abs_path = os.path.abspath(file_path)
    if not os.path.isfile(abs_path):
        return ""
    h = hashlib.sha256()
    with open(abs_path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def _hash_referenced_local_assets(code: str, context_dir: Optional[str]) -> str:
    """Hash any local files in `context_dir` referenced as string literals inside `code`."""
    if not context_dir or not os.path.isdir(context_dir):
        return ""
    candidates = sorted(set(_STRING_LITERAL_RE.findall(code)))
    if not candidates:
        return ""
    parts: list[str] = []
    for rel_candidate in candidates:
        full = os.path.join(context_dir, rel_candidate)
        if os.path.isfile(full):
            parts.append(f"{rel_candidate}:{hash_file(full)}")
    return "|".join(parts)


class BuildImageCache:
    """SQLite-backed image cache storing PNG and WebP (normal + grid) blobs."""

    def __init__(
        self,
        db_path: Optional[str] = None,
        max_size_bytes: int = DEFAULT_MAX_CACHE_BYTES,
        enabled: bool = True,
        lib_version: Optional[str] = None,
        matplotlib_version: Optional[str] = None,
    ) -> None:
        """Initialize the SQLite build image cache.

        Args:
            db_path (Optional[str]): Path to SQLite file. Defaults to `.drawlib/cache.db` in CWD.
            max_size_bytes (int): Maximum total blob bytes before evicting oldest 50%. Defaults to 1 GiB.
            enabled (bool): Whether cache reads/writes are active. When False, no file or DB access occurs.
            lib_version (Optional[str]): Library version override (used for testing version upgrades).
            matplotlib_version (Optional[str]): Matplotlib version override (used for testing version upgrades).
        """
        self._enabled = enabled
        self._max_size_bytes = max_size_bytes
        self._lib_version = lib_version or LIB_VERSION
        self._matplotlib_version = (
            matplotlib_version if matplotlib_version is not None else getattr(matplotlib, "__version__", "")
        )
        resolved_path = db_path or DEFAULT_CACHE_REL_PATH
        self._db_path = os.path.abspath(resolved_path)

        if self._enabled:
            self._init_db_and_evict()

    @property
    def enabled(self) -> bool:
        """Return True if cache is enabled."""
        return self._enabled

    @property
    def db_path(self) -> str:
        """Return absolute path to the SQLite cache database file."""
        return self._db_path

    def _connect(self) -> sqlite3.Connection:
        parent = os.path.dirname(self._db_path)
        if parent:
            os.makedirs(parent, exist_ok=True)
        conn = sqlite3.connect(self._db_path, timeout=30.0)
        conn.execute("PRAGMA journal_mode=WAL;")
        conn.execute("PRAGMA synchronous=NORMAL;")
        return conn

    @staticmethod
    def _create_image_table(conn: sqlite3.Connection) -> None:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS image_cache (
                cache_key            TEXT PRIMARY KEY,
                code_hash            TEXT NOT NULL,
                config_hash          TEXT NOT NULL,

                png_blob             BLOB,
                png_size_bytes       INTEGER NOT NULL DEFAULT 0,
                png_grid_blob        BLOB,
                png_grid_size_bytes  INTEGER NOT NULL DEFAULT 0,

                webp_blob            BLOB,
                webp_size_bytes      INTEGER NOT NULL DEFAULT 0,
                webp_grid_blob       BLOB,
                webp_grid_size_bytes INTEGER NOT NULL DEFAULT 0,

                total_size_bytes     INTEGER NOT NULL DEFAULT 0,

                created_at           REAL NOT NULL,
                last_accessed_at     REAL NOT NULL
            )
            """
        )
        conn.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_image_cache_last_accessed
                ON image_cache(last_accessed_at)
            """
        )

    def _init_db_and_evict(self) -> None:
        conn = self._connect()
        needs_vacuum = False
        try:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS cache_meta (
                    key   TEXT PRIMARY KEY,
                    value TEXT NOT NULL
                )
                """
            )
            cur = conn.execute("SELECT value FROM cache_meta WHERE key = 'lib_version'")
            row_ver = cur.fetchone()
            stored_ver = row_ver[0] if row_ver else None

            cur_mpl = conn.execute("SELECT value FROM cache_meta WHERE key = 'matplotlib_version'")
            row_mpl = cur_mpl.fetchone()
            stored_mpl = row_mpl[0] if row_mpl else None

            cur_schema = conn.execute("SELECT value FROM cache_meta WHERE key = 'schema_version'")
            row_schema = cur_schema.fetchone()
            stored_schema = row_schema[0] if row_schema else None

            if (
                stored_ver != self._lib_version
                or stored_mpl != self._matplotlib_version
                or stored_schema != SCHEMA_VERSION
            ):
                conn.execute("DROP TABLE IF EXISTS image_cache")
                self._create_image_table(conn)
                conn.execute(
                    "INSERT OR REPLACE INTO cache_meta (key, value) VALUES ('lib_version', ?)",
                    (self._lib_version,),
                )
                conn.execute(
                    "INSERT OR REPLACE INTO cache_meta (key, value) VALUES ('matplotlib_version', ?)",
                    (self._matplotlib_version,),
                )
                conn.execute(
                    "INSERT OR REPLACE INTO cache_meta (key, value) VALUES ('schema_version', ?)",
                    (SCHEMA_VERSION,),
                )
                conn.commit()
                if stored_ver is not None or stored_mpl is not None:
                    needs_vacuum = True
            else:
                self._create_image_table(conn)
                conn.commit()

            # Check total size and evict oldest 50% if exceeding max_size_bytes
            cur_size = conn.execute("SELECT COALESCE(SUM(total_size_bytes), 0), COUNT(*) FROM image_cache")
            total_bytes, total_rows = cur_size.fetchone()
            if int(total_bytes) > self._max_size_bytes and int(total_rows) > 0:
                delete_count = max(1, int(total_rows) // 2)
                conn.execute(
                    """
                    DELETE FROM image_cache
                    WHERE cache_key IN (
                        SELECT cache_key FROM image_cache
                        ORDER BY last_accessed_at ASC, created_at ASC
                        LIMIT ?
                    )
                    """,
                    (delete_count,),
                )
                conn.commit()
                needs_vacuum = True

            if needs_vacuum:
                conn.execute("VACUUM")
        finally:
            conn.close()

    @staticmethod
    def compute_keys(
        code: str,
        config_hash: str = "",
        context_dir: Optional[str] = None,
    ) -> tuple[str, str]:
        """Compute `(cache_key, code_hash)` for a given code block, config hash, and local asset context."""
        code_hash = hash_text(code)
        asset_hash = _hash_referenced_local_assets(code, context_dir)
        composite = f"{code_hash}:{config_hash}:{asset_hash}"
        cache_key = hash_text(composite)
        return cache_key, code_hash

    def get(
        self,
        cache_key: str,
        image_format: str = "png",
    ) -> Optional[tuple[bytes, Optional[bytes]]]:
        """Retrieve `(image_blob, grid_blob)` for `cache_key` and `image_format`, updating `last_accessed_at`.

        Returns:
            Optional[tuple[bytes, Optional[bytes]]]: `(normal_bytes, grid_bytes_or_none)` on hit, or `None` on miss.
        """
        if not self._enabled:
            return None

        fmt = "webp" if image_format.lower() == "webp" else "png"
        blob_col = "webp_blob" if fmt == "webp" else "png_blob"
        grid_col = "webp_grid_blob" if fmt == "webp" else "png_grid_blob"

        conn = self._connect()
        try:
            cur = conn.execute(
                f"SELECT {blob_col}, {grid_col} FROM image_cache WHERE cache_key = ? AND {blob_col} IS NOT NULL",  # noqa: S608
                (cache_key,),
            )
            row = cur.fetchone()
            if row is None or row[0] is None:
                return None

            now = time.time()
            conn.execute(
                "UPDATE image_cache SET last_accessed_at = ? WHERE cache_key = ?",
                (now, cache_key),
            )
            conn.commit()

            normal_bytes = bytes(row[0])
            grid_bytes = bytes(row[1]) if row[1] is not None else None
            return normal_bytes, grid_bytes
        finally:
            conn.close()

    def put(
        self,
        cache_key: str,
        code_hash: str,
        config_hash: str,
        image_format: str,
        image_blob: bytes,
        grid_blob: Optional[bytes] = None,
    ) -> None:
        """Insert or update cached image and optional grid blobs for `cache_key` and `image_format`."""
        if not self._enabled:
            return

        fmt = "webp" if image_format.lower() == "webp" else "png"
        blob_size = len(image_blob)
        grid_size = len(grid_blob) if grid_blob is not None else 0
        now = time.time()

        conn = self._connect()
        try:
            cur = conn.execute("SELECT 1 FROM image_cache WHERE cache_key = ?", (cache_key,))
            exists = cur.fetchone() is not None

            if not exists:
                if fmt == "webp":
                    conn.execute(
                        """
                        INSERT INTO image_cache (
                            cache_key, code_hash, config_hash,
                            webp_blob, webp_size_bytes, webp_grid_blob, webp_grid_size_bytes,
                            total_size_bytes, created_at, last_accessed_at
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """,
                        (
                            cache_key,
                            code_hash,
                            config_hash,
                            image_blob,
                            blob_size,
                            grid_blob,
                            grid_size,
                            blob_size + grid_size,
                            now,
                            now,
                        ),
                    )
                else:
                    conn.execute(
                        """
                        INSERT INTO image_cache (
                            cache_key, code_hash, config_hash,
                            png_blob, png_size_bytes, png_grid_blob, png_grid_size_bytes,
                            total_size_bytes, created_at, last_accessed_at
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """,
                        (
                            cache_key,
                            code_hash,
                            config_hash,
                            image_blob,
                            blob_size,
                            grid_blob,
                            grid_size,
                            blob_size + grid_size,
                            now,
                            now,
                        ),
                    )
            elif fmt == "webp":
                conn.execute(
                    """
                        UPDATE image_cache
                        SET webp_blob = ?,
                            webp_size_bytes = ?,
                            webp_grid_blob = ?,
                            webp_grid_size_bytes = ?,
                            total_size_bytes = png_size_bytes + png_grid_size_bytes + ? + ?,
                            last_accessed_at = ?
                        WHERE cache_key = ?
                        """,
                    (
                        image_blob,
                        blob_size,
                        grid_blob,
                        grid_size,
                        blob_size,
                        grid_size,
                        now,
                        cache_key,
                    ),
                )
            else:
                conn.execute(
                    """
                        UPDATE image_cache
                        SET png_blob = ?,
                            png_size_bytes = ?,
                            png_grid_blob = ?,
                            png_grid_size_bytes = ?,
                            total_size_bytes = ? + ? + webp_size_bytes + webp_grid_size_bytes,
                            last_accessed_at = ?
                        WHERE cache_key = ?
                        """,
                    (
                        image_blob,
                        blob_size,
                        grid_blob,
                        grid_size,
                        blob_size,
                        grid_size,
                        now,
                        cache_key,
                    ),
                )
            conn.commit()
        finally:
            conn.close()
