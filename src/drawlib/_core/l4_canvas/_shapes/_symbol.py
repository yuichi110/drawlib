# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Canvas symbol, metaphor, and operator shape feature implementation module."""

from __future__ import annotations

import math

from matplotlib.path import Path
from pydantic import validate_call

from drawlib._core.l2_types import (
    ClockVariant,
    Coordinate,
    FaceVariant,
    HeartVariant,
    LightningVariant,
    MathSymbol,
    MoonVariant,
    NumVertex,
    PosFloat,
    Ratio,
    SunVariant,
)
from drawlib._core.l3_styles import Style
from drawlib._core.l4_canvas._shapes._polygon import CanvasShapePolygonFeature
from drawlib._core.l4_canvas._shapes._symbol_builders import (
    _build_face_feature_patches,
    _build_face_head_patch,
    _build_gear_outer_path_points,
    _build_math_symbol_path,
    build_clock_patches,
    build_heart_path,
    build_lightning_path,
    build_moon_path,
    build_sun_path,
)
from drawlib._core.l4_canvas._shapes._util import ShapeUtil


class CanvasShapeSymbolFeature(CanvasShapePolygonFeature):
    """Canvas symbol, metaphor, and operator shape feature implementation module.

    Provides expressive faces, clocks, nature/energy symbols, gears, and math operators.
    """

    def __init__(self) -> None:
        """Initializes a CanvasShapeSymbolFeature object."""
        super().__init__()

    @validate_call
    def face(
        self,
        xy: Coordinate,
        radius: PosFloat,
        *,
        variant: FaceVariant = "smile",
        style: Style,
        text: str = "",
        text_style: Style | None = None,
    ) -> None:
        """Draw an expressive face shape on the canvas.

        Args:
            xy: Center coordinates (x, y) of the face circle.
            radius: Radius of the face circle.
            variant: Facial expression or silhouette ("smile", "neutral", "sad",
                "angry", "surprised", "dizzy", "dead", "skull", or "devil").
            style: Style object (required).
            text: Text to display inside shape.
            text_style: Style object for text.
        """
        style, text_style = ShapeUtil.format_styles(style, text_style)
        if radius <= 0:
            raise ValueError(f"radius must be positive, but got radius={radius}.")

        width = radius * 2.0
        xy, angle, style = ShapeUtil.prepare_centered_shape(xy, width, width, style)
        cx, cy = xy

        face_fill, stroke_color, feature_color, feature_w = ShapeUtil.resolve_feature_colors(style)
        line_w = style.shape_line_width if style.shape_line_width is not None else 0.0
        line_style = style.shape_line_style if style.shape_line_style is not None else "solid"

        rad = math.radians(angle)
        cos_a = math.cos(rad)
        sin_a = math.sin(rad)

        head_patch = _build_face_head_patch(
            cx=cx,
            cy=cy,
            radius=radius,
            variant=variant,
            cos_a=cos_a,
            sin_a=sin_a,
            face_fill=face_fill,
            stroke_color=stroke_color,
            line_w=line_w,
            line_style=line_style,
        )
        feature_patches = _build_face_feature_patches(
            cx=cx,
            cy=cy,
            radius=radius,
            variant=variant,
            cos_a=cos_a,
            sin_a=sin_a,
            feature_color=feature_color,
            feature_w=feature_w,
        )
        ShapeUtil.append_patches_and_text(
            artists=self._artists,
            patches=[head_patch, *feature_patches],
            text_xy=xy,
            angle=angle,
            style=style,
            text=text,
            text_style=text_style,
        )

    @validate_call
    def clock(
        self,
        xy: Coordinate,
        radius: PosFloat,
        *,
        variant: ClockVariant = "standard",
        hour: float = 10.0,
        minute: float = 10.0,
        style: Style,
        text: str = "",
        text_style: Style | None = None,
    ) -> None:
        """Draw an analog or 7-segment digital clock shape on the canvas.

        Args:
            xy: Center coordinates tuple (x, y).
            radius: Radius of the clock dial (or scale reference for digital clock).
            variant: Clock variant ("standard", "ticks", "dial", "stopwatch",
                "timer", "alarm", "digital").
            hour: Hour value (e.g., 10.0 for 10 o'clock).
            minute: Minute value (e.g., 10.0 for 10 minutes).
            style: Style object (required).
            text: Text to display inside shape.
            text_style: Style object for text.
        """
        style, text_style = ShapeUtil.format_styles(style, text_style)
        width = radius * 2.15 if variant == "digital" else radius * 2.0
        height = radius * 1.22 if variant == "digital" else radius * 2.0
        xy, angle, style = ShapeUtil.prepare_centered_shape(xy, width, height, style)
        face_fill, stroke_color, feature_color, feature_w = ShapeUtil.resolve_feature_colors(style)
        patches = build_clock_patches(
            xy=xy,
            radius=radius,
            variant=variant,
            hour=hour,
            minute=minute,
            angle=angle,
            face_fill=face_fill,
            stroke_color=stroke_color,
            feature_color=feature_color,
            feature_w=feature_w,
            style=style,
        )
        ShapeUtil.append_patches_and_text(
            artists=self._artists,
            patches=patches,
            text_xy=xy,
            angle=angle,
            style=style,
            text=text,
            text_style=text_style,
        )

    @validate_call
    def sun(
        self,
        xy: Coordinate,
        radius: PosFloat,
        *,
        variant: SunVariant = "rays",
        num_rays: NumVertex = 8,
        style: Style,
        text: str = "",
        text_style: Style | None = None,
    ) -> None:
        """Draw a sun shape with surrounding rays on the canvas.

        Args:
            xy: Center coordinates tuple (x, y).
            radius: Outer radius to ray tips.
            variant: Sun variant ("rays", "standard", "ring", "beams").
            num_rays: Number of surrounding rays (must be >= 3).
            style: Style object (required).
            text: Text to display inside shape.
            text_style: Style object for text.
        """
        style, text_style = ShapeUtil.format_styles(style, text_style)
        width = radius * 2.0
        xy, angle, style = ShapeUtil.prepare_centered_shape(xy, width, width, style)
        path = build_sun_path(xy, radius, variant, num_rays, angle)
        ShapeUtil.append_path_and_text(
            artists=self._artists,
            path=path,
            text_xy=xy,
            angle=angle,
            style=style,
            text=text,
            text_style=text_style,
        )

    @validate_call
    def moon(
        self,
        xy: Coordinate,
        width: PosFloat,
        height: PosFloat,
        *,
        variant: MoonVariant = "crescent",
        mirror: bool = False,
        style: Style,
        text: str = "",
        text_style: Style | None = None,
    ) -> None:
        """Draw a crescent or half moon shape on the canvas.

        Args:
            xy: Center coordinates tuple (x, y).
            width: Width of the moon bounding box.
            height: Height of the moon bounding box.
            variant: Moon silhouette ("crescent", "standard", "thin", "waxing", "half").
            mirror: Whether to flip the moon horizontally.
            style: Style object (required).
            text: Text to display inside shape.
            text_style: Style object for text.
        """
        style, text_style = ShapeUtil.format_styles(style, text_style)
        xy, angle, style = ShapeUtil.prepare_centered_shape(xy, width, height, style)
        path = build_moon_path(xy, width, height, variant, mirror, angle)
        ShapeUtil.append_path_and_text(
            artists=self._artists,
            path=path,
            text_xy=xy,
            angle=angle,
            style=style,
            text=text,
            text_style=text_style,
        )

    @validate_call
    def heart(
        self,
        xy: Coordinate,
        width: PosFloat,
        height: PosFloat,
        *,
        variant: HeartVariant = "standard",
        style: Style,
        text: str = "",
        text_style: Style | None = None,
    ) -> None:
        """Draw a heart or broken-heart shape on the canvas.

        Args:
            xy: Center coordinates tuple (x, y).
            width: Width of the heart bounding box.
            height: Height of the heart bounding box.
            variant: Heart silhouette ("standard", "classic", "broken").
            style: Style object (required).
            text: Text to display inside shape.
            text_style: Style object for text.
        """
        style, text_style = ShapeUtil.format_styles(style, text_style)
        xy, angle, style = ShapeUtil.prepare_centered_shape(xy, width, height, style)
        path = build_heart_path(xy, width, height, variant, angle)
        ShapeUtil.append_path_and_text(
            artists=self._artists,
            path=path,
            text_xy=xy,
            angle=angle,
            style=style,
            text=text,
            text_style=text_style,
        )

    @validate_call
    def lightning(
        self,
        xy: Coordinate,
        width: PosFloat,
        height: PosFloat,
        *,
        variant: LightningVariant = "standard",
        mirror: bool = False,
        style: Style,
        text: str = "",
        text_style: Style | None = None,
    ) -> None:
        """Draw a lightning bolt shape on the canvas.

        Args:
            xy: Center coordinates tuple (x, y).
            width: Width of the lightning bolt bounding box.
            height: Height of the lightning bolt bounding box.
            variant: Lightning bolt silhouette ("standard", "flat", "double",
                "flat_double", "angled", "slanted").
            mirror: Whether to flip the lightning bolt horizontally.
            style: Style object (required).
            text: Text to display inside shape.
            text_style: Style object for text.
        """
        style, text_style = ShapeUtil.format_styles(style, text_style)
        xy, angle, style = ShapeUtil.prepare_centered_shape(xy, width, height, style)
        path = build_lightning_path(
            xy=xy,
            width=width,
            height=height,
            variant=variant,
            mirror=mirror,
            shape_r=style.shape_r,
            angle=angle,
        )
        ShapeUtil.append_path_and_text(
            artists=self._artists,
            path=path,
            text_xy=xy,
            angle=angle,
            style=style,
            text=text,
            text_style=text_style,
        )

    @validate_call
    def gear(
        self,
        xy: Coordinate,
        num_teeth: NumVertex,
        radius_ext: PosFloat,
        radius_int: PosFloat,
        *,
        tooth_ext_ratio: Ratio | None = None,
        tooth_int_ratio: Ratio | None = None,
        hole_radius: PosFloat | None = None,
        style: Style,
        text: str = "",
        text_style: Style | None = None,
    ) -> None:
        """Draw a gear shape on the canvas.

        Args:
            xy: Center coordinate tuple (x, y).
            num_teeth: Number of gear teeth (must be >= 3).
            radius_ext: Outer radius of gear tooth tips.
            radius_int: Inner radius of gear tooth roots/valleys.
            tooth_ext_ratio: Ratio of 1 pitch angle (360 / num_teeth) for the outer tooth tip.
                Defaults to 0.35 when None.
            tooth_int_ratio: Ratio of 1 pitch angle (360 / num_teeth) for the inner tooth base.
                Defaults to 0.55 when None.
            hole_radius: Radius of the center circular hole, or None for no hole.
            style: Style object.
            text: Text to display inside shape.
            text_style: Style object for text or None.

        Raises:
            ValueError: If radii, tooth ratios, or hole_radius are out of valid bounds.
        """
        style, text_style = ShapeUtil.format_styles(style, text_style)
        if radius_int <= 0.0:
            raise ValueError("radius_int must be positive.")
        if radius_ext <= radius_int:
            raise ValueError("radius_ext must be bigger than radius_int.")

        ext_ratio = 0.35 if tooth_ext_ratio is None else float(tooth_ext_ratio)
        int_ratio = 0.55 if tooth_int_ratio is None else float(tooth_int_ratio)
        if not (0.0 < ext_ratio < 1.0):
            raise ValueError("tooth_ext_ratio must be strictly between 0.0 and 1.0.")
        if not (0.0 < int_ratio < 1.0):
            raise ValueError("tooth_int_ratio must be strictly between 0.0 and 1.0.")

        if hole_radius is not None and (hole_radius <= 0.0 or hole_radius >= radius_int):
            raise ValueError("hole_radius must be positive and smaller than radius_int.")

        width = radius_ext * 2.0
        (cx, cy), angle, style = ShapeUtil.prepare_centered_shape(xy, width, width, style)

        path_points = _build_gear_outer_path_points(
            cx=cx,
            cy=cy,
            num_teeth=num_teeth,
            radius_ext=radius_ext,
            radius_int=radius_int,
            ext_ratio=ext_ratio,
            int_ratio=int_ratio,
            angle=angle,
            shape_r=style.shape_r,
        )

        outer_path = ShapeUtil.build_matplotlib_path(path_points)
        if hole_radius is not None:
            hole_path = ShapeUtil.build_ellipse_path(cx, cy, hole_radius, hole_radius, cw=True)
            path = Path.make_compound_path(outer_path, hole_path)
        else:
            path = outer_path

        ShapeUtil.append_path_and_text(
            artists=self._artists,
            path=path,
            text_xy=(cx, cy),
            angle=angle,
            style=style,
            text=text,
            text_style=text_style,
        )

    @validate_call
    def math_symbol(
        self,
        xy: Coordinate,
        symbol: MathSymbol,
        width: PosFloat,
        height: PosFloat | None = None,
        *,
        thickness_ratio: Ratio | None = None,
        style: Style,
        text: str = "",
        text_style: Style | None = None,
    ) -> None:
        """Draw a mathematical operator symbol shape (+, -, ×, ÷, =, ≠) on the canvas.

        Args:
            xy: Center coordinate tuple (x, y).
            symbol: Operator symbol ("+", "-", "*", "x", "×", "/", "÷", "=", "!=", "≠").
            width: Horizontal width of the symbol bounding box.
            height: Vertical height of the symbol bounding box (defaults to width when None).
            thickness_ratio: Bar thickness ratio relative to min(width, height).
                Defaults to 0.28 when None.
            style: Style object.
            text: Text to display inside shape.
            text_style: Style object for text or None.

        Raises:
            ValueError: If width, height, or thickness_ratio are out of valid bounds.
        """
        style, text_style = ShapeUtil.format_styles(style, text_style)
        eff_height = width if height is None else height
        if width <= 0.0 or eff_height <= 0.0:
            raise ValueError("width and height must be positive.")

        t_ratio = 0.28 if thickness_ratio is None else float(thickness_ratio)
        if not (0.0 < t_ratio < 1.0):
            raise ValueError("thickness_ratio must be strictly between 0.0 and 1.0.")

        (cx, cy), angle, style = ShapeUtil.prepare_centered_shape(xy, width, eff_height, style)

        path = _build_math_symbol_path(
            cx=cx,
            cy=cy,
            symbol=symbol,
            width=width,
            height=eff_height,
            t_ratio=t_ratio,
            angle=angle,
            shape_r=style.shape_r,
        )
        ShapeUtil.append_path_and_text(
            artists=self._artists,
            path=path,
            text_xy=(cx, cy),
            angle=angle,
            style=style,
            text=text,
            text_style=text_style,
        )


__all__ = [
    "CanvasShapeSymbolFeature",
]
