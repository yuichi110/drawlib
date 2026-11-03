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
import re
import tomllib
import urllib.parse
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from drawlib._templates.langs import normalize_language

PROJECT_MANIFEST_FILENAME = "drawlib.toml"
ProjectArchetype = Literal["images", "doc", "site", "slide", "catalog"]
TwitterCardType = Literal["summary_large_image", "summary"]
_VALID_ARCHETYPES: dict[str, ProjectArchetype] = {
    "images": "images",
    "image": "images",
    "doc": "doc",
    "site": "site",
    "slide": "slide",
    "catalog": "catalog",
}
_I18N_ARCHETYPES: frozenset[str] = frozenset({"doc", "site", "slide", "catalog"})
_SEO_ALLOWED_KEYS: frozenset[str] = frozenset(
    {
        "site_url",
        "og_image",
        "twitter_card",
        "twitter_site",
        "sitemap",
        "robots",
        "llms_txt",
    }
)
_CATALOG_ALLOWED_KEYS: frozenset[str] = frozenset(
    {
        "sidebar_expanded",
        "badge_text",
        "badge_url",
        "repo_url",
        "header_links",
        "breadcrumb_root",
    }
)
_UNSAFE_ATTR_CHARS: tuple[str, ...] = ("\r", "\n", "\x00", '"', "'", "<", ">")
_TWITTER_HANDLE_RE = re.compile(r"^@?[A-Za-z0-9_]{1,30}$")
_SCHEME_PREFIX_RE = re.compile(r"^[A-Za-z][A-Za-z0-9+.-]*:")
_WIN_DRIVE_RE = re.compile(r"^[A-Za-z]:[\\/]")


def _resolve_localized_value(val: str | dict[str, str] | None, lang: str, default_lang: str = "en") -> str:
    """Resolve a plain string or locale-keyed mapping for ``lang`` with ``default_lang`` fallback."""
    if val is None:
        return ""
    if isinstance(val, str):
        return val
    norm_lang = normalize_language(lang)
    if norm_lang in val:
        return val[norm_lang]
    norm_def = normalize_language(default_lang)
    if norm_def in val:
        return val[norm_def]
    return next(iter(val.values()), "")


class ProjectMetadata(BaseModel):
    """Metadata under the ``[project]`` section of ``drawlib.toml``.

    Attributes:
        name: Project identifier / base stem (e.g. ``'quickstart'``, ``'drawlib-dogfooding'``).
        type: Canonical project archetype (``'images'``, ``'doc'``, ``'site'``, ``'slide'``, or ``'catalog'``).
        title: Optional default document/site/slide/catalog title override.
        description: Optional human/agent-facing summary of the project.
        lang: Canonical single-language code for ``images`` projects (``None`` for i18n archetypes).
        style: Style preset theme or CSS path recorded at initialization.
    """

    model_config = ConfigDict(frozen=True)

    name: str
    type: ProjectArchetype
    title: str = ""
    description: str = ""
    lang: str | None = None
    style: str = "default"


class I18nConfig(BaseModel):
    """Parsed locale configuration from the ``[i18n]`` section of ``drawlib.toml``.

    Attributes:
        default_lang: Canonical default language key (e.g. ``'en'``).
        langs: Ordered list of canonical language keys enabled for the project (1 or more locales).
        labels: Optional custom display labels keyed by canonical language code.
        descriptions: Optional localized project descriptions keyed by canonical language code.
    """

    model_config = ConfigDict(frozen=True)

    default_lang: str
    langs: list[str]
    labels: dict[str, str] = Field(default_factory=dict)
    descriptions: dict[str, str] = Field(default_factory=dict)


