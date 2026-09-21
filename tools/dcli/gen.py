# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Code generation toolset (phosphor icons)."""

from __future__ import annotations

import typer

from tools.dcli.common import console, run_command

app = typer.Typer(
    name="gen",
    help="Code generation and asset utilities for icons.",
    no_args_is_help=True,
)


@app.callback()
def callback() -> None:
    """Code generation toolset callback."""


@app.command("icon")
def gen_icon() -> None:
    """Generate Phosphor icon python bindings and code."""
    run_command(
        ["uv", "run", "python", "tools/scripts/generate_icon_phosphor_code.py"],
        desc="Generating Phosphor icon code...",
    )
    console.print("[bold green]✓ Icon code generated successfully![/bold green]")


@app.command("icon-gcp")
def gen_icon_gcp(
    output_dir: str = typer.Option(
        "original_assets/gcp",
        "--output-dir",
        "-o",
        help="Destination directory for original GCP assets.",
    ),
    no_archives: bool = typer.Option(
        False,
        "--no-archives",
        help="Do not keep downloaded raw .zip archives in _archives/.",
    ),
    no_docs: bool = typer.Option(
        False,
        "--no-docs",
        help="Do not download official overview guide PDF.",
    ),
) -> None:
    """Download and extract official Google Cloud architecture diagram icons into original_assets/gcp."""
    cmd = ["uv", "run", "python", "tools/scripts/download_gcp_icons.py", "--output-dir", output_dir]
    if no_archives:
        cmd.append("--no-archives")
    if no_docs:
        cmd.append("--no-docs")
    run_command(cmd, desc="Downloading official Google Cloud diagram icons...")
    console.print("[bold green]✓ Google Cloud icons downloaded successfully![/bold green]")


if __name__ == "__main__":
    app()
