# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Module for generating official theme presets."""

from __future__ import annotations

from typing import Literal, overload

from drawlib._core.l3_fonts import Font, FontSourceCode
from drawlib._core.l3_styles import (
    Colors,
    Colors140,
    ColorsThemeDefault,
    ColorsThemeEssentials,
    ColorsThemeMonochrome,
    Style,
)
from drawlib._preset_styles._models import (
    BasePresetStyles,
    DefaultStyles,
    EssentialsStyles,
    MonochromeStyles,
    PresetStyles,
)


def get_default_styles() -> DefaultStyles:
    """Generate default theme preset.

    Returns:
        DefaultStyles: Default theme preset.
    """
    blue = ColorsThemeDefault.Blue
    black = ColorsThemeDefault.Black

    return DefaultStyles(
        primary=Style(
            text_color=blue,
            fill_color=blue,
            line_color=black,
            line_width=1.5,
            text_font=Font.SANSSERIF_REGULAR,
            text_size=16,
            icon_style="light",
        ),
        light=Style(
            text_color=blue,
            fill_color=blue,
            line_color=black,
            line_width=0.75,
            text_font=Font.SANSSERIF_LIGHT,
            text_size=16,
            icon_style="thin",
        ),
        bold=Style(
            text_color=blue,
            fill_color=blue,
            line_color=black,
            line_width=2.25,
            text_font=Font.SANSSERIF_BOLD,
            text_size=16,
            icon_style="regular",
        ),
        flat=Style(
            text_color=blue,
            fill_color=blue,
            line_color=blue,
            line_width=0,
            text_font=Font.SANSSERIF_REGULAR,
            text_size=16,
            icon_style="fill",
        ),
        solid=Style(
            text_color=blue,
            fill_color=Colors.Transparent,
            line_color=blue,
            line_width=1.5,
            text_font=Font.SANSSERIF_REGULAR,
            text_size=16,
            icon_style="regular",
        ),
        dashed=Style(
            text_color=blue,
            fill_color=Colors.Transparent,
            line_color=blue,
            line_width=1.5,
            line_style="dashed",
            text_font=Font.SANSSERIF_REGULAR,
            text_size=16,
            icon_style="regular",
        ),
        background_color=(255, 255, 255, 1.0),
        sourcecode_font=FontSourceCode.SOURCECODEPRO,
    )


def get_essentials_styles() -> EssentialsStyles:
    """Generate essentials theme preset.

    Returns:
        EssentialsStyles: Essentials theme preset.
    """
    charcoal = ColorsThemeEssentials.Charcoal
    lightblue = ColorsThemeEssentials.LightBlue

    return EssentialsStyles(
        primary=Style(
            text_color=lightblue,
            fill_color=lightblue,
            line_color=charcoal,
            line_width=1.5,
            text_font=Font.SANSSERIF_REGULAR,
            text_size=16,
            icon_style="light",
        ),
        light=Style(
            text_color=lightblue,
            fill_color=lightblue,
            line_color=charcoal,
            line_width=0.75,
            text_font=Font.SANSSERIF_LIGHT,
            text_size=16,
            icon_style="thin",
        ),
        bold=Style(
            text_color=lightblue,
            fill_color=lightblue,
            line_color=charcoal,
            line_width=2.25,
            text_font=Font.SANSSERIF_BOLD,
            text_size=16,
            icon_style="regular",
        ),
        flat=Style(
            text_color=lightblue,
            fill_color=lightblue,
            line_color=lightblue,
            line_width=0,
            text_font=Font.SANSSERIF_REGULAR,
            text_size=16,
            icon_style="fill",
        ),
        solid=Style(
            text_color=lightblue,
            fill_color=Colors.Transparent,
            line_color=lightblue,
            line_width=1.5,
            text_font=Font.SANSSERIF_REGULAR,
            text_size=16,
            icon_style="regular",
        ),
        dashed=Style(
            text_color=lightblue,
            fill_color=Colors.Transparent,
            line_color=lightblue,
            line_width=1.5,
            line_style="dashed",
            text_font=Font.SANSSERIF_REGULAR,
            text_size=16,
            icon_style="regular",
        ),
        background_color=(255, 255, 255, 1.0),
        sourcecode_font=FontSourceCode.SOURCECODEPRO,
    )


