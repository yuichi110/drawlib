# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Block processor for extracting, executing, and replacing drawlib code blocks in text."""

import base64
import hashlib
import io
import os
import re
import shlex
import sys
import tempfile
from dataclasses import dataclass
from typing import Any, Dict, Optional

from drawlib._tools.doc_builder.config import load_config
from drawlib.canvas import clear, save


@dataclass
class DrawlibBlockOptions:
    """Parsed options from ```drawlib header line or <drawlib> tag attributes."""

    width: Optional[str] = None
    height: Optional[str] = None
    align: Optional[str] = None
    format: Optional[str] = None
    caption: Optional[str] = None
    css_class: Optional[str] = None


class DrawlibBlockProcessor:
    """Processor that replaces drawlib code blocks in Markdown/HTML with rendered PNG/SVG images or inline SVG tags."""

    def __init__(self, config_path: Optional[str] = None, cache_dir: str = ".drawlib_cache") -> None:
        """Initialize processor with shared globals and caching.

        Args:
            config_path (Optional[str]): Optional path to Python config script.
            cache_dir (str): Directory for caching rendered SVG files. Defaults to '.drawlib_cache'.
        """
        self.shared_globals: Dict[str, Any] = {}
        self.config_path = config_path
        self.cache_dir = cache_dir

        load_config(config_path=config_path, shared_globals=self.shared_globals)
        os.makedirs(self.cache_dir, exist_ok=True)

    def _get_cache_hash(self, code: str) -> str:
        """Compute SHA-256 hash for code block and config path.

        Args:
            code (str): Drawlib code block.

        Returns:
            str: SHA-256 hex digest.
        """
        hasher = hashlib.sha256()
        hasher.update(code.encode("utf-8"))
        if self.config_path:
            hasher.update(self.config_path.encode("utf-8"))
        return hasher.hexdigest()

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
        import drawlib._core.l4_canvas._canvas
        import drawlib.canvas

        canvas_inst = drawlib._core.l4_canvas._canvas.canvas
        orig_canvas_save = canvas_inst.save
        orig_core_save = drawlib._core.l4_canvas._canvas.save
        orig_canvas_mod_save = getattr(drawlib.canvas, "save", None)

        def _no_op_save(*args: Any, **kwargs: Any) -> None:  # noqa: ANN401
            pass

        clear()
        compiled = compile(code, filename=source_filename, mode="exec")

        exec_globals = shared_globals if shared_globals is not None else {}
        exec_globals["save"] = _no_op_save

        try:
            canvas_inst.save = _no_op_save  # type: ignore[assignment]
            drawlib._core.l4_canvas._canvas.save = _no_op_save  # type: ignore[assignment]
            drawlib.canvas.save = _no_op_save  # type: ignore[assignment]
            exec(compiled, exec_globals)
        except Exception as e:
            print(f"Error executing drawlib code block: {e}\nCode:\n{code}", file=sys.stderr)
            raise
        finally:
            canvas_inst.save = orig_canvas_save  # ty: ignore
            drawlib._core.l4_canvas._canvas.save = orig_core_save  # type: ignore[assignment]
            if orig_canvas_mod_save is not None:
                drawlib.canvas.save = orig_canvas_mod_save  # type: ignore[assignment]

    def render_block_svg(self, code: str, source_filename: str = "<drawlib_block>") -> str:
        """Execute a single drawlib code block and return rendered SVG XML string.

        Args:
            code (str): Drawlib code block.
            source_filename (str): Name used for code compilation traceback reporting.

        Returns:
            str: Rendered SVG XML string.
        """
        cache_hash = self._get_cache_hash(code)
        cache_path = os.path.join(self.cache_dir, f"{cache_hash}.svg")

        if os.path.exists(cache_path):
            with open(cache_path, "r", encoding="utf-8") as f:
                return f.read()

        self._exec_code_block(code, source_filename=source_filename, shared_globals=self.shared_globals)

        cache_abs_path = os.path.abspath(cache_path)
        os.makedirs(os.path.dirname(cache_abs_path), exist_ok=True)
        save(cache_abs_path)

        with open(cache_abs_path, "r", encoding="utf-8") as f:
            svg_content = f.read()

        return svg_content

    def render_block_to_file(
        self,
        code: str,
        target_file_path: str,
        source_filename: str = "<drawlib_block>",
    ) -> None:
        """Execute a single drawlib code block and save output image to target file path.

        Args:
            code (str): Drawlib code block.
            target_file_path (str): File path to save output image (e.g. PNG, SVG).
            source_filename (str): Name used for code compilation traceback reporting.
        """
        self._exec_code_block(code, source_filename=source_filename, shared_globals=self.shared_globals)

        target_abs_path = os.path.abspath(target_file_path)
        os.makedirs(os.path.dirname(target_abs_path), exist_ok=True)
        save(target_abs_path)

    def render_block_to_data_url(
        self,
        code: str,
        image_format: str = "png",
        source_filename: str = "<drawlib_block>",
    ) -> str:
        """Execute a single drawlib code block and return base64 Data URL or inline SVG string.

        Args:
            code (str): Drawlib code block.
            image_format (str): Image format ('png', 'svg', or 'inline_svg').
            source_filename (str): Name used for code compilation traceback reporting.

        Returns:
            str: Data URL string (e.g. data:image/png;base64,...) or inline SVG.
        """
        if image_format in {"svg", "inline_svg"}:
            return self.render_block_svg(code, source_filename=source_filename)

        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_png = os.path.join(tmp_dir, "temp.png")
            self.render_block_to_file(code, tmp_png, source_filename=source_filename)
            with open(tmp_png, "rb") as f:
                b64_str = base64.b64encode(f.read()).decode("utf-8")
            return f"data:image/png;base64,{b64_str}"

    def render_block(self, code: str, source_filename: str = "<drawlib_block>") -> str:
        """Alias for render_block_svg for backwards compatibility."""
        return self.render_block_svg(code, source_filename=source_filename)

    @staticmethod
    def _parse_block_info(info_str: str) -> DrawlibBlockOptions:
        """Parse space-separated key:value / key=value and shorthand options from header line or tag attributes.

        Args:
            info_str (str): Info string following ```drawlib or <drawlib> tag attributes.

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
            val_clean = val.strip()

            if key_lower in {"width", "w"}:
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
                if fmt in {"png", "svg", "inline_svg", "inline"}:
                    options.format = "inline_svg" if fmt in {"inline", "inline_svg"} else fmt
            elif key_lower == "caption":
                options.caption = val_clean
            elif key_lower in {"class", "css_class"}:
                options.css_class = val_clean
            elif not key_lower:
                val_lower = val_clean.lower()
                if val_lower in {"left", "center", "right"}:
                    options.align = val_lower
                elif val_lower in {"png", "svg", "inline_svg", "inline"}:
                    options.format = "inline_svg" if val_lower in {"inline", "inline_svg"} else val_lower
                elif re.match(r"^[0-9]+(?:px|%)?$", val_clean, re.IGNORECASE):
                    options.width = (
                        val_clean if (val_clean.endswith("px") or val_clean.endswith("%")) else f"{val_clean}px"
                    )

        return options

    @staticmethod
    def _format_image_wrapper(
        img_src: str,
        alt: str,
        options: DrawlibBlockOptions,
        is_inline_svg: bool = False,
        svg_content: Optional[str] = None,
    ) -> str:
        """Format HTML wrapper element (<div class="drawlib-image"> or <figure>) for image or inline SVG.

        Args:
            img_src (str): Image source path or Data URL.
            alt (str): Alt text.
            options (DrawlibBlockOptions): Parsed block options.
            is_inline_svg (bool): Whether content is inline SVG XML.
            svg_content (Optional[str]): Inline SVG XML string.

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

        if is_inline_svg and svg_content:
            inner_content = svg_content
        else:
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
    ) -> str:
        """Process Markdown text and replace ```drawlib blocks with rendered images or inline SVG.

        Args:
            markdown_text (str): Input Markdown text.
            doc_base_name (str): Base filename of the target document.
            output_dir (Optional[str]): Target output directory for image files.
            image_format (str): Image format ('png', 'svg', or 'inline_svg'). Default is 'png'.
            use_markdown_syntax (bool): If True, output Markdown image syntax (![alt](path)) instead of HTML img tags.
            embed_images (bool): If True, embed images directly as Data URLs or inline SVG without saving files.

        Returns:
            str: Processed Markdown text with img tags or inline SVG.
        """
        pattern = re.compile(r"(?<=\n)[ \t]*```drawlib([^\n]*)\n(.*?\n)[ \t]*```", re.DOTALL)
        block_counter = 0

        prepend_newline = not markdown_text.startswith("\n")
        text_to_search = "\n" + markdown_text if prepend_newline else markdown_text

        def replacer(match: re.Match[str]) -> str:
            nonlocal block_counter
            block_counter += 1
            info_str = match.group(1).strip()
            code = match.group(2).strip()
            options = self._parse_block_info(info_str)
            eff_format = options.format if options.format else image_format

            if embed_images:
                if eff_format in {"svg", "inline_svg"}:
                    svg = self.render_block_svg(code)
                    wrapper = self._format_image_wrapper(
                        "", f"{doc_base_name}_{block_counter}", options, is_inline_svg=True, svg_content=svg
                    )
                    return f"\n\n```python\n{code}\n```\n\n{wrapper}\n\n"
                data_url = self.render_block_to_data_url(code, image_format=eff_format)
                alt = f"{doc_base_name}_{block_counter}"
                wrapper = self._format_image_wrapper(data_url, alt, options)
                return f"\n\n```python\n{code}\n```\n\n{wrapper}\n\n"

            if eff_format == "inline_svg":
                svg = self.render_block_svg(code)
                wrapper = self._format_image_wrapper(
                    "", f"{doc_base_name}_{block_counter}", options, is_inline_svg=True, svg_content=svg
                )
                return f"\n\n```python\n{code}\n```\n\n{wrapper}\n\n"

            ext = "svg" if eff_format == "svg" else "png"
            img_filename = f"{doc_base_name}_{block_counter}.{ext}"

            if output_dir:
                target_img_path = os.path.join(output_dir, img_filename)
            else:
                target_img_path = img_filename

            self.render_block_to_file(code, target_img_path)

            has_custom_options = bool(
                options.width or options.height or options.align or options.caption or options.css_class
            )
            if use_markdown_syntax and not has_custom_options:
                return f"\n\n```python\n{code}\n```\n\n![{doc_base_name}_{block_counter}]({img_filename})\n\n"

            wrapper = self._format_image_wrapper(img_filename, f"{doc_base_name}_{block_counter}", options)
            return f"\n\n```python\n{code}\n```\n\n{wrapper}\n\n"

        res = pattern.sub(replacer, text_to_search)
        return res[1:] if prepend_newline else res

    def process_html(
        self,
        html_text: str,
        doc_base_name: str = "doc",
        output_dir: Optional[str] = None,
        image_format: str = "png",
        embed_images: bool = False,
    ) -> str:
        """Process HTML text and replace <drawlib> and <script type="text/drawlib"> blocks.

        Args:
            html_text (str): Input HTML text.
            doc_base_name (str): Base filename of the target document.
            output_dir (Optional[str]): Target output directory for image files.
            image_format (str): Image format ('png', 'svg', or 'inline_svg'). Default is 'png'.
            embed_images (bool): If True, embed images directly as Data URLs or inline SVG without saving files.

        Returns:
            str: Processed HTML text with img tags or inline SVG.
        """
        pattern_tag = re.compile(r"<drawlib\b([^>]*)>(.*?)</drawlib>", re.DOTALL | re.IGNORECASE)
        pattern_script = re.compile(
            r'<script\b([^>]*)type=["\']text/drawlib["\']([^>]*)>(.*?)</script>',
            re.DOTALL | re.IGNORECASE,
        )
        block_counter = 0

        def process_block_content(attrs: str, code: str) -> str:
            nonlocal block_counter
            block_counter += 1
            options = self._parse_block_info(attrs)
            eff_format = options.format if options.format else image_format

            if embed_images:
                if eff_format in {"svg", "inline_svg"}:
                    svg = self.render_block_svg(code)
                    wrapper = self._format_image_wrapper(
                        "", f"{doc_base_name}_{block_counter}", options, is_inline_svg=True, svg_content=svg
                    )
                    return f'<pre><code class="language-python">{code}</code></pre>\n{wrapper}'
                data_url = self.render_block_to_data_url(code, image_format=eff_format)
                alt = f"{doc_base_name}_{block_counter}"
                wrapper = self._format_image_wrapper(data_url, alt, options)
                return f'<pre><code class="language-python">{code}</code></pre>\n{wrapper}'

            if eff_format == "inline_svg":
                svg = self.render_block_svg(code)
                wrapper = self._format_image_wrapper(
                    "", f"{doc_base_name}_{block_counter}", options, is_inline_svg=True, svg_content=svg
                )
                return f'<pre><code class="language-python">{code}</code></pre>\n{wrapper}'

            ext = "svg" if eff_format == "svg" else "png"
            img_filename = f"{doc_base_name}_{block_counter}.{ext}"

            if output_dir:
                target_img_path = os.path.join(output_dir, img_filename)
            else:
                target_img_path = img_filename

            self.render_block_to_file(code, target_img_path)
            wrapper = self._format_image_wrapper(img_filename, f"{doc_base_name}_{block_counter}", options)
            return f'<pre><code class="language-python">{code}</code></pre>\n{wrapper}'

        def replacer_tag(match: re.Match[str]) -> str:
            attrs = match.group(1).strip()
            code = match.group(2).strip()
            return process_block_content(attrs, code)

        def replacer_script(match: re.Match[str]) -> str:
            attrs = (match.group(1) + " " + match.group(2)).strip()
            code = match.group(3).strip()
            return process_block_content(attrs, code)

        html_text = pattern_tag.sub(replacer_tag, html_text)
        return pattern_script.sub(replacer_script, html_text)
