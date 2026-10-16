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
from tools.dcli.codegen.icons_build import write_provider_manifest
from tools.dcli.codegen.map_codegen import generate_map_code
from tools.dcli.codegen.map_download import download_original_maps
from tools.dcli.codegen.map_normalize import normalize_all_maps
from tools.dcli.codegen.original_cloud_codegen import (
    generate_original_cloud_code,
    generate_original_provider_code,
)
from tools.dcli.codegen.phosphor import generate_phosphor_code
from tools.dcli.common import PROJECT_ROOT, console, run_command

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


@app.command("icon-original-cloud")
def gen_icon_original_cloud(
    build_images: bool = typer.Option(
        False,
        "--build-images",
        help="Re-render icon PNGs via tools/icons_src/build.sh before generating bindings.",
    ),
    src_dir: str = typer.Option(
        "tools/icons_src/original_cloud",
        "--src-dir",
        help="Source directory for native Drawlib Original Cloud icon scripts.",
    ),
    dest_dir: str = typer.Option(
        "tools/release_assets/v0.3/icons/original_cloud",
        "--dest-dir",
        help="Destination directory for normalized 512x512 release assets.",
    ),
) -> None:
    """Normalize native Drawlib Original Cloud icons and generate Python bindings."""
    src_path = PROJECT_ROOT / src_dir if not Path(src_dir).is_absolute() else Path(src_dir)
    dest_path = PROJECT_ROOT / dest_dir if not Path(dest_dir).is_absolute() else Path(dest_dir)

    if build_images:
        console.print("[bold cyan]Building native Drawlib icon scripts in tools/icons_src/...[/bold cyan]")
        run_command(["bash", str(PROJECT_ROOT / "tools/icons_src/build.sh")])

    console.print("[bold cyan]Updating Original Cloud icon manifest...[/bold cyan]")
    manifest_file = write_provider_manifest("original_cloud", src_path, dest_path)
    console.print(f"[bold green]✓ Manifest written to {manifest_file}[/bold green]")

    console.print("[bold cyan]Generating Original Cloud icon Python bindings...[/bold cyan]")
    generate_original_cloud_code(manifest_file=manifest_file)
    console.print("[bold green]✓ Original Cloud icon bindings generated successfully![/bold green]")


@app.command("icon-original-devops")
def gen_icon_original_devops() -> None:
    """Normalize native Drawlib Original DevOps icons and generate Python bindings."""
    src_path = PROJECT_ROOT / "tools/icons_src/original_devops"
    dest_path = PROJECT_ROOT / "tools/release_assets/v0.3/icons/original_devops"
    manifest_file = write_provider_manifest("original_devops", src_path, dest_path)
    generate_original_provider_code("original_devops", manifest_file=manifest_file)
    console.print("[bold green]✓ Original DevOps icon bindings generated successfully![/bold green]")


@app.command("icon-original-ai")
def gen_icon_original_ai() -> None:
    """Normalize native Drawlib Original AI icons and generate Python bindings."""
    src_path = PROJECT_ROOT / "tools/icons_src/original_ai"
    dest_path = PROJECT_ROOT / "tools/release_assets/v0.3/icons/original_ai"
    manifest_file = write_provider_manifest("original_ai", src_path, dest_path)
    generate_original_provider_code("original_ai", manifest_file=manifest_file)
    console.print("[bold green]✓ Original AI icon bindings generated successfully![/bold green]")


@app.command("icon-original-network")
def gen_icon_original_network() -> None:
    """Normalize native Drawlib Original Network icons and generate Python bindings."""
    src_path = PROJECT_ROOT / "tools/icons_src/original_network"
    dest_path = PROJECT_ROOT / "tools/release_assets/v0.3/icons/original_network"
    manifest_file = write_provider_manifest("original_network", src_path, dest_path)
    generate_original_provider_code("original_network", manifest_file=manifest_file)
    console.print("[bold green]✓ Original Network icon bindings generated successfully![/bold green]")


@app.command("icon-original-server")
def gen_icon_original_server() -> None:
    """Normalize native Drawlib Original Server icons and generate Python bindings."""
    src_path = PROJECT_ROOT / "tools/icons_src/original_server"
    dest_path = PROJECT_ROOT / "tools/release_assets/v0.3/icons/original_server"
    manifest_file = write_provider_manifest("original_server", src_path, dest_path)
    generate_original_provider_code("original_server", manifest_file=manifest_file)
    console.print("[bold green]✓ Original Server icon bindings generated successfully![/bold green]")


@app.command("icon-aws")
def gen_icon_aws() -> None:
    """Normalize native Drawlib AWS icons and generate Python bindings."""
    src_path = PROJECT_ROOT / "tools/icons_src/aws"
    dest_path = PROJECT_ROOT / "tools/release_assets/v0.3/icons/aws"
    manifest_file = write_provider_manifest("aws", src_path, dest_path)
    generate_original_provider_code("aws", manifest_file=manifest_file)
    console.print("[bold green]✓ AWS icon bindings generated successfully![/bold green]")


