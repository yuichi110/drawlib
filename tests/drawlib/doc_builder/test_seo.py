# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Unit, integration, and security tests for project-level SEO, OGP, sitemap.xml, robots.txt, and llms.txt."""

from __future__ import annotations

import os
import xml.etree.ElementTree as ET
from pathlib import Path

import pytest
from PIL import Image

from drawlib._builder._common import (
    PageSeoMetadata,
    SeoConfig,
    SitemapEntry,
    extract_markdown_description,
    format_project_manifest_toml,
    load_project_manifest,
    render_seo_head_tags,
    resolve_public_page_url,
    to_og_locale,
    write_sitemap_xml,
)
from drawlib._builder.doc_builder import build_html
from drawlib._http_server._link_scanner import scan_broken_links
from drawlib._slide.compiler import build_slide
from drawlib._templates import init_project


def _write_dummy_png(path: Path, size: tuple[int, int] = (120, 63)) -> None:
    """Create a small valid RGB PNG image at ``path``."""
    path.parent.mkdir(parents=True, exist_ok=True)
    img = Image.new("RGB", size, color=(26, 115, 232))
    img.save(path, format="PNG")


def test_seo_manifest_parsing_and_roundtrip(tmp_path: Path) -> None:
    """Verify [seo] and [i18n.descriptions] parse cleanly and round-trip via format_project_manifest_toml."""
    proj_dir = tmp_path / "site_src"
    (proj_dir / "en").mkdir(parents=True)
    (proj_dir / "ja").mkdir(parents=True)
    _write_dummy_png(proj_dir / "_assets" / "ogp.png")

    (proj_dir / "drawlib.toml").write_text(
        '[project]\n'
        'type = "site"\n'
        'title = "Drawlib Docs"\n'
        'description = "Fallback project summary."\n\n'
        '[i18n]\n'
        'default_lang = "en"\n'
        'langs = ["en", "jp"]\n\n'
        '[i18n.descriptions]\n'
        'en = "English SEO summary."\n'
        'jp = "日本語の SEO 概要。"\n\n'
        '[seo]\n'
        'site_url = "https://www.drawlib.com/"\n'
        'og_image = "_assets/ogp.png"\n'
        'twitter_card = "summary_large_image"\n'
        'twitter_site = "drawlib"\n'
        'sitemap = true\n'
        'robots = true\n'
        'llms_txt = true\n',
        encoding="utf-8",
    )

    manifest = load_project_manifest(str(proj_dir))
    assert manifest is not None
    assert manifest.i18n is not None
    assert manifest.i18n.descriptions == {
        "en": "English SEO summary.",
        "ja": "日本語の SEO 概要。",
    }
    assert manifest.seo is not None
    assert manifest.seo.site_url == "https://www.drawlib.com"
    assert manifest.seo.og_image == "_assets/ogp.png"
    assert manifest.seo.twitter_card == "summary_large_image"
    assert manifest.seo.twitter_site == "@drawlib"
    assert manifest.seo.sitemap is True
    assert manifest.seo.robots is True
    assert manifest.seo.llms_txt is True

    serialized = format_project_manifest_toml(
        name="round",
        project_type=manifest.project.type,
        style=manifest.project.style,
        lang=manifest.i18n.default_lang,
        langs=manifest.i18n.langs,
        descriptions=manifest.i18n.descriptions,
        title=manifest.project.title,
        description=manifest.project.description,
        seo=manifest.seo,
    )
    round_dir = tmp_path / "round_src"
    (round_dir / "en").mkdir(parents=True)
    (round_dir / "ja").mkdir(parents=True)
    _write_dummy_png(round_dir / "_assets" / "ogp.png")
    (round_dir / "drawlib.toml").write_text(serialized, encoding="utf-8")

    reloaded = load_project_manifest(str(round_dir))
    assert reloaded is not None
    assert reloaded.i18n == manifest.i18n
    assert reloaded.seo == manifest.seo


