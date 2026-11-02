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
    """Test `drawlib init project list` displays available project types and `-l`/`--list` are rejected."""
    res1 = run_drawlib_cli(["init", "project", "list"], cwd=str(tmp_path))
    assert res1.returncode == 0
    assert "Available Drawlib Project Types:" in res1.stdout
    assert "doc" in res1.stdout
    assert "site" in res1.stdout
    assert "slide" in res1.stdout
    assert "images" in res1.stdout
    assert "drawlib init project <type>" in res1.stdout

    # Verify -l and --list are rejected on `init` and `init project`
    for bad_args in (["init", "--list"], ["init", "-l"], ["init", "project", "--list"], ["init", "project", "-l"]):
        res_bad = run_drawlib_cli(bad_args, cwd=str(tmp_path))
        assert res_bad.returncode != 0


def test_cli_init_no_args_shows_help(tmp_path: Path) -> None:
    """Test `drawlib init` and `drawlib init project` without arguments display usage help."""
    res = run_drawlib_cli(["init"], cwd=str(tmp_path))
    assert res.returncode in {0, 2}
    combined = res.stdout + res.stderr
    assert "Usage: drawlib init" in combined
    assert "project" in combined
    assert "agent" in combined

    res_proj = run_drawlib_cli(["init", "project"], cwd=str(tmp_path))
    assert res_proj.returncode in {0, 2}
    assert "Usage: drawlib init project" in (res_proj.stdout + res_proj.stderr)


def test_cli_init_legacy_root_commands_rejected(tmp_path: Path) -> None:
    """Verify abolished legacy root `drawlib init <doc|site|slide|images|image|list>` commands fail."""
    for legacy_cmd in ("doc", "site", "slide", "images", "image", "list", "unknown"):
        res = run_drawlib_cli(["init", legacy_cmd], cwd=str(tmp_path))
        assert res.returncode != 0, f"Expected `drawlib init {legacy_cmd}` to fail"
        assert "No such command" in res.stderr or "Error" in res.stderr


def test_cli_init_unknown_type(tmp_path: Path) -> None:
    """Test `drawlib init project unknown` exits with error."""
    res = run_drawlib_cli(["init", "project", "unknown"], cwd=str(tmp_path))
    assert res.returncode != 0
    assert "No such command" in res.stderr or "Error" in res.stderr


def test_cli_init_doc_default(tmp_path: Path) -> None:
    """Test scaffolding a doc project with default target ('doc_src/')."""
    res = run_drawlib_cli(["init", "project", "doc"], cwd=str(tmp_path))
    assert res.returncode == 0
    assert "Initialized 'doc' project ('doc_src/')" in res.stdout

    # Source files inside doc_src/ and doc_src/en/
    assert (tmp_path / "doc_src" / "README.md").is_file()
    assert (tmp_path / "doc_src" / "drawlib.toml").is_file()
    assert (tmp_path / "doc_src" / "styles.py").is_file()
    assert (tmp_path / "doc_src" / "utils.py").is_file()
    assert (tmp_path / "doc_src" / "en" / "00_cover.md").is_file()
    assert (tmp_path / "doc_src" / "en" / "01_overview.md").is_file()
    assert (tmp_path / "doc_src" / "en" / "02_design.md").is_file()
    assert not (tmp_path / "doc_src" / "00_cover.md").exists()
    assert (tmp_path / "doc_src" / "template.html").is_file()
    assert (tmp_path / "doc_src" / "style.css").is_file()
    assert (tmp_path / "doc_src" / "_assets" / "linux.png").is_file()
    assert (tmp_path / "doc_src" / "_assets" / "favicon.png").is_file()

    for script in [
        "build.sh",
        "build_html.sh",
        "build_pdf.sh",
        "build_docx.sh",
        "build_markdown.sh",
        "build_image.sh",
        "serve.sh",
    ]:
        s = tmp_path / "doc_src" / script
        assert s.is_file()
        if sys.platform != "win32":
            assert os.stat(s).st_mode & 0o111 != 0

    assert "./doc_src/build_docx.sh" in res.stdout

    # No automatic initial build outputs
    assert not (tmp_path / "doc_markdown").exists()
    assert not (tmp_path / "doc_images").exists()
    assert not (tmp_path / "doc_html").exists()
    assert not (tmp_path / "doc_en.pdf").exists()
    assert not (tmp_path / "doc.pdf").exists()
    assert not (tmp_path / "doc_en.docx").exists()
    assert not (tmp_path / "doc.docx").exists()


