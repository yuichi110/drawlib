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

from pathlib import Path
from typing import Optional

import typer

from tools.dcli.common import PROJECT_ROOT, console, err_console, run_command
from tools.dcli.docs.builder import build_docs

app = typer.Typer(
    name="docs",
    help="Build documentation from sources and run local preview server.",
    no_args_is_help=True,
)


@app.callback()
def callback() -> None:
    """Docs toolset callback."""


@app.command("build")
def build(
    target: Optional[str] = typer.Argument(
        None,
        help="Target to build ('site', 'quickstart', 'readme', 'dogfooding', 'dogfooding-en', 'slide', or 'all'). Default: 'site'.",
    ),
    all_targets: bool = typer.Option(
        False,
        "--all",
        "-a",
        help="Build all documentation targets (equivalent to docs_build.sh).",
    ),
    clean: bool = typer.Option(
        True,
        "--clean/--no-clean",
        help="Remove build artifacts before compilation.",
    ),
) -> None:
    """Build documentation, presentations, and illustration assets."""
    try:
        build_docs(target_name=target, build_all=all_targets, clean=clean)
    except Exception as e:
        err_console.print(f"[bold red]{e}[/bold red]")
        raise typer.Exit(code=1) from e


SERVE_TARGET_MAP: dict[str, str] = {
    "site": "docs_html",
    "docs": "docs_html",
    "docs_html": "docs_html",
    "dogfooding": "drawlib-dogfooding_html",
    "dogfooding-en": "drawlib-dogfooding-en_html",
    "quickstart": "quickstart_html",
    "slide": "slide_about_drawlib_html",
    "slide_about_drawlib": "slide_about_drawlib_html",
    "slide-about-drawlib": "slide_about_drawlib_html",
}


@app.command("serve")
def serve(
    target: str = typer.Argument(
        "site",
        help="Directory or target alias to serve ('site', 'dogfooding', 'dogfooding-en', 'quickstart', 'slide', or path).",
    ),
    port: int = typer.Option(8000, "--port", "-p", help="Port to serve the documentation on."),
    no_browser: bool = typer.Option(False, "--no-browser", help="Do not automatically open the browser."),
    skip_check: bool = typer.Option(False, "--skip-check", help="Skip pre-scan for broken links."),
    check: bool = typer.Option(False, "--check", help="Check for broken links and exit without starting server."),
) -> None:
    """Serve documentation or slides locally via drawlib preview server.

    Args:
        target: Documentation target alias or directory to serve.
        port: Port number for the HTTP server.
        no_browser: Whether to prevent opening the default browser.
        skip_check: Whether to skip pre-scan for broken links.
        check: Whether to check for broken links and exit.
    """
    serve_dir = SERVE_TARGET_MAP.get(target, target)
    target_path = PROJECT_ROOT / serve_dir if not Path(serve_dir).is_absolute() else Path(serve_dir)

    if not target_path.exists():
        err_console.print(
            f"[bold red]Serve target directory '{serve_dir}' does not exist.[/bold red]\n"
            f"Please run [bold]./dcli docs build {target}[/bold] first."
        )
        raise typer.Exit(code=1)

    cmd = ["uv", "run", "python", "-m", "drawlib", "serve", str(target_path), "-p", str(port)]
    if no_browser:
        cmd.append("--no-browser")
    if skip_check:
        cmd.append("--skip-check")
    if check:
        cmd.append("--check")
    run_command(cmd, desc=f"Serving {serve_dir} on http://localhost:{port}...")


if __name__ == "__main__":
    app()
