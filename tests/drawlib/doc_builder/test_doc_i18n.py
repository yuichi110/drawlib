# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Unit and integration tests for drawlib.toml manifest and multi-locale (i18n) doc builds."""

from __future__ import annotations

import zipfile
from pathlib import Path
from unittest.mock import patch

import pytest

from drawlib._builder._common import find_project_manifest, load_project_manifest
from drawlib._builder.doc_builder import (
    build_docx,
    build_html,
    build_markdown,
    build_pdf,
    validate_i18n_project,
)
from drawlib._builder.doc_builder.processor import DrawlibBlockProcessor
from drawlib._builder.image_builder import build_image
from drawlib._http_server._link_scanner import scan_broken_links
from drawlib._slide import build_slide
from drawlib._templates import init_project


def test_project_manifest_parsing_and_ancestor_lookup(tmp_path: Path) -> None:
    """Verify drawlib.toml parsing across archetypes, validation errors, and ancestor lookup."""
    doc_dir = tmp_path / "report_src"
    init_project("doc", destination=tmp_path, target="report", lang="en,ja", style="google", force=True)

    manifest = load_project_manifest(str(doc_dir))
    assert manifest is not None
    assert manifest.project.type == "doc"
    assert manifest.project.style == "google"
    assert manifest.project.lang is None
    assert manifest.i18n is not None
    assert manifest.i18n.default_lang == "en"
    assert manifest.i18n.langs == ["en", "ja"]
    assert manifest.i18n.labels == {"en": "English", "ja": "日本語"}
    assert manifest.effective_lang == "en"

    # Ancestor lookup from nested chapter file
    found = find_project_manifest(str(doc_dir / "ja" / "01_overview.md"), max_up=3)
    assert found is not None
    assert Path(found[0]) == doc_dir.resolve()
    assert found[1].project.type == "doc"

    # Accept [i18n] and [i18n.labels] on slide projects
    slide_dir = tmp_path / "deck_src"
    (slide_dir / "en").mkdir(parents=True)
    (slide_dir / "ja").mkdir(parents=True)
    (slide_dir / "drawlib.toml").write_text(
        '[project]\ntype = "slide"\n\n[i18n]\ndefault_lang = "en"\nlangs = ["en", "ja"]\n\n'
        '[i18n.labels]\nen = "EN"\nja = "JP"\n',
        encoding="utf-8",
    )
    slide_manifest = load_project_manifest(str(slide_dir))
    assert slide_manifest is not None
    assert slide_manifest.project.type == "slide"
    assert slide_manifest.project.lang is None
    assert slide_manifest.i18n is not None
    assert slide_manifest.i18n.langs == ["en", "ja"]
    assert slide_manifest.i18n.labels == {"en": "EN", "ja": "JP"}

    # Require [i18n] on doc, site, and slide
    for req_type in ("doc", "site", "slide"):
        missing_i18n = tmp_path / f"missing_i18n_{req_type}_src"
        missing_i18n.mkdir()
        (missing_i18n / "drawlib.toml").write_text(f'[project]\ntype = "{req_type}"\n', encoding="utf-8")
        with pytest.raises(ValueError, match=r'require an "\[i18n\]" table'):
            load_project_manifest(str(missing_i18n))

    # Reject [project].lang on doc, site, and slide
    for bad_proj_lang_type in ("doc", "site", "slide"):
        bad_proj_lang = tmp_path / f"bad_proj_lang_{bad_proj_lang_type}_src"
        (bad_proj_lang / "en").mkdir(parents=True)
        (bad_proj_lang / "drawlib.toml").write_text(
            f'[project]\ntype = "{bad_proj_lang_type}"\nlang = "en"\n\n[i18n]\ndefault_lang = "en"\nlangs = ["en"]\n',
            encoding="utf-8",
        )
        with pytest.raises(ValueError, match=r'"\[project\]\.lang" is not supported'):
            load_project_manifest(str(bad_proj_lang))

    # Accept [project].lang on images and reject [i18n] on images
    imgs_dir = tmp_path / "imgs_src"
    imgs_dir.mkdir()
    (imgs_dir / "drawlib.toml").write_text('[project]\ntype = "images"\nlang = "ja"\n', encoding="utf-8")
    imgs_manifest = load_project_manifest(str(imgs_dir))
    assert imgs_manifest is not None
    assert imgs_manifest.project.type == "images"
    assert imgs_manifest.project.lang == "ja"
    assert imgs_manifest.i18n is None
    assert imgs_manifest.effective_lang == "ja"

    bad_imgs = tmp_path / "bad_imgs_src"
    (bad_imgs / "en").mkdir(parents=True)
    (bad_imgs / "drawlib.toml").write_text(
        '[project]\ntype = "images"\n\n[i18n]\ndefault_lang = "en"\nlangs = ["en"]\n',
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match='only supported for "doc", "site", and "slide" projects'):
        load_project_manifest(str(bad_imgs))

    # Reject unknown project.type
    bad_type = tmp_path / "bad_type_src"
    bad_type.mkdir()
    (bad_type / "drawlib.toml").write_text('[project]\ntype = "book"\n', encoding="utf-8")
    with pytest.raises(ValueError, match=r"\[project\]\.type.*must be one of"):
        load_project_manifest(str(bad_type))


