# Copyright (c) 2024 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.


"""Module for defining official themes."""

from __future__ import annotations

import dataclasses
from copy import deepcopy
from typing import List, Literal, Tuple, Union

from drawlib.v0_1.private.core.colors import (
    Colors,
    ColorsThemeDefault,
    ColorsThemeEssentials,
    ColorsThemeMonochrome,
)
from drawlib.v0_1.private.core.fonts import (
    Font,
    FontBase,
    FontSourceCode,
)
from drawlib.v0_1.private.core.model import (
    IconStyle,
    ImageStyle,
    LineStyle,
    OfficialThemeStyle,
    ShapeStyle,
    ShapeTextStyle,
    TextStyle,
    ThemeStyles,
)

#######################
# Official Themes ###
#######################


def get_default() -> OfficialThemeStyle:
    """Generate the default theme style configuration.

    Returns:
        OfficialThemeStyle: The default theme style configuration.
    """
    blue = ColorsThemeDefault.Blue
    green = ColorsThemeDefault.Green
    red = ColorsThemeDefault.Red
    black = ColorsThemeDefault.Black
    white = ColorsThemeDefault.White

    default_template = OfficialThemeTemplate(
        icon_style="light",
        icon_color=black,
        image_line_width=0,
        line_style="solid",
        line_width=2,
        line_color=black,
        arrowhead_scale=20,
        shape_line_style="solid",
        shape_line_width=1.5,
        shape_line_color=black,
        shape_fill_color=blue,
        shapetext_font=Font.SANSSERIF_REGULAR,
        shapetext_size=16,
        shapetext_color=black,
        text_font=Font.SANSSERIF_REGULAR,
        text_size=16,
        text_color=black,
    )

    default_light_template = OfficialThemeTemplate(
        icon_style="thin",
        icon_color=black,
        image_line_width=0,
        line_style="solid",
        line_width=1,
        line_color=black,
        arrowhead_scale=20,
        shape_line_style="solid",
        shape_line_width=0.75,
        shape_line_color=black,
        shape_fill_color=blue,
        shapetext_font=Font.SANSSERIF_LIGHT,
        shapetext_size=16,
        shapetext_color=white,
        text_font=Font.SANSSERIF_LIGHT,
        text_size=16,
        text_color=black,
    )

    default_bold_template = OfficialThemeTemplate(
        icon_style="regular",
        icon_color=black,
        image_line_width=0,
        line_style="solid",
        line_width=3,
        line_color=black,
        arrowhead_scale=30,
        shape_line_style="solid",
        shape_line_width=2.25,
        shape_line_color=black,
        shape_fill_color=blue,
        shapetext_font=Font.SANSSERIF_BOLD,
        shapetext_size=16,
        shapetext_color=white,
        text_font=Font.SANSSERIF_BOLD,
        text_size=16,
        text_color=black,
    )

    default_style = _generate_styles(default_template, is_default=True)
    colors = [
        ("red", red),
        ("green", green),
        ("blue", blue),
        ("black", black),
        ("white", white),
    ]
    named_styles = get_named_styles(
        default_template,
        default_light_template,
        default_bold_template,
        colors,
        black,
        blue,
    )

    return OfficialThemeStyle(
        default_style=default_style,
        named_styles=named_styles,
        theme_colors=colors,
        backgroundcolor=(255, 255, 255, 1.0),
        sourcecodefont=FontSourceCode.SOURCECODEPRO,
    )


