# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Unit and integration tests for multi-core parallel `drawlib build` execution."""

from __future__ import annotations

import shutil
from collections.abc import Sequence
from pathlib import Path
from unittest.mock import patch

import pytest
from typer.testing import CliRunner

from drawlib._builder._common import (
    ENV_BUILD_WORKERS,
    BlockRenderJob,
    BuildImageCache,
    prerender_document_blocks,
    resolve_build_workers,
)
from drawlib._builder.doc_builder import (
    DrawlibBlockProcessor,
    build_docx,
    build_html,
    build_markdown,
    build_merged_html,
)
from drawlib._builder.image_builder import build_image
from drawlib._cli._drawlib import app as cli_app
from drawlib._slide import build_slide


def _setup_i18n_site_fixture(src_dir: Path) -> None:
    """Create a minimal 2-locale (`en`, `ja`) site project with 3 diagrams across 2 pages."""
    (src_dir / "en").mkdir(parents=True, exist_ok=True)
    (src_dir / "ja").mkdir(parents=True, exist_ok=True)
    (src_dir / "drawlib.toml").write_text(
        '[project]\ntype = "site"\ntitle = "Parallel Site"\n\n'
        '[i18n]\ndefault_lang = "en"\nlangs = ["en", "ja"]\n',
        encoding="utf-8",
    )
    (src_dir / "style.css").write_text("body { margin: 0; }\n", encoding="utf-8")
    (src_dir / "template.html").write_text(
        "<!DOCTYPE html><html><head><title>{{ title }}</title></head><body>{{ body }}</body></html>\n",
        encoding="utf-8",
    )
    (src_dir / "styles.py").write_text(
        "from drawlib.styles import Colors, Styles\n",
        encoding="utf-8",
    )

    (src_dir / "en" / "navbar.md").write_text(
        "# Docs\n- [Home](index.md)\n- [Guide](guide.md)\n",
        encoding="utf-8",
    )
    (src_dir / "ja" / "navbar.md").write_text(
        "# ドキュメント\n- [ホーム](index.md)\n- [ガイド](guide.md)\n",
        encoding="utf-8",
    )

    index_en = (
        "# Home\n\n"
        "Intro paragraph.\n\n"
        "```drawlib file=hero.png\n"
        "from drawlib.canvas import setup\n"
        "from drawlib.shapes import rectangle\n"
        "from drawlib.styles import Styles\n"
        "setup(width=40, height=20)\n"
        "rectangle((20, 10), width=30, height=10, style=Styles.Neutral, text='Hero')\n"
        "```\n"
    )
    index_ja = index_en.replace("# Home", "# ホーム").replace("Intro paragraph.", "紹介文。")

    guide_en = (
        "# Guide\n\n"
        "Details here.\n\n"
        "```drawlib file=step1.png\n"
        "from drawlib.canvas import setup\n"
        "from drawlib.shapes import circle\n"
        "from drawlib.styles import Styles\n"
        "setup(width=30, height=30)\n"
        "circle((15, 15), radius=8, style=Styles.Neutral, text='A')\n"
        "```\n\n"
        "```drawlib file=step2.png\n"
        "from drawlib.canvas import setup\n"
        "from drawlib.shapes import rectangle\n"
        "from drawlib.styles import Styles\n"
        "setup(width=40, height=20)\n"
        "rectangle((20, 10), width=24, height=10, style=Styles.Neutral, text='B')\n"
        "```\n"
    )
    guide_ja = guide_en.replace("# Guide", "# ガイド").replace("Details here.", "詳細説明。")

    (src_dir / "en" / "index.md").write_text(index_en, encoding="utf-8")
    (src_dir / "ja" / "index.md").write_text(index_ja, encoding="utf-8")
    (src_dir / "en" / "guide.md").write_text(guide_en, encoding="utf-8")
    (src_dir / "ja" / "guide.md").write_text(guide_ja, encoding="utf-8")


