# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Unit tests for the Jupyter / Google Colab (.ipynb + HTML + AI Dry-Run) builder."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from drawlib._builder._common import JupyterConfig, load_project_manifest
from drawlib._builder.doc_builder import (
    NotebookExecutionError,
    build_docx,
    build_html,
    build_ipynb_dict,
    build_jupyter,
    build_markdown,
    build_pdf,
    convert_save_to_show,
    execute_notebook_cells,
    parse_notebook_segments,
)
from drawlib._builder.image_builder import build_image
from drawlib._templates import init_project


class TestConvertSaveToShow:
    """Tests for convert_save_to_show()."""

    def test_replaces_import_and_call(self) -> None:
        code = (
            "from drawlib.canvas import save, setup\n"
            "setup(width=80, height=40)\n"
            "save('out.png')\n"
        )
        converted = convert_save_to_show(code)
        assert "from drawlib.canvas import show, setup" in converted
        assert "show()" in converted
        assert "save(" not in converted

    def test_replaces_canvas_qualified_save(self) -> None:
        code = "import drawlib.canvas as canvas\ncanvas.setup(width=50, height=30)\ncanvas.save()\n"
        converted = convert_save_to_show(code)
        assert "canvas.show()" in converted
        assert "canvas.save(" not in converted


class TestNotebookDryRunAndExport:
    """Tests for sequential cell execution, error reporting, and .ipynb generation."""

    def test_sequential_execution_and_self_contained_base64_ipynb(self, tmp_path: Path) -> None:
        assets_dir = tmp_path / "_assets"
        assets_dir.mkdir(parents=True, exist_ok=True)
        local_logo = assets_dir / "logo.png"

        md_text = (
            "# Sample Notebook\n\n"
            "Intro with local image ![Logo](_assets/logo.png) and literal `![skip](_assets/logo.png)`.\n\n"
            '```drawlib file=hero.png caption="Hero Diagram"\n'
            "from drawlib.canvas import save, setup\n"
            "from drawlib.shapes import rectangle\n"
            "from drawlib.styles import Styles\n"
            "setup(width=60, height=30)\n"
            'rectangle((30, 15), width=40, height=16, style=Styles.Neutral, text="Hero")\n'
            "save()\n"
            "```\n\n"
            "## Step 1\n\n"
            "```python\n"
            "!pip install -q drawlib\n"
            "values = [10, 20, 30]\n"
            "total = sum(values)\n"
            "print(f'total={total}')\n"
            "total\n"
            "```\n\n"
            '```drawlib cell=code file=live.png caption="Live Cell"\n'
            "from drawlib.canvas import save, setup\n"
            "from drawlib.shapes import rectangle\n"
            "from drawlib.styles import Styles\n"
            "setup(width=60, height=30)\n"
            "rectangle((30, 15), width=40, height=16, style=Styles.PrimaryFlat, text=f'Sum: {total}')\n"
            "save()\n"
            "```\n"
        )
        md_file = tmp_path / "notebook.md"
        md_file.write_text(md_text, encoding="utf-8")

        segments = parse_notebook_segments(
            md_text,
            doc_base_name="notebook",
            output_dir=str(tmp_path),
            default_format="png",
            require_file=True,
        )
        assert len(segments) == 5
        assert segments[1].kind == "drawlib"
        assert segments[1].cell_mode == "markdown"
        assert segments[3].kind == "code"
        assert segments[3].cell_mode == "code"
        assert segments[4].kind == "drawlib"
        assert segments[4].cell_mode == "code"

        exec_res = execute_notebook_cells(
            segments,
            source_path=str(md_file),
            doc_base_name="notebook",
            output_dir=str(tmp_path),
        )
        assert len(exec_res.cell_outputs) == 2
        out1 = exec_res.cell_outputs[3]
        assert out1.stdout == "total=60\n"
        assert out1.result_repr == "60"

        out2 = exec_res.cell_outputs[4]
        assert len(out2.figures) == 1
        assert len(out2.figures[0]) > 100

        # Populate hero.png and _assets/logo.png so Base64 inliner can read both
        assert segments[1].target_img_path is not None
        Path(segments[1].target_img_path).write_bytes(out2.figures[0])
        local_logo.write_bytes(out2.figures[0])

        ipynb = build_ipynb_dict(
            segments,
            colab_url="https://colab.research.google.com/github/example/repo/blob/main/notebook.ipynb",
            source_dir=str(tmp_path),
            project_root=str(tmp_path),
        )
        assert ipynb["nbformat"] == 4
        assert ipynb["nbformat_minor"] == 5
        cells = ipynb["cells"]
        assert len(cells) == 3
        assert cells[0]["cell_type"] == "markdown"
        first_md = "".join(cells[0]["source"])
        assert 'alt="Open In Colab"' in first_md
        assert "data:image/svg+xml;base64," in first_md
        # Local Markdown image and Hero diagram are inlined as Base64 inside the same unified Markdown cell
        assert first_md.count('<img src="data:image/png;base64,') == 2
        assert "`![skip](_assets/logo.png)`" in first_md
        assert "<em>Hero Diagram</em>" in first_md
        assert "## Step 1" in first_md

        # Explicit !pip install inside user python block is preserved in .ipynb code cell
        assert cells[1]["cell_type"] == "code"
        assert "!pip install -q drawlib" in "".join(cells[1]["source"])

        assert cells[2]["cell_type"] == "code"
        assert "show()" in "".join(cells[2]["source"])

        for c in cells:
            assert "attachments" not in c
            if c["cell_type"] == "code":
                assert c["outputs"] == []
                assert c["execution_count"] is None

    def test_dry_run_raises_notebook_execution_error_with_line_numbers(self, tmp_path: Path) -> None:
        md_text = (
            "# Broken Notebook\n\n"
            "Some intro text.\n\n"
            "```python\n"
            "x = 10\n"
            "y = x + undefined_var\n"
            "```\n"
        )
        md_file = tmp_path / "broken.md"
        md_file.write_text(md_text, encoding="utf-8")

        segments = parse_notebook_segments(
            md_text,
            doc_base_name="broken",
            output_dir=str(tmp_path),
        )
        with pytest.raises(NotebookExecutionError) as exc_info:
            execute_notebook_cells(
                segments,
                source_path=str(md_file),
                doc_base_name="broken",
                output_dir=str(tmp_path),
            )
        err = exc_info.value
        assert err.cell_index == 1
        assert err.cell_line == 2
        assert err.markdown_line == 7
        assert "NameError" in str(err)