@app.command("icon-azure")
def gen_icon_azure() -> None:
    """Normalize native Drawlib Azure icons and generate Python bindings."""
    src_path = PROJECT_ROOT / "tools/icons_src/azure"
    dest_path = PROJECT_ROOT / "tools/release_assets/v0.3/icons/azure"
    manifest_file = write_provider_manifest("azure", src_path, dest_path)
    generate_original_provider_code("azure", manifest_file=manifest_file)
    console.print("[bold green]✓ Azure icon bindings generated successfully![/bold green]")


@app.command("icon-network")
def gen_icon_network() -> None:
    """Normalize native Drawlib Network icons and generate Python bindings."""
    src_path = PROJECT_ROOT / "tools/icons_src/network"
    dest_path = PROJECT_ROOT / "tools/release_assets/v0.3/icons/network"
    manifest_file = write_provider_manifest("network", src_path, dest_path)
    generate_original_provider_code("network", manifest_file=manifest_file)
    console.print("[bold green]✓ Network icon bindings generated successfully![/bold green]")


@app.command("icon-server")
def gen_icon_server() -> None:
    """Normalize native Drawlib Server icons and generate Python bindings."""
    src_path = PROJECT_ROOT / "tools/icons_src/server"
    dest_path = PROJECT_ROOT / "tools/release_assets/v0.3/icons/server"
    manifest_file = write_provider_manifest("server", src_path, dest_path)
    generate_original_provider_code("server", manifest_file=manifest_file)
    console.print("[bold green]✓ Server icon bindings generated successfully![/bold green]")


@app.command("icon-cnative")
def gen_icon_cnative() -> None:
    """Normalize native Drawlib Cloud Native icons and generate Python bindings."""
    src_path = PROJECT_ROOT / "tools/icons_src/cnative"
    dest_path = PROJECT_ROOT / "tools/release_assets/v0.3/icons/cnative"
    manifest_file = write_provider_manifest("cnative", src_path, dest_path)
    generate_original_provider_code("cnative", manifest_file=manifest_file)
    console.print("[bold green]✓ Cloud Native icon bindings generated successfully![/bold green]")


@app.command("icon-gcp")
def gen_icon_gcp(
    build_images: bool = typer.Option(
        False,
        "--build-images",
        help="Re-render icon PNGs via tools/icons_src/build.sh before generating bindings.",
    ),
    src_dir: str = typer.Option(
        "tools/icons_src/gcp",
        "--src-dir",
        help="Source directory for native Drawlib GCP icon scripts.",
    ),
    dest_dir: str = typer.Option(
        "tools/release_assets/v0.3/icons/gcp",
        "--dest-dir",
        help="Destination directory for normalized 512x512 release assets.",
    ),
) -> None:
    """Normalize native Drawlib Google Cloud icons and generate Python bindings."""
    src_path = PROJECT_ROOT / src_dir if not Path(src_dir).is_absolute() else Path(src_dir)
    dest_path = PROJECT_ROOT / dest_dir if not Path(dest_dir).is_absolute() else Path(dest_dir)

    if build_images:
        console.print("[bold cyan]Building native Drawlib icon scripts in tools/icons_src/...[/bold cyan]")
        run_command(["bash", str(PROJECT_ROOT / "tools/icons_src/build.sh")])

    console.print("[bold cyan]Updating Google Cloud icon manifest...[/bold cyan]")
    manifest_file = write_provider_manifest("gcp", src_path, dest_path)
    console.print(f"[bold green]✓ Manifest written to {manifest_file}[/bold green]")

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
        "tools/release_assets/v0.3/maps",
        "--dest-dir",
        help="Destination directory for normalized release asset GeoJSON map files.",
    ),
) -> None:
    """Download, normalize, and generate bindings for preset GeoJSON map assets."""
    src_path = PROJECT_ROOT / src_dir if not Path(src_dir).is_absolute() else Path(src_dir)
    dest_path = PROJECT_ROOT / dest_dir if not Path(dest_dir).is_absolute() else Path(dest_dir)
    cache_path = PROJECT_ROOT / "src/drawlib/_cached_assets/maps"

    should_download = download_only or (not normalize_only and not (src_path / "manifest.json").exists())
    should_normalize = normalize_only or not download_only

    if should_download:
        console.print("[bold cyan]Downloading raw upstream GeoJSON map assets...[/bold cyan]")
        download_original_maps(output_dir=src_path)
        console.print("[bold green]✓ Raw GeoJSON map assets downloaded successfully![/bold green]")

    if should_normalize:
        console.print("[bold cyan]Normalizing GeoJSON map assets...[/bold cyan]")
        normalize_all_maps(src_dir=src_path, dest_dir=dest_path, cache_dir=cache_path)
        console.print("[bold green]✓ GeoJSON map assets normalized successfully![/bold green]")

    if not download_only:
        manifest_file = dest_path / "manifest.json"
        console.print("[bold cyan]Generating GeoMap preset Python bindings...[/bold cyan]")
        generate_map_code(manifest_file=manifest_file)
        console.print("[bold green]✓ GeoMap preset Python bindings generated successfully![/bold green]")


if __name__ == "__main__":
    app()
