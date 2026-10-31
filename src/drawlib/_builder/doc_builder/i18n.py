# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Multi-locale (i18n) configuration, parity validation, and link helpers for site projects."""

from __future__ import annotations

import os
import re
import tomllib
from dataclasses import dataclass
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict

from drawlib._builder.doc_builder.detector import preserve_outer_fences
from drawlib._builder.doc_builder.navbar import NavbarItem, NavbarSection, parse_navbar_markdown
from drawlib._builder.doc_builder.processor.options import parse_block_info
from drawlib._builder.doc_builder.processor.parser import extract_code_blocks
from drawlib._templates.langs import get_language_config, normalize_language

I18N_CONFIG_FILENAME = "i18n.toml"

_IGNORED_DOC_FILENAMES: frozenset[str] = frozenset(
    {
        "readme.md",
        "readme.markdown",
        "output_readme.md",
        "output_html_readme.md",
        "navbar.md",
        "navbar.markdown",
        "template.html",
        "template.html.j2",
    }
)

_PRESERVED_FENCE_RE = re.compile(r"^__DRAWLIB_PRESERVED_FENCE_(\d+)__\r?$")
_PRESERVED_PAD_RE = re.compile(r"^__DRAWLIB_FENCE_PAD_\d+_\d+__\r?$")
_OUTER_FENCE_INFO_RE = re.compile(r"^[ \t]{0,3}(?:`{4,}|~{4,})([^\n\r]*)")
_FENCE_OPEN_RE = re.compile(r"^[ \t]{0,3}(`{3}|~{3})([^\n\r]*)$")
_HEADING_1_TO_3_RE = re.compile(r"^[ \t]{0,3}(#{1,3})[ \t]+(.+?)[ \t]*#*[ \t\r]*$")
_SKIP_URL_PREFIXES: tuple[str, ...] = ("http://", "https://", "//", "mailto:", "javascript:", "data:", "#")


class I18nConfig(BaseModel):
    """Parsed multi-locale site configuration from ``i18n.toml``.

    Attributes:
        default_lang: Canonical default language key (e.g. ``'en'``).
        langs: Ordered list of canonical language keys enabled for the site (e.g. ``['en', 'ja']``).
    """

    model_config = ConfigDict(frozen=True)

    default_lang: str
    langs: list[str]


@dataclass(frozen=True)
class HeadingToken:
    """Heading skeleton token (H1-H3) in a Markdown document."""

    line_number: int
    level: int
    kind: Literal["heading"] = "heading"

    def describe(self) -> str:
        """Return human-readable token summary for parity error messages."""
        return f"Heading(H{self.level})"


@dataclass(frozen=True)
class MarkdownTextToken:
    """Collapsed prose/list/table/blockquote region token in a Markdown document."""

    line_number: int
    kind: Literal["markdown_text"] = "markdown_text"

    def describe(self) -> str:
        """Return human-readable token summary for parity error messages."""
        return "MarkdownText"


@dataclass(frozen=True)
class DrawlibBlockToken:
    """Executable ``drawlib`` code block skeleton token in a Markdown document."""

    line_number: int
    file_name: str
    code: str
    code_mode: str
    align: str | None
    has_caption: bool
    kind: Literal["drawlib_block"] = "drawlib_block"

    def describe(self) -> str:
        """Return human-readable token summary for parity error messages."""
        return f"DrawlibBlock(file={self.file_name}, code={self.code_mode})"


@dataclass(frozen=True)
class CodeBlockToken:
    """Standard fenced code block skeleton token in a Markdown document."""

    line_number: int
    lang: str
    kind: Literal["code_block"] = "code_block"

    def describe(self) -> str:
        """Return human-readable token summary for parity error messages."""
        label = self.lang or "plain"
        return f"CodeBlock({label})"


SkeletonToken = HeadingToken | MarkdownTextToken | DrawlibBlockToken | CodeBlockToken


