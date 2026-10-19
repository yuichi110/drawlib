# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Unit tests for tools/dcli/codegen."""

from __future__ import annotations

from typer.testing import CliRunner

from tools.dcli.codegen import app
from tools.dcli.codegen.gcp_codegen import generate_code
from tools.dcli.codegen.phosphor import parse_css_icons

runner = CliRunner()


def test_gcp_generate_code() -> None:
    """Test GCP icon code generation with variants and aliases."""
    code = generate_code(
        icon_variants={"compute_engine": ["default", "modern"], "app_engine": ["default"]},
        aliases={"gce": "compute_engine"},
    )
    assert "def compute_engine(" in code
    assert 'variant: Literal["default", "modern"] = "default"' in code
    assert "def gce(" in code
    assert 'name="compute_engine"' in code
    assert "def app_engine(" in code
    assert 'variant: Literal["default"] = "default"' in code


def test_parse_css_icons() -> None:
    """Test Phosphor CSS icon parsing."""
    sample_css = """
    .ph.ph-airplane:before {
      content: "\\e002";
    }
    .ph.ph-alarm:before {
      content: "\\e004";
    }
    """
    icons = parse_css_icons(sample_css)
    assert icons.get("airplane") == "e002"
    assert icons.get("alarm") == "e004"


def test_codegen_cli_help() -> None:
    """Test dcli codegen --help."""
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "icon-phosphor" in result.output
    assert "icon-gcp" in result.output
