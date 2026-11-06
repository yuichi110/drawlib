# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Mechanical completeness and i18n parity tests for ``docs_src/api/``."""

from __future__ import annotations

import importlib
import pkgutil
import re
from pathlib import Path
from types import ModuleType
from typing import TYPE_CHECKING, Final

import pytest

import drawlib
from drawlib._builder._common import load_project_manifest
from drawlib._builder.doc_builder.catalog_nav import _mask_fences_and_comments, extract_catalog_headings
from drawlib._builder.doc_builder.i18n import validate_i18n_project
from drawlib._cli._drawlib import app as cli_root_app

if TYPE_CHECKING:
    import typer

REPO_ROOT: Final[Path] = Path(__file__).resolve().parents[3]
API_DOCS_DIR: Final[Path] = REPO_ROOT / "docs_src" / "api"

MODULE_TO_PAGES: Final[dict[str, tuple[str, ...]]] = {
    "drawlib": ("00_overview.md",),
    "drawlib.utils": ("00_overview.md",),
    "drawlib.charts": ("00_overview.md",),
    "drawlib.diagrams": ("00_overview.md",),
    "drawlib.canvas": ("01_canvas.md",),
    "drawlib.shapes": ("02_shapes.md",),
    "drawlib.lines": ("03_lines_and_text.md",),
    "drawlib.text": ("03_lines_and_text.md",),
    "drawlib.images": ("04_images_and_math.md",),
    "drawlib.math": ("04_images_and_math.md",),
    "drawlib.styles": ("05_styles_and_types.md",),
    "drawlib.types": ("05_styles_and_types.md",),
    "drawlib.preset_styles": ("06_presets.md",),
    "drawlib.preset_colors": ("06_presets.md",),
    "drawlib.fonts": ("07_fonts.md",),
    "drawlib.icons": ("08_icons.md",),
    "drawlib.smartarts": ("09_smartarts_lists_cards.md", "10_smartarts_flows_trees_maps.md"),
    "drawlib.charts.bar": ("11_charts_bar.md",),
    "drawlib.charts.line": ("12_charts_line.md",),
    "drawlib.charts.area": ("13_charts_area.md",),
    "drawlib.charts.pie": ("14_charts_pie.md",),
    "drawlib.charts.radar": ("15_charts_radar.md",),
    "drawlib.charts.scatter": ("16_charts_scatter.md",),
    "drawlib.charts.gantt": ("17_charts_gantt.md",),
    "drawlib.charts.heatmap": ("18_charts_heatmap.md",),
    "drawlib.charts.box": ("18b_charts_box.md",),
    "drawlib.diagrams.architecture": ("19_diagrams_architecture.md",),
    "drawlib.diagrams.flow": ("20_diagrams_flow.md",),
    "drawlib.diagrams.sequence": ("21_diagrams_sequence.md",),
    "drawlib.diagrams.class_diagram": ("22_diagrams_class.md",),
    "drawlib.diagrams.er": ("23_diagrams_er.md",),
    "drawlib.diagrams.state": ("24_diagrams_state.md",),
    "drawlib.graph": ("25_graph.md",),
    "drawlib.anim": ("26_anim_and_slide.md",),
    "drawlib.slide": ("26_anim_and_slide.md",),
    "drawlib.tools": ("27_tools.md",),
}

OVERVIEW_REEXPORT_PACKAGES: Final[frozenset[str]] = frozenset(
    {"drawlib", "drawlib.charts", "drawlib.diagrams"}
)
ICON_ENUM_DIAGRAM_MODULES: Final[frozenset[str]] = frozenset(
    {"drawlib.diagrams.architecture", "drawlib.diagrams.sequence"}
)


def _discover_public_modules() -> list[str]:
    """Discover all non-underscore public modules under ``drawlib``."""
    discovered = ["drawlib"]
    for mod_info in pkgutil.walk_packages(drawlib.__path__, "drawlib."):
        if not any(part.startswith("_") for part in mod_info.name.split(".")):
            discovered.append(mod_info.name)
    return sorted(discovered)


