# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Generate Python preset Enum bindings (World, Countries, Cities) from maps/manifest.json."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any

from tools.dcli.common import PROJECT_ROOT

DEFAULT_MANIFEST_FILE = PROJECT_ROOT / "tools/release_assets/v0.3/maps/manifest.json"
DEFAULT_OUTPUT_FILE = PROJECT_ROOT / "src/drawlib/_smartarts/_geomap/_presets.py"

WORLD_PRESETS: list[tuple[str, str, tuple[float, float], tuple[float, float]]] = [
    ("All", "world:all", (-180.0, 180.0), (-60.0, 84.0)),
    ("Africa", "world:africa", (-20.0, 53.0), (-36.0, 38.0)),
    ("APAC", "world:apac", (65.0, 180.0), (-48.0, 55.0)),
    ("Asia", "world:asia", (25.0, 150.0), (-12.0, 56.0)),
    ("EastAsia", "world:east_asia", (73.0, 146.5), (18.0, 54.0)),
    ("Europe", "world:europe", (-25.0, 45.0), (34.0, 72.0)),
    ("MiddleEast", "world:middle_east", (24.0, 64.0), (12.0, 43.5)),
    ("NorthAmerica", "world:north_america", (-170.0, -50.0), (5.0, 75.0)),
    ("Oceania", "world:oceania", (110.0, 180.0), (-48.0, 0.0)),
    ("SouthAmerica", "world:south_america", (-85.0, -32.0), (-58.0, 15.0)),
    ("SoutheastAsia", "world:southeast_asia", (92.0, 142.0), (-11.5, 29.0)),
]

PRESETS_HEADER = '''# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Auto-generated preset target enumerations for GeoMap (do not edit manually)."""

from __future__ import annotations

from enum import StrEnum
from typing import Final
'''


def _build_presets_code(manifest_data: dict[str, Any]) -> str:
    """Build Python source code for _presets.py from manifest.json."""
    files_meta: dict[str, Any] = manifest_data.get("files", {})

    countries_items: list[tuple[str, str]] = []
    cities_items: list[tuple[str, str]] = []
    default_ranges: dict[str, tuple[tuple[float, float], tuple[float, float]]] = {}

    for enum_name, preset_key, lon_r, lat_r in WORLD_PRESETS:
        default_ranges[preset_key] = (lon_r, lat_r)

    for rel_path, meta in files_meta.items():
        category = meta.get("category")
        enum_name = str(meta.get("enum_name") or "")
        preset_key = rel_path.removesuffix(".geojson")
        lon_r = meta.get("default_lon_range")
        lat_r = meta.get("default_lat_range")

        if lon_r and lat_r:
            default_ranges[preset_key] = (
                (float(lon_r[0]), float(lon_r[1])),
                (float(lat_r[0]), float(lat_r[1])),
            )

        if category == "countries" and enum_name:
            countries_items.append((enum_name, preset_key))
        elif category == "cities" and enum_name:
            cities_items.append((enum_name, preset_key))

    countries_items.sort(key=lambda x: x[0])
    cities_items.sort(key=lambda x: x[0])

    lines: list[str] = [PRESETS_HEADER, "\nclass World(StrEnum):"]
    lines.append('    """Preset global and regional world map identifiers."""\n')
    for enum_name, preset_key, _, _ in WORLD_PRESETS:
        lines.append(f'    {enum_name} = "{preset_key}"')

    lines.append("\n\nclass Countries(StrEnum):")
    lines.append('    """Preset country map identifiers (Admin-1 states/prefectures)."""\n')
    for enum_name, preset_key in countries_items:
        lines.append(f'    {enum_name} = "{preset_key}"')

    lines.append("\n\nclass Cities(StrEnum):")
    lines.append('    """Preset city/metropolitan map identifiers (wards/districts)."""\n')
    for enum_name, preset_key in cities_items:
        lines.append(f'    {enum_name} = "{preset_key}"')

    lines.append(
        "\n\nPRESET_DEFAULT_RANGES: Final[dict[str, tuple[tuple[float, float], tuple[float, float]]]] = {"
    )
    for k in sorted(default_ranges.keys()):
        (lon0, lon1), (lat0, lat1) = default_ranges[k]
        lines.append(f'    "{k}": (({lon0}, {lon1}), ({lat0}, {lat1})),')
    lines.append("}\n")

    lines.append(
        '\n__all__ = [\n    "PRESET_DEFAULT_RANGES",\n    "Cities",\n    "Countries",\n    "World",\n]\n'
    )
    return "\n".join(lines)


def generate_map_code(
    manifest_file: Path = DEFAULT_MANIFEST_FILE,
    output_file: Path = DEFAULT_OUTPUT_FILE,
) -> None:
    """Generate Python preset Enum bindings for GeoMap from maps/manifest.json."""
    if not manifest_file.is_file():
        raise FileNotFoundError(f"Map manifest file not found: {manifest_file}")

    manifest_data = json.loads(manifest_file.read_text(encoding="utf-8"))
    code = _build_presets_code(manifest_data)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(code, encoding="utf-8")

    try:
        subprocess.run(["uv", "run", "ruff", "format", str(output_file)], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Failed to format {output_file} with ruff: {e}", file=sys.stderr)