def test_init_project_scaffolds_commented_seo_template(tmp_path: Path) -> None:
    """Verify drawlib init project adds commented # [seo] hints on site/doc/slide, not images."""
    for ptype in ("site", "doc", "slide"):
        target_dir = tmp_path / f"{ptype}_src"
        init_project(ptype, destination=tmp_path, target=target_dir.name, lang="en,ja", force=True)
        toml_text = (target_dir / "drawlib.toml").read_text(encoding="utf-8")
        assert "# [seo]" in toml_text
        loaded = load_project_manifest(str(target_dir))
        assert loaded is not None
        assert loaded.seo is None

    img_dir = tmp_path / "images_src"
    init_project("images", destination=tmp_path, target=img_dir.name, lang="en", force=True)
    img_toml = (img_dir / "drawlib.toml").read_text(encoding="utf-8")
    assert "[seo]" not in img_toml


def test_seo_manifest_validation_and_security_guards(tmp_path: Path) -> None:
    """Verify strict validation blocks path traversal, unsafe URLs, unknown keys, and disallowed archetypes."""
    base = tmp_path / "sec_src"
    (base / "en").mkdir(parents=True)

    # 1. [seo] rejected on images project
    (base / "drawlib.toml").write_text(
        '[project]\ntype = "images"\nlang = "en"\n\n[seo]\nsite_url = "https://example.com"\n',
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match=r'"\[seo\]" is only supported for'):
        load_project_manifest(str(base))

    # 2. Unknown key in [seo]
    (base / "drawlib.toml").write_text(
        '[project]\ntype = "site"\n\n[i18n]\ndefault_lang = "en"\nlangs = ["en"]\n\n[seo]\nunknown_key = true\n',
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match=r"unknown key\(s\)"):
        load_project_manifest(str(base))

    # 3. Unsafe schemes and query/fragment in site_url
    for bad_url in (
        "javascript:alert(1)",
        "file:///etc/passwd",
        "ftp://example.com",
        "https://example.com?foo=1",
        "https://example.com#frag",
        'https://example.com/"><script>',
    ):
        (base / "drawlib.toml").write_text(
            f'[project]\ntype = "site"\n\n[i18n]\ndefault_lang = "en"\nlangs = ["en"]\n\n'
            f'[seo]\nsite_url = \'{bad_url}\'\n',
            encoding="utf-8",
        )
        with pytest.raises(ValueError, match="site_url"):
            load_project_manifest(str(base))

    # 4. Path traversal, absolute path, scheme injection, and missing file on og_image
    outside_secret = tmp_path / "secret.png"
    _write_dummy_png(outside_secret)
    for bad_img in ("../secret.png", "/etc/passwd", "javascript:alert(1)", "data:image/png;base64,AAA", "missing.png"):
        (base / "drawlib.toml").write_text(
            f'[project]\ntype = "site"\n\n[i18n]\ndefault_lang = "en"\nlangs = ["en"]\n\n'
            f'[seo]\nog_image = "{bad_img}"\n',
            encoding="utf-8",
        )
        with pytest.raises(ValueError, match="og_image"):
            load_project_manifest(str(base))

    # 5. Symlink escape outside project root blocked on og_image
    if hasattr(os, "symlink"):
        escape_link = base / "_assets" / "escape.png"
        escape_link.parent.mkdir(parents=True, exist_ok=True)
        escape_link.symlink_to(outside_secret)
        (base / "drawlib.toml").write_text(
            '[project]\ntype = "site"\n\n[i18n]\ndefault_lang = "en"\nlangs = ["en"]\n\n'
            '[seo]\nog_image = "_assets/escape.png"\n',
            encoding="utf-8",
        )
        with pytest.raises(ValueError, match="path traversal outside project root"):
            load_project_manifest(str(base))

    # 6. Invalid twitter_card, twitter_site, and [i18n.descriptions] language not in langs
    (base / "drawlib.toml").write_text(
        '[project]\ntype = "site"\n\n[i18n]\ndefault_lang = "en"\nlangs = ["en"]\n\n'
        '[seo]\ntwitter_site = "><script>alert(1)</script>"\n',
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="twitter_site"):
        load_project_manifest(str(base))

    (base / "drawlib.toml").write_text(
        '[project]\ntype = "site"\n\n[i18n]\ndefault_lang = "en"\nlangs = ["en"]\n\n'
        '[i18n.descriptions]\nfr = "French not in langs"\n',
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match=r"i18n\.descriptions"):
        load_project_manifest(str(base))


