# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Template export and validation utilities for drawlib doc_builder."""

import os
import shutil
from typing import List, Tuple

import jinja2
import jinja2.meta


def export_default_template(output_path: str = "template.html.j2", template_name: str = "sidebar") -> str:
    """Export built-in HTML template (sidebar or simple) to target file path.

    Args:
        output_path (str): File path to save the exported template. Defaults to 'template.html.j2'.
        template_name (str): Name of built-in template to export ('sidebar', 'simple').
            Defaults to 'sidebar'.

    Returns:
        str: Absolute file path of the exported template.

    Raises:
        FileNotFoundError: If built-in template file is missing.
    """
    templates_dir = os.path.join(os.path.dirname(__file__), "html_templates")
    filename = "simple.html.j2" if template_name in {"simple", "standalone"} else "sidebar.html.j2"
    default_template_path = os.path.join(templates_dir, filename)

    if not os.path.exists(default_template_path):
        raise FileNotFoundError(f"Built-in template not found at '{default_template_path}'.")

    dest_abs = os.path.abspath(output_path)
    os.makedirs(os.path.dirname(dest_abs), exist_ok=True)
    shutil.copy2(default_template_path, dest_abs)
    return dest_abs


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