def get_monochrome_styles() -> MonochromeStyles:
    """Generate monochrome theme preset.

    Returns:
        MonochromeStyles: Monochrome theme preset.
    """
    black = ColorsThemeMonochrome.Black
    white = ColorsThemeMonochrome.White

    return MonochromeStyles(
        primary=Style(
            text_color=black,
            fill_color=white,
            line_color=black,
            line_width=1.5,
            text_font=Font.SANSSERIF_REGULAR,
            text_size=16,
            icon_style="light",
        ),
        light=Style(
            text_color=black,
            fill_color=white,
            line_color=black,
            line_width=0.75,
            text_font=Font.SANSSERIF_LIGHT,
            text_size=16,
            icon_style="thin",
        ),
        bold=Style(
            text_color=black,
            fill_color=white,
            line_color=black,
            line_width=2.25,
            text_font=Font.SANSSERIF_BOLD,
            text_size=16,
            icon_style="regular",
        ),
        flat=Style(
            text_color=black,
            fill_color=black,
            line_color=black,
            line_width=0,
            text_font=Font.SANSSERIF_REGULAR,
            text_size=16,
            icon_style="fill",
        ),
        solid=Style(
            text_color=black,
            fill_color=Colors.Transparent,
            line_color=black,
            line_width=1.5,
            text_font=Font.SANSSERIF_REGULAR,
            text_size=16,
            icon_style="regular",
        ),
        dashed=Style(
            text_color=black,
            fill_color=Colors.Transparent,
            line_color=black,
            line_width=1.5,
            line_style="dashed",
            text_font=Font.SANSSERIF_REGULAR,
            text_size=16,
            icon_style="regular",
        ),
        background_color=(255, 255, 255, 1.0),
        sourcecode_font=FontSourceCode.SOURCECODEPRO,
    )


@overload
def get_styles(name: Literal["default"] = "default") -> DefaultStyles: ...


@overload
def get_styles(name: Literal["essentials"]) -> EssentialsStyles: ...


@overload
def get_styles(name: Literal["monochrome"]) -> MonochromeStyles: ...


@overload
def get_styles(name: str) -> BasePresetStyles: ...


def get_styles(
    name: Literal["default", "essentials", "monochrome"] | str = "default",
) -> BasePresetStyles:
    """Get theme preset by name.

    Args:
        name: Theme name ("default", "essentials", "monochrome").

    Returns:
        BasePresetStyles: Theme preset object.
    """
    if name == "default":
        return get_default_styles()
    if name == "essentials":
        return get_essentials_styles()
    if name == "monochrome":
        return get_monochrome_styles()
    raise ValueError(f'Theme "{name}" is not supported.')


def _resolve_color(name: str) -> tuple[int, int, int] | tuple[int, int, int, float] | None:
    cap_name = name.capitalize()
    for colors_cls in (ColorsThemeEssentials, Colors140, Colors):
        if hasattr(colors_cls, cap_name):
            return getattr(colors_cls, cap_name)
        if hasattr(colors_cls, name):
            return getattr(colors_cls, name)
    return None


def get_style(style: Style | str | None = None) -> Style:
    """Get style object by preset name, color name, combined name (e.g. 'red_solid_bold'), or copy given Style.

    Args:
        style: Style instance, preset name ("primary", "light", "bold", "flat", "solid", "dashed",
            "solid_light", "solid_bold", "dashed_light", "dashed_bold"),
            color name (e.g. "red", "blue"), or combined name (e.g. "red_solid_bold").

    Returns:
        Style: Resolved Style object.
    """
    if isinstance(style, Style):
        return style.copy()

    preset = get_default_styles()

    solid_light = preset.solid.copy()
    solid_light.line_width = preset.light.line_width
    solid_light.text_font = preset.light.text_font

    solid_bold = preset.solid.copy()
    solid_bold.line_width = preset.bold.line_width
    solid_bold.text_font = preset.bold.text_font

    dashed_light = preset.dashed.copy()
    dashed_light.line_width = preset.light.line_width
    dashed_light.text_font = preset.light.text_font

    dashed_bold = preset.dashed.copy()
    dashed_bold.line_width = preset.bold.line_width
    dashed_bold.text_font = preset.bold.text_font

    style_map = {
        None: preset.primary,
        "": preset.primary,
        "primary": preset.primary,
        "light": preset.light,
        "bold": preset.bold,
        "flat": preset.flat,
        "solid": preset.solid,
        "dashed": preset.dashed,
        "solid_light": solid_light,
        "solid_bold": solid_bold,
        "dashed_light": dashed_light,
        "dashed_bold": dashed_bold,
    }

    if style in style_map:
        return style_map[style].copy()

    if isinstance(style, str):
        color_name = style
        preset_name = None

        preset_keys = [
            "solid_light",
            "solid_bold",
            "dashed_light",
            "dashed_bold",
            "primary",
            "light",
            "bold",
            "flat",
            "solid",
            "dashed",
        ]
        for pk in preset_keys:
            if style.endswith(f"_{pk}"):
                color_name = style[: -len(pk) - 1]
                preset_name = pk
                break

        color = _resolve_color(color_name)
        if color is not None:
            base_style = style_map[preset_name].copy() if preset_name in style_map else preset.primary.copy()
            base_style.text_color = color
            base_style.line_color = color
            if base_style.fill_color != Colors.Transparent:
                base_style.fill_color = color
            return base_style

    raise ValueError(f'Style preset "{style}" is not supported.')