class SeoConfig(BaseModel):
    """Parsed SEO, Open Graph, and crawler metadata from ``[seo]`` in ``drawlib.toml``.

    Attributes:
        site_url: Canonical public origin/base URL without trailing slash (e.g. ``'https://www.drawlib.com'``).
        og_image: External ``https://`` URL or validated project-relative image path (e.g. ``'_assets/ogp.png'``).
        twitter_card: X/Twitter card layout (``'summary_large_image'`` or ``'summary'``).
        twitter_site: Optional normalized X/Twitter account handle (e.g. ``'@drawlib'``).
        sitemap: Whether to generate ``sitemap.xml`` when ``site_url`` is configured.
        robots: Whether to generate ``robots.txt``.
        llms_txt: Whether to generate ``llms.txt`` (``llmstxt.org`` Markdown index).
    """

    model_config = ConfigDict(frozen=True)

    site_url: str = ""
    og_image: str = ""
    twitter_card: TwitterCardType = "summary_large_image"
    twitter_site: str = ""
    sitemap: bool = True
    robots: bool = True
    llms_txt: bool = True


class CatalogHeaderLink(BaseModel):
    """Single top-bar navigation link configured under ``[catalog].header_links``.

    Attributes:
        label: Link text (either a plain string or localized ``{lang: text}`` mapping).
        url: Destination ``http(s)://`` URL or relative path.
    """

    model_config = ConfigDict(frozen=True)

    label: str | dict[str, str]
    url: str

    def resolve_label(self, lang: str, default_lang: str = "en") -> str:
        """Resolve localized label string for ``lang``."""
        return _resolve_localized_value(self.label, lang, default_lang)

    @property
    def is_external(self) -> bool:
        """Return True if ``url`` is an external ``http://`` or ``https://`` URL."""
        return self.url.lower().startswith(("http://", "https://"))


class CatalogConfig(BaseModel):
    """Parsed configuration from the ``[catalog]`` section of ``drawlib.toml``.

    Attributes:
        sidebar_expanded: Whether all category groups in the left sidebar render open by default.
        breadcrumb_root: Optional root label in the article breadcrumb (plain string or localized mapping).
        badge_text: Optional version/status pill text in the sidebar subbar (plain string or localized mapping).
        badge_url: Optional URL linked from ``badge_text``.
        repo_url: Optional repository ``http(s)://`` URL rendered as an icon link in the sidebar subbar.
        header_links: Optional top-bar right-hand navigation links.
    """

    model_config = ConfigDict(frozen=True)

    sidebar_expanded: bool = True
    breadcrumb_root: str | dict[str, str] | None = None
    badge_text: str | dict[str, str] | None = None
    badge_url: str | None = None
    repo_url: str | None = None
    header_links: tuple[CatalogHeaderLink, ...] = ()

    def resolve_breadcrumb_root(self, lang: str, default_lang: str = "en") -> str:
        """Resolve localized ``breadcrumb_root`` for ``lang`` (empty string if unset)."""
        return _resolve_localized_value(self.breadcrumb_root, lang, default_lang)

    def resolve_badge_text(self, lang: str, default_lang: str = "en") -> str:
        """Resolve localized ``badge_text`` for ``lang`` (empty string if unset)."""
        return _resolve_localized_value(self.badge_text, lang, default_lang)


class ProjectManifest(BaseModel):
    """Validated project manifest parsed from ``drawlib.toml``.

    Attributes:
        project: Core project archetype and metadata from ``[project]``.
        i18n: Locale configuration from ``[i18n]`` (always populated for ``doc``, ``site``, ``slide``, ``catalog``).
        seo: Optional SEO/OGP/crawler configuration from ``[seo]`` (for ``doc``, ``site``, ``slide``, ``catalog``).
        catalog: Catalog & reference layout configuration from ``[catalog]`` (populated for ``catalog`` projects).
    """

    model_config = ConfigDict(frozen=True)

    project: ProjectMetadata
    i18n: I18nConfig | None = None
    seo: SeoConfig | None = None
    catalog: CatalogConfig | None = None

    @property
    def is_i18n(self) -> bool:
        """Return True if this project uses locale ``<lang>/`` subdirectories."""
        return self.i18n is not None

    @property
    def effective_lang(self) -> str:
        """Return default canonical language code for the project."""
        if self.i18n is not None:
            return self.i18n.default_lang
        return self.project.lang or "en"