class TestResolveBuildWorkers:
    """Unit tests for `resolve_build_workers` auto formula, env vars, and validation."""

    @pytest.mark.parametrize(
        ("cpu_count", "expected"),
        [
            (None, 1),
            (1, 1),
            (2, 1),
            (3, 2),
            (4, 3),
            (8, 7),
            (9, 8),
            (16, 8),
            (64, 8),
        ],
    )
    def test_auto_worker_formula(
        self,
        monkeypatch: pytest.MonkeyPatch,
        cpu_count: int | None,
        expected: int,
    ) -> None:
        """Auto mode computes `1 <= (cpu_count - 1) <= 8`."""
        monkeypatch.delenv(ENV_BUILD_WORKERS, raising=False)
        with patch("os.cpu_count", return_value=cpu_count):
            assert resolve_build_workers("auto") == expected
            assert resolve_build_workers(None) == expected

    def test_explicit_and_env_precedence(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Explicit workers overrides DRAWLIB_BUILD_WORKERS; 'auto' honors DRAWLIB_BUILD_WORKERS."""
        monkeypatch.setenv(ENV_BUILD_WORKERS, "3")
        assert resolve_build_workers("auto") == 3
        assert resolve_build_workers(6) == 6
        assert resolve_build_workers("12") == 12

        monkeypatch.setenv(ENV_BUILD_WORKERS, "auto")
        with patch("os.cpu_count", return_value=6):
            assert resolve_build_workers("auto") == 5

    @pytest.mark.parametrize("bad_val", [0, -1, "0", "-4", "abc", "", "   ", True, False])
    def test_invalid_workers_rejected(
        self,
        monkeypatch: pytest.MonkeyPatch,
        bad_val: int | str | bool,
    ) -> None:
        """Non-positive integers, booleans, and non-numeric strings raise ValueError."""
        monkeypatch.delenv(ENV_BUILD_WORKERS, raising=False)
        with pytest.raises(ValueError, match="workers must be 'auto' or a positive integer >= 1"):
            resolve_build_workers(bad_val)

        monkeypatch.setenv(ENV_BUILD_WORKERS, "0")
        with pytest.raises(ValueError, match="workers must be 'auto' or a positive integer >= 1"):
            resolve_build_workers("auto")


class TestParallelBuildExecution:
    """Integration tests verifying parallel rendering across HTML, Markdown, PDF/DOCX, Slide, and Image."""

    def test_html_and_markdown_parallel_parity_and_warm_cache_skip(
        self,
        tmp_path: Path,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """`workers=1` and `workers=2` produce identical HTML/Markdown outputs, and warm cache skips pool."""
        src_dir = tmp_path / "site_src"
        _setup_i18n_site_fixture(src_dir)

        # 1. Sequential cold build (`workers=1`) with isolated cache CWD
        cwd_seq = tmp_path / "cwd_seq"
        cwd_seq.mkdir()
        monkeypatch.chdir(cwd_seq)
        out_html_seq = tmp_path / "out_html_seq"
        out_md_seq = tmp_path / "out_md_seq"
        build_html(str(src_dir), str(out_html_seq), workers=1)
        build_markdown(str(src_dir), str(out_md_seq), workers=1)

        # 2. Parallel cold build (`workers=2`) with fresh isolated cache CWD (3 shared renders across en+ja, not 6)
        cwd_par = tmp_path / "cwd_par"
        cwd_par.mkdir()
        monkeypatch.chdir(cwd_par)
        out_html_par = tmp_path / "out_html_par"
        prerender_counts: list[int] = []

        def _spy_prerender(
            jobs: Sequence[BlockRenderJob],
            *,
            cache: BuildImageCache,
            workers: int | str | None = "auto",
        ) -> int:
            cnt = prerender_document_blocks(jobs, cache=cache, workers=workers)
            prerender_counts.append(cnt)
            return cnt

        with patch("drawlib._builder.doc_builder.compiler.html.prerender_document_blocks", side_effect=_spy_prerender):
            build_html(str(src_dir), str(out_html_par), workers=2)
        assert prerender_counts == [3]

        assert (out_html_seq / "en" / "index.html").read_text("utf-8") == (
            out_html_par / "en" / "index.html"
        ).read_text("utf-8")
        assert (out_html_seq / "ja" / "guide.html").read_text("utf-8") == (
            out_html_par / "ja" / "guide.html"
        ).read_text("utf-8")
        for rel_img in ("index/hero.png", "guide/step1.png", "guide/step2.png"):
            assert (out_html_seq / "images" / rel_img).read_bytes() == (
                out_html_par / "images" / rel_img
            ).read_bytes()

        # 3. Delete output dir and verify warm-cache rebuild with `workers=2` does NOT spawn ProcessPoolExecutor
        shutil.rmtree(out_html_par)
        with patch(
            "drawlib._builder._common.parallel.ProcessPoolExecutor",
            side_effect=AssertionError("ProcessPoolExecutor should not be spawned on warm cache!"),
        ) as mock_pool:
            build_html(str(src_dir), str(out_html_par), workers=2)
            mock_pool.assert_not_called()
        for rel_img in ("index/hero.png", "guide/step1.png", "guide/step2.png"):
            assert (out_html_par / "images" / rel_img).is_file()

        # 4. Parallel cold Markdown build (`no_cache=True, workers=2`)
        out_md_par = tmp_path / "out_md_par"
        build_markdown(str(src_dir), str(out_md_par), no_cache=True, workers=2)
        assert (out_md_seq / "en" / "guide.md").read_text("utf-8") == (
            out_md_par / "en" / "guide.md"
        ).read_text("utf-8")

    def test_no_cache_inline_merged_html_and_docx_consume_prerendered_blobs(
        self,
        tmp_path: Path,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """`no_cache=True` with `workers=2` in merged HTML (PDF) and DOCX does not re-render in parent."""
        monkeypatch.chdir(tmp_path)
        doc_src = tmp_path / "doc_src"
        (doc_src / "en").mkdir(parents=True)
        (doc_src / "drawlib.toml").write_text(
            '[project]\ntype = "doc"\ntitle = "Report"\n\n[i18n]\ndefault_lang = "en"\nlangs = ["en"]\n',
            encoding="utf-8",
        )
        (doc_src / "style.css").write_text("body { font-family: sans-serif; }\n", encoding="utf-8")
        (doc_src / "en" / "01_ch1.md").write_text(
            "# Chapter 1\n\n"
            "```drawlib file=c1.png\n"
            "from drawlib.canvas import setup\n"
            "from drawlib.shapes import rectangle\n"
            "from drawlib.styles import Styles\n"
            "setup(width=30, height=20)\n"
            "rectangle((15, 10), width=20, height=10, style=Styles.Neutral, text='C1')\n"
            "```\n",
            encoding="utf-8",
        )
        (doc_src / "en" / "02_ch2.md").write_text(
            "# Chapter 2\n\n"
            "```drawlib file=c2.png\n"
            "from drawlib.canvas import setup\n"
            "from drawlib.shapes import circle\n"
            "from drawlib.styles import Styles\n"
            "setup(width=30, height=20)\n"
            "circle((15, 10), radius=6, style=Styles.Neutral, text='C2')\n"
            "```\n",
            encoding="utf-8",
        )

        with patch.object(
            DrawlibBlockProcessor,
            "_exec_code_block",
            side_effect=AssertionError("Parent should not re-execute pre-rendered blocks!"),
        ):
            merged_html, _ = build_merged_html(
                inputs=[str(doc_src / "en")],
                no_cache=True,
                project_root=str(doc_src),
                workers=2,
            )
            assert "data:image/png;base64," in merged_html

            out_docx = tmp_path / "report.docx"
            docx_res = build_docx(
                str(doc_src),
                output_file=str(out_docx),
                no_cache=True,
                workers=2,
            )
            assert Path(docx_res).is_file()

        assert not (tmp_path / ".drawlib" / "cache.db").exists()

    def test_slide_parallel_build_preserves_slide_context(
        self,
        tmp_path: Path,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """Parallel `build_slide` preserves `SlideContext` (`current_slide().text`) identically."""
        monkeypatch.chdir(tmp_path)
        slide_src = tmp_path / "deck_src"
        (slide_src / "en").mkdir(parents=True)
        (slide_src / "drawlib.toml").write_text(
            '[project]\ntype = "slide"\ntitle = "Deck"\n\n[i18n]\ndefault_lang = "en"\nlangs = ["en"]\n',
            encoding="utf-8",
        )
        for idx in (1, 2):
            (slide_src / "en" / f"0{idx}_slide.md").write_text(
                f"# Slide {idx}\n\n"
                f"```drawlib file=s{idx}.png\n"
                "from drawlib.canvas import setup\n"
                "from drawlib.shapes import rectangle\n"
                "from drawlib.slide import current_slide\n"
                "from drawlib.styles import Styles\n"
                "setup(width=40, height=20)\n"
                "rectangle((20, 10), width=30, height=10, style=Styles.Neutral, "
                "text=current_slide.format('{index}/{total}'))\n"
                "```\n",
                encoding="utf-8",
            )

        out_seq = tmp_path / "deck_seq"
        out_par = tmp_path / "deck_par"
        build_slide(str(slide_src), str(out_seq), no_cache=True, workers=1)
        build_slide(str(slide_src), str(out_par), no_cache=True, workers=2)

        assert (out_seq / "en" / "index.html").read_text("utf-8") == (
            out_par / "en" / "index.html"
        ).read_text("utf-8")
        assert (out_seq / "images" / "01_slide" / "s1.png").read_bytes() == (
            out_par / "images" / "01_slide" / "s1.png"
        ).read_bytes()
        assert (out_seq / "images" / "02_slide" / "s2.png").read_bytes() == (
            out_par / "images" / "02_slide" / "s2.png"
        ).read_bytes()
        assert (out_par / "images" / "01_slide" / "s1.png").read_bytes() != (
            out_par / "images" / "02_slide" / "s2.png"
        ).read_bytes()

    def test_standalone_image_parallel_and_disable_auto_clear_fallback(
        self,
        tmp_path: Path,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """`build_image` parallelizes directory `.py` scripts and falls back to sequential on `--disable-auto-clear`."""
        scripts_dir = tmp_path / "scripts"
        scripts_dir.mkdir()
        out_seq = tmp_path / "imgs_seq"
        out_par = tmp_path / "imgs_par"

        for idx in (1, 2, 3):
            (scripts_dir / f"0{idx}_draw.py").write_text(
                "from drawlib.canvas import save, setup\n"
                "from drawlib.shapes import rectangle\n"
                "from drawlib.styles import Styles\n"
                "setup(width=30, height=20)\n"
                f"rectangle((15, 10), width=20, height=10, style=Styles.Neutral, text='Img{idx}')\n"
                f"save('img{idx}.png')\n",
                encoding="utf-8",
            )

        cwd_img_seq = tmp_path / "cwd_img_seq"
        cwd_img_seq.mkdir()
        monkeypatch.chdir(cwd_img_seq)
        build_image(str(scripts_dir), str(out_seq), workers=1)

        cwd_img_par = tmp_path / "cwd_img_par"
        cwd_img_par.mkdir()
        monkeypatch.chdir(cwd_img_par)
        build_image(str(scripts_dir), str(out_par), workers=2)

        for idx in (1, 2, 3):
            assert (out_seq / f"img{idx}.png").read_bytes() == (out_par / f"img{idx}.png").read_bytes()

        # Verify disable_auto_clear=True falls back to sequential in-process so state accumulates
        shared_dir = tmp_path / "shared_state"
        shared_dir.mkdir()
        out_shared = tmp_path / "out_shared"
        (shared_dir / "01_base.py").write_text(
            "from drawlib.canvas import save, setup\n"
            "from drawlib.shapes import rectangle\n"
            "from drawlib.styles import Styles\n"
            "setup(width=40, height=20)\n"
            "rectangle((10, 10), width=12, height=10, style=Styles.Neutral, text='Left')\n"
            "save('step1.png')\n",
            encoding="utf-8",
        )
        (shared_dir / "02_overlay.py").write_text(
            "from drawlib.canvas import save\n"
            "from drawlib.shapes import circle\n"
            "from drawlib.styles import Styles\n"
            "circle((30, 10), radius=5, style=Styles.Neutral, text='Right')\n"
            "save('step2.png')\n",
            encoding="utf-8",
        )
        build_image(
            str(shared_dir),
            str(out_shared),
            disable_auto_clear=True,
            no_cache=True,
            workers=2,
        )
        assert (out_shared / "step1.png").is_file()
        assert (out_shared / "step2.png").is_file()

    def test_nested_get_dimage_from_code_inside_parallel_workers(
        self,
        tmp_path: Path,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """Non-daemonic `ProcessPoolExecutor` workers support nested `get_dimage_from_code()` child processes."""
        monkeypatch.chdir(tmp_path)
        src_dir = tmp_path / "nested_src"
        (src_dir / "en").mkdir(parents=True)
        (src_dir / "drawlib.toml").write_text(
            '[project]\ntype = "doc"\n\n[i18n]\ndefault_lang = "en"\nlangs = ["en"]\n',
            encoding="utf-8",
        )
        (src_dir / "style.css").write_text("body {}\n", encoding="utf-8")
        (src_dir / "template.html").write_text("<html><body>{{ body }}</body></html>\n", encoding="utf-8")

        nested_block = (
            "from drawlib.canvas import setup\n"
            "from drawlib.images import get_dimage_from_code, image\n"
            "sub = get_dimage_from_code(\n"
            "    'from drawlib.canvas import setup\\n'\n"
            "    'from drawlib.shapes import circle\\n'\n"
            "    'from drawlib.styles import Styles\\n'\n"
            "    'setup(width=20, height=20)\\n'\n"
            "    'circle((10, 10), radius=6, style=Styles.Neutral)\\n'\n"
            ")\n"
            "setup(width=40, height=20)\n"
            "image((20, 10), width=15, image=sub)\n"
        )
        (src_dir / "en" / "01_doc.md").write_text(
            f"# Nested\n\n```drawlib file=n1.png\n{nested_block}```\n\n```drawlib file=n2.png\n{nested_block}```\n",
            encoding="utf-8",
        )

        out_html = tmp_path / "nested_html"
        build_html(str(src_dir), str(out_html), no_cache=True, workers=2)
        assert (out_html / "images" / "01_doc" / "n1.png").is_file()
        assert (out_html / "images" / "01_doc" / "n2.png").is_file()

    def test_worker_error_propagates_with_file_and_line_and_cli_option(
        self,
        tmp_path: Path,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """Exceptions in parallel workers fail fast with source location, and CLI `-w` validates input."""
        monkeypatch.chdir(tmp_path)
        src_dir = tmp_path / "err_src"
        (src_dir / "en").mkdir(parents=True)
        (src_dir / "drawlib.toml").write_text(
            '[project]\ntype = "doc"\n\n[i18n]\ndefault_lang = "en"\nlangs = ["en"]\n',
            encoding="utf-8",
        )
        (src_dir / "style.css").write_text("body {}\n", encoding="utf-8")
        (src_dir / "template.html").write_text("<html><body>{{ body }}</body></html>\n", encoding="utf-8")
        (src_dir / "en" / "01_bad.md").write_text(
            "# Broken\n\n"
            "```drawlib file=ok.png\n"
            "from drawlib.canvas import setup\n"
            "setup(width=20, height=20)\n"
            "```\n\n"
            "```drawlib file=boom.png\n"
            "class LocalCustomError(Exception):\n"
            "    pass\n"
            "raise LocalCustomError('intentional failure')\n"
            "```\n",
            encoding="utf-8",
        )

        with pytest.raises(RuntimeError, match=r"01_bad\.md.*intentional failure"):
            build_html(str(src_dir), str(tmp_path / "err_out"), no_cache=True, workers=2)

        runner = CliRunner()
        bad_cli = runner.invoke(cli_app, ["build", "html", str(src_dir), "-w", "0"])
        assert bad_cli.exit_code == 1
        assert "workers must be 'auto' or a positive integer >= 1" in (bad_cli.stdout + bad_cli.stderr)