def test_extract_markdown_description_and_xss_xml_escaping(tmp_path: Path) -> None:
    """Verify Markdown summary extraction and strict HTML/XML escaping against injection."""
    md_sample = (
        "<!-- comment -->\n"
        "# Main Page Heading\n\n"
        "```drawlib file=hero.png\n"
        "setup(width=100, height=50)\n"
        "```\n\n"
        "::: note\n"
        "Speaker notes that must never leak into meta descriptions.\n"
        ":::\n\n"
        "::: block xy=(80, 140) width=1760 height=840\n"
        "Drawlib is a **pure-Python** library for [Illustration as Code](https://www.drawlib.com) "
        "using `setup()` & declarative components.\n"
        ":::\n"
    )
    desc = extract_markdown_description(md_sample)
    assert desc == (
        "Drawlib is a pure-Python library for Illustration as Code using setup() & declarative components."
    )
    assert "Speaker notes" not in desc
    assert "hero.png" not in desc

    meta = PageSeoMetadata(
        title='Page "Title" <script>alert(1)</script>',
        og_title='Page "Title" <script>alert(1)</script> — Site & Brand',
        description='Summary with "quotes" & <img src=x onerror=alert(1)>',
        site_name='Site & "Brand"',
        canonical_url="https://www.drawlib.com/en/",
        og_image_url="https://www.drawlib.com/_assets/ogp.png",
        og_locale=to_og_locale("ja"),
        og_alternate_locales=(to_og_locale("en"),),
        twitter_card="summary_large_image",
        twitter_site="@drawlib",
    )
    tags = render_seo_head_tags(meta)
    assert "<script>" not in tags
    assert "<img" not in tags
    assert "&lt;script&gt;alert(1)&lt;/script&gt;" in tags
    assert "&quot;quotes&quot;" in tags
    assert 'content="ja_JP"' in tags
    assert 'content="en_US"' in tags

    sitemap_path = write_sitemap_xml(
        str(tmp_path),
        [
            SitemapEntry(
                loc="https://www.drawlib.com/en/a&b.html",
                alternates=(("en", 'https://www.drawlib.com/en/a&b.html'),),
            ),
            SitemapEntry(loc="https://www.drawlib.com/en/a&b.html"),
        ],
    )
    xml_text = Path(sitemap_path).read_text(encoding="utf-8")
    root = ET.fromstring(xml_text)  # noqa: S314
    ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    urls = root.findall("sm:url", ns)
    assert len(urls) == 1
    assert resolve_public_page_url("https://www.drawlib.com/", "index.html") == "https://www.drawlib.com/"
    assert resolve_public_page_url("https://www.drawlib.com", "en/index.html") == "https://www.drawlib.com/en/"
    assert (
        resolve_public_page_url("https://www.drawlib.com", "en/guide/intro.html")
        == "https://www.drawlib.com/en/guide/intro.html"
    )