def test_cli_init_site_default(tmp_path: Path) -> None:
    """Test scaffolding a documentation site project with default target ('docs_src/')."""
    res = run_drawlib_cli(["init", "project", "site"], cwd=str(tmp_path))
    assert res.returncode == 0
    assert "Initialized 'site' project ('docs_src/')" in res.stdout

    # Source files inside docs_src/ and docs_src/en/
    assert (tmp_path / "docs_src" / "README.md").is_file()
    assert (tmp_path / "docs_src" / "drawlib.toml").is_file()
    assert (tmp_path / "docs_src" / "styles.py").is_file()
    assert (tmp_path / "docs_src" / "utils.py").is_file()
    assert (tmp_path / "docs_src" / "template.html").is_file()
    assert (tmp_path / "docs_src" / "style.css").is_file()
    assert (tmp_path / "docs_src" / "en" / "index.md").is_file()
    assert (tmp_path / "docs_src" / "en" / "navbar.md").is_file()
    assert (tmp_path / "docs_src" / "en" / "architecture" / "index.md").is_file()
    assert (tmp_path / "docs_src" / "en" / "workflow" / "index.md").is_file()
    assert not (tmp_path / "docs_src" / "index.md").exists()
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
    res = run_drawlib_cli(["init", "project", "slide"], cwd=str(tmp_path))
    assert res.returncode == 0
    assert "Initialized 'slide' project ('slide_src/')" in res.stdout

    assert (tmp_path / "slide_src" / "README.md").is_file()
    assert (tmp_path / "slide_src" / "drawlib.toml").is_file()
    assert (tmp_path / "slide_src" / "styles.py").is_file()
    assert (tmp_path / "slide_src" / "utils.py").is_file()
    assert (tmp_path / "slide_src" / "style.css").is_file()
    assert (tmp_path / "slide_src" / "en" / "01_title.md").is_file()
    assert (tmp_path / "slide_src" / "en" / "02_agenda.md").is_file()
    assert (tmp_path / "slide_src" / "en" / "03_architecture.md").is_file()
    assert not (tmp_path / "slide_src" / "01_title.md").exists()
    assert "../_assets/linux.png" in (tmp_path / "slide_src" / "en" / "01_title.md").read_text(encoding="utf-8")
    assert (tmp_path / "slide_src" / "_assets" / "linux.png").is_file()
    assert (tmp_path / "slide_src" / "_assets" / "favicon.png").is_file()

    for script in ["build.sh", "build_html.sh", "build_pdf.sh", "build_pptx.sh", "build_image.sh", "serve.sh"]:
        s = tmp_path / "slide_src" / script
        assert s.is_file()
        if sys.platform != "win32":
            assert os.stat(s).st_mode & 0o111 != 0

    assert "./slide_src/build_pptx.sh" in res.stdout

    assert not (tmp_path / "slide_html").exists()
    assert not (tmp_path / "slide_images").exists()
    assert not (tmp_path / "slide_en.pdf").exists()
    assert not (tmp_path / "slide.pdf").exists()
    assert not (tmp_path / "slide_en.pptx").exists()
    assert not (tmp_path / "slide.pptx").exists()


def test_cli_init_images_default(tmp_path: Path) -> None:
    """Test scaffolding an images project with canonical name 'images'."""
    res = run_drawlib_cli(["init", "project", "images"], cwd=str(tmp_path))
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
    """Test singular 'init project image' alias creates images_src/ seamlessly."""
    res = run_drawlib_cli(["init", "project", "image"], cwd=str(tmp_path))
    assert res.returncode == 0
    assert (tmp_path / "images_src" / "sample1.py").is_file()


