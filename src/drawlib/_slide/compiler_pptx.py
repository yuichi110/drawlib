# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""MS PowerPoint (.pptx) presentation compiler for Drawlib slide decks."""

from __future__ import annotations

import os
import tempfile
from typing import Literal

from drawlib._builder._common import resolve_build_workers
from drawlib._slide.compiler import build_slide, require_slide_manifest


def build_pptx(
    input_dir: str,
    output_file: str | None = None,
    *,
    title: str | None = None,
    theme: str | None = None,
    dpi: int = 240,
    anim_frame: Literal["first", "last"] = "last",
    styles_path: str | None = None,
    utils_path: str | None = None,
    no_cache: bool = False,
    timestamp: bool = False,
    workers: int | Literal["auto"] = "auto",
) -> str:
    """Compile an ``i18n``-native Markdown slide project into native MS PowerPoint (``.pptx``) decks.

    Renders all embedded ````drawlib```` diagrams as high-DPI static PNGs once across locales,
    measures exact 1920x1080 stage layout and computed typography via Headless Chromium for each
    configured language, and writes ``<stem>_<lang>.pptx`` deliverables at 0.5x (960x540 pt) scale.

    Args:
        input_dir: Project root directory containing ``drawlib.toml`` and ``<lang>/`` slide files.
        output_file: Optional destination ``.pptx`` base path or directory (produces ``<stem>_<lang>.pptx``).
        title: Optional presentation title override.
        theme: CSS theme preset name ('google', 'default', 'google-dark', 'default-dark', etc.).
        dpi: Rasterization DPI for embedded drawlib diagrams. Defaults to 240.
        anim_frame: Frame ('first' or 'last') extracted from multi-frame Animation() diagrams.
        styles_path: Optional path to custom styles.py script.
        utils_path: Optional path to custom utils.py script.
        no_cache: If True, disable reading/writing the SQLite build image cache.
        timestamp: If True, include current build timestamp in OpenXML metadata.
        workers: Number of parallel rendering worker processes ('auto' or positive integer >= 1).

    Returns:
        str: Absolute path to the generated default-language ``<stem>_<default_lang>.pptx`` file.

    Raises:
        ValueError: If ``input_dir`` is invalid, lacks ``drawlib.toml``, ``dpi <= 0``, or ``anim_frame`` is invalid.
        RuntimeError: If Playwright, Chromium, or python-pptx fails.
    """
    eff_workers = resolve_build_workers(workers)
    if not input_dir:
        raise ValueError("No input directory specified for build_pptx.")
    input_abs = os.path.abspath(input_dir)
    if not os.path.isdir(input_abs):
        raise ValueError(f"Input directory does not exist: '{input_dir}'")
    if dpi <= 0:
        raise ValueError(f"dpi must be a positive integer, got {dpi}.")
    if anim_frame not in {"first", "last"}:
        raise ValueError(f"anim_frame must be 'first' or 'last', got '{anim_frame}'.")

    manifest = require_slide_manifest(input_abs)
    assert manifest.i18n is not None  # noqa: S101
    i18n_cfg = manifest.i18n

    from drawlib._builder.doc_builder.compiler.base import resolve_multi_locale_dest  # noqa: PLC0415
    from drawlib._slide._pptx_dom import extract_deck_dom  # noqa: PLC0415
    from drawlib._slide._pptx_writer import write_deck_to_pptx  # noqa: PLC0415

    default_base_dir = os.path.dirname(input_abs.rstrip(os.sep))
    default_stem = manifest.project.name

    generated_paths: dict[str, str] = {}
    with tempfile.TemporaryDirectory() as tmp_root:
        stage_dir = os.path.join(tmp_root, "html_stage")
        scratch_dir = os.path.join(tmp_root, "pptx_scratch")
        os.makedirs(scratch_dir, exist_ok=True)

        build_slide(
            input_dir=input_abs,
            output_dir=stage_dir,
            title=title,
            theme=theme,
            image_format="png",
            dpi=dpi,
            force_image_format=True,
            static_anim_frame=anim_frame,
            styles_path=styles_path,
            utils_path=utils_path,
            no_cache=no_cache,
            workers=eff_workers,
        )

        for lang in i18n_cfg.langs:
            dest_abs = resolve_multi_locale_dest(
                default_base_dir,
                default_stem,
                output_file,
                lang,
                ".pptx",
            )
            dest_parent = os.path.dirname(dest_abs)
            if dest_parent:
                os.makedirs(dest_parent, exist_ok=True)

            lang_scratch = os.path.join(scratch_dir, lang)
            os.makedirs(lang_scratch, exist_ok=True)
            lang_index_html = os.path.join(stage_dir, lang, "index.html")
            deck_spec = extract_deck_dom(lang_index_html, svg_capture_dir=lang_scratch)
            written_path = write_deck_to_pptx(
                deck=deck_spec,
                output_path=dest_abs,
                scratch_dir=lang_scratch,
                title=title,
                anim_frame=anim_frame,
                timestamp=timestamp,
            )
            generated_paths[lang] = written_path

    return generated_paths[i18n_cfg.default_lang]
