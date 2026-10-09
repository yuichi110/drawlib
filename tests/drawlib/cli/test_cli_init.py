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
from tests.drawlib.cli.common import run_drawlib_cli


def test_cli_init_list(tmp_path: Path) -> None:
    """Test `drawlib init list` displays available project types and `-l`/`--list` are rejected."""
    res1 = run_drawlib_cli(["init", "list"], cwd=str(tmp_path))
    assert res1.returncode == 0
    assert "Available Drawlib Project Types:" in res1.stdout
    assert "doc" in res1.stdout
    assert "site" in res1.stdout
    assert "slide" in res1.stdout
    assert "images" in res1.stdout

    # Verify -l and --list are rejected
    res2 = run_drawlib_cli(["init", "--list"], cwd=str(tmp_path))
    assert res2.returncode != 0

    res3 = run_drawlib_cli(["init", "-l"], cwd=str(tmp_path))
    assert res3.returncode != 0


def test_cli_init_no_args_shows_help(tmp_path: Path) -> None:
    """Test `drawlib init` without arguments displays usage help."""
    res = run_drawlib_cli(["init"], cwd=str(tmp_path))
    assert res.returncode in {0, 2}
    assert "Usage: drawlib init" in res.stdout or "Usage: drawlib init" in res.stderr


def test_cli_init_unknown_type(tmp_path: Path) -> None:
    """Test `drawlib init unknown` exits with error."""
    res = run_drawlib_cli(["init", "unknown"], cwd=str(tmp_path))
    assert res.returncode != 0
    assert "No such command" in res.stderr or "Error" in res.stderr


def test_cli_init_doc_default(tmp_path: Path) -> None:
    """Test scaffolding a doc project with default target ('doc_src/')."""
    res = run_drawlib_cli(["init", "doc"], cwd=str(tmp_path))
    assert res.returncode == 0
    assert "Initialized 'doc' project ('doc_src/')" in res.stdout

    # Source files inside doc_src/
    assert (tmp_path / "doc_src" / "README.md").is_file()
    assert (tmp_path / "doc_src" / "styles.py").is_file()
    assert (tmp_path / "doc_src" / "utils.py").is_file()
    assert (tmp_path / "doc_src" / "00_cover.md").is_file()
    assert (tmp_path / "doc_src" / "01_overview.md").is_file()
    assert (tmp_path / "doc_src" / "02_design.md").is_file()
    assert (tmp_path / "doc_src" / "template.html").is_file()
    assert (tmp_path / "doc_src" / "style.css").is_file()
    assert (tmp_path / "doc_src" / "_assets" / "linux.png").is_file()
    assert (tmp_path / "doc_src" / "_assets" / "favicon.png").is_file()

    for script in [
        "build.sh",
        "build_html.sh",
        "build_pdf.sh",
        "build_markdown.sh",
        "build_image.sh",
        "serve.sh",
    ]:
        s = tmp_path / "doc_src" / script
        assert s.is_file()
        if sys.platform != "win32":
            assert os.stat(s).st_mode & 0o111 != 0

    # No automatic initial build outputs
    assert not (tmp_path / "doc_markdown").exists()
    assert not (tmp_path / "doc_images").exists()
    assert not (tmp_path / "doc_html").exists()
    assert not (tmp_path / "doc.pdf").exists()


def test_cli_init_site_default(tmp_path: Path) -> None:
    """Test scaffolding a documentation site project with default target ('docs_src/')."""
    res = run_drawlib_cli(["init", "site"], cwd=str(tmp_path))
    assert res.returncode == 0
    assert "Initialized 'site' project ('docs_src/')" in res.stdout

    # Source files inside docs_src/
    assert (tmp_path / "docs_src" / "README.md").is_file()
    assert (tmp_path / "docs_src" / "styles.py").is_file()
    assert (tmp_path / "docs_src" / "utils.py").is_file()
    assert (tmp_path / "docs_src" / "template.html").is_file()
    assert (tmp_path / "docs_src" / "style.css").is_file()
    assert (tmp_path / "docs_src" / "index.md").is_file()
    assert (tmp_path / "docs_src" / "navbar.md").is_file()
    assert (tmp_path / "docs_src" / "architecture" / "index.md").is_file()
    assert (tmp_path / "docs_src" / "workflow" / "index.md").is_file()
    assert (tmp_path / "docs_src" / "_assets" / "linux.png").is_file()
    assert (tmp_path / "docs_src" / "_assets" / "favicon.png").is_file()

    for script in ["build.sh", "build_html.sh", "build_markdown.sh", "build_image.sh", "serve.sh"]:
        s = tmp_path / "docs_src" / script
        assert s.is_file()
        if sys.platform != "win32":
            assert os.stat(s).st_mode & 0o111 != 0

    # No automatic initial build outputs
    assert not (tmp_path / "docs_html").exists()
    assert not (tmp_path / "docs_markdown").exists()
    assert not (tmp_path / "docs_images").exists()


