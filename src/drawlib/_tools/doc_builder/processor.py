# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Block processor for extracting, executing, and replacing drawlib code blocks in Markdown and HTML."""

from __future__ import annotations

import base64
import contextlib
import io
import os
import re
import shlex
import sys
import tempfile
import warnings
from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Literal, Optional

import drawlib._core.l4_canvas._canvas
import drawlib.canvas
from drawlib._core.l1_core import dutil_settings
from drawlib._tools.doc_builder.build_cache import BuildImageCache, hash_file
from drawlib._tools.doc_builder.config import load_config
from drawlib._tools.doc_builder.detector import detect_document_type
from drawlib._utils import dutil_canvas
from drawlib.canvas import save


@dataclass
class DrawlibBlockOptions:
    """Parsed options from ```drawlib header line or <script type="text/drawlib"> attributes."""

    width: Optional[str] = None
    height: Optional[str] = None
    align: Optional[str] = None
    format: Optional[str] = None
    caption: Optional[str] = None
    css_class: Optional[str] = None
    file: Optional[str] = None
    code: Literal["hide", "show", "fold"] = "hide"


def _resolve_block_image_paths(
    options: DrawlibBlockOptions,
    doc_base_name: str,
    block_counter: int,
    default_format: str,
    output_dir: Optional[str],
) -> tuple[str, str]:
    """Resolve relative image reference path and target filesystem path for a drawlib block.

    Args:
        options (DrawlibBlockOptions): Parsed block options.
        doc_base_name (str): Base filename of the document (without extension).
        block_counter (int): 1-based block index.
        default_format (str): Default image format ('png' or 'webp').
        output_dir (Optional[str]): Target output directory for generated assets.

    Returns:
        tuple[str, str]: (rel_img_path for HTML/Markdown src, target_img_path on disk).
    """
    eff_format = options.format if options.format in {"png", "webp"} else default_format
    ext = "webp" if eff_format == "webp" else "png"

    if options.file:
        raw_file = options.file.strip()
        base_part, file_ext = os.path.splitext(raw_file)
        if file_ext.lower() in {".png", ".webp"}:
            img_name = raw_file
        else:
            img_name = f"{raw_file}.{ext}"

        if "/" in img_name or (os.sep in img_name):
            rel_img_path = img_name
        else:
            rel_img_path = f"{doc_base_name}_images/{img_name}"
    else:
        img_name = f"{block_counter}.{ext}"
        rel_img_path = f"{doc_base_name}_images/{img_name}"

    if output_dir:
        target_img_path = os.path.join(output_dir, rel_img_path)
    else:
        target_img_path = rel_img_path

    return rel_img_path, target_img_path


