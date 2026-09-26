# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Development HTTP server for serving rendered drawlib documentation pages."""

import functools
import os
import sys
import threading
import time
import urllib.parse
import webbrowser
from html.parser import HTMLParser
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import List, Optional, Tuple


class _LinkExtractor(HTMLParser):
    """HTML parser to extract local hrefs and srcs."""

    def __init__(self) -> None:
        super().__init__()
        self.links: List[Tuple[str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, Optional[str]]]) -> None:
        attr_dict = {k: v for k, v in attrs if v is not None}
        if tag == "a" and "href" in attr_dict:
            self.links.append((tag, attr_dict["href"]))
        elif tag == "img" and "src" in attr_dict:
            self.links.append((tag, attr_dict["src"]))
        elif tag == "link" and attr_dict.get("rel") == "stylesheet" and "href" in attr_dict:
            self.links.append((tag, attr_dict["href"]))


def scan_broken_links(root_dir: str) -> Tuple[int, int, List[Tuple[str, str, str]]]:
    """Scan all HTML files in root_dir for broken internal links and assets.

    Args:
        root_dir (str): Root directory to scan.

    Returns:
        Tuple[int, int, List[Tuple[str, str, str]]]:
            (total_html_files, total_links_checked, broken_links)
            where broken_links is a list of (html_rel_path, tag, target_url).
    """
    root_path = Path(root_dir).resolve()
    html_files = sorted(root_path.rglob("*.html"))
    total_links = 0
    broken_links: List[Tuple[str, str, str]] = []

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


class _CustomHTTPRequestHandler(SimpleHTTPRequestHandler):
    """Custom request handler that reports referer on 404 error."""

    def send_error(self, code: int, message: Optional[str] = None, explain: Optional[str] = None) -> None:
        if code == 404:
            referer = self.headers.get("Referer", "")
            if referer:
                print(f"[404 NOT FOUND] {self.path} (Referer: {referer})", file=sys.stderr)
        super().send_error(code, message, explain)


def _resolve_serving_directory(directory: Optional[str]) -> str:
    """Resolve and validate serving directory path."""
    if directory is not None:
        target_dir = directory
    elif os.path.isdir("docs/html"):
        target_dir = "docs/html"
    elif os.path.isdir("docs"):
        target_dir = "docs"
    else:
        target_dir = "."

    target_abs = os.path.abspath(target_dir)
    if not os.path.exists(target_abs):
        raise ValueError(f'Serving directory "{target_abs}" does not exist.')
    return target_abs


def _perform_link_check(target_abs: str, skip_check: bool, check_only: bool) -> None:
    """Perform pre-scan link checking and exit if check_only is True."""
    if skip_check:
        if check_only:
            print("Note: --check specified with --skip-check. Exiting.")
            sys.exit(0)
        return

    html_count, link_count, broken = scan_broken_links(target_abs)
    if broken:
        print(f"\n[WARNING] Found {len(broken)} broken link(s) in {target_abs}:", file=sys.stderr)
        for file_path, tag, url in broken:
            print(f"  • {file_path}: <{tag}> '{url}'", file=sys.stderr)
        print("-" * 60, file=sys.stderr)
        if check_only:
            sys.exit(1)
    else:
        print(f"[Link Check] Verified {html_count} HTML file(s) and {link_count} link(s). 0 broken links found.")
        if check_only:
            sys.exit(0)


def run_server(
    directory: Optional[str] = None,
    port: int = 8000,
    open_browser: bool = True,
    skip_check: bool = False,
    check_only: bool = False,
) -> None:
    """Run development HTTP server serving files from the specified directory.

    Args:
        directory (Optional[str]): Root directory to serve files from. Defaults to 'docs/html', 'docs', or '.'.
        port (int): Port number for server. Defaults to 8000.
        open_browser (bool): Whether to open the local browser automatically. Defaults to True.
        skip_check (bool): Whether to skip pre-scan for broken links. Defaults to False.
        check_only (bool): If True, run link scanner and exit without starting HTTP server. Defaults to False.

    Raises:
        ValueError: If specified target directory does not exist.
    """
    target_abs = _resolve_serving_directory(directory)
    _perform_link_check(target_abs=target_abs, skip_check=skip_check, check_only=check_only)

    handler_class = functools.partial(_CustomHTTPRequestHandler, directory=target_abs)
    server_address = ("", port)

    try:
        httpd = ThreadingHTTPServer(server_address, handler_class)
    except OSError as e:
        print(f"Error starting server on port {port}: {e}", file=sys.stderr)
        raise

    url = f"http://localhost:{port}"
    print(f"Serving HTTP on {url} (directory: {target_abs}) ...")
    print("Press Ctrl+C to stop the server.")

    if open_browser:

        def _open_url() -> None:
            time.sleep(0.5)
            webbrowser.open(url)

        threading.Thread(target=_open_url, daemon=True).start()

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping HTTP server...")
    finally:
        httpd.shutdown()
        httpd.server_close()
