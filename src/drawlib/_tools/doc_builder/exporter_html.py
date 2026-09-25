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

from drawlib._tools.doc_builder.template import BUILTIN_HTML_CSS_PRESETS, BUILTIN_PDF_CSS_PRESETS


def get_default_css(
    custom_css_path: Optional[str] = None,
    target: Literal["html", "pdf"] = "html",
) -> str:
    """Get complete theme CSS content string for HTML ('html_css') or PDF ('pdf_css').

    Args:
        custom_css_path (Optional[str]): Built-in CSS preset name or path to custom CSS file.
        target (Literal["html", "pdf"]): Target format ('html' or 'pdf'). Defaults to 'html'.

    Returns:
        str: Complete CSS content string.

    Raises:
        ValueError: If specified CSS preset name is unknown or unsupported for the target format.
    """
    subdir = "pdf_css" if target == "pdf" else "html_css"
    styles_dir = os.path.join(os.path.dirname(__file__), subdir)
    registry = BUILTIN_PDF_CSS_PRESETS if target == "pdf" else BUILTIN_HTML_CSS_PRESETS

    if not custom_css_path:
        default_file = os.path.join(styles_dir, "default.css")
        if os.path.exists(default_file):
            with open(default_file, "r", encoding="utf-8") as f:
                return f.read()
        return ""

    # Check if custom file path exists
    if os.path.exists(custom_css_path):
        with open(custom_css_path, "r", encoding="utf-8") as f:
            return f.read()

    # Check built-in presets
    normalized = "google" if (target == "pdf" and custom_css_path == "google-pdf") else custom_css_path
    if normalized in registry:
        preset_file = os.path.join(styles_dir, registry[normalized]["file"])
        if os.path.exists(preset_file):
            with open(preset_file, "r", encoding="utf-8") as f:
                return f.read()

    available = ", ".join(registry.keys())
    msg = f"Unknown or unsupported {target.upper()} CSS preset '{custom_css_path}'. Available presets: {available}"
    raise ValueError(msg)


def get_pdf_css(custom_css_path: Optional[str] = None) -> str:
    """Get complete PDF CSS content string from pdf_css or custom CSS file path."""
    return get_default_css(custom_css_path=custom_css_path, target="pdf")


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
) -> str:
    """Render full standalone HTML document using html_templates and html_css.

    Args:
        body_html (str): HTML body snippet.
        title (str): Document title.
        custom_css_path (Optional[str]): Preset name or path to custom CSS file to inject.
        css_href (Optional[str]): Relative path/href for external stylesheet link.
        nav_items (Optional[List[Dict[str, Any]]]): Navigation items for sidebar menu.
        nav_sections (Optional[List[Dict[str, Any]]]): Categorized navigation sections for sidebar menu.
        template_path (Optional[str]): Optional HTML template preset ('sidebar', 'simple') or file path.
        index_url (str): Relative URL to root index.html for brand link. Defaults to 'index.html'.
        site_title (Optional[str]): Site / brand title displayed in header (e.g. from navbar.md). Defaults to 'drawlib'.

    Returns:
        str: Complete HTML string.
    """
    templates_dir = os.path.join(os.path.dirname(__file__), "html_templates")
    builtin_env = Environment(loader=FileSystemLoader(templates_dir))

    if template_path in {"simple", "standalone"}:
        template = builtin_env.get_template("simple.html.j2")
    elif template_path == "sidebar":
        template = builtin_env.get_template("sidebar.html.j2")
    elif template_path and os.path.exists(template_path):
        tmpl_abs = os.path.abspath(template_path)
        tmpl_dir = os.path.dirname(tmpl_abs)
        tmpl_name = os.path.basename(tmpl_abs)
        custom_env = Environment(loader=FileSystemLoader(tmpl_dir))
        template = custom_env.get_template(tmpl_name)
    elif (nav_sections and len(nav_sections) > 0) or (nav_items and len(nav_items) > 0):
        template = builtin_env.get_template("sidebar.html.j2")
    else:
        template = builtin_env.get_template("simple.html.j2")

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
    )


def render_pdf_document(
    body_html: str,
    title: str = "Drawlib Document",
    custom_css_path: Optional[str] = None,
    template_path: Optional[str] = None,
) -> str:
    """Render merged HTML document for PDF compilation using pdf_templates and pdf_css.

    Args:
        body_html (str): Merged HTML body snippet.
        title (str): Document title.
        custom_css_path (Optional[str]): PDF CSS preset ('default', 'google', 'github', 'minimal',
            'monochrome') or path to custom CSS file.
        template_path (Optional[str]): PDF template preset ('default', 'book') or custom .html.j2 file path.

    Returns:
        str: Complete HTML string ready for headless PDF export.
    """
    templates_dir = os.path.join(os.path.dirname(__file__), "pdf_templates")
    builtin_env = Environment(loader=FileSystemLoader(templates_dir))

    if template_path in {None, "", "default", "simple", "standalone"}:
        template = builtin_env.get_template("default.html.j2")
    elif template_path == "book":
        template = builtin_env.get_template("book.html.j2")
    elif template_path and os.path.exists(template_path):
        tmpl_abs = os.path.abspath(template_path)
        tmpl_dir = os.path.dirname(tmpl_abs)
        tmpl_name = os.path.basename(tmpl_abs)
        custom_env = Environment(loader=FileSystemLoader(tmpl_dir))
        template = custom_env.get_template(tmpl_name)
    else:
        available = "default, book"
        raise ValueError(f"Unknown PDF template preset '{template_path}'. Available presets: {available}")

    custom_css_content = get_pdf_css(custom_css_path=custom_css_path)

    return template.render(
        title=title,
        body=body_html,
        custom_css=custom_css_content,
        css_href=None,
        nav_items=[],
    )
