import os


def cd_to_project_root():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    os.chdir("../")


HEAD = '''
# Copyright (c) 2024 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

# pylint: disable=too-many-lines, invalid-name

"""dtheme's cache objects implementations. Auto generated codes."""


from abc import ABC, abstractmethod
from typing import Dict, Tuple, List, Union, Any, Optional, Callable

from drawlib.v0_1.private.util import error_handler
from drawlib.v0_1.private.core.model import (
    IconStyle,
    ImageStyle,
    LineStyle,
    ShapeStyle,
    ShapeTextStyle,
    TextStyle,
)
from drawlib.v0_1.private.core.fonts import FontSourceCode
import drawlib.v0_1.private.validators.color as color_validator
import drawlib.v0_1.private.validators.style as style_validator
import drawlib.v0_1.private.validators.types as type_validator

list_ = list


class ThemeColorCache:
    """Cache for theme colors."""

    def __init__(self) -> None:
        """Initializes an instance of ThemeColorCache."""

        self._colors: Dict[str, Tuple[int, int, int, float]] = {}

    @error_handler
    def has(self, name: str) -> bool:
        """Checks if a theme color exists by name.

        Args:
            name (str): Name of the theme color.

        Returns:
            bool: True if the theme color exists, False otherwise.
        """

        return name in self._colors

    @error_handler
    def get(self, name: str = "") -> Tuple[int, int, int, float]:
        """Retrieves a theme color by name.

        Args:
            name (str, optional): Name of the theme color. Defaults to "".

        Returns:
            Tuple[int, int, int, float]: RGBA components of the theme color.

        Raises:
            ValueError: If the specified theme color name does not exist.
        """

        if not self.has(name):
            raise ValueError('Theme colors name "' + name + '" does not exist.')
        return self._colors[name]

    @error_handler
    def list(self) -> List[str]:
        """Lists all existing theme color names.

        Returns:
            List[str]: List of theme color names.
        """

        return list_(self._colors.keys())

    @error_handler
    def set(
        self,
        color: Union[Tuple[int, int, int], Tuple[int, int, int, float]],
        name: str = "",
    ) -> None:
        """Sets or updates a theme color with the given name.

        Args:
            color (Union[Tuple[int, int, int], Tuple[int, int, int, float]]):
                RGB or RGBA components of the theme color.
            name (str, optional): Name of the theme color. Defaults to "".

        Raises:
            ValueError: If the color format is invalid or if the name format is invalid.
        """

        color_validator.validate_color("color", color)
        type_validator.validate_str("name", name)
        if len(color) == 3:
            color = (color[0], color[1], color[2], 1.0)
        self._colors[name] = color

    @error_handler
    def delete(self, name: str) -> None:
        """Deletes a theme color by name.

        Args:
            name (str): Name of the theme color to delete.

        Raises:
            ValueError: If the specified theme color name does not exist.
        """

        if not self.has(name):
            raise ValueError('Theme colors name "' + name + '" does not exist.')
        del self._colors[name]


class BackgroundColorCache:
    """Cache for background colors used in themes."""

    def __init__(self) -> None:
        """Initializes an instance of BackgroundColorCache."""

        self._colors: Dict[str, Tuple[int, int, int, float]] = {}

    @error_handler
    def has(self, name: str) -> bool:
        """Checks if a background color exists by name.

        Args:
            name (str): Name of the background color.

        Returns:
            bool: True if the background color exists, False otherwise.
        """

        return name in self._colors

    @error_handler
    def get(self, name: str = "") -> Tuple[int, int, int, float]:
        """Retrieves a background color by name.

        Args:
            name (str, optional): Name of the background color. Defaults to "".

        Returns:
            Tuple[int, int, int, float]: RGBA components of the background color.

        Raises:
            ValueError: If the specified background color name does not exist.
        """

        if not self.has(name):
            raise ValueError('Theme background-color name "' + name + '" does not exist.')
        return self._colors[name]

    @error_handler
    def list(self) -> List[str]:
        """Lists all existing background color names.

        Returns:
            List[str]: List of background color names.
        """

        return list_(self._colors.keys())

    @error_handler
    def set(
        self,
        color: Union[Tuple[int, int, int], Tuple[int, int, int, float]],
        name: str = "",
    ) -> None:
        """Sets or updates a background color with the given name.

        Args:
            color (Union[Tuple[int, int, int], Tuple[int, int, int, float]]):
                RGB or RGBA components of the background color.
            name (str, optional): Name of the background color. Defaults to "".

        Raises:
            ValueError: If the color format is invalid or if the name format is invalid.
        """

        color_validator.validate_color("color", color)
        type_validator.validate_str("name", name)
        if len(color) == 3:
            color = (color[0], color[1], color[2], 1.0)
        self._colors[name] = color

    @error_handler
    def delete(self, name: str) -> None:
        """Deletes a background color by name.

        Args:
            name (str): Name of the background color to delete.

        Raises:
            ValueError: If the specified background color name does not exist.
        """

        if not self.has(name):
            raise ValueError('Theme background-color name "' + name + '" does not exist.')
        del self._colors[name]


class SourceCodeFontCache:
    """Cache for source code fonts used in themes."""

    def __init__(self) -> None:
        """Initializes an instance of SourceCodeFontCache."""

        self._fonts: Dict[str, FontSourceCode] = {}

    @error_handler
    def has(self, name: str) -> bool:
        """Checks if a source code font exists by name.

        Args:
            name (str): Name of the source code font.

        Returns:
            bool: True if the source code font exists, False otherwise.
        """

        return name in self._fonts

    @error_handler
    def get(self, name: str = "") -> FontSourceCode:
        """Retrieves a source code font by name.

        Args:
            name (str, optional): Name of the source code font. Defaults to "".

        Returns:
            FontSourceCode: Source code font object.

        Raises:
            ValueError: If the specified source code font name does not exist.
        """

        if not self.has(name):
            raise ValueError('Theme sourcecode-font name "' + name + '" does not exist.')
        return self._fonts[name]

    @error_handler
    def list(self) -> List[str]:
        """Lists all existing source code font names.

        Returns:
            List[str]: List of source code font names.
        """

        return list_(self._fonts.keys())

    @error_handler
    def set(
        self,
        font: FontSourceCode,
        name: str = "",
    ) -> None:
        """Sets or updates a source code font with the given name.

        Args:
            font (FontSourceCode): Source code font object.
            name (str, optional): Name of the source code font. Defaults to "".

        Raises:
            ValueError: If the font is not an instance of FontSourceCode or if the name format is invalid.
        """

        if not isinstance(font, FontSourceCode):
            raise ValueError("Arg font must be FontSourceCode.")
        type_validator.validate_str("name", name)

        self._fonts[name] = font

    @error_handler
    def delete(self, name: str) -> None:
        """Deletes a source code font by name.

        Args:
            name (str): Name of the source code font to delete.

        Raises:
            ValueError: If the specified source code font name does not exist.
        """

        if not self.has(name):
            raise ValueError('Theme sourcecode-font name "' + name + '" does not exist.')
        del self._fonts[name]


class AbstractStyleCache(ABC):
    """Abstract base class for caching styles.

    This class defines the interface for caching styles and must be subclassed to implement
    specific caching functionality.
    """

    @abstractmethod
    def has(self, name: str) -> bool:
        """Checks if a style exists by name.

        Args:
            name (str): Name of the style.

        Returns:
            bool: True if the style exists, False otherwise.
        """

    @abstractmethod
    def get(self, name: str = "") -> Any:
        """Retrieves a style by name.

        Args:
            name (str, optional): Name of the style. Defaults to "".

        Returns:
            Any: The retrieved style object.

        Raises:
            NotImplementedError: If the method is not implemented in a subclass.
        """

    @abstractmethod
    def list(self) -> List[str]:
        """Lists all existing style names.

        Returns:
            List[str]: List of style names.
        """

    @abstractmethod
    def set(self, style: Any, name: str = "") -> None:
        """Sets or updates a style with the given name.

        Args:
            style (Any): The style object to cache.
            name (str, optional): Name of the style. Defaults to "".

        Raises:
            NotImplementedError: If the method is not implemented in a subclass.
        """

    @abstractmethod
    def delete(self, name: str) -> None:
        """Deletes a style by name.

        Args:
            name (str): Name of the style to delete.

        Raises:
            NotImplementedError: If the method is not implemented in a subclass.

        """

    @abstractmethod
    def merge(self, style: Any, targets: Optional[List[str]] = None) -> None:
        """Merges a style into existing styles.

        Args:
            style (Any): The style object to merge.
            targets (Optional[List[str]], optional): List of target style names to merge into.
                If None, merge into all existing styles. Defaults to None.

        Raises:
            NotImplementedError: If the method is not implemented in a subclass.
        """
'''