def load_i18n_config(input_dir: str) -> I18nConfig | None:
    """Load and validate ``i18n.toml`` from ``input_dir`` if present.

    Args:
        input_dir: Root source directory of a documentation project.

    Returns:
        I18nConfig | None: Validated multi-locale config, or ``None`` if ``i18n.toml`` is absent.

    Raises:
        ValueError: If ``i18n.toml`` is malformed, specifies unsupported languages, or lacks directories.
    """
    input_abs = os.path.abspath(input_dir)
    cfg_path = os.path.join(input_abs, I18N_CONFIG_FILENAME)
    if not os.path.isfile(cfg_path):
        return None

    try:
        with open(cfg_path, "rb") as f:
            raw = tomllib.load(f)
    except Exception as exc:
        raise ValueError(f'Failed to parse "{cfg_path}": {exc}') from exc

    raw_default = raw.get("default_lang")
    raw_langs = raw.get("langs")
    if not isinstance(raw_default, str) or not raw_default.strip():
        raise ValueError(f'Invalid "{cfg_path}": "default_lang" must be a non-empty string.')
    if not isinstance(raw_langs, list) or len(raw_langs) == 0 or not all(isinstance(x, str) for x in raw_langs):
        raise ValueError(f'Invalid "{cfg_path}": "langs" must be a non-empty list of language code strings.')

    norm_default = normalize_language(raw_default)
    norm_langs: list[str] = []
    for code in raw_langs:
        norm_code = normalize_language(code)
        if norm_code in norm_langs:
            raise ValueError(f'Invalid "{cfg_path}": duplicate language "{norm_code}" in "langs".')
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


def resolve_locale_navbar_path(lang_dir_abs: str) -> str | None:
    """Return absolute path to ``navbar.md`` (or ``navbar.markdown``) inside a locale directory if present."""
    for name in ("navbar.md", "navbar.markdown"):
        cand = os.path.join(lang_dir_abs, name)
        if os.path.isfile(cand):
            return cand
    return None


def collect_locale_doc_files(lang_dir_abs: str, *, markdown_only: bool = False) -> list[str]:
    """Collect sorted POSIX-style relative document paths inside a locale directory.

    Args:
        lang_dir_abs: Absolute path to ``<input_dir>/<lang>``.
        markdown_only: If True, collect only ``.md``/``.markdown`` files; otherwise include ``.html``/``.htm``.

    Returns:
        list[str]: Sorted relative file paths using ``/`` separators (e.g. ``'index.md'``).
    """
    exts = (".md", ".markdown") if markdown_only else (".md", ".markdown", ".html", ".htm")
    collected: list[str] = []
    for root, dirnames, files in os.walk(lang_dir_abs):
        dirnames[:] = sorted(d for d in dirnames if not d.startswith(".") and not d.startswith("_"))
        for fname in sorted(files):
            if fname.startswith(".") or fname.startswith("_"):
                continue
            if fname.lower() in _IGNORED_DOC_FILENAMES:
                continue
            if fname.lower().endswith(exts):
                src_abs = os.path.join(root, fname)
                rel = os.path.relpath(src_abs, lang_dir_abs).replace(os.sep, "/")
                collected.append(rel)
    return sorted(collected)


def _normalize_block_filename(raw_file: str | None, fmt_opt: str | None, default_format: str, index: int) -> str:
    """Resolve canonical output filename for a drawlib block."""
    eff_fmt = fmt_opt if fmt_opt in {"png", "webp", "svg", "apng"} else default_format
    ext = eff_fmt if eff_fmt in {"svg", "webp", "apng"} else "png"
    if raw_file:
        cleaned = raw_file.strip()
        _, file_ext = os.path.splitext(cleaned)
        if file_ext.lower() in {".png", ".webp", ".svg", ".apng"}:
            return cleaned
        return f"{cleaned}.{ext}"
    return f"{index}.{ext}"


def _strip_html_comments(text: str) -> str:
    """Replace HTML comments with spaces while preserving exact line breaks and line numbers."""
    return re.sub(
        r"<!--.*?-->",
        lambda m: re.sub(r"[^\n]", " ", m.group(0)),
        text,
        flags=re.DOTALL,
    )


