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

EXCLUDED_MODULES = frozenset({"__init__.py", "__main__.py", "common.py", "completion.py"})


def get_active_toolsets() -> list[str]:
    """Scan the dcli directory to discover available executable CLI modules.

    Returns:
        list[str]: Sorted list of active CLI toolset names.
    """
    dcli_dir = Path(__file__).resolve().parent
    toolsets = []
    for f in dcli_dir.glob("*.py"):
        if f.name not in EXCLUDED_MODULES and not f.name.startswith("_"):
            toolsets.append(f.stem)
    return sorted(toolsets)


def _suggest_subcommands(toolset_name: str, prefix: str) -> None:
    """Print matching subcommands and groups for a given toolset.

    Args:
        toolset_name: Name of the toolset module.
        prefix: Current partial word prefix to match.
    """
    with contextlib.suppress(Exception):
        mod = importlib.import_module(f"tools.dcli.{toolset_name}")
        app_obj = getattr(mod, "app", None)
        if isinstance(app_obj, typer.Typer):
            for cmd in app_obj.registered_commands:
                if cmd.name and cmd.name.startswith(prefix):
                    print(cmd.name)
            for grp in app_obj.registered_groups:
                if grp.name and grp.name.startswith(prefix):
                    print(grp.name)


def complete() -> None:
    """Generate autocompletion candidates based on COMP_WORDS and COMP_CWORD."""
    comp_words_raw = os.environ.get("COMP_WORDS", "")
    comp_cword_raw = os.environ.get("COMP_CWORD", "0")

    words = comp_words_raw.split()
    try:
        cword = int(comp_cword_raw)
    except ValueError:
        cword = 0

    toolsets = get_active_toolsets()

    # If completing the first argument (the toolset name)
    if cword == 1:
        prefix = words[1] if len(words) > 1 else ""
        for t in toolsets:
            if t.startswith(prefix):
                print(t)
        return

    # If completing subcommands/options of a specific toolset
    if cword > 1 and len(words) > 1:
        toolset_name = words[1]
        if toolset_name in toolsets:
            prefix = words[cword] if cword < len(words) else ""
            _suggest_subcommands(toolset_name, prefix)


if __name__ == "__main__":
    complete()
