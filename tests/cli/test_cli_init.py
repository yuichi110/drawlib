# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

# ruff: noqa: S404, S603, S607

"""Integration tests for drawlib init CLI command and project scaffolding API."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import pytest

from drawlib.tools import init_project, list_project_types
from tests.cli.common import run_drawlib_cli


def test_cli_init_list(tmp_path: Path) -> None:
    """Test `drawlib init list` displays available project types and `-l`/`--list` are rejected."""
    res1 = run_drawlib_cli(["init", "list"], cwd=str(tmp_path))
    assert res1.returncode == 0
    assert "Available Drawlib Project Types:" in res1.stdout
    assert "simple" in res1.stdout
    assert "site" in res1.stdout
    assert "pdf" in res1.stdout
    assert "image" in res1.stdout

    # Verify -l and --list are rejected
    res2 = run_drawlib_cli(["init", "--list"], cwd=str(tmp_path))
    assert res2.returncode != 0

    res3 = run_drawlib_cli(["init", "-l"], cwd=str(tmp_path))
    assert res3.returncode != 0


def test_cli_init_missing_type(tmp_path: Path) -> None:
    """Test `drawlib init` without arguments exits with code 1."""
    res = run_drawlib_cli(["init"], cwd=str(tmp_path))
    assert res.returncode == 1
    assert "Error: Missing project type." in res.stderr
    assert "simple" in res.stderr
    assert "drawlib init list" in res.stderr


def test_cli_init_unknown_type(tmp_path: Path) -> None:
    """Test `drawlib init unknown` exits with code 1."""
    res = run_drawlib_cli(["init", "unknown"], cwd=str(tmp_path))
    assert res.returncode == 1
    assert "Error: Unknown project type 'unknown'." in res.stderr
    assert "drawlib init list" in res.stderr


def test_cli_init_simple(tmp_path: Path) -> None:
    """Test scaffolding a simple project without automatic build."""
    dest = tmp_path / "my_simple"
    res = run_drawlib_cli(["init", "simple", str(dest)], cwd=str(tmp_path))
    assert res.returncode == 0
    assert f"Initialized 'simple' project in {dest}" in res.stdout

    # Source files inside docs_src/
    assert (dest / "docs_src" / "README.md").is_file()
    assert (dest / "docs_src" / "styles.py").is_file()
    assert (dest / "docs_src" / "utils.py").is_file()
    assert (dest / "docs_src" / "doc.md").is_file()
    assert (dest / "docs_src" / "_assets" / "linux.png").is_file()

    build_sh = dest / "docs_src" / "build.sh"
    assert build_sh.is_file()
    assert os.stat(build_sh).st_mode & 0o111 != 0

    # No automatic initial build outputs
    assert not (dest / "docs").exists()
    assert not (dest / "docs_html").exists()


def test_cli_init_site(tmp_path: Path) -> None:
    """Test scaffolding a documentation site project."""
    dest = tmp_path / "my_site"
    res = run_drawlib_cli(["init", "site", str(dest)], cwd=str(tmp_path))
    assert res.returncode == 0
    assert f"Initialized 'site' project in {dest}" in res.stdout

    # Source files inside docs_src/
    assert (dest / "docs_src" / "README.md").is_file()
    assert (dest / "docs_src" / "styles.py").is_file()
    assert (dest / "docs_src" / "utils.py").is_file()
    assert (dest / "docs_src" / "build.sh").is_file()
    assert (dest / "docs_src" / "index.md").is_file()
    assert (dest / "docs_src" / "navbar.md").is_file()
    assert (dest / "docs_src" / "architecture" / "index.md").is_file()
    assert (dest / "docs_src" / "workflow" / "index.md").is_file()
    assert (dest / "docs_src" / "_assets" / "linux.png").is_file()

    # No automatic initial build outputs
    assert not (dest / "docs_html").exists()
    assert not (dest / "docs").exists()


def test_cli_init_pdf(tmp_path: Path) -> None:
    """Test scaffolding a PDF project."""
    dest = tmp_path / "my_pdf"
    res = run_drawlib_cli(["init", "pdf", str(dest)], cwd=str(tmp_path))
    assert res.returncode == 0
    assert f"Initialized 'pdf' project in {dest}" in res.stdout

    assert (dest / "doc_src" / "README.md").is_file()
    assert (dest / "doc_src" / "styles.py").is_file()
    assert (dest / "doc_src" / "utils.py").is_file()
    assert (dest / "doc_src" / "build.sh").is_file()
    assert (dest / "doc_src" / "00_cover.md").is_file()
    assert (dest / "doc_src" / "01_overview.md").is_file()
    assert (dest / "doc_src" / "02_design.md").is_file()
    assert (dest / "doc_src" / "_assets" / "linux.png").is_file()

    # No automatic initial build
    assert not (dest / "doc.pdf").exists()


def test_cli_init_image(tmp_path: Path) -> None:
    """Test scaffolding an image project."""
    dest = tmp_path / "my_images"
    res = run_drawlib_cli(["init", "image", str(dest)], cwd=str(tmp_path))
    assert res.returncode == 0
    assert f"Initialized 'image' project in {dest}" in res.stdout

    # Source files inside images_src/
    assert (dest / "images_src" / "README.md").is_file()
    assert (dest / "images_src" / "styles.py").is_file()
    assert (dest / "images_src" / "utils.py").is_file()
    assert (dest / "images_src" / "build.sh").is_file()
    assert (dest / "images_src" / "sample1.py").is_file()
    assert (dest / "images_src" / "sample2.py").is_file()
    assert (dest / "images_src" / "_assets" / "linux.png").is_file()

    # No automatic initial build output
    assert not (dest / "images").exists()


def test_cli_init_custom_output(tmp_path: Path) -> None:
    """Test scaffolding with custom output name via -o."""
    dest = tmp_path / "my_project"
    res = run_drawlib_cli(["init", "site", str(dest), "-o", "manual"], cwd=str(tmp_path))
    assert res.returncode == 0

    # Source folder is manual_src/
    assert (dest / "manual_src" / "index.md").is_file()
    assert (dest / "manual_src" / "build.sh").is_file()
    build_sh_content = (dest / "manual_src" / "build.sh").read_text(encoding="utf-8")
    assert "manual_src" in build_sh_content
    assert "manual_html" in build_sh_content

    # Output folder not yet built
    assert not (dest / "manual_html").exists()


def test_cli_init_run_build_sh(tmp_path: Path) -> None:
    """Test executing the scaffolded build.sh script compiles the documentation."""
    dest = tmp_path / "my_built_simple"
    res = run_drawlib_cli(["init", "simple", str(dest)], cwd=str(tmp_path))
    assert res.returncode == 0

    build_sh = dest / "docs_src" / "build.sh"
    assert build_sh.is_file()

    # Execute build.sh
    build_res = subprocess.run(
        ["bash", str(build_sh)],
        cwd=str(dest / "docs_src"),
        capture_output=True,
        text=True,
        check=False,
    )
    assert build_res.returncode == 0
    assert (dest / "docs" / "doc.md").is_file()
    assert (dest / "docs_html" / "doc.html").is_file()


def test_cli_init_conflict_and_force(tmp_path: Path) -> None:
    """Test conflict detection and --force overwrite flag."""
    dest = tmp_path / "conflict_test"
    res1 = run_drawlib_cli(["init", "simple", str(dest)], cwd=str(tmp_path))
    assert res1.returncode == 0

    # Second run without force triggers FileExistsError because docs_src exists
    res2 = run_drawlib_cli(["init", "simple", str(dest)], cwd=str(tmp_path))
    assert res2.returncode == 1
    assert "already exists" in res2.stderr

    # With force succeeds
    res3 = run_drawlib_cli(["init", "simple", str(dest), "--force"], cwd=str(tmp_path))
    assert res3.returncode == 0


def test_cli_init_here(tmp_path: Path) -> None:
    """Test `drawlib init <type> --here` inside an existing repository directory."""
    repo_dir = tmp_path / "my_repo"
    repo_dir.mkdir()
    (repo_dir / "app.py").write_text("print('hello')", encoding="utf-8")

    res = run_drawlib_cli(["init", "site", "--here"], cwd=str(repo_dir))
    assert res.returncode == 0
    assert "Initialized 'site' project in ." in res.stdout

    # Existing repo files preserved
    assert (repo_dir / "app.py").read_text(encoding="utf-8") == "print('hello')"

    # Template files deployed into repo_dir
    assert (repo_dir / "build.sh").is_file()
    assert (repo_dir / "styles.py").is_file()
    assert (repo_dir / "index.md").is_file()

    # Second run without force fails because build.sh/styles.py already exists
    res_conflict = run_drawlib_cli(["init", "site", "--here"], cwd=str(repo_dir))
    assert res_conflict.returncode == 1
    assert "already contains project files" in res_conflict.stderr

    # Second run with force succeeds
    res_force = run_drawlib_cli(["init", "site", "--here", "--force"], cwd=str(repo_dir))
    assert res_force.returncode == 0


def test_cli_init_here_conflict_destination(tmp_path: Path) -> None:
    """Test specifying both [DESTINATION] and --here raises error."""
    res = run_drawlib_cli(["init", "simple", "some_dir", "--here"], cwd=str(tmp_path))
    assert res.returncode == 1
    assert "Cannot specify both [DESTINATION] and --here." in res.stderr


def test_python_api_init(tmp_path: Path) -> None:
    """Test Python programmatic API for project initialization."""
    types = list_project_types()
    assert set(types.keys()) == {"simple", "site", "pdf", "image"}

    target = tmp_path / "api_test"
    created = init_project("simple", destination=target)
    assert len(created) >= 4
    assert (target / "docs_src" / "build.sh").is_file()

    with pytest.raises(FileExistsError, match="already exists"):
        init_project("simple", destination=target, force=False)


def test_cli_init_lang_ja(tmp_path: Path) -> None:
    """Test `drawlib init site --lang ja` generates Japanese template assets."""
    res = run_drawlib_cli(["init", "site", "--lang", "ja"], cwd=str(tmp_path))
    assert res.returncode == 0
    assert "Initialized 'site' project" in res.stdout

    src_dir = tmp_path / "docs_src"
    assert (src_dir / "index.md").is_file()
    index_content = (src_dir / "index.md").read_text(encoding="utf-8")
    assert "プロジェクト概要" in index_content

    template_content = (src_dir / "template.html").read_text(encoding="utf-8")
    assert '<html lang="ja"' in template_content

    config_content = (src_dir / "styles.py").read_text(encoding="utf-8")
    assert "FontJapanese" in config_content
    assert "DefaultStyles" in config_content
    assert "DefaultColors" in config_content
    assert "patch_font" in config_content


def test_cli_init_style_option_google(tmp_path: Path) -> None:
    """Test `drawlib init site --style google` configures both style.css and styles.py."""
    res = run_drawlib_cli(["init", "site", "--style", "google"], cwd=str(tmp_path))
    assert res.returncode == 0
    assert "Initialized 'site' project" in res.stdout

    src_dir = tmp_path / "docs_src"
    style_file = src_dir / "style.css"
    assert style_file.is_file()
    content = style_file.read_text(encoding="utf-8")
    assert "Google Sans" in content or "#1a73e8" in content or "google" in content.lower()

    styles_py = (src_dir / "styles.py").read_text(encoding="utf-8")
    assert "from drawlib.preset_styles import GoogleStyles" in styles_py
    assert "from drawlib.preset_colors import GoogleColors" in styles_py
    assert "Styles = GoogleStyles()" in styles_py
    assert "Colors = GoogleColors()" in styles_py


def test_cli_init_style_option_monochrome(tmp_path: Path) -> None:
    """Test `drawlib init site -s monochrome` configures Monochrome styles."""
    res = run_drawlib_cli(["init", "site", "-s", "monochrome"], cwd=str(tmp_path))
    assert res.returncode == 0

    src_dir = tmp_path / "docs_src"
    styles_py = (src_dir / "styles.py").read_text(encoding="utf-8")
    assert "from drawlib.preset_styles import MonochromeStyles" in styles_py
    assert "from drawlib.preset_colors import MonochromeColors" in styles_py
    assert "Styles = MonochromeStyles()" in styles_py
    assert "Colors = MonochromeColors()" in styles_py


def test_cli_init_lang_ja_style_google(tmp_path: Path) -> None:
    """Test `drawlib init site --lang ja -s google` applies font patch to GoogleStyles."""
    res = run_drawlib_cli(["init", "site", "--lang", "ja", "-s", "google"], cwd=str(tmp_path))
    assert res.returncode == 0

    src_dir = tmp_path / "docs_src"
    styles_py = (src_dir / "styles.py").read_text(encoding="utf-8")
    assert "from drawlib.fonts import FontJapanese" in styles_py
    assert "from drawlib.preset_styles import GoogleStyles" in styles_py
    assert "from drawlib.preset_colors import GoogleColors" in styles_py
    assert "Colors = GoogleColors()" in styles_py
    assert "Styles = GoogleStyles().patch_font(" in styles_py


def test_cli_init_lang_th(tmp_path: Path) -> None:
    """Test `drawlib init site --lang th` injects Thai font and falls back gracefully."""
    res = run_drawlib_cli(["init", "site", "--lang", "th"], cwd=str(tmp_path))
    assert res.returncode == 0
    assert "Initialized 'site' project" in res.stdout

    src_dir = tmp_path / "docs_src"
    template_content = (src_dir / "template.html").read_text(encoding="utf-8")
    assert '<html lang="th"' in template_content
    assert "Noto Sans Thai" in template_content

    style_content = (src_dir / "style.css").read_text(encoding="utf-8")
    assert "Noto Sans Thai" in style_content


def test_cli_init_lang_invalid(tmp_path: Path) -> None:
    """Test `drawlib init site --lang invalid` fails with helpful error."""
    res = run_drawlib_cli(["init", "site", "--lang", "unknown_lang"], cwd=str(tmp_path))
    assert res.returncode != 0
    assert "Unsupported language 'unknown_lang'" in res.stderr
