# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Check if internal type aliases appear in @guarded function docstrings."""

import ast
import os
import re
import sys
from typing import Optional, Union

TYPES_TO_CHECK = [
    "StaticContainer",
    "TypeAlpha",
    "TypeAngle",
    "TypeAngle90",
    "TypeBend",
    "TypePosFloat",
    "TypePosInt",
    "TypeNumVertex",
    "TypeFloat",
    "TypeInt",
    "TypeStr",
    "TypeBool",
    "TypeCoordinate",
    "TypeCoordinates",
    "TypeBezier2",
    "TypeBezier3",
    "TypeColor",
    "TypeColorRGB",
    "TypeColorRGBA",
    "TypePathPoint",
    "TypePathPoints",
    "TypeIconStyle",
    "TypeHAlign",
    "TypeVAlign",
    "TypeLineStyle",
    "TypeArrowHead",
    "TypeImageFormat",
    "TypeImageZoom",
    "TypeImageQuality",
    "TypeImageResample",
    "TypeTailEdge",
    "TypeSize",
    "TypeFont",
    "FontBase",
]


def _get_docstring_text(node: Union[ast.FunctionDef, ast.AsyncFunctionDef]) -> Optional[str]:
    """Extract docstring text from a function node body's first statement."""
    if not node.body:
        return None

    first_stmt = node.body[0]
    if not isinstance(first_stmt, ast.Expr):
        return None

    val = first_stmt.value
    if isinstance(val, ast.Constant) and isinstance(val.value, str):
        return val.value
    if isinstance(val, ast.Str):  # type: ignore
        return val.s  # type: ignore
    return None


def _has_guarded_decorator(node: Union[ast.FunctionDef, ast.AsyncFunctionDef]) -> bool:
    """Check if a function has the @guarded decorator."""
    return any(
        (isinstance(dec, ast.Name) and dec.id == "guarded")
        or (isinstance(dec, ast.Attribute) and dec.attr == "guarded")
        for dec in node.decorator_list
    )


def check_file(path: str) -> list[tuple[int, str, str]]:
    """Check a single file for violations.

    Args:
        path (str): Path to the file.

    Returns:
        list[tuple[int, str, str]]: List of (line_number, type_name, file_path).
    """
    violations = []
    with open(path, "r", encoding="utf-8") as f:
        source = f.read()

    try:
        tree = ast.parse(source)
    except Exception:
        return []

    for node in ast.walk(tree):
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue

        if not _has_guarded_decorator(node):
            continue

        doc_text = _get_docstring_text(node)
        if not doc_text:
            continue

        for t in TYPES_TO_CHECK:
            if re.search(rf"\b{t}\b", doc_text):
                # node.body[0] is the Expr node containing the docstring
                violations.append((node.body[0].lineno, t, path))

    return violations


def main() -> None:
    """Main function to run the check across the source directory."""
    target_dir = "src/drawlib/v0_2/private"
    all_violations = []
    for root, _, files in os.walk(target_dir):
        if "drawlib/v0_2/private/types" in root:
            continue
        for f in files:
            if f.endswith(".py"):
                p = os.path.join(root, f)
                all_violations.extend(check_file(p))

    if all_violations:
        print(f"Found {len(all_violations)} violations in docstrings of @guarded functions:")
        for lineno, t, path in all_violations:
            print(f"{path}:{lineno}: Found forbidden type alias '{t}'")
        sys.exit(1)
    else:
        print("No forbidden type aliases found in @guarded function docstrings.")


if __name__ == "__main__":
    main()
