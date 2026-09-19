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
import webbrowser
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from typing import Optional


def run_server(
    directory: Optional[str] = None,
    port: int = 8000,
    open_browser: bool = True,
) -> None:
    """Run development HTTP server serving files from the specified directory.

    Args:
        directory (Optional[str]): Root directory to serve files from. Defaults to 'docs/html', 'docs', or '.'.
        port (int): Port number for server. Defaults to 8000.
        open_browser (bool): Whether to open the local browser automatically. Defaults to True.

    Raises:
        ValueError: If specified target directory does not exist.
    """
    if directory is None:
        if os.path.isdir("docs/html"):
            target_dir = "docs/html"
        elif os.path.isdir("docs"):
            target_dir = "docs"
        else:
            target_dir = "."
    else:
        target_dir = directory

    target_abs = os.path.abspath(target_dir)
    if not os.path.exists(target_abs):
        raise ValueError(f'Serving directory "{target_abs}" does not exist.')

    handler_class = functools.partial(SimpleHTTPRequestHandler, directory=target_abs)
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
