# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""DrawlibBlockProcessor implementation for executing and replacing code blocks."""

from __future__ import annotations

import base64
import contextlib
import io
import os
import re
import sys
import tempfile
import warnings
from typing import Any, Callable, Dict, Optional

import drawlib._core.l4_canvas
import drawlib.canvas
from drawlib._builder._common import (
    BuildImageCache,
    hash_file,
    load_styles_and_utils,
)
from drawlib._builder.doc_builder.detector import (
    preserve_outer_fences,
    restore_outer_fences,
)
from drawlib._builder.doc_builder.processor.options import (
    DrawlibBlockOptions,
    parse_block_info,
    resolve_block_image_paths,
)
from drawlib._core.l1_core import dutil_settings
from drawlib._core.l4_canvas import save


class DrawlibBlockProcessor:
    """Processor that replaces drawlib code blocks in Markdown/HTML with rendered PNG/WebP images."""

    def __init__(
        self,
        styles_path: Optional[str] = None,
        utils_path: Optional[str] = None,
        no_cache: bool = False,
        cache: Optional[BuildImageCache] = None,
        project_root: Optional[str] = None,
        require_file: bool = True,
    ) -> None:
        """Initialize processor with shared globals and SQLite build image cache."""
        self.shared_globals: Dict[str, Any] = {}
        self.styles_path = styles_path
        self.utils_path = utils_path
        s_hash = hash_file(styles_path) if styles_path else ""
        u_hash = hash_file(utils_path) if utils_path else ""
        self.config_hash = f"{s_hash}:{u_hash}"
        self.no_cache = no_cache
        self.require_file = require_file
        self._cache: BuildImageCache = cache if cache is not None else BuildImageCache(enabled=not no_cache)
        self.project_root: Optional[str] = os.path.abspath(project_root) if project_root else None
        if self.project_root is None:
            if styles_path and os.path.isfile(styles_path):
                self.project_root = os.path.dirname(os.path.abspath(styles_path))
            elif utils_path and os.path.isfile(utils_path):
                self.project_root = os.path.dirname(os.path.abspath(utils_path))

        load_styles_and_utils(
            styles_path=styles_path,
            utils_path=utils_path,
            shared_globals=self.shared_globals,
        )

    @staticmethod
    def _exec_code_block(
        code: str,
        source_filename: str = "<drawlib_block>",
        shared_globals: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Execute drawlib code block while temporarily overriding explicit save() calls as no-ops."""
        canvas_inst = drawlib._core.l4_canvas.canvas
        orig_canvas_save = canvas_inst.save
        orig_core_save = drawlib._core.l4_canvas.save
        orig_canvas_mod_save = getattr(drawlib.canvas, "save", None)

        def _no_op_save(*args: Any, **kwargs: Any) -> None:  # noqa: ANN401
            pass

        drawlib._core.l4_canvas.clear()
        compiled = compile(code, filename=source_filename, mode="exec")

        exec_globals = shared_globals if shared_globals is not None else {}
        exec_globals["save"] = _no_op_save

        try:
            setattr(canvas_inst, "save", _no_op_save)
            setattr(drawlib._core.l4_canvas, "save", _no_op_save)
            setattr(drawlib.canvas, "save", _no_op_save)
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
            setattr(canvas_inst, "save", orig_canvas_save)
            setattr(drawlib._core.l4_canvas, "save", orig_core_save)
            if orig_canvas_mod_save is not None:
                setattr(drawlib.canvas, "save", orig_canvas_mod_save)

    def render_block_to_file(
        self,
        code: str,
        target_file_path: str,
        source_filename: str = "<drawlib_block>",
        grid: Optional[bool] = None,
    ) -> None:
        """Execute a single drawlib code block and save output image to target file path."""
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
                project_root=self.project_root,
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

        if self.styles_path or self.utils_path:
            load_styles_and_utils(
                styles_path=self.styles_path,
                utils_path=self.utils_path,
                shared_globals=self.shared_globals,
            )

        self._exec_code_block(code, source_filename=source_filename, shared_globals=self.shared_globals)

        os.makedirs(os.path.dirname(target_abs_path), exist_ok=True)
        if grid is True:
            drawlib._core.l4_canvas.canvas._grid = True
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
        """Execute a single drawlib code block and return a base64 Data URL string."""
        ext = "webp" if image_format == "webp" else "png"
        mime = "image/webp" if ext == "webp" else "image/png"

        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_file = os.path.join(tmp_dir, f"temp.{ext}")
            self.render_block_to_file(code, tmp_file, source_filename=source_filename)
            with open(tmp_file, "rb") as f:
                b64_str = base64.b64encode(f.read()).decode("utf-8")
            return f"data:{mime};base64,{b64_str}"

    @staticmethod
    def _format_image_wrapper(
        img_src: str,
        alt: str,
        options: DrawlibBlockOptions,
    ) -> str:
        """Format <img> wrapped in <div> or <figure> with styles and caption."""
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
        """Process Markdown text and replace ```drawlib blocks with rendered images."""
        masked_text, preserved = preserve_outer_fences(markdown_text)
        pattern = re.compile(r"(?<=\n)[ \t]*```drawlib([^\n]*)\n(.*?)\n[ \t]*```", re.DOTALL)
        block_counter = 0

        prepend_newline = not masked_text.startswith("\n")
        text_to_search = "\n" + masked_text if prepend_newline else masked_text
        total_blocks = len(pattern.findall(text_to_search))

        def replacer(match: re.Match[str]) -> str:
            nonlocal block_counter
            block_counter += 1
            info_str = match.group(1).strip()
            code = match.group(2).strip()
            options = parse_block_info(info_str)

            # Find line number of this block
            match_start = match.start()
            line_no = text_to_search[:match_start].count("\n") + 1

            rel_img_path, target_img_path = resolve_block_image_paths(
                options=options,
                doc_base_name=doc_base_name,
                block_counter=block_counter,
                default_format=image_format,
                output_dir=output_dir,
                require_file=self.require_file,
                line_number=line_no,
            )

            if embed_images:
                data_url = self.render_block_to_data_url(
                    code,
                    image_format=image_format,
                    source_filename=source_filename,
                )
                rel_img_path = data_url
            else:
                self.render_block_to_file(code, target_img_path, source_filename=source_filename)

            if progress_callback is not None:
                progress_callback(block_counter, total_blocks, block_counter == total_blocks)

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

        processed_text = pattern.sub(replacer, text_to_search)
        if prepend_newline and processed_text.startswith("\n"):
            processed_text = processed_text[1:]

        return restore_outer_fences(processed_text, preserved)

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
        """Process HTML text and replace <script type="text/drawlib"> blocks with rendered images."""
        pattern_script = re.compile(
            r"""<script\b([^>]*)type=["']text/drawlib["']([^>]*)>(.*?)</script>""",
            re.DOTALL | re.IGNORECASE,
        )
        block_counter = 0
        total_blocks = len(pattern_script.findall(html_text))

        def replacer_script(match: re.Match[str]) -> str:
            nonlocal block_counter
            block_counter += 1
            info_str = (match.group(1) + " " + match.group(2)).strip()
            code = match.group(3).strip()
            options = parse_block_info(info_str)

            line_no = html_text[:match.start()].count("\n") + 1

            rel_img_path, target_img_path = resolve_block_image_paths(
                options=options,
                doc_base_name=doc_base_name,
                block_counter=block_counter,
                default_format=image_format,
                output_dir=output_dir,
                require_file=self.require_file,
                line_number=line_no,
            )

            if embed_images:
                data_url = self.render_block_to_data_url(
                    code,
                    image_format=image_format,
                    source_filename=source_filename,
                )
                rel_img_path = data_url
            else:
                self.render_block_to_file(code, target_img_path, source_filename=source_filename)

            if progress_callback is not None:
                progress_callback(block_counter, total_blocks, block_counter == total_blocks)

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