def get_essentials() -> OfficialThemeStyle:
    """Generate the essentials theme style configuration.

    Returns:
        OfficialThemeStyle: The default theme style configuration.
    """
    red = ColorsThemeEssentials.Red
    lightred = ColorsThemeEssentials.LightRed
    green = ColorsThemeEssentials.Green
    lightgreen = ColorsThemeEssentials.LightGreen
    blue = ColorsThemeEssentials.Blue
    lightblue = ColorsThemeEssentials.LightBlue
    yellow = ColorsThemeEssentials.Yellow
    purple = ColorsThemeEssentials.Purple
    orange = ColorsThemeEssentials.Orange
    navy = ColorsThemeEssentials.Navy
    pink = ColorsThemeEssentials.Pink
    charcoal = ColorsThemeEssentials.Charcoal
    graphite = ColorsThemeEssentials.Graphite
    gray = ColorsThemeEssentials.Gray
    silver = ColorsThemeEssentials.Silver
    snow = ColorsThemeEssentials.Snow
    teal = ColorsThemeEssentials.Teal
    olive = ColorsThemeEssentials.Olive
    brown = ColorsThemeEssentials.Brown
    black = ColorsThemeEssentials.Black
    white = ColorsThemeEssentials.White
    aqua = ColorsThemeEssentials.Aqua
    greenyellow = ColorsThemeEssentials.GreenYellow
    ivory = ColorsThemeEssentials.Ivory
    steel = ColorsThemeEssentials.Steel

    default_template = OfficialThemeTemplate(
        icon_style="light",
        icon_color=charcoal,
        image_line_width=0,
        line_style="solid",
        line_width=2,
        line_color=charcoal,
        arrowhead_scale=20,
        shape_line_style="solid",
        shape_line_width=1.5,
        shape_line_color=charcoal,
        shape_fill_color=lightblue,
        shapetext_font=Font.SANSSERIF_REGULAR,
        shapetext_size=16,
        shapetext_color=charcoal,
        text_font=Font.SANSSERIF_REGULAR,
        text_size=16,
        text_color=charcoal,
    )

    default_light_template = OfficialThemeTemplate(
        icon_style="thin",
        icon_color=charcoal,
        image_line_width=0,
        line_style="solid",
        line_width=1,
        line_color=charcoal,
        arrowhead_scale=20,
        shape_line_style="solid",
        shape_line_width=0.75,
        shape_line_color=charcoal,
        shape_fill_color=lightblue,
        shapetext_font=Font.SANSSERIF_LIGHT,
        shapetext_size=16,
        shapetext_color=white,
        text_font=Font.SANSSERIF_LIGHT,
        text_size=16,
        text_color=charcoal,
    )

    default_bold_template = OfficialThemeTemplate(
        icon_style="regular",
        icon_color=charcoal,
        image_line_width=0,
        line_style="solid",
        line_width=3,
        line_color=charcoal,
        arrowhead_scale=30,
        shape_line_style="solid",
        shape_line_width=2.25,
        shape_line_color=charcoal,
        shape_fill_color=lightblue,
        shapetext_font=Font.SANSSERIF_BOLD,
        shapetext_size=16,
        shapetext_color=white,
        text_font=Font.SANSSERIF_BOLD,
        text_size=16,
        text_color=charcoal,
    )

    default_style = _generate_styles(default_template, is_default=True)
    colors = [
        ("red", red),
        ("lightred", lightred),
        ("pink", pink),
        ("brown", brown),
        ("orange", orange),
        ("green", green),
        ("lightgreen", lightgreen),
        ("greenyellow", greenyellow),
        ("teal", teal),
        ("olive", olive),
        ("blue", blue),
        ("lightblue", lightblue),
        ("aqua", aqua),
        ("navy", navy),
        ("steel", steel),
        ("yellow", yellow),
        ("purple", purple),
        ("ivory", ivory),
        ("black", black),
        ("charcoal", charcoal),
        ("graphite", graphite),
        ("gray", gray),
        ("silver", silver),
        ("snow", snow),
        ("white", white),
    ]
    named_styles = get_named_styles(
        default_template,
        default_light_template,
        default_bold_template,
        colors,
        charcoal,
        lightblue,
    )

    return OfficialThemeStyle(
        default_style=default_style,
        named_styles=named_styles,
        theme_colors=colors,
        backgroundcolor=(255, 255, 255, 1.0),
        sourcecodefont=FontSourceCode.SOURCECODEPRO,
    )