def _consume_fenced_block(
    lines: list[str],
    start_idx: int,
    fence_char: str,
    info_raw: str,
    block_counter: int,
    default_format: str,
) -> tuple[SkeletonToken, int, int]:
    """Consume a 3-char fenced block starting at ``start_idx`` and return (token, next_idx, block_counter)."""
    start_line = start_idx + 1
    close_re = re.compile(rf"^[ \t]{{0,3}}{re.escape(fence_char)}{{3,}}[ \t\r]*$")
    idx = start_idx + 1
    body_lines: list[str] = []
    while idx < len(lines) and not close_re.match(lines[idx]):
        body_lines.append(lines[idx])
        idx += 1

    info = info_raw.strip()
    is_drawlib = info.lower() == "drawlib" or info.lower().startswith(("drawlib ", "drawlib\t"))
    if is_drawlib:
        block_counter += 1
        opt_str = info[len("drawlib") :].strip()
        opts = parse_block_info(opt_str)
        fn = _normalize_block_filename(opts.file, opts.format, default_format, block_counter)
        norm_code = "\n".join(line.rstrip("\r") for line in body_lines).strip()
        token: SkeletonToken = DrawlibBlockToken(
            line_number=start_line,
            file_name=fn,
            code=norm_code,
            code_mode=opts.code,
            align=opts.align,
            has_caption=bool(opts.caption),
        )
        return token, idx + 1, block_counter

    lang_tag = info.split()[0].lower() if info else ""
    return CodeBlockToken(line_number=start_line, lang=lang_tag), idx + 1, block_counter


def extract_markdown_skeleton(content: str, default_format: str = "png") -> list[SkeletonToken]:
    """Extract ordered structural skeleton tokens from a Markdown document.

    Consecutive paragraphs, bullet lists, tables, blockquotes, horizontal rules, and H4+
    subheadings collapse into a single ``MarkdownTextToken`` so natural translation phrasing
    never causes false positives while missing prose sections, headings, or code blocks are caught.

    Args:
        content: Raw Markdown file content.
        default_format: Default image extension when ``format=``/file extension is omitted.

    Returns:
        list[SkeletonToken]: Ordered sequence of structural skeleton tokens.
    """
    masked_text, preserved = preserve_outer_fences(content)
    cleaned_text = _strip_html_comments(masked_text)
    lines = cleaned_text.split("\n")

    tokens: list[SkeletonToken] = []
    pending_text_line: int | None = None
    block_counter = 0
    idx = 0

    def flush_text() -> None:
        nonlocal pending_text_line
        if pending_text_line is not None:
            tokens.append(MarkdownTextToken(line_number=pending_text_line))
            pending_text_line = None

    while idx < len(lines):
        line = lines[idx]
        line_no = idx + 1

        if _PRESERVED_PAD_RE.match(line):
            idx += 1
            continue

        m_pres = _PRESERVED_FENCE_RE.match(line)
        if m_pres:
            flush_text()
            fence_id = int(m_pres.group(1))
            orig_open = preserved[fence_id][1][0] if fence_id < len(preserved) else ""
            m_info = _OUTER_FENCE_INFO_RE.match(orig_open)
            raw_tag = m_info.group(1).strip() if m_info else ""
            lang_tag = raw_tag.split()[0].lower() if raw_tag else ""
            tokens.append(CodeBlockToken(line_number=line_no, lang=lang_tag))
            idx += 1
            continue

        m_fence = _FENCE_OPEN_RE.match(line)
        if m_fence:
            flush_text()
            tok, next_idx, block_counter = _consume_fenced_block(
                lines=lines,
                start_idx=idx,
                fence_char=m_fence.group(1)[0],
                info_raw=m_fence.group(2),
                block_counter=block_counter,
                default_format=default_format,
            )
            tokens.append(tok)
            idx = next_idx
            continue

        m_heading = _HEADING_1_TO_3_RE.match(line)
        if m_heading:
            flush_text()
            tokens.append(HeadingToken(line_number=line_no, level=len(m_heading.group(1))))
            idx += 1
            continue

        if line.strip():
            if pending_text_line is None:
                pending_text_line = line_no
        idx += 1

    flush_text()
    return tokens


