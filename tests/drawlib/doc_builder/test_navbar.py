# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Unit tests for navbar.md parsing, validation, and relative URL resolution."""

import os

import pytest

from drawlib._builder.doc_builder.navbar import (
    NavbarItem,
    NavbarSection,
    parse_navbar_markdown,
    resolve_navbar_for_page,
)


def test_parse_navbar_valid(tmp_path) -> None:
    """Test parsing a valid navbar.md with sections, top-level items, and external links."""
    (tmp_path / "index.md").write_text("# Home\n", encoding="utf-8")
    sub_dir = tmp_path / "guide"
    sub_dir.mkdir()
    (sub_dir / "quickstart.md").write_text("# Quickstart\n", encoding="utf-8")
    (sub_dir / "advanced.md").write_text("# Advanced\n", encoding="utf-8")

    navbar_md = tmp_path / "navbar.md"
    navbar_md.write_text(
        """# Navigation
- [Home](index.md)

## Guides
- [Quick Start](guide/quickstart.md)
* [Advanced Guide](guide/advanced.md#config)

## External Links
- [GitHub](https://github.com/example/repo)
""",
        encoding="utf-8",
    )

    sections, site_title = parse_navbar_markdown(str(navbar_md), str(tmp_path))
    assert site_title == "Navigation"
    assert len(sections) == 3

    # Section 1: Top-level item without heading
    assert sections[0].title is None
    assert len(sections[0].items) == 1
    assert sections[0].items[0].title == "Home"
    assert sections[0].items[0].is_external is False

    # Section 2: Guides
    assert sections[1].title == "Guides"
    assert len(sections[1].items) == 2
    assert sections[1].items[0].title == "Quick Start"
    assert sections[1].items[1].anchor == "config"

    # Section 3: External Links
    assert sections[2].title == "External Links"
    assert len(sections[2].items) == 1
    assert sections[2].items[0].title == "GitHub"
    assert sections[2].items[0].is_external is True


def test_parse_navbar_missing_target_file_error(tmp_path) -> None:
    """Test that parse_navbar_markdown raises ValueError with line number when target file is missing."""
    (tmp_path / "index.md").write_text("# Home\n", encoding="utf-8")
    navbar_md = tmp_path / "navbar.md"
    navbar_md.write_text(
        """# Navigation
- [Home](index.md)
## Missing
- [Missing Page](docs/not_found.md)
""",
        encoding="utf-8",
    )

    with pytest.raises(ValueError) as exc_info:
        parse_navbar_markdown(str(navbar_md), str(tmp_path))

    err_msg = str(exc_info.value)
    assert "line 4" in err_msg
    assert "docs/not_found.md" in err_msg
    assert "does not exist" in err_msg


def test_parse_navbar_empty_error(tmp_path) -> None:
    """Test that parse_navbar_markdown raises ValueError when navbar has no links."""
    navbar_md = tmp_path / "navbar.md"
    navbar_md.write_text("# Navigation\n\nNo links here\n", encoding="utf-8")

    with pytest.raises(ValueError, match="No navigation links found"):
        parse_navbar_markdown(str(navbar_md), str(tmp_path))


def test_resolve_navbar_for_page(tmp_path) -> None:
    """Test resolving relative links and active page state across directories."""
    src_dir = tmp_path / "src"
    out_dir = tmp_path / "dist"
    src_dir.mkdir()
    sub_dir = src_dir / "guide"
    sub_dir.mkdir()

    (src_dir / "index.md").write_text("# Home\n", encoding="utf-8")
    (sub_dir / "canvas.md").write_text("# Canvas\n", encoding="utf-8")

    navbar_md = src_dir / "navbar.md"
    navbar_md.write_text(
        """- [Home](index.md)
## Guide
- [Canvas](guide/canvas.md)
- [GitHub](https://github.com)
""",
        encoding="utf-8",
    )

    sections, site_title = parse_navbar_markdown(str(navbar_md), str(src_dir))
    assert site_title is None

    # Resolve for root index.html
    root_src = str(src_dir / "index.md")
    root_dest = str(out_dir / "index.html")
    nav_secs_root, nav_items_root = resolve_navbar_for_page(
        sections=sections,
        root_dir_abs=str(src_dir),
        out_dir_abs=str(out_dir),
        current_src_abs=root_src,
        current_dest_abs=root_dest,
    )

    assert len(nav_items_root) == 3
    # Home link on index.html: active, url="index.html"
    assert nav_items_root[0]["title"] == "Home"
    assert nav_items_root[0]["url"] == "index.html"
    assert nav_items_root[0]["active"] is True

    # Canvas link from index.html: url="guide/canvas.html"
    assert nav_items_root[1]["title"] == "Canvas"
    assert nav_items_root[1]["url"] == "guide/canvas.html"
    assert nav_items_root[1]["active"] is False

    # External link
    assert nav_items_root[2]["url"] == "https://github.com"
    assert nav_items_root[2]["is_external"] is True

    # Resolve for nested guide/canvas.html
    sub_src = str(sub_dir / "canvas.md")
    sub_dest = str(out_dir / "guide" / "canvas.html")
    _, nav_items_sub = resolve_navbar_for_page(
        sections=sections,
        root_dir_abs=str(src_dir),
        out_dir_abs=str(out_dir),
        current_src_abs=sub_src,
        current_dest_abs=sub_dest,
    )

    # Home link from guide/canvas.html: url="../index.html"
    assert nav_items_sub[0]["url"] == "../index.html"
    assert nav_items_sub[0]["active"] is False

    # Canvas link on guide/canvas.html: active, url="canvas.html"
    assert nav_items_sub[1]["url"] == "canvas.html"
    assert nav_items_sub[1]["active"] is True


def test_parse_navbar_custom_site_title(tmp_path) -> None:
    """Test extracting custom site_title from the first H1 in navbar.md."""
    (tmp_path / "index.md").write_text("# Home\n", encoding="utf-8")
    navbar_md = tmp_path / "navbar.md"
    navbar_md.write_text(
        """# My Amazing Library
- [Home](index.md)
""",
        encoding="utf-8",
    )
    sections, site_title = parse_navbar_markdown(str(navbar_md), str(tmp_path))
    assert site_title == "My Amazing Library"
    assert len(sections) == 1
    assert sections[0].items[0].title == "Home"
