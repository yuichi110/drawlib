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

from pathlib import Path

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
    download_only: bool = typer.Option(
        False,
        "--download-only",
        help="Only download original GCP assets without normalizing.",
    ),
    normalize_only: bool = typer.Option(
        False,
        "--normalize-only",
        help="Only normalize existing original GCP assets into release_assets.",
    ),
    src_dir: str = typer.Option(
        "original_assets/gcp",
        "--src-dir",
        help="Source directory for original GCP assets.",
    ),
    dest_dir: str = typer.Option(
        "release_assets/v0.3/icons/gcp",
        "--dest-dir",
        help="Destination directory for normalized flat release assets.",
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
    """Download and normalize Google Cloud architecture diagram icons."""
    should_download = download_only or (not normalize_only and not Path(src_dir).exists())
    should_normalize = normalize_only or not download_only

    if should_download:
        dl_cmd = ["uv", "run", "python", "tools/scripts/download_gcp_icons.py", "--output-dir", src_dir]
        if no_archives:
            dl_cmd.append("--no-archives")
        if no_docs:
            dl_cmd.append("--no-docs")
        run_command(dl_cmd, desc="Downloading official Google Cloud diagram icons...")
        console.print("[bold green]✓ Google Cloud icons downloaded successfully![/bold green]")

    if should_normalize:
        norm_cmd = [
            "uv",
            "run",
            "python",
            "tools/scripts/normalize_gcp_icons.py",
            "--src-dir",
            src_dir,
            "--dest-dir",
            dest_dir,
        ]
        run_command(norm_cmd, desc="Normalizing Google Cloud diagram icons...")
        console.print("[bold green]✓ Google Cloud icons normalized successfully![/bold green]")


if __name__ == "__main__":
    app()