def get_monochrome() -> OfficialThemeStyle:
    """Generate the monochrome theme style configuration.

    Returns:
        OfficialThemeStyle: The default theme style configuration.
    """
    black = ColorsThemeMonochrome.Black
    charcoal = ColorsThemeMonochrome.Charcoal
    graphite = ColorsThemeMonochrome.Graphite
    gray = ColorsThemeMonochrome.Gray
    silver = ColorsThemeMonochrome.Silver
    snow = ColorsThemeMonochrome.Snow
    white = ColorsThemeMonochrome.White

    default_template = OfficialThemeTemplate(
        icon_style="light",
        icon_color=black,
        image_line_width=0,
        line_style="solid",
        line_width=2,
        line_color=black,
        arrowhead_scale=20,
        shape_line_style="solid",
        shape_line_width=1.5,
        shape_line_color=black,
        shape_fill_color=white,
        shapetext_font=Font.SANSSERIF_REGULAR,
        shapetext_size=16,
        shapetext_color=black,
        text_font=Font.SANSSERIF_REGULAR,
        text_size=16,
        text_color=black,
    )

    default_light_template = OfficialThemeTemplate(
        icon_style="thin",
        icon_color=black,
        image_line_width=0,
        line_style="solid",
        line_width=1,
        line_color=black,
        arrowhead_scale=20,
        shape_line_style="solid",
        shape_line_width=0.75,
        shape_line_color=black,
        shape_fill_color=white,
        shapetext_font=Font.SANSSERIF_LIGHT,
        shapetext_size=16,
        shapetext_color=black,
        text_font=Font.SANSSERIF_LIGHT,
        text_size=16,
        text_color=black,
    )

    default_bold_template = OfficialThemeTemplate(
        icon_style="regular",
        icon_color=black,
        image_line_width=0,
        line_style="solid",
        line_width=3,
        line_color=black,
        arrowhead_scale=30,
        shape_line_style="solid",
        shape_line_width=2.25,
        shape_line_color=black,
        shape_fill_color=white,
        shapetext_font=Font.SANSSERIF_BOLD,
        shapetext_size=16,
        shapetext_color=black,
        text_font=Font.SANSSERIF_BOLD,
        text_size=16,
        text_color=black,
    )

    default_style = _generate_styles(default_template, is_default=True)
    colors = [
        ("black", black),
        ("charcoal", charcoal),
        ("graphite", graphite),
        ("gray", gray),
        ("silver", silver),
        ("snow", snow),
        ("white", white),
    ]
    named_styles = get_named_styles(
        default_template,
        default_light_template,
        default_bold_template,
        colors,
        black,
        black,
    )

    return OfficialThemeStyle(
        default_style=default_style,
        named_styles=named_styles,
        theme_colors=colors,
        backgroundcolor=(255, 255, 255, 1.0),
        sourcecodefont=FontSourceCode.SOURCECODEPRO,
    )


#
# Data
#