def test_manifest_archetype_guardrails(tmp_path: Path) -> None:
    """Verify cross-archetype build commands raise clear errors when drawlib.toml specifies type."""
    init_project("site", destination=tmp_path, target="mysite", force=True)
    init_project("slide", destination=tmp_path, target="myslide", force=True)
    init_project("images", destination=tmp_path, target="myimgs", force=True)

    site_src = str(tmp_path / "mysite_src")
    slide_src = str(tmp_path / "myslide_src")
    imgs_src = str(tmp_path / "myimgs_src")

    with pytest.raises(ValueError, match='multi-page "site" project'):
        build_pdf(site_src, str(tmp_path / "out.pdf"))

    with pytest.raises(ValueError, match='multi-page "site" project'):
        build_docx(site_src, str(tmp_path / "out.docx"))

    with pytest.raises(ValueError, match='"slide" presentation project'):
        build_html(slide_src, str(tmp_path / "slide_out"))

    with pytest.raises(ValueError, match='"images" script project'):
        build_markdown(imgs_src, str(tmp_path / "md_out"))

    with pytest.raises(ValueError, match='not a "slide" presentation project'):
        build_slide(site_src, str(tmp_path / "bad_slide_out"))


def test_i18n_doc_rejects_navbar_md(tmp_path: Path) -> None:
    """Verify multi-locale doc validation rejects navbar.md inside locale directories."""
    init_project("doc", destination=tmp_path, target="spec", lang="en,ja", force=True)
    src_dir = tmp_path / "spec_src"
    manifest = load_project_manifest(str(src_dir))
    assert manifest is not None and manifest.i18n is not None

    nav_file = src_dir / "en" / "navbar.md"
    nav_file.write_text("# Unexpected Navbar\n- [Cover](00_cover.md)\n", encoding="utf-8")
    with pytest.raises(ValueError, match=r"\[i18n doc structure error\]"):
        validate_i18n_project(str(src_dir), manifest.i18n, project_type="doc")


