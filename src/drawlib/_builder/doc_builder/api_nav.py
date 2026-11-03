# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Heading extraction, semantic badge post-processing, and sidebar builder for ``api`` projects."""

from __future__ import annotations

import html
import os
import re
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, Final

from drawlib._builder.doc_builder.detector import preserve_outer_fences
from drawlib._builder.doc_builder.i18n import resolve_locale_navbar_path
from drawlib._builder.doc_builder.navbar import NavbarSection, parse_navbar_markdown

if TYPE_CHECKING:
    from drawlib._builder._common.manifest import ApiConfig

KNOWN_API_BADGES: Final[dict[str, str]] = {
    "def": "def",
    "fn": "def",
    "func": "def",
    "function": "def",
    "async": "def",
    "async def": "def",
    "class": "class",
    "interface": "class",
    "struct": "class",
    "method": "method",
    "rpc": "method",
    "const": "const",
    "attr": "const",
    "prop": "const",
    "property": "const",
    "event": "const",
    "type": "type",
    "enum": "type",
    "cmd": "cmd",
    "cli": "cmd",
    "get": "get",
    "head": "get",
    "options": "method",
    "post": "post",
    "put": "put",
    "patch": "patch",
    "delete": "delete",
}

_FENCE_OPEN_RE: Final[re.Pattern[str]] = re.compile(r"^[ \t]{0,3}(`{3,}|~{3,})")
_ATX_HEADING_RE: Final[re.Pattern[str]] = re.compile(r"^[ \t]{0,3}(#{1,4})[ \t]+(.+?)[ \t]*#*[ \t\r]*$")
_LEADING_CODE_SPAN_RE: Final[re.Pattern[str]] = re.compile(r"^`([^`\n]+)`[ \t]*(.*)$")
_MD_LINK_INLINE_RE: Final[re.Pattern[str]] = re.compile(r"\[([^\]]+)\]\([^)]+\)")


@dataclass(frozen=True)
class ApiSubItem:
    """Single ``## H2`` endpoint or symbol entry extracted from an API Markdown page.

    Attributes:
        slug: Deterministic HTML ``id`` anchor slug (unique within the page).
        raw_title: Plain-text heading content after any semantic badge token.
        sidebar_label: Compact label rendered in the left navigation pane.
        badge_text: Original badge token text (e.g. ``'GET'``, ``'def'``) or ``None``.
        badge_kind: Normalized CSS badge kind (e.g. ``'get'``, ``'def'``) or ``None``.
    """

    slug: str
    raw_title: str
    sidebar_label: str
    badge_text: str | None = None
    badge_kind: str | None = None


@dataclass(frozen=True)
class ExtractedApiHeadings:
    """Structured headings parsed from a Markdown source file before HTML rendering."""

    h1_title: str
    h1_raw: str | None
    h2_items: tuple[ApiSubItem, ...]
    sub_headings: tuple[tuple[int, str, str], ...]


@dataclass
class CompiledApiPage:
    """Compiled API page metadata, HTML body, and extracted ``H2`` sub-items."""

    rel_path: str
    rel_html: str
    src_abs: str
    dest_abs: str
    section_title: str | None
    h1_title: str
    description: str
    body_html: str
    subitems: list[ApiSubItem] = field(default_factory=list)


def humanize_identifier(stem: str) -> str:
    """Convert a filename or directory stem like ``'01_user_auth'`` into ``'User Auth'``."""
    stripped = re.sub(r"^\d+[_-]+", "", stem.strip())
    cleaned = (stripped or stem).replace("_", " ").replace("-", " ").strip()
    return cleaned.title() if cleaned else "Overview"


def _strip_inline_markdown_preserving_angles(raw: str) -> str:
    """Strip Markdown links, backticks, and emphasis while keeping literal ``<...>`` text intact."""
    text = raw.strip()
    if len(text) >= 2 and text.startswith("`") and text.endswith("`") and "`" not in text[1:-1]:
        return text[1:-1].strip()
    text = _MD_LINK_INLINE_RE.sub(r"\1", text)
    text = re.sub(r"`([^`\n]+)`", r"\1", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"\1", text)
    text = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"\1", text)
    return text.strip()


