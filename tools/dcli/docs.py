# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Documentation generation and local preview toolset."""

from __future__ import annotations

import typer

from tools.dcli.common import console, run_command

app = typer.Typer(
    name="docs",
    help="Build documentation from docs_src and run local preview server.",
    no_args_is_help=True,
)


@app.command("build")
def build() -> None:
    """Build Markdown and HTML documentation from docs_src."""
    run_command(
        ["uv", "run", "python", "tools/scripts/build_docs.py"],
        desc="Building documentation (docs_src -> docs & docs_html)...",
    )
    console.print("[bold green]✓ Documentation built successfully![/bold green]")


@app.command("serve")
def serve(
    port: int = typer.Option(8000, "--port", "-p", help="Port to serve the documentation on."),
    no_browser: bool = typer.Option(False, "--no-browser", help="Do not automatically open the browser."),
) -> None:
    """Serve docs_html locally via drawlib preview server.

    Args:
        port: Port number for the HTTP server.
        no_browser: Whether to prevent opening the default browser.
    """
    cmd = ["uv", "run", "python", "-m", "drawlib", "serve", "docs_html", "-p", str(port)]
    if no_browser:
        cmd.append("--no-browser")
    run_command(cmd, desc=f"Serving documentation on http://localhost:{port}...")


if __name__ == "__main__":
    app()
