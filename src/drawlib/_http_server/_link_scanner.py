# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""HTML link and asset scanner for local documentation validation."""

from __future__ import annotations

import sys
import urllib.parse
from html.parser import HTMLParser
from pathlib import Path


class _LinkExtractor(HTMLParser):
    """HTML parser to extract local hrefs and srcs."""

    def __init__(self) -> None:
        super().__init__()
        self.links: list[tuple[str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr_dict = {k: v for k, v in attrs if v is not None}
        if tag == "a" and "href" in attr_dict:
            self.links.append((tag, attr_dict["href"]))
        elif tag == "img" and "src" in attr_dict:
            self.links.append((tag, attr_dict["src"]))
        elif tag == "link" and attr_dict.get("rel") == "stylesheet" and "href" in attr_dict:
            self.links.append((tag, attr_dict["href"]))


def scan_broken_links(root_dir: str) -> tuple[int, int, list[tuple[str, str, str]]]:
    """Scan all HTML files in root_dir for broken internal links and assets.

    Args:
        root_dir (str): Root directory to scan.

    Returns:
        tuple[int, int, list[tuple[str, str, str]]]:
            (total_html_files, total_links_checked, broken_links)
            where broken_links is a list of (html_rel_path, tag, target_url).
    """
    root_path = Path(root_dir).resolve()
    html_files = sorted(root_path.rglob("*.html"))
    total_links = 0
    broken_links: list[tuple[str, str, str]] = []

    for html_file in html_files:
        try:
            content = html_file.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as e:
            print(f"Warning: Failed to read HTML file '{html_file}': {e}", file=sys.stderr)
            continue

        parser = _LinkExtractor()
        parser.feed(content)

        rel_html_path = str(html_file.relative_to(root_path))
        for tag, url in parser.links:
            trimmed = url.strip()
            if not trimmed or trimmed.startswith(("http://", "https://", "mailto:", "javascript:", "data:", "#")):
                continue
            clean_url = urllib.parse.urldefrag(trimmed)[0].split("?")[0]
            if not clean_url:
                continue

            total_links += 1
            if clean_url.startswith("/"):
                target_path = root_path / clean_url.lstrip("/")
            else:
                target_path = (html_file.parent / clean_url).resolve()

            if not target_path.exists():
                broken_links.append((rel_html_path, tag, trimmed))

    return len(html_files), total_links, broken_links