def test_i18n_doc_end_to_end_all_outputs_and_per_locale_styles(tmp_path: Path) -> None:
    """Verify multi-locale doc HTML, Markdown, Image, DOCX, PDF, and per-locale styles.py overrides."""
    init_project("doc", destination=tmp_path, target="wp", lang="en,ja", style="google", force=True)
    src_dir = tmp_path / "wp_src"

    # Add a per-locale styles.py in ja/ patching FontJapanese onto GoogleStyles
    (src_dir / "ja" / "styles.py").write_text(
        "from drawlib.fonts import FontJapanese\n"
        "from drawlib.preset_colors import GoogleColors\n"
        "from drawlib.preset_styles import GoogleStyles\n\n"
        "Colors = GoogleColors()\n"
        "Styles = GoogleStyles().patch_font(\n"
        "    regular=FontJapanese.SANSSERIF_REGULAR,\n"
        "    bold=FontJapanese.SANSSERIF_BOLD,\n"
        "    thin=FontJapanese.SANSSERIF_THIN,\n"
        ")\n",
        encoding="utf-8",
    )

    # Localize 02_design.md in ja/ to use component_architecture_ja.png and assert FontJapanese is active
    ja_design = src_dir / "ja" / "02_design.md"
    ja_design_text = ja_design.read_text(encoding="utf-8")
    ja_design.write_text(
        ja_design_text.replace("file=component_architecture.png", "file=component_architecture_ja.png")
        .replace(
            "from drawlib.styles import Styles",
            "from drawlib.fonts import FontJapanese\nfrom drawlib.styles import Styles\n"
            "assert Styles.Neutral.text_font == FontJapanese.SANSSERIF_REGULAR",
        )
        .replace(
            'title="Web Client"',
            'title="クライアント"',
        ),
        encoding="utf-8",
    )

    # 1. HTML build: deduplication + TOC localization + switcher + zero broken links
    out_html = tmp_path / "wp_html"
    orig_exec = DrawlibBlockProcessor._exec_code_block
    exec_count = 0

    def _counting_exec(
        code: str,
        source_filename: str = "<drawlib_block>",
        shared_globals: dict[str, object] | None = None,
    ) -> None:
        nonlocal exec_count
        exec_count += 1
        orig_exec(code=code, source_filename=source_filename, shared_globals=shared_globals)

    with patch.object(DrawlibBlockProcessor, "_exec_code_block", staticmethod(_counting_exec)):
        build_html(str(src_dir), str(out_html), no_cache=True)

    # 2 diagrams in en (system_overview.png + component_architecture.png) + 1 localized diagram in ja = 3 executions!
    assert exec_count == 3

    assert (out_html / "index.html").is_file()
    assert (out_html / "en" / "index.html").is_file()
    assert (out_html / "ja" / "index.html").is_file()
    assert (out_html / "en" / "style.css").is_file()
    assert (out_html / "ja" / "style.css").is_file()
    assert (out_html / "images" / "01_overview" / "system_overview.png").is_file()
    assert (out_html / "images" / "02_design" / "component_architecture.png").is_file()
    assert (out_html / "images" / "02_design" / "component_architecture_ja.png").is_file()

    en_html = (out_html / "en" / "index.html").read_text(encoding="utf-8")
    ja_html = (out_html / "ja" / "index.html").read_text(encoding="utf-8")
    root_html = (out_html / "index.html").read_text(encoding="utf-8")

    assert "<h2>Table of Contents</h2>" in en_html
    assert "<h2>目次</h2>" in ja_html
    assert 'class="lang-switcher"' in en_html
    assert 'class="lang-switcher"' in ja_html
    assert 'href="../ja/index.html"' in en_html
    assert 'href="../en/index.html"' in ja_html
    assert 'src="../images/01_overview/system_overview.png"' in en_html
    assert 'src="../images/01_overview/system_overview.png"' in ja_html
    assert 'src="../images/02_design/component_architecture_ja.png"' in ja_html
    assert 'src="images/01_overview/system_overview.png"' in root_html
    assert 'href="ja/index.html"' in root_html

    html_count, total_links, broken_errors = scan_broken_links(str(out_html))
    assert html_count == 3
    assert total_links >= 10
    assert broken_errors == []

    # 2. Markdown build: <out_md>/<lang>/*.md without root index.md
    out_md = tmp_path / "wp_markdown"
    build_markdown(str(src_dir), str(out_md))
    assert not (out_md / "index.md").exists()
    assert (out_md / "en" / "01_overview.md").is_file()
    assert (out_md / "ja" / "02_design.md").is_file()
    assert (out_md / "images" / "02_design" / "component_architecture_ja.png").is_file()

    # 3. Image build: <out_imgs>/<chapter_stem>/*.png
    out_imgs = tmp_path / "wp_images"
    build_image(str(src_dir), str(out_imgs))
    assert (out_imgs / "01_overview" / "system_overview.png").is_file()
    assert (out_imgs / "02_design" / "component_architecture.png").is_file()
    assert (out_imgs / "02_design" / "component_architecture_ja.png").is_file()

    # 4. DOCX build: generates wp_en.docx and wp_ja.docx with localized TOC headings
    default_docx = build_docx(str(src_dir), str(tmp_path / "wp.docx"), generate_index=True)
    en_docx = tmp_path / "wp_en.docx"
    ja_docx = tmp_path / "wp_ja.docx"
    assert Path(default_docx) == en_docx
    assert en_docx.is_file()
    assert ja_docx.is_file()

    with zipfile.ZipFile(en_docx) as z_en:
        en_doc_xml = z_en.read("word/document.xml").decode("utf-8")
    with zipfile.ZipFile(ja_docx) as z_ja:
        ja_doc_xml = z_ja.read("word/document.xml").decode("utf-8")
    assert "Table of Contents" in en_doc_xml
    assert "目次" in ja_doc_xml

    # 5. PDF build (mocking Playwright Chromium export to inspect rendered HTML per locale)
    captured_pdf_html: dict[str, str] = {}

    def _fake_export_pdf(html_content: str, output_path: str, timestamp: bool = False) -> None:
        captured_pdf_html[Path(output_path).name] = html_content
        Path(output_path).write_bytes(b"%PDF-1.4\n%%EOF\n")

    with patch("drawlib._builder.doc_builder.compiler.pdf.export_html_to_pdf", side_effect=_fake_export_pdf):
        default_pdf = build_pdf(str(src_dir), str(tmp_path / "wp.pdf"), generate_index=True)

    assert Path(default_pdf) == tmp_path / "wp_en.pdf"
    assert (tmp_path / "wp_en.pdf").is_file()
    assert (tmp_path / "wp_ja.pdf").is_file()
    assert "<h2>Table of Contents</h2>" in captured_pdf_html["wp_en.pdf"]
    assert "<h2>目次</h2>" in captured_pdf_html["wp_ja.pdf"]
    assert "Noto Sans JP" in captured_pdf_html["wp_ja.pdf"]
    assert 'class="lang-switcher"' not in captured_pdf_html["wp_ja.pdf"]

    # Passing a locale subdirectory directly must raise a clear error pointing to project root
    with pytest.raises(ValueError, match="is a subdirectory inside project"):
        build_pdf(str(src_dir / "ja"), str(tmp_path / "single_ja.pdf"), generate_index=True)