def test_site_build_emits_seo_ogp_sitemap_robots_and_llms_txt(tmp_path: Path) -> None:
    """Verify end-to-end site build with [seo] generates full OGP, canonicals, sitemap.xml, robots.txt, and llms.txt."""
    src_dir = tmp_path / "site_src"
    out_dir = tmp_path / "site_html"
    init_project("site", destination=tmp_path, target=src_dir.name, lang="en,ja", force=True)
    _write_dummy_png(src_dir / "_assets" / "ogp.png")

    toml_str = format_project_manifest_toml(
        name="site",
        project_type="site",
        lang="en",
        langs=["en", "ja"],
        labels={"en": "English", "ja": "日本語"},
        descriptions={
            "en": "Declarative Python diagramming and documentation for AI agents.",
            "ja": "AI エージェントのための Python 図解・ドキュメント生成ライブラリ。",
        },
        title="Drawlib Official",
        description="Default fallback.",
        seo=SeoConfig(
            site_url="https://www.drawlib.com",
            og_image="_assets/ogp.png",
            twitter_card="summary_large_image",
            twitter_site="@drawlib",
            sitemap=True,
            robots=True,
            llms_txt=True,
        ),
    )
    (src_dir / "drawlib.toml").write_text(toml_str, encoding="utf-8")

    build_html(str(src_dir), str(out_dir))

    # Verify OGP banner asset copied
    assert (out_dir / "_assets" / "ogp.png").is_file()

    # Root index.html & localized pages
    root_html = (out_dir / "index.html").read_text(encoding="utf-8")
    en_html = (out_dir / "en" / "index.html").read_text(encoding="utf-8")
    ja_html = (out_dir / "ja" / "index.html").read_text(encoding="utf-8")
    sub_en_html = (out_dir / "en" / "architecture" / "index.html").read_text(encoding="utf-8")

    assert '<link rel="canonical" href="https://www.drawlib.com/">' in root_html
    assert '<link rel="canonical" href="https://www.drawlib.com/en/">' in en_html
    assert '<link rel="canonical" href="https://www.drawlib.com/ja/">' in ja_html
    assert '<link rel="canonical" href="https://www.drawlib.com/en/architecture/">' in sub_en_html

    assert 'content="Declarative Python diagramming and documentation for AI agents."' in en_html
    assert 'content="AI エージェントのための Python 図解・ドキュメント生成ライブラリ。"' in ja_html
    assert '<meta property="og:image" content="https://www.drawlib.com/_assets/ogp.png">' in en_html
    assert '<meta name="twitter:card" content="summary_large_image">' in en_html
    assert '<meta name="twitter:site" content="@drawlib">' in en_html

    # hreflang in <head> is upgraded to canonical URLs, while UI dropdown links remain relative
    assert '<link rel="alternate" hreflang="en" href="https://www.drawlib.com/en/">' in en_html
    assert '<link rel="alternate" hreflang="ja" href="https://www.drawlib.com/ja/">' in en_html
    assert '<link rel="alternate" hreflang="x-default" href="https://www.drawlib.com/">' in en_html
    assert 'href="../ja/index.html"' in en_html

    # sitemap.xml, robots.txt, llms.txt
    sitemap_xml = (out_dir / "sitemap.xml").read_text(encoding="utf-8")
    ET.fromstring(sitemap_xml)  # noqa: S314
    assert "<loc>https://www.drawlib.com/</loc>" in sitemap_xml
    assert "<loc>https://www.drawlib.com/en/</loc>" in sitemap_xml
    assert "<loc>https://www.drawlib.com/ja/</loc>" in sitemap_xml
    assert "<loc>https://www.drawlib.com/en/architecture/</loc>" in sitemap_xml

    robots_txt = (out_dir / "robots.txt").read_text(encoding="utf-8")
    assert "User-agent: *" in robots_txt
    assert "Sitemap: https://www.drawlib.com/sitemap.xml" in robots_txt

    llms_txt = (out_dir / "llms.txt").read_text(encoding="utf-8")
    assert llms_txt.startswith("# Drawlib Official\n")
    assert "> Declarative Python diagramming and documentation for AI agents." in llms_txt
    assert "https://www.drawlib.com/en/architecture/" in llms_txt
    assert "## Locales" in llms_txt

    # Broken link scanner passes with 0 errors
    _, _, broken = scan_broken_links(str(out_dir))
    assert broken == []