def test_cli_init_custom_target(tmp_path: Path) -> None:
    """Test scaffolding with custom target name."""
    res = run_drawlib_cli(["init", "project", "site", "manual"], cwd=str(tmp_path))
    assert res.returncode == 0
    assert "Initialized 'site' project ('manual_src/')" in res.stdout

    # Source folder is manual_src/ with locale subfolder en/
    assert (tmp_path / "manual_src" / "drawlib.toml").is_file()
    assert (tmp_path / "manual_src" / "en" / "index.md").is_file()
    assert not (tmp_path / "manual_src" / "index.md").exists()
    assert (tmp_path / "manual_src" / "build.sh").is_file()
    assert (tmp_path / "manual_src" / "build_html.sh").is_file()
    build_html_content = (tmp_path / "manual_src" / "build_html.sh").read_text(encoding="utf-8")
    assert "manual_src" in build_html_content
    assert "manual_html" in build_html_content


def _is_playwright_available() -> bool:
    try:
        from playwright.sync_api import sync_playwright  # noqa: PLC0415

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            browser.close()
        return True
    except Exception:
        return False


@pytest.mark.skipif(sys.platform == "win32", reason="POSIX bash script execution")
def test_cli_init_run_build_sh(tmp_path: Path) -> None:
    """Test executing the scaffolded build_html.sh, build_docx.sh, and build_pdf.sh scripts."""
    res = run_drawlib_cli(["init", "project", "doc"], cwd=str(tmp_path))
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
    assert (tmp_path / "doc_html" / "en" / "index.html").is_file()
    assert (tmp_path / "doc_html" / "README.md").is_file()
    assert not (tmp_path / "doc_html" / "01_overview.html").exists()
    assert not (tmp_path / "doc_html" / "en" / "01_overview.html").exists()

    # Execute build_docx.sh directly via its executable bit (+x) without bash prefix
    build_docx_sh = tmp_path / "doc_src" / "build_docx.sh"
    assert build_docx_sh.is_file()
    docx_res = subprocess.run(
        [str(build_docx_sh)],
        cwd=str(tmp_path),
        capture_output=True,
        text=True,
        check=False,
    )
    assert docx_res.returncode == 0, docx_res.stderr
    assert (tmp_path / "doc_en.docx").is_file()
    assert not (tmp_path / "doc.docx").exists()

    if _is_playwright_available():
        build_pdf_sh = tmp_path / "doc_src" / "build_pdf.sh"
        assert build_pdf_sh.is_file()
        pdf_res = subprocess.run(
            ["bash", str(build_pdf_sh)],
            cwd=str(tmp_path / "doc_src"),
            capture_output=True,
            text=True,
            check=False,
        )
        assert pdf_res.returncode == 0
        assert (tmp_path / "doc_en.pdf").is_file()
        assert not (tmp_path / "doc.pdf").exists()

        res_slide = run_drawlib_cli(["init", "project", "slide"], cwd=str(tmp_path))
        assert res_slide.returncode == 0
        build_pptx_sh = tmp_path / "slide_src" / "build_pptx.sh"
        assert build_pptx_sh.is_file()
        pptx_res = subprocess.run(
            [str(build_pptx_sh)],
            cwd=str(tmp_path),
            capture_output=True,
            text=True,
            check=False,
        )
        assert pptx_res.returncode == 0, pptx_res.stderr
        assert (tmp_path / "slide_en.pptx").is_file()
        assert not (tmp_path / "slide.pptx").exists()


def test_cli_init_conflict_and_force(tmp_path: Path) -> None:
    """Test conflict detection and --force overwrite flag."""
    res1 = run_drawlib_cli(["init", "project", "doc"], cwd=str(tmp_path))
    assert res1.returncode == 0

    # Second run without force triggers FileExistsError because doc_src exists
    res2 = run_drawlib_cli(["init", "project", "doc"], cwd=str(tmp_path))
    assert res2.returncode == 1
    assert "already exists" in res2.stderr

    # With force succeeds
    res3 = run_drawlib_cli(["init", "project", "doc", "--force"], cwd=str(tmp_path))
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
    """Test `drawlib init project site --lang ja` generates Japanese template assets."""
    res = run_drawlib_cli(["init", "project", "site", "--lang", "ja"], cwd=str(tmp_path))
    assert res.returncode == 0
    assert "Initialized 'site' project" in res.stdout

    src_dir = tmp_path / "docs_src"
    assert (src_dir / "ja" / "index.md").is_file()
    assert not (src_dir / "index.md").exists()
    index_content = (src_dir / "ja" / "index.md").read_text(encoding="utf-8")
    assert "プロジェクト概要" in index_content

    manifest_content = (src_dir / "drawlib.toml").read_text(encoding="utf-8")
    assert "[i18n]" in manifest_content
    assert 'default_lang = "ja"' in manifest_content
    assert 'langs = ["ja"]' in manifest_content

    template_content = (src_dir / "template.html").read_text(encoding="utf-8")
    assert "{{ html_lang | default('en') }}" in template_content
    assert "{{ html_dir | default('ltr') }}" in template_content

    config_content = (src_dir / "styles.py").read_text(encoding="utf-8")
    assert "FontJapanese" in config_content
    assert "DefaultStyles" in config_content
    assert "DefaultColors" in config_content
    assert "patch_font" in config_content


