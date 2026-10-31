# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Unit and integration tests for multi-locale (i18n) site documentation builds."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

import pytest
from PIL import Image

from drawlib._builder.doc_builder import (
    build_html,
    build_markdown,
    extract_markdown_skeleton,
    load_i18n_config,
    validate_i18n_site,
)
from drawlib._builder.doc_builder.processor import DrawlibBlockProcessor
from drawlib._builder.image_builder import build_image
from drawlib._http_server._link_scanner import scan_broken_links
from drawlib._templates import init_project


def _write_minimal_i18n_site(src_dir: Path) -> None:
    """Create a minimal two-locale (en, ja) site directory for parity testing."""
    init_project("site", destination=src_dir.parent, target=src_dir.name, lang="en,ja", force=True)


def test_load_i18n_config_absent_and_valid(tmp_path: Path) -> None:
    """Verify load_i18n_config returns None when absent and normalizes aliases when present."""
    plain_dir = tmp_path / "plain_src"
    plain_dir.mkdir()
    assert load_i18n_config(str(plain_dir)) is None

    i18n_dir = tmp_path / "i18n_src"
    (i18n_dir / "en").mkdir(parents=True)
    (i18n_dir / "ja").mkdir(parents=True)
    (i18n_dir / "zh-cn").mkdir(parents=True)
    (i18n_dir / "i18n.toml").write_text(
        'default_lang = "EN"\nlangs = ["en", "jp", "zh"]\n',
        encoding="utf-8",
    )

    cfg = load_i18n_config(str(i18n_dir))
    assert cfg is not None
    assert cfg.default_lang == "en"
    assert cfg.langs == ["en", "ja", "zh-cn"]


def test_load_i18n_config_validation_errors(tmp_path: Path) -> None:
    """Verify malformed i18n.toml, duplicate langs, missing default_lang, and missing folders error."""
    base = tmp_path / "bad_src"
    base.mkdir()

    # Invalid TOML syntax
    (base / "i18n.toml").write_text("default_lang = [unclosed", encoding="utf-8")
    with pytest.raises(ValueError, match="Failed to parse"):
        load_i18n_config(str(base))

    # Duplicate normalized language codes
    (base / "en").mkdir(exist_ok=True)
    (base / "ja").mkdir(exist_ok=True)
    (base / "i18n.toml").write_text('default_lang = "en"\nlangs = ["en", "ja", "jp"]\n', encoding="utf-8")
    with pytest.raises(ValueError, match="duplicate language"):
        load_i18n_config(str(base))

    # default_lang not in langs
    (base / "i18n.toml").write_text('default_lang = "ko"\nlangs = ["en", "ja"]\n', encoding="utf-8")
    with pytest.raises(ValueError, match="must be included in langs"):
        load_i18n_config(str(base))

    # Missing locale directory on disk
    (base / "i18n.toml").write_text('default_lang = "en"\nlangs = ["en", "fr"]\n', encoding="utf-8")
    with pytest.raises(ValueError, match="Missing locale directory"):
        load_i18n_config(str(base))


def test_check_1_file_set_parity(tmp_path: Path) -> None:
    """Verify Check 1 catches missing and extra files across locale folders."""
    src_dir = tmp_path / "site_src"
    _write_minimal_i18n_site(src_dir)
    cfg = load_i18n_config(str(src_dir))
    assert cfg is not None

    # Extra file in ja/
    extra_md = src_dir / "ja" / "extra.md"
    extra_md.write_text("# Extra\n\nBody.\n", encoding="utf-8")
    with pytest.raises(ValueError, match=r"(?s)\[i18n file parity error\].*Extra files"):
        validate_i18n_site(str(src_dir), cfg)
    extra_md.unlink()

    # Missing file in ja/
    workflow_ja = src_dir / "ja" / "workflow" / "index.md"
    workflow_ja.unlink()
    with pytest.raises(ValueError, match=r"(?s)\[i18n file parity error\].*Missing files"):
        validate_i18n_site(str(src_dir), cfg)


def test_check_2_navbar_parity(tmp_path: Path) -> None:
    """Verify Check 2 catches section count, link count, and target URL mismatches in navbar.md."""
    src_dir = tmp_path / "site_src"
    _write_minimal_i18n_site(src_dir)
    cfg = load_i18n_config(str(src_dir))
    assert cfg is not None

    ja_nav = src_dir / "ja" / "navbar.md"

    # Mismatched link target order (swapping architecture and workflow)
    ja_nav.write_text(
        "# ドキュメント\n\n- [概要](index.md)\n\n## トピック\n"
        "- [ワークフロー](workflow/index.md)\n- [アーキテクチャ](architecture/index.md)\n",
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match=r"\[i18n navbar parity error\]"):
        validate_i18n_site(str(src_dir), cfg)

    # Mismatched section count
    ja_nav.write_text(
        "# ドキュメント\n\n- [概要](index.md)\n",
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match=r"\[i18n navbar parity error\]"):
        validate_i18n_site(str(src_dir), cfg)


