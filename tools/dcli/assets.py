# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Release asset management and publishing toolset for GitHub Releases."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Optional

import typer
from rich.panel import Panel
from rich.table import Table

from drawlib import ASSET_VERSION
from drawlib._release_assets import (
    DEFAULT_RELEASE_TAG,
    RELEASE_ASSET_PACKAGES,
    AssetManifest,
    AssetManifestItem,
    ReleaseAssetPackage,
    ReleaseAssetPackageName,
    get_all_release_asset_packages,
)
from tools.dcli.common import console, err_console
from tools.scripts.release_assets_tool import (
    GitHubReleaseClient,
    build_package_zip,
    resolve_github_token,
)

app = typer.Typer(
    name="assets",
    help="Build, verify, upload, and remove font/icon release asset packages on GitHub Releases.",
    no_args_is_help=True,
)


def _resolve_tag(tag: Optional[str]) -> str:
    """Resolve default release tag from ASSET_VERSION or constant."""
    if tag:
        return tag
    # e.g. "v0_3" -> "v0.3"
    if ASSET_VERSION.startswith("v"):
        parts = ASSET_VERSION[1:].split("_")
        return f"v{'.'.join(parts)}"
    return DEFAULT_RELEASE_TAG


def _resolve_assets_dir(tag: str) -> Path:
    """Locate local source directory for release assets."""
    assets_dir = Path("release_assets") / tag
    if not assets_dir.exists():
        err_console.print(f"[bold red]Error: Asset source directory not found: {assets_dir}[/bold red]")
        raise typer.Exit(code=1)
    return assets_dir


def _select_packages(package_name: Optional[ReleaseAssetPackageName]) -> list[ReleaseAssetPackage]:
    """Filter target packages according to command argument."""
    if package_name is not None:
        pkg = RELEASE_ASSET_PACKAGES.get(package_name)
        if pkg is None:
            err_console.print(f"[bold red]Error: Unknown package '{package_name}'.[/bold red]")
            raise typer.Exit(code=1)
        return [pkg]
    return get_all_release_asset_packages()


@app.command("list")
def list_local_packages() -> None:
    """List all 47 locally defined release asset packages, files, and expected hashes."""
    packages = get_all_release_asset_packages()
    table = Table(
        title=f"Defined Release Asset Packages ({len(packages)})",
        title_style="bold green",
        header_style="bold blue",
    )
    table.add_column("EnumStr Name", style="bold yellow")
    table.add_column("Category", style="cyan")
    table.add_column("Archive Name", style="white")
    table.add_column("Files", style="dim")
    table.add_column("SHA-256 Digest", style="green")

    for pkg in packages:
        files_str = f"{len(pkg.files)} files"
        sha_short = f"{pkg.archive_sha256[:12]}...{pkg.archive_sha256[-8:]}"
        table.add_row(pkg.name.value, pkg.category, pkg.archive_name, files_str, sha_short)

    console.print()
    console.print(table)
    console.print()


@app.command("build")
def build_archives(
    package: Optional[ReleaseAssetPackageName] = typer.Argument(
        None,
        help="Optional package name (ReleaseAssetPackageName enum) to build. Omit to build all.",
    ),
    tag: Optional[str] = typer.Option(
        None,
        "--tag",
        "-t",
        help="Release tag version (defaults to auto-resolving 'v0.3').",
    ),
    output_dir: Path = typer.Option(
        Path("dist/release_assets"),
        "--output-dir",
        "-o",
        help="Directory to save generated ZIP files.",
    ),
) -> None:
    """Build deterministic ZIP archives locally without uploading."""
    resolved_tag = _resolve_tag(tag)
    assets_dir = _resolve_assets_dir(resolved_tag)
    targets = _select_packages(package)

    target_out = output_dir / resolved_tag
    target_out.mkdir(parents=True, exist_ok=True)

    console.print(
        f"[bold cyan]Building {len(targets)} asset package(s) into {target_out}...[/bold cyan]"
    )

    for pkg in targets:
        zip_bytes = build_package_zip(pkg, assets_dir)
        dest_file = target_out / pkg.archive_name
        dest_file.write_bytes(zip_bytes)
        size_kb = len(zip_bytes) / 1024
        console.print(f"  [green]✓[/green] Built {pkg.archive_name} ({size_kb:.1f} KB)")

    console.print(f"[bold green]★ Successfully built {len(targets)} archive(s)![/bold green]")


