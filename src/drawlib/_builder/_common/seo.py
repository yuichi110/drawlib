# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Project-level SEO, Open Graph, ``sitemap.xml``, ``robots.txt``, and ``llms.txt`` utilities."""

from __future__ import annotations

import html
import os
import re
import shutil
import urllib.parse
from collections.abc import Sequence
from dataclasses import dataclass, field
from typing import Final
from xml.sax.saxutils import escape as xml_escape

from drawlib._builder._common.manifest import ProjectManifest, SeoConfig

_OG_LOCALE_BY_LANG: Final[dict[str, str]] = {
    "en": "en_US",
    "ja": "ja_JP",
    "zh-cn": "zh_CN",
    "zh-tw": "zh_TW",
    "ko": "ko_KR",
    "fr": "fr_FR",
    "de": "de_DE",
    "es": "es_ES",
    "pt": "pt_BR",
    "it": "it_IT",
    "ru": "ru_RU",
    "ar": "ar_AR",
    "hi": "hi_IN",
    "th": "th_TH",
    "vi": "vi_VN",
    "id": "id_ID",
    "nl": "nl_NL",
    "pl": "pl_PL",
    "tr": "tr_TR",
    "uk": "uk_UA",
    "sv": "sv_SE",
    "cs": "cs_CZ",
    "el": "el_GR",
    "he": "he_IL",
    "fa": "fa_IR",
    "bn": "bn_BD",
    "ta": "ta_IN",
    "te": "te_IN",
    "ml": "ml_IN",
    "mr": "mr_IN",
    "gu": "gu_IN",
    "kn": "kn_IN",
    "pa": "pa_IN",
    "my": "my_MM",
    "km": "km_KH",
    "lo": "lo_LA",
    "ms": "ms_MY",
    "tl": "tl_PH",
}

_FENCE_LINE_RE: Final[re.Pattern[str]] = re.compile(r"^[ \t]{0,3}(`{3,}|~{3,})")
_ATX_HEADING_RE: Final[re.Pattern[str]] = re.compile(r"^[ \t]{0,3}(#{1,6})[ \t]+(.+?)[ \t#]*$")
_HR_LINE_RE: Final[re.Pattern[str]] = re.compile(r"^[ \t]{0,3}(?:[-*_][ \t]*){3,}$")
_SETEXT_LINE_RE: Final[re.Pattern[str]] = re.compile(r"^[ \t]{0,3}(?:=+|-+)[ \t]*$")
_STANDALONE_IMAGE_RE: Final[re.Pattern[str]] = re.compile(r"^[ \t]*!\[[^\]]*\]\([^)]+\)[ \t]*$")
_HTML_BLOCK_LINE_RE: Final[re.Pattern[str]] = re.compile(
    r"^[ \t]*</?(?:div|section|article|aside|header|footer|nav|main|table|thead|tbody|tr|td|th|ul|ol|li|"
    r"figure|figcaption|details|summary|pre|blockquote|hr|br|img|svg|iframe|canvas)\b",
    re.IGNORECASE,
)
_BULLET_PREFIX_RE: Final[re.Pattern[str]] = re.compile(r"^[ \t]*(?:[-*+]|\d+\.)[ \t]+(.+)$")
_XML_ATTR_ENTITIES: Final[dict[str, str]] = {'"': "&quot;", "'": "&apos;"}


@dataclass(frozen=True)
class PageSeoMetadata:
    """Resolved per-page SEO, Open Graph, and Twitter Card metadata."""

    title: str
    og_title: str
    description: str
    site_name: str
    canonical_url: str
    og_image_url: str
    og_locale: str
    og_alternate_locales: tuple[str, ...] = ()
    twitter_card: str = "summary_large_image"
    twitter_site: str = ""
    og_type: str = "website"


@dataclass(frozen=True)
class SitemapEntry:
    """Single canonical ``<url>`` record for ``sitemap.xml``."""

    loc: str
    alternates: tuple[tuple[str, str], ...] = ()


@dataclass(frozen=True)
class LlmsLink:
    """Single Markdown link entry in ``llms.txt``."""

    title: str
    url: str
    description: str = ""


@dataclass(frozen=True)
class LlmsSection:
    """Categorized ``## Section`` in ``llms.txt``."""

    title: str
    links: list[LlmsLink] = field(default_factory=list)