def test_check_3_markdown_skeleton_sequence_parity(tmp_path: Path) -> None:
    """Verify Check 3 collapses natural prose freely while catching structural omissions."""
    en_md = (
        "# Page Title\n\n"
        "Lead paragraph in English.\n\n"
        "```drawlib align=center code=fold file=hero.png caption=\"Hero\"\n"
        "setup(width=60, height=30)\n"
        "```\n\n"
        "## Usage\n\n"
        "Single English sentence.\n\n"
        "````markdown\n"
        "```drawlib file=nested_example.png\n"
        "setup(width=40, height=20)\n"
        "```\n"
        "````\n\n"
        "Closing note.\n"
    )
    ja_rich_prose_md = (
        "# ページタイトル\n\n"
        "日本語のリード段落 1 です。\n\n"
        "日本語の補足段落 2 です。\n"
        "- 箇条書き項目 A\n"
        "- 箇条書き項目 B\n\n"
        "#### H4 小見出しも本文トークンに吸収されます\n\n"
        "```drawlib align=center code=fold file=hero.png caption=\"ヒーロー図\"\n"
        "setup(width=60, height=30)\n"
        "```\n\n"
        "## 使い方\n\n"
        "| 列1 | 列2 |\n"
        "| --- | --- |\n"
        "| 値A | 値B |\n\n"
        "````markdown\n"
        "```drawlib file=nested_example.png\n"
        "setup(width=999, height=999)\n"
        "```\n"
        "````\n\n"
        "末尾のまとめ文です。\n"
    )

    en_tokens = [t.describe() for t in extract_markdown_skeleton(en_md)]
    ja_tokens = [t.describe() for t in extract_markdown_skeleton(ja_rich_prose_md)]
    assert en_tokens == ja_tokens
    assert en_tokens == [
        "Heading(H1)",
        "MarkdownText",
        "DrawlibBlock(file=hero.png, code=fold)",
        "Heading(H2)",
        "MarkdownText",
        "CodeBlock(markdown)",
        "MarkdownText",
    ]

    # Verify missing trailing prose in ja fails Check 3
    src_dir = tmp_path / "skel_src"
    _write_minimal_i18n_site(src_dir)
    (src_dir / "en" / "index.md").write_text(en_md, encoding="utf-8")
    ja_missing_tail = ja_rich_prose_md.replace("末尾のまとめ文です。\n", "")
    (src_dir / "ja" / "index.md").write_text(ja_missing_tail, encoding="utf-8")

    cfg = load_i18n_config(str(src_dir))
    assert cfg is not None
    with pytest.raises(ValueError, match=r"\[i18n skeleton parity error\].*ended early"):
        validate_i18n_site(str(src_dir), cfg)


def test_check_4_drawlib_code_and_localized_filename_parity(tmp_path: Path) -> None:
    """Verify Check 4 enforces identical code on shared files and allows <stem>_<lang>.<ext> overrides."""
    src_dir = tmp_path / "code_src"
    _write_minimal_i18n_site(src_dir)
    cfg = load_i18n_config(str(src_dir))
    assert cfg is not None

    # 1. Shared filename with different Python code -> error suggesting *_ja.png
    ja_arch = src_dir / "ja" / "architecture" / "index.md"
    orig_ja_arch = ja_arch.read_text(encoding="utf-8")
    ja_arch.write_text(orig_ja_arch.replace('title="Frontend UI"', 'title="Modified Title"'), encoding="utf-8")
    with pytest.raises(ValueError, match=r"\[i18n drawlib code parity error\].*component_breakdown_ja\.png"):
        validate_i18n_site(str(src_dir), cfg)

    # 2. Arbitrary unrelated filename -> error
    ja_arch.write_text(
        orig_ja_arch.replace("file=component_breakdown.png", "file=other_diagram.png").replace(
            'title="Frontend UI"', 'title="Modified Title"'
        ),
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match=r"\[i18n drawlib filename error\]"):
        validate_i18n_site(str(src_dir), cfg)

    # 3. Proper <stem>_ja.png filename with custom localized code -> passes!
    ja_arch.write_text(
        orig_ja_arch.replace("file=component_breakdown.png", "file=component_breakdown_ja.png").replace(
            'title="Frontend UI"', 'title="Localized JP Node"'
        ),
        encoding="utf-8",
    )
    validated = validate_i18n_site(str(src_dir), cfg)
    assert set(validated.keys()) == {"en", "ja"}


