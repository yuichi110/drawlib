# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""HTML and PDF document renderer using html_templates/html_css and pdf_templates/pdf_css."""

from __future__ import annotations

import os
import re
from typing import Any, Literal

from jinja2 import Environment, FileSystemLoader
from markupsafe import Markup

from drawlib._templates import get_css, localize_css_for_language
from drawlib._templates.langs import get_language_config


def get_default_css(
    custom_css_path: str | None = None,
    target: Literal["html", "pdf", "api"] = "html",
    lang: str = "en",
) -> str:
    """Get complete theme CSS content string for HTML, API, or PDF.

    Args:
        custom_css_path (Optional[str]): Built-in CSS preset name or path to custom CSS file.
        target (Literal["html", "pdf", "api"]): Target format ('html', 'pdf', or 'api'). Defaults to 'html'.
        lang (str): Language code or alias (e.g. 'en', 'ja', 'th'). Defaults to 'en'.

    Returns:
        str: Complete CSS content string.

    Raises:
        ValueError: If specified CSS preset name is unknown or unsupported for the target format.
    """
    if custom_css_path and os.path.exists(custom_css_path):
        with open(custom_css_path, "r", encoding="utf-8") as f:
            return localize_css_for_language(f.read(), lang=lang)
    return get_css(name=custom_css_path, target=target, lang=lang)


def get_pdf_css(custom_css_path: str | None = None, lang: str = "en") -> str:
    """Get complete PDF CSS content string from pdf or custom CSS file path.

    Args:
        custom_css_path (Optional[str]): Built-in PDF CSS preset name or path to custom CSS file.
        lang (str): Language code or alias (e.g. 'en', 'ja', 'th'). Defaults to 'en'.

    Returns:
        str: Complete PDF CSS content string.
    """
    return get_css(name=custom_css_path, target="pdf", lang=lang)


def _ensure_i18n_head_metadata(
    rendered: str,
    html_lang: str | None,
    html_dir: str | None,
    font_link_html: str | None,
    alternate_links: list[dict[str, str]] | None,
    seo_meta_html: str | None = None,
) -> str:
    """Ensure html lang/dir, Google Fonts link, hreflang links, and SEO tags are present on templates."""
    import html as html_lib  # noqa: PLC0415

    if html_lang:
        eff_dir = html_dir or "ltr"
        esc_lang = html_lib.escape(html_lang, quote=True)
        esc_dir = html_lib.escape(eff_dir, quote=True)
        rendered = re.sub(
            r"<html\b[^>]*>",
            f'<html lang="{esc_lang}" dir="{esc_dir}">',
            rendered,
            count=1,
            flags=re.IGNORECASE,
        )

    extra_head_lines: list[str] = []
    if font_link_html and "fonts.googleapis.com" not in rendered:
        extra_head_lines.append(f"    {font_link_html}")
    if alternate_links and 'rel="alternate"' not in rendered:
        for alt in alternate_links:
            esc_hreflang = html_lib.escape(alt["hreflang"], quote=True)
            esc_url = html_lib.escape(alt["url"], quote=True)
            extra_head_lines.append(
                f'    <link rel="alternate" hreflang="{esc_hreflang}" href="{esc_url}">'
            )
    if seo_meta_html and 'property="og:title"' not in rendered:
        extra_head_lines.append(seo_meta_html)

    if extra_head_lines and "</head>" in rendered:
        injection = "\n".join(extra_head_lines) + "\n</head>"
        rendered = rendered.replace("</head>", injection, 1)

    return rendered