def to_og_locale(lang: str) -> str:
    """Convert a canonical Drawlib language code into an Open Graph ``ll_TERRITORY`` locale tag.

    Args:
        lang: Canonical language code (e.g. ``'en'``, ``'ja'``, ``'zh-cn'``).

    Returns:
        str: Open Graph locale identifier (e.g. ``'en_US'``, ``'ja_JP'``, ``'zh_CN'``).
    """
    key = lang.strip().lower()
    if key in _OG_LOCALE_BY_LANG:
        return _OG_LOCALE_BY_LANG[key]
    if "-" in key:
        lang_part, region_part = key.split("-", 1)
        return f"{lang_part}_{region_part.upper()}"
    if len(key) == 2 and key.isalpha():
        return f"{key}_{key.upper()}"
    return "en_US"


def _strip_fenced_and_directive_blocks(markdown_text: str) -> list[str]:
    """Remove HTML comments, script/style tags, slide directives, and fenced code blocks."""
    cleaned = re.sub(r"<!--.*?-->", " ", markdown_text, flags=re.DOTALL)
    cleaned = re.sub(r"(?is)<(?:script|style)\b[^>]*>.*?</(?:script|style)>", " ", cleaned)
    cleaned = re.sub(
        r"^[ \t]*:::[ \t]+note\b.*?^[ \t]*:::[ \t\r]*$",
        "",
        cleaned,
        flags=re.MULTILINE | re.DOTALL,
    )
    cleaned = re.sub(r"^[ \t]*:::(?:[ \t]+block\b[^\n]*)?[ \t\r]*$", "", cleaned, flags=re.MULTILINE)

    out_lines: list[str] = []
    in_fence = False
    fence_char = ""
    fence_len = 0

    for line in cleaned.splitlines():
        if not in_fence:
            m_open = _FENCE_LINE_RE.match(line)
            if m_open:
                marker = m_open.group(1)
                in_fence = True
                fence_char = marker[0]
                fence_len = len(marker)
                continue
            out_lines.append(line)
        else:
            close_pat = rf"^[ \t]{{0,3}}{re.escape(fence_char)}{{{fence_len},}}[ \t\r]*$"
            if re.match(close_pat, line):
                in_fence = False
                fence_char = ""
                fence_len = 0
    return out_lines