TEMPLATE = '''
class {class_name}(AbstractStyleCache):
    """Cache for managing {style_class} styles.

    This class provides methods to manage and manipulate {style_class} objects
    within a cache, implementing the AbstractStyleCache interface.
    """

    def __init__(
        self,
        callback_set:Callable[[str,], None],
        callback_delete:Callable[[str,], None],
    ) -> None:
        """Initialize {class_name} with callbacks for set and delete operations.

        Args:
            callback_set: Callback function for set operation.
            callback_delete: Callback function for delete operation.
        """

        self._callback_set = callback_set
        self._callback_delete = callback_delete
        self._styles: Dict[str, {style_class}] = {{}}

    @error_handler
    def has(self, name: str) -> bool:
        """Check if a style exists by name.

        Args:
            name (str): Name of the style.

        Returns:
            bool: True if the style exists, False otherwise.
        """

        return name in self._styles

    @error_handler
    def get(self, name: str = "") -> {style_class}:
        """Retrieve a style by name.

        Args:
            name (str, optional): Name of the style to retrieve. Defaults to "".

        Returns:
            {style_class}: The retrieved IconStyle object.

        Raises:
            ValueError: If the style with the specified name does not exist.
        """

        if not self.has(name):
            raise ValueError('Theme style name "' + name + '" does not exist.')
        return self._styles[name].copy()

    @error_handler
    def list(self) -> List[str]:
        """List all existing style names.

        Returns:
            List[str]: List of style names.
        """

        return list_(self._styles.keys())

    @error_handler
    def set(self, style: {style_class}, name: str = "") -> None:
        """Set or update a style with the given name.

        Args:
            style ({style_class}): The {style_class} object to cache.
            name (str, optional): Name of the style. Defaults to "".

        Raises:
            ValueError: If the style is invalid or name is not a string.
        """

        style_validator.validate_{validate_class_name}("style", style)
        type_validator.validate_str("name", name)
        self._styles[name] = style.copy()
        self._callback_set(name)

    @error_handler
    def delete(self, name: str) -> None:
        """Delete a style by name.

        Args:
            name (str): Name of the style to delete.

        Raises:
            ValueError: If the style with the specified name does not exist.
        """

        if not self.has(name):
            raise ValueError('Theme style name "' + name + '" does not exist.')
        del self._styles[name]
        self._callback_delete(name)

    @error_handler
    def merge(self, style: {style_class}, targets: Optional[List[str]] = None) -> None:
        """Merge a style into existing styles.

        Args:
            style ({style_class}): The {style_class} object to merge.
            targets (Optional[List[str]], optional): List of target style names to merge into.
                If None, merge into all existing styles. Defaults to None.

        Raises:
            ValueError: If the style is invalid or merging fails.
        """

        style_validator.validate_{validate_class_name}("style", style)
        if targets is None:
            targets = self.list()
        for target in targets:
            if not self.has(target):
                continue
            merged_style = self.get(target).merge(style)
            self.set(merged_style, target)
'''

