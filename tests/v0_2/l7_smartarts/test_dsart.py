# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Unit tests for the dsart package exports facade."""

from drawlib.v0_2.private.l7_smartarts import _dsart as dsart


class TestDsartFacade:
    """Tests to verify all required smart art models are correctly exposed in dsart facade."""

    def test_dsart_exports(self) -> None:
        """Verify that all standard smart art constructors exist in the dsart exports."""
        assert hasattr(dsart, "BoxList")
        assert hasattr(dsart, "bubblespeech")
        assert hasattr(dsart, "BulletPoints")
        assert hasattr(dsart, "GridLayout")
        assert hasattr(dsart, "Pyramid")
        assert hasattr(dsart, "SourceCode")
        assert hasattr(dsart, "Table")
        assert hasattr(dsart, "TreeNode")