def _clean_inline_markdown(raw_text: str) -> str:
    """Convert inline Markdown and HTML markup into normalized single-line plain text."""
    text = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", raw_text)
    text = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"`([^`]+)`", r"\1", text)
    text = re.sub(r"<[^>]+>", " ", text)
    text = html.unescape(text)
    text = re.sub(r"(\*\*|__|~~)", "", text)
    text = re.sub(r"(?<!\w)\*([^*\n]+)\*(?!\w)", r"\1", text)
    text = re.sub(r"(?<!\w)_([^_\n]+)_(?!\w)", r"\1", text)
    text = re.sub(r"[\r\n\t\x00]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def _truncate_description(text: str, max_length: int) -> str:
    """Truncate ``text`` cleanly to ``max_length`` characters with an ellipsis if needed."""
    if max_length <= 0 or len(text) <= max_length:
        return text
    limit = max(1, max_length - 1)
    sliced = text[:limit].rstrip()
    last_space = sliced.rfind(" ")
    if last_space >= int(limit * 0.65):
        sliced = sliced[:last_space].rstrip(" ,;:-—")
    return f"{sliced}…"


def extract_markdown_description(
    markdown_text: str,
    max_length: int = 160,
    *,
    allow_heading_fallback: bool = False,
) -> str:
    """Extract the first plain-text prose paragraph summary from a Markdown document.

    Strips fenced code blocks (including ````drawlib````), HTML comments, slide ``::: block`` /
    ``::: note`` directives, tables, headings, and inline formatting.

    Args:
        markdown_text: Raw Markdown document content.
        max_length: Maximum summary length in characters before ellipsis truncation.
        allow_heading_fallback: If True and no prose paragraph exists, fall back to H2+ headings or bullets.

    Returns:
        str: Sanitized plain-text summary (empty string if none found).
    """
    lines = _strip_fenced_and_directive_blocks(markdown_text)
    paragraph_lines: list[str] = []
    fallback_candidates: list[str] = []

    for line in lines:
        stripped = line.strip()
        if not stripped:
            if paragraph_lines:
                break
            continue

        m_heading = _ATX_HEADING_RE.match(line)
        if m_heading:
            if paragraph_lines:
                break
            if allow_heading_fallback and len(m_heading.group(1)) >= 2:
                fallback_candidates.append(m_heading.group(2))
            continue

        if _HR_LINE_RE.match(line) or _SETEXT_LINE_RE.match(line) or _STANDALONE_IMAGE_RE.match(line):
            if paragraph_lines:
                break
            continue

        if stripped.startswith("|") or _HTML_BLOCK_LINE_RE.match(line):
            if paragraph_lines:
                break
            continue

        if stripped.startswith(">"):
            if paragraph_lines:
                break
            quote_body = stripped.lstrip(">").strip()
            if quote_body:
                fallback_candidates.append(quote_body)
            continue

        m_bullet = _BULLET_PREFIX_RE.match(line)
        if m_bullet:
            if paragraph_lines:
                break
            fallback_candidates.append(m_bullet.group(1))
            continue

        paragraph_lines.append(stripped)

    if paragraph_lines:
        cleaned = _clean_inline_markdown(" ".join(paragraph_lines))
        if cleaned:
            return _truncate_description(cleaned, max_length)

    if allow_heading_fallback:
        for cand in fallback_candidates:
            cleaned_cand = _clean_inline_markdown(cand)
            if cleaned_cand:
                return _truncate_description(cleaned_cand, max_length)

    return ""


def resolve_localized_description(
    manifest: ProjectManifest | None,
    lang: str,
    page_description: str = "",
    *,
    prefer_manifest: bool = False,
    max_length: int = 160,
) -> str:
    """Resolve effective plain-text description from page prose and ``drawlib.toml`` metadata.

    Args:
        manifest: Parsed ``ProjectManifest`` (or ``None``).
        lang: Active canonical language code.
        page_description: Extracted description from the current page/chapter/slide.
        prefer_manifest: If True, prioritize ``[i18n.descriptions][lang]`` (and ``[project].description``
            on the default language) ahead of ``page_description``.
        max_length: Maximum character length.

    Returns:
        str: Effective single-line plain-text description.
    """
    if manifest is None:
        return _truncate_description(_clean_inline_markdown(page_description), max_length) if page_description else ""

    i18n_desc = ""
    is_default_lang = True
    if manifest.i18n is not None:
        i18n_desc = manifest.i18n.descriptions.get(lang, "").strip()
        is_default_lang = lang == manifest.i18n.default_lang

    proj_desc = manifest.project.description.strip()
    if prefer_manifest:
        raw_candidates = [i18n_desc, proj_desc if is_default_lang else "", page_description, proj_desc]
    else:
        raw_candidates = [page_description, i18n_desc, proj_desc]

    for cand in raw_candidates:
        if cand:
            cleaned = _clean_inline_markdown(cand)
            if cleaned:
                return _truncate_description(cleaned, max_length)
    return ""


def _quote_posix_rel_path(rel_posix: str) -> str:
    """Percent-encode individual POSIX path segments while preserving ``/`` separators."""
    parts = [urllib.parse.quote(seg, safe="-._~") for seg in rel_posix.split("/") if seg]
    return "/".join(parts)


def resolve_public_page_url(site_url: str, rel_out_path: str) -> str:
    """Resolve canonical public URL for a file path relative to ``out_dir_abs``.

    Normalizes ``index.html`` -> ``<site_url>/`` and ``<subpath>/index.html`` -> ``<site_url>/<subpath>/``.

    Args:
        site_url: Validated base URL without trailing slash (or empty string).
        rel_out_path: Output-root-relative POSIX path (e.g. ``'index.html'``, ``'en/index.html'``).

    Returns:
        str: Canonical absolute URL, or ``''`` if ``site_url`` is empty.
    """
    base = site_url.strip().rstrip("/")
    if not base:
        return ""

    norm_rel = rel_out_path.replace("\\", "/").lstrip("/")
    if not norm_rel or norm_rel == "index.html":
        return f"{base}/"
    if norm_rel.endswith("/index.html"):
        prefix = norm_rel[: -len("/index.html")]
        encoded_prefix = _quote_posix_rel_path(prefix)
        return f"{base}/{encoded_prefix}/" if encoded_prefix else f"{base}/"
    return f"{base}/{_quote_posix_rel_path(norm_rel)}"


def upgrade_alternate_links(
    alternate_links: list[dict[str, str]],
    site_url: str,
    out_dir_abs: str,
    current_dest_abs: str,
) -> list[dict[str, str]]:
    """Upgrade relative ``hreflang`` links to canonical ``site_url`` URLs when ``site_url`` is configured.

    Args:
        alternate_links: Relative ``[{'hreflang': ..., 'url': ...}]`` list from ``build_language_switcher_context``.
        site_url: Configured ``[seo].site_url`` (or empty string).
        out_dir_abs: Root HTML output directory.
        current_dest_abs: Absolute path to the HTML file being rendered.

    Returns:
        list[dict[str, str]]: Upgraded ``alternate_links`` list.
    """
    base = site_url.strip().rstrip("/")
    if not base or not alternate_links:
        return alternate_links

    current_dir = os.path.dirname(os.path.abspath(current_dest_abs))
    out_root = os.path.abspath(out_dir_abs)
    upgraded: list[dict[str, str]] = []
    for entry in alternate_links:
        raw_href = entry.get("url", "").strip()
        if raw_href.startswith(("http://", "https://")):
            upgraded.append({"hreflang": entry["hreflang"], "url": raw_href})
            continue
        target_abs = os.path.normpath(os.path.join(current_dir, raw_href))
        rel_out = os.path.relpath(target_abs, out_root).replace(os.sep, "/")
        upgraded.append(
            {
                "hreflang": entry["hreflang"],
                "url": resolve_public_page_url(base, rel_out),
            }
        )
    return upgraded


def resolve_og_image_url(seo: SeoConfig, out_dir_abs: str, current_dest_abs: str) -> str:
    """Resolve ``og:image`` / ``twitter:image`` URL as absolute ``site_url`` asset or relative fallback."""
    if not seo.og_image:
        return ""
    if seo.og_image.lower().startswith(("http://", "https://")):
        return seo.og_image
    rel_posix = seo.og_image.replace("\\", "/").lstrip("/")
    if seo.site_url:
        return f"{seo.site_url.rstrip('/')}/{_quote_posix_rel_path(rel_posix)}"
    target_abs = os.path.normpath(os.path.join(out_dir_abs, *rel_posix.split("/")))
    return os.path.relpath(target_abs, os.path.dirname(os.path.abspath(current_dest_abs))).replace(os.sep, "/")


def ensure_seo_og_image_copied(input_abs: str, out_dir_abs: str, seo: SeoConfig | None) -> None:
    """Ensure local project-relative ``[seo].og_image`` is copied into ``out_dir_abs`` safely."""
    if seo is None or not seo.og_image or seo.og_image.lower().startswith(("http://", "https://")):
        return

    rel_parts = [p for p in seo.og_image.replace("\\", "/").split("/") if p]
    if not rel_parts:
        return

    real_in_root = os.path.realpath(input_abs)
    real_out_root = os.path.realpath(out_dir_abs)
    src_candidate = os.path.normpath(os.path.join(input_abs, *rel_parts))
    dst_candidate = os.path.normpath(os.path.join(out_dir_abs, *rel_parts))

    real_src = os.path.realpath(src_candidate)
    if os.path.commonpath([real_in_root, real_src]) != real_in_root or not os.path.isfile(real_src):
        return

    os.makedirs(os.path.dirname(dst_candidate), exist_ok=True)
    real_dst_parent = os.path.realpath(os.path.dirname(dst_candidate))
    if os.path.commonpath([real_out_root, real_dst_parent]) != real_out_root:
        return

    if os.path.abspath(real_src) != os.path.abspath(dst_candidate) and not os.path.isfile(dst_candidate):
        shutil.copy2(real_src, dst_candidate)


def build_page_seo_metadata(
    *,
    manifest: ProjectManifest | None,
    out_dir_abs: str,
    dest_abs: str,
    lang: str,
    page_title: str,
    site_title: str | None = None,
    page_description: str = "",
    prefer_manifest_description: bool = False,
    canonical_rel_override: str | None = None,
) -> PageSeoMetadata | None:
    """Construct ``PageSeoMetadata`` for a destination HTML file when ``[seo]`` is enabled.

    Args:
        manifest: Loaded ``ProjectManifest`` (returns ``None`` if absent or ``manifest.seo is None``).
        out_dir_abs: Root HTML output directory.
        dest_abs: Absolute path to the HTML file being generated.
        lang: Active canonical language code for this page.
        page_title: Resolved ``<title>`` of the page.
        site_title: Optional site/brand title (e.g. from ``navbar.md`` or ``[project].title``).
        page_description: Extracted summary from the page's Markdown content.
        prefer_manifest_description: If True, prefer ``[i18n.descriptions]`` / ``[project].description``.
        canonical_rel_override: Optional output-relative path override for canonical URL (e.g. redirect target).

    Returns:
        PageSeoMetadata | None: Populated metadata object, or ``None`` if ``[seo]`` is not configured.
    """
    if manifest is None or manifest.seo is None:
        return None

    seo = manifest.seo
    resolved_site_name = (site_title or manifest.project.title or "").strip()
    clean_title = _clean_inline_markdown(page_title) or resolved_site_name or "Drawlib"
    if resolved_site_name and resolved_site_name.lower() not in clean_title.lower():
        og_title = f"{clean_title} — {resolved_site_name}"
    else:
        og_title = clean_title

    description = resolve_localized_description(
        manifest=manifest,
        lang=lang,
        page_description=page_description,
        prefer_manifest=prefer_manifest_description,
    )

    if canonical_rel_override is not None:
        rel_out = canonical_rel_override.replace("\\", "/").lstrip("/")
    else:
        rel_out = os.path.relpath(os.path.abspath(dest_abs), os.path.abspath(out_dir_abs)).replace(os.sep, "/")

    canonical_url = resolve_public_page_url(seo.site_url, rel_out)
    og_image_url = resolve_og_image_url(seo, out_dir_abs, dest_abs)
    og_locale = to_og_locale(lang)

    alt_locales: list[str] = []
    if manifest.i18n is not None and len(manifest.i18n.langs) > 1:
        for other_lang in manifest.i18n.langs:
            if other_lang != lang:
                loc_code = to_og_locale(other_lang)
                if loc_code != og_locale and loc_code not in alt_locales:
                    alt_locales.append(loc_code)

    return PageSeoMetadata(
        title=clean_title,
        og_title=og_title,
        description=description,
        site_name=resolved_site_name,
        canonical_url=canonical_url,
        og_image_url=og_image_url,
        og_locale=og_locale,
        og_alternate_locales=tuple(alt_locales),
        twitter_card=seo.twitter_card,
        twitter_site=seo.twitter_site,
    )


def render_seo_head_tags(
    meta: PageSeoMetadata,
    *,
    indent: str = "    ",
    include_canonical: bool = True,
) -> str:
    """Render strictly HTML-escaped ``<meta>`` and ``<link rel="canonical">`` tags for ``<head>``.

    Args:
        meta: Resolved ``PageSeoMetadata``.
        indent: Leading indentation prefix for each emitted line.
        include_canonical: Whether to emit ``<link rel="canonical">`` when ``meta.canonical_url`` is set.

    Returns:
        str: Newline-joined HTML tag lines.
    """
    lines: list[str] = []
    esc = lambda val: html.escape(val, quote=True)  # noqa: E731

    if meta.description:
        lines.append(f'{indent}<meta name="description" content="{esc(meta.description)}">')
    if include_canonical and meta.canonical_url:
        lines.append(f'{indent}<link rel="canonical" href="{esc(meta.canonical_url)}">')

    lines.append(f'{indent}<meta property="og:type" content="{esc(meta.og_type)}">')
    if meta.site_name:
        lines.append(f'{indent}<meta property="og:site_name" content="{esc(meta.site_name)}">')
    lines.append(f'{indent}<meta property="og:title" content="{esc(meta.og_title)}">')
    if meta.description:
        lines.append(f'{indent}<meta property="og:description" content="{esc(meta.description)}">')
    if meta.canonical_url:
        lines.append(f'{indent}<meta property="og:url" content="{esc(meta.canonical_url)}">')
    if meta.og_image_url:
        lines.append(f'{indent}<meta property="og:image" content="{esc(meta.og_image_url)}">')
    if meta.og_locale:
        lines.append(f'{indent}<meta property="og:locale" content="{esc(meta.og_locale)}">')
    for alt_loc in meta.og_alternate_locales:
        lines.append(f'{indent}<meta property="og:locale:alternate" content="{esc(alt_loc)}">')

    lines.append(f'{indent}<meta name="twitter:card" content="{esc(meta.twitter_card)}">')
    if meta.twitter_site:
        lines.append(f'{indent}<meta name="twitter:site" content="{esc(meta.twitter_site)}">')
    lines.append(f'{indent}<meta name="twitter:title" content="{esc(meta.og_title)}">')
    if meta.description:
        lines.append(f'{indent}<meta name="twitter:description" content="{esc(meta.description)}">')
    if meta.og_image_url:
        lines.append(f'{indent}<meta name="twitter:image" content="{esc(meta.og_image_url)}">')

    return "\n".join(lines)


def write_sitemap_xml(out_dir_abs: str, entries: Sequence[SitemapEntry]) -> str:
    """Write ``<out_dir_abs>/sitemap.xml`` following Sitemap 0.9 + ``xhtml:link`` specification.

    Args:
        out_dir_abs: Target HTML output directory.
        entries: Ordered ``SitemapEntry`` items with absolute ``loc`` URLs.

    Returns:
        str: Absolute path to the generated ``sitemap.xml``.
    """
    has_alternates = any(bool(entry.alternates) for entry in entries)
    ns_xhtml = ' xmlns:xhtml="http://www.w3.org/1999/xhtml"' if has_alternates else ""
    xml_lines: list[str] = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"{ns_xhtml}>',
    ]

    seen_locs: set[str] = set()
    for entry in entries:
        if not entry.loc or entry.loc in seen_locs:
            continue
        seen_locs.add(entry.loc)
        esc_loc = xml_escape(entry.loc, _XML_ATTR_ENTITIES)
        xml_lines.append("  <url>")
        xml_lines.append(f"    <loc>{esc_loc}</loc>")
        for hreflang, alt_href in entry.alternates:
            esc_lang = xml_escape(hreflang, _XML_ATTR_ENTITIES)
            esc_href = xml_escape(alt_href, _XML_ATTR_ENTITIES)
            xml_lines.append(f'    <xhtml:link rel="alternate" hreflang="{esc_lang}" href="{esc_href}" />')
        xml_lines.append("  </url>")

    xml_lines.append("</urlset>")
    os.makedirs(out_dir_abs, exist_ok=True)
    dest_path = os.path.join(out_dir_abs, "sitemap.xml")
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write("\n".join(xml_lines) + "\n")
    return dest_path