def test_cli_init_style_option_google(tmp_path: Path) -> None:
    """Test `drawlib init project site --style google` configures both style.css and styles.py."""
    res = run_drawlib_cli(["init", "project", "site", "--style", "google"], cwd=str(tmp_path))
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
    """Test `drawlib init project site -s monochrome` configures Monochrome styles."""
    res = run_drawlib_cli(["init", "project", "site", "-s", "monochrome"], cwd=str(tmp_path))
    assert res.returncode == 0

    src_dir = tmp_path / "docs_src"
    styles_py = (src_dir / "styles.py").read_text(encoding="utf-8")
    assert "from drawlib.preset_styles import MonochromeStyles" in styles_py
    assert "from drawlib.preset_colors import MonochromeColors" in styles_py
    assert "Styles = MonochromeStyles()" in styles_py
    assert "Colors = MonochromeColors()" in styles_py


def test_cli_init_lang_ja_style_google(tmp_path: Path) -> None:
    """Test `drawlib init project site --lang ja -s google` applies font patch to GoogleStyles."""
    res = run_drawlib_cli(["init", "project", "site", "--lang", "ja", "-s", "google"], cwd=str(tmp_path))
    assert res.returncode == 0

    src_dir = tmp_path / "docs_src"
    styles_py = (src_dir / "styles.py").read_text(encoding="utf-8")
    assert "from drawlib.fonts import FontJapanese" in styles_py
    assert "from drawlib.preset_styles import GoogleStyles" in styles_py
    assert "from drawlib.preset_colors import GoogleColors" in styles_py
    assert "Colors = GoogleColors()" in styles_py
    assert "Styles = GoogleStyles().patch_font(" in styles_py


def test_cli_init_lang_th(tmp_path: Path) -> None:
    """Test `drawlib init project site --lang th` configures Thai locale, CSS font, and Jinja template."""
    res = run_drawlib_cli(["init", "project", "site", "--lang", "th"], cwd=str(tmp_path))
    assert res.returncode == 0
    assert "Initialized 'site' project" in res.stdout

    src_dir = tmp_path / "docs_src"
    assert (src_dir / "th" / "index.md").is_file()
    assert not (src_dir / "index.md").exists()

    manifest_content = (src_dir / "drawlib.toml").read_text(encoding="utf-8")
    assert "[i18n]" in manifest_content
    assert 'default_lang = "th"' in manifest_content
    assert 'langs = ["th"]' in manifest_content

    template_content = (src_dir / "template.html").read_text(encoding="utf-8")
    assert "{{ html_lang | default('en') }}" in template_content
    assert "{{ html_dir | default('ltr') }}" in template_content
    assert "{{ font_link_html | default('') | safe }}" in template_content

    style_content = (src_dir / "style.css").read_text(encoding="utf-8")
    assert "Noto Sans Thai" in style_content


def test_cli_init_lang_invalid(tmp_path: Path) -> None:
    """Test `drawlib init project site --lang invalid` fails with helpful error."""
    res = run_drawlib_cli(["init", "project", "site", "--lang", "unknown_lang"], cwd=str(tmp_path))
    assert res.returncode != 0
    assert "Unsupported language 'unknown_lang'" in res.stderr