def test_single_locale_ja_doc_and_legacy_without_manifest(tmp_path: Path) -> None:
    """Verify single-locale Japanese doc outputs jadoc_ja.{pdf,docx} & ja/index.html, and requires drawlib.toml."""
    init_project("doc", destination=tmp_path, target="jadoc", lang="ja", force=True)
    ja_src = tmp_path / "jadoc_src"
    for starter_md in (ja_src / "ja").glob("*.md"):
        starter_md.unlink()
    (ja_src / "ja" / "00_cover.md").write_text("# 設計書\n\n概要リード文。\n", encoding="utf-8")
    (ja_src / "ja" / "01_body.md").write_text("# システム構成\n\n本文セクション。\n", encoding="utf-8")

    ja_html_dir = tmp_path / "jadoc_html"
    build_html(str(ja_src), str(ja_html_dir))
    assert (ja_html_dir / "ja" / "index.html").is_file()
    assert (ja_html_dir / "index.html").is_file()
    ja_index = (ja_html_dir / "ja" / "index.html").read_text(encoding="utf-8")
    assert "<h2>目次</h2>" in ja_index
    assert '<html lang="ja" dir="ltr">' in ja_index
    assert 'class="lang-switcher"' not in ja_index

    ja_docx = build_docx(str(ja_src), generate_index=True)
    assert Path(ja_docx) == tmp_path / "jadoc_ja.docx"
    assert (tmp_path / "jadoc_ja.docx").is_file()

    captured_ja_pdf: dict[str, str] = {}

    def _fake_ja_pdf(html_content: str, output_path: str, timestamp: bool = False) -> None:
        captured_ja_pdf[Path(output_path).name] = html_content
        Path(output_path).write_bytes(b"%PDF-1.4\n%%EOF\n")

    with patch("drawlib._builder.doc_builder.compiler.pdf.export_html_to_pdf", side_effect=_fake_ja_pdf):
        ja_pdf = build_pdf(str(ja_src), generate_index=True)
    assert Path(ja_pdf) == tmp_path / "jadoc_ja.pdf"
    assert (tmp_path / "jadoc_ja.pdf").is_file()
    assert "<h2>目次</h2>" in captured_ja_pdf["jadoc_ja.pdf"]

    # Removing drawlib.toml raises ValueError across directory builders
    (ja_src / "drawlib.toml").unlink()
    with pytest.raises(ValueError, match='Missing required "drawlib.toml"'):
        build_html(str(ja_src), str(tmp_path / "legacy_html"))
    with pytest.raises(ValueError, match='Missing required "drawlib.toml"'):
        build_docx(str(ja_src))
    with pytest.raises(ValueError, match='Missing required "drawlib.toml"'):
        build_pdf(str(ja_src))