def _render_safe_inline_heading_html(raw: str) -> str:
    """Render escaped heading text allowing only safe ``<code>`` spans for inline backticks."""
    cleaned = _MD_LINK_INLINE_RE.sub(r"\1", raw.strip())
    if len(cleaned) >= 2 and cleaned.startswith("`") and cleaned.endswith("`") and "`" not in cleaned[1:-1]:
        return html.escape(cleaned[1:-1].strip(), quote=True)

    parts = re.split(r"(`[^`\n]+`)", cleaned)
    out: list[str] = []
    for part in parts:
        if len(part) >= 2 and part.startswith("`") and part.endswith("`"):
            out.append(f"<code>{html.escape(part[1:-1], quote=True)}</code>")
        elif part:
            esc = html.escape(part, quote=True)
            esc = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", esc)
            out.append(esc)
    return "".join(out)


def slugify_api_heading(
    text_after_badge: str,
    used_slugs: set[str],
    *,
    has_badge: bool = False,
) -> str:
    """Generate a deterministic, collision-free URL anchor slug for an API heading.

    Strips parameter lists ``(...)`` on badged function/method signatures so anchors remain
    concise and stable (e.g. ``#rectangle``, ``#barchart-draw``, ``#v1-users-id``).
    """
    base_target = text_after_badge.strip()
    if has_badge and "(" in base_target:
        base_target = base_target.split("(", 1)[0].strip()

    normalized = re.sub(r"[^\w]+", "-", base_target.lower(), flags=re.UNICODE).replace("_", "-")
    slug = re.sub(r"-{2,}", "-", normalized).strip("-")
    if not slug:
        slug = "section"

    cand = slug
    suffix = 2
    while cand in used_slugs:
        cand = f"{slug}-{suffix}"
        suffix += 1
    used_slugs.add(cand)
    return cand


def compact_sidebar_label(badge_kind: str | None, text_after_badge: str) -> str:
    """Format compact ``H2`` label for the left sidebar while preserving ``Ctrl+F`` symbol names."""
    cleaned = text_after_badge.strip()
    if badge_kind in {"def", "method"} and "(" in cleaned:
        sym_name = cleaned.split("(", 1)[0].strip()
        return f"{sym_name}()"
    return cleaned


def _mask_fences_and_comments(md_text: str) -> list[str]:
    """Return Markdown lines with outer fences, 3-tick/tilde fences, and HTML comments blanked out."""
    masked_outer, _ = preserve_outer_fences(md_text)
    without_comments = re.sub(
        r"<!--.*?-->",
        lambda m: re.sub(r"[^\n]", " ", m.group(0)),
        masked_outer,
        flags=re.DOTALL,
    )
    lines = without_comments.split("\n")
    result: list[str] = []
    in_fence = False
    fence_char = ""
    fence_len = 0

    for line in lines:
        if line.startswith(("__DRAWLIB_PRESERVED_FENCE_", "__DRAWLIB_FENCE_PAD_")):
            result.append("")
            continue
        if not in_fence:
            m_open = _FENCE_OPEN_RE.match(line)
            if m_open:
                in_fence = True
                marker = m_open.group(1)
                fence_char = marker[0]
                fence_len = len(marker)
                result.append("")
                continue
            result.append(line)
        else:
            result.append("")
            close_re = re.compile(rf"^[ \t]{{0,3}}{re.escape(fence_char)}{{{fence_len},}}[ \t\r]*$")
            if close_re.match(line):
                in_fence = False
                fence_char = ""
                fence_len = 0

    return result