def _check_file_set_parity(
    input_abs: str,
    default_lang: str,
    default_files: list[str],
    default_has_navbar: bool,
    lang: str,
) -> list[str]:
    """Validate Check 1: File set parity and navbar presence between default_lang and lang."""
    lang_dir = os.path.join(input_abs, lang)
    lang_has_navbar = resolve_locale_navbar_path(lang_dir) is not None
    if default_has_navbar != lang_has_navbar:
        raise ValueError(
            f'[i18n navbar parity error] Locale "{lang}" navbar.md presence ({lang_has_navbar}) '
            f'does not match default_lang "{default_lang}" ({default_has_navbar}).'
        )

    lang_files = collect_locale_doc_files(lang_dir)
    def_set = set(default_files)
    lang_set = set(lang_files)
    missing = sorted(def_set - lang_set)
    extra = sorted(lang_set - def_set)
    if missing or extra:
        details: list[str] = []
        if missing:
            details.append("  Missing files in " + f'"{lang}/": ' + ", ".join(missing))
        if extra:
            details.append("  Extra files in " + f'"{lang}/": ' + ", ".join(extra))
        joined = "\n".join(details)
        raise ValueError(
            f'[i18n file parity error] Locale "{lang}/" does not match "{default_lang}/":\n{joined}'
        )
    return lang_files


def _navbar_item_target_key(item: NavbarItem, lang_dir_abs: str) -> tuple[bool, str, str]:
    """Normalize a NavbarItem destination into a language-neutral comparison tuple."""
    if item.is_external:
        return (True, item.url, "")
    if item.target_file_abs is None:
        return (False, "", item.anchor)
    rel_target = os.path.relpath(item.target_file_abs, lang_dir_abs).replace(os.sep, "/")
    return (False, rel_target, item.anchor)


def _check_navbar_parity(
    default_lang: str,
    default_dir: str,
    default_sections: list[NavbarSection],
    lang: str,
    lang_dir: str,
    lang_navbar_path: str,
) -> None:
    """Validate Check 2: navbar.md section structure and link target parity."""
    lang_sections, _ = parse_navbar_markdown(lang_navbar_path, lang_dir)
    if len(lang_sections) != len(default_sections):
        raise ValueError(
            f'[i18n navbar parity error] "{lang}/navbar.md" has {len(lang_sections)} section(s), '
            f'expected {len(default_sections)} to match "{default_lang}/navbar.md".'
        )

    for sec_idx, (def_sec, lang_sec) in enumerate(zip(default_sections, lang_sections), start=1):
        if (def_sec.title is not None) != (lang_sec.title is not None):
            raise ValueError(
                f'[i18n navbar parity error] Section #{sec_idx} heading presence in "{lang}/navbar.md" '
                f'does not match "{default_lang}/navbar.md".'
            )
        if len(lang_sec.items) != len(def_sec.items):
            raise ValueError(
                f'[i18n navbar parity error] Section #{sec_idx} in "{lang}/navbar.md" has '
                f'{len(lang_sec.items)} link(s), expected {len(def_sec.items)} to match "{default_lang}/navbar.md".'
            )
        for item_idx, (def_item, lang_item) in enumerate(zip(def_sec.items, lang_sec.items), start=1):
            def_key = _navbar_item_target_key(def_item, default_dir)
            lang_key = _navbar_item_target_key(lang_item, lang_dir)
            if def_key != lang_key:
                raise ValueError(
                    f'[i18n navbar parity error] Link #{item_idx} in section #{sec_idx} of "{lang}/navbar.md" '
                    f'points to "{lang_item.url}", expected target matching "{def_item.url}" '
                    f'in "{default_lang}/navbar.md".'
                )


def _first_diff_line_hint(def_code: str, lang_code: str) -> str:
    """Return a concise 1-based line hint indicating where two code strings diverge."""
    def_lines = def_code.splitlines()
    lang_lines = lang_code.splitlines()
    for idx, (d_line, l_line) in enumerate(zip(def_lines, lang_lines), start=1):
        if d_line != l_line:
            return f"first difference at block line {idx}: expected {d_line!r}, got {l_line!r}"
    return f"line count differs ({len(def_lines)} vs {len(lang_lines)} lines)"


