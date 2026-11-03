# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Unit and integration tests for the ``api`` project archetype."""

from __future__ import annotations

import re
from pathlib import Path

import pytest

from drawlib._builder._common import format_project_manifest_toml, load_project_manifest
from drawlib._builder.doc_builder.api_nav import (
    extract_api_headings,
    inject_api_heading_ids_and_badges,
)
from drawlib._http_server._link_scanner import scan_broken_links
from drawlib.tools import (
    build_docx,
    build_html,
    build_image,
    build_markdown,
    build_pdf,
    get_css,
    init_project,
    list_css,
    list_project_types,
)


def test_api_manifest_parsing_and_defaults(tmp_path: Path) -> None:
    """Verify [api] defaults, localized badges/links, and security validation in drawlib.toml."""
    # Omitted [api] section defaults to ApiConfig(sidebar_expanded=True)
    minimal_dir = tmp_path / "min_api"
    (minimal_dir / "en").mkdir(parents=True)
    (minimal_dir / "drawlib.toml").write_text(
        '[project]\nname = "demo"\ntype = "api"\n\n[i18n]\ndefault_lang = "en"\nlangs = ["en"]\n',
        encoding="utf-8",
    )
    m_min = load_project_manifest(str(minimal_dir))
    assert m_min is not None
    assert m_min.project.type == "api"
    assert m_min.api is not None
    assert m_min.api.sidebar_expanded is True
    assert m_min.api.badge_text is None
    assert m_min.api.repo_url is None
    assert m_min.api.header_links == ()

    # Rich [api] section with localized badge_text and header_links
    rich_dir = tmp_path / "rich_api"
    (rich_dir / "en").mkdir(parents=True)
    (rich_dir / "ja").mkdir(parents=True)
    (rich_dir / "drawlib.toml").write_text(
        '[project]\nname = "sdk"\ntitle = "SDK API"\ntype = "api"\n\n'
        '[i18n]\ndefault_lang = "en"\nlangs = ["en", "ja"]\n\n'
        "[api]\n"
        "sidebar_expanded = false\n"
        'badge_text = { en = "v2.1 Stable", ja = "v2.1 安定版" }\n'
        'badge_url = "https://example.com/releases"\n'
        'repo_url = "https://github.com/example/sdk"\n'
        "header_links = [\n"
        '  { label = { en = "Guides", ja = "ガイド" }, url = "https://docs.example.com" },\n'
        '  { label = "Changelog", url = "00_overview.html#changelog" },\n'
        "]\n",
        encoding="utf-8",
    )
    m_rich = load_project_manifest(str(rich_dir))
    assert m_rich is not None and m_rich.api is not None
    assert m_rich.api.sidebar_expanded is False
    assert m_rich.api.resolve_badge_text("en") == "v2.1 Stable"
    assert m_rich.api.resolve_badge_text("ja") == "v2.1 安定版"
    assert m_rich.api.badge_url == "https://example.com/releases"
    assert m_rich.api.repo_url == "https://github.com/example/sdk"
    assert len(m_rich.api.header_links) == 2
    assert m_rich.api.header_links[0].resolve_label("ja") == "ガイド"
    assert m_rich.api.header_links[0].is_external is True
    assert m_rich.api.header_links[1].is_external is False

    # Verify generated TOML includes [api] sidebar_expanded = true
    toml_out = format_project_manifest_toml(name="myapi", project_type="api", langs=["en"])
    assert 'type = "api"' in toml_out
    assert "[api]" in toml_out
    assert "sidebar_expanded = true" in toml_out