def extract_api_headings(md_text: str, fallback_stem: str = "overview") -> ExtractedApiHeadings:
    """Extract ``# H1`` category title, ``## H2`` symbol items, and ``###/####`` subheadings from Markdown.

    Ignores fenced code blocks (including ````drawlib```` blocks) and HTML comments, and preserves
    literal angle-bracket placeholders such as ``/v1/users/<id>`` or ``Result<T>`` as plain text.

    Args:
        md_text: Raw Markdown source content.
        fallback_stem: Filename stem used if no ``# H1`` heading is present.

    Returns:
        ExtractedApiHeadings: Parsed heading hierarchy with deterministic, collision-free slugs.
    """
    lines = _mask_fences_and_comments(md_text)
    h1_title: str | None = None
    h1_raw: str | None = None
    used_slugs: set[str] = set()
    h2_items: list[ApiSubItem] = []
    sub_headings: list[tuple[int, str, str]] = []

    for line in lines:
        m = _ATX_HEADING_RE.match(line)
        if not m:
            continue
        level = len(m.group(1))
        raw_body = m.group(2).strip()

        if level == 1:
            if h1_title is None:
                h1_raw = raw_body
                h1_title = _strip_inline_markdown_preserving_angles(raw_body) or humanize_identifier(fallback_stem)
            continue

        if level == 2:
            badge_text: str | None = None
            badge_kind: str | None = None
            rest_raw = raw_body

            m_code = _LEADING_CODE_SPAN_RE.match(raw_body)
            if m_code:
                cand_badge = m_code.group(1).strip()
                norm_badge = cand_badge.lower()
                if norm_badge in KNOWN_API_BADGES and m_code.group(2).strip():
                    badge_text = cand_badge
                    badge_kind = KNOWN_API_BADGES[norm_badge]
                    rest_raw = m_code.group(2).strip()

            rest_plain = _strip_inline_markdown_preserving_angles(rest_raw)
            slug = slugify_api_heading(rest_plain, used_slugs, has_badge=(badge_kind is not None))
            s_label = compact_sidebar_label(badge_kind, rest_plain)
            h2_items.append(
                ApiSubItem(
                    slug=slug,
                    raw_title=rest_plain,
                    sidebar_label=s_label,
                    badge_text=badge_text,
                    badge_kind=badge_kind,
                )
            )
            continue

        if level in {3, 4}:
            sub_plain = _strip_inline_markdown_preserving_angles(raw_body)
            sub_slug = slugify_api_heading(sub_plain, used_slugs, has_badge=False)
            sub_headings.append((level, sub_slug, raw_body))

    resolved_h1 = h1_title if h1_title else humanize_identifier(fallback_stem)
    return ExtractedApiHeadings(
        h1_title=resolved_h1,
        h1_raw=h1_raw,
        h2_items=tuple(h2_items),
        sub_headings=tuple(sub_headings),
    )


def _strip_html_tags_plain(fragment: str) -> str:
    """Fallback HTML tag stripper for raw ``.html`` inputs."""
    return html.unescape(re.sub(r"<[^>]+>", "", fragment)).strip()


def _format_h2_html(item: ApiSubItem, raw_h2_markdown: str | None = None) -> str:
    """Format an upgraded ``<h2>`` HTML element with escaped ``id``, semantic badge, signature, and permalink."""
    esc_slug = html.escape(item.slug, quote=True)
    esc_aria = html.escape(f"Permalink to {item.sidebar_label}", quote=True)

    if item.badge_kind is not None and item.badge_text is not None:
        esc_badge = html.escape(item.badge_text, quote=True)
        esc_kind = html.escape(item.badge_kind, quote=True)
        if "(" in item.raw_title:
            sym_part, params_part = item.raw_title.split("(", 1)
            sig_inner = (
                f'<span class="api-sig-name">{html.escape(sym_part, quote=True)}</span>'
                f'<span class="api-sig-params">({html.escape(params_part, quote=True)}</span>'
            )
        else:
            sig_inner = f'<span class="api-sig-name">{html.escape(item.raw_title, quote=True)}</span>'

        return (
            f'<h2 id="{esc_slug}" class="api-symbol-heading">'
            f'<span class="api-badge api-badge-{esc_kind}">{esc_badge}</span>'
            f'<code class="api-sig">{sig_inner}</code>'
            f'<a class="header-anchor" href="#{esc_slug}" aria-label="{esc_aria}">#</a>'
            f"</h2>"
        )

    safe_inner = (
        _render_safe_inline_heading_html(raw_h2_markdown)
        if raw_h2_markdown is not None
        else html.escape(item.raw_title, quote=True)
    )
    return (
        f'<h2 id="{esc_slug}" class="api-section-heading">'
        f"<span>{safe_inner}</span>"
        f'<a class="header-anchor" href="#{esc_slug}" aria-label="{esc_aria}">#</a>'
        f"</h2>"
    )


