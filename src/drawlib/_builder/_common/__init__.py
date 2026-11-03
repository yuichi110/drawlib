# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Common infrastructure and utilities for drawlib builders."""

from __future__ import annotations

from drawlib._builder._common.browser import (
    import_sync_playwright,
    install_headless_chromium,
    launch_headless_chromium,
)
from drawlib._builder._common.cache import (
    BuildImageCache,
    CliImageCache,
    hash_file,
    hash_text,
)
from drawlib._builder._common.cache_manager import (
    clear_cache,
    clear_image_cache,
    download_cache,
    list_cache,
)
from drawlib._builder._common.manifest import (
    PROJECT_MANIFEST_FILENAME,
    ApiConfig,
    ApiHeaderLink,
    I18nConfig,
    ProjectArchetype,
    ProjectManifest,
    ProjectMetadata,
    SeoConfig,
    TwitterCardType,
    find_project_manifest,
    format_project_manifest_toml,
    load_project_manifest,
)
from drawlib._builder._common.office import (
    ensure_static_office_image,
    normalize_opc_zip_timestamps,
    resolve_office_datetime,
)
from drawlib._builder._common.progress import (
    BAR_WIDTH,
    FileBuildProgress,
    format_duplicate_output_error,
    format_progress_line,
)
from drawlib._builder._common.seo import (
    LlmsLink,
    LlmsSection,
    PageSeoMetadata,
    SitemapEntry,
    build_page_seo_metadata,
    ensure_seo_og_image_copied,
    extract_markdown_description,
    render_seo_head_tags,
    resolve_localized_description,
    resolve_og_image_url,
    resolve_public_page_url,
    to_og_locale,
    upgrade_alternate_links,
    write_llms_txt,
    write_robots_txt,
    write_sitemap_xml,
)
from drawlib._builder._common.styles_loader import (
    load_styles,
    load_styles_and_utils,
    load_utils,
    resolve_styles_and_utils,
)

__all__ = [
    "BAR_WIDTH",
    "PROJECT_MANIFEST_FILENAME",
    "ApiConfig",
    "ApiHeaderLink",
    "BuildImageCache",
    "CliImageCache",
    "FileBuildProgress",
    "I18nConfig",
    "LlmsLink",
    "LlmsSection",
    "PageSeoMetadata",
    "ProjectArchetype",
    "ProjectManifest",
    "ProjectMetadata",
    "SeoConfig",
    "SitemapEntry",
    "TwitterCardType",
    "build_page_seo_metadata",
    "clear_cache",
    "clear_image_cache",
    "download_cache",
    "ensure_seo_og_image_copied",
    "ensure_static_office_image",
    "extract_markdown_description",
    "find_project_manifest",
    "format_duplicate_output_error",
    "format_progress_line",
    "format_project_manifest_toml",
    "hash_file",
    "hash_text",
    "import_sync_playwright",
    "install_headless_chromium",
    "launch_headless_chromium",
    "list_cache",
    "load_project_manifest",
    "load_styles",
    "load_styles_and_utils",
    "load_utils",
    "normalize_opc_zip_timestamps",
    "render_seo_head_tags",
    "resolve_localized_description",
    "resolve_og_image_url",
    "resolve_office_datetime",
    "resolve_public_page_url",
    "resolve_styles_and_utils",
    "to_og_locale",
    "upgrade_alternate_links",
    "write_llms_txt",
    "write_robots_txt",
    "write_sitemap_xml",
]