TEMPLATE_SHAPE_TYPES = '''
class {class_name}(AbstractStyleCache):
    """Cache for managing {name} styles.

    This class provides methods to manage and manipulate ShapeStyle objects
    specifically tailored for {name} within a cache.
    """

    def __init__(
        self,
        shapestyles: ShapeStyleCache,
        callback_set:Callable[[str,], None],
        callback_delete:Callable[[str,], None],
    ) -> None:
        """Initialize {class_name}.

        Args:
            shapestyles (ShapeStyleCache): Cache of shape styles to use as fallback.
            callback_set: Callback function for set operation.
            callback_delete: Callback function for delete operation.
        """

        self._callback_set = callback_set
        self._callback_delete = callback_delete
        self._styles: Dict[str, ShapeStyle] = {{}}
        self._shapestyles = shapestyles

    @error_handler
    def has(self, name: str) -> bool:
        """Check if an {name} style exists by name.

        Args:
            name (str): Name of the {name} style.

        Returns:
            bool: True if the {name} style exists, False otherwise.
        """

        return name in self._styles

    @error_handler
    def get(self, name: str = "", use_shapestyles_if_not_exist: bool = True) -> ShapeStyle:
        """Retrieve an {name} style by name.

        Args:
            name (str, optional): Name of the {name} style to retrieve. Defaults to "".
            use_shapestyles_if_not_exist (bool, optional): Whether to fallback to ShapeStyleCache if
                the style does not exist in _styles. Defaults to True.

        Returns:
            ShapeStyle: The retrieved ShapeStyle object.

        Raises:
            ValueError: If the {name} style with the specified name does not exist and
                use_shapestyles_if_not_exist is False.
        """

        if self.has(name):
            style = self._styles[name].copy()
        elif use_shapestyles_if_not_exist:
            style = self._shapestyles.get(name)
        else:
            raise ValueError('Theme style name "' + name + '" does not exist.')
        return style

    @error_handler
    def list(self) -> List[str]:
        """List all existing {name} style names.

        Returns:
            List[str]: List of {name} style names.
        """

        return list_(self._styles.keys())

    @error_handler
    def set(self, style: ShapeStyle, name: str = "") -> None:
        """Set or update an {name} style with the given name.

        Args:
            style (ShapeStyle): The ShapeStyle object to cache.
            name (str, optional): Name of the {name} style. Defaults to "".

        Raises:
            ValueError: If the style is invalid or name is not a string.
        """

        style_validator.validate_shapestyle("style", style)
        type_validator.validate_str("name", name)
        self._styles[name] = style.copy()
        self._callback_set(name)

    @error_handler
    def delete(self, name: str) -> None:
        """Delete an {name} style by name.

        Args:
            name (str): Name of the {name} style to delete.

        Raises:
            ValueError: If the {name} style with the specified name does not exist.
        """

        if not self.has(name):
            raise ValueError('Theme style name "' + name + '" does not exist.')
        del self._styles[name]
        self._callback_delete(name)

    @error_handler
    def merge(self, style: ShapeStyle, targets: Optional[List[str]] = None) -> None:
        """Merge an {name} style into existing {name} styles.

        Args:
            style (ShapeStyle): The ShapeStyle object to merge.
            targets (Optional[List[str]], optional): List of target {name} style names to merge into.
                If None, merge into all existing {name} styles. Defaults to None.

        Raises:
            ValueError: If the style is invalid or merging fails.
        """

        style_validator.validate_shapestyle("style", style)
        if targets is None:
            targets = self.list()
        for target in targets:
            if not self.has(target):
                continue
            merged_style = self.get(target).merge(style)
            self.set(merged_style, target)
'''