def test_cli_init_slide_default(tmp_path: Path) -> None:
    """Test scaffolding a slide presentation project with default target ('slide_src/')."""
    res = run_drawlib_cli(["init", "slide"], cwd=str(tmp_path))
    assert res.returncode == 0
    assert "Initialized 'slide' project ('slide_src/')" in res.stdout

    assert (tmp_path / "slide_src" / "README.md").is_file()
    assert (tmp_path / "slide_src" / "styles.py").is_file()
    assert (tmp_path / "slide_src" / "utils.py").is_file()
    assert (tmp_path / "slide_src" / "style.css").is_file()
    assert (tmp_path / "slide_src" / "01_title.md").is_file()
    assert (tmp_path / "slide_src" / "02_agenda.md").is_file()
    assert (tmp_path / "slide_src" / "03_architecture.md").is_file()
    assert (tmp_path / "slide_src" / "_assets" / "linux.png").is_file()
    assert (tmp_path / "slide_src" / "_assets" / "favicon.png").is_file()

    for script in ["build.sh", "build_html.sh", "build_pdf.sh", "build_image.sh", "serve.sh"]:
        s = tmp_path / "slide_src" / script
        assert s.is_file()
        if sys.platform != "win32":
            assert os.stat(s).st_mode & 0o111 != 0

    assert not (tmp_path / "slide_html").exists()
    assert not (tmp_path / "slide_images").exists()
    assert not (tmp_path / "slide.pdf").exists()


def test_cli_init_images_default(tmp_path: Path) -> None:
    """Test scaffolding an images project with canonical name 'images'."""
    res = run_drawlib_cli(["init", "images"], cwd=str(tmp_path))
    assert res.returncode == 0
    assert "Initialized 'images' project ('images_src/')" in res.stdout

    # Source files inside images_src/
    assert (tmp_path / "images_src" / "README.md").is_file()
    assert (tmp_path / "images_src" / "styles.py").is_file()
    assert (tmp_path / "images_src" / "utils.py").is_file()
    assert (tmp_path / "images_src" / "sample1.py").is_file()
    assert (tmp_path / "images_src" / "sample2.py").is_file()
    assert (tmp_path / "images_src" / "_assets" / "linux.png").is_file()
    assert (tmp_path / "images_src" / "_assets" / "favicon.png").is_file()

    for script in ["build.sh", "build_image.sh"]:
        s = tmp_path / "images_src" / script
        assert s.is_file()
        if sys.platform != "win32":
            assert os.stat(s).st_mode & 0o111 != 0

    # Next steps outputs correctly
    assert "./images_src/build.sh" in res.stdout


def test_cli_init_image_alias(tmp_path: Path) -> None:
    """Test legacy 'init image' alias creates images_src/ seamlessly."""
    res = run_drawlib_cli(["init", "image"], cwd=str(tmp_path))
    assert res.returncode == 0
    assert (tmp_path / "images_src" / "sample1.py").is_file()


def test_cli_init_custom_target(tmp_path: Path) -> None:
    """Test scaffolding with custom target name."""
    res = run_drawlib_cli(["init", "site", "manual"], cwd=str(tmp_path))
    assert res.returncode == 0
    assert "Initialized 'site' project ('manual_src/')" in res.stdout

    # Source folder is manual_src/
    assert (tmp_path / "manual_src" / "index.md").is_file()
    assert (tmp_path / "manual_src" / "build.sh").is_file()
    assert (tmp_path / "manual_src" / "build_html.sh").is_file()
    build_html_content = (tmp_path / "manual_src" / "build_html.sh").read_text(encoding="utf-8")
    assert "manual_src" in build_html_content
    assert "manual_html" in build_html_content


@pytest.mark.skipif(sys.platform == "win32", reason="POSIX bash script execution")
def test_cli_init_run_build_sh(tmp_path: Path) -> None:
    """Test executing the scaffolded build_html.sh script compiles the documentation."""
    res = run_drawlib_cli(["init", "doc"], cwd=str(tmp_path))
    assert res.returncode == 0

    build_sh = tmp_path / "doc_src" / "build_html.sh"
    assert build_sh.is_file()

    # Execute build_html.sh
    build_res = subprocess.run(
        ["bash", str(build_sh)],
        cwd=str(tmp_path / "doc_src"),
        capture_output=True,
        text=True,
        check=False,
    )
    assert build_res.returncode == 0
    assert (tmp_path / "doc_html" / "index.html").is_file()
    assert (tmp_path / "doc_html" / "README.md").is_file()
    assert not (tmp_path / "doc_html" / "01_overview.html").exists()


def test_cli_init_conflict_and_force(tmp_path: Path) -> None:
    """Test conflict detection and --force overwrite flag."""
    res1 = run_drawlib_cli(["init", "doc"], cwd=str(tmp_path))
    assert res1.returncode == 0

    # Second run without force triggers FileExistsError because doc_src exists
    res2 = run_drawlib_cli(["init", "doc"], cwd=str(tmp_path))
    assert res2.returncode == 1
    assert "already exists" in res2.stderr

    # With force succeeds
    res3 = run_drawlib_cli(["init", "doc", "--force"], cwd=str(tmp_path))
    assert res3.returncode == 0


def test_python_api_init(tmp_path: Path) -> None:
    """Test Python programmatic API for project initialization."""
    types = list_project_types()
    assert set(types.keys()) == {"doc", "site", "slide", "images"}

    target = tmp_path / "api_test"
    created = init_project("doc", destination=target)
    assert len(created) >= 4
    assert (target / "doc_src" / "build.sh").is_file()

    with pytest.raises(FileExistsError, match="already exists"):
        init_project("doc", destination=target, force=False)


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
    assert "Noto+Sans+Thai" in template_content

    style_content = (src_dir / "style.css").read_text(encoding="utf-8")
    assert "Noto Sans Thai" in style_content


def test_cli_init_lang_invalid(tmp_path: Path) -> None:
    """Test `drawlib init site --lang invalid` fails with helpful error."""
    res = run_drawlib_cli(["init", "site", "--lang", "unknown_lang"], cwd=str(tmp_path))
    assert res.returncode != 0
    assert "Unsupported language 'unknown_lang'" in res.stderr
