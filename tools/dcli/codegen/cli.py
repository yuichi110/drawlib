# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Code generation toolset (phosphor and GCP icons)."""

from __future__ import annotations

from pathlib import Path

import typer

from tools.dcli.codegen.gcp_codegen import generate_gcp_code
from tools.dcli.codegen.gcp_download import download_and_extract_gcp_icons
from tools.dcli.codegen.gcp_normalize import normalize_all_gcp_icons
from tools.dcli.codegen.map_download import download_original_maps
from tools.dcli.codegen.map_normalize import normalize_all_maps
from tools.dcli.codegen.phosphor import generate_phosphor_code
from tools.dcli.common import PROJECT_ROOT, console

app = typer.Typer(
    name="codegen",
    help="Code generation utilities for icons, maps, and Python bindings.",
    no_args_is_help=True,
)


@app.callback()
def callback() -> None:
    """Code generation toolset callback."""


@app.command("icon-phosphor")
def gen_icon_phosphor() -> None:
    """Generate Phosphor icon python bindings and code."""
    console.print("[bold cyan]Generating Phosphor icon code...[/bold cyan]")
    generate_phosphor_code()
    console.print("[bold green]✓ Phosphor icon code generated successfully![/bold green]")


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
        "tools/original_assets/gcp",
        "--src-dir",
        help="Source directory for original GCP assets.",
    ),
    dest_dir: str = typer.Option(
        "tools/release_assets/v0.3/icons/gcp",
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
    src_path = PROJECT_ROOT / src_dir if not Path(src_dir).is_absolute() else Path(src_dir)
    dest_path = PROJECT_ROOT / dest_dir if not Path(dest_dir).is_absolute() else Path(dest_dir)

    should_download = download_only or (not normalize_only and not src_path.exists())
    should_normalize = normalize_only or not download_only

    if should_download:
        console.print("[bold cyan]Downloading official Google Cloud diagram icons...[/bold cyan]")
        download_and_extract_gcp_icons(
            output_dir=src_path,
            save_archives=not no_archives,
            download_doc=not no_docs,
        )
        console.print("[bold green]✓ Google Cloud icons downloaded successfully![/bold green]")

    if should_normalize:
        console.print("[bold cyan]Normalizing Google Cloud diagram icons...[/bold cyan]")
        normalize_all_gcp_icons(
            src_dir=src_path,
            dest_dir=dest_path,
        )
        console.print("[bold green]✓ Google Cloud icons normalized successfully![/bold green]")

    if not download_only and not normalize_only:
        manifest_file = dest_path / "manifest.json"
        console.print("[bold cyan]Generating Google Cloud icon Python bindings...[/bold cyan]")
        generate_gcp_code(manifest_file=manifest_file)
        console.print("[bold green]✓ Google Cloud icon bindings generated successfully![/bold green]")


@app.command("map")
def gen_map(
    download_only: bool = typer.Option(
        False,
        "--download-only",
        help="Only download raw upstream GeoJSON files into tools/original_assets/maps.",
    ),
    normalize_only: bool = typer.Option(
        False,
        "--normalize-only",
        help="Only normalize existing original GeoJSON files.",
    ),
    src_dir: str = typer.Option(
        "tools/original_assets/maps",
        "--src-dir",
        help="Source directory for raw original GeoJSON files.",
    ),
    dest_dir: str = typer.Option(
        "src/drawlib/_cached_assets/maps",
        "--dest-dir",
        help="Destination directory for normalized GeoJSON map files.",
    ),
) -> None:
    """Download and normalize preset GeoJSON map assets (world, japan, tokyo)."""
    src_path = PROJECT_ROOT / src_dir if not Path(src_dir).is_absolute() else Path(src_dir)
    dest_path = PROJECT_ROOT / dest_dir if not Path(dest_dir).is_absolute() else Path(dest_dir)

    should_download = download_only or (not normalize_only and not (src_path / "manifest.json").exists())
    should_normalize = normalize_only or not download_only

    if should_download:
        console.print("[bold cyan]Downloading raw upstream GeoJSON map assets...[/bold cyan]")
        download_original_maps(output_dir=src_path)
        console.print("[bold green]✓ Raw GeoJSON map assets downloaded successfully![/bold green]")

    if should_normalize:
        console.print("[bold cyan]Normalizing GeoJSON map assets...[/bold cyan]")
        normalize_all_maps(src_dir=src_path, dest_dir=dest_path)
        console.print("[bold green]✓ GeoJSON map assets normalized successfully![/bold green]")


if __name__ == "__main__":
    app()