TEMPLATE_SHAPETEXT_TYPES = '''
class {class_name}(AbstractStyleCache):
    """Cache for managing {name} text styles.

    This class provides methods to manage and manipulate ShapeTextStyle objects
    specifically tailored for {name} within a cache.
    """

    def __init__(
        self, 
        shapetextstyles: ShapeTextStyleCache,
        callback_set:Callable[[str,], None],
        callback_delete:Callable[[str,], None],
    ) -> None:
        """Initialize {class_name}.

        Args:
            shapetextstyles (ShapeTextStyleCache): Cache of shape text styles to use as fallback.
            callback_set: Callback function for set operation.
            callback_delete: Callback function for delete operation.
        """

        self._callback_set = callback_set
        self._callback_delete = callback_delete
        self._styles: Dict[str, ShapeTextStyle] = {{}}
        self._shapetextstyles = shapetextstyles

    @error_handler
    def has(self, name: str) -> bool:
        """Check if an {name} text style exists by name.

        Args:
            name (str): Name of the {name} text style.

        Returns:
            bool: True if the {name} text style exists, False otherwise.
        """

        return name in self._styles

    @error_handler
    def get(self, name: str = "", use_shapetextstyles_if_not_exist: bool = True) -> ShapeTextStyle:
        """Retrieve an {name} text style by name.

        Args:
            name (str, optional): Name of the {name} text style to retrieve. Defaults to "".
            use_shapetextstyles_if_not_exist (bool, optional): Whether to fallback to ShapeTextStyleCache if
                the style does not exist in _styles. Defaults to True.

        Returns:
            ShapeTextStyle: The retrieved ShapeTextStyle object.

        Raises:
            ValueError: If the {name} text style with the specified name does not exist and
                use_shapetextstyles_if_not_exist is False.
        """

        if self.has(name):
            return self._styles[name].copy()
        if not use_shapetextstyles_if_not_exist:
            raise ValueError('Theme style name "' + name + '" does not exist.')
        return self._shapetextstyles.get(name)

    @error_handler
    def list(self) -> List[str]:
        """List all existing {name} text style names.

        Returns:
            List[str]: List of {name} text style names.
        """

        return list_(self._styles.keys())

    @error_handler
    def set(self, style: ShapeTextStyle, name: str = "") -> None:
        """Set or update an {name} text style with the given name.

        Args:
            style (ShapeTextStyle): The ShapeTextStyle object to cache.
            name (str, optional): Name of the {name} text style. Defaults to "".

        Raises:
            ValueError: If the style is invalid or name is not a string.
        """

        style_validator.validate_shapetextstyle("style", style)
        type_validator.validate_str("name", name)
        self._styles[name] = style.copy()
        self._callback_set(name)

    @error_handler
    def delete(self, name: str) -> None:
        """Delete an {name} text style by name.

        Args:
            name (str): Name of the {name} text style to delete.

        Raises:
            ValueError: If the {name} text style with the specified name does not exist.
        """

        if not self.has(name):
            raise ValueError('Theme style name "' + name + '" does not exist.')
        del self._styles[name]
        self._callback_delete(name)

    @error_handler
    def merge(self, style: ShapeTextStyle, targets: Optional[List[str]] = None) -> None:
        """Merge an {name} text style into existing {name} text styles.

        Args:
            style (ShapeTextStyle): The ShapeTextStyle object to merge.
            targets (Optional[List[str]], optional): List of target {name} text style names to merge into.
                If None, merge into all existing {name} text styles. Defaults to None.

        Raises:
            ValueError: If the style is invalid or merging fails.
        """

        style_validator.validate_shapetextstyle("style", style)
        if targets is None:
            targets = self.list()
        for target in targets:
            if not self.has(target):
                continue
            merged_style = self.get(target).merge(style)
            self.set(merged_style, target)
'''


