# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Template and CSS preset listing, export, and validation utilities for drawlib doc_builder."""

from __future__ import annotations

import os
import shutil
from typing import Dict, List, Tuple

import jinja2
import jinja2.meta

BUILTIN_TEMPLATES: Dict[str, Dict[str, str]] = {
    "sidebar": {
        "file": "sidebar.html.j2",
        "description": "Multi-page documentation layout with collapsible left sidebar navigation.",
    },
    "simple": {
        "file": "simple.html.j2",
        "description": "Standalone single-column document layout without sidebar.",
    },
}

BUILTIN_CSS_PRESETS: Dict[str, Dict[str, str]] = {
    "default": {
        "file": "default.css",
        "description": "Modern responsive documentation theme with clean typography.",
    },
    "google": {
        "file": "google.css",
        "description": "Clean editorial Google Blog (The Keyword) & Material Design style.",
    },
    "github": {
        "file": "github.css",
        "description": "GitHub-flavored Markdown style with familiar code block and table formatting.",
    },
    "minimal": {
        "file": "minimal.css",
        "description": "Lightweight, distraction-free minimalist typography.",
    },
    "monochrome": {
        "file": "monochrome.css",
        "description": "High-contrast black-and-white style suited for printing and formal publications.",
    },
}


def list_templates() -> List[Dict[str, str]]:
    """Return metadata for all built-in Jinja2 HTML templates.

    Returns:
        List[Dict[str, str]]: List of dicts with keys 'name', 'file', and 'description'.
    """
    return [
        {"name": name, "file": meta["file"], "description": meta["description"]}
        for name, meta in BUILTIN_TEMPLATES.items()
    ]


def export_template(name: str = "sidebar", output: str = "template.html.j2") -> str:
    """Export a built-in HTML template ('sidebar' or 'simple') to a target file path.

    Args:
        name (str): Name of built-in template ('sidebar' or 'simple'). Defaults to 'sidebar'.
        output (str): Destination file path. Defaults to 'template.html.j2'.

    Returns:
        str: Absolute file path of the exported template.

    Raises:
        ValueError: If template name is unknown.
        FileNotFoundError: If built-in template file is missing.
    """
    normalized = "simple" if name == "standalone" else name
    if normalized not in BUILTIN_TEMPLATES:
        available = ", ".join(BUILTIN_TEMPLATES.keys())
        raise ValueError(f"Unknown template preset '{name}'. Available presets: {available}")

    templates_dir = os.path.join(os.path.dirname(__file__), "templates")
    filename = BUILTIN_TEMPLATES[normalized]["file"]
    src_path = os.path.join(templates_dir, filename)

    if not os.path.exists(src_path):
        raise FileNotFoundError(f"Built-in template not found at '{src_path}'.")

    dest_abs = os.path.abspath(output)
    os.makedirs(os.path.dirname(dest_abs), exist_ok=True)
    shutil.copy2(src_path, dest_abs)
    return dest_abs


def export_default_template(output_path: str = "template.html.j2", template_name: str = "sidebar") -> str:
    """Export built-in HTML template (alias for export_template for backward compatibility).

    Args:
        output_path (str): File path to save the exported template.
        template_name (str): Name of built-in template to export ('sidebar' or 'simple').

    Returns:
        str: Absolute file path of the exported template.
    """
    return export_template(name=template_name, output=output_path)


def validate_template(template_path: str) -> Tuple[bool, List[str]]:
    """Validate Jinja2 syntax and required variable placeholders in a custom template file.

    Args:
        template_path (str): File path to Jinja2 HTML template.

    Returns:
        Tuple[bool, List[str]]: (is_valid, messages_list).
    """
    path_abs = os.path.abspath(template_path)
    if not os.path.exists(path_abs):
        return False, [f"Template file '{path_abs}' does not exist."]

    try:
        with open(path_abs, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        return False, [f"Failed to read template file: {e}"]

    env = jinja2.Environment()
    try:
        parsed_ast = env.parse(content)
    except jinja2.exceptions.TemplateSyntaxError as e:
        return False, [f"Jinja2 Syntax Error at line {e.lineno}: {e.message}"]
    except Exception as e:
        return False, [f"Template Parsing Error: {e}"]

    referenced_vars = jinja2.meta.find_undeclared_variables(parsed_ast)
    messages: List[str] = []

    if "body" not in referenced_vars:
        msg = "Error: Template is missing mandatory placeholder 'body' (e.g. {{ body }} or {{ body | safe }})."
        messages.append(msg)
        return False, messages

    messages.append(f"Template '{os.path.basename(template_path)}' is valid.")

    missing_recommended: List[str] = []
    if "title" not in referenced_vars:
        missing_recommended.append("title")
    if "nav_items" not in referenced_vars:
        missing_recommended.append("nav_items")
    if "css_href" not in referenced_vars and "custom_css" not in referenced_vars:
        missing_recommended.append("css_href / custom_css")

    if missing_recommended:
        joined = ", ".join(missing_recommended)
        messages.append(f"Note: Template does not reference recommended variables: {joined}.")

    return True, messages


def list_css() -> List[Dict[str, str]]:
    """Return metadata for all built-in CSS presets.

    Returns:
        List[Dict[str, str]]: List of dicts with keys 'name', 'file', and 'description'.
    """
    return [
        {"name": name, "file": meta["file"], "description": meta["description"]}
        for name, meta in BUILTIN_CSS_PRESETS.items()
    ]


def export_css(name: str = "default", output: str = "style.css") -> str:
    """Export a built-in CSS preset ('default', 'github', 'minimal', 'monochrome') to a target file path.

    Args:
        name (str): Name of built-in CSS preset. Defaults to 'default'.
        output (str): Destination file path. Defaults to 'style.css'.

    Returns:
        str: Absolute file path of the exported CSS file.

    Raises:
        ValueError: If CSS preset name is unknown.
        FileNotFoundError: If built-in CSS file is missing.
    """
    if name not in BUILTIN_CSS_PRESETS:
        available = ", ".join(BUILTIN_CSS_PRESETS.keys())
        raise ValueError(f"Unknown CSS preset '{name}'. Available presets: {available}")

    styles_dir = os.path.join(os.path.dirname(__file__), "css")
    filename = BUILTIN_CSS_PRESETS[name]["file"]
    src_path = os.path.join(styles_dir, filename)

    if not os.path.exists(src_path):
        raise FileNotFoundError(f"Built-in CSS file not found at '{src_path}'.")

    dest_abs = os.path.abspath(output)
    os.makedirs(os.path.dirname(dest_abs), exist_ok=True)
    shutil.copy2(src_path, dest_abs)
    return dest_abs
