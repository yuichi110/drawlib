# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Helper script for generating Phosphor icon python bindings."""

from __future__ import annotations

import argparse
import sys
import urllib.request
from pathlib import Path

project_root = Path(__file__).parent.parent.parent.resolve()
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from tools.scripts.utils import cd_to_project_root  # noqa: E402

PHOSPHOR_CSS_LOCAL = Path("release_assets/v0.3/fonticons/phosphor/regular.css")
PHOSPHOR_CSS_REMOTE = (
    "https://raw.githubusercontent.com/yuichi110/drawlib_assets/main/assets/v0_2/fonticons/phosphor/regular.css"
)
DEFAULT_OUTPUT_FILE = Path("src/drawlib/_icons/font_icons/phosphor/_generated.py")

PHOSPHOR_HEAD = '''# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Phosphor icon functions."""

from __future__ import annotations

from drawlib._core.l1_core import guarded
from drawlib._core.l2_types import (
    TypeAngle,
    TypeCoordinate,
    TypePosFloat,
    TypeStr,
)
from drawlib._core.l3_styles import Style
from drawlib._icons.font_icons.phosphor._base import _write
'''

PHOSPHOR_FUNCTION_TEMPLATE = '''
@guarded
def {function_name}(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    style: Style | TypeStr | None = None,
) -> None:
    """Draws a Phosphor icon representing an {icon_name}.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style of the icon as an Style object, string, or None.

    """
    _write(xy=xy, width=width, code="\\u{icon_code}", angle=angle, style=style)
'''


def parse_css_icons(css_text: str) -> dict[str, str]:
    """Parse icon name and Unicode codepoint mapping from Phosphor CSS.

    Args:
        css_text: Raw CSS content.

    Returns:
        Dictionary mapping icon name to hex code string (e.g. 'airplane' -> 'e002').
    """
    icons: dict[str, str] = {}
    key = ""
    for line in css_text.splitlines():
        line = line.strip()
        if line.startswith(".ph") and line.endswith(":before {"):
            words = line.split(".")
            key = words[2][3:-9]
        elif key:
            words = line.split(":")
            value = words[1].strip()[2:-2]
            icons[key] = value
            key = ""
    return icons


def load_phosphor_icons() -> dict[str, str]:
    """Load Phosphor icon definitions from local asset CSS or remote fallback.

    Returns:
        Dictionary mapping icon name to hex codepoints.
    """
    if PHOSPHOR_CSS_LOCAL.exists():
        print(f"[*] Reading Phosphor CSS from local asset: {PHOSPHOR_CSS_LOCAL}")
        css_text = PHOSPHOR_CSS_LOCAL.read_text(encoding="utf-8")
    else:
        print(f"[*] Fetching Phosphor CSS from remote: {PHOSPHOR_CSS_REMOTE}")
        req = urllib.request.Request(PHOSPHOR_CSS_REMOTE, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req) as resp:
            css_text = resp.read().decode("utf-8")

    icons = parse_css_icons(css_text)
    print(f"[✓] Loaded {len(icons)} Phosphor icon definitions.")
    return icons


def generate_phosphor_code(output_path: Path) -> None:
    """Generate Phosphor icon module code and write directly to destination.

    Args:
        output_path: Target Python file path.
    """
    icons = load_phosphor_icons()

    chunks: list[str] = [PHOSPHOR_HEAD.strip()]
    for icon_name in sorted(icons.keys()):
        icon_code = icons[icon_name]
        function_name = icon_name.replace("-", "_")
        func_text = PHOSPHOR_FUNCTION_TEMPLATE.format(
            function_name=function_name,
            icon_name=icon_name,
            icon_code=icon_code,
        )
        chunks.append(func_text.strip())

    full_code = "\n\n\n".join(chunks) + "\n"

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(full_code, encoding="utf-8")
    print(f"[✓] Generated Phosphor icon code directly at: {output_path}")


def main() -> None:
    """CLI entry point for generating Phosphor icon code."""
    cd_to_project_root()

    parser = argparse.ArgumentParser(description="Generate Phosphor icon Python bindings.")
    parser.add_argument(
        "--output",
        "-o",
        type=Path,
        default=DEFAULT_OUTPUT_FILE,
        help=f"Target file path (default: {DEFAULT_OUTPUT_FILE}).",
    )
    args = parser.parse_args()

    generate_phosphor_code(output_path=args.output)


if __name__ == "__main__":
    main()