@app.command("remote")
def inspect_remote(
    tag: Optional[str] = typer.Option(
        None,
        "--tag",
        "-t",
        help="Release tag version (defaults to auto-resolving 'v0.3').",
    ),
    token: Optional[str] = typer.Option(
        None,
        "--token",
        help="GitHub token (optional for public read access).",
    ),
) -> None:
    """Inspect GitHub Release assets and compare with local definitions."""
    resolved_tag = _resolve_tag(tag)
    resolved_token = resolve_github_token(token)
    client = GitHubReleaseClient(token=resolved_token)

    console.print(f"[bold cyan]Querying GitHub Release for tag '{resolved_tag}'...[/bold cyan]")
    release = client.get_release_by_tag(resolved_tag)
    if release is None:
        console.print(
            Panel(
                f"[yellow]Release tag '[bold]{resolved_tag}[/bold]' does not exist on GitHub yet.[/yellow]\n"
                f"Run [bold]./dcli assets upload[/bold] to create the release and upload assets.",
                title="Remote Release Status",
                border_style="yellow",
            )
        )
        return

    remote_manifest = client.get_remote_manifest(release)
    remote_assets = {a["name"]: a for a in release.get("assets", [])}

    table = Table(
        title=f"GitHub Release '{resolved_tag}' Assets ({len(remote_assets)} remote)",
        title_style="bold green",
        header_style="bold blue",
    )
    table.add_column("Package Name", style="bold yellow")
    table.add_column("Archive Name", style="white")
    table.add_column("Size", style="dim")
    table.add_column("Sync Status", style="bold")

    packages = get_all_release_asset_packages()
    for pkg in packages:
        asset = remote_assets.get(pkg.archive_name)
        if asset is None:
            table.add_row(pkg.name.value, pkg.archive_name, "-", "[red]Missing on remote[/red]")
        else:
            size_kb = f"{asset.get('size', 0) / 1024:.1f} KB"
            manifest_item = remote_manifest.assets.get(pkg.archive_name) if remote_manifest else None
            if manifest_item and manifest_item.sha256 == pkg.archive_sha256:
                table.add_row(pkg.name.value, pkg.archive_name, size_kb, "[green]Synchronized (hash matches)[/green]")
            elif manifest_item:
                table.add_row(pkg.name.value, pkg.archive_name, size_kb, "[yellow]Hash mismatch[/yellow]")
            else:
                table.add_row(pkg.name.value, pkg.archive_name, size_kb, "[blue]Uploaded (no manifest)[/blue]")

    console.print()
    console.print(table)
    console.print()