class DrawlibBlockProcessor:
    """Processor that replaces drawlib code blocks in Markdown/HTML with rendered PNG/WebP images."""

    def __init__(
        self,
        config_path: Optional[str] = None,
        no_cache: bool = False,
        cache: Optional[BuildImageCache] = None,
    ) -> None:
        """Initialize processor with shared globals and SQLite build image cache.

        Args:
            config_path (Optional[str]): Optional path to Python config script.
            no_cache (bool): If True, disable reading/writing the SQLite build image cache.
            cache (Optional[BuildImageCache]): Optional shared BuildImageCache instance.
        """
        self.shared_globals: Dict[str, Any] = {}
        self.config_path = config_path
        self.config_hash = hash_file(config_path)
        self.no_cache = no_cache
        self._cache: BuildImageCache = (
            cache if cache is not None else BuildImageCache(enabled=not no_cache)
        )

        load_config(config_path=config_path, shared_globals=self.shared_globals)

    @staticmethod
    def _exec_code_block(
        code: str,
        source_filename: str = "<drawlib_block>",
        shared_globals: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Execute drawlib code block while temporarily overriding explicit save() calls as no-ops.

        Args:
            code (str): Drawlib code block.
            source_filename (str): Name used for code compilation traceback reporting.
            shared_globals (Optional[Dict[str, Any]]): Shared execution globals dictionary.
        """
        canvas_inst = drawlib._core.l4_canvas._canvas.canvas
        orig_canvas_save = canvas_inst.save
        orig_core_save = drawlib._core.l4_canvas._canvas.save
        orig_canvas_mod_save = getattr(drawlib.canvas, "save", None)

        def _no_op_save(*args: Any, **kwargs: Any) -> None:  # noqa: ANN401
            pass

        dutil_canvas.initialize()
        compiled = compile(code, filename=source_filename, mode="exec")

        exec_globals = shared_globals if shared_globals is not None else {}
        exec_globals["save"] = _no_op_save

        try:
            canvas_inst.save = _no_op_save  # type: ignore[assignment]
            drawlib._core.l4_canvas._canvas.save = _no_op_save  # type: ignore[assignment]
            drawlib.canvas.save = _no_op_save  # type: ignore[assignment]
            with warnings.catch_warnings():
                if dutil_settings.get_logging_mode() not in {"verbose", "developer"}:
                    warnings.filterwarnings("ignore", message=r"Glyph .* missing from font", category=UserWarning)
                    with contextlib.redirect_stdout(io.StringIO()):
                        exec(compiled, exec_globals)
                else:
                    exec(compiled, exec_globals)
        except Exception as e:
            print(f"Error executing drawlib code block: {e}\nCode:\n{code}", file=sys.stderr)
            raise
        finally:
            canvas_inst.save = orig_canvas_save  # ty: ignore
            drawlib._core.l4_canvas._canvas.save = orig_core_save  # type: ignore[assignment]
            if orig_canvas_mod_save is not None:
                drawlib.canvas.save = orig_canvas_mod_save  # type: ignore[assignment]

    def render_block_to_file(
        self,
        code: str,
        target_file_path: str,
        source_filename: str = "<drawlib_block>",
        grid: Optional[bool] = None,
    ) -> None:
        """Execute a single drawlib code block and save output image to target file path.

        Args:
            code (str): Drawlib code block.
            target_file_path (str): File path to save output image (e.g. PNG, WebP).
            source_filename (str): Name used for code compilation traceback reporting.
            grid (Optional[bool]): Whether to overlay coordinate grid on output image.
        """
        target_abs_path = os.path.abspath(target_file_path)
        stem, ext_dot = os.path.splitext(target_abs_path)
        fmt = "webp" if ext_dot.lower() == ".webp" else "png"
        grid_abs_path = f"{stem}_grid{ext_dot}"

        use_cache = self._cache.enabled and grid is None
        cache_key = ""
        code_hash = ""
        if use_cache:
            context_dir = (
                os.path.dirname(os.path.abspath(source_filename))
                if source_filename != "<drawlib_block>" and os.path.exists(source_filename)
                else os.getcwd()
            )
            cache_key, code_hash = self._cache.compute_keys(
                code=code,
                config_hash=self.config_hash,
                context_dir=context_dir,
            )
            cached = self._cache.get(cache_key, image_format=fmt)
            if cached is not None:
                normal_bytes, grid_bytes = cached
                os.makedirs(os.path.dirname(target_abs_path), exist_ok=True)
                with open(target_abs_path, "wb") as f:
                    f.write(normal_bytes)
                if grid_bytes is not None:
                    with open(grid_abs_path, "wb") as gf:
                        gf.write(grid_bytes)
                return

        if self.config_path:
            load_config(config_path=self.config_path, shared_globals=self.shared_globals)

        self._exec_code_block(code, source_filename=source_filename, shared_globals=self.shared_globals)

        os.makedirs(os.path.dirname(target_abs_path), exist_ok=True)
        if grid is True:
            drawlib._core.l4_canvas._canvas.canvas._grid = True
        with warnings.catch_warnings():
            if dutil_settings.get_logging_mode() not in {"verbose", "developer"}:
                warnings.filterwarnings("ignore", message=r"Glyph .* missing from font", category=UserWarning)
            save(target_abs_path)

        if use_cache and os.path.isfile(target_abs_path):
            with open(target_abs_path, "rb") as f:
                normal_bytes = f.read()
            grid_bytes: Optional[bytes] = None
            if os.path.isfile(grid_abs_path):
                with open(grid_abs_path, "rb") as gf:
                    grid_bytes = gf.read()
            self._cache.put(
                cache_key=cache_key,
                code_hash=code_hash,
                config_hash=self.config_hash,
                image_format=fmt,
                image_blob=normal_bytes,
                grid_blob=grid_bytes,
            )

    def render_block_to_data_url(
        self,
        code: str,
        image_format: str = "png",
        source_filename: str = "<drawlib_block>",
    ) -> str:
        """Execute a single drawlib code block and return a base64 Data URL string.

        Args:
            code (str): Drawlib code block.
            image_format (str): Image format ('png' or 'webp').
            source_filename (str): Name used for code compilation traceback reporting.

        Returns:
            str: Data URL string (e.g. data:image/png;base64,...).
        """
        ext = "webp" if image_format == "webp" else "png"
        mime = "image/webp" if ext == "webp" else "image/png"

        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_file = os.path.join(tmp_dir, f"temp.{ext}")
            self.render_block_to_file(code, tmp_file, source_filename=source_filename)
            with open(tmp_file, "rb") as f:
                b64_str = base64.b64encode(f.read()).decode("utf-8")
            return f"data:{mime};base64,{b64_str}"

    @staticmethod
    def _parse_block_info(info_str: str) -> DrawlibBlockOptions:
        """Parse space-separated key:value / key=value and shorthand options from header line or tag attributes.

        Args:
            info_str (str): Info string following ```drawlib or <script type="text/drawlib"> attributes.

        Returns:
            DrawlibBlockOptions: Parsed options object.
        """
        options = DrawlibBlockOptions()
        info = info_str.strip()
        if not info:
            return options

        try:
            tokens = shlex.split(info, posix=True)
        except ValueError:
            tokens = info.split()

        for token in tokens:
            if ":" in token:
                key, val = token.split(":", 1)
            elif "=" in token:
                key, val = token.split("=", 1)
            else:
                key, val = "", token

            key_lower = key.strip().lower()
            val_clean = val.strip().strip("\"'")

            if key_lower == "type":
                continue
            elif key_lower == "code":
                val_code = val_clean.lower()
                if val_code == "show":
                    options.code = "show"
                elif val_code == "fold":
                    options.code = "fold"
                elif val_code == "hide":
                    options.code = "hide"
            elif key_lower in {"width", "w"}:
                options.width = val_clean if (val_clean.endswith("px") or val_clean.endswith("%")) else f"{val_clean}px"
            elif key_lower in {"height", "h"}:
                options.height = (
                    val_clean if (val_clean.endswith("px") or val_clean.endswith("%")) else f"{val_clean}px"
                )
            elif key_lower in {"align", "a"}:
                if val_clean.lower() in {"left", "center", "right"}:
                    options.align = val_clean.lower()
            elif key_lower in {"format", "fmt"}:
                fmt = val_clean.lower()
                if fmt in {"png", "webp"}:
                    options.format = fmt
            elif key_lower == "caption":
                options.caption = val_clean
            elif key_lower in {"class", "css_class"}:
                options.css_class = val_clean
            elif key_lower == "file":
                options.file = val_clean
            elif not key_lower:
                val_lower = val_clean.lower()
                if val_lower in {"show-code", "show_code"}:
                    options.code = "show"
                elif val_lower in {"fold-code", "fold_code"}:
                    options.code = "fold"
                elif val_lower in {"hide-code", "hide_code"}:
                    options.code = "hide"
                elif val_lower in {"left", "center", "right"}:
                    options.align = val_lower
                elif val_lower in {"png", "webp"}:
                    options.format = val_lower
                elif re.match(r"^\d+(px|%)$", val_lower) or val_lower.isdigit():
                    has_unit = val_lower.endswith("px") or val_lower.endswith("%")
                    options.width = val_clean if has_unit else f"{val_clean}px"

        return options

    @staticmethod
    def _format_image_wrapper(
        img_src: str,
        alt: str,
        options: DrawlibBlockOptions,
    ) -> str:
        """Format <img> wrapped in <div> or <figure> with styles and caption.

        Args:
            img_src (str): Image source path or Data URL.
            alt (str): Alt text for image.
            options (DrawlibBlockOptions): Parsed block options.

        Returns:
            str: Formatted HTML block string.
        """
        classes = ["drawlib-image"]
        if options.css_class:
            classes.append(options.css_class)
        class_str = " ".join(classes)

        container_styles = []
        if options.align == "center":
            container_styles.append("text-align: center;")
        elif options.align == "left":
            container_styles.append("text-align: left;")
        elif options.align == "right":
            container_styles.append("text-align: right;")
        container_style_attr = f' style="{" ".join(container_styles)}"' if container_styles else ""

        img_styles = []
        if options.width:
            img_styles.append(f"width: {options.width};")
        if options.height:
            img_styles.append(f"height: {options.height};")
        if img_styles:
            img_styles.append("max-width: 100%;")
        img_style_attr = f' style="{" ".join(img_styles)}"' if img_styles else ""

        tag_name = "figure" if options.caption else "div"
        inner_content = f'<img src="{img_src}" alt="{alt}"{img_style_attr} />'

        if options.caption:
            caption_html = f'\n  <figcaption class="drawlib-caption">{options.caption}</figcaption>'
            return (
                f'<{tag_name} class="{class_str}"{container_style_attr}>\n'
                f"  {inner_content}{caption_html}\n"
                f"</{tag_name}>"
            )

        return f'<{tag_name} class="{class_str}"{container_style_attr}>\n  {inner_content}\n</{tag_name}>'

    def process_markdown(
        self,
        markdown_text: str,
        doc_base_name: str = "doc",
        output_dir: Optional[str] = None,
        image_format: str = "png",
        use_markdown_syntax: bool = False,
        embed_images: bool = False,
        source_filename: str = "<drawlib_block>",
        progress_callback: Optional[Callable[[int, int, bool], None]] = None,
    ) -> str:
        """Process Markdown text and replace ```drawlib blocks with rendered images.

        Args:
            markdown_text (str): Input Markdown text.
            doc_base_name (str): Base filename of the target document.
            output_dir (Optional[str]): Target output directory for image files.
            image_format (str): Image format ('png' or 'webp'). Default is 'png'.
            use_markdown_syntax (bool): If True, output Markdown image syntax (![alt](path)) instead of HTML img tags.
            embed_images (bool): If True, embed images directly as Data URLs without saving files.
            source_filename (str): Path of source markdown file used for code execution context.
            progress_callback (Optional[Callable[[int, int, bool], None]]): Progress callback `(step, total, done)`.

        Returns:
            str: Processed Markdown text with img tags or Markdown image links.
        """
        pattern = re.compile(r"(?<=\n)[ \t]*```drawlib([^\n]*)\n(.*?\n)[ \t]*```", re.DOTALL)
        block_counter = 0

        prepend_newline = not markdown_text.startswith("\n")
        text_to_search = "\n" + markdown_text if prepend_newline else markdown_text
        total_blocks = len(pattern.findall(text_to_search))

        def replacer(match: re.Match[str]) -> str:
            nonlocal block_counter
            block_counter += 1
            info_str = match.group(1).strip()
            code = match.group(2).strip()
            options = self._parse_block_info(info_str)
            eff_format = options.format if options.format in {"png", "webp"} else image_format

            if embed_images:
                data_url = self.render_block_to_data_url(code, image_format=eff_format, source_filename=source_filename)
                alt = f"{doc_base_name}_{block_counter}"
                wrapper = self._format_image_wrapper(data_url, alt, options)
                if progress_callback is not None:
                    progress_callback(block_counter, total_blocks, False)
                if options.code == "show":
                    return f"\n\n```python\n{code}\n```\n\n{wrapper}\n\n"
                elif options.code == "fold":
                    return (
                        f"\n\n{wrapper}\n\n"
                        f'<details class="drawlib-code-details">\n'
                        f"<summary>Source Code</summary>\n\n"
                        f"```python\n{code}\n```\n\n"
                        f"</details>\n\n"
                    )
                else:
                    return f"\n\n{wrapper}\n\n"

            rel_img_path, target_img_path = _resolve_block_image_paths(
                options=options,
                doc_base_name=doc_base_name,
                block_counter=block_counter,
                default_format=eff_format,
                output_dir=output_dir,
            )

            self.render_block_to_file(code, target_img_path, source_filename=source_filename)
            if progress_callback is not None:
                progress_callback(block_counter, total_blocks, False)

            has_custom_options = bool(
                options.width or options.height or options.align or options.caption or options.css_class
            )
            if use_markdown_syntax and not has_custom_options:
                img_part = f"![{doc_base_name}_{block_counter}]({rel_img_path})"
            else:
                img_part = self._format_image_wrapper(rel_img_path, f"{doc_base_name}_{block_counter}", options)

            if options.code == "show":
                return f"\n\n```python\n{code}\n```\n\n{img_part}\n\n"
            elif options.code == "fold":
                return (
                    f"\n\n{img_part}\n\n"
                    f'<details class="drawlib-code-details">\n'
                    f"<summary>Source Code</summary>\n\n"
                    f"```python\n{code}\n```\n\n"
                    f"</details>\n\n"
                )
            else:
                return f"\n\n{img_part}\n\n"

        res = pattern.sub(replacer, text_to_search)
        return res[1:] if prepend_newline else res

    def process_html(
        self,
        html_text: str,
        doc_base_name: str = "doc",
        output_dir: Optional[str] = None,
        image_format: str = "png",
        embed_images: bool = False,
        source_filename: str = "<drawlib_block>",
        progress_callback: Optional[Callable[[int, int, bool], None]] = None,
    ) -> str:
        """Process HTML text and replace <script type="text/drawlib"> blocks with rendered images.

        Args:
            html_text (str): Input HTML text.
            doc_base_name (str): Base filename of the target document.
            output_dir (Optional[str]): Target output directory for image files.
            image_format (str): Image format ('png' or 'webp'). Default is 'png'.
            embed_images (bool): If True, embed images directly as Data URLs without saving files.
            source_filename (str): Path of source HTML file used for code execution context.
            progress_callback (Optional[Callable[[int, int, bool], None]]): Progress callback `(step, total, done)`.

        Returns:
            str: Processed HTML text with img tags.
        """
        pattern_script = re.compile(
            r'<script\b([^>]*)type=["\']text/drawlib["\']([^>]*)>(.*?)</script>',
            re.DOTALL | re.IGNORECASE,
        )
        block_counter = 0
        total_blocks = len(pattern_script.findall(html_text))

        def replacer_script(match: re.Match[str]) -> str:
            nonlocal block_counter
            block_counter += 1
            attrs = (match.group(1) + " " + match.group(2)).strip()
            code = match.group(3).strip()
            options = self._parse_block_info(attrs)
            eff_format = options.format if options.format in {"png", "webp"} else image_format

            if embed_images:
                data_url = self.render_block_to_data_url(code, image_format=eff_format, source_filename=source_filename)
                alt = f"{doc_base_name}_{block_counter}"
                wrapper = self._format_image_wrapper(data_url, alt, options)
                if progress_callback is not None:
                    progress_callback(block_counter, total_blocks, False)
                if options.code == "show":
                    return f'<pre><code class="language-python">{code}</code></pre>\n{wrapper}'
                elif options.code == "fold":
                    return (
                        f"{wrapper}\n"
                        f'<details class="drawlib-code-details">\n'
                        f"<summary>Source Code</summary>\n"
                        f'<pre><code class="language-python">{code}</code></pre>\n'
                        f"</details>"
                    )
                else:
                    return wrapper

            rel_img_path, target_img_path = _resolve_block_image_paths(
                options=options,
                doc_base_name=doc_base_name,
                block_counter=block_counter,
                default_format=eff_format,
                output_dir=output_dir,
            )

            self.render_block_to_file(code, target_img_path, source_filename=source_filename)
            if progress_callback is not None:
                progress_callback(block_counter, total_blocks, False)
            wrapper = self._format_image_wrapper(rel_img_path, f"{doc_base_name}_{block_counter}", options)
            if options.code == "show":
                return f'<pre><code class="language-python">{code}</code></pre>\n{wrapper}'
            elif options.code == "fold":
                return (
                    f"{wrapper}\n"
                    f'<details class="drawlib-code-details">\n'
                    f"<summary>Source Code</summary>\n"
                    f'<pre><code class="language-python">{code}</code></pre>\n'
                    f"</details>"
                )
            else:
                return wrapper

        return pattern_script.sub(replacer_script, html_text)


@dataclass
class ExtractedBlockInfo:
    """Extracted code block information for show and export subcommands."""

    index: int
    code: str
    info_str: str
    options: DrawlibBlockOptions
    file_name: str
    line_number: int


def extract_code_blocks(text: str, is_html: bool = False) -> List[ExtractedBlockInfo]:
    """Extract all drawlib code blocks from Markdown or HTML text.

    Args:
        text (str): Input Markdown or HTML text.
        is_html (bool): If True, extract <script type="text/drawlib"> blocks; otherwise extract ```drawlib blocks.

    Returns:
        List[ExtractedBlockInfo]: List of extracted code block information objects.
    """
    blocks: List[ExtractedBlockInfo] = []

    if is_html:
        pattern_script = re.compile(
            r'<script\b([^>]*)type=["\']text/drawlib["\']([^>]*)>(.*?)</script>',
            re.DOTALL | re.IGNORECASE,
        )
        for idx, match in enumerate(pattern_script.finditer(text), start=1):
            start_line = text[: match.start()].count("\n") + 1
            info_str = (match.group(1) + " " + match.group(2)).strip()
            code = match.group(3).strip()
            options = DrawlibBlockProcessor._parse_block_info(info_str)
            ext = "webp" if (options.format == "webp") else "png"
            if options.file:
                fn = options.file if ("." in options.file) else f"{options.file}.{ext}"
            else:
                fn = f"{idx}.{ext}"

            blocks.append(
                ExtractedBlockInfo(
                    index=idx,
                    code=code,
                    info_str=info_str,
                    options=options,
                    file_name=fn,
                    line_number=start_line,
                )
            )
        return blocks

    lines = text.splitlines()
    i = 0
    block_index = 0
    while i < len(lines):
        line = lines[i]
        match = re.match(r"^[ \t]*```drawlib([^\n]*)", line)
        if match:
            block_index += 1
            start_line = i + 1
            info_str = match.group(1).strip()
            options = DrawlibBlockProcessor._parse_block_info(info_str)
            code_lines = []
            i += 1
            while i < len(lines) and not re.match(r"^[ \t]*```", lines[i]):
                code_lines.append(lines[i])
                i += 1
            code = "\n".join(code_lines).strip()

            ext = "webp" if (options.format == "webp") else "png"
            if options.file:
                fn = options.file if ("." in options.file) else f"{options.file}.{ext}"
            else:
                fn = f"{block_index}.{ext}"

            blocks.append(
                ExtractedBlockInfo(
                    index=block_index,
                    code=code,
                    info_str=info_str,
                    options=options,
                    file_name=fn,
                    line_number=start_line,
                )
            )
        i += 1
    return blocks


def _resolve_selected_block(
    blocks: List[ExtractedBlockInfo],
    target: str,
) -> Optional[ExtractedBlockInfo]:
    """Find matching ExtractedBlockInfo by 1-based index or filename.

    Args:
        blocks (List[ExtractedBlockInfo]): List of extracted code blocks.
        target (str): 1-based index string (e.g. '1', '-1') or filename (e.g. '1.png', 'my_image').

    Returns:
        Optional[ExtractedBlockInfo]: Matching block info or None.
    """
    if target.isdigit() or (target.startswith("-") and target[1:].isdigit()):
        idx = int(target)
        if idx < 0:
            idx = len(blocks) + idx + 1
        for b in blocks:
            if b.index == idx:
                return b
        return None

    target_clean = target.lower()
    for b in blocks:
        b_fn = b.file_name.lower()
        b_base = os.path.splitext(b_fn)[0]
        b_basename_only = os.path.basename(b_fn)
        b_basename_stem = os.path.splitext(b_basename_only)[0]
        if target_clean in {b_fn, b_base, b_basename_only, b_basename_stem}:
            return b
    return None


def _render_code_with_context(
    code: str,
    dest_abs: str,
    source_filename: str,
    file_dir: str,
    config_path: Optional[str],
    grid: bool,
) -> None:
    """Execute code block and render directly to destination path under directory context.

    Args:
        code (str): Python drawing code block.
        dest_abs (str): Absolute destination file path.
        source_filename (str): Name used for code compilation traceback reporting.
        file_dir (str): Directory to chdir and insert into sys.path during execution.
        config_path (Optional[str]): Optional path to config/setup Python script.
        grid (bool): Whether to overlay coordinate grid.
    """
    processor = DrawlibBlockProcessor(config_path=config_path)
    orig_cwd = os.getcwd()
    sys_path_added = False
    try:
        os.chdir(file_dir)
        if file_dir not in sys.path:
            sys.path.insert(0, file_dir)
            sys_path_added = True

        processor.render_block_to_file(code, dest_abs, source_filename=source_filename, grid=grid)
    finally:
        os.chdir(orig_cwd)
        if sys_path_added and file_dir in sys.path:
            sys.path.remove(file_dir)


def export_code_block(
    file_path: Optional[str] = None,
    target: Optional[str] = None,
    output_path: Optional[str] = None,
    config_path: Optional[str] = None,
    grid: bool = False,
    *,
    markdown_path: Optional[str] = None,
) -> str:
    """Execute target code block from Markdown, HTML, or Python file and export image to specified output path.

    Args:
        file_path (Optional[str]): Path to input Markdown (.md), HTML (.html), or Python script (.py).
        target (Optional[str]): Optional index or file specifier for Markdown/HTML code blocks.
        output_path (Optional[str]): Destination image path. If omitted, defaults to block filename in cwd.
        config_path (Optional[str]): Optional path to Python setup/config script (e.g. config.py).
        grid (bool): Whether to overlay coordinate grid on exported image.
        markdown_path (Optional[str]): Deprecated alias for file_path for backward compatibility.

    Returns:
        str: Absolute path of the exported image file, or empty string if list was displayed.

    Raises:
        ValueError: If file path is invalid or target code block cannot be found.
    """
    target_path = file_path or markdown_path
    if not target_path:
        raise ValueError("No file path provided.")

    if not os.path.exists(target_path):
        raise ValueError(f"File '{target_path}' does not exist.")

    abs_path = os.path.abspath(target_path)
    file_dir = os.path.dirname(abs_path)

    if target_path.endswith(".py"):
        with open(target_path, "r", encoding="utf-8") as f:
            code = f.read()

        dest = output_path if output_path else f"{os.path.splitext(os.path.basename(target_path))[0]}.png"
        dest_abs = os.path.abspath(dest)
        _render_code_with_context(
            code=code,
            dest_abs=dest_abs,
            source_filename=abs_path,
            file_dir=file_dir,
            config_path=config_path,
            grid=grid,
        )
        print(f"Successfully exported Python script to: {dest_abs}")
        return dest_abs

    doc_base_name = os.path.splitext(os.path.basename(target_path))[0]
    with open(target_path, "r", encoding="utf-8") as f:
        content = f.read()

    doc_info = detect_document_type(target_path, content)
    blocks = extract_code_blocks(content, is_html=doc_info.is_html)
    if not blocks:
        raise ValueError(f"No drawlib code blocks found in '{target_path}' (detected type: {doc_info.doc_type}).")

    if not target:
        print(f"Available drawlib code blocks in '{target_path}':")
        print(f"{'Index':<7} {'Line':<7} {'File Target':<28} {'Header Options'}")
        print("-" * 65)
        for b in blocks:
            target_rel_path = b.file_name if ("/" in b.file_name) else f"{doc_base_name}_images/{b.file_name}"
            opts = b.info_str if b.info_str else "-"
            print(f"{b.index:<7} L{b.line_number:<6} {target_rel_path:<28} {opts}")
        return ""

    selected_block = _resolve_selected_block(blocks, target)
    if not selected_block:
        raise ValueError(f"Could not find block matching '{target}' in '{target_path}'.")

    if output_path:
        if os.path.isdir(output_path) or output_path.endswith(os.sep) or output_path.endswith("/"):
            dest = os.path.join(output_path, os.path.basename(selected_block.file_name))
        else:
            dest = output_path
    else:
        dest = os.path.basename(selected_block.file_name)

    dest_abs = os.path.abspath(dest)
    _render_code_with_context(
        code=selected_block.code,
        dest_abs=dest_abs,
        source_filename=abs_path,
        file_dir=file_dir,
        config_path=config_path,
        grid=grid,
    )
    print(f"Successfully exported block #{selected_block.index} to: {dest_abs}")
    return dest_abs


def show_code_block(
    file_path: Optional[str] = None,
    target: Optional[str] = None,
    config_path: Optional[str] = None,
    grid: bool = False,
    output_path: Optional[str] = None,
    *,
    markdown_path: Optional[str] = None,
) -> None:
    """Execute target code block from Markdown/HTML file or Python drawing script and display output image.

    Args:
        file_path (Optional[str]): File path to input Markdown (.md), HTML (.html), or Python script (.py).
        target (Optional[str]): Optional index or file specifier for Markdown/HTML code blocks.
        config_path (Optional[str]): Optional path to Python setup/config script.
        grid (bool): Whether to overlay coordinate grid on displayed image.
        output_path (Optional[str]): Optional destination image path. If specified, saves image without GUI display.
        markdown_path (Optional[str]): Deprecated alias for file_path for backward compatibility.
    """
    if output_path:
        export_code_block(
            file_path=file_path,
            target=target,
            output_path=output_path,
            config_path=config_path,
            grid=grid,
            markdown_path=markdown_path,
        )
        return

    target_path = file_path or markdown_path
    if not target_path:
        print("Error: No file path provided.", file=sys.stderr)
        sys.exit(1)

    if not os.path.exists(target_path):
        print(f"Error: File '{target_path}' does not exist.", file=sys.stderr)
        sys.exit(1)

    if target_path.endswith(".py"):
        print(f"Executing Python script '{target_path}'" + (" with grid overlay..." if grid else "..."))
        with open(target_path, "r", encoding="utf-8") as f:
            code = f.read()

        abs_file = os.path.abspath(target_path)
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
            tmp_path = tmp.name

        base, ext = os.path.splitext(tmp_path)
        grid_path = f"{base}_grid{ext}"
        _render_code_with_context(
            code=code,
            dest_abs=tmp_path,
            source_filename=abs_file,
            file_dir=os.path.dirname(abs_file),
            config_path=config_path,
            grid=grid,
        )
        display_path = grid_path if (grid and os.path.exists(grid_path)) else tmp_path
        _display_image_file(display_path)
        return

    doc_base_name = os.path.splitext(os.path.basename(target_path))[0]
    with open(target_path, "r", encoding="utf-8") as f:
        content = f.read()

    doc_info = detect_document_type(target_path, content)
    blocks = extract_code_blocks(content, is_html=doc_info.is_html)
    if not blocks:
        print(f"No drawlib code blocks found in '{target_path}' (detected type: {doc_info.doc_type}).")
        return

    if not target:
        print(f"Available drawlib code blocks in '{target_path}':")
        print(f"{'Index':<7} {'Line':<7} {'File Target':<28} {'Header Options'}")
        print("-" * 65)
        for b in blocks:
            target_rel_path = b.file_name if ("/" in b.file_name) else f"{doc_base_name}_images/{b.file_name}"
            opts = b.info_str if b.info_str else "-"
            print(f"{b.index:<7} L{b.line_number:<6} {target_rel_path:<28} {opts}")
        return

    selected_block = _resolve_selected_block(blocks, target)
    if not selected_block:
        print(f"Error: Could not find block matching '{target}' in '{target_path}'.", file=sys.stderr)
        sys.exit(1)

    target_rel_path = (
        selected_block.file_name
        if ("/" in selected_block.file_name)
        else f"{doc_base_name}_images/{selected_block.file_name}"
    )
    print(
        f"Executing block #{selected_block.index} (L{selected_block.line_number} -> {target_rel_path})"
        + (" with grid overlay..." if grid else "...")
    )

    abs_doc = os.path.abspath(target_path)
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
        tmp_path = tmp.name

    base, ext = os.path.splitext(tmp_path)
    grid_path = f"{base}_grid{ext}"
    _render_code_with_context(
        code=selected_block.code,
        dest_abs=tmp_path,
        source_filename=abs_doc,
        file_dir=os.path.dirname(abs_doc),
        config_path=config_path,
        grid=grid,
    )
    display_path = grid_path if (grid and os.path.exists(grid_path)) else tmp_path
    _display_image_file(display_path)


def _display_image_file(image_path: str) -> None:
    """Open and display image file using PIL Image.show() unless disabled.

    Args:
        image_path (str): File path to the image to display.
    """
    print(f"Rendered successfully to temp file: {image_path}")
    from PIL import Image

    img = Image.open(image_path)
    if os.environ.get("DRAWLIB_SHOW_NO_DISPLAY") != "1":
        img.show()