def write_robots_txt(out_dir_abs: str, site_url: str, *, include_sitemap: bool = True) -> str:
    """Write ``<out_dir_abs>/robots.txt`` with optional ``Sitemap:`` directive.

    Args:
        out_dir_abs: Target HTML output directory.
        site_url: Configured ``[seo].site_url`` (or empty string).
        include_sitemap: Whether ``sitemap.xml`` was also emitted.

    Returns:
        str: Absolute path to the generated ``robots.txt``.
    """
    lines = [
        "User-agent: *",
        "Allow: /",
    ]
    base = site_url.strip().rstrip("/")
    if include_sitemap and base:
        lines.extend(["", f"Sitemap: {base}/sitemap.xml"])

    os.makedirs(out_dir_abs, exist_ok=True)
    dest_path = os.path.join(out_dir_abs, "robots.txt")
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    return dest_path


def _sanitize_llms_text(value: str) -> str:
    """Normalize single-line Markdown text for ``llms.txt`` output."""
    return re.sub(r"\s+", " ", re.sub(r"[\r\n\t\x00]+", " ", value)).strip()


def write_llms_txt(
    out_dir_abs: str,
    *,
    title: str,
    summary: str = "",
    sections: Sequence[LlmsSection] = (),
) -> str:
    """Write ``<out_dir_abs>/llms.txt`` following the ``llmstxt.org`` Markdown standard.

    Args:
        out_dir_abs: Target HTML output directory.
        title: Top-level H1 project title.
        summary: Optional blockquote summary right below H1.
        sections: Ordered ``LlmsSection`` groups containing links and 1-line descriptions.

    Returns:
        str: Absolute path to the generated ``llms.txt``.
    """
    clean_title = _sanitize_llms_text(title) or "Documentation"
    lines: list[str] = [f"# {clean_title}"]

    clean_summary = _sanitize_llms_text(summary)
    if clean_summary:
        lines.extend(["", f"> {clean_summary}"])

    for section in sections:
        if not section.links:
            continue
        sec_title = _sanitize_llms_text(section.title) or "Pages"
        lines.extend(["", f"## {sec_title}", ""])
        for item in section.links:
            item_title = _sanitize_llms_text(item.title).replace("[", "(").replace("]", ")") or item.url
            item_url = _sanitize_llms_text(item.url)
            item_desc = _sanitize_llms_text(item.description)
            if item_url:
                if item_desc:
                    lines.append(f"- [{item_title}]({item_url}): {item_desc}")
                else:
                    lines.append(f"- [{item_title}]({item_url})")
            elif item_desc:
                lines.append(f"- {item_title}: {item_desc}")
            else:
                lines.append(f"- {item_title}")

    os.makedirs(out_dir_abs, exist_ok=True)
    dest_path = os.path.join(out_dir_abs, "llms.txt")
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    return dest_path
