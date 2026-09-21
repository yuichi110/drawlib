# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Base class and common functions for PNG raster icon providers."""

from __future__ import annotations

from pathlib import Path

from drawlib._core.l2_types import (
    TypeAngle,
    TypeCoordinate,
    TypePosFloat,
    TypeStr,
)
from drawlib._core.l3_styles import Style
from drawlib._core.l4_canvas import image
from drawlib._preset_styles import get_style
from drawlib._release_assets import RELEASE_ASSET_PACKAGES, ReleaseAssetPackage, ensure_asset_available


class PngIconProvider:
    """Base provider for PNG raster icons (GCP, AWS, Azure, etc.)."""

    def __init__(
        self,
        name: str,
        package_name: str,
        asset_subdir: str,
    ) -> None:
        """Initialize PngIconProvider.

        Args:
            name: Vendor/family name of the icon collection (e.g. 'gcp').
            package_name: Package identifier in RELEASE_ASSET_PACKAGES (e.g. 'icon_gcp').
            asset_subdir: Relative subdirectory path under drawlib._assets (e.g. 'icons/gcp').
        """
        self.name = name
        self.package_name = package_name
        self.asset_subdir = asset_subdir

    def get_icon_path(self, icon_name: str) -> str:
        """Resolve local file path for an icon, ensuring it is downloaded if missing.

        Args:
            icon_name: Base name of the icon file without extension (e.g. 'compute_engine').

        Returns:
            str: Absolute file path to the icon PNG.

        Raises:
            FileNotFoundError: If the icon file does not exist after download/extraction.
            ValueError: If the package is not registered in RELEASE_ASSET_PACKAGES.
        """
        filename = f"{icon_name}.png"
        pkg: ReleaseAssetPackage | None = RELEASE_ASSET_PACKAGES.get(self.package_name)
        if pkg is None:
            raise ValueError(f"Release asset package '{self.package_name}' is not registered.")

        local_dir = pkg.get_local_dir()
        icon_path = local_dir / filename

        # If missing locally in _assets, check developer release_assets or download from GitHub Releases
        if not icon_path.is_file():
            dev_source = Path("release_assets") / "v0.3" / self.asset_subdir / filename
            if dev_source.is_file():
                return str(dev_source.resolve())

            ensure_asset_available(f"{self.asset_subdir}/{filename}")

        if not icon_path.is_file():
            dev_source = Path("release_assets") / "v0.3" / self.asset_subdir / filename
            if dev_source.is_file():
                return str(dev_source.resolve())
            raise FileNotFoundError(f"Icon '{icon_name}' not found at '{icon_path}'.")

        return str(icon_path.resolve())

    def write(
        self,
        xy: TypeCoordinate,
        width: TypePosFloat,
        name: str,
        angle: TypeAngle = 0.0,
        style: Style | TypeStr | None = None,
    ) -> None:
        """Draw an icon at the specified position using canvas image().

        Args:
            xy: (x, y) coordinates of the icon center.
            width: Width of the icon.
            name: Base name of the icon file (without .png).
            angle: Rotation angle in degrees (default 0.0).
            style: Style object, style name string, or None.
        """
        # Icons default to transparent background and borderless frame (line_width=0)
        # unless line_width is explicitly specified in style.
        applied_style: Style
        if style is None:
            applied_style = Style(line_width=0)
        elif isinstance(style, Style):
            applied_style = style.copy()
            if applied_style.line_width is None:
                applied_style.line_width = 0
        else:
            applied_style = get_style(style).copy()
            if applied_style.line_width is None:
                applied_style.line_width = 0

        abs_path = self.get_icon_path(name)
        image(
            xy=xy,
            width=width,
            image=abs_path,
            angle=angle,
            style=applied_style,
        )
