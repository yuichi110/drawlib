# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Helper module for generating Original concept icon Python bindings (cloud, devops, ai)."""

from __future__ import annotations

from pathlib import Path

from tools.dcli.codegen.gcp_codegen import format_code, load_gcp_manifest
from tools.dcli.common import PROJECT_ROOT

DEFAULT_MANIFEST_FILE = PROJECT_ROOT / "tools/release_assets/v0.3/icons/original_cloud/manifest.json"
DEFAULT_OUTPUT_FILE = PROJECT_ROOT / "src/drawlib/_icons/png_icons/original_cloud/_generated.py"

ORIGINAL_HEAD_TEMPLATE = '''# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""{provider_label} concept icon functions."""

from __future__ import annotations

from typing import Literal

from drawlib._core.l2_types import Coordinate, PosFloat
from drawlib._core.l3_styles import Style
from drawlib._icons.png_icons.{provider}._base import _write
'''

ORIGINAL_FUNCTION_TEMPLATE = '''
def {function_name}(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal[{variant_literal}] = "default",
) -> None:
    """Draws an {provider_label} concept icon representing {display_name}.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ({variant_doc}). Defaults to "default".

    """
    _write(xy=xy, width=width, name="{target_icon_name}", style=style, variant=variant)
'''

PROVIDER_LABELS: dict[str, str] = {
    "original_cloud": "Original Cloud",
    "original_devops": "Original DevOps",
    "original_ai": "Original AI",
    "aws": "AWS",
    "azure": "Azure",
}


def generate_code(
    icon_variants: dict[str, list[str]],
    aliases: dict[str, str] | None = None,
    *,
    provider: str = "original_cloud",
) -> str:
    """Generate Python source code for Original concept icons and shorthand aliases."""
    provider_label = PROVIDER_LABELS.get(provider, provider.replace("_", " ").title())
    code_parts: list[str] = [ORIGINAL_HEAD_TEMPLATE.format(provider=provider, provider_label=provider_label)]
    alias_map = aliases or {}

    all_functions: dict[str, tuple[str, list[str]]] = {}
    for icon_name, variants in icon_variants.items():
        all_functions[icon_name] = (icon_name, variants)
    for alias_name, target_name in alias_map.items():
        if target_name in icon_variants:
            all_functions[alias_name] = (target_name, icon_variants[target_name])

    for func_name in sorted(all_functions.keys()):
        target_name, variants = all_functions[func_name]
        display_name = func_name.replace("_", " ")
        variant_literal = ", ".join(f'"{v}"' for v in variants)
        variant_doc = " or ".join(f"'{v}'" for v in variants)
        code = ORIGINAL_FUNCTION_TEMPLATE.format(
            function_name=func_name,
            target_icon_name=target_name,
            display_name=display_name,
            variant_literal=variant_literal,
            variant_doc=variant_doc,
            provider_label=provider_label,
        )
        code_parts.append(code)

    return "".join(code_parts)


def generate_original_provider_code(
    provider: str,
    manifest_file: Path | None = None,
    output_file: Path | None = None,
) -> None:
    """Generate Python code for a specific Original icon provider from its manifest."""
    m_file = manifest_file or (PROJECT_ROOT / f"tools/release_assets/v0.3/icons/{provider}/manifest.json")
    o_file = output_file or (PROJECT_ROOT / f"src/drawlib/_icons/png_icons/{provider}/_generated.py")
    if not m_file.is_file():
        raise FileNotFoundError(f"Manifest file '{m_file}' not found.")

    provider_label = PROVIDER_LABELS.get(provider, provider)
    print(f"Reading {provider_label} icon manifest from {m_file}...")
    icon_variants, aliases = load_gcp_manifest(m_file)
    total_funcs = len(set(icon_variants.keys()) | set(aliases.keys()))
    print(f"Loaded {len(icon_variants)} canonical icons and {len(aliases)} aliases ({total_funcs} functions).")

    print(f"Generating Python code into {o_file}...")
    o_file.parent.mkdir(parents=True, exist_ok=True)
    generated_code = generate_code(icon_variants, aliases, provider=provider)
    o_file.write_text(generated_code, encoding="utf-8")

    print(f"Formatting {o_file} with ruff...")
    format_code(o_file)
    print(f"Successfully generated {total_funcs} {provider_label} icon functions in {o_file}!")


def generate_original_cloud_code(
    manifest_file: Path = DEFAULT_MANIFEST_FILE,
    output_file: Path = DEFAULT_OUTPUT_FILE,
) -> None:
    """Generate Python code for Original Cloud icons from manifest."""
    generate_original_provider_code("original_cloud", manifest_file=manifest_file, output_file=output_file)
