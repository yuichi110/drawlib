# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Development HTTP server for serving rendered drawlib documentation pages."""

from __future__ import annotations

import functools
import os
import socketserver
import sys
import threading
import time
import webbrowser
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

from drawlib._http_server._link_scanner import scan_broken_links


class _CustomHTTPServer(ThreadingHTTPServer):
    """ThreadingHTTPServer that avoids slow reverse DNS lookups in server_bind."""

    allow_reuse_address = True

    def server_bind(self) -> None:
        """Bind socket without calling socket.getfqdn, which can stall on macOS."""
        socketserver.TCPServer.server_bind(self)
        host, port = self.server_address[:2]
        self.server_name = str(host) if host else "localhost"
        self.server_port = int(port)


class _CustomHTTPRequestHandler(SimpleHTTPRequestHandler):
    """Custom request handler that reports referer on 404 error."""

    def send_error(self, code: int, message: str | None = None, explain: str | None = None) -> None:
        if code == 404:
            referer = self.headers.get("Referer", "")
            if referer:
                print(f"[404 NOT FOUND] {self.path} (Referer: {referer})", file=sys.stderr)
        super().send_error(code, message, explain)


def _resolve_serving_directory(directory: str) -> str:
    """Resolve and validate serving directory path.

    Args:
        directory (str): Target directory path.

    Returns:
        str: Absolute path to the validated directory.

    Raises:
        ValueError: If directory does not exist or is not a directory.
    """
    target_abs = os.path.abspath(directory)
    if not os.path.exists(target_abs):
        raise ValueError(f'Serving directory "{target_abs}" does not exist.')
    if not os.path.isdir(target_abs):
        raise ValueError(f'Serving path "{target_abs}" is a file, not a directory.')
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


def serve_docs(
    directory: str,
    port: int = 8000,
    open_browser: bool = True,
    skip_check: bool = False,
    check_only: bool = False,
) -> None:
    """Run development HTTP server serving files from the specified directory.

    Args:
        directory (str): Root directory to serve HTML files from (required).
        port (int): Port number for server. Defaults to 8000.
        open_browser (bool): Whether to open the local browser automatically. Defaults to True.
        skip_check (bool): Whether to skip pre-scan for broken links. Defaults to False.
        check_only (bool): If True, run link scanner and exit without starting HTTP server. Defaults to False.

    Raises:
        ValueError: If specified target directory does not exist or is not a directory.
    """
    target_abs = _resolve_serving_directory(directory)
    _perform_link_check(target_abs=target_abs, skip_check=skip_check, check_only=check_only)

    handler_class = functools.partial(_CustomHTTPRequestHandler, directory=target_abs)
    server_address = ("", port)

    try:
        httpd = _CustomHTTPServer(server_address, handler_class)
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
