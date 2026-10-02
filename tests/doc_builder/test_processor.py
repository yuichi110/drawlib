# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Unit tests for DrawlibBlockProcessor in doc_builder."""

import pytest

from drawlib._builder.doc_builder.processor import DrawlibBlockProcessor, extract_code_blocks


def test_block_processor_render_block_to_file_and_data_url(tmp_path) -> None:
    """Test single drawlib block rendering into PNG and WebP files and Data URLs."""
    processor = DrawlibBlockProcessor()

    code = (
        "from drawlib.shapes import circle\n"
        "from drawlib.styles import Styles\n"
        "circle((50, 50), radius=20, style=Styles.Primary)"
    )
    png_path = tmp_path / "out.png"
    processor.render_block_to_file(code, str(png_path))
    assert png_path.exists()
    assert png_path.read_bytes().startswith(b"\x89PNG")

    webp_path = tmp_path / "out.webp"
    processor.render_block_to_file(code, str(webp_path))
    assert webp_path.exists()
    assert webp_path.read_bytes().startswith(b"RIFF")

    data_url = processor.render_block_to_data_url(code, image_format="png")
    assert data_url.startswith("data:image/png;base64,")


def test_block_processor_markdown_replacement(tmp_path) -> None:
    """Test replacing ```drawlib blocks in Markdown with PNG image tags."""
    out_dir = tmp_path / "out"
    out_dir.mkdir()
    processor = DrawlibBlockProcessor()

    md_input = """# Test Title

Hello World

```drawlib file:diag.png
from drawlib.shapes import circle
from drawlib.styles import Styles
circle((50, 50), radius=10, style=Styles.Primary)
```

Footer
"""
    processed_md = processor.process_markdown(md_input, doc_base_name="my_doc", output_dir=str(out_dir))

    assert "# Test Title" in processed_md
    assert '<img src="my_doc_images/diag.png"' in processed_md
    assert "```drawlib" not in processed_md
    assert (out_dir / "my_doc_images" / "diag.png").exists()


def test_block_processor_html_script_tag(tmp_path) -> None:
    """Test processing <script type="text/drawlib"> tags with file attribute."""
    out_dir = tmp_path / "out"
    out_dir.mkdir()
    processor = DrawlibBlockProcessor()

    html_input = """<h1>HTML Document</h1>
<script type="text/drawlib" width="400px" align="center" caption="HTML Diagram" file="custom_diag.png">
from drawlib.shapes import circle
from drawlib.styles import Styles
circle((50, 50), radius=15, style=Styles.Primary)
</script>
"""
    blocks = extract_code_blocks(html_input, is_html=True)
    assert len(blocks) == 1
    assert blocks[0].file_name == "custom_diag.png"
    assert blocks[0].options.width == "400px"
    assert blocks[0].options.caption == "HTML Diagram"

    processed_html = processor.process_html(html_input, doc_base_name="page", output_dir=str(out_dir))
    assert '<img src="page_images/custom_diag.png"' in processed_html
    assert (out_dir / "page_images" / "custom_diag.png").exists()


def test_block_processor_with_utils(tmp_path) -> None:
    """Test that functions/variables defined in utils.py are accessible in drawlib blocks."""
    utils_file = tmp_path / "utils.py"
    utils_file.write_text(
        """
def draw_my_node(label: str) -> None:
    from drawlib.shapes import circle
    from drawlib.styles import Styles
    circle((50, 50), radius=15, style=Styles.Primary, text=label)
""",
        encoding="utf-8",
    )

    out_dir = tmp_path / "out"
    out_dir.mkdir()
    processor = DrawlibBlockProcessor(utils_path=str(utils_file))

    md_input = """
```drawlib file:node.webp
draw_my_node("Configured Node")
```
"""
    processed_md = processor.process_markdown(
        md_input,
        image_format="webp",
        doc_base_name="cfg_doc",
        output_dir=str(out_dir),
    )

    assert 'src="cfg_doc_images/node.webp"' in processed_md
    assert (out_dir / "cfg_doc_images" / "node.webp").exists()


def test_block_processor_ignore_explicit_save(tmp_path) -> None:
    """Test that explicit save() calls inside drawlib blocks are ignored and do not create unwanted files."""
    out_dir = tmp_path / "out"
    out_dir.mkdir()
    processor = DrawlibBlockProcessor()

    ignored_file = tmp_path / "should_not_be_created.png"
    md_input = f"""
```drawlib file:save_diag.png
from drawlib.canvas import save
from drawlib.styles import Styles
from drawlib.shapes import circle
circle((50, 50), radius=10, style=Styles.Primary)
save(r"{ignored_file}")
```
"""
    processed_md = processor.process_markdown(md_input, doc_base_name="save_test", output_dir=str(out_dir))

    assert "save_test_images/save_diag.png" in processed_md
    assert (out_dir / "save_test_images" / "save_diag.png").exists()
    assert not ignored_file.exists(), "Explicit save() file should not have been created"