@pytest.mark.parametrize(
    ("bad_toml", "expected_msg"),
    [
        (
            '[project]\ntype = "site"\n[i18n]\ndefault_lang = "en"\nlangs = ["en"]\n[api]\nsidebar_expanded = true\n',
            'only supported for "api" projects',
        ),
        (
            '[project]\ntype = "api"\n[i18n]\ndefault_lang = "en"\nlangs = ["en"]\n[api]\nunknown_key = 1\n',
            r'unknown key\(s\).*in "\[api\]"',
        ),
        (
            '[project]\ntype = "api"\n[i18n]\ndefault_lang = "en"\nlangs = ["en"]\n'
            '[api]\nbadge_text = "v1"\nbadge_url = "javascript:alert(1)"\n',
            r"must be an http\(s\):// URL or safe relative path",
        ),
        (
            '[project]\ntype = "api"\n[i18n]\ndefault_lang = "en"\nlangs = ["en"]\n'
            '[api]\nheader_links = [{ label = "XSS", '
            'url = "data:text/html;base64,PHNjcmlwdD5hbGVydCgxKTwvc2NyaXB0Pg==" }]\n',
            r"must be an http\(s\):// URL or safe relative path",
        ),
        (
            '[project]\ntype = "api"\n[i18n]\ndefault_lang = "en"\nlangs = ["en"]\n'
            '[api]\nheader_links = [{ label = "AttrXSS", url = "https://example.com/><script>" }]\n',
            "contains unsafe whitespace or quote/angle characters",
        ),
        (
            '[project]\ntype = "api"\n[i18n]\ndefault_lang = "en"\nlangs = ["en"]\n'
            '[api]\nheader_links = [{ label = "ProtoRel", url = "//evil.example.com" }]\n',
            r"must be an http\(s\):// URL or safe relative path",
        ),
        (
            '[project]\ntype = "api"\n[i18n]\ndefault_lang = "en"\nlangs = ["en"]\n[api]\nrepo_url = "../relative"\n',
            "must be an http:// or https:// URL",
        ),
    ],
)
def test_api_manifest_rejects_invalid_and_unsafe_configs(
    tmp_path: Path,
    bad_toml: str,
    expected_msg: str,
) -> None:
    """Verify [api] rejects unsafe URL schemes, non-api archetypes, and unknown keys."""
    proj_dir = tmp_path / "bad_proj"
    (proj_dir / "en").mkdir(parents=True)
    (proj_dir / "drawlib.toml").write_text(bad_toml, encoding="utf-8")
    with pytest.raises(ValueError, match=expected_msg):
        load_project_manifest(str(proj_dir))


def test_extract_api_headings_and_xss_angle_safety() -> None:
    """Verify fence masking, badge extraction, slug deduplication, <id> preservation, and XSS escaping."""
    md = (
        "# drawlib.shapes <script>alert(1)</script>\n\n"
        "<!-- ## `GET` /commented/out -->\n\n"
        "```python\n"
        "# Not an H1\n"
        "## `def` ignored_in_code_block()\n"
        "```\n\n"
        "```drawlib file=demo.png\n"
        "# Ignored in drawlib fence\n"
        "## `POST` /ignored\n"
        "```\n\n"
        "## `def` rectangle(xy, width, height)\n\n"
        "## `def` rectangle(xy, size)\n\n"
        "## `GET` /v1/users/<id>\n\n"
        '## `POST` "><img src=x onerror=alert(1)>\n\n'
        "### Parameters <T>\n"
    )
    extracted = extract_api_headings(md, fallback_stem="shapes")
    assert extracted.h1_title == "drawlib.shapes <script>alert(1)</script>"
    assert len(extracted.h2_items) == 4

    assert extracted.h2_items[0].badge_kind == "def"
    assert extracted.h2_items[0].slug == "rectangle"
    assert extracted.h2_items[0].sidebar_label == "rectangle()"

    # Duplicate signature deduplicates cleanly with -2
    assert extracted.h2_items[1].slug == "rectangle-2"

    # Angle-bracket placeholder preserved intact
    assert extracted.h2_items[2].badge_kind == "get"
    assert extracted.h2_items[2].raw_title == "/v1/users/<id>"
    assert extracted.h2_items[2].slug == "v1-users-id"

    # Malicious HTML payload treated as literal text
    assert extracted.h2_items[3].badge_kind == "post"
    assert "<img" in extracted.h2_items[3].raw_title

    raw_body = (
        "<h1>drawlib.shapes <script>alert(1)</script></h1>\n"
        "<pre><code><h2>not touched</h2></code></pre>\n"
        "<h2><code>def</code> rectangle(xy, width, height)</h2>\n"
        "<h2><code>def</code> rectangle(xy, size)</h2>\n"
        "<h2><code>GET</code> /v1/users/<id></h2>\n"
        '<h2><code>POST</code> "><img src=x onerror=alert(1)></h2>\n'
        "<h3>Parameters <T></h3>\n"
    )
    _, upgraded, subitems = inject_api_heading_ids_and_badges(raw_body, md, fallback_stem="shapes")
    assert len(subitems) == 4
    assert "<script>" not in upgraded
    assert "&lt;script&gt;alert(1)&lt;/script&gt;" in upgraded
    assert "<img src=x" not in upgraded
    assert "&lt;img src=x onerror=alert(1)&gt;" in upgraded
    assert "/v1/users/&lt;id&gt;" in upgraded
    assert "Parameters &lt;T&gt;" in upgraded
    assert "<pre><code><h2>not touched</h2></code></pre>" in upgraded


