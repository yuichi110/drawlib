# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Automated dry-run and structure verification tests for official docs_src/jupyter notebooks."""

from __future__ import annotations

import json
from pathlib import Path

from drawlib.tools import build_jupyter

PROJECT_ROOT = Path(__file__).resolve().parents[3]
JUPYTER_SRC_DIR = PROJECT_ROOT / "docs_src" / "jupyter"


def test_official_jupyter_docs_dry_run(tmp_path: Path) -> None:
    """Verify all official EN/JA notebooks in docs_src/jupyter execute cleanly in dry-run mode."""
    assert JUPYTER_SRC_DIR.is_dir()
    out_dir = tmp_path / "jupyter_out"
    build_jupyter(str(JUPYTER_SRC_DIR), output_dir=str(out_dir), dry_run=True, execute=True)


def test_official_jupyter_docs_build_outputs(tmp_path: Path) -> None:
    """Verify full build of docs_src/jupyter produces valid nbformat v4.5 .ipynb and HTML files."""
    out_dir = tmp_path / "docs_jupyter"
    build_jupyter(str(JUPYTER_SRC_DIR), output_dir=str(out_dir), execute=True)

    for lang in ("en", "ja"):
        lang_dir = out_dir / lang
        assert lang_dir.is_dir()
        ipynb_files = sorted(lang_dir.glob("*.ipynb"))
        assert len(ipynb_files) == 6
        for ipynb_path in ipynb_files:
            nb = json.loads(ipynb_path.read_text(encoding="utf-8"))
            assert nb["nbformat"] == 4
            assert nb["nbformat_minor"] == 5
            assert len(nb["cells"]) >= 4
            # First cell has Open in Colab badge
            first_md = "".join(nb["cells"][0]["source"])
            assert "colab.research.google.com/github/yuichi110/drawlib/blob/main/docs/jupyter/" in first_md
            # Second cell is !pip install -q drawlib setup cell
            setup_src = "".join(nb["cells"][1]["source"])
            assert "!pip install -q drawlib" in setup_src
            # All code cells in .ipynb must be clean/unexecuted (outputs rendered in HTML only)
            for cell in nb["cells"]:
                if cell["cell_type"] == "code":
                    assert cell["outputs"] == []
                    assert cell["execution_count"] is None

            # Companion HTML preview must contain rendered Out[n] figures
            html_path = ipynb_path.with_suffix(".html")
            assert html_path.is_file()
            html_text = html_path.read_text(encoding="utf-8")
            assert "nb-output-figure" in html_text, f"{html_path.name} missing rendered output figure in HTML"
