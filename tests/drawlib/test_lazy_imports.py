# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Subprocess regression tests for lazy module loading and startup isolation."""

from __future__ import annotations

import subprocess
import sys


def _run_isolated_python(code: str) -> subprocess.CompletedProcess[str]:
    """Execute Python code in a fresh interpreter subprocess."""
    return subprocess.run(  # noqa: S603
        [sys.executable, "-W", "error::DeprecationWarning", "-c", code],
        capture_output=True,
        text=True,
        check=False,
    )


def test_top_level_import_is_lazy() -> None:
    """Verify `import drawlib` does not eagerly load matplotlib, pydantic, playwright, icons, or preset styles."""
    res = _run_isolated_python(
        """
import sys
import drawlib

assert isinstance(drawlib.__version__, str)
assert "matplotlib" not in sys.modules
assert "pydantic" not in sys.modules
assert "playwright" not in sys.modules
assert "drawlib._preset_styles" not in sys.modules
assert "drawlib._icons" not in sys.modules
assert "drawlib.canvas" not in sys.modules

# Accessing a lazy submodule attribute loads it on demand
from drawlib import math as dmath
assert dmath is drawlib.math
"""
    )
    assert res.returncode == 0, res.stderr


def test_tools_import_does_not_load_matplotlib() -> None:
    """Verify `drawlib.tools` helpers do not import matplotlib, playwright, or preset styles."""
    res = _run_isolated_python(
        """
import sys
from drawlib.tools import init_project, list_css, scan_broken_links

assert callable(init_project)
assert callable(list_css)
assert callable(scan_broken_links)
assert "matplotlib" not in sys.modules
assert "playwright" not in sys.modules
assert "drawlib._preset_styles" not in sys.modules
"""
    )
    assert res.returncode == 0, res.stderr


def test_styles_import_instantiates_only_active_preset() -> None:
    """Verify `from drawlib.styles import Colors, Styles` does not instantiate unused presets or load matplotlib."""
    res = _run_isolated_python(
        """
import sys
from drawlib.styles import Colors, Styles

assert Styles.Primary is not None
assert Colors.Primary is not None
assert "matplotlib" not in sys.modules
assert "playwright" not in sys.modules
assert "drawlib._preset_styles._style_google" not in sys.modules
assert "drawlib._preset_styles._style_monochrome" not in sys.modules

from drawlib._core.l3_styles._base_styles import _BaseStylesMeta
from drawlib._preset_styles._style_default import DefaultStyles, DefaultStyles1, DefaultStyles2

assert DefaultStyles in _BaseStylesMeta._default_instances
assert DefaultStyles1 not in _BaseStylesMeta._default_instances
assert DefaultStyles2 not in _BaseStylesMeta._default_instances
"""
    )
    assert res.returncode == 0, res.stderr


def test_icons_submodule_import_isolates_suites() -> None:
    """Verify importing a single icon suite does not eagerly import all 27 icon suites."""
    res = _run_isolated_python(
        """
import sys
from drawlib.icons.phosphor import airplane
import drawlib.icons.gcp as gcp

assert callable(airplane)
assert hasattr(gcp, "__name__")
assert "drawlib._icons.png_icons.original_workspace" not in sys.modules
assert "drawlib._icons.png_icons.phosphor_thin" not in sys.modules
assert "drawlib._icons.png_icons.phosphor_fill" not in sys.modules
"""
    )
    assert res.returncode == 0, res.stderr


def test_cli_app_import_does_not_load_matplotlib_or_presets() -> None:
    """Verify loading the CLI root app and browser helper does not import matplotlib, playwright, or presets."""
    res = _run_isolated_python(
        """
import sys
from drawlib._cli._drawlib import app
import drawlib._builder._common.browser as browser_mod

assert app is not None
assert browser_mod is not None
assert "matplotlib" not in sys.modules
assert "playwright" not in sys.modules
assert "drawlib._preset_styles._style_default" not in sys.modules
assert "drawlib._preset_styles._style_google" not in sys.modules
"""
    )
    assert res.returncode == 0, res.stderr


def test_no_pydantic_211_model_fields_deprecation_warning() -> None:
    """Verify preset style operations emit zero PydanticDeprecatedSince211 warnings."""
    res = _run_isolated_python(
        """
import warnings
warnings.simplefilter("error")

from drawlib.fonts import FontRoboto
from drawlib.preset_styles import DefaultStyles, GoogleStyles, MonochromeStyles

d = DefaultStyles()
_ = dict(d)
_ = d.styles()
_ = dir(d)
_ = d.patch_font(regular=FontRoboto.ROBOTO_REGULAR)
_ = GoogleStyles.Primary
_ = MonochromeStyles.Primary
"""
    )
    assert res.returncode == 0, res.stderr
