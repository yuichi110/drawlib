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
    build_html,
    build_ipynb_dict,
    build_jupyter,
    convert_save_to_show,
    execute_notebook_cells,
    parse_notebook_segments,
)
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

    def test_sequential_execution_and_ipynb_attachment_mode(self, tmp_path: Path) -> None:
        md_text = (
            "# Sample Notebook\n\n"
            "```drawlib file=hero.png caption=\"Hero Diagram\"\n"
            "from drawlib.canvas import save, setup\n"
            "from drawlib.shapes import rectangle\n"
            "from drawlib.styles import Styles\n"
            "setup(width=60, height=30)\n"
            "rectangle((30, 15), width=40, height=16, style=Styles.Neutral, text=\"Hero\")\n"
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
            "```drawlib cell=code file=live.png caption=\"Live Cell\"\n"
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

        # Create dummy hero.png so attachment mode can embed it
        assert segments[1].target_img_path is not None
        Path(segments[1].target_img_path).write_bytes(out2.figures[0])

        ipynb = build_ipynb_dict(
            segments,
            execution_result=exec_res,
            image_mode="attachment",
            colab_url="https://colab.research.google.com/github/example/repo/blob/main/notebook.ipynb",
            setup_packages=("drawlib",),
        )
        assert ipynb["nbformat"] == 4
        assert ipynb["nbformat_minor"] == 5
        cells = ipynb["cells"]
        assert cells[0]["cell_type"] == "markdown"
        assert "colab-badge.svg" in "".join(cells[0]["source"])
        assert cells[1]["cell_type"] == "code"
        assert "!pip install -q drawlib" in "".join(cells[1]["source"])

        # Find markdown cell with attachment
        att_cells = [c for c in cells if c["cell_type"] == "markdown" and "attachments" in c]
        assert len(att_cells) == 1
        assert "hero.png" in att_cells[0]["attachments"]
        assert "attachment:hero.png" in "".join(att_cells[0]["source"])

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

        # 2. Full build should generate .ipynb and .html for both locales + root index.html
        res_out = build_jupyter(str(src_dir), str(out_dir), workers=1)
        assert Path(res_out) == out_dir
        assert (out_dir / "index.html").is_file()
        assert (out_dir / "en" / "01_sample_notebook.ipynb").is_file()
        assert (out_dir / "en" / "01_sample_notebook.html").is_file()
        assert (out_dir / "ja" / "01_sample_notebook.ipynb").is_file()
        assert (out_dir / "ja" / "01_sample_notebook.html").is_file()

        nb_data = json.loads((out_dir / "en" / "01_sample_notebook.ipynb").read_text(encoding="utf-8"))
        assert nb_data["nbformat"] == 4
        code_cells = [c for c in nb_data["cells"] if c["cell_type"] == "code"]
        # 1 setup cell + 1 python cell + 1 drawlib cell=code cell
        assert len(code_cells) == 3
        assert len(code_cells[1]["outputs"]) >= 1
        assert len(code_cells[2]["outputs"]) >= 1

        html_text = (out_dir / "en" / "01_sample_notebook.html").read_text(encoding="utf-8")
        assert "jupyter-notebook" in html_text
        assert "nb-code-cell" in html_text
        assert "01_sample_notebook.ipynb" in html_text

        # 3. build_html on a jupyter project also bundles .ipynb alongside .html in <target>_html/
        res_html_dir = Path(build_html(str(src_dir), workers=1))
        assert res_html_dir == tmp_path / "tutorials_html"
        assert (res_html_dir / "en" / "01_sample_notebook.html").is_file()
        assert (res_html_dir / "en" / "01_sample_notebook.ipynb").is_file()
        assert (res_html_dir / "ja" / "01_sample_notebook.html").is_file()
        assert (res_html_dir / "ja" / "01_sample_notebook.ipynb").is_file()

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

