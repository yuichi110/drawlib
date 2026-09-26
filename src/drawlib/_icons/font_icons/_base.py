# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Base class and common functions for font glyph icon providers."""

from __future__ import annotations

import os
from urllib.parse import urljoin

import drawlib._assets
from drawlib import ASSET_VERSION
from drawlib._core.fonts import FontMetadata, FontResource
from drawlib._core.types import Style, TypeAngle, TypeCoordinate, TypeIconStyle, TypePosFloat, TypeStr
from drawlib._core.utils import download_if_not_exist
from drawlib._icons._utils import IconUtil
from drawlib._icons.font_icons._font_icon import font_icon


class FontIconProvider:
    """Base provider for font glyph icons (Phosphor, FontAwesome, etc.)."""

    def __init__(
        self,
        name: str,
        font_resources: dict[str, FontResource],
        default_style: TypeIconStyle,
        asset_subdir: str = "fonticons",
    ) -> None:
        """Initialize FontIconProvider.

        Args:
            name: Name of the icon family (e.g. 'phosphor').
            font_resources: Dictionary mapping style name to FontResource.
            default_style: Default font style (e.g. 'thin' or 'regular').
            asset_subdir: Subdirectory under assets URL (default 'fonticons').
        """
        self.name = name
        self.font_resources = font_resources
        self.default_style: TypeIconStyle = default_style
        self.asset_subdir = asset_subdir

    def get_font_metadata(self, font: str) -> FontMetadata:
        """Resolve full metadata for a given font style.

        Args:
            font: The font style name.

        Returns:
            FontMetadata: Resolved metadata including absolute path and URL.

        Raises:
            ValueError: If font style is not in font_resources.
        """
        resource = self.font_resources.get(font)
        if not resource:
            raise ValueError(f"Font style '{font}' not found for icon provider '{self.name}'.")

        paths = [p for p in resource.path.split("/") if p]
        dir_path = os.path.join(os.path.dirname(drawlib._assets.__file__), self.asset_subdir)
        abs_path = os.path.join(dir_path, *paths)

        url = urljoin(
            f"https://raw.githubusercontent.com/yuichi110/drawlib_assets/main/assets/{ASSET_VERSION}/{self.asset_subdir}/",
            "/".join(paths),
        )

        return FontMetadata(
            path=resource.path,
            abs_path=abs_path,
            url=url,
            md5=resource.md5,
        )

    def write(
        self,
        xy: TypeCoordinate,
        width: TypePosFloat,
        code: str,
        angle: TypeAngle = 0.0,
        *,
        style: Style,
    ) -> None:
        """Draw an icon at the specified position using the configured font.

        Args:
            xy: (x, y) coordinates of the icon center.
            width: Width of the icon.
            code: Unicode character or codepoint for the icon glyph.
            angle: Rotation angle in degrees (default 0.0).
            style: Style object (required).

        Raises:
            ValueError: If an unsupported icon_style is specified.
        """
        style_obj = IconUtil.format_style(style, default_icon_style=self.default_style)

        if style_obj.icon_style not in self.font_resources:
            valid_styles = list(self.font_resources.keys())
            raise ValueError(
                f"Icon provider '{self.name}' does not support style '{style_obj.icon_style}'. "
                f"Valid styles: {valid_styles}"
            )

        font_metadata = self.get_font_metadata(style_obj.icon_style)
        download_if_not_exist(
            file_path=font_metadata.abs_path,
            download_url=font_metadata.url,
            md5_hash=font_metadata.md5,
        )

        font_icon(
            xy=xy,
            width=width,
            code=code,
            file=font_metadata.abs_path,
            angle=angle,
            style=style_obj,
        )