def _discover_cli_commands(typer_app: typer.Typer, prefix: str = "drawlib") -> list[str]:
    """Walk a Typer app tree and return sorted ``'drawlib ...'`` group and leaf command paths."""
    commands: list[str] = []
    for group in typer_app.registered_groups:
        sub_app = group.typer_instance
        if sub_app is None:
            continue
        group_name = group.name or sub_app.info.name or ""
        full_group = f"{prefix} {group_name}".strip()
        commands.append(full_group)
        commands.extend(_discover_cli_commands(sub_app, full_group))

    for cmd in typer_app.registered_commands:
        callback_name = str(getattr(cmd.callback, "__name__", ""))
        cmd_name = cmd.name or callback_name.removeprefix("cmd_").replace("_", "-")
        commands.append(f"{prefix} {cmd_name}".strip())

    return sorted(commands)


def _extract_page_symbols_and_spans(md_path: Path) -> tuple[set[str], set[str]]:
    """Return badged H2 symbol names and non-fence inline code spans from ``md_path``."""
    md_text = md_path.read_text(encoding="utf-8")
    headings = extract_catalog_headings(md_text, fallback_stem=md_path.stem)
    h2_symbols: set[str] = set()
    for item in headings.h2_items:
        if item.badge_kind is None:
            continue
        sym_head = item.raw_title.split("(", 1)[0].strip()
        h2_symbols.add(sym_head)
        if "." in sym_head:
            h2_symbols.add(sym_head.rsplit(".", 1)[-1])

    prose_text = "\n".join(_mask_fences_and_comments(md_text))
    code_spans = set(re.findall(r"`([^`\n]+)`", prose_text))
    return h2_symbols, code_spans


def _is_tabulated_symbol(mod_name: str, sym: str, obj: object) -> bool:
    """Return True if ``sym`` is intentionally documented in a structured summary table."""
    if mod_name in OVERVIEW_REEXPORT_PACKAGES and isinstance(obj, ModuleType):
        return True
    return mod_name in ICON_ENUM_DIAGRAM_MODULES and sym.endswith("Icon")


def _load_pages_union(
    lang: str,
    mod_name: str,
    pages: tuple[str, ...],
    page_cache: dict[str, tuple[set[str], set[str]]],
) -> tuple[set[str], set[str], list[str]]:
    """Aggregate H2 symbol names and inline code spans across ``pages`` for ``mod_name``."""
    lang_dir = API_DOCS_DIR / lang
    h2_union: set[str] = set()
    span_union: set[str] = set()
    errors: list[str] = []

    for page_name in pages:
        page_path = lang_dir / page_name
        if not page_path.is_file():
            errors.append(f"[{lang}] Missing page {page_name} for {mod_name}")
            continue
        if page_name not in page_cache:
            page_cache[page_name] = _extract_page_symbols_and_spans(page_path)
        h2_syms, spans = page_cache[page_name]
        h2_union.update(h2_syms)
        span_union.update(spans)

    return h2_union, span_union, errors


def _check_module_exports(
    lang: str,
    mod_name: str,
    pages: tuple[str, ...],
    h2_union: set[str],
    span_union: set[str],
) -> list[str]:
    """Return missing-symbol error messages for a single public module."""
    if mod_name == "drawlib.utils":
        if "drawlib.utils" not in h2_union and "utils" not in h2_union:
            return [f"[{lang}] drawlib.utils missing badged H2 on {pages}"]
        return []

    mod = importlib.import_module(mod_name)
    missing: list[str] = []
    for sym in getattr(mod, "__all__", []):
        obj = getattr(mod, sym)
        if _is_tabulated_symbol(mod_name, sym, obj):
            if sym not in h2_union and sym not in span_union:
                missing.append(f"[{lang}] {mod_name}.{sym} missing from table/headings in {pages}")
        elif sym not in h2_union and f"{mod_name}.{sym}" not in h2_union:
            missing.append(f"[{lang}] {mod_name}.{sym} missing badged ## heading in {pages}")
    return missing


def _collect_missing_symbols_for_locale(lang: str) -> list[str]:
    """Verify every public module export is documented in ``docs_src/api/<lang>/``."""
    page_cache: dict[str, tuple[set[str], set[str]]] = {}
    missing: list[str] = []

    for mod_name, pages in sorted(MODULE_TO_PAGES.items()):
        h2_union, span_union, page_errors = _load_pages_union(lang, mod_name, pages, page_cache)
        missing.extend(page_errors)
        if not page_errors:
            missing.extend(_check_module_exports(lang, mod_name, pages, h2_union, span_union))

    return missing


