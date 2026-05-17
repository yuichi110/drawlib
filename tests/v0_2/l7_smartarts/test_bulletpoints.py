# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Unit and integration tests for BulletPoints smart art."""

from drawlib.v0_2.apis import (
    clear,
    dsart,
    save,
)

OUTPUT_DIR = "../../../output_tests/v0_2/l7_smartarts/bulletpoints/"


class TestBulletPoints:
    """Tests for the BulletPoints class drawing operations."""

    def test_bulletpoints_default(self) -> None:
        """Verify BulletPoints rendering with multi-level indents."""
        clear()
        b = dsart.BulletPoints(4, 4)
        b.add("level 0")
        b.set_indent(1)
        b.add("level 1-1")
        b.add("level 1-2")
        b.set_indent(2)
        b.add("level 2-1")
        b.add("level 2-2")
        b.set_indent(1)
        b.add("level 1-3")
        b.draw((10, 80))
        save(f"{OUTPUT_DIR}test_bulletpoints_default.png")

    def test_bulletpoints_japanese(self) -> None:
        """Verify BulletPoints rendering using Japanese text at multiple levels."""
        clear()
        b = dsart.BulletPoints(4, 4)
        b.add("レベル 0")
        b.set_indent(1)
        b.add("レベル 1-1")
        b.add("レベル 1-2")
        b.set_indent(2)
        b.add("レベル 2-1")
        b.add("レベル 2-2")
        b.set_indent(1)
        b.add("レベル 1-3")
        b.draw((10, 80))
        save(f"{OUTPUT_DIR}test_bulletpoints_japanese.png")
