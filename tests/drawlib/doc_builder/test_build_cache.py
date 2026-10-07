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

from drawlib._builder._common.cache import (
    BuildImageCache,
    CliImageCache,
    hash_file,
    hash_text,
)
from drawlib.canvas import clear, save, setup
from drawlib.shapes import circle
from drawlib.styles import Styles
from drawlib.tools import build_html, build_image, build_markdown, build_pdf


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

    src_dir = tmp_path / "docs_src"
    src_dir.mkdir()
    md_file = src_dir / "sample.md"
    md_file.write_text(
        """# Sample
```drawlib file:cached_circle.png
from drawlib.shapes import circle
from drawlib.styles import Styles
circle((50, 50), 20, style=Styles.Primary)
```
""",
        encoding="utf-8",
    )

    out_dir1 = tmp_path / "out1"
    # 1st run: fills cache
    build_markdown(input_dir=str(src_dir), output_dir=str(out_dir1))
    db_path = tmp_path / ".drawlib" / "cache.db"
    assert db_path.exists()

    conn = sqlite3.connect(str(db_path))
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM image_cache")
    count_after_first = cur.fetchone()[0]
    assert count_after_first == 1
    conn.close()

    # 2nd run with same code: cache hit (no new entries added)
    out_dir2 = tmp_path / "out2"
    build_markdown(input_dir=str(src_dir), output_dir=str(out_dir2))
    assert (out_dir2 / "sample_images" / "cached_circle.png").exists()

    # 3rd run with no_cache=True: runs successfully without cache interaction
    out_dir3 = tmp_path / "out3"
    build_markdown(input_dir=str(src_dir), output_dir=str(out_dir3), no_cache=True)
    assert (out_dir3 / "sample_images" / "cached_circle.png").exists()