def test_doc_and_slide_builds_emit_seo_and_preserve_backward_compat(tmp_path: Path) -> None:
    """Verify doc and slide builds emit SEO/OGP/sitemap/llms.txt, and omitting [seo] emits none."""
    # 1. doc project with [seo]
    doc_src = tmp_path / "doc_src"
    doc_out = tmp_path / "doc_html"
    init_project("doc", destination=tmp_path, target=doc_src.name, lang="en,ja", force=True)
    _write_dummy_png(doc_src / "_assets" / "ogp.png")
    (doc_src / "drawlib.toml").write_text(
        '[project]\n'
        'type = "doc"\n'
        'title = "Architecture Whitepaper"\n\n'
        '[i18n]\n'
        'default_lang = "en"\n'
        'langs = ["en", "ja"]\n\n'
        '[i18n.descriptions]\n'
        'en = "Whitepaper English summary."\n'
        'ja = "ホワイトペーパー日本語概要。"\n\n'
        '[seo]\n'
        'site_url = "https://doc.drawlib.com"\n'
        'og_image = "_assets/ogp.png"\n',
        encoding="utf-8",
    )
    build_html(str(doc_src), str(doc_out))
    assert '<link rel="canonical" href="https://doc.drawlib.com/en/">' in (
        doc_out / "en" / "index.html"
    ).read_text(encoding="utf-8")
    assert "#chapter-" in (doc_out / "llms.txt").read_text(encoding="utf-8")
    assert (doc_out / "sitemap.xml").is_file()
    assert (doc_out / "robots.txt").is_file()
    assert scan_broken_links(str(doc_out))[2] == []

    # 2. slide project with [seo] (including root redirect OGP card!)
    slide_src = tmp_path / "slide_src"
    slide_out = tmp_path / "slide_html"
    init_project("slide", destination=tmp_path, target=slide_src.name, lang="en,ja", force=True)
    _write_dummy_png(slide_src / "_assets" / "ogp.png")
    (slide_src / "drawlib.toml").write_text(
        '[project]\n'
        'type = "slide"\n'
        'title = "Drawlib Pitch Deck"\n\n'
        '[i18n]\n'
        'default_lang = "en"\n'
        'langs = ["en", "ja"]\n\n'
        '[i18n.descriptions]\n'
        'en = "Interactive 16:9 HTML slide deck."\n'
        'ja = "16:9 インタラクティブ HTML スライドデッキ。"\n\n'
        '[seo]\n'
        'site_url = "https://slide.drawlib.com"\n'
        'og_image = "_assets/ogp.png"\n',
        encoding="utf-8",
    )
    build_slide(str(slide_src), str(slide_out))

    slide_root_html = (slide_out / "index.html").read_text(encoding="utf-8")
    slide_en_html = (slide_out / "en" / "index.html").read_text(encoding="utf-8")
    slide_sitemap = (slide_out / "sitemap.xml").read_text(encoding="utf-8")
    slide_llms = (slide_out / "llms.txt").read_text(encoding="utf-8")

    # Root redirect has canonical -> /en/ AND full OGP tags for SNS card previews
    assert '<link rel="canonical" href="https://slide.drawlib.com/en/">' in slide_root_html
    assert '<meta property="og:image" content="https://slide.drawlib.com/_assets/ogp.png">' in slide_root_html
    assert '<meta property="og:title"' in slide_en_html
    assert "<loc>https://slide.drawlib.com/en/</loc>" in slide_sitemap
    assert "<loc>https://slide.drawlib.com/ja/</loc>" in slide_sitemap
    assert "<loc>https://slide.drawlib.com/</loc>" not in slide_sitemap
    assert "https://slide.drawlib.com/en/#1" in slide_llms
    assert scan_broken_links(str(slide_out))[2] == []

    # 3. Backward compatibility: project without [seo] emits no SEO files
    plain_src = tmp_path / "plain_site_src"
    plain_out = tmp_path / "plain_site_html"
    init_project("site", destination=tmp_path, target=plain_src.name, lang="en", force=True)
    build_html(str(plain_src), str(plain_out))
    assert not (plain_out / "sitemap.xml").exists()
    assert not (plain_out / "robots.txt").exists()
    assert not (plain_out / "llms.txt").exists()
    assert '<meta property="og:title"' not in (plain_out / "en" / "index.html").read_text(encoding="utf-8")
