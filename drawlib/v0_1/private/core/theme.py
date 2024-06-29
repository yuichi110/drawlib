# Copyright (c) 2024 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.


"""dtheme implementation module."""

from __future__ import annotations

from typing import List, Literal, Optional, Tuple, Union

import drawlib.v0_1.private.validators.color as color_validator
import drawlib.v0_1.private.validators.text as text_validator
import drawlib.v0_1.private.validators.types as types_validator
from drawlib.v0_1.private.core import theme_officials
from drawlib.v0_1.private.core.colors import Colors
from drawlib.v0_1.private.core.fonts import (
    Font,
    FontArabic,
    FontBase,
    FontChinese,
    FontFile,
    FontJapanese,
    FontKorean,
    FontMonoSpace,
    FontRoboto,
    FontSansSerif,
    FontSerif,
    FontSourceCode,
)
from drawlib.v0_1.private.core.model import (
    IconStyle,
    ImageStyle,
    LineStyle,
    ShapeStyle,
    ShapeTextStyle,
    TextStyle,
    ThemeStyles,
)
from drawlib.v0_1.private.core.theme_style_caches import (
    AbstractStyleCache,
    # Patch Styles
    ArcStyleCache,
    ArcTextStyleCache,
    # Original arrows
    ArrowStyleCache,
    ArrowTextStyleCache,
    BackgroundColorCache,
    # Smart art
    BubblespeechStyleCache,
    BubblespeechTextStyleCache,
    # Original polygons
    ChevronStyleCache,
    ChevronTextStyleCache,
    CircleStyleCache,
    CircleTextStyleCache,
    DonutsStyleCache,
    DonutsTextStyleCache,
    EllipseStyleCache,
    EllipseTextStyleCache,
    FanStyleCache,
    FanTextStyleCache,
    IconStyleCache,
    ImageStyleCache,
    LineStyleCache,
    ParallelogramStyleCache,
    ParallelogramTextStyleCache,
    PolygonStyleCache,
    PolygonTextStyleCache,
    RectangleStyleCache,
    RectangleTextStyleCache,
    RegularpolygonStyleCache,
    RegularpolygonTextStyleCache,
    RhombusStyleCache,
    RhombusTextStyleCache,
    ShapeStyleCache,
    ShapeTextStyleCache,
    SourceCodeFontCache,
    StarStyleCache,
    StarTextStyleCache,
    TextStyleCache,
    ThemeColorCache,
    TrapezoidStyleCache,
    TrapezoidTextStyleCache,
    TriangleStyleCache,
    TriangleTextStyleCache,
    WedgeStyleCache,
    WedgeTextStyleCache,
)
from drawlib.v0_1.private.util import error_handler


