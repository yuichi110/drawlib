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

import re
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
    "original_network": "Original Network",
    "aws": "AWS",
    "azure": "Azure",
    "network": "Network",
    "server": "Server",
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
        if provider == "network" and "default" in variants and "classic" not in variants:
            idx = variants.index("default")
            variants = [*variants[: idx + 1], "classic", *variants[idx + 1 :]]
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


PROVIDER_ENUM_NAMES: dict[str, str] = {
    "original_cloud": "OriginalCloudIcon",
    "original_devops": "OriginalDevopsIcon",
    "original_ai": "OriginalAiIcon",
    "original_network": "OriginalNetworkIcon",
    "aws": "AwsIcon",
    "azure": "AzureIcon",
    "network": "NetworkIcon",
    "server": "ServerIcon",
}


def _update_architecture_enum(provider: str, func_names: list[str]) -> None:
    """Synchronize the provider's Enum class in `src/drawlib/_diagrams/architecture/_icons.py`."""
    enum_name = PROVIDER_ENUM_NAMES.get(provider)
    if not enum_name:
        return
    icons_py = PROJECT_ROOT / "src/drawlib/_diagrams/architecture/_icons.py"
    if not icons_py.is_file():
        return

    text = icons_py.read_text(encoding="utf-8")
    pattern = re.compile(
        rf"(class {enum_name}\(str, Enum\):\n"
        rf'    """[^\n]+"""\n\n)'
        rf"(?:    [A-Z0-9_]+ = \"[^\"]+\"(?:  # noqa: S105)?\n)+",
    )
    match = pattern.search(text)
    if not match:
        return

    lines: list[str] = []
    for fn in sorted(func_names):
        const_name = fn.upper()
        suffix = "  # noqa: S105" if "secret" in fn or "password" in fn or "token" in fn else ""
        lines.append(f'    {const_name} = "{fn}"{suffix}\n')

    replacement = match.group(1) + "".join(lines)
    new_text = text[: match.start()] + replacement + text[match.end() :]
    if new_text != text:
        icons_py.write_text(new_text, encoding="utf-8")
        format_code(icons_py)


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
    all_func_names = sorted(set(icon_variants.keys()) | {k for k, v in aliases.items() if v in icon_variants})
    total_funcs = len(all_func_names)
    print(f"Loaded {len(icon_variants)} canonical icons and {len(aliases)} aliases ({total_funcs} functions).")

    print(f"Generating Python code into {o_file}...")
    o_file.parent.mkdir(parents=True, exist_ok=True)
    generated_code = generate_code(icon_variants, aliases, provider=provider)
    o_file.write_text(generated_code, encoding="utf-8")

    print(f"Formatting {o_file} with ruff...")
    format_code(o_file)
    _update_architecture_enum(provider, all_func_names)
    print(f"Successfully generated {total_funcs} {provider_label} icon functions in {o_file}!")


def generate_original_cloud_code(
    manifest_file: Path = DEFAULT_MANIFEST_FILE,
    output_file: Path = DEFAULT_OUTPUT_FILE,
) -> None:
    """Generate Python code for Original Cloud icons from manifest."""
    generate_original_provider_code("original_cloud", manifest_file=manifest_file, output_file=output_file)