class TestInitAndBuildJupyterProject:
    """End-to-end tests for drawlib init project jupyter and build_jupyter."""

    def test_init_and_build_multi_locale_jupyter_project(self, tmp_path: Path) -> None:
        created = init_project(
            project_type="jupyter",
            destination=tmp_path,
            target="tutorials",
            lang="en,ja",
        )
        src_dir = tmp_path / "tutorials_src"
        assert src_dir.is_dir()
        assert (src_dir / "drawlib.toml").is_file()
        assert (src_dir / "en" / "01_sample_notebook.md").is_file()
        assert (src_dir / "ja" / "01_sample_notebook.md").is_file()
        assert len(created) > 0

        # 1. Dry-run only should not create tutorials_jupyter
        out_dir = tmp_path / "tutorials_jupyter"
        res_dry = build_jupyter(str(src_dir), str(out_dir), dry_run=True)
        assert Path(res_dry) == src_dir
        assert not out_dir.exists()

        # 2. build_jupyter emits standalone .ipynb ONLY (no HTML, CSS, index.html, images/, _assets/, or README.md)
        res_out = build_jupyter(str(src_dir), str(out_dir), workers=1)
        assert Path(res_out) == out_dir
        assert (out_dir / "en" / "01_sample_notebook.ipynb").is_file()
        assert (out_dir / "ja" / "01_sample_notebook.ipynb").is_file()
        assert not (out_dir / "index.html").exists()
        assert not (out_dir / "README.md").exists()
        assert not (out_dir / "images").exists()
        assert not (out_dir / "_assets").exists()
        assert not (out_dir / "en" / "01_sample_notebook.html").exists()
        assert not (out_dir / "en" / "style.css").exists()
        assert not (out_dir / "ja" / "01_sample_notebook.html").exists()
        assert sorted(p.relative_to(out_dir).as_posix() for p in out_dir.rglob("*") if p.is_file()) == [
            "en/01_sample_notebook.ipynb",
            "ja/01_sample_notebook.ipynb",
        ]

        nb_data = json.loads((out_dir / "en" / "01_sample_notebook.ipynb").read_text(encoding="utf-8"))
        assert nb_data["nbformat"] == 4
        code_cells = [c for c in nb_data["cells"] if c["cell_type"] == "code"]
        # 1 explicit !pip install python cell + 1 dataset python cell + 1 drawlib cell=code cell — all clean in .ipynb
        assert len(code_cells) == 3
        assert "!pip install -q drawlib" in "".join(code_cells[0]["source"])
        for code_cell in code_cells:
            assert code_cell["outputs"] == []
            assert code_cell["execution_count"] is None

        # 2b. Single-file build_jupyter writes ONLY the .ipynb file (no stray *_images/ folder)
        single_out_dir = tmp_path / "single_out"
        single_out_dir.mkdir()
        single_ipynb = Path(
            build_jupyter(str(src_dir / "en" / "01_sample_notebook.md"), str(single_out_dir / "solo.ipynb"))
        )
        assert single_ipynb == single_out_dir / "solo.ipynb"
        assert single_ipynb.is_file()
        assert sorted(p.relative_to(single_out_dir).as_posix() for p in single_out_dir.rglob("*")) == ["solo.ipynb"]

        # 3. build_html on a jupyter project generates 2-column HTML preview bundled with .ipynb in <target>_html/
        res_html_dir = Path(build_html(str(src_dir), workers=1))
        assert res_html_dir == tmp_path / "tutorials_html"
        assert (res_html_dir / "index.html").is_file()
        assert (res_html_dir / "en" / "01_sample_notebook.html").is_file()
        assert (res_html_dir / "en" / "01_sample_notebook.ipynb").is_file()
        assert (res_html_dir / "ja" / "01_sample_notebook.html").is_file()
        assert (res_html_dir / "ja" / "01_sample_notebook.ipynb").is_file()

        html_text = (res_html_dir / "en" / "01_sample_notebook.html").read_text(encoding="utf-8")
        assert "jupyter-notebook" in html_text
        assert "drawlib-image drawlib-figure" in html_text
        assert "drawlib-caption" in html_text
        assert "drawlib-code-details drawlib-code-fold" in html_text
        assert "nb-code-cell" in html_text
        assert "nb-output" in html_text
        assert "nb-output-figure" in html_text
        assert "01_sample_notebook.ipynb" in html_text

        css_text = (src_dir / "style.css").read_text(encoding="utf-8")
        assert ".drawlib-figure" in css_text
        assert ".drawlib-figure img" in css_text
        assert "details.drawlib-code-fold" in css_text
        assert ".nb-markdown-cell img" in css_text

        # 4. build_image on a jupyter project extracts both cell=markdown and cell=code diagrams
        out_img_dir = tmp_path / "tutorials_images"
        executed_imgs = build_image(str(src_dir), str(out_img_dir), workers=1)
        assert len(executed_imgs) >= 2
        assert (out_img_dir / "01_sample_notebook" / "pipeline_overview.png").is_file()
        assert (out_img_dir / "01_sample_notebook" / "live_bar_chart.png").is_file()

        # 5. Unsupported targets (pdf, docx, markdown) raise explicit guidance errors for jupyter projects
        with pytest.raises(ValueError, match="drawlib build jupyter"):
            build_pdf(str(src_dir), str(tmp_path / "tutorials.pdf"))
        with pytest.raises(ValueError, match="drawlib build jupyter"):
            build_docx(str(src_dir), str(tmp_path / "tutorials.docx"))
        with pytest.raises(ValueError, match="drawlib build jupyter"):
            build_markdown(str(src_dir), str(tmp_path / "tutorials_md"))

    def test_build_image_jupyter_with_execute_false_skips_colab_code_cells(self, tmp_path: Path) -> None:
        proj_dir = tmp_path / "colab_src"
        (proj_dir / "ja").mkdir(parents=True)
        (proj_dir / "drawlib.toml").write_text(
            '[project]\nname = "colab"\ntype = "jupyter"\n\n'
            '[i18n]\ndefault_lang = "ja"\nlangs = ["ja"]\n\n'
            '[jupyter]\ndrawlib_cell_mode = "markdown"\nexecute = false\n',
            encoding="utf-8",
        )
        (proj_dir / "ja" / "01_colab.md").write_text(
            "# Colab Notebook\n\n"
            '```drawlib file=overview.png caption="Overview"\n'
            "from drawlib.canvas import save, setup\n"
            "from drawlib.shapes import rectangle\n"
            "from drawlib.styles import Styles\n"
            "setup(width=60, height=30)\n"
            'rectangle((30, 15), width=40, height=16, style=Styles.Neutral, text="Colab")\n'
            "save()\n"
            "```\n\n"
            "```python\n"
            "from google.colab import userdata\n"
            "api_key = userdata.get('API_KEY')\n"
            "```\n",
            encoding="utf-8",
        )

        # build_jupyter succeeds with execute=false and emits only .ipynb
        nb_out = Path(build_jupyter(str(proj_dir), str(tmp_path / "colab_jupyter"), workers=1))
        assert (nb_out / "ja" / "01_colab.ipynb").is_file()
        assert not (nb_out / "ja" / "01_colab.html").exists()

        # build_image succeeds with execute=false by extracting markdown diagrams while skipping Colab cells
        img_out = tmp_path / "colab_images"
        executed = build_image(str(proj_dir), str(img_out), workers=1)
        assert len(executed) == 1
        assert (img_out / "01_colab" / "overview.png").is_file()

    def test_colab_base_url_prefix_and_path_template(self, tmp_path: Path) -> None:
        cfg_empty = JupyterConfig()
        assert cfg_empty.build_colab_url("en/01_intro.ipynb") == ""

        cfg_prefix = JupyterConfig(
            colab_base_url="https://colab.research.google.com/github/owner/repo/blob/main/docs/jupyter/"
        )
        assert (
            cfg_prefix.build_colab_url("en/01_intro.ipynb")
            == "https://colab.research.google.com/github/owner/repo/blob/main/docs/jupyter/en/01_intro.ipynb"
        )

        cfg_template = JupyterConfig(
            colab_base_url="https://colab.example.com/open?notebook={path}&env=prod"
        )
        assert (
            cfg_template.build_colab_url("ja/01_intro.ipynb")
            == "https://colab.example.com/open?notebook=ja/01_intro.ipynb&env=prod"
        )

        # Verify manifest parsing of colab_base_url
        proj_dir = tmp_path / "nb_src"
        (proj_dir / "en").mkdir(parents=True)
        (proj_dir / "drawlib.toml").write_text(
            '[project]\nname = "nb"\ntype = "jupyter"\n\n'
            '[i18n]\ndefault_lang = "en"\nlangs = ["en"]\n\n'
            '[jupyter]\ncolab_base_url = "https://colab.example.com/notebooks/{path}"\n',
            encoding="utf-8",
        )
        manifest = load_project_manifest(str(proj_dir))
        assert manifest is not None and manifest.jupyter is not None
        assert (
            manifest.jupyter.build_colab_url("en/01_intro.ipynb")
            == "https://colab.example.com/notebooks/en/01_intro.ipynb"
        )

        # Obsolete keys (image_mode, setup_packages) must be rejected by strict manifest validation
        for obsolete_line in ('image_mode = "url"', 'setup_packages = ["drawlib"]'):
            (proj_dir / "drawlib.toml").write_text(
                '[project]\nname = "nb"\ntype = "jupyter"\n\n'
                '[i18n]\ndefault_lang = "en"\nlangs = ["en"]\n\n'
                f"[jupyter]\n{obsolete_line}\n",
                encoding="utf-8",
            )
            with pytest.raises(ValueError, match="unknown key"):
                load_project_manifest(str(proj_dir))


