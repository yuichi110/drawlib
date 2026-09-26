# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Tests for build script/README exclusions and config.py auto-discovery."""

from __future__ import annotations

from pathlib import Path

from drawlib._builder.doc_builder import build_html, build_markdown
from drawlib._builder.doc_builder.merger import expand_input_files
from drawlib._builder.image_builder import build_image


def test_doc_builder_exclusions_and_auto_config(tmp_path: Path) -> None:
    """Test that README.md, build.sh, and config.py are excluded from output and config.py is auto-detected."""
    src = tmp_path / "docs_src"
    src.mkdir()

    # Create config.py, style.css, template.html
    (src / "config.py").write_text("# config\n", encoding="utf-8")
    (src / "build.sh").write_text("#!/bin/bash\necho build\n", encoding="utf-8")
    (src / "README.md").write_text("# Internal Guide\nDo not build this.\n", encoding="utf-8")
    (src / "style.css").write_text("/* custom-css-marker */\nbody { background: #123456; }\n", encoding="utf-8")
    (src / "template.html").write_text(
        "<!DOCTYPE html><html><body><!-- custom-template-marker -->{{ body }}</body></html>\n",
        encoding="utf-8",
    )
    (src / "index.md").write_text("# Welcome\nHome page content.\n", encoding="utf-8")
    (src / "navbar.md").write_text("# Site\n- [Home](index.md)\n- [Guide](guide.md)\n", encoding="utf-8")
    (src / "guide.md").write_text(
        "# Guide\n```drawlib\nsetup(50, 50)\ncircle((25, 25), 10, style=styles.primary)\nsave()\n```\n",
        encoding="utf-8",
    )

    out_html = tmp_path / "docs_html"
    build_html(input_path=str(src), output=str(out_html), no_cache=True)

    assert (out_html / "index.html").is_file()
    assert (out_html / "guide.html").is_file()
    assert (out_html / "style.css").is_file()
    assert "custom-css-marker" in (out_html / "style.css").read_text(encoding="utf-8")
    assert "custom-template-marker" in (out_html / "index.html").read_text(encoding="utf-8")
    assert not (out_html / "README.html").exists()
    assert not (out_html / "README.md").exists()
    assert not (out_html / "build.sh").exists()
    assert not (out_html / "config.py").exists()
    assert not (out_html / "template.html").exists()

    out_md = tmp_path / "docs_md"
    build_markdown(input_path=str(src), output=str(out_md), no_cache=True)

    assert (out_md / "index.md").is_file()
    assert (out_md / "guide.md").is_file()
    assert not (out_md / "README.md").exists()
    assert not (out_md / "build.sh").exists()
    assert not (out_md / "config.py").exists()
    assert not (out_md / "style.css").exists()
    assert not (out_md / "template.html").exists()


def test_merger_excludes_readme(tmp_path: Path) -> None:
    """Test that expand_input_files in merger excludes README.md from directories."""
    src = tmp_path / "chapters"
    src.mkdir()

    (src / "README.md").write_text("# Ignore me\n", encoding="utf-8")
    (src / "01_intro.md").write_text("# Intro\n", encoding="utf-8")
    (src / "02_body.md").write_text("# Body\n", encoding="utf-8")

    files = expand_input_files([str(src)])
    basenames = [Path(f).name for f in files]
    assert "README.md" not in basenames
    assert "01_intro.md" in basenames
    assert "02_body.md" in basenames


def test_image_builder_exclusions_and_auto_config(tmp_path: Path) -> None:
    """Test that image_builder excludes config.py, build.sh, and __init__.py and auto-loads config.py."""
    src = tmp_path / "images_src"
    src.mkdir()

    (src / "config.py").write_text("# config\n", encoding="utf-8")
    (src / "build.sh").write_text("#!/bin/bash\necho build\n", encoding="utf-8")
    (src / "README.md").write_text("# Ignore\n", encoding="utf-8")
    (src / "__init__.py").write_text("# init\n", encoding="utf-8")
    (src / "diagram.py").write_text(
        "from drawlib.canvas import setup, save\nfrom drawlib.config import styles\n"
        "from drawlib.shapes import circle\nsetup(50, 50)\ncircle((25, 25), 10, style=styles.primary)\nsave()\n",
        encoding="utf-8",
    )

    out_img = tmp_path / "images"
    build_image(inputs=str(src), output=str(out_img), no_cache=True)

    assert (out_img / "diagram.png").is_file()
    assert not (out_img / "config.png").exists()
    assert not (out_img / "build.png").exists()
    assert not (out_img / "__init__.png").exists()