def _validate_drawlib_block_pair(
    rel_path: str,
    default_lang: str,
    lang: str,
    def_tok: DrawlibBlockToken,
    lang_tok: DrawlibBlockToken,
) -> None:
    """Validate Check 4: DrawlibBlock options, filename convention, and code parity."""
    if (
        def_tok.code_mode != lang_tok.code_mode
        or def_tok.align != lang_tok.align
        or def_tok.has_caption != lang_tok.has_caption
    ):
        raise ValueError(
            f'[i18n skeleton parity error] Drawlib block attributes mismatch in "{lang}/{rel_path}" '
            f"(line {lang_tok.line_number}) vs \"{default_lang}/{rel_path}\" (line {def_tok.line_number}): "
            f"expected (code={def_tok.code_mode}, align={def_tok.align}, has_caption={def_tok.has_caption}), "
            f"got (code={lang_tok.code_mode}, align={lang_tok.align}, has_caption={lang_tok.has_caption})."
        )

    def_stem, def_ext = os.path.splitext(def_tok.file_name)
    lang_underscore = lang.replace("-", "_")
    allowed_localized = {
        f"{def_stem}_{lang}{def_ext}",
        f"{def_stem}_{lang_underscore}{def_ext}",
    }

    if lang_tok.file_name == def_tok.file_name:
        if lang_tok.code != def_tok.code:
            hint = _first_diff_line_hint(def_tok.code, lang_tok.code)
            suggested = f"{def_stem}_{lang}{def_ext}"
            raise ValueError(
                f'[i18n drawlib code parity error] Shared image "{def_tok.file_name}" has different Python code '
                f'in "{lang}/{rel_path}" (line {lang_tok.line_number}) vs "{default_lang}/{rel_path}" '
                f"(line {def_tok.line_number}; {hint}). "
                f'Keep shared diagram code identical, or use localized filename "file={suggested}".'
            )
        return

    if lang_tok.file_name in allowed_localized:
        return

    suggested = f"{def_stem}_{lang}{def_ext}"
    raise ValueError(
        f'[i18n drawlib filename error] Unexpected image file "{lang_tok.file_name}" in "{lang}/{rel_path}" '
        f'(line {lang_tok.line_number}) at position of "{def_tok.file_name}" in "{default_lang}/{rel_path}" '
        f'(line {def_tok.line_number}). Expected "{def_tok.file_name}" (shared) or "{suggested}" (localized).'
    )


def _tokens_match_structure(def_tok: SkeletonToken, lang_tok: SkeletonToken) -> bool:
    """Return True if two skeleton tokens represent the same structural element."""
    if type(def_tok) is not type(lang_tok):
        return False
    if isinstance(def_tok, HeadingToken) and isinstance(lang_tok, HeadingToken):
        return def_tok.level == lang_tok.level
    if isinstance(def_tok, CodeBlockToken) and isinstance(lang_tok, CodeBlockToken):
        return def_tok.lang == lang_tok.lang
    return True


