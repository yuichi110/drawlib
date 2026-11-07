# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""CLI commands for creating and syncing versioned GitHub Releases."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Optional

import typer
from rich.table import Table

from tools.dcli.common import console, err_console
from tools.dcli.github_release.notes import (
    DEFAULT_RELEASE_NOTES_PATH,
    ReleaseNoteEntry,
    extract_release_note,
    format_github_release_body,
    is_prerelease_version,
    normalize_version_and_tag,
    parse_release_notes,
    resolve_commit_for_version,
)
from tools.dcli.pypi.client import _parse_version, get_new_version
from tools.dcli.release_assets.client import GitHubReleaseClient, resolve_github_token

app = typer.Typer(
    name="github-release",
    help="Create, inspect, and sync versioned GitHub Releases from release_notes.md.",
    no_args_is_help=True,
)


def _require_token(token: str | None, dry_run: bool) -> str | None:
    """Resolve GitHub token and exit with helpful error when missing in non-dry-run mode."""
    resolved = resolve_github_token(token)
    if not dry_run and not resolved:
        err_console.print(
            "[bold red]Error: GitHub token required to publish releases.\n"
            "Pass --token <TOKEN>, or set GITHUB_TOKEN / GH_TOKEN environment variable.[/bold red]"
        )
        raise typer.Exit(code=1)
    return resolved


def _publish_single_entry(
    client: GitHubReleaseClient,
    entry: ReleaseNoteEntry,
    *,
    existing_release: dict[str, Any] | None,
    commit: str | None,
    make_latest: str,
    prerelease: bool,
    update: bool,
    dry_run: bool,
) -> str:
    """Publish or update a single ReleaseNoteEntry and return action label."""
    title = f"v{entry.version}"
    body = format_github_release_body(entry)

    if existing_release is not None and not update:
        console.print(f"  [dim green]↷ Skipped {entry.tag} (already exists on GitHub)[/dim green]")
        return "skipped"

    action_label = "updated" if existing_release is not None else "created"
    if dry_run:
        commit_note = f", target_commitish={commit[:8]}" if commit else ""
        console.print(
            f"  [cyan][DRY-RUN][/cyan] Would {action_label[:-1]} {entry.tag} "
            f"(make_latest={make_latest}, prerelease={prerelease}{commit_note})"
        )
        return action_label

    if existing_release is not None:
        client.update_release(
            existing_release["id"],
            name=title,
            body=body,
            prerelease=prerelease,
            make_latest=make_latest,
        )
        console.print(f"  [bold green]✓[/bold green] Updated GitHub Release [bold]{entry.tag}[/bold]")
        return "updated"

    client.create_release(
        tag=entry.tag,
        name=title,
        body=body,
        draft=False,
        prerelease=prerelease,
        target_commitish=commit,
        make_latest=make_latest,
    )
    console.print(f"  [bold green]✓[/bold green] Created GitHub Release [bold]{entry.tag}[/bold]")
    return "created"


def _filter_entries_by_range(
    entries: list[ReleaseNoteEntry],
    from_ver: str | None,
    to_ver: str | None,
) -> list[ReleaseNoteEntry]:
    """Filter chronologically sorted entries by inclusive [from_ver, to_ver] bounds."""
    filtered = entries
    if from_ver is not None:
        min_v, _ = normalize_version_and_tag(from_ver)
        min_key = _parse_version(min_v)
        filtered = [e for e in filtered if _parse_version(e.version) >= min_key]
    if to_ver is not None:
        max_v, _ = normalize_version_and_tag(to_ver)
        max_key = _parse_version(max_v)
        filtered = [e for e in filtered if _parse_version(e.version) <= max_key]
    return filtered


@app.command("notes")
def show_notes(
    version: Optional[str] = typer.Argument(
        None,
        help="Version or tag (e.g. '0.3.6' or 'v0.3.6'). Defaults to pyproject.toml version.",
    ),
    notes_file: Path = typer.Option(
        DEFAULT_RELEASE_NOTES_PATH,
        "--notes-file",
        help="Path to release_notes.md.",
    ),
) -> None:
    """Preview formatted GitHub Release Markdown extracted from release_notes.md."""
    target = version or get_new_version()
    try:
        entry = extract_release_note(target, notes_path=notes_file)
    except (ValueError, KeyError) as e:
        err_console.print(f"[bold red]Error: {e}[/bold red]")
        raise typer.Exit(code=1) from e

    console.print(f"[bold cyan]# Release {entry.tag}[/bold cyan]\n")
    print(format_github_release_body(entry))


@app.command("list")
def list_github_releases(
    token: Optional[str] = typer.Option(
        None,
        "--token",
        help="GitHub token (optional for public reads, avoids rate limits).",
    ),
    notes_file: Path = typer.Option(
        DEFAULT_RELEASE_NOTES_PATH,
        "--notes-file",
        help="Path to release_notes.md.",
    ),
) -> None:
    """Compare versions in release_notes.md against published GitHub Releases."""
    resolved_token = resolve_github_token(token)
    client = GitHubReleaseClient(token=resolved_token)
    entries = parse_release_notes(notes_file)
    remote_releases = client.list_releases()
    remote_by_tag = {r["tag_name"]: r for r in remote_releases}

    latest_rel = None
    try:
        latest_rel = next((r for r in remote_releases if not r.get("draft") and not r.get("prerelease")), None)
    except Exception:
        latest_rel = None
    latest_tag = latest_rel["tag_name"] if latest_rel else None

    table = Table(title="GitHub Releases Sync Status", show_header=True, header_style="bold blue")
    table.add_column("Tag", style="bold yellow")
    table.add_column("In release_notes.md", justify="center")
    table.add_column("GitHub Status")
    table.add_column("Published At", style="dim")

    for entry in reversed(entries):
        rel = remote_by_tag.get(entry.tag)
        if rel is None:
            table.add_row(entry.tag, "Yes", "[red]Missing on GitHub[/red]", "-")
        else:
            badge = " [bold green](Latest)[/bold green]" if entry.tag == latest_tag else ""
            pub_at = (rel.get("published_at") or "-")[:10]
            table.add_row(entry.tag, "Yes", f"[green]Published[/green]{badge}", pub_at)

    console.print()
    console.print(table)
    console.print()