@app.command("upload")
def upload_assets(
    package: Optional[ReleaseAssetPackageName] = typer.Argument(
        None,
        help="Optional package name (ReleaseAssetPackageName enum) to upload individually. Omit to upload all 47.",
    ),
    tag: Optional[str] = typer.Option(
        None,
        "--tag",
        "-t",
        help="Release tag version (defaults to auto-resolving 'v0.3').",
    ),
    token: Optional[str] = typer.Option(
        None,
        "--token",
        help="GitHub token with repo scope (or via GITHUB_TOKEN env var).",
    ),
    force: bool = typer.Option(
        False,
        "--force",
        "-f",
        help="Force re-upload even if asset already exists with matching hash.",
    ),
    dry_run: bool = typer.Option(
        False,
        "--dry-run",
        help="Preview actions and hash checks without uploading to GitHub.",
    ),
) -> None:
    """Upload asset ZIP packages to GitHub Releases with duplicate skip logic."""
    resolved_tag = _resolve_tag(tag)
    assets_dir = _resolve_assets_dir(resolved_tag)
    resolved_token = resolve_github_token(token)

    if not dry_run and not resolved_token:
        err_console.print(
            "[bold red]Error: GitHub token required for uploading.\n"
            "Pass --token <TOKEN>, or set GITHUB_TOKEN / GH_TOKEN environment variable, or add to .env file.[/bold red]"
        )
        raise typer.Exit(code=1)

    targets = _select_packages(package)
    client = GitHubReleaseClient(token=resolved_token)

    console.print(f"[bold cyan]Target release: [bold yellow]{resolved_tag}[/bold yellow][/bold cyan]")
    if dry_run:
        console.print("[dim yellow][DRY-RUN MODE] No network upload calls will be executed.[/dim yellow]")

    # Check or create release
    remote_manifest: Optional[AssetManifest] = None
    remote_assets: dict[str, dict[str, Any]] = {}
    release: Optional[dict[str, Any]] = None

    if not dry_run:
        console.print("Resolving remote GitHub release...")
        release = client.get_or_create_release(resolved_tag)
        remote_manifest = client.get_remote_manifest(release)
        remote_assets = {a["name"]: a for a in release.get("assets", [])}
    else:
        # Try read-only fetch during dry-run
        with typer.progressbar(length=1, label="Checking remote release (dry-run)") as bar:
            release = client.get_release_by_tag(resolved_tag)
            if release:
                remote_manifest = client.get_remote_manifest(release)
                remote_assets = {a["name"]: a for a in release.get("assets", [])}
            bar.update(1)

    uploaded_count = 0
    skipped_count = 0

    manifest_map: dict[str, AssetManifestItem] = (
        dict(remote_manifest.assets) if remote_manifest else {}
    )

    for pkg in targets:
        existing_asset = remote_assets.get(pkg.archive_name)
        existing_item = manifest_map.get(pkg.archive_name)

        # Skip check: if file exists and hash matches and not force
        if existing_asset and existing_item and existing_item.sha256 == pkg.archive_sha256 and not force:
            console.print(f"  [dim green]↷ Skipped {pkg.archive_name} (already up-to-date)[/dim green]")
            skipped_count += 1
            continue

        action_desc = "Replacing" if existing_asset else "Uploading"
        action_verb = "replace" if existing_asset else "upload"
        zip_bytes = build_package_zip(pkg, assets_dir)
        size_kb = len(zip_bytes) / 1024

        if dry_run:
            msg = (
                f"  [cyan][DRY-RUN][/cyan] Would {action_verb} {pkg.archive_name} "
                f"({size_kb:.1f} KB, SHA: {pkg.archive_sha256[:8]}...)"
            )
            console.print(msg)
            uploaded_count += 1
            continue

        assert release is not None

        # If asset already exists, delete old one before uploading replacement
        if existing_asset:
            client.delete_asset(existing_asset["id"])

        upload_res = client.upload_asset(release["id"], pkg.archive_name, zip_bytes)
        manifest_map[pkg.archive_name] = AssetManifestItem(
            archive_name=pkg.archive_name,
            sha256=pkg.archive_sha256,
            size=upload_res.get("size", len(zip_bytes)),
        )
        console.print(f"  [bold green]✓[/bold green] {action_desc} {pkg.archive_name} ({size_kb:.1f} KB)")
        uploaded_count += 1

    # Upload updated manifest if any files were uploaded and not dry-run
    if not dry_run and release is not None and uploaded_count > 0:
        console.print("Synchronizing remote asset_manifest.json...")
        new_manifest = AssetManifest(version=resolved_tag, assets=manifest_map)
        client.upload_manifest(release, new_manifest)
        console.print("  [bold green]✓[/bold green] Updated asset_manifest.json on GitHub Release")

    console.print()
    console.print(
        f"[bold green]★ Complete! Uploaded: {uploaded_count}, Skipped: {skipped_count}[/bold green]"
    )


def _determine_removal_targets(
    package: Optional[ReleaseAssetPackageName],
    all_assets: bool,
    remote_assets: dict[str, Any],
    resolved_tag: str,
) -> list[str]:
    """Identify which remote archive assets to delete."""
    if all_assets:
        return [name for name in remote_assets if name != "asset_manifest.json"]

    assert package is not None
    pkg = RELEASE_ASSET_PACKAGES[package]
    if pkg.archive_name not in remote_assets:
        console.print(
            f"[yellow]Asset '{pkg.archive_name}' does not exist on remote release '{resolved_tag}'.[/yellow]"
        )
        return []
    return [pkg.archive_name]


