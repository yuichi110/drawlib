# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Unified ``drawlib.toml`` project manifest parser and validator."""

from __future__ import annotations

import os
import tomllib
from typing import Literal

from pydantic import BaseModel, ConfigDict

from drawlib._templates.langs import normalize_language

PROJECT_MANIFEST_FILENAME = "drawlib.toml"
ProjectArchetype = Literal["images", "doc", "site", "slide"]
_VALID_ARCHETYPES: dict[str, ProjectArchetype] = {
    "images": "images",
    "image": "images",
    "doc": "doc",
    "site": "site",
    "slide": "slide",
}


class ProjectMetadata(BaseModel):
    """Metadata under the ``[project]`` section of ``drawlib.toml``.

    Attributes:
        name: Project identifier / base stem (e.g. ``'quickstart'``, ``'drawlib-dogfooding'``).
        type: Canonical project archetype (``'images'``, ``'doc'``, ``'site'``, or ``'slide'``).
        title: Optional default document/site title override.
        description: Optional human/agent-facing summary of the project.
        lang: Canonical single-language code (e.g. ``'en'``, ``'ja'``).
        style: Style preset theme or CSS path recorded at initialization.
    """

    model_config = ConfigDict(frozen=True)

    name: str
    type: ProjectArchetype
    title: str = ""
    description: str = ""
    lang: str = "en"
    style: str = "default"


class I18nConfig(BaseModel):
    """Parsed multi-locale configuration from the ``[i18n]`` section of ``drawlib.toml``.

    Attributes:
        default_lang: Canonical default language key (e.g. ``'en'``).
        langs: Ordered list of canonical language keys enabled for the project (e.g. ``['en', 'ja']``).
    """

    model_config = ConfigDict(frozen=True)

    default_lang: str
    langs: list[str]


class ProjectManifest(BaseModel):
    """Validated project manifest parsed from ``drawlib.toml``.

    Attributes:
        project: Core project archetype and metadata from ``[project]``.
        i18n: Optional multi-locale configuration from ``[i18n]``.
    """

    model_config = ConfigDict(frozen=True)

    project: ProjectMetadata
    i18n: I18nConfig | None = None

    @property
    def is_i18n(self) -> bool:
        """Return True if this project uses multi-locale ``<lang>/`` subdirectories."""
        return self.i18n is not None

    @property
    def effective_lang(self) -> str:
        """Return default canonical language code for single-locale or multi-locale projects."""
        if self.i18n is not None:
            return self.i18n.default_lang
        return self.project.lang


def _parse_project_section(raw_proj: object, cfg_path: str, input_abs: str) -> ProjectMetadata:
    """Validate and normalize the ``[project]`` table."""
    if not isinstance(raw_proj, dict):
        raise ValueError(f'Invalid "{cfg_path}": missing required "[project]" table.')

    raw_type = raw_proj.get("type")
    if not isinstance(raw_type, str) or raw_type.strip().lower() not in _VALID_ARCHETYPES:
        valid_str = ", ".join(("images", "doc", "site", "slide"))
        raise ValueError(f'Invalid "{cfg_path}": "[project].type" must be one of [{valid_str}], got {raw_type!r}.')
    norm_type = _VALID_ARCHETYPES[raw_type.strip().lower()]

    raw_name = raw_proj.get("name")
    if raw_name is None:
        dir_base = os.path.basename(input_abs.rstrip(os.sep))
        norm_name = dir_base[:-4] if dir_base.endswith("_src") and len(dir_base) > 4 else (dir_base or norm_type)
    elif isinstance(raw_name, str) and raw_name.strip():
        norm_name = raw_name.strip()
    else:
        raise ValueError(f'Invalid "{cfg_path}": "[project].name" must be a non-empty string.')

    raw_title = raw_proj.get("title", "")
    if not isinstance(raw_title, str):
        raise ValueError(f'Invalid "{cfg_path}": "[project].title" must be a string.')

    raw_desc = raw_proj.get("description", "")
    if not isinstance(raw_desc, str):
        raise ValueError(f'Invalid "{cfg_path}": "[project].description" must be a string.')

    raw_style = raw_proj.get("style", "default")
    if not isinstance(raw_style, str) or not raw_style.strip():
        raise ValueError(f'Invalid "{cfg_path}": "[project].style" must be a non-empty string.')

    raw_lang = raw_proj.get("lang", "en")
    if not isinstance(raw_lang, str) or not raw_lang.strip():
        raise ValueError(f'Invalid "{cfg_path}": "[project].lang" must be a non-empty language code string.')
    norm_lang = normalize_language(raw_lang)

    return ProjectMetadata(
        name=norm_name,
        type=norm_type,
        title=raw_title.strip(),
        description=raw_desc.strip(),
        lang=norm_lang,
        style=raw_style.strip(),
    )