def test_block_processor_space_separated_options(tmp_path) -> None:
    """Test parsing space-separated key:value and shorthand block options."""
    out_dir = tmp_path / "out"
    out_dir.mkdir()
    processor = DrawlibBlockProcessor()

    opts1 = processor._parse_block_info("400px center format:webp caption:'My Chart'")
    assert opts1.width == "400px"
    assert opts1.align == "center"
    assert opts1.format == "webp"
    assert opts1.caption == "My Chart"

    opts2 = processor._parse_block_info("w:500 h:300 align:right class:hero-img")
    assert opts2.width == "500px"
    assert opts2.height == "300px"
    assert opts2.align == "right"
    assert opts2.css_class == "hero-img"

    md_input = """
```drawlib file:arch.png 400px center caption:"System Architecture"
from drawlib.shapes import circle
from drawlib.styles import Styles
circle((50, 50), radius=10, style=Styles.Primary)
```
"""
    processed_md = processor.process_markdown(md_input, doc_base_name="opts_test", output_dir=str(out_dir))
    assert '<figure class="drawlib-image" style="text-align: center;">' in processed_md
    assert 'style="width: 400px; max-width: 100%;"' in processed_md
    assert '<figcaption class="drawlib-caption">System Architecture</figcaption>' in processed_md
    assert "</figure>" in processed_md


def test_block_processor_code_visibility_modes(tmp_path) -> None:
    """Test hide, show, and fold code visibility modes in Markdown and HTML."""
    out_dir = tmp_path / "out"
    out_dir.mkdir()
    processor = DrawlibBlockProcessor()

    # 1. Default (no option) -> hide code
    md_default = """
```drawlib file:default.png
from drawlib.shapes import circle
from drawlib.styles import Styles
circle((50, 50), radius=10, style=Styles.Primary)
```
"""
    res_default = processor.process_markdown(md_default, doc_base_name="default_doc", output_dir=str(out_dir))
    assert "```python" not in res_default
    assert "details" not in res_default
    assert 'src="default_doc_images/default.png"' in res_default

    # 2. show-code -> show code block followed by image
    md_show = """
```drawlib file:show.png show-code
from drawlib.shapes import circle
from drawlib.styles import Styles
circle((50, 50), radius=10, style=Styles.Primary)
```
"""
    res_show = processor.process_markdown(md_show, doc_base_name="show_doc", output_dir=str(out_dir))
    expected_md_code = (
        "```python\n"
        "from drawlib.shapes import circle\n"
        "from drawlib.styles import Styles\n"
        "circle((50, 50), radius=10, style=Styles.Primary)\n"
        "```"
    )
    assert expected_md_code in res_show
    assert 'src="show_doc_images/show.png"' in res_show
    # Python code comes before image
    assert res_show.find("```python") < res_show.find("show_doc_images/show.png")

    # 3. fold-code -> image followed by details tag
    md_fold = """
```drawlib file:fold.png fold-code
from drawlib.shapes import circle
from drawlib.styles import Styles
circle((50, 50), radius=10, style=Styles.Primary)
```
"""
    res_fold = processor.process_markdown(md_fold, doc_base_name="fold_doc", output_dir=str(out_dir))
    assert '<details class="drawlib-code-details">' in res_fold
    assert "<summary>Source Code</summary>" in res_fold
    assert expected_md_code in res_fold
    assert "</details>" in res_fold
    # Image comes before details
    assert res_fold.find("fold_doc_images/fold.png") < res_fold.find("<details")

    # 4. HTML script tag fold-code and show-code
    html_input = """
<script type="text/drawlib" code="fold" file="fold_img.png">
from drawlib.shapes import circle
from drawlib.styles import Styles
circle((50, 50), radius=10, style=Styles.Primary)
</script>
<script type="text/drawlib" code="show" file="show_img.png">
from drawlib.shapes import circle
from drawlib.styles import Styles
circle((50, 50), radius=10, style=Styles.Primary)
</script>
<script type="text/drawlib" file="hide_img.png">
from drawlib.shapes import circle
from drawlib.styles import Styles
circle((50, 50), radius=10, style=Styles.Primary)
</script>
"""
    res_html = processor.process_html(html_input, doc_base_name="html_doc", output_dir=str(out_dir))
    assert '<details class="drawlib-code-details">' in res_html
    expected_code = (
        '<pre><code class="language-python">'
        "from drawlib.shapes import circle\n"
        "from drawlib.styles import Styles\n"
        "circle((50, 50), radius=10, style=Styles.Primary)"
        "</code></pre>"
    )
    assert expected_code in res_html
    assert 'src="html_doc_images/fold_img.png"' in res_html
    assert 'src="html_doc_images/show_img.png"' in res_html
    assert 'src="html_doc_images/hide_img.png"' in res_html


