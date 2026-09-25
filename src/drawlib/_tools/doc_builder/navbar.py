# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Parser and validator for navbar.md in drawlib doc_builder."""

from __future__ import annotations

import dataclasses
import os
import re
from typing import Any, Dict, List, Optional, Tuple


@dataclasses.dataclass
class NavbarItem:
    """Represents a single navigation link in navbar.md.

    Attributes:
        title (str): Display title of the link.
        url (str): Raw target URL or relative path from navbar.md.
        target_file_abs (Optional[str]): Absolute file path if local file, None if external.
        is_external (bool): True if URL is external (http://, https://, //).
        anchor (str): Anchor fragment if any (e.g. 'section-1').
    """

    title: str
    url: str
    target_file_abs: Optional[str] = None
    is_external: bool = False
    anchor: str = ""


@dataclasses.dataclass
class NavbarSection:
    """Represents a category / group of navigation items under a heading.

    Attributes:
        title (Optional[str]): Category heading text, or None for top-level items.
        items (List[NavbarItem]): List of navigation items in this section.
    """

    title: Optional[str]
    items: List[NavbarItem] = dataclasses.field(default_factory=list)


_LINK_PATTERN = re.compile(r"^\s*[-*+]\s+\[(.*?)\]\(\s*([^\s)]+)(?:\s+[\"'].*?[\"'])?\s*\)\s*$")


def parse_navbar_markdown(navbar_path: str, root_dir: str) -> Tuple[List[NavbarSection], Optional[str]]:
    """Parse and validate navbar.md against files in root_dir.

    Args:
        navbar_path (str): Path to navbar.md file.
        root_dir (str): Root directory of the documentation project.

    Returns:
        Tuple[List[NavbarSection], Optional[str]]: (sections, site_title)
            - sections: Parsed sections containing validated items.
            - site_title: First H1 heading text if found in navbar.md (e.g. site brand name), else None.

    Raises:
        ValueError: If navbar.md cannot be read, contains invalid links, or has no links.
    """
    navbar_abs = os.path.abspath(navbar_path)
    root_dir_abs = os.path.abspath(root_dir)

    if not os.path.isfile(navbar_abs):
        raise ValueError(f"Navbar file '{navbar_abs}' does not exist.")

    try:
        with open(navbar_abs, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except Exception as e:
        raise ValueError(f"Failed to read navbar file '{navbar_abs}': {e}") from e

    sections: List[NavbarSection] = []
    current_section: Optional[NavbarSection] = None
    first_heading_seen = False
    site_title: Optional[str] = None

    for line_no, raw_line in enumerate(lines, start=1):
        line = raw_line.strip()
        if not line or line.startswith("<!--"):
            continue

        if line.startswith("#"):
            heading_level = len(line) - len(line.lstrip("#"))
            heading_text = line.lstrip("#").strip()

            if heading_level == 1 and not first_heading_seen:
                first_heading_seen = True
                site_title = heading_text
                continue

            first_heading_seen = True
            current_section = NavbarSection(title=heading_text)
            sections.append(current_section)
            continue

        match = _LINK_PATTERN.match(raw_line)
        if match:
            title = match.group(1).strip()
            raw_url = match.group(2).strip()

            if raw_url.startswith(("http://", "https://", "//")):
                item = NavbarItem(title=title, url=raw_url, is_external=True)
            else:
                clean_path = raw_url.split("?")[0]
                anchor = ""
                if "#" in clean_path:
                    clean_path, anchor = clean_path.split("#", 1)
                clean_path = clean_path.strip()

                if not clean_path:
                    item = NavbarItem(title=title, url=raw_url, anchor=anchor, is_external=False)
                else:
                    target_abs = os.path.abspath(os.path.join(root_dir_abs, clean_path))
                    if not os.path.isfile(target_abs):
                        raise ValueError(
                            f"Navbar error in '{navbar_path}' (line {line_no}): "
                            f"Target file '{raw_url}' does not exist (resolved to '{target_abs}')."
                        )
                    item = NavbarItem(
                        title=title,
                        url=raw_url,
                        target_file_abs=target_abs,
                        is_external=False,
                        anchor=anchor,
                    )

            if current_section is None:
                current_section = NavbarSection(title=None)
                sections.append(current_section)

            current_section.items.append(item)

    non_empty_sections = [s for s in sections if len(s.items) > 0]
    total_items = sum(len(s.items) for s in non_empty_sections)
    if total_items == 0:
        raise ValueError(f"Navbar error in '{navbar_path}': No navigation links found.")

    return non_empty_sections, site_title


def resolve_navbar_for_page(
    sections: List[NavbarSection],
    root_dir_abs: str,
    out_dir_abs: str,
    current_src_abs: str,
    current_dest_abs: str,
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """Resolve navbar links and active states relative to a specific destination HTML page.

    Args:
        sections (List[NavbarSection]): Parsed navbar sections.
        root_dir_abs (str): Absolute path to the source root directory.
        out_dir_abs (str): Absolute path to the output destination root directory.
        current_src_abs (str): Absolute path to the current source Markdown/HTML file.
        current_dest_abs (str): Absolute path to the current destination HTML file.

    Returns:
        Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]: (nav_sections, nav_items)
            - nav_sections: List of section dicts with 'title' and 'items'.
            - nav_items: Flat list of all items for backwards compatibility.
    """
    current_dest_dir = os.path.dirname(current_dest_abs)
    nav_sections: List[Dict[str, Any]] = []
    nav_items: List[Dict[str, Any]] = []

    for section in sections:
        resolved_items: List[Dict[str, Any]] = []
        for item in section.items:
            if item.is_external:
                url = item.url
                active = False
            elif item.target_file_abs is None:
                url = f"#{item.anchor}" if item.anchor else "#"
                active = False
            else:
                rel_from_root = os.path.relpath(item.target_file_abs, root_dir_abs)
                rel_base, _ = os.path.splitext(rel_from_root)
                item_dest_abs = os.path.join(out_dir_abs, rel_base + ".html")
                rel_url = os.path.relpath(item_dest_abs, current_dest_dir).replace(os.sep, "/")
                if item.anchor:
                    rel_url = f"{rel_url}#{item.anchor}"
                url = rel_url
                active = os.path.abspath(item.target_file_abs) == os.path.abspath(current_src_abs)

            item_dict: Dict[str, Any] = {
                "title": item.title,
                "url": url,
                "active": active,
                "is_external": item.is_external,
            }
            resolved_items.append(item_dict)
            nav_items.append(item_dict)

        nav_sections.append({
            "title": section.title,
            "items": resolved_items,
        })

    return nav_sections, nav_items