def _check_markdown_page_parity(
    input_abs: str,
    rel_path: str,
    default_lang: str,
    lang: str,
    default_tokens: list[SkeletonToken],
    default_format: str,
) -> None:
    """Validate Check 3 (Skeleton Sequence) and Check 4 (Drawlib Code) for a single Markdown page."""
    lang_file_abs = os.path.join(input_abs, lang, rel_path)
    with open(lang_file_abs, "r", encoding="utf-8") as f:
        lang_content = f.read()

    lang_tokens = extract_markdown_skeleton(lang_content, default_format=default_format)
    for idx, (def_tok, lang_tok) in enumerate(zip(default_tokens, lang_tokens), start=1):
        if not _tokens_match_structure(def_tok, lang_tok):
            raise ValueError(
                f'[i18n skeleton parity error] Structural mismatch at element #{idx} in "{lang}/{rel_path}" '
                f'(line {lang_tok.line_number}) vs "{default_lang}/{rel_path}" (line {def_tok.line_number}): '
                f"expected {def_tok.describe()}, got {lang_tok.describe()}."
            )
        if isinstance(def_tok, DrawlibBlockToken) and isinstance(lang_tok, DrawlibBlockToken):
            _validate_drawlib_block_pair(rel_path, default_lang, lang, def_tok, lang_tok)

    if len(lang_tokens) != len(default_tokens):
        if len(lang_tokens) < len(default_tokens):
            missing_tok = default_tokens[len(lang_tokens)]
            raise ValueError(
                f'[i18n skeleton parity error] "{lang}/{rel_path}" ended early (has {len(lang_tokens)} elements, '
                f'expected {len(default_tokens)}): missing {missing_tok.describe()} from '
                f'"{default_lang}/{rel_path}" (line {missing_tok.line_number}).'
            )
        extra_tok = lang_tokens[len(default_tokens)]
        raise ValueError(
            f'[i18n skeleton parity error] "{lang}/{rel_path}" has extra {extra_tok.describe()} at '
            f'line {extra_tok.line_number} (has {len(lang_tokens)} elements, expected {len(default_tokens)} '
            f'to match "{default_lang}/{rel_path}").'
        )


def _check_html_page_parity(
    input_abs: str,
    rel_path: str,
    default_lang: str,
    lang: str,
    default_content: str,
    default_format: str,
) -> None:
    """Validate drawlib script block count and code parity for raw HTML pages."""
    lang_file_abs = os.path.join(input_abs, lang, rel_path)
    with open(lang_file_abs, "r", encoding="utf-8") as f:
        lang_content = f.read()

    def_blocks = extract_code_blocks(default_content, is_html=True)
    lang_blocks = extract_code_blocks(lang_content, is_html=True)
    if len(def_blocks) != len(lang_blocks):
        raise ValueError(
            f'[i18n skeleton parity error] "{lang}/{rel_path}" has {len(lang_blocks)} drawlib block(s), '
            f'expected {len(def_blocks)} to match "{default_lang}/{rel_path}".'
        )
    for def_b, lang_b in zip(def_blocks, lang_blocks):
        def_tok = DrawlibBlockToken(
            line_number=def_b.line_number,
            file_name=_normalize_block_filename(def_b.options.file, def_b.options.format, default_format, def_b.index),
            code=def_b.code.strip(),
            code_mode=def_b.options.code,
            align=def_b.options.align,
            has_caption=bool(def_b.options.caption),
        )
        lang_tok = DrawlibBlockToken(
            line_number=lang_b.line_number,
            file_name=_normalize_block_filename(
                lang_b.options.file, lang_b.options.format, default_format, lang_b.index
            ),
            code=lang_b.code.strip(),
            code_mode=lang_b.options.code,
            align=lang_b.options.align,
            has_caption=bool(lang_b.options.caption),
        )
        _validate_drawlib_block_pair(rel_path, default_lang, lang, def_tok, lang_tok)