def _parse_project_section(raw_proj: object, cfg_path: str, input_abs: str) -> ProjectMetadata:
    """Validate and normalize the ``[project]`` table."""
    if not isinstance(raw_proj, dict):
        raise ValueError(f'Invalid "{cfg_path}": missing required "[project]" table.')

    raw_type = raw_proj.get("type")
    if not isinstance(raw_type, str) or raw_type.strip().lower() not in _VALID_ARCHETYPES:
        valid_str = ", ".join(("images", "doc", "site", "slide", "catalog"))
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

    norm_lang: str | None = None
    if norm_type in _I18N_ARCHETYPES:
        if "lang" in raw_proj:
            raise ValueError(
                f'Invalid "{cfg_path}": "[project].lang" is not supported for "{norm_type}" projects; '
                'configure "default_lang" and "langs" under "[i18n]" instead.'
            )
    else:
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


def _parse_i18n_string_map(
    raw_map: object,
    norm_langs: list[str],
    cfg_path: str,
    section_label: str,
) -> dict[str, str]:
    """Validate optional ``[i18n.labels]`` or ``[i18n.descriptions]`` string mapping."""
    if raw_map is None:
        return {}
    if not isinstance(raw_map, dict):
        raise ValueError(f'Invalid "{cfg_path}": "{section_label}" must be a TOML table.')
    parsed: dict[str, str] = {}
    for raw_k, raw_v in raw_map.items():
        if not isinstance(raw_k, str) or not isinstance(raw_v, str) or not raw_v.strip():
            raise ValueError(f'Invalid "{cfg_path}": "{section_label}" entries must be non-empty strings.')
        norm_k = normalize_language(raw_k)
        if norm_k not in norm_langs:
            raise ValueError(
                f'Invalid "{cfg_path}": "{section_label}" key "{norm_k}" is not listed in "[i18n].langs" {norm_langs}.'
            )
        parsed[norm_k] = raw_v.strip()
    return parsed


def _parse_i18n_section(
    raw_i18n: object,
    project_meta: ProjectMetadata,
    cfg_path: str,
    input_abs: str,
) -> I18nConfig:
    """Validate and normalize the ``[i18n]`` table and verify locale directories exist."""
    if not isinstance(raw_i18n, dict):
        raise ValueError(f'Invalid "{cfg_path}": "[i18n]" must be a TOML table.')

    if project_meta.type not in _I18N_ARCHETYPES:
        raise ValueError(
            f'Invalid "{cfg_path}": "[i18n]" is only supported for "doc", "site", "slide", and "catalog" projects, '
            f'not "{project_meta.type}".'
        )

    unknown_keys = sorted(set(raw_i18n.keys()) - {"default_lang", "langs", "labels", "descriptions"})
    if unknown_keys:
        raise ValueError(f'Invalid "{cfg_path}": unknown key(s) {unknown_keys} in "[i18n]".')

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

    labels = _parse_i18n_string_map(raw_i18n.get("labels"), norm_langs, cfg_path, "[i18n.labels]")
    descriptions = _parse_i18n_string_map(
        raw_i18n.get("descriptions"),
        norm_langs,
        cfg_path,
        "[i18n.descriptions]",
    )
    return I18nConfig(
        default_lang=norm_default,
        langs=norm_langs,
        labels=labels,
        descriptions=descriptions,
    )