@dataclasses.dataclass
class OfficialThemeTemplate:
    """Helper dataclass for defining theme styles"""

    def copy(self) -> OfficialThemeTemplate:
        """Creates a deep copy of the OfficialThemeTemplate instance.

        This method returns a new instance of OfficialThemeTemplate that is
        a deep copy of the current instance. Deep copying means that all
        nested objects are recursively copied, ensuring that modifications
        to the copy do not affect the original instance.

        Returns:
            OfficialThemeTemplate: A deep copy of the current instance.

        """
        return deepcopy(self)

    # icon
    icon_style: Literal["thin", "light", "regular", "bold", "fill"]
    icon_color: Union[
        Tuple[int, int, int],
        Tuple[int, int, int, float],
    ]
    image_line_width: float

    # line
    line_style: Literal["solid", "dashed", "dotted", "dashdot"]
    line_width: float
    line_color: Union[
        Tuple[int, int, int],
        Tuple[int, int, int, float],
    ]
    arrowhead_scale: int

    # shape
    shape_line_style: Literal["solid", "dashed", "dotted", "dashdot"]
    shape_line_width: float
    shape_line_color: Union[
        Tuple[int, int, int],
        Tuple[int, int, int, float],
    ]
    shape_fill_color: Union[
        Tuple[int, int, int],
        Tuple[int, int, int, float],
    ]

    # shapetext
    shapetext_font: FontBase
    shapetext_size: int
    shapetext_color: Union[
        Tuple[int, int, int],
        Tuple[int, int, int, float],
    ]

    # text
    text_font: FontBase
    text_size: int
    text_color: Union[
        Tuple[int, int, int],
        Tuple[int, int, int, float],
    ]


#
# Util
#


def get_named_styles(
    default_template: OfficialThemeTemplate,
    light_template: OfficialThemeTemplate,
    bold_template: OfficialThemeTemplate,
    colors: List[Tuple[str, Tuple[int, int, int]]],
    default_shapeline_color: Tuple[int, int, int],
    default_shapefill_color: Tuple[int, int, int],
) -> List[Tuple[str, ThemeStyles]]:
    """Generates a list of named styles based on the provided templates and colors.

    This function creates a variety of styles using the given templates and colors,
    and names them according to a specific pattern. It includes default, light, bold,
    flat, solid, and dashed styles, as well as custom styles for each color provided.

    Args:
        default_template (OfficialThemeTemplate): The default theme template.
        light_template (OfficialThemeTemplate): The light theme template.
        bold_template (OfficialThemeTemplate): The bold theme template.
        colors (Tuple[str, Union[Tuple[int, int, int], Tuple[int, int, int, float]]]):
            A tuple containing color names and their corresponding RGB or RGBA values.
        default_shapeline_color (Tuple[int, int, int]): The default shape line color as an RGB tuple.
        default_shapefill_color (Tuple[int, int, int]): The default shape fill color as an RGB tuple.

    Returns:
        List[Tuple[str, ThemeStyles]]: A list of tuples where each tuple contains a style name and
                                         its corresponding ThemeStyles object.

    """
    named_styles = [
        ("light", _generate_styles(light_template, is_default=True)),
        ("bold", _generate_styles(bold_template, is_default=True)),
        ("flat", _get_flat_style(default_template, default_shapefill_color)),
        ("solid", _get_solid_style(default_template, default_shapeline_color)),
        ("solid_light", _get_solid_style(light_template, default_shapeline_color)),
        ("solid_bold", _get_solid_style(bold_template, default_shapeline_color)),
        ("dashed", _get_dashed_style(default_template, default_shapeline_color)),
        ("dashed_light", _get_dashed_style(light_template, default_shapeline_color)),
        ("dashed_bold", _get_dashed_style(bold_template, default_shapeline_color)),
    ]

    for name, color in colors:
        for style_type in ["", "_flat", "_solid", "_dashed"]:
            for width_type, template in [("", default_template), ("_light", light_template), ("_bold", bold_template)]:
                if style_type == "":
                    named_styles.append((
                        f"{name}{width_type}",
                        _get_default_style(template, color, default_shapeline_color),
                    ))

                elif style_type == "_flat":
                    if width_type == "":
                        named_styles.append((f"{name}_flat", _get_flat_style(template, color)))

                elif style_type == "_solid":
                    named_styles.append((f"{name}_solid{width_type}", _get_solid_style(template, color)))

                elif style_type == "_dashed":
                    named_styles.append((f"{name}_dashed{width_type}", _get_dashed_style(template, color)))

    return named_styles