def _parse_i18n_section(
    raw_i18n: object,
    project_meta: ProjectMetadata,
    cfg_path: str,
    input_abs: str,
) -> I18nConfig:
    """Validate and normalize the ``[i18n]`` table and verify locale directories exist."""
    if not isinstance(raw_i18n, dict):
        raise ValueError(f'Invalid "{cfg_path}": "[i18n]" must be a TOML table.')

    if project_meta.type not in {"doc", "site"}:
        raise ValueError(
            f'Invalid "{cfg_path}": "[i18n]" is only supported for "doc" and "site" projects, '
            f'not "{project_meta.type}".'
        )

    raw_default = raw_i18n.get("default_lang")
    raw_langs = raw_i18n.get("langs")
    if not isinstance(raw_default, str) or not raw_default.strip():
        raise ValueError(f'Invalid "{cfg_path}": "[i18n].default_lang" must be a non-empty string.')
    if not isinstance(raw_langs, list) or len(raw_langs) == 0 or not all(isinstance(x, str) for x in raw_langs):
        raise ValueError(f'Invalid "{cfg_path}": "[i18n].langs" must be a non-empty list of language code strings.')

    norm_default = normalize_language(raw_default)
    norm_langs: list[str] = []
    for code in raw_langs:
        norm_code = normalize_language(code)
        if norm_code in norm_langs:
            raise ValueError(f'Invalid "{cfg_path}": duplicate language "{norm_code}" in "[i18n].langs".')
        norm_langs.append(norm_code)

    if norm_default not in norm_langs:
        raise ValueError(
            f'Invalid "{cfg_path}": default_lang "{norm_default}" must be included in langs {norm_langs}.'
        )

    for lang_code in norm_langs:
        lang_dir = os.path.join(input_abs, lang_code)
        if not os.path.isdir(lang_dir):
            raise ValueError(
                f'Missing locale directory "{lang_dir}" required by "{cfg_path}" (lang="{lang_code}").'
            )

    return I18nConfig(default_lang=norm_default, langs=norm_langs)


def load_project_manifest(input_dir: str) -> ProjectManifest | None:
    """Load and validate ``drawlib.toml`` directly inside ``input_dir`` if present.

    Args:
        input_dir: Root source directory of a Drawlib project.

    Returns:
        ProjectManifest | None: Validated manifest, or ``None`` if ``drawlib.toml`` is absent.

    Raises:
        ValueError: If ``drawlib.toml`` is malformed or violates schema/directory constraints.
    """
    input_abs = os.path.abspath(input_dir)
    cfg_path = os.path.join(input_abs, PROJECT_MANIFEST_FILENAME)
    if not os.path.isfile(cfg_path):
        return None

    try:
        with open(cfg_path, "rb") as f:
            raw = tomllib.load(f)
    except Exception as exc:
        raise ValueError(f'Failed to parse "{cfg_path}": {exc}') from exc

    project_meta = _parse_project_section(raw.get("project"), cfg_path, input_abs)
    i18n_cfg: I18nConfig | None = None
    if "i18n" in raw:
        i18n_cfg = _parse_i18n_section(raw["i18n"], project_meta, cfg_path, input_abs)
        if raw.get("project", {}).get("lang") is None:
            project_meta = project_meta.model_copy(update={"lang": i18n_cfg.default_lang})

    return ProjectManifest(project=project_meta, i18n=i18n_cfg)


def find_project_manifest(path: str, max_up: int = 4) -> tuple[str, ProjectManifest] | None:
    """Locate ``drawlib.toml`` in ``path`` or up to ``max_up`` parent directories.

    Args:
        path: File or directory path inside a Drawlib project.
        max_up: Maximum number of ancestor directories to inspect.

    Returns:
        tuple[str, ProjectManifest] | None: ``(project_root_abs, manifest)`` if found, else ``None``.
    """
    abs_path = os.path.abspath(path)
    curr = abs_path if os.path.isdir(abs_path) else os.path.dirname(abs_path)
    for _ in range(max_up + 1):
        manifest = load_project_manifest(curr)
        if manifest is not None:
            return curr, manifest
        parent = os.path.dirname(curr)
        if not parent or parent == curr:
            break
        curr = parent
    return None


def format_project_manifest_toml(
    *,
    name: str,
    project_type: ProjectArchetype,
    style: str = "default",
    lang: str = "en",
    langs: list[str] | None = None,
    title: str = "",
    description: str = "",
) -> str:
    """Serialize a clean, human-readable ``drawlib.toml`` string for ``drawlib init``.

    Args:
        name: Project identifier / base stem.
        project_type: Canonical project archetype.
        style: Selected style preset or CSS path.
        lang: Primary / default canonical language code.
        langs: Optional list of canonical languages; when ``len(langs) > 1``, emits ``[i18n]``.
        title: Optional default title override.
        description: Optional project description.

    Returns:
        str: Formatted TOML text ending with a newline.
    """

    def _esc(val: str) -> str:
        return val.replace("\\", "\\\\").replace('"', '\\"')

    lines = [
        "[project]",
        f'name = "{_esc(name)}"',
        f'type = "{_esc(project_type)}"',
        f'title = "{_esc(title)}"',
        f'description = "{_esc(description)}"',
    ]

    is_multi = langs is not None and len(langs) > 1
    if not is_multi:
        lines.append(f'lang = "{_esc(lang)}"')
    lines.append(f'style = "{_esc(style)}"')

    if is_multi and langs is not None:
        langs_literal = ", ".join(f'"{_esc(lc)}"' for lc in langs)
        lines.extend(
            [
                "",
                "[i18n]",
                f'default_lang = "{_esc(lang)}"',
                f"langs = [{langs_literal}]",
            ]
        )

    return "\n".join(lines) + "\n"
