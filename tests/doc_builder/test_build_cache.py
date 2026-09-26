# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Unit and integration tests for BuildImageCache and --no-cache option in doc_builder."""

from __future__ import annotations

import os
import sqlite3
import time
from pathlib import Path

import pytest

from drawlib._builder.doc_builder.build_cache import (
    BuildImageCache,
    hash_file,
    hash_text,
)
from drawlib.tools.build import build_html, build_image, build_markdown, build_pdf


def test_build_cache_put_get_png_webp(tmp_path: Path) -> None:
    """Test storing and retrieving PNG and WebP blobs with companion grid blobs."""
    db_path = str(tmp_path / ".drawlib" / "cache.db")
    cache = BuildImageCache(db_path=db_path)

    key1 = "key_png_1"
    png_data = b"\x89PNG\r\n\x1a\nfake_png"
    grid_png_data = b"\x89PNG\r\n\x1a\nfake_grid_png"

    # Initially missing
    assert cache.get(key1, image_format="png") is None

    # Put PNG + grid
    cache.put(
        cache_key=key1,
        code_hash="code_1",
        config_hash="cfg_1",
        image_format="png",
        image_blob=png_data,
        grid_blob=grid_png_data,
    )

    # Hit
    retrieved = cache.get(key1, image_format="png")
    assert retrieved is not None
    assert retrieved[0] == png_data
    assert retrieved[1] == grid_png_data

    # Put WebP into same entry
    webp_data = b"RIFFfake_webp"
    cache.put(
        cache_key=key1,
        code_hash="code_1",
        config_hash="cfg_1",
        image_format="webp",
        image_blob=webp_data,
        grid_blob=None,
    )

    ret_webp = cache.get(key1, image_format="webp")
    assert ret_webp is not None
    assert ret_webp[0] == webp_data
    assert ret_webp[1] is None

    # PNG is still intact
    ret_png2 = cache.get(key1, image_format="png")
    assert ret_png2 is not None
    assert ret_png2[0] == png_data


def test_build_cache_lib_version_mismatch_drops_table(tmp_path: Path) -> None:
    """Test that if lib_version in cache_meta differs, image_cache is dropped and recreated."""
    db_path = str(tmp_path / ".drawlib" / "cache.db")
    cache_old = BuildImageCache(db_path=db_path, lib_version="0.1.0")
    cache_old.put(
        cache_key="k1",
        code_hash="c1",
        config_hash="",
        image_format="png",
        image_blob=b"data1",
    )
    assert cache_old.get("k1", image_format="png") is not None

    # Instantiate with newer lib_version -> image_cache is dropped and recreated
    cache_new = BuildImageCache(db_path=db_path, lib_version="0.2.0")
    assert cache_new.get("k1", image_format="png") is None

    # Check cache_meta
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("SELECT value FROM cache_meta WHERE key = 'lib_version'")
    assert cur.fetchone()[0] == "0.2.0"
    conn.close()


def test_build_cache_matplotlib_version_mismatch_drops_table(tmp_path: Path) -> None:
    """Test that if matplotlib_version in cache_meta differs, image_cache is dropped and recreated."""
    db_path = str(tmp_path / ".drawlib" / "cache.db")
    cache_old = BuildImageCache(db_path=db_path, matplotlib_version="3.8.0")
    cache_old.put(
        cache_key="k1",
        code_hash="c1",
        config_hash="",
        image_format="png",
        image_blob=b"data1",
    )
    assert cache_old.get("k1", image_format="png") is not None

    # Instantiate with newer matplotlib_version -> image_cache is dropped and recreated
    cache_new = BuildImageCache(db_path=db_path, matplotlib_version="3.9.0")
    assert cache_new.get("k1", image_format="png") is None

    # Check cache_meta has new matplotlib_version
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("SELECT value FROM cache_meta WHERE key = 'matplotlib_version'")
    assert cur.fetchone()[0] == "3.9.0"
    conn.close()


