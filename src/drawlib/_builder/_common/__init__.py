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
    CatalogConfig,
    CatalogHeaderLink,
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
from drawlib._builder._common.parallel import (
    DEFAULT_AUTO_MAX_WORKERS,
    ENV_BUILD_WORKERS,
    BlockRenderJob,
    BlockRenderResult,
    ParallelRenderProgress,
    ScriptRenderJob,
    ScriptRenderResult,
    ScriptSavedFile,
    WorkersSpec,
    build_block_render_job,
    collect_docx_chapter_block_jobs,
    collect_standard_document_block_jobs,
    compute_processor_config_hash,
    execute_scripts_parallel,
    prerender_document_blocks,
    resolve_build_workers,
    resolve_processor_project_root,
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
    "DEFAULT_AUTO_MAX_WORKERS",
    "ENV_BUILD_WORKERS",
    "PROJECT_MANIFEST_FILENAME",
    "BlockRenderJob",
    "BlockRenderResult",
    "BuildImageCache",
    "CatalogConfig",
    "CatalogHeaderLink",
    "CliImageCache",
    "FileBuildProgress",
    "I18nConfig",
    "LlmsLink",
    "LlmsSection",
    "PageSeoMetadata",
    "ParallelRenderProgress",
    "ProjectArchetype",
    "ProjectManifest",
    "ProjectMetadata",
    "ScriptRenderJob",
    "ScriptRenderResult",
    "ScriptSavedFile",
    "SeoConfig",
    "SitemapEntry",
    "TwitterCardType",
    "WorkersSpec",
    "build_block_render_job",
    "build_page_seo_metadata",
    "clear_cache",
    "clear_image_cache",
    "collect_docx_chapter_block_jobs",
    "collect_standard_document_block_jobs",
    "compute_processor_config_hash",
    "download_cache",
    "ensure_seo_og_image_copied",
    "ensure_static_office_image",
    "execute_scripts_parallel",
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
    "prerender_document_blocks",
    "render_seo_head_tags",
    "resolve_build_workers",
    "resolve_localized_description",
    "resolve_office_datetime",
    "resolve_og_image_url",
    "resolve_processor_project_root",
    "resolve_public_page_url",
    "resolve_styles_and_utils",
    "to_og_locale",
    "upgrade_alternate_links",
    "write_llms_txt",
    "write_robots_txt",
    "write_sitemap_xml",
]