def _validate_site_url(raw_url: object, cfg_path: str) -> str:
    """Validate and normalize optional ``[seo].site_url``."""
    if not isinstance(raw_url, str):
        raise ValueError(f'Invalid "{cfg_path}": "[seo].site_url" must be a string.')
    cleaned = raw_url.strip()
    if not cleaned:
        return ""
    if any(ch in cleaned for ch in (*_UNSAFE_ATTR_CHARS, " ", "\t")):
        raise ValueError(
            f'Invalid "{cfg_path}": "[seo].site_url" contains unsafe whitespace or quote/angle characters.'
        )
    parsed = urllib.parse.urlsplit(cleaned)
    if parsed.scheme.lower() not in {"http", "https"} or not parsed.netloc:
        raise ValueError(
            f'Invalid "{cfg_path}": "[seo].site_url" must be an absolute http:// or https:// URL, got {raw_url!r}.'
        )
    if parsed.query or parsed.fragment:
        raise ValueError(
            f'Invalid "{cfg_path}": "[seo].site_url" must not contain query parameters or URL fragments.'
        )
    return cleaned.rstrip("/")


def _validate_og_image(raw_og_image: object, cfg_path: str, input_abs: str) -> str:
    """Validate and normalize optional ``[seo].og_image`` as external URL or confined relative asset."""
    if not isinstance(raw_og_image, str):
        raise ValueError(f'Invalid "{cfg_path}": "[seo].og_image" must be a string.')
    cleaned = raw_og_image.strip()
    if not cleaned:
        return ""
    if any(ch in cleaned for ch in _UNSAFE_ATTR_CHARS):
        raise ValueError(f'Invalid "{cfg_path}": "[seo].og_image" contains unsafe characters.')

    lower = cleaned.lower()
    if lower.startswith(("http://", "https://")):
        if any(ws in cleaned for ws in (" ", "\t")):
            raise ValueError(f'Invalid "{cfg_path}": "[seo].og_image" URL must not contain whitespace.')
        parsed = urllib.parse.urlsplit(cleaned)
        if not parsed.netloc:
            raise ValueError(f'Invalid "{cfg_path}": "[seo].og_image" URL is missing host: {raw_og_image!r}.')
        return cleaned

    if (
        cleaned.startswith(("/", "\\"))
        or os.path.isabs(cleaned)
        or _WIN_DRIVE_RE.match(cleaned)
        or _SCHEME_PREFIX_RE.match(cleaned)
    ):
        raise ValueError(
            f'Invalid "{cfg_path}": "[seo].og_image" must be an https:// URL or a project-relative file path, '
            f"got {raw_og_image!r}."
        )

    rel_posix = cleaned.replace("\\", "/")
    real_root = os.path.realpath(input_abs)
    joined_norm = os.path.normpath(os.path.join(input_abs, *rel_posix.split("/")))
    real_target = os.path.realpath(joined_norm)
    try:
        common = os.path.commonpath([real_root, real_target])
    except ValueError as exc:
        raise ValueError(
            f'Invalid "{cfg_path}": "[seo].og_image" must stay within project root "{input_abs}".'
        ) from exc

    if common != real_root or real_target == real_root:
        raise ValueError(
            f'Invalid "{cfg_path}": "[seo].og_image" path traversal outside project root "{input_abs}" is prohibited.'
        )
    if not os.path.isfile(real_target):
        raise ValueError(f'Missing "[seo].og_image" file "{real_target}" required by "{cfg_path}".')

    return os.path.relpath(joined_norm, input_abs).replace(os.sep, "/")


