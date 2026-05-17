# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Unit tests for StaticContainer class."""

import pytest

from drawlib.v0_2.private.l2_models_._container import StaticContainer


class TestStaticContainer:
    """Test cases for StaticContainer."""

    def test_cannot_instantiate(self):
        """Test that attempting to instantiate StaticContainer raises a TypeError."""
        with pytest.raises(TypeError) as exc_info:
            StaticContainer()

        assert "is a static container (namespace) and cannot be instantiated" in str(exc_info.value)