class AllStyleModifier:
    """Utility class to modify styles within a Theme object.

    Attributes:
        _theme (Theme): The Theme object containing style collections.
    """

    def __init__(self, theme: Theme) -> None:
        """Initializes the AllStyleModifier with a Theme object.

        Args:
            theme (Theme): The Theme object to modify.
        """
        self._theme = theme

    @error_handler
    def list(self) -> List[str]:
        """List all style names present in the theme.

        Returns:
            List[str]: A list of style names.
        """
        return self._theme._style_names.copy()

    @error_handler
    def copy(self, from_name: str, to_name: str) -> None:
        """Copy a style from `from_name` to `to_name`.

        Args:
            from_name (str): The name of the style to copy from.
            to_name (str): The name of the style to copy to.

        Raises:
            ValueError: If `from_name` does not exist in the theme.
        """
        if from_name not in self._theme._style_names:
            raise ValueError(f'Original style name "{from_name}" does not exist.')

        for style in self._theme._get_style_caches():
            if not style.has(from_name):
                continue
            style.set(style.get(from_name), to_name)

    @error_handler
    def delete(self, name: str) -> None:
        """Delete a style with the given `name`.

        Args:
            name (str): The name of the style to delete.

        Raises:
            ValueError: If attempting to delete the default style name.
        """
        if name == "":
            raise ValueError("Deleting default style name is prohibited.")

        for style in self._theme._get_style_caches():
            if not style.has(name):
                continue
            style.delete(name)

    @error_handler
    def rename(self, from_name: str, to_name: str) -> None:
        """Rename a style from `from_name` to `to_name`.

        Args:
            from_name (str): The current name of the style.
            to_name (str): The new name to assign to the style.

        Raises:
            ValueError: If `from_name` is empty(default style) or does not exist in the theme.
        """
        if from_name == "":
            raise ValueError("Renaming default style name is prohibited.")
        if from_name not in self._theme._style_names:
            raise ValueError(f'Original style name "{from_name}" does not exist.')

        index = self._theme._style_names.index(from_name)
        self.copy(from_name, to_name)
        self.delete(from_name)
        self._theme._style_names.pop()
        self._theme._style_names.insert(index, to_name)

    @error_handler
    def merge(self, theme_styles: ThemeStyles, targets: Optional[List[str]] = None) -> None:  # noqa: C901
        """Merge styles from `theme_styles` into corresponding style collections in the theme.

        Args:
            theme_styles (ThemeStyles): The dtheme.ThemeStyles object containing styles to merge.
            targets (Optional[List[str]], optional): List of specific style names to target for merging.

        Notes:
            This method merges styles from `theme_styles` into corresponding style collections
            in the theme object.
        """
        # basics
        if theme_styles.iconstyle is not None:
            self._theme.iconstyles.merge(theme_styles.iconstyle, targets)
        if theme_styles.imagestyle is not None:
            self._theme.imagestyles.merge(theme_styles.imagestyle, targets)
        if theme_styles.linestyle is not None:
            self._theme.linestyles.merge(theme_styles.linestyle, targets)
        if theme_styles.shapestyle is not None:
            self._theme.shapestyles.merge(theme_styles.shapestyle, targets)
        if theme_styles.shapetextstyle is not None:
            self._theme.shapetextstyles.merge(theme_styles.shapetextstyle, targets)
        if theme_styles.textstyle is not None:
            self._theme.textstyles.merge(theme_styles.textstyle, targets)

        # patchs
        if theme_styles.arcstyle is not None:
            self._theme.arcstyles.merge(theme_styles.arcstyle, targets)
        if theme_styles.arctextstyle is not None:
            self._theme.arctextstyles.merge(theme_styles.arctextstyle, targets)
        if theme_styles.circlestyle is not None:
            self._theme.circlestyles.merge(theme_styles.circlestyle, targets)
        if theme_styles.circletextstyle is not None:
            self._theme.circletextstyles.merge(theme_styles.circletextstyle, targets)
        if theme_styles.donutsstyle is not None:
            self._theme.donutsstyles.merge(theme_styles.donutsstyle, targets)
        if theme_styles.donutstextstyle is not None:
            self._theme.donutstextstyles.merge(theme_styles.donutstextstyle, targets)
        if theme_styles.ellipsestyle is not None:
            self._theme.ellipsestyles.merge(theme_styles.ellipsestyle, targets)
        if theme_styles.ellipsetextstyle is not None:
            self._theme.ellipsetextstyles.merge(theme_styles.ellipsetextstyle, targets)
        if theme_styles.fanstyle is not None:
            self._theme.fanstyles.merge(theme_styles.fanstyle, targets)
        if theme_styles.fantextstyle is not None:
            self._theme.fantextstyles.merge(theme_styles.fantextstyle, targets)
        if theme_styles.polygonstyle is not None:
            self._theme.polygonstyles.merge(theme_styles.polygonstyle, targets)
        if theme_styles.polygontextstyle is not None:
            self._theme.polygontextstyles.merge(theme_styles.polygontextstyle, targets)
        if theme_styles.rectanglestyle is not None:
            self._theme.rectanglestyles.merge(theme_styles.rectanglestyle, targets)
        if theme_styles.rectangletextstyle is not None:
            self._theme.rectangletextstyles.merge(theme_styles.rectangletextstyle, targets)
        if theme_styles.regularpolygonstyle is not None:
            self._theme.regularpolygonstyles.merge(theme_styles.regularpolygonstyle, targets)
        if theme_styles.regularpolygontextstyle is not None:
            self._theme.regularpolygontextstyles.merge(theme_styles.regularpolygontextstyle, targets)
        if theme_styles.wedgestyle is not None:
            self._theme.wedgestyles.merge(theme_styles.wedgestyle, targets)
        if theme_styles.wedgetextstyle is not None:
            self._theme.wedgetextstyles.merge(theme_styles.wedgetextstyle, targets)

        # original
        if theme_styles.arrowstyle is not None:
            self._theme.arrowstyles.merge(theme_styles.arrowstyle, targets)
        if theme_styles.arrowtextstyle is not None:
            self._theme.arrowtextstyles.merge(theme_styles.arrowtextstyle, targets)
        if theme_styles.chevronstyle is not None:
            self._theme.chevronstyles.merge(theme_styles.chevronstyle, targets)
        if theme_styles.chevrontextstyle is not None:
            self._theme.chevrontextstyles.merge(theme_styles.chevrontextstyle, targets)
        if theme_styles.parallelogramstyle is not None:
            self._theme.parallelogramstyles.merge(theme_styles.parallelogramstyle, targets)
        if theme_styles.parallelogramtextstyle is not None:
            self._theme.parallelogramtextstyles.merge(theme_styles.parallelogramtextstyle, targets)
        if theme_styles.rhombusstyle is not None:
            self._theme.rhombusstyles.merge(theme_styles.rhombusstyle, targets)
        if theme_styles.rhombustextstyle is not None:
            self._theme.rhombustextstyles.merge(theme_styles.rhombustextstyle, targets)
        if theme_styles.starstyle is not None:
            self._theme.starstyles.merge(theme_styles.starstyle, targets)
        if theme_styles.startextstyle is not None:
            self._theme.startextstyles.merge(theme_styles.startextstyle, targets)
        if theme_styles.trapezoidstyle is not None:
            self._theme.trapezoidstyles.merge(theme_styles.trapezoidstyle, targets)
        if theme_styles.trapezoidtextstyle is not None:
            self._theme.trapezoidtextstyles.merge(theme_styles.trapezoidtextstyle, targets)
        if theme_styles.trianglestyle is not None:
            self._theme.trianglestyles.merge(theme_styles.trianglestyle, targets)
        if theme_styles.triangletextstyle is not None:
            self._theme.triangletextstyles.merge(theme_styles.triangletextstyle, targets)

        # smart art
        if theme_styles.bubblespeechstyle is not None:
            self._theme.bubblespeechstyles.merge(theme_styles.bubblespeechstyle, targets)
        if theme_styles.bubblespeechtextstyle is not None:
            self._theme.bubblespeechtextstyles.merge(theme_styles.bubblespeechtextstyle, targets)


