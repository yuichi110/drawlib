# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Unit tests for slide components, drawing helpers, and presentation templates."""

from __future__ import annotations

from pathlib import Path

import pytest

import drawlib.slide as slide_module
from drawlib._builder.project_init import init_project
from drawlib._css_templates import get_css, get_slide_js, list_slide_css
from drawlib._slide import (
    BoundingBox,
    build_slide,
)
from drawlib.canvas import clear, save, setup
from slide_src.utils import draw_curved_agenda, draw_kpi_cards
from tests.cli.common import run_drawlib_cli


class TestSlideFoundation:
    """Test suite for slide foundation and bounding boxes."""

    def test_bounding_box_attributes_and_immutability(self) -> None:
        """Verify BoundingBox attributes and frozen immutability."""
        box = BoundingBox(x=100.0, y=200.0, width=800.0, height=600.0)
        assert box.x == 100.0
        assert box.y == 200.0
        assert box.width == 800.0
        assert box.height == 600.0

        with pytest.raises(Exception):
            # Should be frozen/immutable
            setattr(box, "x", 150.0)

    def test_list_slide_css_presets(self) -> None:
        """Verify list_slide_css returns available presentation presets."""
        presets = list_slide_css()
        assert len(presets) >= 2
        names = {p["name"] for p in presets}
        assert "google" in names
        assert "default" in names

    def test_get_slide_css_content(self) -> None:
        """Verify get_css with target='slide' returns complete presentation stylesheet."""
        google_css = get_css(name="google", target="slide")
        assert "--slide-width" in google_css
        assert "presentation-stage" in google_css

        default_css = get_css(name="default", target="slide")
        assert "--slide-width" in default_css

    def test_get_slide_js_content(self) -> None:
        """Verify get_slide_js returns the vanilla JS deck controller."""
        js_code = get_slide_js()
        assert "STAGE_WIDTH" in js_code
        assert "goToSlide" in js_code
        assert "updateScale" in js_code

    def test_public_slide_facade(self) -> None:
        """Verify public drawlib.slide facade exposes expected domain symbols."""
        assert hasattr(slide_module, "BoundingBox")
        assert hasattr(slide_module, "build_slide")
        assert slide_module.BoundingBox is BoundingBox


class TestSlideDrawingHelpers:
    """Test suite for slide drawing helpers with Native SVG vector rendering."""

    def test_draw_curved_agenda_svg(self, tmp_path: Path) -> None:
        """Verify draw_curved_agenda renders geometry and searchable native text into SVG."""
        output_svg = tmp_path / "agenda.svg"
        clear()
        setup(width=104, height=86)
        items = [
            ("Team Introductions", "チーム紹介"),
            ("Architecture Overview", "設計概要"),
            ("Production Deployment", "本番公開"),
        ]
        draw_curved_agenda(items, width=104.0, height=86.0)
        save(str(output_svg), format="svg")
        clear()

        assert output_svg.is_file()
        svg_content = output_svg.read_text(encoding="utf-8")
        assert "<svg" in svg_content
        assert "<text" in svg_content
        assert "Team Introductions" in svg_content
        assert "チーム紹介" in svg_content
        assert "Architecture Overview" in svg_content

    def test_draw_kpi_cards_svg(self, tmp_path: Path) -> None:
        """Verify draw_kpi_cards renders metrics and searchable native text into SVG."""
        output_svg = tmp_path / "kpi.svg"
        clear()
        setup(width=100, height=84)
        cards = [
            ("99.99%", "System Availability", "Tier-1 SLA Guaranteed"),
            ("1.2s", "Fast Build Time", "Sub-second SQLite cache hit"),
        ]
        draw_kpi_cards(cards, width=100.0, height=84.0)
        save(str(output_svg), format="svg")
        clear()

        assert output_svg.is_file()
        svg_content = output_svg.read_text(encoding="utf-8")
        assert "<svg" in svg_content
        assert "<text" in svg_content
        assert "99.99%" in svg_content
        assert "System Availability" in svg_content
        assert "Tier-1 SLA Guaranteed" in svg_content


