# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""HTML exporter for rendering standalone single-file HTML documents."""

import os
from typing import Any, Dict, List, Optional

from jinja2 import Environment, FileSystemLoader


def get_default_css(custom_css_path: Optional[str] = None) -> str:
    """Get complete theme CSS content string (built-in preset or custom CSS file).

    Args:
        custom_css_path (Optional[str]): Built-in CSS preset name ('default', 'github', 'monochrome', 'minimal')
            or path to custom CSS file.

    Returns:
        str: Complete CSS content string.
    """
    styles_dir = os.path.join(os.path.dirname(__file__), "html_styles")

    # Built-in presets
    if custom_css_path in {"default", "github", "monochrome", "minimal"}:
        preset_file = os.path.join(styles_dir, f"{custom_css_path}.css")
        if os.path.exists(preset_file):
            with open(preset_file, "r", encoding="utf-8") as f:
                return f.read()

    # Custom file path
    if custom_css_path and os.path.exists(custom_css_path):
        with open(custom_css_path, "r", encoding="utf-8") as f:
            return f.read()

    # Fallback to built-in default.css
    default_file = os.path.join(styles_dir, "default.css")
    if os.path.exists(default_file):
        with open(default_file, "r", encoding="utf-8") as f:
            return f.read()

    return ""


def render_html_document(
    body_html: str,
    title: str = "Drawlib Document",
    custom_css_path: Optional[str] = None,
    css_href: Optional[str] = None,
    nav_items: Optional[List[Dict[str, Any]]] = None,
    template_path: Optional[str] = None,
) -> str:
    """Render full standalone HTML document with embedded CSS or external CSS link.

    Args:
        body_html (str): HTML body snippet.
        title (str): Document title.
        custom_css_path (Optional[str]): Path to custom CSS file to inject.
        css_href (Optional[str]): Relative path/href for external stylesheet link.
        nav_items (Optional[List[Dict[str, Any]]]): Navigation items for sidebar menu.
        template_path (Optional[str]): Optional path to custom Jinja2 HTML template.

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
    elif nav_items and len(nav_items) > 0:
        template = builtin_env.get_template("sidebar.html.j2")
    else:
        template = builtin_env.get_template("simple.html.j2")

    custom_css = get_default_css(custom_css_path) if custom_css_path else get_default_css("default")

    return template.render(
        body=body_html,
        title=title,
        custom_css=custom_css,
        css_href=css_href,
        nav_items=nav_items or [],
    )
