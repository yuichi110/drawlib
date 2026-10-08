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

import base64
import importlib.machinery
import importlib.util
from importlib.resources import files
from pathlib import Path

import pytest

import drawlib.slide as slide_module
from drawlib._slide import (
    BoundingBox,
    build_slide,
)
from drawlib._slide._blocks import extract_slide_notes
from drawlib._slide.base import reset_slide_context, set_slide_context
from drawlib._templates import get_css, get_slide_js, init_project, list_slide_css
from drawlib.canvas import clear, save, setup
from tests.drawlib.cli.common import run_drawlib_cli

_SLIDE_UTILS_PATH = Path(str(files("drawlib._templates").joinpath("project/slide/utils/google.py.template")))
_loader = importlib.machinery.SourceFileLoader("_slide_template_utils", str(_SLIDE_UTILS_PATH))
_spec = importlib.util.spec_from_loader(_loader.name, _loader)
assert _spec is not None
_slide_utils = importlib.util.module_from_spec(_spec)
_loader.exec_module(_slide_utils)
draw_curved_agenda = _slide_utils.draw_curved_agenda
draw_kpi_cards = _slide_utils.draw_kpi_cards


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
        assert hasattr(slide_module, "SlideContext")
        assert hasattr(slide_module, "current_slide")
        assert hasattr(slide_module, "build_slide")
        assert slide_module.BoundingBox is BoundingBox

    def test_current_slide_introspection(self) -> None:
        """Verify current_slide introspection properties and format method."""
        # Outside of build context, current_slide defaults safely to 1/1
        assert slide_module.current_slide.index == 1
        assert slide_module.current_slide.total == 1
        assert slide_module.current_slide.text == "1 / 1"
        assert str(slide_module.current_slide) == "1 / 1"
        assert slide_module.current_slide.format("{index} of {total}") == "1 of 1"

        # Within slide context
        token = set_slide_context(4, 9)
        try:
            assert slide_module.current_slide.index == 4
            assert slide_module.current_slide.total == 9
            assert slide_module.current_slide.text == "4 / 9"
            assert str(slide_module.current_slide) == "4 / 9"
            assert slide_module.current_slide.format("Slide {index} / {total}") == "Slide 4 / 9"
        finally:
            reset_slide_context(token)

        assert slide_module.current_slide.index == 1


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
            """::: block (160, 240) (1600, 600)
# Drawlib Test Deck
## Presentation as Code
:::
""",
            encoding="utf-8",
        )

        (src_dir / "utils.py").write_text(_SLIDE_UTILS_PATH.read_text(encoding="utf-8"), encoding="utf-8")

        (src_dir / "02_agenda.md").write_text(
            """::: block (80, 40) (1760, 60)
# Presentation Agenda
:::

::: block (80, 140) (700, 840)
# Topics
- Key milestones
:::

::: block (820, 140) (1040, 860)
```drawlib file:agenda.svg
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
:::
""",
            encoding="utf-8",
        )

        (src_dir / "03_features.md").write_text(
            """::: block (80, 40) (1760, 60)
# Features
:::

::: block (80, 140) (740, 840)
# Declarative Illustrations

- Pure Python code
- Native SVG text elements
:::

::: block (880, 140) (960, 840)
```drawlib file:diag.svg
from drawlib.shapes import rectangle
from drawlib.styles import Styles
from drawlib.slide import current_slide
from drawlib.text import text
from drawlib.canvas import setup, clear

clear()
setup(width=100, height=60)
rectangle((50, 30), width=40, height=20, style=Styles.PrimaryFlat, text="Box", text_style=Styles.WhiteBold)
text((50, 10), current_slide.text, style=Styles.Dark)
```
:::
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
        assert (out_dir / "style.css").is_file()
        assert (out_dir / "slide.js").is_file()
        assert (out_dir / "images" / "02_agenda" / "agenda.svg").is_file()
        assert (out_dir / "images" / "03_features" / "diag.svg").is_file()

        # Check SVG has text
        agenda_svg = (out_dir / "images" / "02_agenda" / "agenda.svg").read_text(encoding="utf-8")
        assert "First Step" in agenda_svg
        assert "はじめに" in agenda_svg

        # Check current_slide in diag.svg
        diag_svg = (out_dir / "images" / "03_features" / "diag.svg").read_text(encoding="utf-8")
        assert "3 / 3" in diag_svg

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

    def test_build_slide_full_bleed_canvas(self, tmp_path: Path) -> None:
        """Verify full-bleed 1920x1080 stage renders pure section without injected chrome."""
        src_dir = tmp_path / "slide_src"
        out_dir = tmp_path / "slide"
        src_dir.mkdir()

        (src_dir / "01_canvas.md").write_text(
            """::: block (0, 0) (1920, 1080)
```drawlib file:hero.svg
from drawlib.canvas import setup, clear
from drawlib.shapes import rectangle
from drawlib.slide import current_slide
from drawlib.text import text
from drawlib.styles import Styles

clear()
setup(width=192, height=108)
rectangle((96, 54), width=180, height=90, style=Styles.PrimaryFlat)
text((96, 20), current_slide.text, style=Styles.White)
```
:::
""",
            encoding="utf-8",
        )

        result_html = build_slide(str(src_dir), str(out_dir), no_cache=True)
        content = Path(result_html).read_text(encoding="utf-8")
        assert "slide-header" not in content
        assert "slide-footer" not in content
        assert "layout-canvas" not in content
        assert "slide-block" in content
        assert 'data-slide-index="1"' in content
        assert (out_dir / "images" / "01_canvas" / "hero.svg").is_file()
        hero_svg = (out_dir / "images" / "01_canvas" / "hero.svg").read_text(encoding="utf-8")
        assert "1 / 1" in hero_svg

    def test_build_slide_container_boxes_and_coordinates(self, tmp_path: Path) -> None:
        """Verify ::: block container syntax creates absolutely positioned, styled blocks."""
        src_dir = tmp_path / "slide_src"
        out_dir = tmp_path / "slide"
        src_dir.mkdir()

        (src_dir / "01_boxes.md").write_text(
            """::: block (80, 140) (740, 480) font:21px compact z:10
# Ingress Controller
- **TLS**: Terminated at edge
- **Routing**: Path-based dispatch
:::

::: block (80, 660) (740, 320) align:center
> Note: Zero-trust network policy active.
:::
""",
            encoding="utf-8",
        )

        result_html = build_slide(str(src_dir), str(out_dir), no_cache=True)
        content = Path(result_html).read_text(encoding="utf-8")
        assert "slide-block" in content
        assert "left: 80.0px; top: 140.0px; width: 740.0px; height: 480.0px;" in content
        assert "font-size: 21px;" in content
        assert "compact" in content
        assert "z-index: 10;" in content
        assert "left: 80.0px; top: 660.0px; width: 740.0px; height: 320.0px;" in content
        assert "text-align: center;" in content

    def test_build_slide_chrome_free_by_default(self, tmp_path: Path) -> None:
        """Verify slides are completely chrome-free by default without injected header/footer/paginate."""
        src_dir = tmp_path / "slide_src"
        out_dir = tmp_path / "slide"
        src_dir.mkdir()

        (src_dir / "01_clean.md").write_text(
            """::: block (80, 140) (800, 400)
# Clean Slide Without Chrome
- Focused content only
:::
""",
            encoding="utf-8",
        )

        result_html = build_slide(str(src_dir), str(out_dir), no_cache=True)
        content = Path(result_html).read_text(encoding="utf-8")
        assert "slide-header" not in content
        assert "slide-footer" not in content
        assert "page-number" not in content
        assert "layout-" not in content
        assert "Clean Slide Without Chrome" in content

    def test_build_slide_block_options_and_styling(self, tmp_path: Path) -> None:
        """Verify ::: block options: font_size, compact, align, z-index, and custom styles."""
        src_dir = tmp_path / "slide_src"
        out_dir = tmp_path / "slide"
        src_dir.mkdir()

        (src_dir / "01_options.md").write_text(
            """::: block (80, 140) (740, 840) font:20px compact style:"transform: translateY(-25px);"
# Title Inside Block
- Point 1
- Point 2
:::
""",
            encoding="utf-8",
        )

        result_html = build_slide(str(src_dir), str(out_dir), no_cache=True)
        content = Path(result_html).read_text(encoding="utf-8")
        assert "transform: translateY(-25px);" in content
        assert "font-size: 20px;" in content
        assert "compact" in content
        assert "slide-block" in content
        assert "left: 80.0px; top: 140.0px; width: 740.0px; height: 840.0px;" in content

    def test_build_slide_cleans_obsolete_output_files(self, tmp_path: Path) -> None:
        """Verify build_slide clears previous output files to avoid obsolete ghost files."""
        src_dir = tmp_path / "slide_src"
        out_dir = tmp_path / "slide"
        src_dir.mkdir()
        out_dir.mkdir()

        # Seed old/obsolete files in output directory
        (out_dir / "obsolete.svg").write_text("<svg>old</svg>", encoding="utf-8")
        old_images = out_dir / "images" / "old_slide"
        old_images.mkdir(parents=True)
        (old_images / "legacy.svg").write_text("<svg>legacy</svg>", encoding="utf-8")

        (src_dir / "01_slide.md").write_text(
            """::: block (80, 140) (800, 400)
# Fresh Slide
:::
""",
            encoding="utf-8",
        )

        build_slide(str(src_dir), str(out_dir), no_cache=True)

        assert not (out_dir / "obsolete.svg").exists()
        assert not (out_dir / "images" / "old_slide").exists()
        assert (out_dir / "index.html").is_file()
        assert (out_dir / "style.css").is_file()


class TestSlideCli:
    """Test suite for slide CLI commands."""

    def test_cli_build_slide(self, tmp_path: Path) -> None:
        """Verify `drawlib build slide` CLI command execution."""
        src_dir = tmp_path / "slide_src"
        out_dir = tmp_path / "slide_dist"
        src_dir.mkdir()

        (src_dir / "01_title.md").write_text(
            """::: block (160, 240) (1600, 600)
# CLI Slide Test
:::
""",
            encoding="utf-8",
        )

        res = run_drawlib_cli(["build", "slide", str(src_dir), "-o", str(out_dir), "--theme", "google", "--no-cache"])
        assert res.returncode == 0
        assert (out_dir / "index.html").is_file()
        assert (out_dir / "style.css").is_file()
        assert (out_dir / "README.md").is_file()
        assert "Presenter View" in (out_dir / "README.md").read_text(encoding="utf-8")

    def test_cli_init_slide(self, tmp_path: Path) -> None:
        """Verify `drawlib init slide` scaffolding."""
        target_dir = tmp_path / "my_presentation"
        target_dir.mkdir()
        res = run_drawlib_cli(["init", "slide"], cwd=str(target_dir))
        assert res.returncode == 0

        src_dir = target_dir / "slide_src"
        assert src_dir.is_dir()
        assert (src_dir / "01_title.md").is_file()
        assert (src_dir / "02_agenda.md").is_file()
        assert (src_dir / "build.sh").is_file()
        assert (src_dir / "build_image.sh").is_file()
        assert (src_dir / "serve.sh").is_file()
        assert (src_dir / "style.css").is_file()
        assert (src_dir / "utils.py").is_file()
        assert (src_dir / "styles.py").is_file()

    @pytest.mark.parametrize("style_name", ["default", "google", "monochrome"])
    def test_cli_init_slide_styles(self, tmp_path: Path, style_name: str) -> None:
        """Verify `drawlib init slide --style <style>` deploys matching utils.py and style.css."""
        target_dir = tmp_path / f"deck_{style_name}"
        target_dir.mkdir()
        res = run_drawlib_cli(["init", "slide", "--style", style_name], cwd=str(target_dir))
        assert res.returncode == 0

        src_dir = target_dir / "slide_src"
        utils_content = (src_dir / "utils.py").read_text(encoding="utf-8")
        styles_content = (src_dir / "styles.py").read_text(encoding="utf-8")
        css_content = (src_dir / "style.css").read_text(encoding="utf-8")

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
        target_dir.mkdir()
        res = run_drawlib_cli(["init", "slide", "--style", "unsupported_theme"], cwd=str(target_dir))
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

    def test_build_slide_copies_static_assets(self, tmp_path: Path) -> None:
        """Verify static assets in _assets are copied to output directory."""
        src_dir = tmp_path / "slide_src"
        out_dir = tmp_path / "slide"
        src_dir.mkdir()
        assets_dir = src_dir / "_assets"
        assets_dir.mkdir()
        (assets_dir / "logo.png").write_bytes(b"\x89PNG\r\n\x1a\nfakeimage")

        (src_dir / "01_title.md").write_text(
            """
::: block (100, 100) (400, 400)
![Logo](_assets/logo.png)
:::
""",
            encoding="utf-8",
        )

        build_slide(str(src_dir), str(out_dir))

        assert (out_dir / "_assets" / "logo.png").is_file()
        assert (out_dir / "_assets" / "logo.png").read_bytes() == b"\x89PNG\r\n\x1a\nfakeimage"
        html_content = (out_dir / "index.html").read_text(encoding="utf-8")
        assert '<img src="_assets/logo.png" alt="Logo" />' in html_content

    def test_build_slide_page_numbers_unique_per_slide(self, tmp_path: Path) -> None:
        """Verify identical page number code blocks produce unique cached SVGs per slide."""
        src_dir = tmp_path / "slide_src"
        out_dir = tmp_path / "slide"
        src_dir.mkdir()

        page_block = """
::: block (1700, 1010) (140, 30)
```drawlib file:page.svg
from drawlib.canvas import clear, setup
from drawlib.slide import current_slide
from drawlib.text import text
from drawlib.styles import Styles

clear()
setup(width=14, height=3, alpha=0.0)
text((7, 1.5), current_slide.text, style=Styles.Black)
```
:::
"""

        (src_dir / "01_first.md").write_text(f"# Slide 1\n{page_block}", encoding="utf-8")
        (src_dir / "02_second.md").write_text(f"# Slide 2\n{page_block}", encoding="utf-8")
        (src_dir / "03_third.md").write_text(f"# Slide 3\n{page_block}", encoding="utf-8")

        build_slide(str(src_dir), str(out_dir))

        svg1 = (out_dir / "images" / "01_first" / "page.svg").read_text(encoding="utf-8")
        svg2 = (out_dir / "images" / "02_second" / "page.svg").read_text(encoding="utf-8")
        svg3 = (out_dir / "images" / "03_third" / "page.svg").read_text(encoding="utf-8")

        assert "1 / 3" in svg1
        assert "2 / 3" in svg2
        assert "3 / 3" in svg3

    def test_build_slide_page_numbers_invalidation_when_total_slides_changes(self, tmp_path: Path) -> None:
        """Verify adding a slide invalidates cache across deck and updates total slides in page numbers."""
        src_dir = tmp_path / "slide_src"
        out_dir = tmp_path / "slide"
        src_dir.mkdir()

        page_block = """
::: block (1700, 1010) (140, 30)
```drawlib file:page.svg
from drawlib.canvas import clear, setup
from drawlib.slide import current_slide
from drawlib.text import text
from drawlib.styles import Styles

clear()
setup(width=14, height=3, alpha=0.0)
text((7, 1.5), current_slide.text, style=Styles.Black)
```
:::
"""

        (src_dir / "01_first.md").write_text(f"# Slide 1\n{page_block}", encoding="utf-8")
        (src_dir / "02_second.md").write_text(f"# Slide 2\n{page_block}", encoding="utf-8")
        (src_dir / "03_third.md").write_text(f"# Slide 3\n{page_block}", encoding="utf-8")

        build_slide(str(src_dir), str(out_dir))
        assert "1 / 3" in (out_dir / "images" / "01_first" / "page.svg").read_text(encoding="utf-8")

        # Now add a 4th slide and re-build with cache enabled
        (src_dir / "04_fourth.md").write_text(f"# Slide 4\n{page_block}", encoding="utf-8")
        build_slide(str(src_dir), str(out_dir))

        svg1 = (out_dir / "images" / "01_first" / "page.svg").read_text(encoding="utf-8")
        svg4 = (out_dir / "images" / "04_fourth" / "page.svg").read_text(encoding="utf-8")
        assert "1 / 4" in svg1
        assert "4 / 4" in svg4

    def test_build_slide_anim_playback_markup(self, tmp_path: Path) -> None:
        """Verify animated drawlib blocks with anim-trigger/loop/pause emit <canvas> player markup with data-base64."""
        src_dir = tmp_path / "slide_src"
        out_dir = tmp_path / "slide"
        src_dir.mkdir()

        (src_dir / "01_anim.md").write_text(
            """::: block (80, 140) (800, 500)
```drawlib file:flow anim-trigger:click anim-loop:once anim-pause:2,4
from drawlib.anim import Animation
from drawlib.canvas import clear, save, setup
from drawlib.shapes import rectangle
from drawlib.styles import Styles

clear()
setup(width=40, height=20)
anim = Animation(fps=2.0, loop=0)
for i in range(6):
    with anim.frame(duration=0.5):
        rectangle((10 + i * 3, 10), width=6, height=6, style=Styles.PrimaryFlat)
save()
```
:::

::: block (920, 140) (800, 500)
```drawlib file:static_box.png
from drawlib.canvas import clear, setup
from drawlib.shapes import rectangle
from drawlib.styles import Styles

clear()
setup(width=40, height=20)
rectangle((20, 10), width=10, height=10, style=Styles.Neutral)
```
:::
""",
            encoding="utf-8",
        )

        result_html = build_slide(str(src_dir), str(out_dir), no_cache=True)
        html_content = Path(result_html).read_text(encoding="utf-8")

        # Animated block without extension defaults to APNG (.png)
        anim_file = out_dir / "images" / "01_anim" / "flow.png"
        assert anim_file.is_file()
        expected_b64 = base64.b64encode(anim_file.read_bytes()).decode("ascii")

        # Animated block with playback options -> canvas container + play badge + data-base64
        assert 'class="drawlib-image drawlib-anim-container"' in html_content
        assert 'data-anim-trigger="click"' in html_content
        assert 'data-anim-loop="once"' in html_content
        assert 'data-anim-pause="2,4"' in html_content
        assert (
            f'<canvas class="drawlib-anim-canvas" data-src="images/01_anim/flow.png" '
            f'data-base64="{expected_b64}"'
        ) in html_content
        assert 'class="anim-play-badge"' in html_content

        # Static block without playback options -> standard <img>
        assert '<img src="images/01_anim/static_box.png"' in html_content

    def test_extract_slide_notes_single_and_multiple(self) -> None:
        """Verify extract_slide_notes extracts ::: note / ::: notes and joins multiple blocks with a blank line."""
        raw = """::: block (80, 40) (1760, 60)
# Slide Title
:::

::: note
First speaker note paragraph.
:::

::: notes
Second speaker note with **bold** text.
:::
"""
        cleaned, notes_html = extract_slide_notes(raw)
        assert "::: note" not in cleaned
        assert "First speaker note paragraph." not in cleaned
        assert "# Slide Title" in cleaned
        assert "<p>First speaker note paragraph.</p>" in notes_html
        assert "<p>Second speaker note with <strong>bold</strong> text.</p>" in notes_html

    def test_build_slide_speaker_notes_and_presenter_button(self, tmp_path: Path) -> None:
        """Verify build_slide compiles ::: note blocks into .slide-notes and emits #btn-presenter."""
        src_dir = tmp_path / "slide_src"
        out_dir = tmp_path / "slide"
        src_dir.mkdir()

        (src_dir / "01_with_notes.md").write_text(
            """::: block (80, 40) (1760, 60)
# Slide With Notes
:::

::: note
Note block one.
:::

::: note
- Bullet item A
- Bullet item B
:::
""",
            encoding="utf-8",
        )

        (src_dir / "02_no_notes.md").write_text(
            """::: block (80, 40) (1760, 60)
# Slide Without Notes
:::
""",
            encoding="utf-8",
        )

        result_html = build_slide(str(src_dir), str(out_dir), no_cache=True)
        html_content = Path(result_html).read_text(encoding="utf-8")

        assert '<aside class="slide-notes" hidden>' in html_content
        assert "<p>Note block one.</p>" in html_content
        assert "<li>Bullet item A</li>" in html_content
        assert html_content.count('<aside class="slide-notes" hidden></aside>') == 1
        assert 'id="btn-presenter"' in html_content

    def test_build_slide_svg_font_auto_bundling_and_cache(self, tmp_path: Path) -> None:
        """Verify SVG font auto-bundling copies used fonts and injects @font-face even on cache hit."""
        src_dir = tmp_path / "slide_src"
        out_dir_1 = tmp_path / "slide_out_1"
        out_dir_2 = tmp_path / "slide_out_2"
        src_dir.mkdir()

        custom_font_path = (
            Path(__file__).resolve().parents[2] / "assets" / "avenger" / "regular.ttf"
        ).as_posix()

        (src_dir / "01_fonts.md").write_text(
            f"""::: block (80, 40) (1760, 900)
```drawlib file:fonts_demo.svg
from drawlib.canvas import setup, clear
from drawlib.fonts import FontFile, FontRoboto
from drawlib.icons import phosphor
from drawlib.styles import Colors, Style, Styles
from drawlib.text import text

clear()
setup(width=100, height=50)
custom_font = FontFile("{custom_font_path}")
text((20, 40), "Regular Text", style=Style(text_color=Colors.Black, text_font=FontRoboto.ROBOTO_REGULAR, text_size=14))
text((20, 25), "Bold Text", style=Style(text_color=Colors.Black, text_font=FontRoboto.ROBOTO_BOLD, text_size=14))
text((20, 10), "Custom Font", style=Style(text_color=Colors.Black, text_font=custom_font, text_size=14))
phosphor.rocket((75, 25), width=12, style=Styles.Primary)
```
:::
""",
            encoding="utf-8",
        )

        # 1. Build with cache enabled (cold cache -> populates SQLite cache)
        result_html_1 = build_slide(str(src_dir), str(out_dir_1), no_cache=False)
        html_1 = Path(result_html_1).read_text(encoding="utf-8")
        css_1 = (out_dir_1 / "style.css").read_text(encoding="utf-8")
        svg_disk_1 = (out_dir_1 / "images" / "01_fonts" / "fonts_demo.svg").read_text(encoding="utf-8")

        # Verify SVG on disk has metadata comment, while inline HTML strips it
        assert "<!-- drawlib-svg-fonts:" in svg_disk_1
        assert "<!-- drawlib-svg-fonts:" not in html_1

        # Verify collision-free drawlib-* font families in inline SVG
        assert "drawlib-roboto-regular" in html_1
        assert "drawlib-roboto-bold" in html_1
        assert "drawlib-phosphor-regular" in html_1
        assert "drawlib-custom-regular-" in html_1

        # Verify font files copied into _assets/fonts/
        assert (out_dir_1 / "_assets" / "fonts" / "roboto" / "regular.ttf").is_file()
        assert (out_dir_1 / "_assets" / "fonts" / "roboto" / "bold.ttf").is_file()
        assert (out_dir_1 / "_assets" / "fonts" / "phosphor" / "regular.ttf").is_file()
        custom_fonts_dir = out_dir_1 / "_assets" / "fonts" / "custom"
        assert custom_fonts_dir.is_dir()
        assert len(list(custom_fonts_dir.glob("*_regular.ttf"))) == 1

        # Verify @font-face declarations in style.css
        assert "font-family: 'drawlib-roboto-regular';" in css_1
        assert "src: url('_assets/fonts/roboto/regular.ttf') format('truetype');" in css_1
        assert "font-family: 'drawlib-roboto-bold';" in css_1
        assert "font-family: 'drawlib-phosphor-regular';" in css_1

        # 2. Rebuild into a fresh output directory using warm cache
        build_slide(str(src_dir), str(out_dir_2), no_cache=False)
        css_2 = (out_dir_2 / "style.css").read_text(encoding="utf-8")
        assert (out_dir_2 / "_assets" / "fonts" / "roboto" / "regular.ttf").is_file()
        assert (out_dir_2 / "_assets" / "fonts" / "roboto" / "bold.ttf").is_file()
        assert (out_dir_2 / "_assets" / "fonts" / "phosphor" / "regular.ttf").is_file()
        assert "font-family: 'drawlib-phosphor-regular';" in css_2

    def test_build_slide_with_chapter_subdirectories(self, tmp_path: Path) -> None:
        """Verify slides in chapter subdirectories sort in order, resolve root utils/styles, and avoid collisions."""
        src_dir = tmp_path / "slide_src"
        out_dir = tmp_path / "slide_out"
        src_dir.mkdir()

        (src_dir / "utils.py").write_text(
            """from drawlib.canvas import clear, setup
from drawlib.slide import current_slide
from drawlib.styles import Styles
from drawlib.text import text

def draw_page_number():
    clear()
    setup(width=14, height=3, alpha=0.0)
    text((7, 1.5), current_slide.text, style=Styles.Black)
""",
            encoding="utf-8",
        )

        ch0 = src_dir / "00_opening"
        ch1 = src_dir / "01_chapter_one"
        ch0.mkdir()
        ch1.mkdir()

        slide_tpl = """::: block (80, 140) (1760, 840)
# {title}
:::

::: block (1700, 1010) (140, 30)
```drawlib file:page.svg
import utils
utils.draw_page_number()
```
:::
"""
        (ch0 / "01_title.md").write_text(slide_tpl.format(title="Opening Slide"), encoding="utf-8")
        (ch1 / "01_section.md").write_text(slide_tpl.format(title="Chapter 1 Divider"), encoding="utf-8")
        (ch1 / "02_content.md").write_text(slide_tpl.format(title="Chapter 1 Content"), encoding="utf-8")

        result_html = build_slide(str(src_dir), str(out_dir), no_cache=True)
        html = Path(result_html).read_text(encoding="utf-8")

        assert "Opening Slide" in html
        assert "Chapter 1 Divider" in html
        assert "Chapter 1 Content" in html
        assert html.index("Opening Slide") < html.index("Chapter 1 Divider") < html.index("Chapter 1 Content")

        svg1 = (out_dir / "images" / "00_opening" / "01_title" / "page.svg").read_text(encoding="utf-8")
        svg2 = (out_dir / "images" / "01_chapter_one" / "01_section" / "page.svg").read_text(encoding="utf-8")
        svg3 = (out_dir / "images" / "01_chapter_one" / "02_content" / "page.svg").read_text(encoding="utf-8")
        assert "1 / 3" in svg1
        assert "2 / 3" in svg2
        assert "3 / 3" in svg3