def _parse_seo_section(
    raw_seo: object,
    project_meta: ProjectMetadata,
    cfg_path: str,
    input_abs: str,
) -> SeoConfig:
    """Validate and normalize the ``[seo]`` table."""
    if not isinstance(raw_seo, dict):
        raise ValueError(f'Invalid "{cfg_path}": "[seo]" must be a TOML table.')

    if project_meta.type not in _I18N_ARCHETYPES:
        raise ValueError(
            f'Invalid "{cfg_path}": "[seo]" is only supported for "doc", "site", "slide", and "catalog" projects, '
            f'not "{project_meta.type}".'
        )

    unknown_keys = sorted(set(raw_seo.keys()) - _SEO_ALLOWED_KEYS)
    if unknown_keys:
        raise ValueError(f'Invalid "{cfg_path}": unknown key(s) {unknown_keys} in "[seo]".')

    site_url = _validate_site_url(raw_seo.get("site_url", ""), cfg_path)
    og_image = _validate_og_image(raw_seo.get("og_image", ""), cfg_path, input_abs)

    raw_card = raw_seo.get("twitter_card", "summary_large_image")
    if raw_card not in {"summary_large_image", "summary"}:
        raise ValueError(
            f'Invalid "{cfg_path}": "[seo].twitter_card" must be "summary_large_image" or "summary", '
            f"got {raw_card!r}."
        )
    twitter_card: TwitterCardType = "summary_large_image" if raw_card == "summary_large_image" else "summary"

    raw_twitter_site = raw_seo.get("twitter_site", "")
    if not isinstance(raw_twitter_site, str):
        raise ValueError(f'Invalid "{cfg_path}": "[seo].twitter_site" must be a string.')
    cleaned_handle = raw_twitter_site.strip()
    if cleaned_handle:
        if not _TWITTER_HANDLE_RE.match(cleaned_handle):
            raise ValueError(
                f'Invalid "{cfg_path}": "[seo].twitter_site" must be a valid @handle (1-30 alphanumeric/underscore '
                f"characters), got {raw_twitter_site!r}."
            )
        norm_twitter_site = cleaned_handle if cleaned_handle.startswith("@") else f"@{cleaned_handle}"
    else:
        norm_twitter_site = ""

    bool_flags: dict[str, bool] = {}
    for flag_key in ("sitemap", "robots", "llms_txt"):
        raw_flag = raw_seo.get(flag_key, True)
        if not isinstance(raw_flag, bool):
            raise ValueError(f'Invalid "{cfg_path}": "[seo].{flag_key}" must be a boolean.')
        bool_flags[flag_key] = raw_flag

    return SeoConfig(
        site_url=site_url,
        og_image=og_image,
        twitter_card=twitter_card,
        twitter_site=norm_twitter_site,
        sitemap=bool_flags["sitemap"],
        robots=bool_flags["robots"],
        llms_txt=bool_flags["llms_txt"],
    )


def _validate_nav_url(
    raw_url: object,
    cfg_path: str,
    key_label: str,
    *,
    require_http: bool = False,
) -> str:
    """Validate a navigation link URL against unsafe characters and dangerous schemes."""
    if not isinstance(raw_url, str) or not raw_url.strip():
        raise ValueError(f'Invalid "{cfg_path}": "{key_label}" must be a non-empty URL string.')
    cleaned = raw_url.strip()
    if any(ch in cleaned for ch in (*_UNSAFE_ATTR_CHARS, " ", "\t")):
        raise ValueError(f'Invalid "{cfg_path}": "{key_label}" contains unsafe whitespace or quote/angle characters.')

    lower = cleaned.lower()
    if lower.startswith(("http://", "https://")):
        parsed = urllib.parse.urlsplit(cleaned)
        if not parsed.netloc:
            raise ValueError(f'Invalid "{cfg_path}": "{key_label}" URL is missing host: {raw_url!r}.')
        return cleaned

    if require_http:
        raise ValueError(
            f'Invalid "{cfg_path}": "{key_label}" must be an http:// or https:// URL, got {raw_url!r}.'
        )

    if cleaned.startswith("//") or _WIN_DRIVE_RE.match(cleaned) or _SCHEME_PREFIX_RE.match(cleaned):
        raise ValueError(
            f'Invalid "{cfg_path}": "{key_label}" must be an http(s):// URL or safe relative path, got {raw_url!r}.'
        )

    return cleaned