class TestSlideCompiler:
    """Test suite for slide markdown compiler and presentation deck generator."""

    def test_build_slide_compilation(self, tmp_path: Path) -> None:
        """Verify end-to-end compilation of a multi-slide presentation."""
        src_dir = tmp_path / "slide_src"
        out_dir = tmp_path / "slide"
        src_dir.mkdir()

        (src_dir / "01_title.md").write_text(
            """---
layout: cover
theme: google
paginate: false
---

# Drawlib Test Deck
## Presentation as Code
""",
            encoding="utf-8",
        )

        (src_dir / "utils.py").write_text(Path("slide_src/utils.py").read_text(encoding="utf-8"), encoding="utf-8")

        (src_dir / "02_agenda.md").write_text(
            """---
header: "Presentation Agenda"
layout: default
---

# Topics

```drawlib (820, 140) (1040, 860) file:agenda.svg
from drawlib.canvas import setup, clear
from utils import draw_curved_agenda

clear()
setup(width=104, height=86)
draw_curved_agenda(
    [
        ("First Step", "はじめに"),
        ("Second Step", "つづき"),
    ],
    width=104,
    height=86,
)
```
""",
            encoding="utf-8",
        )

        (src_dir / "03_features.md").write_text(
            """---
header: "Features"
layout: split-right
ratio: "4:6"
---

# Declarative Illustrations

- Pure Python code
- Native SVG text elements

```drawlib 100% center file:diag.svg slot:right
from drawlib.shapes import rectangle
from drawlib.styles import Styles
from drawlib.canvas import setup, clear

clear()
setup(width=100, height=60)
rectangle((50, 30), width=40, height=20, style=Styles.PrimaryFlat, text="Box", text_style=Styles.WhiteBold)
```
""",
            encoding="utf-8",
        )

        result_html = build_slide(str(src_dir), str(out_dir), no_cache=True)
        assert Path(result_html).is_file()

        index_content = Path(result_html).read_text(encoding="utf-8")
        assert "Drawlib Test Deck" in index_content
        assert "presentation-stage" in index_content
        assert 'data-slide-index="1"' in index_content
        assert 'data-slide-index="2"' in index_content
        assert 'data-slide-index="3"' in index_content

        # Assets
        assert (out_dir / "slide.css").is_file()
        assert (out_dir / "slide.js").is_file()
        assert (out_dir / "agenda.svg").is_file()
        assert (out_dir / "diag.svg").is_file()

        # Check SVG has text
        agenda_svg = (out_dir / "agenda.svg").read_text(encoding="utf-8")
        assert "First Step" in agenda_svg
        assert "はじめに" in agenda_svg

    def test_build_slide_missing_dir_raises(self, tmp_path: Path) -> None:
        """Verify ValueError raised when source directory does not exist."""
        with pytest.raises(ValueError, match="Input directory does not exist"):
            build_slide(str(tmp_path / "non_existent_dir"))

    def test_build_slide_no_md_files_raises(self, tmp_path: Path) -> None:
        """Verify ValueError raised when source directory contains no markdown files."""
        empty_dir = tmp_path / "empty_dir"
        empty_dir.mkdir()
        with pytest.raises(ValueError, match="No Markdown slide files"):
            build_slide(str(empty_dir))

    def test_build_slide_canvas_mode(self, tmp_path: Path) -> None:
        """Verify layout: canvas produces full-bleed 1920x1080 stage without header or footer."""
        src_dir = tmp_path / "slide_src"
        out_dir = tmp_path / "slide"
        src_dir.mkdir()

        (src_dir / "01_canvas.md").write_text(
            """---
layout: canvas
---

```drawlib (0, 0) (1920, 1080) file:hero.svg
from drawlib.canvas import setup, clear
from drawlib.shapes import rectangle
from drawlib.styles import Styles

clear()
setup(width=192, height=108)
rectangle((96, 54), width=180, height=90, style=Styles.PrimaryFlat)
```
""",
            encoding="utf-8",
        )

        result_html = build_slide(str(src_dir), str(out_dir), no_cache=True)
        content = Path(result_html).read_text(encoding="utf-8")
        assert "layout-canvas" in content
        assert "slide-header" not in content
        assert "slide-footer" not in content
        assert "slide-positioned-asset" in content
        assert (out_dir / "hero.svg").is_file()

    def test_build_slide_container_boxes_and_coordinates(self, tmp_path: Path) -> None:
        """Verify ::: box container syntax creates absolutely positioned, styled text boxes."""
        src_dir = tmp_path / "slide_src"
        out_dir = tmp_path / "slide"
        src_dir.mkdir()

        (src_dir / "01_boxes.md").write_text(
            """---
header: "Microservices"
---

::: box (80, 140) (740, 480) font:21px compact z:10
# Ingress Controller
- **TLS**: Terminated at edge
- **Routing**: Path-based dispatch
:::

::: box (80, 660) (740, 320) align:center
> Note: Zero-trust network policy active.
:::
""",
            encoding="utf-8",
        )

        result_html = build_slide(str(src_dir), str(out_dir), no_cache=True)
        content = Path(result_html).read_text(encoding="utf-8")
        assert "slide-text-box" in content
        assert "left: 80.0px; top: 140.0px; width: 740.0px; height: 480.0px;" in content
        assert "font-size: 21px;" in content
        assert "compact" in content
        assert "z-index: 10;" in content
        assert "left: 80.0px; top: 660.0px; width: 740.0px; height: 320.0px;" in content
        assert "text-align: center;" in content

    def test_build_slide_header_footer_suppression(self, tmp_path: Path) -> None:
        """Verify header: none and footer: none suppress master frame components."""
        src_dir = tmp_path / "slide_src"
        out_dir = tmp_path / "slide"
        src_dir.mkdir()

        (src_dir / "01_suppressed.md").write_text(
            """---
header: none
footer: none
layout: default
---

# Clean Slide Without Chrome
- Focused content only
""",
            encoding="utf-8",
        )

        result_html = build_slide(str(src_dir), str(out_dir), no_cache=True)
        content = Path(result_html).read_text(encoding="utf-8")
        assert "slide-header" not in content
        assert "slide-footer" not in content
        assert "Clean Slide Without Chrome" in content

    def test_build_slide_frontmatter_options(self, tmp_path: Path) -> None:
        """Verify slide-level frontmatter: offset_y, font_size, compact, and box."""
        src_dir = tmp_path / "slide_src"
        out_dir = tmp_path / "slide"
        src_dir.mkdir()

        (src_dir / "01_options.md").write_text(
            """---
header: "Fine Tuned Slide"
offset_y: -25px
font_size: 20px
compact: true
box: "(80, 140) (740, 840)"
---

# Title Inside Auto-Box
- Point 1
- Point 2
""",
            encoding="utf-8",
        )

        result_html = build_slide(str(src_dir), str(out_dir), no_cache=True)
        content = Path(result_html).read_text(encoding="utf-8")
        assert "transform: translateY(-25px);" in content
        assert "font-size: 20px;" in content
        assert "compact" in content
        assert "slide-text-box" in content
        assert "left: 80.0px; top: 140.0px; width: 740.0px; height: 840.0px;" in content


