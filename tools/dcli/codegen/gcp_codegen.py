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

import json
import subprocess
import sys
from pathlib import Path

from tools.dcli.common import PROJECT_ROOT

DEFAULT_MANIFEST_FILE = PROJECT_ROOT / "tools/release_assets/v0.3/icons/gcp/manifest.json"
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

from typing import Literal

from drawlib._core.l2_types import Coordinate, PosFloat
from drawlib._core.l3_styles import Style
from drawlib._icons.png_icons.gcp._base import _write
'''

GCP_FUNCTION_TEMPLATE = '''
def {function_name}(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal[{variant_literal}] = "default",
) -> None:
    """Draws a GCP icon representing {display_name}.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ({variant_doc}). Defaults to "default".

    """
    _write(xy=xy, width=width, name="{target_icon_name}", style=style, variant=variant)
'''


def load_gcp_manifest(manifest_path: Path) -> dict[str, list[str]]:
    """Load canonical icon variants from a provider manifest file.

    Args:
        manifest_path: Path to manifest.json.

    Returns:
        Mapping of canonical icon name to sorted list of variants.
    """
    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    files = data.get("files", {})

    icon_variants: dict[str, set[str]] = {}
    for fname, meta in files.items():
        if isinstance(meta, dict) and "icon_name" in meta:
            icon_name = str(meta["icon_name"])
            variant = str(meta.get("variant", "default"))
        else:
            stem = fname.removesuffix(".png")
            icon_name, variant = stem.rsplit("_", 1) if stem.endswith(("_default", "_modern")) else (stem, "default")
        icon_variants.setdefault(icon_name, set()).add(variant)

    def _sort_variants(variants: set[str]) -> list[str]:
        order = {"default": 0, "modern": 1}
        return sorted(variants, key=lambda v: (order.get(v, 99), v))

    return {k: _sort_variants(v) for k, v in sorted(icon_variants.items())}


def generate_code(
    icon_variants: dict[str, list[str]],
) -> str:
    """Generate Python source code for canonical GCP icons.

    Args:
        icon_variants: Mapping of canonical icon name to available variants.

    Returns:
        Generated Python code string.
    """
    code_parts: list[str] = [GCP_HEAD]

    for func_name in sorted(icon_variants.keys()):
        variants = icon_variants[func_name]
        display_name = func_name.replace("_", " ")
        variant_literal = ", ".join(f'"{v}"' for v in variants)
        variant_doc = " or ".join(f"'{v}'" for v in variants)
        code = GCP_FUNCTION_TEMPLATE.format(
            function_name=func_name,
            target_icon_name=func_name,
            display_name=display_name,
            variant_literal=variant_literal,
            variant_doc=variant_doc,
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
    icon_variants = load_gcp_manifest(manifest_file)
    total_funcs = len(icon_variants)
    print(f"Loaded {total_funcs} canonical icons.")

    print(f"Generating Python code into {output_file}...")
    output_file.parent.mkdir(parents=True, exist_ok=True)
    generated_code = generate_code(icon_variants)
    output_file.write_text(generated_code, encoding="utf-8")

    print(f"Formatting {output_file} with ruff...")
    format_code(output_file)
    print(f"Successfully generated {total_funcs} GCP icon functions in {output_file}!")