def inject_api_heading_ids_and_badges(
    body_html: str,
    md_text: str | None = None,
    *,
    fallback_stem: str = "overview",
) -> tuple[str, str, list[ApiSubItem]]:
    """Upgrade ``<h1>``–``<h4>`` tags in ``body_html`` with deterministic ``id`` anchors and semantic badges.

    Protects ``<pre>...</pre>`` code blocks from modification, escapes all heading text and
    attribute values against XSS, and returns ``(h1_title, upgraded_html, subitems)``.
    """
    extracted = extract_api_headings(md_text, fallback_stem=fallback_stem) if md_text is not None else None
    raw_h2_lines: list[str] = []
    if md_text is not None:
        for line in _mask_fences_and_comments(md_text):
            m = _ATX_HEADING_RE.match(line)
            if m and len(m.group(1)) == 2:
                raw_h2_lines.append(m.group(2).strip())

    protected_pres: list[str] = []

    def _protect_pre(match: re.Match[str]) -> str:
        idx = len(protected_pres)
        protected_pres.append(match.group(0))
        return f"__DRAWLIB_API_PRE_MASK_{idx}__"

    masked_html = re.sub(r"(?is)<pre\b[^>]*>.*?</pre>", _protect_pre, body_html)

    h1_title = extracted.h1_title if extracted is not None else humanize_identifier(fallback_stem)
    h1_replaced = False

    def _replace_h1(match: re.Match[str]) -> str:
        nonlocal h1_replaced, h1_title
        if h1_replaced:
            return match.group(0)
        h1_replaced = True
        if extracted is None:
            h1_title = _strip_html_tags_plain(match.group(1)) or h1_title
            safe_h1 = html.escape(h1_title, quote=True)
        elif extracted.h1_raw is not None:
            safe_h1 = _render_safe_inline_heading_html(extracted.h1_raw)
        else:
            safe_h1 = html.escape(h1_title, quote=True)

        is_module_name = "." in h1_title or (bool(h1_title) and h1_title.islower())
        h1_cls = "api-page-title is-module" if is_module_name else "api-page-title"
        return f'<h1 class="{h1_cls}">{safe_h1}</h1>'

    masked_html = re.sub(r"(?is)<h1\b[^>]*>(.*?)</h1>", _replace_h1, masked_html, count=1)

    fallback_used_slugs: set[str] = (
        {it.slug for it in extracted.h2_items} | {sh[1] for sh in extracted.sub_headings}
        if extracted is not None
        else set()
    )
    final_subitems: list[ApiSubItem] = []
    h2_idx = 0

    def _replace_h2(match: re.Match[str]) -> str:
        nonlocal h2_idx
        if extracted is not None and h2_idx < len(extracted.h2_items):
            item = extracted.h2_items[h2_idx]
            raw_line = raw_h2_lines[h2_idx] if h2_idx < len(raw_h2_lines) else None
            h2_idx += 1
            final_subitems.append(item)
            return _format_h2_html(item, raw_h2_markdown=raw_line)

        h2_idx += 1
        inner_html = match.group(2).strip()
        badge_text: str | None = None
        badge_kind: str | None = None
        rest_html = inner_html
        code_prefix = re.match(r"^<code>([^<]+)</code>\s*(.*)$", inner_html, flags=re.DOTALL)
        if code_prefix:
            cand_badge = html.unescape(code_prefix.group(1)).strip()
            norm = cand_badge.lower()
            if norm in KNOWN_API_BADGES and _strip_html_tags_plain(code_prefix.group(2)):
                badge_text = cand_badge
                badge_kind = KNOWN_API_BADGES[norm]
                rest_html = code_prefix.group(2).strip()

        rest_plain = _strip_html_tags_plain(rest_html)
        slug = slugify_api_heading(rest_plain, fallback_used_slugs, has_badge=(badge_kind is not None))
        s_label = compact_sidebar_label(badge_kind, rest_plain)
        fallback_item = ApiSubItem(
            slug=slug,
            raw_title=rest_plain,
            sidebar_label=s_label,
            badge_text=badge_text,
            badge_kind=badge_kind,
        )
        final_subitems.append(fallback_item)
        return _format_h2_html(fallback_item)

    masked_html = re.sub(r"(?is)<h2([^>]*)>(.*?)</h2>", _replace_h2, masked_html)

    sub_idx = 0

    def _replace_sub_h(match: re.Match[str]) -> str:
        nonlocal sub_idx
        tag = match.group(1).lower()
        attrs = match.group(2)
        inner = match.group(3)
        level = 3 if tag == "h3" else 4

        if extracted is not None and sub_idx < len(extracted.sub_headings):
            exp_level, sub_slug, sub_raw = extracted.sub_headings[sub_idx]
            if exp_level == level:
                sub_idx += 1
                esc_slug = html.escape(sub_slug, quote=True)
                safe_sub = _render_safe_inline_heading_html(sub_raw)
                if tag == "h3":
                    return (
                        f'<h3 id="{esc_slug}">{safe_sub}'
                        f'<a class="header-anchor" href="#{esc_slug}" aria-label="Permalink">#</a></h3>'
                    )
                return f'<h4 id="{esc_slug}">{safe_sub}</h4>'

        if re.search(r"\bid\s*=", attrs, flags=re.IGNORECASE):
            return match.group(0)
        txt = _strip_html_tags_plain(inner)
        slug = slugify_api_heading(txt, fallback_used_slugs, has_badge=False)
        esc_slug = html.escape(slug, quote=True)
        safe_txt = html.escape(txt, quote=True)
        return f'<{tag} id="{esc_slug}">{safe_txt}</{tag}>'

    masked_html = re.sub(r"(?is)<(h[34])([^>]*)>(.*?)</\1>", _replace_sub_h, masked_html)

    for idx, orig_pre in enumerate(protected_pres):
        masked_html = masked_html.replace(f"__DRAWLIB_API_PRE_MASK_{idx}__", orig_pre)

    return h1_title, masked_html, final_subitems