def validate_i18n_site(
    input_dir: str,
    config: I18nConfig,
    default_format: str = "png",
) -> dict[str, list[str]]:
    """Run all 4 mechanical consistency checks across every locale in ``config``.

    Checks performed:
    1. File set parity across ``<input_dir>/<lang>/``.
    2. ``navbar.md`` section and link target parity.
    3. Markdown skeleton sequence parity (``H1..H3``, ``MarkdownText``, ``DrawlibBlock``, ``CodeBlock``).
    4. ``DrawlibBlock`` Python code parity (exact match for shared filenames, ``<stem>_<lang>.<ext>`` for localized).

    Args:
        input_dir: Root source directory containing ``i18n.toml``.
        config: Loaded ``I18nConfig`` instance.
        default_format: Default image output format (``'png'`` or ``'webp'``).

    Returns:
        dict[str, list[str]]: Mapping from ``lang`` to sorted relative document paths.

    Raises:
        ValueError: If any consistency check fails.
    """
    input_abs = os.path.abspath(input_dir)
    default_lang = config.default_lang
    default_dir = os.path.join(input_abs, default_lang)

    default_files = collect_locale_doc_files(default_dir)
    if not default_files:
        raise ValueError(f'No Markdown or HTML documentation files found in "{default_dir}".')

    default_navbar_path = resolve_locale_navbar_path(default_dir)
    default_sections: list[NavbarSection] = []
    if default_navbar_path is not None:
        default_sections, _ = parse_navbar_markdown(default_navbar_path, default_dir)

    locale_files: dict[str, list[str]] = {default_lang: default_files}
    other_langs = [lang for lang in config.langs if lang != default_lang]

    for lang in other_langs:
        locale_files[lang] = _check_file_set_parity(
            input_abs=input_abs,
            default_lang=default_lang,
            default_files=default_files,
            default_has_navbar=(default_navbar_path is not None),
            lang=lang,
        )

    if default_navbar_path is not None:
        for lang in other_langs:
            lang_dir = os.path.join(input_abs, lang)
            lang_navbar = resolve_locale_navbar_path(lang_dir)
            if lang_navbar is not None:
                _check_navbar_parity(
                    default_lang=default_lang,
                    default_dir=default_dir,
                    default_sections=default_sections,
                    lang=lang,
                    lang_dir=lang_dir,
                    lang_navbar_path=lang_navbar,
                )

    for rel_path in default_files:
        def_file_abs = os.path.join(default_dir, rel_path)
        with open(def_file_abs, "r", encoding="utf-8") as f:
            def_content = f.read()

        if rel_path.lower().endswith((".md", ".markdown")):
            def_tokens = extract_markdown_skeleton(def_content, default_format=default_format)
            for lang in other_langs:
                _check_markdown_page_parity(
                    input_abs=input_abs,
                    rel_path=rel_path,
                    default_lang=default_lang,
                    lang=lang,
                    default_tokens=def_tokens,
                    default_format=default_format,
                )
        else:
            for lang in other_langs:
                _check_html_page_parity(
                    input_abs=input_abs,
                    rel_path=rel_path,
                    default_lang=default_lang,
                    lang=lang,
                    default_content=def_content,
                    default_format=default_format,
                )

    return locale_files


def _rebase_single_url(
    raw_url: str,
    from_dir: str,
    to_dir: str,
    skip_prefixes: tuple[str, ...],
) -> str:
    """Rebase a single relative URL from ``from_dir`` to ``to_dir`` while preserving query/fragment."""
    trimmed = raw_url.strip()
    if not trimmed or trimmed.startswith(_SKIP_URL_PREFIXES) or trimmed.startswith("/"):
        return raw_url
    if skip_prefixes and trimmed.startswith(skip_prefixes):
        return raw_url

    fragment = ""
    base_part = trimmed
    if "#" in base_part:
        base_part, fragment = base_part.split("#", 1)
        fragment = f"#{fragment}"

    query = ""
    if "?" in base_part:
        base_part, query = base_part.split("?", 1)
        query = f"?{query}"

    if not base_part:
        return raw_url

    resolved_abs = os.path.normpath(os.path.join(from_dir, base_part))
    rebased = os.path.relpath(resolved_abs, to_dir).replace(os.sep, "/")
    return f"{rebased}{query}{fragment}"


def rebase_html_relative_urls(
    html: str,
    from_dir: str,
    to_dir: str,
    skip_prefixes: tuple[str, ...] = ("images/",),
) -> str:
    """Rewrite relative ``href`` and ``src`` attributes in an HTML body from ``from_dir`` to ``to_dir``."""
    protected_blocks: list[str] = []

    def _protect(m: re.Match[str]) -> str:
        idx = len(protected_blocks)
        protected_blocks.append(m.group(0))
        return f"__DRAWLIB_HTML_CODE_MASK_{idx}__"

    masked = re.sub(r"(?is)<pre\b[^>]*>.*?</pre>|<code\b[^>]*>.*?</code>", _protect, html)
    attr_re = re.compile(r'(\b(?:href|src)=["\'])([^"\']+)(["\'])', re.IGNORECASE)

    def _repl(match: re.Match[str]) -> str:
        prefix, url, suffix = match.group(1), match.group(2), match.group(3)
        return f"{prefix}{_rebase_single_url(url, from_dir, to_dir, skip_prefixes)}{suffix}"

    rebased = attr_re.sub(_repl, masked)
    for idx, original in enumerate(protected_blocks):
        rebased = rebased.replace(f"__DRAWLIB_HTML_CODE_MASK_{idx}__", original)
    return rebased