def test_build_image_caching_and_no_cache(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Test that build_image caches standalone Python drawings and restores from cache."""
    monkeypatch.chdir(tmp_path)

    script = tmp_path / "my_draw.py"
    script.write_text(
        """from drawlib.canvas import save, setup
from drawlib.styles import Styles
from drawlib.shapes import circle

setup(width=100, height=100)
circle((50, 50), 20, style=Styles.Primary)
save("my_output.png")
""",
        encoding="utf-8",
    )

    # 1st run
    build_image(input_path=str(script))
    out_img = tmp_path / "my_output.png"
    assert out_img.exists()
    db_path = tmp_path / ".drawlib" / "cache.db"
    assert db_path.exists()

    # Delete output image to verify cache restoration on second run
    out_img.unlink()
    assert not out_img.exists()

    # 2nd run: restored from cache without executing Python code
    build_image(input_path=str(script))
    assert out_img.exists()


def test_cli_image_cache_put_get_clear(tmp_path: Path) -> None:
    """Test storing, retrieving, and clearing PNG blobs in CliImageCache."""
    db_path = str(tmp_path / ".drawlib" / "cache.db")
    cache = CliImageCache(db_path=db_path)

    key1 = "styles_show:monochrome:1:25:None:False:v0.3"
    png_data = b"\x89PNG\r\n\x1a\nfake_cli_png"

    # Initially missing
    assert cache.get(key1) is None

    # Put entry
    cache.put(
        cache_key=key1,
        category="styles",
        preset_name="monochrome",
        page=1,
        has_grid=False,
        png_blob=png_data,
    )

    # Hit
    retrieved = cache.get(key1)
    assert retrieved == png_data

    # Clear
    cache.clear()
    assert cache.get(key1) is None


def test_build_cache_referenced_asset_invalidation(tmp_path: Path) -> None:
    """Test that referenced assets in project_root/_assets are hashed and invalidate cache on change."""
    docs_root = tmp_path / "docs_src"
    docs_root.mkdir()
    assets_dir = docs_root / "_assets"
    assets_dir.mkdir()
    logo_file = assets_dir / "logo.png"
    logo_file.write_bytes(b"initial_logo_png_bytes")
    unrelated_file = assets_dir / "unrelated.png"
    unrelated_file.write_bytes(b"unrelated_bytes")

    sub_dir = docs_root / "guide"
    sub_dir.mkdir()

    # Code referencing _assets/logo.png
    code = 'image((10, 10), width=20, image="_assets/logo.png")'

    # Compute key with explicit project_root
    key1, _ = BuildImageCache.compute_keys(code, context_dir=str(sub_dir), project_root=str(docs_root))

    # Compute key with auto-detected project_root (walking up from context_dir to find _assets/)
    key1_auto, _ = BuildImageCache.compute_keys(code, context_dir=str(sub_dir), project_root=None)
    assert key1 == key1_auto

    # Modify unrelated asset -> key MUST NOT change (only referenced assets affect cache)
    unrelated_file.write_bytes(b"modified_unrelated_bytes")
    key_unrelated, _ = BuildImageCache.compute_keys(code, context_dir=str(sub_dir), project_root=str(docs_root))
    assert key_unrelated == key1

    # Modify the referenced logo file -> key MUST change
    logo_file.write_bytes(b"updated_new_logo_png_bytes")
    key2, _ = BuildImageCache.compute_keys(code, context_dir=str(sub_dir), project_root=str(docs_root))
    assert key2 != key1


def test_compute_keys_differentiates_source_and_target_files(tmp_path: Path) -> None:
    """Verify that different source_file or target_file absolute paths produce distinct cache keys."""
    code = "from drawlib.shapes import circle\ncircle((50, 50), radius=10)"

    src1 = str(tmp_path / "slide1.md")
    src2 = str(tmp_path / "slide2.md")
    tgt1 = str(tmp_path / "out1.png")
    tgt2 = str(tmp_path / "out2.png")

    key_s1_t1, _ = BuildImageCache.compute_keys(code, source_file=src1, target_file=tgt1)
    key_s1_t1_repeat, _ = BuildImageCache.compute_keys(code, source_file=src1, target_file=tgt1)
    assert key_s1_t1 == key_s1_t1_repeat

    # Different source file
    key_s2_t1, _ = BuildImageCache.compute_keys(code, source_file=src2, target_file=tgt1)
    assert key_s1_t1 != key_s2_t1

    # Different target file
    key_s1_t2, _ = BuildImageCache.compute_keys(code, source_file=src1, target_file=tgt2)
    assert key_s1_t1 != key_s1_t2


def test_build_cache_creates_gitignore_and_cachedir_tag(tmp_path: Path) -> None:
    """Verify that BuildImageCache and CliImageCache create .gitignore and CACHEDIR.TAG in cache dir."""
    cache_dir = tmp_path / ".drawlib"
    db_path = str(cache_dir / "cache.db")

    BuildImageCache(db_path=db_path)

    gitignore = cache_dir / ".gitignore"
    cachedir_tag = cache_dir / "CACHEDIR.TAG"
    assert gitignore.is_file()
    assert cachedir_tag.is_file()
    assert gitignore.read_text(encoding="utf-8") == "# Created by drawlib automatically.\n*\n"
    assert cachedir_tag.read_text(encoding="utf-8").startswith("Signature: 8a477f597d28d172789f06886806bc55\n")

    # Verify CliImageCache also creates them in a fresh directory
    cli_cache_dir = tmp_path / ".drawlib_cli"
    CliImageCache(db_path=str(cli_cache_dir / "cache.db"))
    assert (cli_cache_dir / ".gitignore").is_file()
    assert (cli_cache_dir / "CACHEDIR.TAG").is_file()


def test_build_cache_preserves_existing_gitignore_and_cachedir_tag(tmp_path: Path) -> None:
    """Verify that existing .gitignore and CACHEDIR.TAG files are not overwritten."""
    cache_dir = tmp_path / ".drawlib"
    cache_dir.mkdir(parents=True)

    gitignore = cache_dir / ".gitignore"
    cachedir_tag = cache_dir / "CACHEDIR.TAG"
    gitignore.write_text("# Custom user gitignore\n*.db\n", encoding="utf-8")
    cachedir_tag.write_text("Signature: 8a477f597d28d172789f06886806bc55\n# Custom tag\n", encoding="utf-8")

    BuildImageCache(db_path=str(cache_dir / "cache.db"))

    assert gitignore.read_text(encoding="utf-8") == "# Custom user gitignore\n*.db\n"
    assert cachedir_tag.read_text(encoding="utf-8") == "Signature: 8a477f597d28d172789f06886806bc55\n# Custom tag\n"


def test_canvas_save_into_drawlib_dir_creates_gitignore_and_cachedir_tag(tmp_path: Path) -> None:
    """Verify that saving an image into .drawlib/scratch/ creates .drawlib/.gitignore and CACHEDIR.TAG."""
    cache_dir = tmp_path / ".drawlib"
    out_file = cache_dir / "scratch" / "preview.png"

    clear()
    setup(width=50, height=50)
    circle((25, 25), radius=10, style=Styles.Neutral)
    save(str(out_file))

    assert out_file.is_file()
    assert (cache_dir / ".gitignore").is_file()
    assert (cache_dir / "CACHEDIR.TAG").is_file()