def _parse_localized_str_or_map(
    raw_val: object,
    norm_langs: list[str] | None,
    cfg_path: str,
    key_label: str,
) -> str | dict[str, str]:
    """Validate a plain non-empty string or locale-keyed ``{lang: text}`` dictionary."""
    if isinstance(raw_val, str):
        cleaned = raw_val.strip()
        if not cleaned:
            raise ValueError(f'Invalid "{cfg_path}": "{key_label}" must be a non-empty string.')
        return cleaned

    if isinstance(raw_val, dict) and len(raw_val) > 0:
        parsed: dict[str, str] = {}
        for raw_k, raw_v in raw_val.items():
            if not isinstance(raw_k, str) or not isinstance(raw_v, str) or not raw_v.strip():
                raise ValueError(f'Invalid "{cfg_path}": "{key_label}" entries must be non-empty strings.')
            norm_k = normalize_language(raw_k)
            if norm_langs is not None and norm_k not in norm_langs:
                raise ValueError(
                    f'Invalid "{cfg_path}": "{key_label}" key "{norm_k}" is not listed in "[i18n].langs" {norm_langs}.'
                )
            parsed[norm_k] = raw_v.strip()
        return parsed

    raise ValueError(
        f'Invalid "{cfg_path}": "{key_label}" must be a non-empty string or locale table {{ en = "...", ... }}.'
    )


def _parse_catalog_header_links(
    raw_links: object,
    norm_langs: list[str] | None,
    cfg_path: str,
) -> tuple[CatalogHeaderLink, ...]:
    """Validate optional ``[catalog].header_links`` list of ``{ label, url }`` tables."""
    if not isinstance(raw_links, list):
        raise ValueError(f'Invalid "{cfg_path}": "[catalog].header_links" must be a list of {{ label, url }} tables.')

    parsed_links: list[CatalogHeaderLink] = []
    for idx, item in enumerate(raw_links):
        item_label = f"[catalog].header_links[{idx}]"
        if not isinstance(item, dict):
            raise ValueError(f'Invalid "{cfg_path}": "{item_label}" must be a table with "label" and "url".')
        extra_item_keys = sorted(set(item.keys()) - {"label", "url"})
        if extra_item_keys:
            raise ValueError(f'Invalid "{cfg_path}": unknown key(s) {extra_item_keys} in "{item_label}".')
        if "label" not in item or "url" not in item:
            raise ValueError(f'Invalid "{cfg_path}": "{item_label}" requires both "label" and "url".')
        lbl = _parse_localized_str_or_map(item["label"], norm_langs, cfg_path, f"{item_label}.label")
        url = _validate_nav_url(item["url"], cfg_path, f"{item_label}.url", require_http=False)
        parsed_links.append(CatalogHeaderLink(label=lbl, url=url))
    return tuple(parsed_links)