def test_block_processor_code_options_parsing() -> None:
    """Test parsing code options in _parse_block_info."""
    processor = DrawlibBlockProcessor()

    assert processor._parse_block_info("").code == "hide"
    assert processor._parse_block_info("400px center").code == "hide"
    assert processor._parse_block_info("show-code").code == "show"
    assert processor._parse_block_info("show_code").code == "show"
    assert processor._parse_block_info("code:show").code == "show"
    assert processor._parse_block_info("code=show").code == "show"
    assert processor._parse_block_info("fold-code").code == "fold"
    assert processor._parse_block_info("fold_code").code == "fold"
    assert processor._parse_block_info("code:fold").code == "fold"
    assert processor._parse_block_info("code=fold").code == "fold"
    assert processor._parse_block_info("hide-code").code == "hide"
    assert processor._parse_block_info("code:hide").code == "hide"
    assert processor._parse_block_info("500px fold-code center").code == "fold"


def test_nested_drawlib_in_outer_code_fence_not_compiled(tmp_path) -> None:
    """Test that drawlib blocks nested inside outer Markdown fences (4+ backticks) are preserved literally."""
    out_dir = tmp_path / "out"
    out_dir.mkdir()
    processor = DrawlibBlockProcessor()

    md_input = """# Tutorial

Here is how to write a diagram in Drawlib:

````markdown
```drawlib 400px center
circle((50, 50), radius=10, style=Styles.Primary)
```
````

End of tutorial.
"""
    # 1. extract_code_blocks must not return nested blocks
    blocks = extract_code_blocks(md_input, is_html=False)
    assert len(blocks) == 0

    # 2. process_markdown must keep the block untouched and create no image
    processed_md = processor.process_markdown(md_input, doc_base_name="tut", output_dir=str(out_dir))
    assert processed_md == md_input
    assert not (out_dir / "tut_images").exists()


def test_mixed_nested_and_real_drawlib_blocks(tmp_path) -> None:
    """Test document with both a nested example block and an actual executable drawlib block."""
    out_dir = tmp_path / "out"
    out_dir.mkdir()
    processor = DrawlibBlockProcessor()

    md_input = """# Document

Example snippet:
````markdown
```drawlib
circle((0, 0), radius=5)
```
````

Actual diagram:
```drawlib file:mixed_circle.png
from drawlib.shapes import circle
from drawlib.styles import Styles
circle((50, 50), radius=20, style=Styles.Primary)
```
"""
    # 1. extract_code_blocks should only extract the real block
    blocks = extract_code_blocks(md_input, is_html=False)
    assert len(blocks) == 1
    assert blocks[0].index == 1
    assert "radius=20" in blocks[0].code
    # Line 11 is '```drawlib' for the actual diagram
    assert blocks[0].line_number == 11

    # 2. process_markdown renders the real block and preserves the nested example
    processed = processor.process_markdown(md_input, doc_base_name="mixed", output_dir=str(out_dir))
    # Outer fence snippet preserved
    assert "````markdown\n```drawlib\ncircle((0, 0), radius=5)\n```\n````" in processed
    # Real block replaced with image
    assert 'src="mixed_images/mixed_circle.png"' in processed
    assert (out_dir / "mixed_images" / "mixed_circle.png").exists()


def test_tilde_and_varied_length_outer_fences(tmp_path) -> None:
    """Test outer fences with tildes (~~~~) and 5 backticks."""
    out_dir = tmp_path / "out"
    out_dir.mkdir()
    processor = DrawlibBlockProcessor()

    md_input = """~~~~markdown
```drawlib
circle((10, 10), radius=5)
```
~~~~

`````text
```drawlib
circle((20, 20), radius=5)
```
`````
"""
    blocks = extract_code_blocks(md_input, is_html=False)
    assert len(blocks) == 0

    processed = processor.process_markdown(md_input, doc_base_name="fences", output_dir=str(out_dir))
    assert processed == md_input
    assert not (out_dir / "fences_images").exists()


def test_block_processor_require_file_validation(tmp_path) -> None:
    """Test that missing file:<name> raises ValueError by default and works when require_file=False."""
    out_dir = tmp_path / "out"
    out_dir.mkdir()

    # 1. Default require_file=True raises ValueError
    processor = DrawlibBlockProcessor()
    bad_md = """# Title
```drawlib
from drawlib.shapes import circle
from drawlib.styles import Styles
circle((50, 50), radius=10, style=Styles.Primary)
```
"""
    with pytest.raises(ValueError, match="Missing required 'file:<filename.ext>' option"):
        processor.process_markdown(bad_md, doc_base_name="bad", output_dir=str(out_dir))

    # 2. extract_code_blocks with require_file=True also raises ValueError
    with pytest.raises(ValueError, match="Missing required 'file:<filename.ext>' option"):
        extract_code_blocks(bad_md, is_html=False, require_file=True)

    # 3. require_file=False allows auto-indexing
    lenient_processor = DrawlibBlockProcessor(require_file=False)
    processed = lenient_processor.process_markdown(bad_md, doc_base_name="lenient", output_dir=str(out_dir))
    assert 'src="lenient_images/1.png"' in processed
    assert (out_dir / "lenient_images" / "1.png").exists()