def test_cli_init_site_and_doc_multi_lang(tmp_path: Path) -> None:
    """Test unified i18n manifest/layout for doc, site, slide (single & multi-locale) and flat images."""
    for single_type, folder in [("doc", "s_doc"), ("site", "s_site"), ("slide", "s_slide")]:
        res_single = run_drawlib_cli(["init", "project", single_type, folder], cwd=str(tmp_path))
        assert res_single.returncode == 0
        manifest_text = (tmp_path / f"{folder}_src" / "drawlib.toml").read_text(encoding="utf-8")
        assert f'type = "{single_type}"' in manifest_text
        assert "[i18n]" in manifest_text
        assert 'default_lang = "en"' in manifest_text
        assert 'langs = ["en"]' in manifest_text
        assert '\nlang = "en"' not in manifest_text
        assert "[i18n.labels]" not in manifest_text

    res_imgs = run_drawlib_cli(["init", "project", "images", "s_imgs"], cwd=str(tmp_path))
    assert res_imgs.returncode == 0
    imgs_manifest = (tmp_path / "s_imgs_src" / "drawlib.toml").read_text(encoding="utf-8")
    assert 'type = "images"' in imgs_manifest
    assert 'lang = "en"' in imgs_manifest
    assert "[i18n]" not in imgs_manifest
    assert (tmp_path / "s_imgs_src" / "sample1.py").is_file()

    res = run_drawlib_cli(["init", "project", "site", "sub/portal", "-l", "en,ja"], cwd=str(tmp_path))
    assert res.returncode == 0
    assert "sub/portal_src/" in res.stdout

    src_dir = tmp_path / "sub" / "portal_src"
    assert (src_dir / "drawlib.toml").is_file()
    site_toml = (src_dir / "drawlib.toml").read_text(encoding="utf-8")
    assert 'type = "site"' in site_toml
    assert "[i18n]" in site_toml
    assert 'default_lang = "en"' in site_toml
    assert 'langs = ["en", "ja"]' in site_toml
    assert "[i18n.labels]" in site_toml
    assert (src_dir / "en" / "index.md").is_file()
    assert (src_dir / "ja" / "index.md").is_file()
    assert (src_dir / "en" / "navbar.md").is_file()
    assert (src_dir / "ja" / "navbar.md").is_file()

    res_doc = run_drawlib_cli(
        ["init", "project", "doc", "sub/whitepaper", "-l", "en,ja", "-s", "google"],
        cwd=str(tmp_path),
    )
    assert res_doc.returncode == 0
    doc_dir = tmp_path / "sub" / "whitepaper_src"
    assert (doc_dir / "drawlib.toml").is_file()
    doc_toml = (doc_dir / "drawlib.toml").read_text(encoding="utf-8")
    assert 'type = "doc"' in doc_toml
    assert 'style = "google"' in doc_toml
    assert "[i18n]" in doc_toml
    assert 'default_lang = "en"' in doc_toml
    assert 'langs = ["en", "ja"]' in doc_toml
    assert "[i18n.labels]" in doc_toml
    assert (doc_dir / "en" / "00_cover.md").is_file()
    assert (doc_dir / "ja" / "00_cover.md").is_file()
    assert not (doc_dir / "en" / "navbar.md").exists()

    res_slide = run_drawlib_cli(["init", "project", "slide", "sub/deck", "-l", "en,ja"], cwd=str(tmp_path))
    assert res_slide.returncode == 0
    slide_dir = tmp_path / "sub" / "deck_src"
    assert (slide_dir / "drawlib.toml").is_file()
    slide_toml = (slide_dir / "drawlib.toml").read_text(encoding="utf-8")
    assert 'type = "slide"' in slide_toml
    assert "[i18n]" in slide_toml
    assert 'default_lang = "en"' in slide_toml
    assert 'langs = ["en", "ja"]' in slide_toml
    assert "[i18n.labels]" in slide_toml
    assert 'en = "English"' in slide_toml
    assert 'ja = "日本語"' in slide_toml
    assert (slide_dir / "en" / "01_title.md").is_file()
    assert (slide_dir / "en" / "02_agenda.md").is_file()
    assert (slide_dir / "en" / "03_architecture.md").is_file()
    assert (slide_dir / "ja" / "01_title.md").is_file()
    assert (slide_dir / "ja" / "02_agenda.md").is_file()
    assert (slide_dir / "ja" / "03_architecture.md").is_file()

    # Images multi-lang should fail cleanly
    res_bad = run_drawlib_cli(["init", "project", "images", "-l", "en,ja"], cwd=str(tmp_path))
    assert res_bad.returncode != 0
    assert "supported for 'doc', 'site', and 'slide' projects, not 'images'" in res_bad.stderr