class TestSlideCli:
    """Test suite for slide CLI commands."""

    def test_cli_build_slide(self, tmp_path: Path) -> None:
        """Verify `drawlib build slide` CLI command execution."""
        src_dir = tmp_path / "slide_src"
        out_dir = tmp_path / "slide_dist"
        src_dir.mkdir()

        (src_dir / "01_title.md").write_text(
            """---
layout: cover
---
# CLI Slide Test
""",
            encoding="utf-8",
        )

        res = run_drawlib_cli(["build", "slide", str(src_dir), "-o", str(out_dir), "--no-cache"])
        assert res.returncode == 0
        assert (out_dir / "index.html").is_file()
        assert (out_dir / "slide.css").is_file()

    def test_cli_init_slide(self, tmp_path: Path) -> None:
        """Verify `drawlib init slide` scaffolding."""
        target_dir = tmp_path / "my_presentation"
        res = run_drawlib_cli(["init", "slide", str(target_dir)])
        assert res.returncode == 0

        src_dir = target_dir / "slide_src"
        assert src_dir.is_dir()
        assert (src_dir / "01_title.md").is_file()
        assert (src_dir / "02_agenda.md").is_file()
        assert (src_dir / "build.sh").is_file()
        assert (src_dir / "serve.sh").is_file()
        assert (src_dir / "slide.css").is_file()
        assert (src_dir / "utils.py").is_file()
        assert (src_dir / "styles.py").is_file()

    @pytest.mark.parametrize("style_name", ["default", "google", "monochrome"])
    def test_cli_init_slide_styles(self, tmp_path: Path, style_name: str) -> None:
        """Verify `drawlib init slide --style <style>` deploys matching utils.py and slide.css."""
        target_dir = tmp_path / f"deck_{style_name}"
        res = run_drawlib_cli(["init", "slide", str(target_dir), "--style", style_name])
        assert res.returncode == 0

        src_dir = target_dir / "slide_src"
        utils_content = (src_dir / "utils.py").read_text(encoding="utf-8")
        styles_content = (src_dir / "styles.py").read_text(encoding="utf-8")
        css_content = (src_dir / "slide.css").read_text(encoding="utf-8")

        assert "draw_curved_agenda" in utils_content
        assert "draw_kpi_cards" in utils_content
        assert "service_card" in utils_content
        assert "connect" in utils_content

        if style_name == "google":
            assert "(26, 115, 232)" in utils_content
            assert "GoogleStyles" in styles_content
            assert "GoogleColors" in styles_content
            assert "Google Sans" in css_content
        elif style_name == "monochrome":
            assert "(20, 20, 20)" in utils_content
            assert "MonochromeStyles" in styles_content
            assert "MonochromeColors" in styles_content
            assert "Monochrome" in css_content or "--slide-bg: #ffffff" in css_content
        elif style_name == "default":
            assert "(37, 99, 235)" in utils_content
            assert "DefaultStyles" in styles_content
            assert "DefaultColors" in styles_content

    def test_cli_init_slide_unsupported_style(self, tmp_path: Path) -> None:
        """Verify `drawlib init slide --style invalid` fails with a helpful error."""
        target_dir = tmp_path / "deck_invalid"
        res = run_drawlib_cli(["init", "slide", str(target_dir), "--style", "unsupported_theme"])
        assert res.returncode != 0
        error_output = res.stderr + res.stdout
        assert "Unsupported slide style 'unsupported_theme'" in error_output
        assert "Available styles: default, google, monochrome" in error_output

    def test_python_api_init_slide_unsupported_style_raises(self, tmp_path: Path) -> None:
        """Verify init_project('slide', style='invalid') raises ValueError."""
        with pytest.raises(ValueError, match="Unsupported slide style 'unknown'"):
            init_project("slide", destination=tmp_path / "invalid_slide", style="unknown")

    def test_python_api_init_non_slide_uses_shared_utils(self, tmp_path: Path) -> None:
        """Verify non-slide projects use the general _shared/utils.py without slide macros."""
        target = tmp_path / "site_proj"
        init_project("site", destination=target)

        utils_content = (target / "docs_src" / "utils.py").read_text(encoding="utf-8")
        assert "service_card" in utils_content
        assert "connect" in utils_content
        assert "draw_curved_agenda" not in utils_content
        assert "draw_kpi_cards" not in utils_content