@app.command("create")
def create_github_release(
    version: Optional[str] = typer.Argument(
        None,
        help="Version or tag to publish (e.g. '0.3.6' or 'v0.3.6'). Defaults to pyproject.toml version.",
    ),
    commit: Optional[str] = typer.Option(
        None,
        "--commit",
        help="Target commit SHA or branch if git tag does not exist yet.",
    ),
    latest: Optional[bool] = typer.Option(
        None,
        "--latest/--no-latest",
        help="Mark as GitHub Latest release (defaults to True for stable, False for pre-releases).",
    ),
    prerelease: Optional[bool] = typer.Option(
        None,
        "--prerelease/--no-prerelease",
        help="Mark as pre-release (auto-detected from dev/rc suffix by default).",
    ),
    update: bool = typer.Option(
        False,
        "--update",
        "-u",
        help="Update release notes if the GitHub Release already exists.",
    ),
    dry_run: bool = typer.Option(
        False,
        "--dry-run",
        help="Preview release creation without calling write APIs.",
    ),
    token: Optional[str] = typer.Option(
        None,
        "--token",
        help="GitHub token with contents:write / repo scope.",
    ),
    notes_file: Path = typer.Option(
        DEFAULT_RELEASE_NOTES_PATH,
        "--notes-file",
        help="Path to release_notes.md.",
    ),
) -> None:
    """Create (or idempotently skip/update) a single GitHub Release from release_notes.md."""
    target = version or get_new_version()
    try:
        entry = extract_release_note(target, notes_path=notes_file)
    except (ValueError, KeyError) as e:
        err_console.print(f"[bold red]Error: {e}[/bold red]")
        raise typer.Exit(code=1) from e

    resolved_token = _require_token(token, dry_run=dry_run)
    client = GitHubReleaseClient(token=resolved_token)

    is_pre = prerelease if prerelease is not None else is_prerelease_version(entry.version)
    is_latest = latest if latest is not None else (not is_pre)
    make_latest_val = "true" if is_latest else "false"
    resolved_commit = commit or resolve_commit_for_version(entry.version)

    existing = client.get_release_by_tag(entry.tag) if (resolved_token or not dry_run) else None
    _publish_single_entry(
        client,
        entry,
        existing_release=existing,
        commit=resolved_commit,
        make_latest=make_latest_val,
        prerelease=is_pre,
        update=update,
        dry_run=dry_run,
    )


@app.command("sync")
def sync_github_releases(
    from_version: Optional[str] = typer.Option(
        None,
        "--from",
        help="Minimum version to include (inclusive, e.g. '0.3.0').",
    ),
    to_version: Optional[str] = typer.Option(
        None,
        "--to",
        help="Maximum version to include (inclusive, e.g. '0.3.6').",
    ),
    update: bool = typer.Option(
        False,
        "--update",
        "-u",
        help="Update existing GitHub Releases in addition to creating missing ones.",
    ),
    dry_run: bool = typer.Option(
        False,
        "--dry-run",
        help="Preview all releases to be created/updated without modifying GitHub.",
    ),
    token: Optional[str] = typer.Option(
        None,
        "--token",
        help="GitHub token with contents:write / repo scope.",
    ),
    notes_file: Path = typer.Option(
        DEFAULT_RELEASE_NOTES_PATH,
        "--notes-file",
        help="Path to release_notes.md.",
    ),
) -> None:
    """Backfill or synchronize multiple GitHub Releases in chronological order."""
    try:
        all_entries = parse_release_notes(notes_file)
        targets = _filter_entries_by_range(all_entries, from_version, to_version)
    except ValueError as e:
        err_console.print(f"[bold red]Error: {e}[/bold red]")
        raise typer.Exit(code=1) from e

    if not targets:
        console.print("[yellow]No matching release entries found in release_notes.md.[/yellow]")
        return

    resolved_token = _require_token(token, dry_run=dry_run)
    client = GitHubReleaseClient(token=resolved_token)
    remote_by_tag = {r["tag_name"]: r for r in client.list_releases()}

    # Highest stable version in all_entries determines which release gets make_latest="true"
    stable_entries = [e for e in all_entries if not is_prerelease_version(e.version)]
    highest_stable_tag = stable_entries[-1].tag if stable_entries else None

    counts = {"created": 0, "updated": 0, "skipped": 0}
    console.print(f"[bold cyan]Synchronizing {len(targets)} release(s) from {notes_file.name}...[/bold cyan]")

    for entry in targets:
        is_pre = is_prerelease_version(entry.version)
        make_latest_val = "true" if entry.tag == highest_stable_tag else "false"
        resolved_commit = resolve_commit_for_version(entry.version)
        action = _publish_single_entry(
            client,
            entry,
            existing_release=remote_by_tag.get(entry.tag),
            commit=resolved_commit,
            make_latest=make_latest_val,
            prerelease=is_pre,
            update=update,
            dry_run=dry_run,
        )
        counts[action] += 1

    console.print(
        f"\n[bold green]★ Sync complete! Created: {counts['created']}, "
        f"Updated: {counts['updated']}, Skipped: {counts['skipped']}[/bold green]"
    )


if __name__ == "__main__":
    app()