def get_text_basics():
    texts = []
    for class_name, style_class in [
        ("IconStyleCache", "IconStyle"),
        ("ImageStyleCache", "ImageStyle"),
        ("LineStyleCache", "LineStyle"),
        ("ShapeStyleCache", "ShapeStyle"),
        ("ShapeTextStyleCache", "ShapeTextStyle"),
        ("TextStyleCache", "TextStyle"),
    ]:
        text = TEMPLATE.format(
            class_name=class_name,
            style_class=style_class,
            validate_class_name=style_class.lower(),
        )
        texts.append(text.strip())
    return "\n\n\n".join(texts)


def get_text_shape_types():
    texts = []
    for class_name, name in [
        # patchs
        ("ArcStyleCache", "arc"),
        ("CircleStyleCache", "circle"),
        ("DonutsStyleCache", "donuts"),
        ("EllipseStyleCache", "ellipse"),
        ("FanStyleCache", "fan"),
        ("PolygonStyleCache", "polygon"),
        ("RectangleStyleCache", "rectangle"),
        ("RegularpolygonStyleCache", "regular polygon"),
        ("WedgeStyleCache", "wedge"),
        # original arrows
        ("ArrowStyleCache", "arrow"),
        # original polygons
        ("ChevronStyleCache", "chevron"),
        ("ParallelogramStyleCache", "parallelogram"),
        ("RhombusStyleCache", "rhombus"),
        ("StarStyleCache", "star"),
        ("TrapezoidStyleCache", "trapezoid"),
        ("TriangleStyleCache", "triangle"),
        # smart art
        ("BubblespeechStyleCache", "bubble speech"),
    ]:
        text = TEMPLATE_SHAPE_TYPES.format(
            class_name=class_name,
            name=name,
        )
        texts.append(text.strip())
    return "\n\n\n".join(texts)


def get_text_shapetext_types():
    texts = []
    for class_name, name in [
        # patchs
        ("ArcTextStyleCache", "arc"),
        ("CircleTextStyleCache", "circle"),
        ("DonutsTextStyleCache", "donuts"),
        ("EllipseTextStyleCache", "ellipse"),
        ("FanTextStyleCache", "fan"),
        ("PolygonTextStyleCache", "polygon"),
        ("RectangleTextStyleCache", "rectangle"),
        ("RegularpolygonTextStyleCache", "regular polygon"),
        ("WedgeTextStyleCache", "wedge"),
        # original arrows
        ("ArrowTextStyleCache", "arrow"),
        # original polygons
        ("ChevronTextStyleCache", "chevron"),
        ("ParallelogramTextStyleCache", "parallelogram"),
        ("RhombusTextStyleCache", "rhombus"),
        ("StarTextStyleCache", "star"),
        ("TrapezoidTextStyleCache", "trapezoid"),
        ("TriangleTextStyleCache", "triangle"),
        # smart art
        ("BubblespeechTextStyleCache", "bubble speech"),
    ]:
        text = TEMPLATE_SHAPETEXT_TYPES.format(
            class_name=class_name,
            name=name,
        )
        texts.append(text.strip())
    return "\n\n\n".join(texts)


def write():
    texts = []
    texts.append(HEAD.strip())
    texts.append(get_text_basics().strip())
    texts.append(get_text_shape_types().strip())
    texts.append(get_text_shapetext_types().strip())
    text = "\n\n\n".join(texts)

    # write to file
    os.makedirs("output_codes", exist_ok=True)
    with open("output_codes/theme_style_caches.py", "w") as fout:
        fout.write(text)
        fout.write("\n")  # last new line


if __name__ == "__main__":
    cd_to_project_root()
    write()
