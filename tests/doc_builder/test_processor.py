# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Unit tests for DrawlibBlockProcessor in doc_builder."""

import os
import tempfile

import pytest

from drawlib._tools.doc_builder.processor import DrawlibBlockProcessor


def test_block_processor_render_block(tmp_path) -> None:
    """Test single drawlib block rendering and caching."""
    cache_dir = tmp_path / ".cache"
    processor = DrawlibBlockProcessor(cache_dir=str(cache_dir))

    code = "circle((50, 50), radius=20)"
    svg1 = processor.render_block(code)

    assert "<svg" in svg1
    assert "</svg>" in svg1

    # Second render should hit cache
    svg2 = processor.render_block(code)
    assert svg1 == svg2


def test_block_processor_markdown_replacement(tmp_path) -> None:
    """Test replacing ```drawlib blocks in Markdown with PNG image tags."""
    cache_dir = tmp_path / ".cache"
    out_dir = tmp_path / "out"
    out_dir.mkdir()
    processor = DrawlibBlockProcessor(cache_dir=str(cache_dir))

    md_input = """# Test Title

Hello World

```drawlib
circle((50, 50), radius=10)
```

Footer
"""
    processed_md = processor.process_markdown(md_input, doc_base_name="my_doc", output_dir=str(out_dir))

    assert "# Test Title" in processed_md
    assert '<img src="my_doc_images/1.png"' in processed_md
    assert "```drawlib" not in processed_md
    assert (out_dir / "my_doc_images" / "1.png").exists()


def test_block_processor_with_config(tmp_path) -> None:
    """Test that functions/variables defined in config.py are accessible in drawlib blocks."""
    config_file = tmp_path / "config.py"
    config_file.write_text(
        """
def draw_my_node(label: str) -> None:
    circle((50, 50), radius=15, text=label)
""",
        encoding="utf-8",
    )

    cache_dir = tmp_path / ".cache"
    processor = DrawlibBlockProcessor(config_path=str(config_file), cache_dir=str(cache_dir))

    md_input = """
```drawlib
draw_my_node("Configured Node")
```
"""
    processed_md = processor.process_markdown(md_input, image_format="inline_svg")

    assert "<svg" in processed_md
    assert "Configured Node" in processed_md


def test_block_processor_ignore_explicit_save(tmp_path) -> None:
    """Test that explicit save() calls inside drawlib blocks are ignored and do not create unwanted files."""
    cache_dir = tmp_path / ".cache"
    out_dir = tmp_path / "out"
    out_dir.mkdir()
    processor = DrawlibBlockProcessor(cache_dir=str(cache_dir))

    ignored_file = tmp_path / "should_not_be_created.png"
    md_input = f"""
```drawlib
from drawlib.canvas import save
from drawlib.shapes import circle
circle((50, 50), radius=10)
save(r"{ignored_file}")
```
"""
    processed_md = processor.process_markdown(md_input, doc_base_name="save_test", output_dir=str(out_dir))

    assert "save_test_images/1.png" in processed_md
    assert (out_dir / "save_test_images" / "1.png").exists()
    assert not ignored_file.exists(), "Explicit save() file should not have been created"


def test_block_processor_space_separated_options(tmp_path) -> None:
    """Test parsing space-separated key:value and shorthand block options."""
    cache_dir = tmp_path / ".cache"
    out_dir = tmp_path / "out"
    out_dir.mkdir()
    processor = DrawlibBlockProcessor(cache_dir=str(cache_dir))

    opts1 = processor._parse_block_info("400px center format:svg caption:'My Chart'")
    assert opts1.width == "400px"
    assert opts1.align == "center"
    assert opts1.format == "svg"
    assert opts1.caption == "My Chart"

    opts2 = processor._parse_block_info("w:500 h:300 align:right class:hero-img")
    assert opts2.width == "500px"
    assert opts2.height == "300px"
    assert opts2.align == "right"
    assert opts2.css_class == "hero-img"

    md_input = """
```drawlib 400px center caption:"System Architecture"
from drawlib.shapes import circle
circle((50, 50), radius=10)
```
"""
    processed_md = processor.process_markdown(md_input, doc_base_name="opts_test", output_dir=str(out_dir))
    assert '<figure class="drawlib-image" style="text-align: center;">' in processed_md
    assert 'style="width: 400px; max-width: 100%;"' in processed_md
    assert '<figcaption class="drawlib-caption">System Architecture</figcaption>' in processed_md
    assert "</figure>" in processed_md