def _confirm_deletion(targets: list[str], resolved_tag: str, yes: bool) -> None:
    """Prompt user for confirmation before deleting remote assets."""
    if yes:
        return
    prompt_msg = f"Are you sure you want to delete {len(targets)} asset(s) from release '{resolved_tag}'?"
    if not typer.confirm(prompt_msg):
        console.print("[yellow]Deletion cancelled.[/yellow]")
        raise typer.Abort()


@app.command("remove")
def remove_assets(
    package: Optional[ReleaseAssetPackageName] = typer.Argument(
        None,
        help="Specific package name (ReleaseAssetPackageName enum) to remove from GitHub Release.",
    ),
    all_assets: bool = typer.Option(
        False,
        "--all",
        help="Remove ALL asset packages from the GitHub Release.",
    ),
    tag: Optional[str] = typer.Option(
        None,
        "--tag",
        "-t",
        help="Release tag version (defaults to auto-resolving 'v0.3').",
    ),
    token: Optional[str] = typer.Option(
        None,
        "--token",
        help="GitHub token with repo scope (or via GITHUB_TOKEN env var).",
    ),
    yes: bool = typer.Option(
        False,
        "--yes",
        "-y",
        help="Confirm deletion without interactive prompt.",
    ),
    dry_run: bool = typer.Option(
        False,
        "--dry-run",
        help="Preview deletion actions without modifying GitHub Release.",
    ),
) -> None:
    """Remove one or all release asset packages from a GitHub Release."""
    if package is None and not all_assets:
        err_console.print(
            "[bold red]Error: Specify a package name to remove, or pass --all to remove all release assets.[/bold red]"
        )
        raise typer.Exit(code=1)

    resolved_tag = _resolve_tag(tag)
    resolved_token = resolve_github_token(token)

    if not dry_run and not resolved_token:
        err_console.print(
            "[bold red]Error: GitHub token required for removing assets.\n"
            "Pass --token <TOKEN>, or set GITHUB_TOKEN / GH_TOKEN environment variable.[/bold red]"
        )
        raise typer.Exit(code=1)

    client = GitHubReleaseClient(token=resolved_token)
    release = client.get_release_by_tag(resolved_tag)
    if release is None:
        if dry_run:
            console.print(
                f"[cyan][DRY-RUN][/cyan] Release tag '{resolved_tag}' does not exist on GitHub. Nothing to remove."
            )
            return
        err_console.print(f"[bold red]Error: Release tag '{resolved_tag}' not found on GitHub.[/bold red]")
        raise typer.Exit(code=1)

    remote_assets = {a["name"]: a for a in release.get("assets", [])}
    remote_manifest = client.get_remote_manifest(release)

    targets = _determine_removal_targets(package, all_assets, remote_assets, resolved_tag)
    if not targets:
        console.print("[yellow]No matching remote assets found to remove.[/yellow]")
        return

    console.print(f"[bold red]Target assets to remove from '{resolved_tag}':[/bold red]")
    for t in targets:
        console.print(f"  • {t}")

    if dry_run:
        console.print(f"[cyan][DRY-RUN][/cyan] Would remove {len(targets)} asset(s). No changes made.")
        return

    _confirm_deletion(targets, resolved_tag, yes)

    for filename in targets:
        asset_info = remote_assets[filename]
        client.delete_asset(asset_info["id"])
        console.print(f"  [bold red]✗[/bold red] Deleted {filename}")

    if remote_manifest:
        new_assets = {k: v for k, v in remote_manifest.assets.items() if k not in targets}
        client.upload_manifest(release, AssetManifest(version=resolved_tag, assets=new_assets))
        console.print("  [bold green]✓[/bold green] Updated remote asset_manifest.json")

    console.print(f"[bold green]★ Successfully removed {len(targets)} asset(s)![/bold green]")


if __name__ == "__main__":
    app()
