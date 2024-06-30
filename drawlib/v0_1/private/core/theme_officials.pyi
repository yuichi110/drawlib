"""
This type stub file was generated by pyright.
"""

import dataclasses
from typing import List, Literal, Tuple, Union
from drawlib.v0_1.private.core.fonts import FontBase
from drawlib.v0_1.private.core.model import OfficialThemeStyle, ThemeStyles

"""Module for defining official themes."""
def get_default() -> OfficialThemeStyle:
    """Generate the default theme style configuration.

    Returns:
        OfficialThemeStyle: The default theme style configuration.
    """
    ...

def get_essentials() -> OfficialThemeStyle:
    """Generate the essentials theme style configuration.

    Returns:
        OfficialThemeStyle: The default theme style configuration.
    """
    ...

def get_monochrome() -> OfficialThemeStyle:
    """Generate the monochrome theme style configuration.

    Returns:
        OfficialThemeStyle: The default theme style configuration.
    """
    ...

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
        ...
    
    icon_style: Literal["thin", "light", "regular", "bold", "fill"]
    icon_color: Union[Tuple[int, int, int], Tuple[int, int, int, float],]
    image_line_width: float
    line_style: Literal["solid", "dashed", "dotted", "dashdot"]
    line_width: float
    line_color: Union[Tuple[int, int, int], Tuple[int, int, int, float],]
    arrowhead_scale: int
    shape_line_style: Literal["solid", "dashed", "dotted", "dashdot"]
    shape_line_width: float
    shape_line_color: Union[Tuple[int, int, int], Tuple[int, int, int, float],]
    shape_fill_color: Union[Tuple[int, int, int], Tuple[int, int, int, float],]
    shapetext_font: FontBase
    shapetext_size: int
    shapetext_color: Union[Tuple[int, int, int], Tuple[int, int, int, float],]
    text_font: FontBase
    text_size: int
    text_color: Union[Tuple[int, int, int], Tuple[int, int, int, float],]


def get_named_styles(default_template: OfficialThemeTemplate, light_template: OfficialThemeTemplate, bold_template: OfficialThemeTemplate, colors: List[Tuple[str, Tuple[int, int, int]]], default_shapeline_color: Tuple[int, int, int], default_shapefill_color: Tuple[int, int, int]) -> List[Tuple[str, ThemeStyles]]:
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
    ...

