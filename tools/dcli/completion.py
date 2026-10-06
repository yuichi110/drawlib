# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Dynamic Autocomplete Candidate Generator for dcli."""

from __future__ import annotations

import contextlib
import importlib
import os
from pathlib import Path

import typer

from tools.dcli.common import EXCLUDED_MODULES, discover_toolsets

get_active_toolsets = discover_toolsets


def get_subcommand_candidates(toolset_name: str, prefix: str = "") -> list[str]:
    """Return matching subcommands and groups for a given toolset.

    Args:
        toolset_name: Name of the toolset module.
        prefix: Current partial word prefix to match.

    Returns:
        list[str]: Matching subcommand and group names.
    """
    candidates: list[str] = []
    with contextlib.suppress(Exception):
        mod_name = toolset_name.replace("-", "_")
        mod = importlib.import_module(f"tools.dcli.{mod_name}")
        app_obj = getattr(mod, "app", None)
        if isinstance(app_obj, typer.Typer):
            for cmd in app_obj.registered_commands:
                if cmd.name and cmd.name.startswith(prefix):
                    candidates.append(cmd.name)
            for grp in app_obj.registered_groups:
                if grp.name and grp.name.startswith(prefix):
                    candidates.append(grp.name)
    return sorted(set(candidates))


def get_completion_candidates(words: list[str], cword: int) -> list[str]:
    """Calculate matching candidates based on parsed words and cursor word index.

    Args:
        words: Command line words list.
        cword: 0-based index of the word currently being completed.

    Returns:
        list[str]: Matching completion candidates.
    """
    toolsets = get_active_toolsets()

    # If completing the first argument (the toolset name)
    if cword == 1:
        prefix = words[1] if len(words) > 1 else ""
        return [t for t in toolsets if t.startswith(prefix)]

    # If completing subcommands/options of a specific toolset
    if cword > 1 and len(words) > 1:
        toolset_name = words[1].replace("_", "-")
        if toolset_name in toolsets:
            prefix = words[cword] if cword < len(words) else ""
            return get_subcommand_candidates(toolset_name, prefix)

    return []


def complete() -> None:
    """Generate autocompletion candidates based on COMP_WORDS and COMP_CWORD."""
    comp_words_raw = os.environ.get("COMP_WORDS", "")
    comp_cword_raw = os.environ.get("COMP_CWORD", "0")

    words = comp_words_raw.split()
    try:
        cword = int(comp_cword_raw)
    except ValueError:
        cword = 0

    for candidate in get_completion_candidates(words, cword):
        print(candidate)


if __name__ == "__main__":
    complete()