def test_i18n_build_html_markdown_image_and_link_integrity(tmp_path: Path) -> None:
    """Verify end-to-end i18n HTML, Markdown, and image builds deduplicate shared renders and pass link checks."""
    src_dir = tmp_path / "docs_src"
    _write_minimal_i18n_site(src_dir)

    # Create a custom static asset in root _assets/ and reference it via ../_assets/badge.png in index.md
    badge_path = src_dir / "_assets" / "badge.png"
    Image.new("RGBA", (16, 16), (59, 130, 246, 255)).save(badge_path)

    en_index = src_dir / "en" / "index.md"
    ja_index = src_dir / "ja" / "index.md"
    en_index.write_text(
        en_index.read_text(encoding="utf-8") + "\n![Badge](../_assets/badge.png)\n",
        encoding="utf-8",
    )
    ja_index.write_text(
        ja_index.read_text(encoding="utf-8") + "\n![バッジ](../_assets/badge.png)\n",
        encoding="utf-8",
    )

    # Make workflow diagram localized in ja (execution_lifecycle_ja.png)
    ja_wf = src_dir / "ja" / "workflow" / "index.md"
    ja_wf.write_text(
        ja_wf.read_text(encoding="utf-8")
        .replace("file=execution_lifecycle.png", "file=execution_lifecycle_ja.png")
        .replace('text="Start"', 'text="JP Start"'),
        encoding="utf-8",
    )

    out_html = tmp_path / "docs_html"
    orig_exec = DrawlibBlockProcessor._exec_code_block
    exec_sources: list[str] = []

    def _counting_exec(
        code: str,
        source_filename: str = "<drawlib_block>",
        shared_globals: dict[str, object] | None = None,
    ) -> None:
        exec_sources.append(Path(source_filename).parent.name + "/" + Path(source_filename).name)
        orig_exec(code=code, source_filename=source_filename, shared_globals=shared_globals)

    with patch.object(DrawlibBlockProcessor, "_exec_code_block", staticmethod(_counting_exec)):
        build_html(str(src_dir), str(out_html), no_cache=True)

    # 4 shared diagrams rendered on 'en' (2 in en/index.md, 1 in architecture/index.md, 1 in workflow/index.md)
    # + 1 localized diagram rendered on 'ja' (1 in workflow/index.md) = 5 total code executions across 7 HTML pages!
    assert len(exec_sources) == 5

    # Check output layout
    assert (out_html / "index.html").is_file()
    assert (out_html / "en" / "index.html").is_file()
    assert (out_html / "ja" / "index.html").is_file()
    assert (out_html / "en" / "style.css").is_file()
    assert (out_html / "ja" / "style.css").is_file()
    assert (out_html / "images" / "index" / "basic_architecture.png").is_file()
    assert (out_html / "images" / "architecture" / "index" / "component_breakdown.png").is_file()
    assert (out_html / "images" / "workflow" / "index" / "execution_lifecycle.png").is_file()
    assert (out_html / "images" / "workflow" / "index" / "execution_lifecycle_ja.png").is_file()
    assert (out_html / "_assets" / "badge.png").is_file()

    # Check localized CSS typography
    ja_css = (out_html / "ja" / "style.css").read_text(encoding="utf-8")
    assert "Noto Sans JP" in ja_css

    # Check root index.html rebased URLs and language switcher links
    root_html = (out_html / "index.html").read_text(encoding="utf-8")
    assert '<html lang="en" dir="ltr">' in root_html
    assert 'href="en/style.css"' in root_html
    assert 'src="images/index/basic_architecture.png"' in root_html
    assert 'src="_assets/badge.png"' in root_html
    assert 'href="en/architecture/index.html"' in root_html
    assert 'href="ja/index.html"' in root_html

    # Check ja page metadata and switcher links
    ja_wf_html = (out_html / "ja" / "workflow" / "index.html").read_text(encoding="utf-8")
    assert '<html lang="ja" dir="ltr">' in ja_wf_html
    assert "Noto+Sans+JP" in ja_wf_html
    assert 'src="../../images/workflow/index/execution_lifecycle_ja.png"' in ja_wf_html
    assert 'href="../../en/workflow/index.html"' in ja_wf_html

    # Zero broken links across entire compiled site (including <a href>, <img>, <link rel="alternate">)
    html_count, total_links, broken_errors = scan_broken_links(str(out_html))
    assert html_count == 7
    assert total_links > 20
    assert broken_errors == []

    # Verify build_markdown output and root index.md rebasing
    out_md = tmp_path / "docs_markdown"
    build_markdown(str(src_dir), str(out_md))
    assert (out_md / "index.md").is_file()
    assert (out_md / "en" / "index.md").is_file()
    assert (out_md / "ja" / "index.md").is_file()
    assert (out_md / "images" / "index" / "basic_architecture.png").is_file()
    root_md = (out_md / "index.md").read_text(encoding="utf-8")
    assert "images/index/basic_architecture.png" in root_md
    assert "(en/architecture/index.md)" in root_md
    assert "(_assets/badge.png)" in root_md

    # Verify build_image deduplicated output
    out_imgs = tmp_path / "docs_images"
    build_image(str(src_dir), str(out_imgs))
    assert (out_imgs / "index" / "basic_architecture.png").is_file()
    assert (out_imgs / "workflow" / "index" / "execution_lifecycle.png").is_file()
    assert (out_imgs / "workflow" / "index" / "execution_lifecycle_ja.png").is_file()
