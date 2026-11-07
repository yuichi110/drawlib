# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Release notes parser and commit resolver for GitHub Releases."""

from __future__ import annotations

import re
import subprocess
from dataclasses import dataclass
from pathlib import Path

from tools.dcli.common import PROJECT_ROOT
from tools.dcli.pypi.client import _parse_version

DEFAULT_RELEASE_NOTES_PATH = PROJECT_ROOT / "docs_src" / "site" / "en" / "01_getting_started" / "release_notes.md"

_VERSION_HEADING_RE = re.compile(r"^##\s+Version\s+([0-9]+\.[0-9]+\.[0-9]+(?:\.[A-Za-z0-9]+)?)\s*$", re.MULTILINE)
_ANY_H2_RE = re.compile(r"^##\s+", re.MULTILINE)
_TRAILING_HR_RE = re.compile(r"(?:\n---\s*)+\Z")


@dataclass(frozen=True)
class ReleaseNoteEntry:
    """Structured release note entry parsed from release_notes.md."""

    version: str
    tag: str
    body: str


def normalize_version_and_tag(version_or_tag: str) -> tuple[str, str]:
    """Normalize a version or tag string into (version, tag).

    Args:
        version_or_tag: Version string like '0.3.6' or tag like 'v0.3.6'.

    Returns:
        tuple[str, str]: Normalized '(version, tag)', e.g. '("0.3.6", "v0.3.6")'.

    Raises:
        ValueError: If the version does not have at least 3 numeric segments.
    """
    cleaned = version_or_tag.strip()
    version = cleaned[1:] if cleaned.startswith("v") else cleaned
    parts = version.split(".")
    if len(parts) < 3 or not all(p.isdigit() for p in parts[:3]):
        raise ValueError(
            f"Invalid release version '{version_or_tag}'. Expected 3-segment version like '0.3.6' or 'v0.3.6'."
        )
    return version, f"v{version}"


def is_prerelease_version(version: str) -> bool:
    """Return True if the version string represents a pre-release (dev or rc)."""
    parts = version.split(".")
    return len(parts) > 3


def parse_release_notes(notes_path: Path = DEFAULT_RELEASE_NOTES_PATH) -> list[ReleaseNoteEntry]:
    """Parse all 3-segment version sections from release_notes.md.

    Args:
        notes_path: Path to the English release_notes.md file.

    Returns:
        list[ReleaseNoteEntry]: Entries sorted chronologically (oldest to newest).
    """
    content = notes_path.read_text(encoding="utf-8")
    matches = list(_VERSION_HEADING_RE.finditer(content))
    entries: list[ReleaseNoteEntry] = []

    for match in matches:
        version = match.group(1)
        section_start = match.end()
        next_h2 = _ANY_H2_RE.search(content, pos=section_start)
        section_end = next_h2.start() if next_h2 else len(content)

        raw_section = content[section_start:section_end].strip()
        cleaned_section = _TRAILING_HR_RE.sub("", raw_section).strip()
        entries.append(
            ReleaseNoteEntry(
                version=version,
                tag=f"v{version}",
                body=cleaned_section,
            )
        )

    entries.sort(key=lambda e: _parse_version(e.version))
    return entries


def extract_release_note(
    version_or_tag: str,
    notes_path: Path = DEFAULT_RELEASE_NOTES_PATH,
) -> ReleaseNoteEntry:
    """Extract a single ReleaseNoteEntry for the requested version or tag.

    Args:
        version_or_tag: Target version ('0.3.6') or tag ('v0.3.6').
        notes_path: Path to release_notes.md.

    Returns:
        ReleaseNoteEntry: Matching parsed entry.

    Raises:
        KeyError: If no matching '## Version X.Y.Z' heading exists in release_notes.md.
    """
    version, _ = normalize_version_and_tag(version_or_tag)
    for entry in parse_release_notes(notes_path):
        if entry.version == version:
            return entry
    raise KeyError(f"Version '{version}' not found in {notes_path}")


def format_github_release_body(entry: ReleaseNoteEntry) -> str:
    """Format extracted release notes with PyPI and bilingual documentation links.

    Args:
        entry: Parsed release note entry.

    Returns:
        str: Formatted GitHub Release Markdown body.
    """
    footer = (
        "\n\n---\n\n"
        f"- **PyPI**: https://pypi.org/project/drawlib/{entry.version}/\n"
        "- **Release Notes (English)**: https://www.drawlib.com/en/01_getting_started/release_notes.html\n"
        "- **リリースノート (日本語)**: https://www.drawlib.com/ja/01_getting_started/release_notes.html"
    )
    return f"{entry.body}{footer}"


def _git_tag_exists(tag: str, cwd: Path = PROJECT_ROOT) -> bool:
    """Return True if the given git tag exists in the local repository."""
    proc = subprocess.run(
        ["git", "rev-parse", "-q", "--verify", f"refs/tags/{tag}"],
        cwd=cwd,
        capture_output=True,
        text=True,
        check=False,
    )
    return proc.returncode == 0


def resolve_commit_for_version(version: str, cwd: Path = PROJECT_ROOT) -> str | None:
    """Resolve the git commit SHA for a version if its tag does not already exist.

    If tag 'v<version>' already exists, returns None so GitHub attaches to the
    existing tag ref. Otherwise searches git history of pyproject.toml for the
    commit that set 'version = "<version>"'.

    Args:
        version: Normalized version string (e.g. '0.3.1').
        cwd: Git repository root.

    Returns:
        str | None: Commit SHA when untagged, or None when already tagged or not found.
    """
    tag = f"v{version}"
    if _git_tag_exists(tag, cwd=cwd):
        return None

    escaped = re.escape(version)
    version_line_re = re.compile(rf'^version\s*=\s*"{escaped}"\s*$', re.MULTILINE)
    proc = subprocess.run(
        ["git", "log", "-G", f'^version\\s*=\\s*"{escaped}"', "--format=%H", "pyproject.toml"],
        cwd=cwd,
        capture_output=True,
        text=True,
        check=False,
    )
    for sha in proc.stdout.splitlines():
        sha = sha.strip()
        if not sha:
            continue
        show_proc = subprocess.run(
            ["git", "show", f"{sha}:pyproject.toml"],
            cwd=cwd,
            capture_output=True,
            text=True,
            check=False,
        )
        if show_proc.returncode == 0 and version_line_re.search(show_proc.stdout):
            return sha
    return None