def _get_default_style(
    template: OfficialThemeTemplate,
    color: Union[
        Tuple[int, int, int],
        Tuple[int, int, int, float],
    ],
    shape_line_color: Union[
        Tuple[int, int, int],
        Tuple[int, int, int, float],
        None,
    ] = None,
) -> ThemeStyles:
    t = template.copy()
    t.icon_color = color
    t.image_line_width = t.shape_line_width
    t.line_color = color
    if shape_line_color is not None:
        t.shape_line_color = shape_line_color
    t.shape_fill_color = color
    t.shapetext_color = color
    t.text_color = color
    return _generate_styles(t)


def _get_flat_style(
    template: OfficialThemeTemplate,
    color: Union[
        Tuple[int, int, int],
        Tuple[int, int, int, float],
    ],
    shape_line_color: Union[
        Tuple[int, int, int],
        Tuple[int, int, int, float],
        None,
    ] = None,
) -> ThemeStyles:
    # image doesn't have border
    # shape has white border with white background

    t = template.copy()
    t.icon_color = color
    t.icon_style = "fill"
    t.image_line_width = 0
    t.line_color = color
    if shape_line_color is not None:
        t.shape_line_color = shape_line_color
    else:
        t.shape_line_color = color
    t.shape_fill_color = color
    t.shapetext_color = color
    t.text_color = color
    s = _generate_styles(t)
    s.linestyle = None
    s.shapetextstyle = None
    s.textstyle = None
    return s


def _get_solid_style(
    template: OfficialThemeTemplate,
    color: Union[
        Tuple[int, int, int],
        Tuple[int, int, int, float],
    ],
) -> ThemeStyles:
    t = template.copy()
    t.image_line_width = t.shape_line_width
    t.line_color = color
    t.shape_line_color = color
    t.shape_fill_color = Colors.Transparent
    s = _generate_styles(t)
    s.iconstyle = None
    s.shapetextstyle = None
    s.textstyle = None
    return s


def _get_dashed_style(
    template: OfficialThemeTemplate,
    color: Union[
        Tuple[int, int, int],
        Tuple[int, int, int, float],
    ],
) -> ThemeStyles:
    t = template.copy()
    t.image_line_width = t.shape_line_width
    t.line_color = color
    t.line_style = "dashed"
    t.shape_line_color = color
    t.shape_line_style = "dashed"
    t.shape_fill_color = Colors.Transparent
    s = _generate_styles(t)
    s.iconstyle = None
    s.shapetextstyle = None
    s.textstyle = None
    return s


def _generate_styles(
    template: OfficialThemeTemplate,
    is_default: bool = False,
) -> ThemeStyles:
    if is_default:
        imagestyle_fcolor = None
    elif template.shape_fill_color == Colors.Transparent:
        imagestyle_fcolor = None
    else:
        imagestyle_fcolor = template.shape_fill_color

    return ThemeStyles(
        iconstyle=IconStyle(
            style=template.icon_style,
            color=template.icon_color,
            halign="center",
            valign="center",
        ),
        imagestyle=ImageStyle(
            lwidth=template.image_line_width,
            lstyle=template.shape_line_style,
            lcolor=template.shape_line_color,
            fcolor=imagestyle_fcolor,
            halign="center",
            valign="center",
        ),
        linestyle=LineStyle(
            width=template.line_width,
            color=template.line_color,
            style=template.line_style,
        ),
        shapestyle=ShapeStyle(
            lwidth=template.shape_line_width,
            lstyle=template.shape_line_style,
            lcolor=template.shape_line_color,
            fcolor=template.shape_fill_color,
            halign="center",
            valign="center",
        ),
        shapetextstyle=ShapeTextStyle(
            font=template.text_font,
            size=template.text_size,
            color=template.shapetext_color,
            halign="center",
            valign="center",
        ),
        textstyle=TextStyle(
            font=template.text_font,
            size=template.text_size,
            color=template.text_color,
            halign="center",
            valign="center",
        ),
    )
