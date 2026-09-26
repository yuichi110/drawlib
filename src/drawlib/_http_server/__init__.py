# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""HTTP server package for drawlib documentation preview."""

from drawlib._http_server.server import run_server, scan_broken_links

serve_docs = run_server

__all__ = ["run_server", "scan_broken_links", "serve_docs"]
