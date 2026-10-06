# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Helper script for counting lines of code in the project."""

from __future__ import annotations

import glob
import os
from pathlib import Path

from tools.dcli.common import PROJECT_ROOT, console

SRC_DIR = PROJECT_ROOT / "src" / "drawlib"
TESTS_DIR = PROJECT_ROOT / "tests"


def count_lines_in_file(file_path: str | Path) -> int:
    """Counts the number of lines in a file."""
    with open(file_path, "r", encoding="utf-8") as file:
        return sum(1 for _ in file)


def count_lines_in_directory(directory: str | Path) -> list[tuple[str, int]]:
    """Counts lines in each Python file in the given directory and returns a sorted list."""
    file_lines = []
    dir_str = str(directory)
    for file_path in glob.glob(os.path.join(dir_str, "**", "*.py"), recursive=True):
        lines = count_lines_in_file(file_path)
        rel_path = os.path.relpath(file_path, str(PROJECT_ROOT))
        file_lines.append((rel_path, lines))

    file_lines.sort(key=lambda x: x[1], reverse=True)
    return file_lines


def print_lines_summary(target_path: Path, label: str) -> int:
    """Print line counts for a given directory and return total lines."""
    console.print(f"[bold cyan]==={label}===[/bold cyan]")
    lines_per_file = count_lines_in_directory(target_path)
    if not lines_per_file:
        console.print("No Python files found.")
        return 0

    max_path_length = max(len(file_path) for file_path, _ in lines_per_file)
    for file_path, line_count in lines_per_file:
        console.print(f"{file_path.ljust(max_path_length)} : [yellow]{line_count:>5}[/yellow] lines")

    console.print("----------------------------------------")
    total = sum(count for _, count in lines_per_file)
    console.print(f"Total in {label}: [bold green]{total}[/bold green] lines\n")
    return total


def run_count_lines() -> int:
    """Count lines across src and tests and print summary."""
    t1 = print_lines_summary(SRC_DIR, "src/drawlib")
    t2 = print_lines_summary(TESTS_DIR, "tests")
    grand_total = t1 + t2
    console.print(f"[bold green]Grand Total: {grand_total} lines[/bold green]")
    return grand_total


def main() -> None:
    """Count lines across src and tests."""
    run_count_lines()


if __name__ == "__main__":
    main()