def render_html_document(
    body_html: str,
    title: str = "Drawlib Document",
    custom_css_path: str | None = None,
    css_href: str | None = None,
    nav_items: list[dict[str, Any]] | None = None,
    nav_sections: list[dict[str, Any]] | None = None,
    template_path: str | None = None,
    index_url: str = "index.html",
    site_title: str | None = None,
    favicon_href: str | None = None,
    logo_href: str | None = None,
    logo_dark_href: str | None = None,
    html_lang: str | None = None,
    html_dir: str | None = None,
    font_link_html: str | None = None,
    languages: list[dict[str, Any]] | None = None,
    alternate_links: list[dict[str, str]] | None = None,
    css_lang: str = "en",
    seo_meta_html: str | None = None,
    css_target: Literal["html", "api"] = "html",
    extra_context: dict[str, Any] | None = None,
) -> str:
    """Render full standalone HTML document using template and html_css.

    Args:
        body_html (str): HTML body snippet.
        title (str): Document title.
        custom_css_path (Optional[str]): Preset name or path to custom CSS file to inject.
        css_href (Optional[str]): Relative path/href for external stylesheet link.
        nav_items (Optional[List[Dict[str, Any]]]): Navigation items for sidebar menu.
        nav_sections (Optional[List[Dict[str, Any]]]): Categorized navigation sections for sidebar menu.
        template_path (Optional[str]): File path to template.html.
        index_url (str): Relative URL to root index.html for brand link. Defaults to 'index.html'.
        site_title (Optional[str]): Site / brand title displayed in header (e.g. from navbar.md). Defaults to 'drawlib'.
        favicon_href (Optional[str]): Relative path/href for favicon link. Defaults to None.
        logo_href (Optional[str]): Relative path/href for light mode brand logo image. Defaults to None.
        logo_dark_href (Optional[str]): Relative path/href for dark mode brand logo image. Defaults to None.
        html_lang (Optional[str]): Explicit BCP-47 language tag for ``<html lang="...">``.
        html_dir (Optional[str]): Explicit writing direction (``'ltr'`` or ``'rtl'``).
        font_link_html (Optional[str]): Explicit Google Fonts ``<link>`` HTML snippet.
        languages (Optional[List[Dict[str, Any]]]): Multi-locale language switcher link items.
        alternate_links (Optional[List[Dict[str, str]]]): ``hreflang`` alternate link entries.
        css_lang (str): Language code for embedded CSS font localization when ``css_href`` is None.
        seo_meta_html (Optional[str]): Pre-escaped SEO/OGP/Twitter ``<meta>`` and canonical ``<link>`` snippet.
        css_target (Literal["html", "api"]): CSS target preset when embedding CSS inline.
        extra_context (Optional[Dict[str, Any]]): Additional Jinja2 template variables (e.g. API navigation context).

    Returns:
        str: Complete HTML string.

    Raises:
        ValueError: If template_path is not specified or does not exist.
    """
    if not template_path or not os.path.exists(template_path):
        raise ValueError(f'Template file "{template_path}" does not exist.')

    tmpl_abs = os.path.abspath(template_path)
    tmpl_dir = os.path.dirname(tmpl_abs)
    tmpl_name = os.path.basename(tmpl_abs)
    custom_env = Environment(loader=FileSystemLoader(tmpl_dir), autoescape=True)
    template = custom_env.get_template(tmpl_name)

    custom_css_content = ""
    if not css_href:
        custom_css_content = get_default_css(custom_css_path=custom_css_path, target=css_target, lang=css_lang)

    render_kwargs: dict[str, Any] = {
        "title": title,
        "body": Markup(body_html),  # noqa: S704
        "custom_css": Markup(custom_css_content),  # noqa: S704
        "css_href": css_href,
        "nav_items": nav_items or [],
        "nav_sections": nav_sections or [],
        "index_url": index_url,
        "site_title": site_title or "drawlib",
        "favicon_href": favicon_href,
        "logo_href": logo_href,
        "logo_dark_href": logo_dark_href,
        "languages": languages or [],
        "alternate_links": alternate_links or [],
        "seo_meta_html": Markup(seo_meta_html or ""),  # noqa: S704
    }
    if html_lang is not None:
        render_kwargs["html_lang"] = html_lang
    if html_dir is not None:
        render_kwargs["html_dir"] = html_dir
    if font_link_html is not None:
        render_kwargs["font_link_html"] = Markup(font_link_html)  # noqa: S704
    if extra_context:
        render_kwargs.update(extra_context)

    rendered = template.render(**render_kwargs)
    if html_lang is not None or font_link_html is not None or alternate_links or seo_meta_html:
        rendered = _ensure_i18n_head_metadata(
            rendered=rendered,
            html_lang=html_lang,
            html_dir=html_dir,
            font_link_html=font_link_html,
            alternate_links=alternate_links,
            seo_meta_html=seo_meta_html,
        )
    return rendered


def render_pdf_document(
    body_html: str,
    title: str = "Drawlib Document",
    custom_css_path: str | None = None,
    template_path: str | None = None,
    lang: str = "en",
) -> str:
    """Render merged HTML document for PDF compilation using template and pdf_css.

    Args:
        body_html (str): Merged HTML body snippet.
        title (str): Document title.
        custom_css_path (Optional[str]): PDF CSS preset or path to custom CSS file.
        template_path (Optional[str]): File path to template.html.
        lang (str): Canonical language code for CSS font localization and HTML metadata.

    Returns:
        str: Complete HTML string ready for headless PDF export.

    Raises:
        ValueError: If template_path is not specified or does not exist.
    """
    if template_path and os.path.exists(template_path):
        tmpl_abs = os.path.abspath(template_path)
        tmpl_dir = os.path.dirname(tmpl_abs)
        tmpl_name = os.path.basename(tmpl_abs)
        custom_env = Environment(loader=FileSystemLoader(tmpl_dir), autoescape=True)
        template = custom_env.get_template(tmpl_name)
    else:
        template = Environment(autoescape=True).from_string(
            "<!DOCTYPE html>\n"
            '<html lang="en">\n'
            "<head>\n"
            '    <meta charset="UTF-8">\n'
            '    <title>{{ title | default("Drawlib Document") }}</title>\n'
            "    {% if custom_css %}\n"
            "    <style>\n"
            "{{ custom_css | safe }}\n"
            "    </style>\n"
            "    {% endif %}\n"
            "</head>\n"
            '<body class="pdf-document">\n'
            '    <div class="main-content">\n'
            "        {{ body | safe }}\n"
            "    </div>\n"
            "</body>\n"
            "</html>"
        )

    lang_cfg = get_language_config(lang)
    custom_css_content = get_pdf_css(custom_css_path=custom_css_path, lang=lang)

    rendered = template.render(
        title=title,
        body=Markup(body_html),  # noqa: S704
        custom_css=Markup(custom_css_content),  # noqa: S704
        css_href=None,
        nav_items=[],
        nav_sections=[],
        languages=[],
        alternate_links=[],
        seo_meta_html="",
        html_lang=lang_cfg.code,
        html_dir=lang_cfg.direction,
        font_link_html=Markup(lang_cfg.font_link_html),  # noqa: S704
    )
    return _ensure_i18n_head_metadata(
        rendered=rendered,
        html_lang=lang_cfg.code,
        html_dir=lang_cfg.direction,
        font_link_html=lang_cfg.font_link_html,
        alternate_links=None,
    )
