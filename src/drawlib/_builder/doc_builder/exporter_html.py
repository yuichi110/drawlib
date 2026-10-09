# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""HTML and PDF document renderer using html_templates/html_css and pdf_templates/pdf_css."""

import os
from typing import Any, Dict, List, Literal, Optional

from jinja2 import Environment, FileSystemLoader

from drawlib._templates import get_css


def get_default_css(
    custom_css_path: Optional[str] = None,
    target: Literal["html", "pdf"] = "html",
    lang: str = "en",
) -> str:
    """Get complete theme CSS content string for HTML or PDF.

    Args:
        custom_css_path (Optional[str]): Built-in CSS preset name or path to custom CSS file.
        target (Literal["html", "pdf"]): Target format ('html' or 'pdf'). Defaults to 'html'.
        lang (str): Language code or alias (e.g. 'en', 'ja', 'th'). Defaults to 'en'.

    Returns:
        str: Complete CSS content string.

    Raises:
        ValueError: If specified CSS preset name is unknown or unsupported for the target format.
    """
    return get_css(name=custom_css_path, target=target, lang=lang)


def get_pdf_css(custom_css_path: Optional[str] = None, lang: str = "en") -> str:
    """Get complete PDF CSS content string from pdf or custom CSS file path.

    Args:
        custom_css_path (Optional[str]): Built-in PDF CSS preset name or path to custom CSS file.
        lang (str): Language code or alias (e.g. 'en', 'ja', 'th'). Defaults to 'en'.

    Returns:
        str: Complete PDF CSS content string.
    """
    return get_css(name=custom_css_path, target="pdf", lang=lang)


def render_html_document(
    body_html: str,
    title: str = "Drawlib Document",
    custom_css_path: Optional[str] = None,
    css_href: Optional[str] = None,
    nav_items: Optional[List[Dict[str, Any]]] = None,
    nav_sections: Optional[List[Dict[str, Any]]] = None,
    template_path: Optional[str] = None,
    index_url: str = "index.html",
    site_title: Optional[str] = None,
    favicon_href: Optional[str] = None,
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
    custom_env = Environment(loader=FileSystemLoader(tmpl_dir))
    template = custom_env.get_template(tmpl_name)

    custom_css_content = ""
    if not css_href:
        custom_css_content = get_default_css(custom_css_path=custom_css_path, target="html")

    return template.render(
        title=title,
        body=body_html,
        custom_css=custom_css_content,
        css_href=css_href,
        nav_items=nav_items or [],
        nav_sections=nav_sections or [],
        index_url=index_url,
        site_title=site_title or "drawlib",
        favicon_href=favicon_href,
    )


def render_pdf_document(
    body_html: str,
    title: str = "Drawlib Document",
    custom_css_path: Optional[str] = None,
    template_path: Optional[str] = None,
) -> str:
    """Render merged HTML document for PDF compilation using template and pdf_css.

    Args:
        body_html (str): Merged HTML body snippet.
        title (str): Document title.
        custom_css_path (Optional[str]): PDF CSS preset or path to custom CSS file.
        template_path (Optional[str]): File path to template.html.

    Returns:
        str: Complete HTML string ready for headless PDF export.

    Raises:
        ValueError: If template_path is not specified or does not exist.
    """
    if template_path and os.path.exists(template_path):
        tmpl_abs = os.path.abspath(template_path)
        tmpl_dir = os.path.dirname(tmpl_abs)
        tmpl_name = os.path.basename(tmpl_abs)
        custom_env = Environment(loader=FileSystemLoader(tmpl_dir))
        template = custom_env.get_template(tmpl_name)
    else:
        template = Environment().from_string(
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

    custom_css_content = get_pdf_css(custom_css_path=custom_css_path)

    return template.render(
        title=title,
        body=body_html,
        custom_css=custom_css_content,
        css_href=None,
        nav_items=[],
    )