def order_api_locale_files(
    lang_dir_abs: str,
    rel_files: list[str],
) -> tuple[list[tuple[str, str | None]], str | None]:
    """Determine deterministic page ordering and optional group titles for an ``api`` locale.

    If ``navbar.md`` exists in ``lang_dir_abs``, uses its section titles and file order (appending
    any unlisted files afterward). Otherwise places root ``index.*`` first (when present) followed
    by sorted paths, deriving group headings from top-level subdirectory names when nested.

    Returns:
        tuple[list[tuple[str, str | None]], str | None]:
            - Ordered list of ``(rel_path, section_title)`` pairs.
            - Optional ``site_title`` extracted from ``navbar.md`` ``# H1`` if present.
    """
    nav_path = resolve_locale_navbar_path(lang_dir_abs)
    rel_by_abs: dict[str, str] = {
        os.path.abspath(os.path.join(lang_dir_abs, *rp.split("/"))): rp for rp in rel_files
    }

    if nav_path is not None:
        nav_sections: list[NavbarSection]
        nav_site_title: str | None
        nav_sections, nav_site_title = parse_navbar_markdown(nav_path, lang_dir_abs)
        ordered: list[tuple[str, str | None]] = []
        seen: set[str] = set()
        for sec in nav_sections:
            for item in sec.items:
                if item.is_external or not item.target_file_abs:
                    continue
                abs_target = os.path.abspath(item.target_file_abs)
                rp = rel_by_abs.get(abs_target)
                if rp is not None and rp not in seen:
                    seen.add(rp)
                    ordered.append((rp, sec.title))
        for rp in rel_files:
            if rp not in seen:
                top_dir = rp.split("/", 1)[0] if "/" in rp else ""
                sec_lbl = humanize_identifier(top_dir) if top_dir else None
                ordered.append((rp, sec_lbl))
        return ordered, nav_site_title

    index_names = {"index.md", "index.markdown", "index.html", "index.htm"}
    root_indices = [rp for rp in rel_files if "/" not in rp and rp.lower() in index_names]
    others = [rp for rp in rel_files if rp not in set(root_indices)]
    sorted_all = root_indices + others

    ordered_auto: list[tuple[str, str | None]] = []
    for rp in sorted_all:
        if "/" in rp:
            top_dir = rp.split("/", 1)[0]
            ordered_auto.append((rp, humanize_identifier(top_dir)))
        else:
            ordered_auto.append((rp, None))
    return ordered_auto, None


