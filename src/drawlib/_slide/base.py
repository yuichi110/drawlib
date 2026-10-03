# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Base interfaces and data structures for modular slide SmartArt components."""

from __future__ import annotations

import abc
from dataclasses import dataclass
from typing import ClassVar


@dataclass(frozen=True)
class BoundingBox:
    """A rectangular bounding box on the slide stage (typically 1920x1080).

    Attributes:
        x: The horizontal coordinate of the top-left corner in stage pixels.
        y: The vertical coordinate of the top-left corner in stage pixels.
        width: The width of the bounding box in stage pixels.
        height: The height of the bounding box in stage pixels.
    """

    x: float
    y: float
    width: float
    height: float


class SmartArtComponent(abc.ABC):
    """Abstract base class for modular SmartArt slide components.

    Subclasses implement the `render` method to draw illustrations with shapes
    and text entirely in Drawlib, saving the output as Native SVG.
    """

    name: ClassVar[str] = ""

    @abc.abstractmethod
    def render(
        self,
        box: BoundingBox,
        content: str,
        output_file: str,
        **kwargs: object,
    ) -> None:
        """Render the SmartArt component into an SVG file within the given bounding box.

        Args:
            box: Target bounding box on the 1920x1080 slide stage.
            content: Raw or parsed Markdown content of the block.
            output_file: Path to save the generated SVG image file.
            **kwargs: Additional component-specific attributes.
        """
        raise NotImplementedError