class Theme:
    """Drawlib Theme control class.

    This class handles the management and customization of themes within the Drawlib library.
    It provides methods to apply official themes, change default styles, and list available themes.
    """

    ThemeStyles = ThemeStyles

    @error_handler
    def __init__(self) -> None:
        """Initialize the Theme object.

        This constructor initializes all styles and applies the default theme.
        """
        self.allstyles = AllStyleModifier(self)
        self.apply_official_theme("default")

    @error_handler
    def change_default_linearrow_fill(self, fill: bool) -> None:
        """Change the default fill setting for line arrows.

        Args:
            fill (bool): A boolean indicating whether to fill line arrows.

        Returns:
            None
        """
        types_validator.validate_bool("fill", fill)
        self.linestyles.merge(LineStyle(ahfill=fill))

    @error_handler
    def change_default_font_size(self, size: float) -> None:
        """Change the default font size for text and shape text.

        Args:
            size (float): A positive float representing the new font size. Zero is not acceptable.

        Returns:
            None
        """
        types_validator.validate_plus_float("size", size, is_0_ok=False)
        self.textstyles.merge(TextStyle(size=size))
        self.shapetextstyles.merge(ShapeTextStyle(size=size))

    @error_handler
    def change_default_fonts(
        self,
        light_font: Union[
            Font,
            FontArabic,
            FontBase,
            FontSerif,
            FontSansSerif,
            FontChinese,
            FontJapanese,
            FontKorean,
            FontMonoSpace,
            FontRoboto,
            FontSourceCode,
            FontFile,
        ],
        regular_font: Union[
            Font,
            FontArabic,
            FontBase,
            FontSerif,
            FontSansSerif,
            FontChinese,
            FontJapanese,
            FontKorean,
            FontMonoSpace,
            FontRoboto,
            FontSourceCode,
            FontFile,
        ],
        bold_font: Union[
            Font,
            FontArabic,
            FontBase,
            FontSerif,
            FontSansSerif,
            FontChinese,
            FontJapanese,
            FontKorean,
            FontMonoSpace,
            FontRoboto,
            FontSourceCode,
            FontFile,
        ],
    ) -> None:
        """Change the default fonts for light, regular, and bold text styles.

        Args:
            light_font: The font to use for light text styles.
            regular_font: The font to use for regular text styles.
            bold_font: The font to use for bold text styles.

        Returns:
            None
        """
        text_validator.validate_font("light_font", light_font)
        text_validator.validate_font("regular_font", regular_font)
        text_validator.validate_font("bold_font", bold_font)

        # create target lists
        light_styles = ["light"]
        regular_styles = [""]
        bold_styles = ["bold"]
        for color_name in self.colors.list():
            light_styles.append(f"{color_name}_light")
            regular_styles.append(color_name)
            bold_styles.append(f"{color_name}_bold")

        # merge light
        self.textstyles.merge(TextStyle(font=light_font), targets=light_styles)
        self.shapetextstyles.merge(ShapeTextStyle(font=light_font), targets=light_styles)

        # merge regular
        self.textstyles.merge(TextStyle(font=regular_font), targets=regular_styles)
        self.shapetextstyles.merge(ShapeTextStyle(font=regular_font), targets=regular_styles)

        # merge bold
        self.textstyles.merge(TextStyle(font=bold_font), targets=bold_styles)
        self.shapetextstyles.merge(ShapeTextStyle(font=bold_font), targets=bold_styles)

    @staticmethod
    @error_handler
    def list_official_themes() -> List[str]:
        """List all available official themes.

        Returns:
            List[str]: A list of names of official themes.
        """
        return [
            "default",
            "essentials",
            "monochrome",
        ]

    @error_handler
    def apply_official_theme(
        self,
        name: Literal[
            "default",
            "essentials",
            "monochrome",
        ],
    ) -> None:
        """Apply an official theme by name.

        Args:
            name (Literal['default', 'essentials', 'monochrome']): The name of the official theme to apply.

        Raises:
            ValueError: If the provided theme name is not supported.

        Returns:
            None
        """
        if name == "default":
            t = theme_officials.get_default()
        elif name == "essentials":
            t = theme_officials.get_essentials()
        elif name == "monochrome":
            t = theme_officials.get_monochrome()
        else:
            raise ValueError(f'Theme "{name}" is not supported.')

        self.apply_custom_theme(
            default_style=t.default_style,
            named_styles=t.named_styles,
            theme_colors=t.theme_colors,
            backgroundcolor=t.backgroundcolor,
            sourcecodefont=t.sourcecodefont,
        )

    @error_handler
    def print_theme_colors(self) -> None:
        """Print the current theme colors.

        Returns:
            None
        """
        print(self._get_theme_colors())

    @error_handler
    def print_style_table(self, max_columns: int = 11) -> None:
        """Print a table of styles with a specified maximum number of columns.

        Args:
            max_columns (int, optional): The maximum number of columns to display in the style table. Default is 11.

        Returns:
            None
        """
        types_validator.validate_plus_int("max_columns", max_columns)
        if max_columns <= 1:
            raise ValueError("max_column must be bigger than 2.")
        print(self._get_style_table(max_columns))

    @error_handler
    def apply_custom_theme(  # noqa: C901
        self,
        default_style: Theme.ThemeStyles,
        named_styles: Optional[
            List[
                Tuple[
                    str,
                    Theme.ThemeStyles,
                ]
            ]
        ] = None,
        theme_colors: Optional[List[Tuple[str, Tuple[int, int, int]]]] = None,
        backgroundcolor: Union[Tuple[int, int, int], Tuple[int, int, int, float]] = Colors.White,
        sourcecodefont: Optional[FontSourceCode] = FontSourceCode.SOURCECODEPRO,
    ) -> None:
        """Apply a custom theme.

        Args:
            default_style (dtheme.ThemeStyles): The default theme styles to be applied.
            named_styles (List[Tuple[str, Theme.ThemeStyles]], optional):
                A list of named theme styles.
                Each tuple contains a name and a `ThemeStyles` object. Defaults to [].
            theme_colors (List[Tuple[str, Union[Tuple[int, int, int], Tuple[int, int, int, float]]]], optional):
                A list of theme colors. Each tuple contains a name and a color
                in the format (R, G, B) or (R, G, B, A). Defaults to [].
            backgroundcolor (Union[Tuple[int, int, int], Tuple[int, int, int, float]], optional):
                The background color in the format (R, G, B) or (R, G, B, A). Defaults to Colors.White.
            sourcecodefont (Optional[FontSourceCode], optional): The source code font.
                Defaults to FontSourceCode.SOURCECODEPRO.

        Raises:
            ValueError: If any of the style or color formats are incorrect.

        Returns:
            None
        """
        if named_styles is None:
            named_styles = []
        if theme_colors is None:
            theme_colors = []

        # initialize
        self._initialize()

        # set default background color
        color_validator.validate_color(
            "backgroundcolor",
            backgroundcolor,
        )
        self.backgroundcolors.set(backgroundcolor)

        # set default soucecode font
        if not isinstance(sourcecodefont, FontSourceCode):
            raise ValueError("default_style.sourcecodefont is mandatory. Type must be FontSourceCode.")
        self.sourcecodefonts.set(sourcecodefont)

        # set default styles
        if not isinstance(default_style.iconstyle, IconStyle):
            raise ValueError("default_style.iconstyle is mandatory. Type must be IconStyle.")
        self.iconstyles.set(default_style.iconstyle)

        if not isinstance(default_style.imagestyle, ImageStyle):
            raise ValueError("default_style.imagestyle is mandatory. Type must be ImageStyle.")
        self.imagestyles.set(default_style.imagestyle)

        if not isinstance(default_style.linestyle, LineStyle):
            raise ValueError("default_style.linestyle is mandatory. Type must be LineStyle.")
        self.linestyles.set(default_style.linestyle)

        if not isinstance(default_style.shapestyle, ShapeStyle):
            raise ValueError("default_style.shapestyle is mandatory. Type must be ShapeStyle.")
        self.shapestyles.set(default_style.shapestyle)

        if not isinstance(default_style.shapetextstyle, ShapeTextStyle):
            raise ValueError("default_style.shapetextstyle is mandatory. Type must be ShapeTextStyle.")
        self.shapetextstyles.set(default_style.shapetextstyle)

        if not isinstance(default_style.textstyle, TextStyle):
            raise ValueError("default_style.textstyle is mandatory. Type must be TextStyle.")
        self.textstyles.set(default_style.textstyle)

        for (
            shapestyle_name,
            shapestyle_object,
            shapestyle_setter,
            shapetextstyle_name,
            shapetextstyle_object,
            shapetextstyle_setter,
        ) in [
            (
                "default_style.arcstyle",
                default_style.arcstyle,
                self.arcstyles.set,
                "default_style.arctextstyle",
                default_style.arctextstyle,
                self.arctextstyles.set,
            ),
            (
                "default_style.circlestyle",
                default_style.circlestyle,
                self.circlestyles.set,
                "default_style.circletextstyle",
                default_style.circletextstyle,
                self.circletextstyles.set,
            ),
            (
                "default_style.ellipsestyle",
                default_style.ellipsestyle,
                self.ellipsestyles.set,
                "default_style.ellipsetextstyle",
                default_style.ellipsetextstyle,
                self.ellipsetextstyles.set,
            ),
            (
                "default_style.polygonstyle",
                default_style.polygonstyle,
                self.polygonstyles.set,
                "default_style.polygontextstyle",
                default_style.polygontextstyle,
                self.polygontextstyles.set,
            ),
            (
                "default_style.rectanglestyle",
                default_style.rectanglestyle,
                self.rectanglestyles.set,
                "default_style.rectangletextstyle",
                default_style.rectangletextstyle,
                self.rectangletextstyles.set,
            ),
            (
                "default_style.regularpolygonstyle",
                default_style.regularpolygonstyle,
                self.regularpolygonstyles.set,
                "default_style.regularpolygontextstyle",
                default_style.regularpolygontextstyle,
                self.regularpolygontextstyles.set,
            ),
            (
                "default_style.wedgestyle",
                default_style.wedgestyle,
                self.wedgestyles.set,
                "default_style.wedgetextstyle",
                default_style.wedgetextstyle,
                self.wedgetextstyles.set,
            ),
            (
                "default_style.donutsstyle",
                default_style.donutsstyle,
                self.donutsstyles.set,
                "default_style.donutstextstyle",
                default_style.donutstextstyle,
                self.donutstextstyles.set,
            ),
            (
                "default_style.fanstyle",
                default_style.fanstyle,
                self.fanstyles.set,
                "default_style.fantextstyle",
                default_style.fantextstyle,
                self.fantextstyles.set,
            ),
            (
                "default_style.arrowstyle",
                default_style.arrowstyle,
                self.arrowstyles.set,
                "default_style.arrowtextstyle",
                default_style.arrowtextstyle,
                self.arrowtextstyles.set,
            ),
            (
                "default_style.rhombusstyle",
                default_style.rhombusstyle,
                self.rhombusstyles.set,
                "default_style.rhombustextstyle",
                default_style.rhombustextstyle,
                self.rhombustextstyles.set,
            ),
            (
                "default_style.parallelogramstyle",
                default_style.parallelogramstyle,
                self.parallelogramstyles.set,
                "default_style.parallelogramtextstyle",
                default_style.parallelogramtextstyle,
                self.parallelogramtextstyles.set,
            ),
            (
                "default_style.trapezoidstyle",
                default_style.trapezoidstyle,
                self.trapezoidstyles.set,
                "default_style.trapezoidtextstyle",
                default_style.trapezoidtextstyle,
                self.trapezoidtextstyles.set,
            ),
            (
                "default_style.trianglestyle",
                default_style.trianglestyle,
                self.trianglestyles.set,
                "default_style.triangletextstyle",
                default_style.triangletextstyle,
                self.triangletextstyles.set,
            ),
            (
                "default_style.starstyle",
                default_style.starstyle,
                self.starstyles.set,
                "default_style.startextstyle",
                default_style.startextstyle,
                self.startextstyles.set,
            ),
            (
                "default_style.chevronstyle",
                default_style.chevronstyle,
                self.chevronstyles.set,
                "default_style.chevrontextstyle",
                default_style.chevrontextstyle,
                self.chevrontextstyles.set,
            ),
            (
                "default_style.bubblespeechstyle",
                default_style.bubblespeechstyle,
                self.bubblespeechstyles.set,
                "default_style.bubblespeechtextstyle",
                default_style.bubblespeechtextstyle,
                self.bubblespeechtextstyles.set,
            ),
        ]:
            if shapestyle_object is not None:
                if not isinstance(shapestyle_object, ShapeStyle):
                    raise ValueError(f"{shapestyle_name} is optional. But type must be None or ShapeStyle")
                shapestyle_setter(shapestyle_object)

            if shapetextstyle_object is not None:
                if not isinstance(shapetextstyle_object, ShapeTextStyle):
                    raise ValueError(f"{shapetextstyle_name} is optional. But type must be None or ShapeTextStyle")
                shapetextstyle_setter(shapetextstyle_object)

        # named styles
        for name, styles in named_styles:
            if styles.iconstyle is not None:
                if not isinstance(styles.iconstyle, IconStyle):
                    raise ValueError(f"name={name}, ThemeStyle.iconstyle type must be IconStyle.")
                self.iconstyles.set(styles.iconstyle, name)

            if styles.imagestyle is not None:
                if not isinstance(styles.imagestyle, ImageStyle):
                    raise ValueError(f"name={name}, ThemeStyle.imagestyle type must be ImageStyle.")
                self.imagestyles.set(styles.imagestyle, name)

            if styles.linestyle is not None:
                if not isinstance(styles.linestyle, LineStyle):
                    raise ValueError(f"name={name}, ThemeStyle.linestyle type must be LineStyle.")
                self.linestyles.set(styles.linestyle, name)

            if styles.shapestyle is not None:
                if not isinstance(styles.shapestyle, ShapeStyle):
                    raise ValueError(f"name={name}, ThemeStyle.shapestyle type must be ShapeStyle.")
                self.shapestyles.set(styles.shapestyle, name)

            if styles.shapetextstyle is not None:
                if not isinstance(styles.shapetextstyle, ShapeTextStyle):
                    raise ValueError(f"name={name}, ThemeStyle.shapetextstyle type must be ShapeTextStyle.")
                self.shapetextstyles.set(styles.shapetextstyle, name)

            if styles.textstyle is not None:
                if not isinstance(styles.textstyle, TextStyle):
                    raise ValueError(f"name={name}, ThemeStyle.textstyle type must be TextStyle.")
                self.textstyles.set(styles.textstyle, name)

            for (
                shapestyle_name,
                shapestyle_object,
                shapestyle_setter,
                shapetextstyle_name,
                shapetextstyle_object,
                shapetextstyle_setter,
            ) in [
                (
                    "arcstyle",
                    styles.arcstyle,
                    self.arcstyles.set,
                    "arctextstyle",
                    styles.arctextstyle,
                    self.arctextstyles.set,
                ),
                (
                    "circlestyle",
                    styles.circlestyle,
                    self.circlestyles.set,
                    "circletextstyle",
                    styles.circletextstyle,
                    self.circletextstyles.set,
                ),
                (
                    "ellipsestyle",
                    styles.ellipsestyle,
                    self.ellipsestyles.set,
                    "ellipsetextstyle",
                    styles.ellipsetextstyle,
                    self.ellipsetextstyles.set,
                ),
                (
                    "polygonstyle",
                    styles.polygonstyle,
                    self.polygonstyles.set,
                    "polygontextstyle",
                    styles.polygontextstyle,
                    self.polygontextstyles.set,
                ),
                (
                    "rectanglestyle",
                    styles.rectanglestyle,
                    self.rectanglestyles.set,
                    "rectangletextstyle",
                    styles.rectangletextstyle,
                    self.rectangletextstyles.set,
                ),
                (
                    "regularpolygonstyle",
                    styles.regularpolygonstyle,
                    self.regularpolygonstyles.set,
                    "regularpolygontextstyle",
                    styles.regularpolygontextstyle,
                    self.regularpolygontextstyles.set,
                ),
                (
                    "wedgestyle",
                    styles.wedgestyle,
                    self.wedgestyles.set,
                    "wedgetextstyle",
                    styles.wedgetextstyle,
                    self.wedgetextstyles.set,
                ),
                (
                    "donutsstyle",
                    styles.donutsstyle,
                    self.donutsstyles.set,
                    "donutstextstyle",
                    styles.donutstextstyle,
                    self.donutstextstyles.set,
                ),
                (
                    "fanstyle",
                    styles.fanstyle,
                    self.fanstyles.set,
                    "fantextstyle",
                    styles.fantextstyle,
                    self.fantextstyles.set,
                ),
                (
                    "arrowstyle",
                    styles.arrowstyle,
                    self.arrowstyles.set,
                    "arrowtextstyle",
                    styles.arrowtextstyle,
                    self.arrowtextstyles.set,
                ),
                (
                    "rhombusstyle",
                    styles.rhombusstyle,
                    self.rhombusstyles.set,
                    "rhombustextstyle",
                    styles.rhombustextstyle,
                    self.rhombustextstyles.set,
                ),
                (
                    "parallelogramstyle",
                    styles.parallelogramstyle,
                    self.parallelogramstyles.set,
                    "parallelogramtextstyle",
                    styles.parallelogramtextstyle,
                    self.parallelogramtextstyles.set,
                ),
                (
                    "trapezoidstyle",
                    styles.trapezoidstyle,
                    self.trapezoidstyles.set,
                    "trapezoidtextstyle",
                    styles.trapezoidtextstyle,
                    self.trapezoidtextstyles.set,
                ),
                (
                    "trianglestyle",
                    styles.trianglestyle,
                    self.trianglestyles.set,
                    "triangletextstyle",
                    styles.triangletextstyle,
                    self.triangletextstyles.set,
                ),
                (
                    "starstyle",
                    styles.starstyle,
                    self.starstyles.set,
                    "startextstyle",
                    styles.startextstyle,
                    self.startextstyles.set,
                ),
                (
                    "chevronstyle",
                    styles.chevronstyle,
                    self.chevronstyles.set,
                    "chevrontextstyle",
                    styles.chevrontextstyle,
                    self.chevrontextstyles.set,
                ),
                (
                    "bubblespeechstyle",
                    styles.bubblespeechstyle,
                    self.bubblespeechstyles.set,
                    "bubblespeechtextstyle",
                    styles.bubblespeechtextstyle,
                    self.bubblespeechtextstyles.set,
                ),
            ]:
                if shapestyle_object is not None:
                    if not isinstance(shapestyle_object, ShapeStyle):
                        raise ValueError(
                            f'name="{name}" ThemeStyles.{shapestyle_name} is optional.'
                            " But type must be None or ShapeStyle"
                        )
                    shapestyle_setter(shapestyle_object, name)

                if shapetextstyle_object is not None:
                    if not isinstance(shapetextstyle_object, ShapeTextStyle):
                        raise ValueError(
                            f'name="{name}" ThemeStyles.{shapetextstyle_name} is optional.'
                            " But type must be None or ShapeTextStyle"
                        )
                    shapetextstyle_setter(shapetextstyle_object, name)

        for t in theme_colors:
            if not isinstance(t, tuple):
                raise ValueError()
            if len(t) != 2:
                raise ValueError()

            name, theme_color = t
            if not isinstance(name, str):
                raise ValueError()
            color_validator.validate_color(
                "theme_color(elem of theme_colors)",
                theme_color,
            )

            self.colors.set(theme_color, name)

    #
    # Private
    #

    @error_handler
    def _initialize(self) -> None:
        """Initialize the theme.

        This method needs to be called before setting a manual theme.

        Returns:
            None
        """
        self._style_names: List[str] = []

        self.colors = ThemeColorCache()
        self.backgroundcolors = BackgroundColorCache()
        self.sourcecodefonts = SourceCodeFontCache()
        self.iconstyles = IconStyleCache(self._callback_set, self._callback_delete)
        self.imagestyles = ImageStyleCache(self._callback_set, self._callback_delete)
        self.linestyles = LineStyleCache(self._callback_set, self._callback_delete)
        self.shapestyles = ShapeStyleCache(self._callback_set, self._callback_delete)
        self.shapetextstyles = ShapeTextStyleCache(self._callback_set, self._callback_delete)
        self.textstyles = TextStyleCache(self._callback_set, self._callback_delete)

        # patchs
        self.arcstyles = ArcStyleCache(self.shapestyles, self._callback_set, self._callback_delete)
        self.arctextstyles = ArcTextStyleCache(self.shapetextstyles, self._callback_set, self._callback_delete)
        self.circlestyles = CircleStyleCache(self.shapestyles, self._callback_set, self._callback_delete)
        self.circletextstyles = CircleTextStyleCache(self.shapetextstyles, self._callback_set, self._callback_delete)
        self.donutsstyles = DonutsStyleCache(self.shapestyles, self._callback_set, self._callback_delete)
        self.donutstextstyles = DonutsTextStyleCache(self.shapetextstyles, self._callback_set, self._callback_delete)
        self.ellipsestyles = EllipseStyleCache(self.shapestyles, self._callback_set, self._callback_delete)
        self.ellipsetextstyles = EllipseTextStyleCache(self.shapetextstyles, self._callback_set, self._callback_delete)
        self.fanstyles = FanStyleCache(self.shapestyles, self._callback_set, self._callback_delete)
        self.fantextstyles = FanTextStyleCache(self.shapetextstyles, self._callback_set, self._callback_delete)
        self.polygonstyles = PolygonStyleCache(self.shapestyles, self._callback_set, self._callback_delete)
        self.polygontextstyles = PolygonTextStyleCache(self.shapetextstyles, self._callback_set, self._callback_delete)
        self.rectanglestyles = RectangleStyleCache(self.shapestyles, self._callback_set, self._callback_delete)
        self.rectangletextstyles = RectangleTextStyleCache(
            self.shapetextstyles, self._callback_set, self._callback_delete
        )
        self.regularpolygonstyles = RegularpolygonStyleCache(
            self.shapestyles, self._callback_set, self._callback_delete
        )
        self.regularpolygontextstyles = RegularpolygonTextStyleCache(
            self.shapetextstyles, self._callback_set, self._callback_delete
        )
        self.wedgestyles = WedgeStyleCache(self.shapestyles, self._callback_set, self._callback_delete)
        self.wedgetextstyles = WedgeTextStyleCache(self.shapetextstyles, self._callback_set, self._callback_delete)

        # original arrows
        self.arrowstyles = ArrowStyleCache(self.shapestyles, self._callback_set, self._callback_delete)
        self.arrowtextstyles = ArrowTextStyleCache(self.shapetextstyles, self._callback_set, self._callback_delete)

        # original polygons
        self.chevronstyles = ChevronStyleCache(self.shapestyles, self._callback_set, self._callback_delete)
        self.chevrontextstyles = ChevronTextStyleCache(self.shapetextstyles, self._callback_set, self._callback_delete)
        self.parallelogramstyles = ParallelogramStyleCache(self.shapestyles, self._callback_set, self._callback_delete)
        self.parallelogramtextstyles = ParallelogramTextStyleCache(
            self.shapetextstyles, self._callback_set, self._callback_delete
        )
        self.rhombusstyles = RhombusStyleCache(self.shapestyles, self._callback_set, self._callback_delete)
        self.rhombustextstyles = RhombusTextStyleCache(self.shapetextstyles, self._callback_set, self._callback_delete)
        self.starstyles = StarStyleCache(self.shapestyles, self._callback_set, self._callback_delete)
        self.startextstyles = StarTextStyleCache(self.shapetextstyles, self._callback_set, self._callback_delete)
        self.trapezoidstyles = TrapezoidStyleCache(self.shapestyles, self._callback_set, self._callback_delete)
        self.trapezoidtextstyles = TrapezoidTextStyleCache(
            self.shapetextstyles, self._callback_set, self._callback_delete
        )
        self.trianglestyles = TriangleStyleCache(self.shapestyles, self._callback_set, self._callback_delete)
        self.triangletextstyles = TriangleTextStyleCache(
            self.shapetextstyles, self._callback_set, self._callback_delete
        )

        # smart art
        self.bubblespeechstyles = BubblespeechStyleCache(self.shapestyles, self._callback_set, self._callback_delete)
        self.bubblespeechtextstyles = BubblespeechTextStyleCache(
            self.shapetextstyles, self._callback_set, self._callback_delete
        )

    def _get_style_caches(self) -> List[AbstractStyleCache]:
        """Retrieve all style caches.

        Returns:
            List[AbstractStyleCache]: A list containing all style caches.
        """
        styles: List[AbstractStyleCache] = [
            self.iconstyles,
            self.imagestyles,
            self.linestyles,
            self.shapestyles,
            self.shapetextstyles,
            self.textstyles,
            # patchs
            self.arcstyles,
            self.arctextstyles,
            self.circlestyles,
            self.circletextstyles,
            self.donutsstyles,
            self.donutstextstyles,
            self.ellipsestyles,
            self.ellipsetextstyles,
            self.fanstyles,
            self.fantextstyles,
            self.polygonstyles,
            self.polygontextstyles,
            self.rectanglestyles,
            self.rectangletextstyles,
            self.regularpolygonstyles,
            self.regularpolygontextstyles,
            self.wedgestyles,
            self.wedgetextstyles,
            # original arrows
            self.arrowstyles,
            self.arrowtextstyles,
            # original polygons
            self.chevronstyles,
            self.chevrontextstyles,
            self.parallelogramstyles,
            self.parallelogramtextstyles,
            self.rhombusstyles,
            self.rhombustextstyles,
            self.starstyles,
            self.startextstyles,
            self.trapezoidstyles,
            self.trapezoidtextstyles,
            self.trianglestyles,
            self.triangletextstyles,
            # smart art
            self.bubblespeechstyles,
            self.bubblespeechtextstyles,
        ]
        return styles

    def _get_theme_colors(self) -> str:
        """Retrieve the theme colors formatted as a string.

        Returns:
            str: A string representing the theme colors.
        """
        max_len = 0
        for name in self.colors.list():
            max_len = max(max_len, len(name))

        lines = []
        for name in self.colors.list():
            c = self.colors.get(name)
            c0 = str(c[0]).rjust(3)
            c1 = str(c[1]).rjust(3)
            c2 = str(c[2]).rjust(3)
            color_text = f"({c0}, {c1}, {c2}, {c[3]})"
            lines.append(f"{name.ljust(max_len)}: {color_text}")

        return "\n".join(lines).strip()

    def _get_style_table(self, max_columns: int = 11) -> str:  # noqa: C901
        """Retrieve a table of styles formatted as a string.

        Args:
            max_columns (int): The maximum number of columns in the table. Must be at least 2.

        Returns:
            str: A string representing the style table.

        Raises:
            ValueError: If max_columns is not an integer or is less than 2.
        """
        if not isinstance(max_columns, int):
            raise ValueError("Arg max_columns must be int 2+")
        if max_columns < 2:
            raise ValueError("Arg max_columns must be int 2+")

        col1: List[str] = [
            "class \\ name",
            "IconStyle",
            "ImageStyle",
            "LineStyle",
            "ShapeStyle",
            "ShapeTextStyle",
            "TextStyle",
        ]

        row_objects = [
            self.iconstyles,
            self.imagestyles,
            self.linestyles,
            self.shapestyles,
            self.shapetextstyles,
            self.textstyles,
        ]

        def get_text(style_names: List[str]) -> str:  # noqa: C901
            lines: List[str] = []

            # create columns
            cols: List[List[str]] = [col1]
            for style_name in style_names:
                col: List[str] = [style_name]
                for row_object in row_objects:
                    if row_object.has(style_name):
                        col.append("x")
                    else:
                        col.append("")
                cols.append(col)

            # modify text length
            cols2 = []
            for col in cols:
                max_length = max(len(s) for s in col)
                padded_strings = [s.ljust(max_length) for s in col]
                cols2.append(padded_strings)

            def draw_border() -> None:
                text = "+"
                for col in cols2:
                    t = "-" * (len(col[0]) + 2)
                    text += f"{t}+"
                lines.append(text)

            for i in range(len(col1)):
                if i == 0:
                    draw_border()

                text = "|"
                for col in cols2:
                    text += f" {col[i]} |"
                lines.append(text)

                if i == 0:
                    draw_border()

                if i == len(col1) - 1:
                    draw_border()

            return "\n".join(lines).strip()

        def split_list(input_list: List[str], chunk_size: int) -> List[List[str]]:
            result = []
            for i in range(0, len(input_list), chunk_size):
                chunk = input_list[i : i + chunk_size]
                result.append(chunk)
            return result

        texts = []
        list_of_list = split_list(self._style_names, max_columns - 1)
        for style_names in list_of_list:
            texts.append(get_text(style_names))

        return "\n\n".join(texts).strip()

    def _callback_set(self, name: str) -> None:
        """Callback function which is called from style caches.

        Add a new style name to the self._style_names if not exist yet.

        Args:
            name (str): The name of the style to add.

        Returns:
            None
        """
        if name in self._style_names:
            return

        self._style_names.append(name)

    def _callback_delete(self, name: str) -> None:
        """Callback function which is called from style caches.

        Remove a style name from the self._style_names if not used in any style caches.

        Args:
            name (str): The name of the style to add.

        Returns:
            None
        """
        if name not in self._style_names:
            return

        name_exist = False
        for style in self._get_style_caches():
            if style.has(name):
                name_exist = True
                break

        if not name_exist:
            self._style_names.remove(name)


dtheme = Theme()
"""Represents the theme handler for drawlib.

This object manages drawlib's theme configurations and provides access
to pre-defined styles for various elements. It includes caches for colors, fonts,
styles for shapes, text, icons, images, lines, and various geometric figures.
The theme can be initialized and modified through this object.
"""
