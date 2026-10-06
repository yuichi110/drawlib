# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Helper module for generating GCP icon Python bindings."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

from tools.dcli.common import PROJECT_ROOT

DEFAULT_MANIFEST_FILE = PROJECT_ROOT / "release_assets/v0.3/icons/gcp/manifest.json"
DEFAULT_OUTPUT_FILE = PROJECT_ROOT / "src/drawlib/_icons/png_icons/gcp/_generated.py"

GCP_HEAD = '''# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""GCP icon functions."""

from __future__ import annotations

from drawlib._core.l2_types import Angle, Coordinate, PosFloat
from drawlib._core.l3_styles import Style
from drawlib._icons.png_icons.gcp._base import _write
'''

GCP_FUNCTION_TEMPLATE = '''
def {function_name}(
    xy: Coordinate,
    width: PosFloat,
    angle: Angle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing {display_name}.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="{icon_name}", angle=angle, style=style)
'''


def load_gcp_manifest(manifest_path: Path) -> list[str]:
    """Load icon names from GCP manifest file.

    Args:
        manifest_path: Path to manifest.json.

    Returns:
        Sorted list of icon names (without .png extension).
    """
    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    files = data.get("files", {})
    names = sorted([fname.removesuffix(".png") for fname in files.keys()])
    return names


def generate_code(icon_names: list[str]) -> str:
    """Generate Python source code for GCP icons.

    Args:
        icon_names: List of icon names.

    Returns:
        Generated Python code string.
    """
    code_parts: list[str] = [GCP_HEAD]

    for icon_name in icon_names:
        display_name = icon_name.replace("_", " ")
        code = GCP_FUNCTION_TEMPLATE.format(
            function_name=icon_name,
            icon_name=icon_name,
            display_name=display_name,
        )
        code_parts.append(code)

    return "".join(code_parts)


def format_code(file_path: Path) -> None:
    """Format Python code file using ruff.

    Args:
        file_path: Path to the Python file to format.
    """
    try:
        subprocess.run(["uv", "run", "ruff", "format", str(file_path)], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Failed to format {file_path} with ruff: {e}", file=sys.stderr)


def generate_gcp_code(
    manifest_file: Path = DEFAULT_MANIFEST_FILE,
    output_file: Path = DEFAULT_OUTPUT_FILE,
) -> None:
    """Generate Python code for GCP icons from manifest.

    Args:
        manifest_file: Path to manifest.json file.
        output_file: Target output Python file path.
    """
    if not manifest_file.is_file():
        raise FileNotFoundError(f"Manifest file '{manifest_file}' not found.")

    print(f"Reading GCP icon manifest from {manifest_file}...")
    icon_names = load_gcp_manifest(manifest_file)
    print(f"Loaded {len(icon_names)} icons.")

    print(f"Generating Python code into {output_file}...")
    output_file.parent.mkdir(parents=True, exist_ok=True)
    generated_code = generate_code(icon_names)
    output_file.write_text(generated_code, encoding="utf-8")

    print(f"Formatting {output_file} with ruff...")
    format_code(output_file)
    print(f"Successfully generated {len(icon_names)} GCP icon functions in {output_file}!")


def main() -> None:
    """CLI entrypoint for generating GCP icon functions."""
    parser = argparse.ArgumentParser(description="Generate GCP icon Python bindings.")
    parser.add_argument(
        "--manifest-file",
        type=Path,
        default=DEFAULT_MANIFEST_FILE,
        help=f"Path to GCP manifest JSON file (default: {DEFAULT_MANIFEST_FILE}).",
    )
    parser.add_argument(
        "--output-file",
        type=Path,
        default=DEFAULT_OUTPUT_FILE,
        help=f"Output Python file (default: {DEFAULT_OUTPUT_FILE}).",
    )
    args = parser.parse_args()

    generate_gcp_code(manifest_file=args.manifest_file, output_file=args.output_file)


if __name__ == "__main__":
    main()