def test_build_cache_eviction_when_exceeding_max_bytes(tmp_path: Path) -> None:
    """Test that oldest 50% entries are evicted when total size exceeds max_size_bytes."""
    db_path = str(tmp_path / ".drawlib" / "cache.db")
    # Set small max_size_bytes of 300 bytes
    cache = BuildImageCache(db_path=db_path, max_size_bytes=300)

    # Insert 4 items of 100 bytes each (total 400 bytes)
    for i in range(1, 5):
        cache.put(
            cache_key=f"k{i}",
            code_hash=f"c{i}",
            config_hash="",
            image_format="png",
            image_blob=b"X" * 100,
        )
        time.sleep(0.01)

    # At initialization of next cache instance on same DB, eviction triggers
    cache_next = BuildImageCache(db_path=db_path, max_size_bytes=300)

    # Total 4 rows -> delete_count = max(1, 4 // 2) = 2. k1 and k2 (oldest) should be evicted
    assert cache_next.get("k1", image_format="png") is None
    assert cache_next.get("k2", image_format="png") is None
    assert cache_next.get("k3", image_format="png") is not None
    assert cache_next.get("k4", image_format="png") is not None


def test_build_cache_disabled_no_db_created(tmp_path: Path) -> None:
    """Test that BuildImageCache with enabled=False does not create or write to DB."""
    db_path = str(tmp_path / ".drawlib" / "cache.db")
    cache = BuildImageCache(db_path=db_path, enabled=False)

    cache.put(
        cache_key="k1",
        code_hash="c1",
        config_hash="",
        image_format="png",
        image_blob=b"data",
    )
    assert cache.get("k1", image_format="png") is None
    assert not os.path.exists(db_path)


def test_build_markdown_caching_and_no_cache(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Test that build_markdown uses cache on repeat runs and respects no_cache=True."""
    monkeypatch.chdir(tmp_path)

    md_file = tmp_path / "sample.md"
    md_file.write_text(
        """# Sample
```drawlib
circle((50, 50), 20, style=styles.primary)
```
""",
        encoding="utf-8",
    )

    out_file1 = tmp_path / "out1.md"
    # 1st run: fills cache
    build_markdown(str(md_file), output=str(out_file1))
    db_path = tmp_path / ".drawlib" / "cache.db"
    assert db_path.exists()

    conn = sqlite3.connect(str(db_path))
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM image_cache")
    count_after_first = cur.fetchone()[0]
    assert count_after_first == 1
    conn.close()

    # 2nd run with same code: cache hit (no new entries added)
    out_file2 = tmp_path / "out2.md"
    build_markdown(str(md_file), output=str(out_file2))
    assert (tmp_path / "out2_images" / "1.png").exists()

    # 3rd run with no_cache=True: runs successfully without cache interaction
    out_file3 = tmp_path / "out3.md"
    build_markdown(str(md_file), output=str(out_file3), no_cache=True)
    assert (tmp_path / "out3_images" / "1.png").exists()


def test_build_image_caching_and_no_cache(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Test that build_image caches standalone Python drawings and restores from cache."""
    monkeypatch.chdir(tmp_path)

    script = tmp_path / "my_draw.py"
    script.write_text(
        """from drawlib.canvas import save, setup
from drawlib.config import styles
from drawlib.shapes import circle

setup(width=100, height=100)
circle((50, 50), 20, style=styles.primary)
save("my_output.png")
""",
        encoding="utf-8",
    )

    # 1st run
    build_image(str(script))
    out_img = tmp_path / "my_output.png"
    assert out_img.exists()
    db_path = tmp_path / ".drawlib" / "cache.db"
    assert db_path.exists()

    # Delete output image to verify cache restoration on second run
    out_img.unlink()
    assert not out_img.exists()

    # 2nd run: restored from cache without executing Python code
    build_image(str(script))
    assert out_img.exists()