def _compute_category_filter_key(h1_title: str, common_pkg_prefix: str | None) -> str:
    """Compute category filter key stripping a shared package prefix (e.g. ``'drawlib.'``) if common."""
    if common_pkg_prefix and h1_title.lower().startswith(common_pkg_prefix.lower()):
        trimmed = h1_title[len(common_pkg_prefix) :].strip()
        if trimmed:
            return trimmed
    return h1_title


def _detect_common_dotted_prefix(pages: list[CompiledApiPage]) -> str | None:
    """Detect a shared leading ``<pkg>.`` prefix across 2+ module-named pages."""
    prefixes: list[str] = []
    for p in pages:
        if "." in p.h1_title and " " not in p.h1_title.strip():
            head = p.h1_title.split(".", 1)[0]
            if head:
                prefixes.append(f"{head}.")
    if len(prefixes) >= 2 and len(set(p.lower() for p in prefixes)) == 1:
        return prefixes[0]
    return None


def build_api_page_navigation_context(
    *,
    pages: list[CompiledApiPage],
    active_index: int,
    current_dest_abs: str,
    sidebar_expanded: bool,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """Build ``(api_nav_sections, api_pager)`` template context relative to ``current_dest_abs``."""
    current_dir = os.path.dirname(os.path.abspath(current_dest_abs))
    common_prefix = _detect_common_dotted_prefix(pages)

    sections: list[dict[str, Any]] = []
    for idx, page in enumerate(pages):
        is_active = idx == active_index
        rel_page_url = os.path.relpath(page.dest_abs, current_dir).replace(os.sep, "/")
        is_prose = "." not in page.h1_title and not (bool(page.h1_title) and page.h1_title.islower())
        cat_filter = _compute_category_filter_key(page.h1_title, common_prefix)

        items_ctx: list[dict[str, Any]] = []
        for sub in page.subitems:
            sub_href = f"#{sub.slug}" if is_active else f"{rel_page_url}#{sub.slug}"
            items_ctx.append(
                {
                    "slug": sub.slug,
                    "label": sub.sidebar_label,
                    "url": sub_href,
                    "badge_text": sub.badge_text,
                    "badge_kind": sub.badge_kind,
                    "filter_text": f"{sub.badge_text or ''} {sub.sidebar_label}".strip(),
                }
            )

        page_entry: dict[str, Any] = {
            "title": page.h1_title,
            "filter_key": cat_filter,
            "url": rel_page_url,
            "is_prose": is_prose,
            "active": is_active,
            "expanded": bool(sidebar_expanded or is_active),
            "subitems": items_ctx,
        }

        if not sections or sections[-1]["title"] != page.section_title:
            sections.append({"title": page.section_title, "pages": [page_entry]})
        else:
            sections[-1]["pages"].append(page_entry)

    prev_ctx: dict[str, str] | None = None
    if active_index > 0:
        prev_p = pages[active_index - 1]
        prev_ctx = {
            "title": prev_p.h1_title,
            "url": os.path.relpath(prev_p.dest_abs, current_dir).replace(os.sep, "/"),
        }

    next_ctx: dict[str, str] | None = None
    if active_index + 1 < len(pages):
        next_p = pages[active_index + 1]
        next_ctx = {
            "title": next_p.h1_title,
            "url": os.path.relpath(next_p.dest_abs, current_dir).replace(os.sep, "/"),
        }

    return sections, {"prev": prev_ctx, "next": next_ctx}


def resolve_api_chrome_context(
    *,
    api_cfg: ApiConfig,
    lang: str,
    default_lang: str,
    lang_out_dir: str,
    current_dest_abs: str,
) -> dict[str, Any]:
    """Resolve localized subbar badge, repo URL, header links, and UI labels for ``current_dest_abs``."""
    current_dir = os.path.dirname(os.path.abspath(current_dest_abs))

    def _rebase_if_rel(url: str | None) -> str | None:
        if not url:
            return None
        trimmed = url.strip()
        if trimmed.lower().startswith(("http://", "https://")) or trimmed.startswith(("/", "#")):
            return trimmed
        frag = ""
        base_u = trimmed
        if "#" in base_u:
            base_u, frag = base_u.split("#", 1)
            frag = f"#{frag}"
        query = ""
        if "?" in base_u:
            base_u, query = base_u.split("?", 1)
            query = f"?{query}"
        if not base_u:
            return trimmed
        resolved_target = os.path.normpath(os.path.join(lang_out_dir, base_u))
        rebased = os.path.relpath(resolved_target, current_dir).replace(os.sep, "/")
        return f"{rebased}{query}{frag}"

    badge_text = api_cfg.resolve_badge_text(lang, default_lang=default_lang) or None
    badge_url = _rebase_if_rel(api_cfg.badge_url) if badge_text else None
    repo_url = api_cfg.repo_url

    header_links_ctx: list[dict[str, Any]] = []
    for hlink in api_cfg.header_links:
        lbl = hlink.resolve_label(lang, default_lang=default_lang)
        if not lbl:
            continue
        resolved_u = hlink.url if hlink.is_external else (_rebase_if_rel(hlink.url) or hlink.url)
        header_links_ctx.append(
            {
                "label": lbl,
                "url": resolved_u,
                "is_external": hlink.is_external,
            }
        )

    is_ja = lang.lower().startswith("ja")
    ui_labels = (
        {
            "breadcrumb_root": "API リファレンス",
            "filter_placeholder": "API シンボルを絞り込み...",
            "modules_label": "カテゴリ & シンボル",
            "expand_all": "すべて展開",
            "collapse_all": "すべて折りたたむ",
            "no_matches": "一致するシンボルが見つかりません。",
            "prev_label": "前へ",
            "next_label": "次へ",
        }
        if is_ja
        else {
            "breadcrumb_root": "API Reference",
            "filter_placeholder": "Filter API symbols...",
            "modules_label": "Categories & Symbols",
            "expand_all": "Expand All",
            "collapse_all": "Collapse All",
            "no_matches": "No matching symbols found.",
            "prev_label": "Previous",
            "next_label": "Next",
        }
    )

    return {
        "sidebar_expanded": api_cfg.sidebar_expanded,
        "api_badge_text": badge_text,
        "api_badge_url": badge_url,
        "api_repo_url": repo_url,
        "api_header_links": header_links_ctx,
        "api_ui": ui_labels,
    }