def test_api_project_types_and_css_exports() -> None:
    """Verify 'api' is listed in project types and CSS targets, and ref/reference aliases do not exist."""
    types = list_project_types()
    assert "api" in types
    assert "ref" not in types
    assert "reference" not in types

    api_presets = list_css(target="api")
    preset_names = [p["name"] for p in api_presets]
    assert "default" in preset_names
    assert "google" in preset_names
    api_css = get_css("default", target="api")
    assert ".api-nav-group" in api_css
    assert ".api-badge-get" in api_css


def test_init_rejects_ref_and_reference_aliases(tmp_path: Path) -> None:
    """Verify 'ref' and 'reference' are strictly rejected per design specification."""
    for alias in ("ref", "reference"):
        with pytest.raises(ValueError, match="Unknown project type"):
            init_project(alias, destination=tmp_path)


def test_api_multi_locale_build_seo_and_link_integrity(tmp_path: Path) -> None:
    """End-to-end test of multi-locale api build, chrome customization, SEO outputs, and link scanner."""
    init_project("api", destination=tmp_path, target="cloudapi", lang="en,ja")
    src_dir = tmp_path / "cloudapi_src"
    out_html = tmp_path / "cloudapi_html"
    out_md = tmp_path / "cloudapi_markdown"
    out_img = tmp_path / "cloudapi_images"

    # Replace drawlib blocks with fast minimal blocks so test runs in <2s while testing full pipeline
    for lc in ("en", "ja"):
        (src_dir / lc / "00_overview.md").write_text(
            "# Platform Overview\n\nOverview intro paragraph.\n\n"
            '```drawlib file=overview_arch.png caption="Overview"\n'
            "from drawlib.canvas import save, setup\n"
            "from drawlib.shapes import rectangle\n"
            "from drawlib.styles import Styles\n"
            "setup(width=80, height=30)\n"
            'rectangle((40, 15), width=40, height=14, style=Styles.Neutral, text="API")\n'
            "save()\n"
            "```\n\n"
            "## Authentication\n\nUse Bearer tokens.\n",
            encoding="utf-8",
        )
        (src_dir / lc / "01_users.md").write_text(
            "# Users Service\n\nManage accounts.\n\n"
            "## `GET` /v1/users\n\nList users.\n\n"
            "## `GET` /v1/users/<id>\n\nFetch user [User](02_models.md#user).\n",
            encoding="utf-8",
        )
        (src_dir / lc / "02_models.md").write_text(
            "# Data Models\n\nCore schemas.\n\n"
            "## `class` User\n\nUser record.\n\n"
            "## `def` verify_token(token)\n\nVerify JWT.\n",
            encoding="utf-8",
        )

    # Append [seo], [i18n.descriptions], and rich [api] options
    toml_path = src_dir / "drawlib.toml"
    base_toml = toml_path.read_text(encoding="utf-8")
    updated_toml = base_toml.replace(
        "[api]\nsidebar_expanded = true\n",
        "[i18n.descriptions]\n"
        'en = "Cloud API Reference"\n'
        'ja = "Cloud API リファレンス"\n\n'
        "[api]\n"
        "sidebar_expanded = true\n"
        'badge_text = { en = "v1.4", ja = "v1.4 日本語" }\n'
        'repo_url = "https://github.com/example/cloudapi"\n'
        'header_links = [{ label = { en = "Docs", ja = "ドキュメント" }, url = "https://docs.example.com" }]\n\n'
        "[seo]\n"
        'site_url = "https://api.example.com"\n',
    )
    toml_path.write_text(updated_toml, encoding="utf-8")

    build_html(str(src_dir), str(out_html))

    assert (out_html / "index.html").is_file()
    assert (out_html / "en" / "index.html").is_file()
    assert (out_html / "en" / "00_overview.html").is_file()
    assert (out_html / "en" / "01_users.html").is_file()
    assert (out_html / "en" / "02_models.html").is_file()
    assert (out_html / "ja" / "index.html").is_file()
    assert (out_html / "ja" / "01_users.html").is_file()
    assert (out_html / "sitemap.xml").is_file()
    assert (out_html / "robots.txt").is_file()
    assert (out_html / "llms.txt").is_file()

    # Check sidebar_expanded = true: all 3 category <details> are open on en/01_users.html
    users_en_html = (out_html / "en" / "01_users.html").read_text(encoding="utf-8")
    details_tags = re.findall(r"<details class=\"api-nav-group[^\"]*\"[^>]*>", users_en_html)
    assert len(details_tags) == 3
    assert all(" open" in tag for tag in details_tags)
    assert "sidebar-header has-subbar" in users_en_html
    assert "v1.4" in users_en_html
    assert "https://github.com/example/cloudapi" in users_en_html
    assert "https://docs.example.com" in users_en_html
    assert "/v1/users/&lt;id&gt;" in users_en_html

    # Verify localized Japanese chrome
    users_ja_html = (out_html / "ja" / "01_users.html").read_text(encoding="utf-8")
    assert "v1.4 日本語" in users_ja_html
    assert "ドキュメント" in users_ja_html

    # Verify zero broken links across all generated HTML pages AND every #slug anchor exists
    scanned_files, checked_links, broken = scan_broken_links(str(out_html))
    assert scanned_files == 9
    assert checked_links > 100
    assert broken == [], f"Unexpected broken links: {broken}"

    for html_file in out_html.rglob("*.html"):
        text = html_file.read_text(encoding="utf-8")
        for href in re.findall(r'<a[^>]+href="([^"]+)"', text):
            if href.startswith(("http://", "https://", "mailto:")) or "#" not in href:
                continue
            page_part, frag = href.split("#", 1)
            target_file = (html_file.parent / page_part).resolve() if page_part else html_file
            assert target_file.is_file(), f"Missing target file {target_file} from {html_file}"
            target_text = target_file.read_text(encoding="utf-8")
            assert f'id="{frag}"' in target_text, f"Missing anchor #{frag} in {target_file} (from {html_file})"

    # Now test sidebar_expanded = false: only active category is open, inactive categories are closed
    collapsed_toml = updated_toml.replace("sidebar_expanded = true", "sidebar_expanded = false")
    toml_path.write_text(collapsed_toml, encoding="utf-8")
    build_html(str(src_dir), str(out_html))

    users_collapsed = (out_html / "en" / "01_users.html").read_text(encoding="utf-8")
    collapsed_details = re.findall(r"<details class=\"api-nav-group[^\"]*\"[^>]*>", users_collapsed)
    assert len(collapsed_details) == 3
    open_tags = [t for t in collapsed_details if " open" in t]
    assert len(open_tags) == 1
    assert "is-current-page" in open_tags[0]

    # Verify build_markdown and build_image succeed, while build_pdf and build_docx raise ValueError
    build_markdown(str(src_dir), str(out_md))
    assert (out_md / "en" / "01_users.md").is_file()
    build_image(str(src_dir), str(out_img))
    assert (out_img / "00_overview" / "overview_arch.png").is_file()

    with pytest.raises(ValueError, match='multi-page "api" project'):
        build_pdf(str(src_dir), str(tmp_path / "out.pdf"))
    with pytest.raises(ValueError, match='multi-page "api" project'):
        build_docx(str(src_dir), str(tmp_path / "out.docx"))