def test_all_public_modules_mapped_in_api_reference() -> None:
    """Ensure every non-underscore ``drawlib.*`` module is mapped to an API Reference page."""
    discovered = _discover_public_modules()
    assert set(discovered) == set(MODULE_TO_PAGES.keys()), (
        f"Public module set changed! Unmapped: { sorted(set(discovered) - set(MODULE_TO_PAGES)) }, "
        f"Stale: { sorted(set(MODULE_TO_PAGES) - set(discovered)) }"
    )


def test_python_public_api_100_percent_documented() -> None:
    """Verify 100% of ``__all__`` exports across all 36 public modules are documented in EN and JA."""
    if not API_DOCS_DIR.exists():
        pytest.skip("docs_src/api not present in clean-room container.")
    for lang in ("en", "ja"):
        missing = _collect_missing_symbols_for_locale(lang)
        assert not missing, "Undocumented public Python API symbols:\n" + "\n".join(missing)


def test_cli_commands_100_percent_documented() -> None:
    """Verify 100% of ``drawlib`` Typer CLI groups and subcommands appear as ``cmd`` H2s in EN and JA."""
    expected_cmds = _discover_cli_commands(cli_root_app)
    assert len(expected_cmds) >= 39
    if not API_DOCS_DIR.exists():
        pytest.skip("docs_src/api not present in clean-room container.")

    for lang in ("en", "ja"):
        cli_md = API_DOCS_DIR / lang / "28_cli.md"
        assert cli_md.is_file(), f"Missing {cli_md}"
        headings = extract_catalog_headings(cli_md.read_text(encoding="utf-8"), fallback_stem="28_cli")
        cmd_titles = [item.raw_title.strip() for item in headings.h2_items if item.badge_kind == "cmd"]

        missing_cmds = [
            cmd
            for cmd in expected_cmds
            if not any(title == cmd or title.startswith(f"{cmd} ") for title in cmd_titles)
        ]
        assert not missing_cmds, f"[{lang}] Undocumented CLI commands in 28_cli.md: {missing_cmds}"


def test_api_reference_i18n_slug_and_hero_parity() -> None:
    """Verify bilingual manifest, skeleton/code parity, identical H2 slugs, and Top Hero diagrams."""
    if not API_DOCS_DIR.exists():
        pytest.skip("docs_src/api not present in clean-room container.")
    manifest = load_project_manifest(str(API_DOCS_DIR))
    assert manifest is not None
    assert manifest.project.type == "catalog"
    assert manifest.catalog is not None
    assert manifest.catalog.resolve_breadcrumb_root("en") == "API Reference"
    assert manifest.catalog.resolve_breadcrumb_root("ja") == "API リファレンス"
    assert manifest.i18n is not None
    assert tuple(manifest.i18n.langs) == ("en", "ja")

    files_by_lang = validate_i18n_project(str(API_DOCS_DIR), manifest.i18n, project_type="catalog")
    en_files = files_by_lang["en"]
    assert len(en_files) >= 29

    for rel_md in en_files:
        en_text = (API_DOCS_DIR / "en" / rel_md).read_text(encoding="utf-8")
        ja_text = (API_DOCS_DIR / "ja" / rel_md).read_text(encoding="utf-8")

        assert "```drawlib" in en_text, f"en/{rel_md} must include at least a Top Hero drawlib diagram"
        assert "```drawlib" in ja_text, f"ja/{rel_md} must include at least a Top Hero drawlib diagram"

        en_h = extract_catalog_headings(en_text, fallback_stem=Path(rel_md).stem)
        ja_h = extract_catalog_headings(ja_text, fallback_stem=Path(rel_md).stem)
        en_sig = [(item.badge_kind, item.slug) for item in en_h.h2_items]
        ja_sig = [(item.badge_kind, item.slug) for item in ja_h.h2_items]
        assert en_sig == ja_sig, f"H2 badge/slug mismatch in {rel_md}:\nEN={en_sig}\nJA={ja_sig}"