def rebase_markdown_relative_urls(
    markdown_text: str,
    from_dir: str,
    to_dir: str,
    skip_prefixes: tuple[str, ...] = ("images/",),
) -> str:
    """Rewrite relative Markdown links/images and raw HTML ``href``/``src`` outside fenced code blocks."""
    md_link_re = re.compile(r"(!?\[[^\]]*\]\()([^)\s]+)((?:\s+[\"'][^\"']*[\"'])?\))")
    fence_re = re.compile(r"^[ \t]{0,3}(`{3,}|~{3,})")

    out_lines: list[str] = []
    in_fence = False
    fence_marker = ""

    for line in markdown_text.split("\n"):
        if not in_fence:
            m = fence_re.match(line)
            if m:
                in_fence = True
                fence_marker = m.group(1)
                out_lines.append(line)
                continue

            line_rebased = md_link_re.sub(
                lambda m_lnk: (
                    f"{m_lnk.group(1)}"
                    f"{_rebase_single_url(m_lnk.group(2), from_dir, to_dir, skip_prefixes)}"
                    f"{m_lnk.group(3)}"
                ),
                line,
            )
            line_rebased = rebase_html_relative_urls(line_rebased, from_dir, to_dir, skip_prefixes=skip_prefixes)
            out_lines.append(line_rebased)
        else:
            out_lines.append(line)
            close_pat = rf"^[ \t]{{0,3}}{re.escape(fence_marker[0])}{{{len(fence_marker)},}}[ \t\r]*$"
            if re.match(close_pat, line):
                in_fence = False
                fence_marker = ""

    return "\n".join(out_lines)


def build_language_switcher_context(
    config: I18nConfig,
    out_dir_abs: str,
    rel_html_path: str,
    current_dest_abs: str,
    active_lang: str,
) -> tuple[list[dict[str, Any]], list[dict[str, str]]]:
    """Build ``(languages, alternate_links)`` template context for a specific destination HTML page.

    Args:
        config: Multi-locale site configuration.
        out_dir_abs: Root output HTML directory.
        rel_html_path: Locale-relative HTML path (e.g. ``'index.html'`` or ``'04_smartarts/table.html'``).
        current_dest_abs: Absolute path of the HTML file currently being rendered.
        active_lang: Canonical language code active on this page.

    Returns:
        tuple[list[dict[str, Any]], list[dict[str, str]]]:
            - ``languages``: List of switcher items (empty if ``len(config.langs) < 2``).
            - ``alternate_links``: List of ``{'hreflang': ..., 'url': ...}`` dicts for ``<head>``.
    """
    if len(config.langs) < 2:
        return [], []

    current_dest_dir = os.path.dirname(os.path.abspath(current_dest_abs))
    languages: list[dict[str, Any]] = []
    alternate_links: list[dict[str, str]] = []

    for lang_key in config.langs:
        lang_cfg = get_language_config(lang_key)
        target_abs = os.path.join(out_dir_abs, lang_key, rel_html_path)
        rel_url = os.path.relpath(target_abs, current_dest_dir).replace(os.sep, "/")
        languages.append(
            {
                "code": lang_key,
                "html_lang": lang_cfg.code,
                "label": lang_cfg.display_name,
                "url": rel_url,
                "active": (lang_key == active_lang),
            }
        )
        alternate_links.append({"hreflang": lang_cfg.code, "url": rel_url})

    if rel_html_path == "index.html":
        x_default_target = os.path.join(out_dir_abs, "index.html")
    else:
        x_default_target = os.path.join(out_dir_abs, config.default_lang, rel_html_path)
    x_default_url = os.path.relpath(x_default_target, current_dest_dir).replace(os.sep, "/")
    alternate_links.append({"hreflang": "x-default", "url": x_default_url})

    return languages, alternate_links