def _parse_catalog_section(
    raw_catalog: object,
    project_meta: ProjectMetadata,
    i18n_cfg: I18nConfig | None,
    cfg_path: str,
) -> CatalogConfig:
    """Validate and normalize the ``[catalog]`` table."""
    if not isinstance(raw_catalog, dict):
        raise ValueError(f'Invalid "{cfg_path}": "[catalog]" must be a TOML table.')

    if project_meta.type != "catalog":
        raise ValueError(
            f'Invalid "{cfg_path}": "[catalog]" is only supported for "catalog" projects, not "{project_meta.type}".'
        )

    unknown_keys = sorted(set(raw_catalog.keys()) - _CATALOG_ALLOWED_KEYS)
    if unknown_keys:
        raise ValueError(f'Invalid "{cfg_path}": unknown key(s) {unknown_keys} in "[catalog]".')

    raw_expanded = raw_catalog.get("sidebar_expanded", True)
    if not isinstance(raw_expanded, bool):
        raise ValueError(f'Invalid "{cfg_path}": "[catalog].sidebar_expanded" must be a boolean.')

    norm_langs = i18n_cfg.langs if i18n_cfg is not None else None

    raw_broot = raw_catalog.get("breadcrumb_root")
    breadcrumb_root: str | dict[str, str] | None = None
    if raw_broot is not None and raw_broot != "":
        breadcrumb_root = _parse_localized_str_or_map(raw_broot, norm_langs, cfg_path, "[catalog].breadcrumb_root")

    raw_badge_text = raw_catalog.get("badge_text")
    badge_text: str | dict[str, str] | None = None
    if raw_badge_text is not None and raw_badge_text != "":
        badge_text = _parse_localized_str_or_map(raw_badge_text, norm_langs, cfg_path, "[catalog].badge_text")

    raw_badge_url = raw_catalog.get("badge_url")
    badge_url: str | None = None
    if raw_badge_url is not None and raw_badge_url != "":
        badge_url = _validate_nav_url(raw_badge_url, cfg_path, "[catalog].badge_url", require_http=False)

    raw_repo_url = raw_catalog.get("repo_url")
    repo_url: str | None = None
    if raw_repo_url is not None and raw_repo_url != "":
        repo_url = _validate_nav_url(raw_repo_url, cfg_path, "[catalog].repo_url", require_http=True)

    header_links = _parse_catalog_header_links(raw_catalog.get("header_links", []), norm_langs, cfg_path)

    return CatalogConfig(
        sidebar_expanded=raw_expanded,
        breadcrumb_root=breadcrumb_root,
        badge_text=badge_text,
        badge_url=badge_url,
        repo_url=repo_url,
        header_links=header_links,
    )


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
    if project_meta.type in _I18N_ARCHETYPES:
        if "i18n" not in raw:
            raise ValueError(
                f'Invalid "{cfg_path}": "{project_meta.type}" projects require an "[i18n]" table '
                'defining "default_lang" and "langs".'
            )
        i18n_cfg = _parse_i18n_section(raw["i18n"], project_meta, cfg_path, input_abs)
    elif "i18n" in raw:
        i18n_cfg = _parse_i18n_section(raw["i18n"], project_meta, cfg_path, input_abs)

    seo_cfg: SeoConfig | None = None
    if "seo" in raw:
        seo_cfg = _parse_seo_section(raw["seo"], project_meta, cfg_path, input_abs)

    catalog_cfg: CatalogConfig | None = None
    if "catalog" in raw:
        catalog_cfg = _parse_catalog_section(raw["catalog"], project_meta, i18n_cfg, cfg_path)
    elif project_meta.type == "catalog":
        catalog_cfg = CatalogConfig()

    return ProjectManifest(project=project_meta, i18n=i18n_cfg, seo=seo_cfg, catalog=catalog_cfg)


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
    labels: dict[str, str] | None = None,
    descriptions: dict[str, str] | None = None,
    title: str = "",
    description: str = "",
    seo: SeoConfig | None = None,
    catalog: CatalogConfig | None = None,
    include_seo_comment: bool = True,
) -> str:
    """Serialize a clean, human-readable ``drawlib.toml`` string for ``drawlib init``.

    Args:
        name: Project identifier / base stem.
        project_type: Canonical project archetype.
        style: Selected style preset or CSS path.
        lang: Primary / default canonical language code.
        langs: Ordered list of canonical languages for ``doc``, ``site``, ``slide``, and ``catalog``.
        labels: Optional custom display labels for ``[i18n.labels]``.
        descriptions: Optional localized descriptions for ``[i18n.descriptions]``.
        title: Optional default title override.
        description: Optional project description.
        seo: Optional active ``[seo]`` configuration block.
        catalog: Optional active ``[catalog]`` configuration block for ``catalog`` projects.
        include_seo_comment: If True and ``seo`` is None, append a commented ``[seo]`` template on web projects.

    Returns:
        str: Formatted TOML text ending with a newline.
    """

    def _esc(val: str) -> str:
        return val.replace("\\", "\\\\").replace('"', '\\"')

    def _fmt_loc(val: str | dict[str, str]) -> str:
        if isinstance(val, str):
            return f'"{_esc(val)}"'
        pairs = ", ".join(f'{_esc(k)} = "{_esc(v)}"' for k, v in val.items())
        return f"{{ {pairs} }}"

    lines = [
        "[project]",
        f'name = "{_esc(name)}"',
        f'type = "{_esc(project_type)}"',
        f'title = "{_esc(title)}"',
        f'description = "{_esc(description)}"',
    ]

    if project_type not in _I18N_ARCHETYPES:
        lines.append(f'lang = "{_esc(lang)}"')
    lines.append(f'style = "{_esc(style)}"')

    if project_type in _I18N_ARCHETYPES:
        eff_langs = langs if langs else [lang]
        langs_literal = ", ".join(f'"{_esc(lc)}"' for lc in eff_langs)
        lines.extend(
            [
                "",
                "[i18n]",
                f'default_lang = "{_esc(lang)}"',
                f"langs = [{langs_literal}]",
            ]
        )
        if labels:
            lines.extend(["", "[i18n.labels]"])
            for lc, lbl in labels.items():
                lines.append(f'{_esc(lc)} = "{_esc(lbl)}"')
        if descriptions:
            lines.extend(["", "[i18n.descriptions]"])
            for lc, desc in descriptions.items():
                lines.append(f'{_esc(lc)} = "{_esc(desc)}"')

        if project_type == "catalog":
            eff_catalog = catalog or CatalogConfig()
            lines.extend(
                [
                    "",
                    "[catalog]",
                    f"sidebar_expanded = {str(eff_catalog.sidebar_expanded).lower()}",
                ]
            )
            if eff_catalog.breadcrumb_root is not None:
                lines.append(f"breadcrumb_root = {_fmt_loc(eff_catalog.breadcrumb_root)}")
            else:
                lines.append('# breadcrumb_root = "Catalog"')
            if eff_catalog.badge_text is not None:
                lines.append(f"badge_text = {_fmt_loc(eff_catalog.badge_text)}")
            else:
                lines.append('# badge_text = "Catalog · v1.0"')
            if eff_catalog.badge_url is not None:
                lines.append(f'badge_url = "{_esc(eff_catalog.badge_url)}"')
            else:
                lines.append('# badge_url = "index.html"')
            if eff_catalog.repo_url is not None:
                lines.append(f'repo_url = "{_esc(eff_catalog.repo_url)}"')
            else:
                lines.append('# repo_url = "https://github.com/org/repo"')
            if eff_catalog.header_links:
                lines.append("header_links = [")
                for hlink in eff_catalog.header_links:
                    lines.append(f'    {{ label = {_fmt_loc(hlink.label)}, url = "{_esc(hlink.url)}" }},')
                lines.append("]")
            else:
                lines.extend(
                    [
                        "# header_links = [",
                        '#     { label = "Docs", url = "https://example.com/docs" },',
                        "# ]",
                    ]
                )

        if seo is not None:
            lines.extend(
                [
                    "",
                    "[seo]",
                    f'site_url = "{_esc(seo.site_url)}"',
                    f'og_image = "{_esc(seo.og_image)}"',
                    f'twitter_card = "{_esc(seo.twitter_card)}"',
                ]
            )
            if seo.twitter_site:
                lines.append(f'twitter_site = "{_esc(seo.twitter_site)}"')
            lines.extend(
                [
                    f"sitemap = {str(seo.sitemap).lower()}",
                    f"robots = {str(seo.robots).lower()}",
                    f"llms_txt = {str(seo.llms_txt).lower()}",
                ]
            )
        elif include_seo_comment:
            lines.extend(
                [
                    "",
                    "# [seo]",
                    '# site_url = "https://example.com"',
                    '# og_image = "_assets/ogp.png"',
                    '# twitter_card = "summary_large_image"',
                    "# sitemap = true",
                    "# robots = true",
                    "# llms_txt = true",
                ]
            )

    return "\n".join(lines) + "\n"



