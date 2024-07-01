# Copyright (c) 2024 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""dtheme's cache objects implementations. Auto generated codes."""

from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

import drawlib.v0_2.private.validators.color as color_validator
import drawlib.v0_2.private.validators.style as style_validator
import drawlib.v0_2.private.validators.types as type_validator
from drawlib.v0_2.private.core.fonts import FontSourceCode
from drawlib.v0_2.private.core.model import (
    IconStyle,
    ImageStyle,
    LineStyle,
    ShapeStyle,
    ShapeTextStyle,
    TextStyle,
)
from drawlib.v0_2.private.util import error_handler

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
    def get(self, name: str = "") -> Any:  # noqa: ANN401
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
    def set(self, style: Any, name: str = "") -> None:  # noqa: ANN401
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
    def merge(self, style: Any, targets: Optional[List[str]] = None) -> None:  # noqa: ANN401
        """Merges a style into existing styles.

        Args:
            style (Any): The style object to merge.
            targets (Optional[List[str]], optional): List of target style names to merge into.
                If None, merge into all existing styles. Defaults to None.

        Raises:
            NotImplementedError: If the method is not implemented in a subclass.
        """


class IconStyleCache(AbstractStyleCache):
    """Cache for managing IconStyle styles.

    This class provides methods to manage and manipulate IconStyle objects
    within a cache, implementing the AbstractStyleCache interface.
    """

    def __init__(
        self,
        callback_set: Callable[
            [
                str,
            ],
            None,
        ],
        callback_delete: Callable[
            [
                str,
            ],
            None,
        ],
    ) -> None:
        """Initialize IconStyleCache with callbacks for set and delete operations.

        Args:
            callback_set: Callback function for set operation.
            callback_delete: Callback function for delete operation.
        """
        self._callback_set = callback_set
        self._callback_delete = callback_delete
        self._styles: Dict[str, IconStyle] = {}

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
    def get(self, name: str = "") -> IconStyle:
        """Retrieve a style by name.

        Args:
            name (str, optional): Name of the style to retrieve. Defaults to "".

        Returns:
            IconStyle: The retrieved IconStyle object.

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
    def set(self, style: IconStyle, name: str = "") -> None:
        """Set or update a style with the given name.

        Args:
            style (IconStyle): The IconStyle object to cache.
            name (str, optional): Name of the style. Defaults to "".

        Raises:
            ValueError: If the style is invalid or name is not a string.
        """
        style_validator.validate_iconstyle("style", style)
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
    def merge(self, style: IconStyle, targets: Optional[List[str]] = None) -> None:
        """Merge a style into existing styles.

        Args:
            style (IconStyle): The IconStyle object to merge.
            targets (Optional[List[str]], optional): List of target style names to merge into.
                If None, merge into all existing styles. Defaults to None.

        Raises:
            ValueError: If the style is invalid or merging fails.
        """
        style_validator.validate_iconstyle("style", style)
        if targets is None:
            targets = self.list()
        for target in targets:
            if not self.has(target):
                continue
            merged_style = self.get(target).merge(style)
            self.set(merged_style, target)


class ImageStyleCache(AbstractStyleCache):
    """Cache for managing ImageStyle styles.

    This class provides methods to manage and manipulate ImageStyle objects
    within a cache, implementing the AbstractStyleCache interface.
    """

    def __init__(
        self,
        callback_set: Callable[
            [
                str,
            ],
            None,
        ],
        callback_delete: Callable[
            [
                str,
            ],
            None,
        ],
    ) -> None:
        """Initialize ImageStyleCache with callbacks for set and delete operations.

        Args:
            callback_set: Callback function for set operation.
            callback_delete: Callback function for delete operation.
        """
        self._callback_set = callback_set
        self._callback_delete = callback_delete
        self._styles: Dict[str, ImageStyle] = {}

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
    def get(self, name: str = "") -> ImageStyle:
        """Retrieve a style by name.

        Args:
            name (str, optional): Name of the style to retrieve. Defaults to "".

        Returns:
            ImageStyle: The retrieved IconStyle object.

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
    def set(self, style: ImageStyle, name: str = "") -> None:
        """Set or update a style with the given name.

        Args:
            style (ImageStyle): The ImageStyle object to cache.
            name (str, optional): Name of the style. Defaults to "".

        Raises:
            ValueError: If the style is invalid or name is not a string.
        """
        style_validator.validate_imagestyle("style", style)
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
    def merge(self, style: ImageStyle, targets: Optional[List[str]] = None) -> None:
        """Merge a style into existing styles.

        Args:
            style (ImageStyle): The ImageStyle object to merge.
            targets (Optional[List[str]], optional): List of target style names to merge into.
                If None, merge into all existing styles. Defaults to None.

        Raises:
            ValueError: If the style is invalid or merging fails.
        """
        style_validator.validate_imagestyle("style", style)
        if targets is None:
            targets = self.list()
        for target in targets:
            if not self.has(target):
                continue
            merged_style = self.get(target).merge(style)
            self.set(merged_style, target)


class LineStyleCache(AbstractStyleCache):
    """Cache for managing LineStyle styles.

    This class provides methods to manage and manipulate LineStyle objects
    within a cache, implementing the AbstractStyleCache interface.
    """

    def __init__(
        self,
        callback_set: Callable[
            [
                str,
            ],
            None,
        ],
        callback_delete: Callable[
            [
                str,
            ],
            None,
        ],
    ) -> None:
        """Initialize LineStyleCache with callbacks for set and delete operations.

        Args:
            callback_set: Callback function for set operation.
            callback_delete: Callback function for delete operation.
        """
        self._callback_set = callback_set
        self._callback_delete = callback_delete
        self._styles: Dict[str, LineStyle] = {}

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
    def get(self, name: str = "") -> LineStyle:
        """Retrieve a style by name.

        Args:
            name (str, optional): Name of the style to retrieve. Defaults to "".

        Returns:
            LineStyle: The retrieved IconStyle object.

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
    def set(self, style: LineStyle, name: str = "") -> None:
        """Set or update a style with the given name.

        Args:
            style (LineStyle): The LineStyle object to cache.
            name (str, optional): Name of the style. Defaults to "".

        Raises:
            ValueError: If the style is invalid or name is not a string.
        """
        style_validator.validate_linestyle("style", style)
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
    def merge(self, style: LineStyle, targets: Optional[List[str]] = None) -> None:
        """Merge a style into existing styles.

        Args:
            style (LineStyle): The LineStyle object to merge.
            targets (Optional[List[str]], optional): List of target style names to merge into.
                If None, merge into all existing styles. Defaults to None.

        Raises:
            ValueError: If the style is invalid or merging fails.
        """
        style_validator.validate_linestyle("style", style)
        if targets is None:
            targets = self.list()
        for target in targets:
            if not self.has(target):
                continue
            merged_style = self.get(target).merge(style)
            self.set(merged_style, target)


class ShapeStyleCache(AbstractStyleCache):
    """Cache for managing ShapeStyle styles.

    This class provides methods to manage and manipulate ShapeStyle objects
    within a cache, implementing the AbstractStyleCache interface.
    """

    def __init__(
        self,
        callback_set: Callable[
            [
                str,
            ],
            None,
        ],
        callback_delete: Callable[
            [
                str,
            ],
            None,
        ],
    ) -> None:
        """Initialize ShapeStyleCache with callbacks for set and delete operations.

        Args:
            callback_set: Callback function for set operation.
            callback_delete: Callback function for delete operation.
        """
        self._callback_set = callback_set
        self._callback_delete = callback_delete
        self._styles: Dict[str, ShapeStyle] = {}

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
    def get(self, name: str = "") -> ShapeStyle:
        """Retrieve a style by name.

        Args:
            name (str, optional): Name of the style to retrieve. Defaults to "".

        Returns:
            ShapeStyle: The retrieved IconStyle object.

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
    def set(self, style: ShapeStyle, name: str = "") -> None:
        """Set or update a style with the given name.

        Args:
            style (ShapeStyle): The ShapeStyle object to cache.
            name (str, optional): Name of the style. Defaults to "".

        Raises:
            ValueError: If the style is invalid or name is not a string.
        """
        style_validator.validate_shapestyle("style", style)
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
    def merge(self, style: ShapeStyle, targets: Optional[List[str]] = None) -> None:
        """Merge a style into existing styles.

        Args:
            style (ShapeStyle): The ShapeStyle object to merge.
            targets (Optional[List[str]], optional): List of target style names to merge into.
                If None, merge into all existing styles. Defaults to None.

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


class ShapeTextStyleCache(AbstractStyleCache):
    """Cache for managing ShapeTextStyle styles.

    This class provides methods to manage and manipulate ShapeTextStyle objects
    within a cache, implementing the AbstractStyleCache interface.
    """

    def __init__(
        self,
        callback_set: Callable[
            [
                str,
            ],
            None,
        ],
        callback_delete: Callable[
            [
                str,
            ],
            None,
        ],
    ) -> None:
        """Initialize ShapeTextStyleCache with callbacks for set and delete operations.

        Args:
            callback_set: Callback function for set operation.
            callback_delete: Callback function for delete operation.
        """
        self._callback_set = callback_set
        self._callback_delete = callback_delete
        self._styles: Dict[str, ShapeTextStyle] = {}

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
    def get(self, name: str = "") -> ShapeTextStyle:
        """Retrieve a style by name.

        Args:
            name (str, optional): Name of the style to retrieve. Defaults to "".

        Returns:
            ShapeTextStyle: The retrieved IconStyle object.

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
    def set(self, style: ShapeTextStyle, name: str = "") -> None:
        """Set or update a style with the given name.

        Args:
            style (ShapeTextStyle): The ShapeTextStyle object to cache.
            name (str, optional): Name of the style. Defaults to "".

        Raises:
            ValueError: If the style is invalid or name is not a string.
        """
        style_validator.validate_shapetextstyle("style", style)
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
    def merge(self, style: ShapeTextStyle, targets: Optional[List[str]] = None) -> None:
        """Merge a style into existing styles.

        Args:
            style (ShapeTextStyle): The ShapeTextStyle object to merge.
            targets (Optional[List[str]], optional): List of target style names to merge into.
                If None, merge into all existing styles. Defaults to None.

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


class TextStyleCache(AbstractStyleCache):
    """Cache for managing TextStyle styles.

    This class provides methods to manage and manipulate TextStyle objects
    within a cache, implementing the AbstractStyleCache interface.
    """

    def __init__(
        self,
        callback_set: Callable[
            [
                str,
            ],
            None,
        ],
        callback_delete: Callable[
            [
                str,
            ],
            None,
        ],
    ) -> None:
        """Initialize TextStyleCache with callbacks for set and delete operations.

        Args:
            callback_set: Callback function for set operation.
            callback_delete: Callback function for delete operation.
        """
        self._callback_set = callback_set
        self._callback_delete = callback_delete
        self._styles: Dict[str, TextStyle] = {}

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
    def get(self, name: str = "") -> TextStyle:
        """Retrieve a style by name.

        Args:
            name (str, optional): Name of the style to retrieve. Defaults to "".

        Returns:
            TextStyle: The retrieved IconStyle object.

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
    def set(self, style: TextStyle, name: str = "") -> None:
        """Set or update a style with the given name.

        Args:
            style (TextStyle): The TextStyle object to cache.
            name (str, optional): Name of the style. Defaults to "".

        Raises:
            ValueError: If the style is invalid or name is not a string.
        """
        style_validator.validate_textstyle("style", style)
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
    def merge(self, style: TextStyle, targets: Optional[List[str]] = None) -> None:
        """Merge a style into existing styles.

        Args:
            style (TextStyle): The TextStyle object to merge.
            targets (Optional[List[str]], optional): List of target style names to merge into.
                If None, merge into all existing styles. Defaults to None.

        Raises:
            ValueError: If the style is invalid or merging fails.
        """
        style_validator.validate_textstyle("style", style)
        if targets is None:
            targets = self.list()
        for target in targets:
            if not self.has(target):
                continue
            merged_style = self.get(target).merge(style)
            self.set(merged_style, target)


class ArcStyleCache(AbstractStyleCache):
    """Cache for managing arc styles.

    This class provides methods to manage and manipulate ShapeStyle objects
    specifically tailored for arc within a cache.
    """

    def __init__(
        self,
        shapestyles: ShapeStyleCache,
        callback_set: Callable[
            [
                str,
            ],
            None,
        ],
        callback_delete: Callable[
            [
                str,
            ],
            None,
        ],
    ) -> None:
        """Initialize ArcStyleCache.

        Args:
            shapestyles (ShapeStyleCache): Cache of shape styles to use as fallback.
            callback_set: Callback function for set operation.
            callback_delete: Callback function for delete operation.
        """
        self._callback_set = callback_set
        self._callback_delete = callback_delete
        self._styles: Dict[str, ShapeStyle] = {}
        self._shapestyles = shapestyles

    @error_handler
    def has(self, name: str) -> bool:
        """Check if an arc style exists by name.

        Args:
            name (str): Name of the arc style.

        Returns:
            bool: True if the arc style exists, False otherwise.
        """
        return name in self._styles

    @error_handler
    def get(self, name: str = "", use_shapestyles_if_not_exist: bool = True) -> ShapeStyle:
        """Retrieve an arc style by name.

        Args:
            name (str, optional): Name of the arc style to retrieve. Defaults to "".
            use_shapestyles_if_not_exist (bool, optional): Whether to fallback to ShapeStyleCache if
                the style does not exist in _styles. Defaults to True.

        Returns:
            ShapeStyle: The retrieved ShapeStyle object.

        Raises:
            ValueError: If the arc style with the specified name does not exist and
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
        """List all existing arc style names.

        Returns:
            List[str]: List of arc style names.
        """
        return list_(self._styles.keys())

    @error_handler
    def set(self, style: ShapeStyle, name: str = "") -> None:
        """Set or update an arc style with the given name.

        Args:
            style (ShapeStyle): The ShapeStyle object to cache.
            name (str, optional): Name of the arc style. Defaults to "".

        Raises:
            ValueError: If the style is invalid or name is not a string.
        """
        style_validator.validate_shapestyle("style", style)
        type_validator.validate_str("name", name)
        self._styles[name] = style.copy()
        self._callback_set(name)

    @error_handler
    def delete(self, name: str) -> None:
        """Delete an arc style by name.

        Args:
            name (str): Name of the arc style to delete.

        Raises:
            ValueError: If the arc style with the specified name does not exist.
        """
        if not self.has(name):
            raise ValueError('Theme style name "' + name + '" does not exist.')
        del self._styles[name]
        self._callback_delete(name)

    @error_handler
    def merge(self, style: ShapeStyle, targets: Optional[List[str]] = None) -> None:
        """Merge an arc style into existing arc styles.

        Args:
            style (ShapeStyle): The ShapeStyle object to merge.
            targets (Optional[List[str]], optional): List of target arc style names to merge into.
                If None, merge into all existing arc styles. Defaults to None.

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


class CircleStyleCache(AbstractStyleCache):
    """Cache for managing circle styles.

    This class provides methods to manage and manipulate ShapeStyle objects
    specifically tailored for circle within a cache.
    """

    def __init__(
        self,
        shapestyles: ShapeStyleCache,
        callback_set: Callable[
            [
                str,
            ],
            None,
        ],
        callback_delete: Callable[
            [
                str,
            ],
            None,
        ],
    ) -> None:
        """Initialize CircleStyleCache.

        Args:
            shapestyles (ShapeStyleCache): Cache of shape styles to use as fallback.
            callback_set: Callback function for set operation.
            callback_delete: Callback function for delete operation.
        """
        self._callback_set = callback_set
        self._callback_delete = callback_delete
        self._styles: Dict[str, ShapeStyle] = {}
        self._shapestyles = shapestyles

    @error_handler
    def has(self, name: str) -> bool:
        """Check if an circle style exists by name.

        Args:
            name (str): Name of the circle style.

        Returns:
            bool: True if the circle style exists, False otherwise.
        """
        return name in self._styles

    @error_handler
    def get(self, name: str = "", use_shapestyles_if_not_exist: bool = True) -> ShapeStyle:
        """Retrieve an circle style by name.

        Args:
            name (str, optional): Name of the circle style to retrieve. Defaults to "".
            use_shapestyles_if_not_exist (bool, optional): Whether to fallback to ShapeStyleCache if
                the style does not exist in _styles. Defaults to True.

        Returns:
            ShapeStyle: The retrieved ShapeStyle object.

        Raises:
            ValueError: If the circle style with the specified name does not exist and
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
        """List all existing circle style names.

        Returns:
            List[str]: List of circle style names.
        """
        return list_(self._styles.keys())

    @error_handler
    def set(self, style: ShapeStyle, name: str = "") -> None:
        """Set or update an circle style with the given name.

        Args:
            style (ShapeStyle): The ShapeStyle object to cache.
            name (str, optional): Name of the circle style. Defaults to "".

        Raises:
            ValueError: If the style is invalid or name is not a string.
        """
        style_validator.validate_shapestyle("style", style)
        type_validator.validate_str("name", name)
        self._styles[name] = style.copy()
        self._callback_set(name)

    @error_handler
    def delete(self, name: str) -> None:
        """Delete an circle style by name.

        Args:
            name (str): Name of the circle style to delete.

        Raises:
            ValueError: If the circle style with the specified name does not exist.
        """
        if not self.has(name):
            raise ValueError('Theme style name "' + name + '" does not exist.')
        del self._styles[name]
        self._callback_delete(name)

    @error_handler
    def merge(self, style: ShapeStyle, targets: Optional[List[str]] = None) -> None:
        """Merge an circle style into existing circle styles.

        Args:
            style (ShapeStyle): The ShapeStyle object to merge.
            targets (Optional[List[str]], optional): List of target circle style names to merge into.
                If None, merge into all existing circle styles. Defaults to None.

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


class DonutsStyleCache(AbstractStyleCache):
    """Cache for managing donuts styles.

    This class provides methods to manage and manipulate ShapeStyle objects
    specifically tailored for donuts within a cache.
    """

    def __init__(
        self,
        shapestyles: ShapeStyleCache,
        callback_set: Callable[
            [
                str,
            ],
            None,
        ],
        callback_delete: Callable[
            [
                str,
            ],
            None,
        ],
    ) -> None:
        """Initialize DonutsStyleCache.

        Args:
            shapestyles (ShapeStyleCache): Cache of shape styles to use as fallback.
            callback_set: Callback function for set operation.
            callback_delete: Callback function for delete operation.
        """
        self._callback_set = callback_set
        self._callback_delete = callback_delete
        self._styles: Dict[str, ShapeStyle] = {}
        self._shapestyles = shapestyles

    @error_handler
    def has(self, name: str) -> bool:
        """Check if an donuts style exists by name.

        Args:
            name (str): Name of the donuts style.

        Returns:
            bool: True if the donuts style exists, False otherwise.
        """
        return name in self._styles

    @error_handler
    def get(self, name: str = "", use_shapestyles_if_not_exist: bool = True) -> ShapeStyle:
        """Retrieve an donuts style by name.

        Args:
            name (str, optional): Name of the donuts style to retrieve. Defaults to "".
            use_shapestyles_if_not_exist (bool, optional): Whether to fallback to ShapeStyleCache if
                the style does not exist in _styles. Defaults to True.

        Returns:
            ShapeStyle: The retrieved ShapeStyle object.

        Raises:
            ValueError: If the donuts style with the specified name does not exist and
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
        """List all existing donuts style names.

        Returns:
            List[str]: List of donuts style names.
        """
        return list_(self._styles.keys())

    @error_handler
    def set(self, style: ShapeStyle, name: str = "") -> None:
        """Set or update an donuts style with the given name.

        Args:
            style (ShapeStyle): The ShapeStyle object to cache.
            name (str, optional): Name of the donuts style. Defaults to "".

        Raises:
            ValueError: If the style is invalid or name is not a string.
        """
        style_validator.validate_shapestyle("style", style)
        type_validator.validate_str("name", name)
        self._styles[name] = style.copy()
        self._callback_set(name)

    @error_handler
    def delete(self, name: str) -> None:
        """Delete an donuts style by name.

        Args:
            name (str): Name of the donuts style to delete.

        Raises:
            ValueError: If the donuts style with the specified name does not exist.
        """
        if not self.has(name):
            raise ValueError('Theme style name "' + name + '" does not exist.')
        del self._styles[name]
        self._callback_delete(name)

    @error_handler
    def merge(self, style: ShapeStyle, targets: Optional[List[str]] = None) -> None:
        """Merge an donuts style into existing donuts styles.

        Args:
            style (ShapeStyle): The ShapeStyle object to merge.
            targets (Optional[List[str]], optional): List of target donuts style names to merge into.
                If None, merge into all existing donuts styles. Defaults to None.

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


class EllipseStyleCache(AbstractStyleCache):
    """Cache for managing ellipse styles.

    This class provides methods to manage and manipulate ShapeStyle objects
    specifically tailored for ellipse within a cache.
    """

    def __init__(
        self,
        shapestyles: ShapeStyleCache,
        callback_set: Callable[
            [
                str,
            ],
            None,
        ],
        callback_delete: Callable[
            [
                str,
            ],
            None,
        ],
    ) -> None:
        """Initialize EllipseStyleCache.

        Args:
            shapestyles (ShapeStyleCache): Cache of shape styles to use as fallback.
            callback_set: Callback function for set operation.
            callback_delete: Callback function for delete operation.
        """
        self._callback_set = callback_set
        self._callback_delete = callback_delete
        self._styles: Dict[str, ShapeStyle] = {}
        self._shapestyles = shapestyles

    @error_handler
    def has(self, name: str) -> bool:
        """Check if an ellipse style exists by name.

        Args:
            name (str): Name of the ellipse style.

        Returns:
            bool: True if the ellipse style exists, False otherwise.
        """
        return name in self._styles

    @error_handler
    def get(self, name: str = "", use_shapestyles_if_not_exist: bool = True) -> ShapeStyle:
        """Retrieve an ellipse style by name.

        Args:
            name (str, optional): Name of the ellipse style to retrieve. Defaults to "".
            use_shapestyles_if_not_exist (bool, optional): Whether to fallback to ShapeStyleCache if
                the style does not exist in _styles. Defaults to True.

        Returns:
            ShapeStyle: The retrieved ShapeStyle object.

        Raises:
            ValueError: If the ellipse style with the specified name does not exist and
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
        """List all existing ellipse style names.

        Returns:
            List[str]: List of ellipse style names.
        """
        return list_(self._styles.keys())

    @error_handler
    def set(self, style: ShapeStyle, name: str = "") -> None:
        """Set or update an ellipse style with the given name.

        Args:
            style (ShapeStyle): The ShapeStyle object to cache.
            name (str, optional): Name of the ellipse style. Defaults to "".

        Raises:
            ValueError: If the style is invalid or name is not a string.
        """
        style_validator.validate_shapestyle("style", style)
        type_validator.validate_str("name", name)
        self._styles[name] = style.copy()
        self._callback_set(name)

    @error_handler
    def delete(self, name: str) -> None:
        """Delete an ellipse style by name.

        Args:
            name (str): Name of the ellipse style to delete.

        Raises:
            ValueError: If the ellipse style with the specified name does not exist.
        """
        if not self.has(name):
            raise ValueError('Theme style name "' + name + '" does not exist.')
        del self._styles[name]
        self._callback_delete(name)

    @error_handler
    def merge(self, style: ShapeStyle, targets: Optional[List[str]] = None) -> None:
        """Merge an ellipse style into existing ellipse styles.

        Args:
            style (ShapeStyle): The ShapeStyle object to merge.
            targets (Optional[List[str]], optional): List of target ellipse style names to merge into.
                If None, merge into all existing ellipse styles. Defaults to None.

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


class FanStyleCache(AbstractStyleCache):
    """Cache for managing fan styles.

    This class provides methods to manage and manipulate ShapeStyle objects
    specifically tailored for fan within a cache.
    """

    def __init__(
        self,
        shapestyles: ShapeStyleCache,
        callback_set: Callable[
            [
                str,
            ],
            None,
        ],
        callback_delete: Callable[
            [
                str,
            ],
            None,
        ],
    ) -> None:
        """Initialize FanStyleCache.

        Args:
            shapestyles (ShapeStyleCache): Cache of shape styles to use as fallback.
            callback_set: Callback function for set operation.
            callback_delete: Callback function for delete operation.
        """
        self._callback_set = callback_set
        self._callback_delete = callback_delete
        self._styles: Dict[str, ShapeStyle] = {}
        self._shapestyles = shapestyles

    @error_handler
    def has(self, name: str) -> bool:
        """Check if an fan style exists by name.

        Args:
            name (str): Name of the fan style.

        Returns:
            bool: True if the fan style exists, False otherwise.
        """
        return name in self._styles

    @error_handler
    def get(self, name: str = "", use_shapestyles_if_not_exist: bool = True) -> ShapeStyle:
        """Retrieve an fan style by name.

        Args:
            name (str, optional): Name of the fan style to retrieve. Defaults to "".
            use_shapestyles_if_not_exist (bool, optional): Whether to fallback to ShapeStyleCache if
                the style does not exist in _styles. Defaults to True.

        Returns:
            ShapeStyle: The retrieved ShapeStyle object.

        Raises:
            ValueError: If the fan style with the specified name does not exist and
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
        """List all existing fan style names.

        Returns:
            List[str]: List of fan style names.
        """
        return list_(self._styles.keys())

    @error_handler
    def set(self, style: ShapeStyle, name: str = "") -> None:
        """Set or update an fan style with the given name.

        Args:
            style (ShapeStyle): The ShapeStyle object to cache.
            name (str, optional): Name of the fan style. Defaults to "".

        Raises:
            ValueError: If the style is invalid or name is not a string.
        """
        style_validator.validate_shapestyle("style", style)
        type_validator.validate_str("name", name)
        self._styles[name] = style.copy()
        self._callback_set(name)

    @error_handler
    def delete(self, name: str) -> None:
        """Delete an fan style by name.

        Args:
            name (str): Name of the fan style to delete.

        Raises:
            ValueError: If the fan style with the specified name does not exist.
        """
        if not self.has(name):
            raise ValueError('Theme style name "' + name + '" does not exist.')
        del self._styles[name]
        self._callback_delete(name)

    @error_handler
    def merge(self, style: ShapeStyle, targets: Optional[List[str]] = None) -> None:
        """Merge an fan style into existing fan styles.

        Args:
            style (ShapeStyle): The ShapeStyle object to merge.
            targets (Optional[List[str]], optional): List of target fan style names to merge into.
                If None, merge into all existing fan styles. Defaults to None.

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


class PolygonStyleCache(AbstractStyleCache):
    """Cache for managing polygon styles.

    This class provides methods to manage and manipulate ShapeStyle objects
    specifically tailored for polygon within a cache.
    """

    def __init__(
        self,
        shapestyles: ShapeStyleCache,
        callback_set: Callable[
            [
                str,
            ],
            None,
        ],
        callback_delete: Callable[
            [
                str,
            ],
            None,
        ],
    ) -> None:
        """Initialize PolygonStyleCache.

        Args:
            shapestyles (ShapeStyleCache): Cache of shape styles to use as fallback.
            callback_set: Callback function for set operation.
            callback_delete: Callback function for delete operation.
        """
        self._callback_set = callback_set
        self._callback_delete = callback_delete
        self._styles: Dict[str, ShapeStyle] = {}
        self._shapestyles = shapestyles

    @error_handler
    def has(self, name: str) -> bool:
        """Check if an polygon style exists by name.

        Args:
            name (str): Name of the polygon style.

        Returns:
            bool: True if the polygon style exists, False otherwise.
        """
        return name in self._styles

    @error_handler
    def get(self, name: str = "", use_shapestyles_if_not_exist: bool = True) -> ShapeStyle:
        """Retrieve an polygon style by name.

        Args:
            name (str, optional): Name of the polygon style to retrieve. Defaults to "".
            use_shapestyles_if_not_exist (bool, optional): Whether to fallback to ShapeStyleCache if
                the style does not exist in _styles. Defaults to True.

        Returns:
            ShapeStyle: The retrieved ShapeStyle object.

        Raises:
            ValueError: If the polygon style with the specified name does not exist and
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
        """List all existing polygon style names.

        Returns:
            List[str]: List of polygon style names.
        """
        return list_(self._styles.keys())

    @error_handler
    def set(self, style: ShapeStyle, name: str = "") -> None:
        """Set or update an polygon style with the given name.

        Args:
            style (ShapeStyle): The ShapeStyle object to cache.
            name (str, optional): Name of the polygon style. Defaults to "".

        Raises:
            ValueError: If the style is invalid or name is not a string.
        """
        style_validator.validate_shapestyle("style", style)
        type_validator.validate_str("name", name)
        self._styles[name] = style.copy()
        self._callback_set(name)

    @error_handler
    def delete(self, name: str) -> None:
        """Delete an polygon style by name.

        Args:
            name (str): Name of the polygon style to delete.

        Raises:
            ValueError: If the polygon style with the specified name does not exist.
        """
        if not self.has(name):
            raise ValueError('Theme style name "' + name + '" does not exist.')
        del self._styles[name]
        self._callback_delete(name)

    @error_handler
    def merge(self, style: ShapeStyle, targets: Optional[List[str]] = None) -> None:
        """Merge an polygon style into existing polygon styles.

        Args:
            style (ShapeStyle): The ShapeStyle object to merge.
            targets (Optional[List[str]], optional): List of target polygon style names to merge into.
                If None, merge into all existing polygon styles. Defaults to None.

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


class RectangleStyleCache(AbstractStyleCache):
    """Cache for managing rectangle styles.

    This class provides methods to manage and manipulate ShapeStyle objects
    specifically tailored for rectangle within a cache.
    """

    def __init__(
        self,
        shapestyles: ShapeStyleCache,
        callback_set: Callable[
            [
                str,
            ],
            None,
        ],
        callback_delete: Callable[
            [
                str,
            ],
            None,
        ],
    ) -> None:
        """Initialize RectangleStyleCache.

        Args:
            shapestyles (ShapeStyleCache): Cache of shape styles to use as fallback.
            callback_set: Callback function for set operation.
            callback_delete: Callback function for delete operation.
        """
        self._callback_set = callback_set
        self._callback_delete = callback_delete
        self._styles: Dict[str, ShapeStyle] = {}
        self._shapestyles = shapestyles

    @error_handler
    def has(self, name: str) -> bool:
        """Check if an rectangle style exists by name.

        Args:
            name (str): Name of the rectangle style.

        Returns:
            bool: True if the rectangle style exists, False otherwise.
        """
        return name in self._styles

    @error_handler
    def get(self, name: str = "", use_shapestyles_if_not_exist: bool = True) -> ShapeStyle:
        """Retrieve an rectangle style by name.

        Args:
            name (str, optional): Name of the rectangle style to retrieve. Defaults to "".
            use_shapestyles_if_not_exist (bool, optional): Whether to fallback to ShapeStyleCache if
                the style does not exist in _styles. Defaults to True.

        Returns:
            ShapeStyle: The retrieved ShapeStyle object.

        Raises:
            ValueError: If the rectangle style with the specified name does not exist and
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
        """List all existing rectangle style names.

        Returns:
            List[str]: List of rectangle style names.
        """
        return list_(self._styles.keys())

    @error_handler
    def set(self, style: ShapeStyle, name: str = "") -> None:
        """Set or update an rectangle style with the given name.

        Args:
            style (ShapeStyle): The ShapeStyle object to cache.
            name (str, optional): Name of the rectangle style. Defaults to "".

        Raises:
            ValueError: If the style is invalid or name is not a string.
        """
        style_validator.validate_shapestyle("style", style)
        type_validator.validate_str("name", name)
        self._styles[name] = style.copy()
        self._callback_set(name)

    @error_handler
    def delete(self, name: str) -> None:
        """Delete an rectangle style by name.

        Args:
            name (str): Name of the rectangle style to delete.

        Raises:
            ValueError: If the rectangle style with the specified name does not exist.
        """
        if not self.has(name):
            raise ValueError('Theme style name "' + name + '" does not exist.')
        del self._styles[name]
        self._callback_delete(name)

    @error_handler
    def merge(self, style: ShapeStyle, targets: Optional[List[str]] = None) -> None:
        """Merge an rectangle style into existing rectangle styles.

        Args:
            style (ShapeStyle): The ShapeStyle object to merge.
            targets (Optional[List[str]], optional): List of target rectangle style names to merge into.
                If None, merge into all existing rectangle styles. Defaults to None.

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


class RegularpolygonStyleCache(AbstractStyleCache):
    """Cache for managing regular polygon styles.

    This class provides methods to manage and manipulate ShapeStyle objects
    specifically tailored for regular polygon within a cache.
    """

    def __init__(
        self,
        shapestyles: ShapeStyleCache,
        callback_set: Callable[
            [
                str,
            ],
            None,
        ],
        callback_delete: Callable[
            [
                str,
            ],
            None,
        ],
    ) -> None:
        """Initialize RegularpolygonStyleCache.

        Args:
            shapestyles (ShapeStyleCache): Cache of shape styles to use as fallback.
            callback_set: Callback function for set operation.
            callback_delete: Callback function for delete operation.
        """
        self._callback_set = callback_set
        self._callback_delete = callback_delete
        self._styles: Dict[str, ShapeStyle] = {}
        self._shapestyles = shapestyles

    @error_handler
    def has(self, name: str) -> bool:
        """Check if an regular polygon style exists by name.

        Args:
            name (str): Name of the regular polygon style.

        Returns:
            bool: True if the regular polygon style exists, False otherwise.
        """
        return name in self._styles

    @error_handler
    def get(self, name: str = "", use_shapestyles_if_not_exist: bool = True) -> ShapeStyle:
        """Retrieve an regular polygon style by name.

        Args:
            name (str, optional): Name of the regular polygon style to retrieve. Defaults to "".
            use_shapestyles_if_not_exist (bool, optional): Whether to fallback to ShapeStyleCache if
                the style does not exist in _styles. Defaults to True.

        Returns:
            ShapeStyle: The retrieved ShapeStyle object.

        Raises:
            ValueError: If the regular polygon style with the specified name does not exist and
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
        """List all existing regular polygon style names.

        Returns:
            List[str]: List of regular polygon style names.
        """
        return list_(self._styles.keys())

    @error_handler
    def set(self, style: ShapeStyle, name: str = "") -> None:
        """Set or update an regular polygon style with the given name.

        Args:
            style (ShapeStyle): The ShapeStyle object to cache.
            name (str, optional): Name of the regular polygon style. Defaults to "".

        Raises:
            ValueError: If the style is invalid or name is not a string.
        """
        style_validator.validate_shapestyle("style", style)
        type_validator.validate_str("name", name)
        self._styles[name] = style.copy()
        self._callback_set(name)

    @error_handler
    def delete(self, name: str) -> None:
        """Delete an regular polygon style by name.

        Args:
            name (str): Name of the regular polygon style to delete.

        Raises:
            ValueError: If the regular polygon style with the specified name does not exist.
        """
        if not self.has(name):
            raise ValueError('Theme style name "' + name + '" does not exist.')
        del self._styles[name]
        self._callback_delete(name)

    @error_handler
    def merge(self, style: ShapeStyle, targets: Optional[List[str]] = None) -> None:
        """Merge an regular polygon style into existing regular polygon styles.

        Args:
            style (ShapeStyle): The ShapeStyle object to merge.
            targets (Optional[List[str]], optional): List of target regular polygon style names to merge into.
                If None, merge into all existing regular polygon styles. Defaults to None.

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


class WedgeStyleCache(AbstractStyleCache):
    """Cache for managing wedge styles.

    This class provides methods to manage and manipulate ShapeStyle objects
    specifically tailored for wedge within a cache.
    """

    def __init__(
        self,
        shapestyles: ShapeStyleCache,
        callback_set: Callable[
            [
                str,
            ],
            None,
        ],
        callback_delete: Callable[
            [
                str,
            ],
            None,
        ],
    ) -> None:
        """Initialize WedgeStyleCache.

        Args:
            shapestyles (ShapeStyleCache): Cache of shape styles to use as fallback.
            callback_set: Callback function for set operation.
            callback_delete: Callback function for delete operation.
        """
        self._callback_set = callback_set
        self._callback_delete = callback_delete
        self._styles: Dict[str, ShapeStyle] = {}
        self._shapestyles = shapestyles

    @error_handler
    def has(self, name: str) -> bool:
        """Check if an wedge style exists by name.

        Args:
            name (str): Name of the wedge style.

        Returns:
            bool: True if the wedge style exists, False otherwise.
        """
        return name in self._styles

    @error_handler
    def get(self, name: str = "", use_shapestyles_if_not_exist: bool = True) -> ShapeStyle:
        """Retrieve an wedge style by name.

        Args:
            name (str, optional): Name of the wedge style to retrieve. Defaults to "".
            use_shapestyles_if_not_exist (bool, optional): Whether to fallback to ShapeStyleCache if
                the style does not exist in _styles. Defaults to True.

        Returns:
            ShapeStyle: The retrieved ShapeStyle object.

        Raises:
            ValueError: If the wedge style with the specified name does not exist and
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
        """List all existing wedge style names.

        Returns:
            List[str]: List of wedge style names.
        """
        return list_(self._styles.keys())

    @error_handler
    def set(self, style: ShapeStyle, name: str = "") -> None:
        """Set or update an wedge style with the given name.

        Args:
            style (ShapeStyle): The ShapeStyle object to cache.
            name (str, optional): Name of the wedge style. Defaults to "".

        Raises:
            ValueError: If the style is invalid or name is not a string.
        """
        style_validator.validate_shapestyle("style", style)
        type_validator.validate_str("name", name)
        self._styles[name] = style.copy()
        self._callback_set(name)

    @error_handler
    def delete(self, name: str) -> None:
        """Delete an wedge style by name.

        Args:
            name (str): Name of the wedge style to delete.

        Raises:
            ValueError: If the wedge style with the specified name does not exist.
        """
        if not self.has(name):
            raise ValueError('Theme style name "' + name + '" does not exist.')
        del self._styles[name]
        self._callback_delete(name)

    @error_handler
    def merge(self, style: ShapeStyle, targets: Optional[List[str]] = None) -> None:
        """Merge an wedge style into existing wedge styles.

        Args:
            style (ShapeStyle): The ShapeStyle object to merge.
            targets (Optional[List[str]], optional): List of target wedge style names to merge into.
                If None, merge into all existing wedge styles. Defaults to None.

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


class ArrowStyleCache(AbstractStyleCache):
    """Cache for managing arrow styles.

    This class provides methods to manage and manipulate ShapeStyle objects
    specifically tailored for arrow within a cache.
    """

    def __init__(
        self,
        shapestyles: ShapeStyleCache,
        callback_set: Callable[
            [
                str,
            ],
            None,
        ],
        callback_delete: Callable[
            [
                str,
            ],
            None,
        ],
    ) -> None:
        """Initialize ArrowStyleCache.

        Args:
            shapestyles (ShapeStyleCache): Cache of shape styles to use as fallback.
            callback_set: Callback function for set operation.
            callback_delete: Callback function for delete operation.
        """
        self._callback_set = callback_set
        self._callback_delete = callback_delete
        self._styles: Dict[str, ShapeStyle] = {}
        self._shapestyles = shapestyles

    @error_handler
    def has(self, name: str) -> bool:
        """Check if an arrow style exists by name.

        Args:
            name (str): Name of the arrow style.

        Returns:
            bool: True if the arrow style exists, False otherwise.
        """
        return name in self._styles

    @error_handler
    def get(self, name: str = "", use_shapestyles_if_not_exist: bool = True) -> ShapeStyle:
        """Retrieve an arrow style by name.

        Args:
            name (str, optional): Name of the arrow style to retrieve. Defaults to "".
            use_shapestyles_if_not_exist (bool, optional): Whether to fallback to ShapeStyleCache if
                the style does not exist in _styles. Defaults to True.

        Returns:
            ShapeStyle: The retrieved ShapeStyle object.

        Raises:
            ValueError: If the arrow style with the specified name does not exist and
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
        """List all existing arrow style names.

        Returns:
            List[str]: List of arrow style names.
        """
        return list_(self._styles.keys())

    @error_handler
    def set(self, style: ShapeStyle, name: str = "") -> None:
        """Set or update an arrow style with the given name.

        Args:
            style (ShapeStyle): The ShapeStyle object to cache.
            name (str, optional): Name of the arrow style. Defaults to "".

        Raises:
            ValueError: If the style is invalid or name is not a string.
        """
        style_validator.validate_shapestyle("style", style)
        type_validator.validate_str("name", name)
        self._styles[name] = style.copy()
        self._callback_set(name)

    @error_handler
    def delete(self, name: str) -> None:
        """Delete an arrow style by name.

        Args:
            name (str): Name of the arrow style to delete.

        Raises:
            ValueError: If the arrow style with the specified name does not exist.
        """
        if not self.has(name):
            raise ValueError('Theme style name "' + name + '" does not exist.')
        del self._styles[name]
        self._callback_delete(name)

    @error_handler
    def merge(self, style: ShapeStyle, targets: Optional[List[str]] = None) -> None:
        """Merge an arrow style into existing arrow styles.

        Args:
            style (ShapeStyle): The ShapeStyle object to merge.
            targets (Optional[List[str]], optional): List of target arrow style names to merge into.
                If None, merge into all existing arrow styles. Defaults to None.

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


class ChevronStyleCache(AbstractStyleCache):
    """Cache for managing chevron styles.

    This class provides methods to manage and manipulate ShapeStyle objects
    specifically tailored for chevron within a cache.
    """

    def __init__(
        self,
        shapestyles: ShapeStyleCache,
        callback_set: Callable[
            [
                str,
            ],
            None,
        ],
        callback_delete: Callable[
            [
                str,
            ],
            None,
        ],
    ) -> None:
        """Initialize ChevronStyleCache.

        Args:
            shapestyles (ShapeStyleCache): Cache of shape styles to use as fallback.
            callback_set: Callback function for set operation.
            callback_delete: Callback function for delete operation.
        """
        self._callback_set = callback_set
        self._callback_delete = callback_delete
        self._styles: Dict[str, ShapeStyle] = {}
        self._shapestyles = shapestyles

    @error_handler
    def has(self, name: str) -> bool:
        """Check if an chevron style exists by name.

        Args:
            name (str): Name of the chevron style.

        Returns:
            bool: True if the chevron style exists, False otherwise.
        """
        return name in self._styles

    @error_handler
    def get(self, name: str = "", use_shapestyles_if_not_exist: bool = True) -> ShapeStyle:
        """Retrieve an chevron style by name.

        Args:
            name (str, optional): Name of the chevron style to retrieve. Defaults to "".
            use_shapestyles_if_not_exist (bool, optional): Whether to fallback to ShapeStyleCache if
                the style does not exist in _styles. Defaults to True.

        Returns:
            ShapeStyle: The retrieved ShapeStyle object.

        Raises:
            ValueError: If the chevron style with the specified name does not exist and
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
        """List all existing chevron style names.

        Returns:
            List[str]: List of chevron style names.
        """
        return list_(self._styles.keys())

    @error_handler
    def set(self, style: ShapeStyle, name: str = "") -> None:
        """Set or update an chevron style with the given name.

        Args:
            style (ShapeStyle): The ShapeStyle object to cache.
            name (str, optional): Name of the chevron style. Defaults to "".

        Raises:
            ValueError: If the style is invalid or name is not a string.
        """
        style_validator.validate_shapestyle("style", style)
        type_validator.validate_str("name", name)
        self._styles[name] = style.copy()
        self._callback_set(name)

    @error_handler
    def delete(self, name: str) -> None:
        """Delete an chevron style by name.

        Args:
            name (str): Name of the chevron style to delete.

        Raises:
            ValueError: If the chevron style with the specified name does not exist.
        """
        if not self.has(name):
            raise ValueError('Theme style name "' + name + '" does not exist.')
        del self._styles[name]
        self._callback_delete(name)

    @error_handler
    def merge(self, style: ShapeStyle, targets: Optional[List[str]] = None) -> None:
        """Merge an chevron style into existing chevron styles.

        Args:
            style (ShapeStyle): The ShapeStyle object to merge.
            targets (Optional[List[str]], optional): List of target chevron style names to merge into.
                If None, merge into all existing chevron styles. Defaults to None.

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


class ParallelogramStyleCache(AbstractStyleCache):
    """Cache for managing parallelogram styles.

    This class provides methods to manage and manipulate ShapeStyle objects
    specifically tailored for parallelogram within a cache.
    """

    def __init__(
        self,
        shapestyles: ShapeStyleCache,
        callback_set: Callable[
            [
                str,
            ],
            None,
        ],
        callback_delete: Callable[
            [
                str,
            ],
            None,
        ],
    ) -> None:
        """Initialize ParallelogramStyleCache.

        Args:
            shapestyles (ShapeStyleCache): Cache of shape styles to use as fallback.
            callback_set: Callback function for set operation.
            callback_delete: Callback function for delete operation.
        """
        self._callback_set = callback_set
        self._callback_delete = callback_delete
        self._styles: Dict[str, ShapeStyle] = {}
        self._shapestyles = shapestyles

    @error_handler
    def has(self, name: str) -> bool:
        """Check if an parallelogram style exists by name.

        Args:
            name (str): Name of the parallelogram style.

        Returns:
            bool: True if the parallelogram style exists, False otherwise.
        """
        return name in self._styles

    @error_handler
    def get(self, name: str = "", use_shapestyles_if_not_exist: bool = True) -> ShapeStyle:
        """Retrieve an parallelogram style by name.

        Args:
            name (str, optional): Name of the parallelogram style to retrieve. Defaults to "".
            use_shapestyles_if_not_exist (bool, optional): Whether to fallback to ShapeStyleCache if
                the style does not exist in _styles. Defaults to True.

        Returns:
            ShapeStyle: The retrieved ShapeStyle object.

        Raises:
            ValueError: If the parallelogram style with the specified name does not exist and
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
        """List all existing parallelogram style names.

        Returns:
            List[str]: List of parallelogram style names.
        """
        return list_(self._styles.keys())

    @error_handler
    def set(self, style: ShapeStyle, name: str = "") -> None:
        """Set or update an parallelogram style with the given name.

        Args:
            style (ShapeStyle): The ShapeStyle object to cache.
            name (str, optional): Name of the parallelogram style. Defaults to "".

        Raises:
            ValueError: If the style is invalid or name is not a string.
        """
        style_validator.validate_shapestyle("style", style)
        type_validator.validate_str("name", name)
        self._styles[name] = style.copy()
        self._callback_set(name)

    @error_handler
    def delete(self, name: str) -> None:
        """Delete an parallelogram style by name.

        Args:
            name (str): Name of the parallelogram style to delete.

        Raises:
            ValueError: If the parallelogram style with the specified name does not exist.
        """
        if not self.has(name):
            raise ValueError('Theme style name "' + name + '" does not exist.')
        del self._styles[name]
        self._callback_delete(name)

    @error_handler
    def merge(self, style: ShapeStyle, targets: Optional[List[str]] = None) -> None:
        """Merge an parallelogram style into existing parallelogram styles.

        Args:
            style (ShapeStyle): The ShapeStyle object to merge.
            targets (Optional[List[str]], optional): List of target parallelogram style names to merge into.
                If None, merge into all existing parallelogram styles. Defaults to None.

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


class RhombusStyleCache(AbstractStyleCache):
    """Cache for managing rhombus styles.

    This class provides methods to manage and manipulate ShapeStyle objects
    specifically tailored for rhombus within a cache.
    """

    def __init__(
        self,
        shapestyles: ShapeStyleCache,
        callback_set: Callable[
            [
                str,
            ],
            None,
        ],
        callback_delete: Callable[
            [
                str,
            ],
            None,
        ],
    ) -> None:
        """Initialize RhombusStyleCache.

        Args:
            shapestyles (ShapeStyleCache): Cache of shape styles to use as fallback.
            callback_set: Callback function for set operation.
            callback_delete: Callback function for delete operation.
        """
        self._callback_set = callback_set
        self._callback_delete = callback_delete
        self._styles: Dict[str, ShapeStyle] = {}
        self._shapestyles = shapestyles

    @error_handler
    def has(self, name: str) -> bool:
        """Check if an rhombus style exists by name.

        Args:
            name (str): Name of the rhombus style.

        Returns:
            bool: True if the rhombus style exists, False otherwise.
        """
        return name in self._styles

    @error_handler
    def get(self, name: str = "", use_shapestyles_if_not_exist: bool = True) -> ShapeStyle:
        """Retrieve an rhombus style by name.

        Args:
            name (str, optional): Name of the rhombus style to retrieve. Defaults to "".
            use_shapestyles_if_not_exist (bool, optional): Whether to fallback to ShapeStyleCache if
                the style does not exist in _styles. Defaults to True.

        Returns:
            ShapeStyle: The retrieved ShapeStyle object.

        Raises:
            ValueError: If the rhombus style with the specified name does not exist and
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
        """List all existing rhombus style names.

        Returns:
            List[str]: List of rhombus style names.
        """
        return list_(self._styles.keys())

    @error_handler
    def set(self, style: ShapeStyle, name: str = "") -> None:
        """Set or update an rhombus style with the given name.

        Args:
            style (ShapeStyle): The ShapeStyle object to cache.
            name (str, optional): Name of the rhombus style. Defaults to "".

        Raises:
            ValueError: If the style is invalid or name is not a string.
        """
        style_validator.validate_shapestyle("style", style)
        type_validator.validate_str("name", name)
        self._styles[name] = style.copy()
        self._callback_set(name)

    @error_handler
    def delete(self, name: str) -> None:
        """Delete an rhombus style by name.

        Args:
            name (str): Name of the rhombus style to delete.

        Raises:
            ValueError: If the rhombus style with the specified name does not exist.
        """
        if not self.has(name):
            raise ValueError('Theme style name "' + name + '" does not exist.')
        del self._styles[name]
        self._callback_delete(name)

    @error_handler
    def merge(self, style: ShapeStyle, targets: Optional[List[str]] = None) -> None:
        """Merge an rhombus style into existing rhombus styles.

        Args:
            style (ShapeStyle): The ShapeStyle object to merge.
            targets (Optional[List[str]], optional): List of target rhombus style names to merge into.
                If None, merge into all existing rhombus styles. Defaults to None.

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


class StarStyleCache(AbstractStyleCache):
    """Cache for managing star styles.

    This class provides methods to manage and manipulate ShapeStyle objects
    specifically tailored for star within a cache.
    """

    def __init__(
        self,
        shapestyles: ShapeStyleCache,
        callback_set: Callable[
            [
                str,
            ],
            None,
        ],
        callback_delete: Callable[
            [
                str,
            ],
            None,
        ],
    ) -> None:
        """Initialize StarStyleCache.

        Args:
            shapestyles (ShapeStyleCache): Cache of shape styles to use as fallback.
            callback_set: Callback function for set operation.
            callback_delete: Callback function for delete operation.
        """
        self._callback_set = callback_set
        self._callback_delete = callback_delete
        self._styles: Dict[str, ShapeStyle] = {}
        self._shapestyles = shapestyles

    @error_handler
    def has(self, name: str) -> bool:
        """Check if an star style exists by name.

        Args:
            name (str): Name of the star style.

        Returns:
            bool: True if the star style exists, False otherwise.
        """
        return name in self._styles

    @error_handler
    def get(self, name: str = "", use_shapestyles_if_not_exist: bool = True) -> ShapeStyle:
        """Retrieve an star style by name.

        Args:
            name (str, optional): Name of the star style to retrieve. Defaults to "".
            use_shapestyles_if_not_exist (bool, optional): Whether to fallback to ShapeStyleCache if
                the style does not exist in _styles. Defaults to True.

        Returns:
            ShapeStyle: The retrieved ShapeStyle object.

        Raises:
            ValueError: If the star style with the specified name does not exist and
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
        """List all existing star style names.

        Returns:
            List[str]: List of star style names.
        """
        return list_(self._styles.keys())

    @error_handler
    def set(self, style: ShapeStyle, name: str = "") -> None:
        """Set or update an star style with the given name.

        Args:
            style (ShapeStyle): The ShapeStyle object to cache.
            name (str, optional): Name of the star style. Defaults to "".

        Raises:
            ValueError: If the style is invalid or name is not a string.
        """
        style_validator.validate_shapestyle("style", style)
        type_validator.validate_str("name", name)
        self._styles[name] = style.copy()
        self._callback_set(name)

    @error_handler
    def delete(self, name: str) -> None:
        """Delete an star style by name.

        Args:
            name (str): Name of the star style to delete.

        Raises:
            ValueError: If the star style with the specified name does not exist.
        """
        if not self.has(name):
            raise ValueError('Theme style name "' + name + '" does not exist.')
        del self._styles[name]
        self._callback_delete(name)

    @error_handler
    def merge(self, style: ShapeStyle, targets: Optional[List[str]] = None) -> None:
        """Merge an star style into existing star styles.

        Args:
            style (ShapeStyle): The ShapeStyle object to merge.
            targets (Optional[List[str]], optional): List of target star style names to merge into.
                If None, merge into all existing star styles. Defaults to None.

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


class TrapezoidStyleCache(AbstractStyleCache):
    """Cache for managing trapezoid styles.

    This class provides methods to manage and manipulate ShapeStyle objects
    specifically tailored for trapezoid within a cache.
    """

    def __init__(
        self,
        shapestyles: ShapeStyleCache,
        callback_set: Callable[
            [
                str,
            ],
            None,
        ],
        callback_delete: Callable[
            [
                str,
            ],
            None,
        ],
    ) -> None:
        """Initialize TrapezoidStyleCache.

        Args:
            shapestyles (ShapeStyleCache): Cache of shape styles to use as fallback.
            callback_set: Callback function for set operation.
            callback_delete: Callback function for delete operation.
        """
        self._callback_set = callback_set
        self._callback_delete = callback_delete
        self._styles: Dict[str, ShapeStyle] = {}
        self._shapestyles = shapestyles

    @error_handler
    def has(self, name: str) -> bool:
        """Check if an trapezoid style exists by name.

        Args:
            name (str): Name of the trapezoid style.

        Returns:
            bool: True if the trapezoid style exists, False otherwise.
        """
        return name in self._styles

    @error_handler
    def get(self, name: str = "", use_shapestyles_if_not_exist: bool = True) -> ShapeStyle:
        """Retrieve an trapezoid style by name.

        Args:
            name (str, optional): Name of the trapezoid style to retrieve. Defaults to "".
            use_shapestyles_if_not_exist (bool, optional): Whether to fallback to ShapeStyleCache if
                the style does not exist in _styles. Defaults to True.

        Returns:
            ShapeStyle: The retrieved ShapeStyle object.

        Raises:
            ValueError: If the trapezoid style with the specified name does not exist and
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
        """List all existing trapezoid style names.

        Returns:
            List[str]: List of trapezoid style names.
        """
        return list_(self._styles.keys())

    @error_handler
    def set(self, style: ShapeStyle, name: str = "") -> None:
        """Set or update an trapezoid style with the given name.

        Args:
            style (ShapeStyle): The ShapeStyle object to cache.
            name (str, optional): Name of the trapezoid style. Defaults to "".

        Raises:
            ValueError: If the style is invalid or name is not a string.
        """
        style_validator.validate_shapestyle("style", style)
        type_validator.validate_str("name", name)
        self._styles[name] = style.copy()
        self._callback_set(name)

    @error_handler
    def delete(self, name: str) -> None:
        """Delete an trapezoid style by name.

        Args:
            name (str): Name of the trapezoid style to delete.

        Raises:
            ValueError: If the trapezoid style with the specified name does not exist.
        """
        if not self.has(name):
            raise ValueError('Theme style name "' + name + '" does not exist.')
        del self._styles[name]
        self._callback_delete(name)

    @error_handler
    def merge(self, style: ShapeStyle, targets: Optional[List[str]] = None) -> None:
        """Merge an trapezoid style into existing trapezoid styles.

        Args:
            style (ShapeStyle): The ShapeStyle object to merge.
            targets (Optional[List[str]], optional): List of target trapezoid style names to merge into.
                If None, merge into all existing trapezoid styles. Defaults to None.

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


class TriangleStyleCache(AbstractStyleCache):
    """Cache for managing triangle styles.

    This class provides methods to manage and manipulate ShapeStyle objects
    specifically tailored for triangle within a cache.
    """

    def __init__(
        self,
        shapestyles: ShapeStyleCache,
        callback_set: Callable[
            [
                str,
            ],
            None,
        ],
        callback_delete: Callable[
            [
                str,
            ],
            None,
        ],
    ) -> None:
        """Initialize TriangleStyleCache.

        Args:
            shapestyles (ShapeStyleCache): Cache of shape styles to use as fallback.
            callback_set: Callback function for set operation.
            callback_delete: Callback function for delete operation.
        """
        self._callback_set = callback_set
        self._callback_delete = callback_delete
        self._styles: Dict[str, ShapeStyle] = {}
        self._shapestyles = shapestyles

    @error_handler
    def has(self, name: str) -> bool:
        """Check if an triangle style exists by name.

        Args:
            name (str): Name of the triangle style.

        Returns:
            bool: True if the triangle style exists, False otherwise.
        """
        return name in self._styles

    @error_handler
    def get(self, name: str = "", use_shapestyles_if_not_exist: bool = True) -> ShapeStyle:
        """Retrieve an triangle style by name.

        Args:
            name (str, optional): Name of the triangle style to retrieve. Defaults to "".
            use_shapestyles_if_not_exist (bool, optional): Whether to fallback to ShapeStyleCache if
                the style does not exist in _styles. Defaults to True.

        Returns:
            ShapeStyle: The retrieved ShapeStyle object.

        Raises:
            ValueError: If the triangle style with the specified name does not exist and
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
        """List all existing triangle style names.

        Returns:
            List[str]: List of triangle style names.
        """
        return list_(self._styles.keys())

    @error_handler
    def set(self, style: ShapeStyle, name: str = "") -> None:
        """Set or update an triangle style with the given name.

        Args:
            style (ShapeStyle): The ShapeStyle object to cache.
            name (str, optional): Name of the triangle style. Defaults to "".

        Raises:
            ValueError: If the style is invalid or name is not a string.
        """
        style_validator.validate_shapestyle("style", style)
        type_validator.validate_str("name", name)
        self._styles[name] = style.copy()
        self._callback_set(name)

    @error_handler
    def delete(self, name: str) -> None:
        """Delete an triangle style by name.

        Args:
            name (str): Name of the triangle style to delete.

        Raises:
            ValueError: If the triangle style with the specified name does not exist.
        """
        if not self.has(name):
            raise ValueError('Theme style name "' + name + '" does not exist.')
        del self._styles[name]
        self._callback_delete(name)

    @error_handler
    def merge(self, style: ShapeStyle, targets: Optional[List[str]] = None) -> None:
        """Merge an triangle style into existing triangle styles.

        Args:
            style (ShapeStyle): The ShapeStyle object to merge.
            targets (Optional[List[str]], optional): List of target triangle style names to merge into.
                If None, merge into all existing triangle styles. Defaults to None.

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


class BubblespeechStyleCache(AbstractStyleCache):
    """Cache for managing bubble speech styles.

    This class provides methods to manage and manipulate ShapeStyle objects
    specifically tailored for bubble speech within a cache.
    """

    def __init__(
        self,
        shapestyles: ShapeStyleCache,
        callback_set: Callable[
            [
                str,
            ],
            None,
        ],
        callback_delete: Callable[
            [
                str,
            ],
            None,
        ],
    ) -> None:
        """Initialize BubblespeechStyleCache.

        Args:
            shapestyles (ShapeStyleCache): Cache of shape styles to use as fallback.
            callback_set: Callback function for set operation.
            callback_delete: Callback function for delete operation.
        """
        self._callback_set = callback_set
        self._callback_delete = callback_delete
        self._styles: Dict[str, ShapeStyle] = {}
        self._shapestyles = shapestyles

    @error_handler
    def has(self, name: str) -> bool:
        """Check if an bubble speech style exists by name.

        Args:
            name (str): Name of the bubble speech style.

        Returns:
            bool: True if the bubble speech style exists, False otherwise.
        """
        return name in self._styles

    @error_handler
    def get(self, name: str = "", use_shapestyles_if_not_exist: bool = True) -> ShapeStyle:
        """Retrieve an bubble speech style by name.

        Args:
            name (str, optional): Name of the bubble speech style to retrieve. Defaults to "".
            use_shapestyles_if_not_exist (bool, optional): Whether to fallback to ShapeStyleCache if
                the style does not exist in _styles. Defaults to True.

        Returns:
            ShapeStyle: The retrieved ShapeStyle object.

        Raises:
            ValueError: If the bubble speech style with the specified name does not exist and
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
        """List all existing bubble speech style names.

        Returns:
            List[str]: List of bubble speech style names.
        """
        return list_(self._styles.keys())

    @error_handler
    def set(self, style: ShapeStyle, name: str = "") -> None:
        """Set or update an bubble speech style with the given name.

        Args:
            style (ShapeStyle): The ShapeStyle object to cache.
            name (str, optional): Name of the bubble speech style. Defaults to "".

        Raises:
            ValueError: If the style is invalid or name is not a string.
        """
        style_validator.validate_shapestyle("style", style)
        type_validator.validate_str("name", name)
        self._styles[name] = style.copy()
        self._callback_set(name)

    @error_handler
    def delete(self, name: str) -> None:
        """Delete an bubble speech style by name.

        Args:
            name (str): Name of the bubble speech style to delete.

        Raises:
            ValueError: If the bubble speech style with the specified name does not exist.
        """
        if not self.has(name):
            raise ValueError('Theme style name "' + name + '" does not exist.')
        del self._styles[name]
        self._callback_delete(name)

    @error_handler
    def merge(self, style: ShapeStyle, targets: Optional[List[str]] = None) -> None:
        """Merge an bubble speech style into existing bubble speech styles.

        Args:
            style (ShapeStyle): The ShapeStyle object to merge.
            targets (Optional[List[str]], optional): List of target bubble speech style names to merge into.
                If None, merge into all existing bubble speech styles. Defaults to None.

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


class ArcTextStyleCache(AbstractStyleCache):
    """Cache for managing arc text styles.

    This class provides methods to manage and manipulate ShapeTextStyle objects
    specifically tailored for arc within a cache.
    """

    def __init__(
        self,
        shapetextstyles: ShapeTextStyleCache,
        callback_set: Callable[
            [
                str,
            ],
            None,
        ],
        callback_delete: Callable[
            [
                str,
            ],
            None,
        ],
    ) -> None:
        """Initialize ArcTextStyleCache.

        Args:
            shapetextstyles (ShapeTextStyleCache): Cache of shape text styles to use as fallback.
            callback_set: Callback function for set operation.
            callback_delete: Callback function for delete operation.
        """
        self._callback_set = callback_set
        self._callback_delete = callback_delete
        self._styles: Dict[str, ShapeTextStyle] = {}
        self._shapetextstyles = shapetextstyles

    @error_handler
    def has(self, name: str) -> bool:
        """Check if an arc text style exists by name.

        Args:
            name (str): Name of the arc text style.

        Returns:
            bool: True if the arc text style exists, False otherwise.
        """
        return name in self._styles

    @error_handler
    def get(self, name: str = "", use_shapetextstyles_if_not_exist: bool = True) -> ShapeTextStyle:
        """Retrieve an arc text style by name.

        Args:
            name (str, optional): Name of the arc text style to retrieve. Defaults to "".
            use_shapetextstyles_if_not_exist (bool, optional): Whether to fallback to ShapeTextStyleCache if
                the style does not exist in _styles. Defaults to True.

        Returns:
            ShapeTextStyle: The retrieved ShapeTextStyle object.

        Raises:
            ValueError: If the arc text style with the specified name does not exist and
                use_shapetextstyles_if_not_exist is False.
        """
        if self.has(name):
            return self._styles[name].copy()
        if not use_shapetextstyles_if_not_exist:
            raise ValueError('Theme style name "' + name + '" does not exist.')
        return self._shapetextstyles.get(name)

    @error_handler
    def list(self) -> List[str]:
        """List all existing arc text style names.

        Returns:
            List[str]: List of arc text style names.
        """
        return list_(self._styles.keys())

    @error_handler
    def set(self, style: ShapeTextStyle, name: str = "") -> None:
        """Set or update an arc text style with the given name.

        Args:
            style (ShapeTextStyle): The ShapeTextStyle object to cache.
            name (str, optional): Name of the arc text style. Defaults to "".

        Raises:
            ValueError: If the style is invalid or name is not a string.
        """
        style_validator.validate_shapetextstyle("style", style)
        type_validator.validate_str("name", name)
        self._styles[name] = style.copy()
        self._callback_set(name)

    @error_handler
    def delete(self, name: str) -> None:
        """Delete an arc text style by name.

        Args:
            name (str): Name of the arc text style to delete.

        Raises:
            ValueError: If the arc text style with the specified name does not exist.
        """
        if not self.has(name):
            raise ValueError('Theme style name "' + name + '" does not exist.')
        del self._styles[name]
        self._callback_delete(name)

    @error_handler
    def merge(self, style: ShapeTextStyle, targets: Optional[List[str]] = None) -> None:
        """Merge an arc text style into existing arc text styles.

        Args:
            style (ShapeTextStyle): The ShapeTextStyle object to merge.
            targets (Optional[List[str]], optional): List of target arc text style names to merge into.
                If None, merge into all existing arc text styles. Defaults to None.

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


class CircleTextStyleCache(AbstractStyleCache):
    """Cache for managing circle text styles.

    This class provides methods to manage and manipulate ShapeTextStyle objects
    specifically tailored for circle within a cache.
    """

    def __init__(
        self,
        shapetextstyles: ShapeTextStyleCache,
        callback_set: Callable[
            [
                str,
            ],
            None,
        ],
        callback_delete: Callable[
            [
                str,
            ],
            None,
        ],
    ) -> None:
        """Initialize CircleTextStyleCache.

        Args:
            shapetextstyles (ShapeTextStyleCache): Cache of shape text styles to use as fallback.
            callback_set: Callback function for set operation.
            callback_delete: Callback function for delete operation.
        """
        self._callback_set = callback_set
        self._callback_delete = callback_delete
        self._styles: Dict[str, ShapeTextStyle] = {}
        self._shapetextstyles = shapetextstyles

    @error_handler
    def has(self, name: str) -> bool:
        """Check if an circle text style exists by name.

        Args:
            name (str): Name of the circle text style.

        Returns:
            bool: True if the circle text style exists, False otherwise.
        """
        return name in self._styles

    @error_handler
    def get(self, name: str = "", use_shapetextstyles_if_not_exist: bool = True) -> ShapeTextStyle:
        """Retrieve an circle text style by name.

        Args:
            name (str, optional): Name of the circle text style to retrieve. Defaults to "".
            use_shapetextstyles_if_not_exist (bool, optional): Whether to fallback to ShapeTextStyleCache if
                the style does not exist in _styles. Defaults to True.

        Returns:
            ShapeTextStyle: The retrieved ShapeTextStyle object.

        Raises:
            ValueError: If the circle text style with the specified name does not exist and
                use_shapetextstyles_if_not_exist is False.
        """
        if self.has(name):
            return self._styles[name].copy()
        if not use_shapetextstyles_if_not_exist:
            raise ValueError('Theme style name "' + name + '" does not exist.')
        return self._shapetextstyles.get(name)

    @error_handler
    def list(self) -> List[str]:
        """List all existing circle text style names.

        Returns:
            List[str]: List of circle text style names.
        """
        return list_(self._styles.keys())

    @error_handler
    def set(self, style: ShapeTextStyle, name: str = "") -> None:
        """Set or update an circle text style with the given name.

        Args:
            style (ShapeTextStyle): The ShapeTextStyle object to cache.
            name (str, optional): Name of the circle text style. Defaults to "".

        Raises:
            ValueError: If the style is invalid or name is not a string.
        """
        style_validator.validate_shapetextstyle("style", style)
        type_validator.validate_str("name", name)
        self._styles[name] = style.copy()
        self._callback_set(name)

    @error_handler
    def delete(self, name: str) -> None:
        """Delete an circle text style by name.

        Args:
            name (str): Name of the circle text style to delete.

        Raises:
            ValueError: If the circle text style with the specified name does not exist.
        """
        if not self.has(name):
            raise ValueError('Theme style name "' + name + '" does not exist.')
        del self._styles[name]
        self._callback_delete(name)

    @error_handler
    def merge(self, style: ShapeTextStyle, targets: Optional[List[str]] = None) -> None:
        """Merge an circle text style into existing circle text styles.

        Args:
            style (ShapeTextStyle): The ShapeTextStyle object to merge.
            targets (Optional[List[str]], optional): List of target circle text style names to merge into.
                If None, merge into all existing circle text styles. Defaults to None.

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


class DonutsTextStyleCache(AbstractStyleCache):
    """Cache for managing donuts text styles.

    This class provides methods to manage and manipulate ShapeTextStyle objects
    specifically tailored for donuts within a cache.
    """

    def __init__(
        self,
        shapetextstyles: ShapeTextStyleCache,
        callback_set: Callable[
            [
                str,
            ],
            None,
        ],
        callback_delete: Callable[
            [
                str,
            ],
            None,
        ],
    ) -> None:
        """Initialize DonutsTextStyleCache.

        Args:
            shapetextstyles (ShapeTextStyleCache): Cache of shape text styles to use as fallback.
            callback_set: Callback function for set operation.
            callback_delete: Callback function for delete operation.
        """
        self._callback_set = callback_set
        self._callback_delete = callback_delete
        self._styles: Dict[str, ShapeTextStyle] = {}
        self._shapetextstyles = shapetextstyles

    @error_handler
    def has(self, name: str) -> bool:
        """Check if an donuts text style exists by name.

        Args:
            name (str): Name of the donuts text style.

        Returns:
            bool: True if the donuts text style exists, False otherwise.
        """
        return name in self._styles

    @error_handler
    def get(self, name: str = "", use_shapetextstyles_if_not_exist: bool = True) -> ShapeTextStyle:
        """Retrieve an donuts text style by name.

        Args:
            name (str, optional): Name of the donuts text style to retrieve. Defaults to "".
            use_shapetextstyles_if_not_exist (bool, optional): Whether to fallback to ShapeTextStyleCache if
                the style does not exist in _styles. Defaults to True.

        Returns:
            ShapeTextStyle: The retrieved ShapeTextStyle object.

        Raises:
            ValueError: If the donuts text style with the specified name does not exist and
                use_shapetextstyles_if_not_exist is False.
        """
        if self.has(name):
            return self._styles[name].copy()
        if not use_shapetextstyles_if_not_exist:
            raise ValueError('Theme style name "' + name + '" does not exist.')
        return self._shapetextstyles.get(name)

    @error_handler
    def list(self) -> List[str]:
        """List all existing donuts text style names.

        Returns:
            List[str]: List of donuts text style names.
        """
        return list_(self._styles.keys())

    @error_handler
    def set(self, style: ShapeTextStyle, name: str = "") -> None:
        """Set or update an donuts text style with the given name.

        Args:
            style (ShapeTextStyle): The ShapeTextStyle object to cache.
            name (str, optional): Name of the donuts text style. Defaults to "".

        Raises:
            ValueError: If the style is invalid or name is not a string.
        """
        style_validator.validate_shapetextstyle("style", style)
        type_validator.validate_str("name", name)
        self._styles[name] = style.copy()
        self._callback_set(name)

    @error_handler
    def delete(self, name: str) -> None:
        """Delete an donuts text style by name.

        Args:
            name (str): Name of the donuts text style to delete.

        Raises:
            ValueError: If the donuts text style with the specified name does not exist.
        """
        if not self.has(name):
            raise ValueError('Theme style name "' + name + '" does not exist.')
        del self._styles[name]
        self._callback_delete(name)

    @error_handler
    def merge(self, style: ShapeTextStyle, targets: Optional[List[str]] = None) -> None:
        """Merge an donuts text style into existing donuts text styles.

        Args:
            style (ShapeTextStyle): The ShapeTextStyle object to merge.
            targets (Optional[List[str]], optional): List of target donuts text style names to merge into.
                If None, merge into all existing donuts text styles. Defaults to None.

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


class EllipseTextStyleCache(AbstractStyleCache):
    """Cache for managing ellipse text styles.

    This class provides methods to manage and manipulate ShapeTextStyle objects
    specifically tailored for ellipse within a cache.
    """

    def __init__(
        self,
        shapetextstyles: ShapeTextStyleCache,
        callback_set: Callable[
            [
                str,
            ],
            None,
        ],
        callback_delete: Callable[
            [
                str,
            ],
            None,
        ],
    ) -> None:
        """Initialize EllipseTextStyleCache.

        Args:
            shapetextstyles (ShapeTextStyleCache): Cache of shape text styles to use as fallback.
            callback_set: Callback function for set operation.
            callback_delete: Callback function for delete operation.
        """
        self._callback_set = callback_set
        self._callback_delete = callback_delete
        self._styles: Dict[str, ShapeTextStyle] = {}
        self._shapetextstyles = shapetextstyles

    @error_handler
    def has(self, name: str) -> bool:
        """Check if an ellipse text style exists by name.

        Args:
            name (str): Name of the ellipse text style.

        Returns:
            bool: True if the ellipse text style exists, False otherwise.
        """
        return name in self._styles

    @error_handler
    def get(self, name: str = "", use_shapetextstyles_if_not_exist: bool = True) -> ShapeTextStyle:
        """Retrieve an ellipse text style by name.

        Args:
            name (str, optional): Name of the ellipse text style to retrieve. Defaults to "".
            use_shapetextstyles_if_not_exist (bool, optional): Whether to fallback to ShapeTextStyleCache if
                the style does not exist in _styles. Defaults to True.

        Returns:
            ShapeTextStyle: The retrieved ShapeTextStyle object.

        Raises:
            ValueError: If the ellipse text style with the specified name does not exist and
                use_shapetextstyles_if_not_exist is False.
        """
        if self.has(name):
            return self._styles[name].copy()
        if not use_shapetextstyles_if_not_exist:
            raise ValueError('Theme style name "' + name + '" does not exist.')
        return self._shapetextstyles.get(name)

    @error_handler
    def list(self) -> List[str]:
        """List all existing ellipse text style names.

        Returns:
            List[str]: List of ellipse text style names.
        """
        return list_(self._styles.keys())

    @error_handler
    def set(self, style: ShapeTextStyle, name: str = "") -> None:
        """Set or update an ellipse text style with the given name.

        Args:
            style (ShapeTextStyle): The ShapeTextStyle object to cache.
            name (str, optional): Name of the ellipse text style. Defaults to "".

        Raises:
            ValueError: If the style is invalid or name is not a string.
        """
        style_validator.validate_shapetextstyle("style", style)
        type_validator.validate_str("name", name)
        self._styles[name] = style.copy()
        self._callback_set(name)

    @error_handler
    def delete(self, name: str) -> None:
        """Delete an ellipse text style by name.

        Args:
            name (str): Name of the ellipse text style to delete.

        Raises:
            ValueError: If the ellipse text style with the specified name does not exist.
        """
        if not self.has(name):
            raise ValueError('Theme style name "' + name + '" does not exist.')
        del self._styles[name]
        self._callback_delete(name)

    @error_handler
    def merge(self, style: ShapeTextStyle, targets: Optional[List[str]] = None) -> None:
        """Merge an ellipse text style into existing ellipse text styles.

        Args:
            style (ShapeTextStyle): The ShapeTextStyle object to merge.
            targets (Optional[List[str]], optional): List of target ellipse text style names to merge into.
                If None, merge into all existing ellipse text styles. Defaults to None.

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


class FanTextStyleCache(AbstractStyleCache):
    """Cache for managing fan text styles.

    This class provides methods to manage and manipulate ShapeTextStyle objects
    specifically tailored for fan within a cache.
    """

    def __init__(
        self,
        shapetextstyles: ShapeTextStyleCache,
        callback_set: Callable[
            [
                str,
            ],
            None,
        ],
        callback_delete: Callable[
            [
                str,
            ],
            None,
        ],
    ) -> None:
        """Initialize FanTextStyleCache.

        Args:
            shapetextstyles (ShapeTextStyleCache): Cache of shape text styles to use as fallback.
            callback_set: Callback function for set operation.
            callback_delete: Callback function for delete operation.
        """
        self._callback_set = callback_set
        self._callback_delete = callback_delete
        self._styles: Dict[str, ShapeTextStyle] = {}
        self._shapetextstyles = shapetextstyles

    @error_handler
    def has(self, name: str) -> bool:
        """Check if an fan text style exists by name.

        Args:
            name (str): Name of the fan text style.

        Returns:
            bool: True if the fan text style exists, False otherwise.
        """
        return name in self._styles

    @error_handler
    def get(self, name: str = "", use_shapetextstyles_if_not_exist: bool = True) -> ShapeTextStyle:
        """Retrieve an fan text style by name.

        Args:
            name (str, optional): Name of the fan text style to retrieve. Defaults to "".
            use_shapetextstyles_if_not_exist (bool, optional): Whether to fallback to ShapeTextStyleCache if
                the style does not exist in _styles. Defaults to True.

        Returns:
            ShapeTextStyle: The retrieved ShapeTextStyle object.

        Raises:
            ValueError: If the fan text style with the specified name does not exist and
                use_shapetextstyles_if_not_exist is False.
        """
        if self.has(name):
            return self._styles[name].copy()
        if not use_shapetextstyles_if_not_exist:
            raise ValueError('Theme style name "' + name + '" does not exist.')
        return self._shapetextstyles.get(name)

    @error_handler
    def list(self) -> List[str]:
        """List all existing fan text style names.

        Returns:
            List[str]: List of fan text style names.
        """
        return list_(self._styles.keys())

    @error_handler
    def set(self, style: ShapeTextStyle, name: str = "") -> None:
        """Set or update an fan text style with the given name.

        Args:
            style (ShapeTextStyle): The ShapeTextStyle object to cache.
            name (str, optional): Name of the fan text style. Defaults to "".

        Raises:
            ValueError: If the style is invalid or name is not a string.
        """
        style_validator.validate_shapetextstyle("style", style)
        type_validator.validate_str("name", name)
        self._styles[name] = style.copy()
        self._callback_set(name)

    @error_handler
    def delete(self, name: str) -> None:
        """Delete an fan text style by name.

        Args:
            name (str): Name of the fan text style to delete.

        Raises:
            ValueError: If the fan text style with the specified name does not exist.
        """
        if not self.has(name):
            raise ValueError('Theme style name "' + name + '" does not exist.')
        del self._styles[name]
        self._callback_delete(name)

    @error_handler
    def merge(self, style: ShapeTextStyle, targets: Optional[List[str]] = None) -> None:
        """Merge an fan text style into existing fan text styles.

        Args:
            style (ShapeTextStyle): The ShapeTextStyle object to merge.
            targets (Optional[List[str]], optional): List of target fan text style names to merge into.
                If None, merge into all existing fan text styles. Defaults to None.

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


class PolygonTextStyleCache(AbstractStyleCache):
    """Cache for managing polygon text styles.

    This class provides methods to manage and manipulate ShapeTextStyle objects
    specifically tailored for polygon within a cache.
    """

    def __init__(
        self,
        shapetextstyles: ShapeTextStyleCache,
        callback_set: Callable[
            [
                str,
            ],
            None,
        ],
        callback_delete: Callable[
            [
                str,
            ],
            None,
        ],
    ) -> None:
        """Initialize PolygonTextStyleCache.

        Args:
            shapetextstyles (ShapeTextStyleCache): Cache of shape text styles to use as fallback.
            callback_set: Callback function for set operation.
            callback_delete: Callback function for delete operation.
        """
        self._callback_set = callback_set
        self._callback_delete = callback_delete
        self._styles: Dict[str, ShapeTextStyle] = {}
        self._shapetextstyles = shapetextstyles

    @error_handler
    def has(self, name: str) -> bool:
        """Check if an polygon text style exists by name.

        Args:
            name (str): Name of the polygon text style.

        Returns:
            bool: True if the polygon text style exists, False otherwise.
        """
        return name in self._styles

    @error_handler
    def get(self, name: str = "", use_shapetextstyles_if_not_exist: bool = True) -> ShapeTextStyle:
        """Retrieve an polygon text style by name.

        Args:
            name (str, optional): Name of the polygon text style to retrieve. Defaults to "".
            use_shapetextstyles_if_not_exist (bool, optional): Whether to fallback to ShapeTextStyleCache if
                the style does not exist in _styles. Defaults to True.

        Returns:
            ShapeTextStyle: The retrieved ShapeTextStyle object.

        Raises:
            ValueError: If the polygon text style with the specified name does not exist and
                use_shapetextstyles_if_not_exist is False.
        """
        if self.has(name):
            return self._styles[name].copy()
        if not use_shapetextstyles_if_not_exist:
            raise ValueError('Theme style name "' + name + '" does not exist.')
        return self._shapetextstyles.get(name)

    @error_handler
    def list(self) -> List[str]:
        """List all existing polygon text style names.

        Returns:
            List[str]: List of polygon text style names.
        """
        return list_(self._styles.keys())

    @error_handler
    def set(self, style: ShapeTextStyle, name: str = "") -> None:
        """Set or update an polygon text style with the given name.

        Args:
            style (ShapeTextStyle): The ShapeTextStyle object to cache.
            name (str, optional): Name of the polygon text style. Defaults to "".

        Raises:
            ValueError: If the style is invalid or name is not a string.
        """
        style_validator.validate_shapetextstyle("style", style)
        type_validator.validate_str("name", name)
        self._styles[name] = style.copy()
        self._callback_set(name)

    @error_handler
    def delete(self, name: str) -> None:
        """Delete an polygon text style by name.

        Args:
            name (str): Name of the polygon text style to delete.

        Raises:
            ValueError: If the polygon text style with the specified name does not exist.
        """
        if not self.has(name):
            raise ValueError('Theme style name "' + name + '" does not exist.')
        del self._styles[name]
        self._callback_delete(name)

    @error_handler
    def merge(self, style: ShapeTextStyle, targets: Optional[List[str]] = None) -> None:
        """Merge an polygon text style into existing polygon text styles.

        Args:
            style (ShapeTextStyle): The ShapeTextStyle object to merge.
            targets (Optional[List[str]], optional): List of target polygon text style names to merge into.
                If None, merge into all existing polygon text styles. Defaults to None.

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


class RectangleTextStyleCache(AbstractStyleCache):
    """Cache for managing rectangle text styles.

    This class provides methods to manage and manipulate ShapeTextStyle objects
    specifically tailored for rectangle within a cache.
    """

    def __init__(
        self,
        shapetextstyles: ShapeTextStyleCache,
        callback_set: Callable[
            [
                str,
            ],
            None,
        ],
        callback_delete: Callable[
            [
                str,
            ],
            None,
        ],
    ) -> None:
        """Initialize RectangleTextStyleCache.

        Args:
            shapetextstyles (ShapeTextStyleCache): Cache of shape text styles to use as fallback.
            callback_set: Callback function for set operation.
            callback_delete: Callback function for delete operation.
        """
        self._callback_set = callback_set
        self._callback_delete = callback_delete
        self._styles: Dict[str, ShapeTextStyle] = {}
        self._shapetextstyles = shapetextstyles

    @error_handler
    def has(self, name: str) -> bool:
        """Check if an rectangle text style exists by name.

        Args:
            name (str): Name of the rectangle text style.

        Returns:
            bool: True if the rectangle text style exists, False otherwise.
        """
        return name in self._styles

    @error_handler
    def get(self, name: str = "", use_shapetextstyles_if_not_exist: bool = True) -> ShapeTextStyle:
        """Retrieve an rectangle text style by name.

        Args:
            name (str, optional): Name of the rectangle text style to retrieve. Defaults to "".
            use_shapetextstyles_if_not_exist (bool, optional): Whether to fallback to ShapeTextStyleCache if
                the style does not exist in _styles. Defaults to True.

        Returns:
            ShapeTextStyle: The retrieved ShapeTextStyle object.

        Raises:
            ValueError: If the rectangle text style with the specified name does not exist and
                use_shapetextstyles_if_not_exist is False.
        """
        if self.has(name):
            return self._styles[name].copy()
        if not use_shapetextstyles_if_not_exist:
            raise ValueError('Theme style name "' + name + '" does not exist.')
        return self._shapetextstyles.get(name)

    @error_handler
    def list(self) -> List[str]:
        """List all existing rectangle text style names.

        Returns:
            List[str]: List of rectangle text style names.
        """
        return list_(self._styles.keys())

    @error_handler
    def set(self, style: ShapeTextStyle, name: str = "") -> None:
        """Set or update an rectangle text style with the given name.

        Args:
            style (ShapeTextStyle): The ShapeTextStyle object to cache.
            name (str, optional): Name of the rectangle text style. Defaults to "".

        Raises:
            ValueError: If the style is invalid or name is not a string.
        """
        style_validator.validate_shapetextstyle("style", style)
        type_validator.validate_str("name", name)
        self._styles[name] = style.copy()
        self._callback_set(name)

    @error_handler
    def delete(self, name: str) -> None:
        """Delete an rectangle text style by name.

        Args:
            name (str): Name of the rectangle text style to delete.

        Raises:
            ValueError: If the rectangle text style with the specified name does not exist.
        """
        if not self.has(name):
            raise ValueError('Theme style name "' + name + '" does not exist.')
        del self._styles[name]
        self._callback_delete(name)

    @error_handler
    def merge(self, style: ShapeTextStyle, targets: Optional[List[str]] = None) -> None:
        """Merge an rectangle text style into existing rectangle text styles.

        Args:
            style (ShapeTextStyle): The ShapeTextStyle object to merge.
            targets (Optional[List[str]], optional): List of target rectangle text style names to merge into.
                If None, merge into all existing rectangle text styles. Defaults to None.

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


class RegularpolygonTextStyleCache(AbstractStyleCache):
    """Cache for managing regular polygon text styles.

    This class provides methods to manage and manipulate ShapeTextStyle objects
    specifically tailored for regular polygon within a cache.
    """

    def __init__(
        self,
        shapetextstyles: ShapeTextStyleCache,
        callback_set: Callable[
            [
                str,
            ],
            None,
        ],
        callback_delete: Callable[
            [
                str,
            ],
            None,
        ],
    ) -> None:
        """Initialize RegularpolygonTextStyleCache.

        Args:
            shapetextstyles (ShapeTextStyleCache): Cache of shape text styles to use as fallback.
            callback_set: Callback function for set operation.
            callback_delete: Callback function for delete operation.
        """
        self._callback_set = callback_set
        self._callback_delete = callback_delete
        self._styles: Dict[str, ShapeTextStyle] = {}
        self._shapetextstyles = shapetextstyles

    @error_handler
    def has(self, name: str) -> bool:
        """Check if an regular polygon text style exists by name.

        Args:
            name (str): Name of the regular polygon text style.

        Returns:
            bool: True if the regular polygon text style exists, False otherwise.
        """
        return name in self._styles

    @error_handler
    def get(self, name: str = "", use_shapetextstyles_if_not_exist: bool = True) -> ShapeTextStyle:
        """Retrieve an regular polygon text style by name.

        Args:
            name (str, optional): Name of the regular polygon text style to retrieve. Defaults to "".
            use_shapetextstyles_if_not_exist (bool, optional): Whether to fallback to ShapeTextStyleCache if
                the style does not exist in _styles. Defaults to True.

        Returns:
            ShapeTextStyle: The retrieved ShapeTextStyle object.

        Raises:
            ValueError: If the regular polygon text style with the specified name does not exist and
                use_shapetextstyles_if_not_exist is False.
        """
        if self.has(name):
            return self._styles[name].copy()
        if not use_shapetextstyles_if_not_exist:
            raise ValueError('Theme style name "' + name + '" does not exist.')
        return self._shapetextstyles.get(name)

    @error_handler
    def list(self) -> List[str]:
        """List all existing regular polygon text style names.

        Returns:
            List[str]: List of regular polygon text style names.
        """
        return list_(self._styles.keys())

    @error_handler
    def set(self, style: ShapeTextStyle, name: str = "") -> None:
        """Set or update an regular polygon text style with the given name.

        Args:
            style (ShapeTextStyle): The ShapeTextStyle object to cache.
            name (str, optional): Name of the regular polygon text style. Defaults to "".

        Raises:
            ValueError: If the style is invalid or name is not a string.
        """
        style_validator.validate_shapetextstyle("style", style)
        type_validator.validate_str("name", name)
        self._styles[name] = style.copy()
        self._callback_set(name)

    @error_handler
    def delete(self, name: str) -> None:
        """Delete an regular polygon text style by name.

        Args:
            name (str): Name of the regular polygon text style to delete.

        Raises:
            ValueError: If the regular polygon text style with the specified name does not exist.
        """
        if not self.has(name):
            raise ValueError('Theme style name "' + name + '" does not exist.')
        del self._styles[name]
        self._callback_delete(name)

    @error_handler
    def merge(self, style: ShapeTextStyle, targets: Optional[List[str]] = None) -> None:
        """Merge an regular polygon text style into existing regular polygon text styles.

        Args:
            style (ShapeTextStyle): The ShapeTextStyle object to merge.
            targets (Optional[List[str]], optional): List of target regular polygon text style names to merge into.
                If None, merge into all existing regular polygon text styles. Defaults to None.

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


class WedgeTextStyleCache(AbstractStyleCache):
    """Cache for managing wedge text styles.

    This class provides methods to manage and manipulate ShapeTextStyle objects
    specifically tailored for wedge within a cache.
    """

    def __init__(
        self,
        shapetextstyles: ShapeTextStyleCache,
        callback_set: Callable[
            [
                str,
            ],
            None,
        ],
        callback_delete: Callable[
            [
                str,
            ],
            None,
        ],
    ) -> None:
        """Initialize WedgeTextStyleCache.

        Args:
            shapetextstyles (ShapeTextStyleCache): Cache of shape text styles to use as fallback.
            callback_set: Callback function for set operation.
            callback_delete: Callback function for delete operation.
        """
        self._callback_set = callback_set
        self._callback_delete = callback_delete
        self._styles: Dict[str, ShapeTextStyle] = {}
        self._shapetextstyles = shapetextstyles

    @error_handler
    def has(self, name: str) -> bool:
        """Check if an wedge text style exists by name.

        Args:
            name (str): Name of the wedge text style.

        Returns:
            bool: True if the wedge text style exists, False otherwise.
        """
        return name in self._styles

    @error_handler
    def get(self, name: str = "", use_shapetextstyles_if_not_exist: bool = True) -> ShapeTextStyle:
        """Retrieve an wedge text style by name.

        Args:
            name (str, optional): Name of the wedge text style to retrieve. Defaults to "".
            use_shapetextstyles_if_not_exist (bool, optional): Whether to fallback to ShapeTextStyleCache if
                the style does not exist in _styles. Defaults to True.

        Returns:
            ShapeTextStyle: The retrieved ShapeTextStyle object.

        Raises:
            ValueError: If the wedge text style with the specified name does not exist and
                use_shapetextstyles_if_not_exist is False.
        """
        if self.has(name):
            return self._styles[name].copy()
        if not use_shapetextstyles_if_not_exist:
            raise ValueError('Theme style name "' + name + '" does not exist.')
        return self._shapetextstyles.get(name)

    @error_handler
    def list(self) -> List[str]:
        """List all existing wedge text style names.

        Returns:
            List[str]: List of wedge text style names.
        """
        return list_(self._styles.keys())

    @error_handler
    def set(self, style: ShapeTextStyle, name: str = "") -> None:
        """Set or update an wedge text style with the given name.

        Args:
            style (ShapeTextStyle): The ShapeTextStyle object to cache.
            name (str, optional): Name of the wedge text style. Defaults to "".

        Raises:
            ValueError: If the style is invalid or name is not a string.
        """
        style_validator.validate_shapetextstyle("style", style)
        type_validator.validate_str("name", name)
        self._styles[name] = style.copy()
        self._callback_set(name)

    @error_handler
    def delete(self, name: str) -> None:
        """Delete an wedge text style by name.

        Args:
            name (str): Name of the wedge text style to delete.

        Raises:
            ValueError: If the wedge text style with the specified name does not exist.
        """
        if not self.has(name):
            raise ValueError('Theme style name "' + name + '" does not exist.')
        del self._styles[name]
        self._callback_delete(name)

    @error_handler
    def merge(self, style: ShapeTextStyle, targets: Optional[List[str]] = None) -> None:
        """Merge an wedge text style into existing wedge text styles.

        Args:
            style (ShapeTextStyle): The ShapeTextStyle object to merge.
            targets (Optional[List[str]], optional): List of target wedge text style names to merge into.
                If None, merge into all existing wedge text styles. Defaults to None.

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


class ArrowTextStyleCache(AbstractStyleCache):
    """Cache for managing arrow text styles.

    This class provides methods to manage and manipulate ShapeTextStyle objects
    specifically tailored for arrow within a cache.
    """

    def __init__(
        self,
        shapetextstyles: ShapeTextStyleCache,
        callback_set: Callable[
            [
                str,
            ],
            None,
        ],
        callback_delete: Callable[
            [
                str,
            ],
            None,
        ],
    ) -> None:
        """Initialize ArrowTextStyleCache.

        Args:
            shapetextstyles (ShapeTextStyleCache): Cache of shape text styles to use as fallback.
            callback_set: Callback function for set operation.
            callback_delete: Callback function for delete operation.
        """
        self._callback_set = callback_set
        self._callback_delete = callback_delete
        self._styles: Dict[str, ShapeTextStyle] = {}
        self._shapetextstyles = shapetextstyles

    @error_handler
    def has(self, name: str) -> bool:
        """Check if an arrow text style exists by name.

        Args:
            name (str): Name of the arrow text style.

        Returns:
            bool: True if the arrow text style exists, False otherwise.
        """
        return name in self._styles

    @error_handler
    def get(self, name: str = "", use_shapetextstyles_if_not_exist: bool = True) -> ShapeTextStyle:
        """Retrieve an arrow text style by name.

        Args:
            name (str, optional): Name of the arrow text style to retrieve. Defaults to "".
            use_shapetextstyles_if_not_exist (bool, optional): Whether to fallback to ShapeTextStyleCache if
                the style does not exist in _styles. Defaults to True.

        Returns:
            ShapeTextStyle: The retrieved ShapeTextStyle object.

        Raises:
            ValueError: If the arrow text style with the specified name does not exist and
                use_shapetextstyles_if_not_exist is False.
        """
        if self.has(name):
            return self._styles[name].copy()
        if not use_shapetextstyles_if_not_exist:
            raise ValueError('Theme style name "' + name + '" does not exist.')
        return self._shapetextstyles.get(name)

    @error_handler
    def list(self) -> List[str]:
        """List all existing arrow text style names.

        Returns:
            List[str]: List of arrow text style names.
        """
        return list_(self._styles.keys())

    @error_handler
    def set(self, style: ShapeTextStyle, name: str = "") -> None:
        """Set or update an arrow text style with the given name.

        Args:
            style (ShapeTextStyle): The ShapeTextStyle object to cache.
            name (str, optional): Name of the arrow text style. Defaults to "".

        Raises:
            ValueError: If the style is invalid or name is not a string.
        """
        style_validator.validate_shapetextstyle("style", style)
        type_validator.validate_str("name", name)
        self._styles[name] = style.copy()
        self._callback_set(name)

    @error_handler
    def delete(self, name: str) -> None:
        """Delete an arrow text style by name.

        Args:
            name (str): Name of the arrow text style to delete.

        Raises:
            ValueError: If the arrow text style with the specified name does not exist.
        """
        if not self.has(name):
            raise ValueError('Theme style name "' + name + '" does not exist.')
        del self._styles[name]
        self._callback_delete(name)

    @error_handler
    def merge(self, style: ShapeTextStyle, targets: Optional[List[str]] = None) -> None:
        """Merge an arrow text style into existing arrow text styles.

        Args:
            style (ShapeTextStyle): The ShapeTextStyle object to merge.
            targets (Optional[List[str]], optional): List of target arrow text style names to merge into.
                If None, merge into all existing arrow text styles. Defaults to None.

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


class ChevronTextStyleCache(AbstractStyleCache):
    """Cache for managing chevron text styles.

    This class provides methods to manage and manipulate ShapeTextStyle objects
    specifically tailored for chevron within a cache.
    """

    def __init__(
        self,
        shapetextstyles: ShapeTextStyleCache,
        callback_set: Callable[
            [
                str,
            ],
            None,
        ],
        callback_delete: Callable[
            [
                str,
            ],
            None,
        ],
    ) -> None:
        """Initialize ChevronTextStyleCache.

        Args:
            shapetextstyles (ShapeTextStyleCache): Cache of shape text styles to use as fallback.
            callback_set: Callback function for set operation.
            callback_delete: Callback function for delete operation.
        """
        self._callback_set = callback_set
        self._callback_delete = callback_delete
        self._styles: Dict[str, ShapeTextStyle] = {}
        self._shapetextstyles = shapetextstyles

    @error_handler
    def has(self, name: str) -> bool:
        """Check if an chevron text style exists by name.

        Args:
            name (str): Name of the chevron text style.

        Returns:
            bool: True if the chevron text style exists, False otherwise.
        """
        return name in self._styles

    @error_handler
    def get(self, name: str = "", use_shapetextstyles_if_not_exist: bool = True) -> ShapeTextStyle:
        """Retrieve an chevron text style by name.

        Args:
            name (str, optional): Name of the chevron text style to retrieve. Defaults to "".
            use_shapetextstyles_if_not_exist (bool, optional): Whether to fallback to ShapeTextStyleCache if
                the style does not exist in _styles. Defaults to True.

        Returns:
            ShapeTextStyle: The retrieved ShapeTextStyle object.

        Raises:
            ValueError: If the chevron text style with the specified name does not exist and
                use_shapetextstyles_if_not_exist is False.
        """
        if self.has(name):
            return self._styles[name].copy()
        if not use_shapetextstyles_if_not_exist:
            raise ValueError('Theme style name "' + name + '" does not exist.')
        return self._shapetextstyles.get(name)

    @error_handler
    def list(self) -> List[str]:
        """List all existing chevron text style names.

        Returns:
            List[str]: List of chevron text style names.
        """
        return list_(self._styles.keys())

    @error_handler
    def set(self, style: ShapeTextStyle, name: str = "") -> None:
        """Set or update an chevron text style with the given name.

        Args:
            style (ShapeTextStyle): The ShapeTextStyle object to cache.
            name (str, optional): Name of the chevron text style. Defaults to "".

        Raises:
            ValueError: If the style is invalid or name is not a string.
        """
        style_validator.validate_shapetextstyle("style", style)
        type_validator.validate_str("name", name)
        self._styles[name] = style.copy()
        self._callback_set(name)

    @error_handler
    def delete(self, name: str) -> None:
        """Delete an chevron text style by name.

        Args:
            name (str): Name of the chevron text style to delete.

        Raises:
            ValueError: If the chevron text style with the specified name does not exist.
        """
        if not self.has(name):
            raise ValueError('Theme style name "' + name + '" does not exist.')
        del self._styles[name]
        self._callback_delete(name)

    @error_handler
    def merge(self, style: ShapeTextStyle, targets: Optional[List[str]] = None) -> None:
        """Merge an chevron text style into existing chevron text styles.

        Args:
            style (ShapeTextStyle): The ShapeTextStyle object to merge.
            targets (Optional[List[str]], optional): List of target chevron text style names to merge into.
                If None, merge into all existing chevron text styles. Defaults to None.

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


class ParallelogramTextStyleCache(AbstractStyleCache):
    """Cache for managing parallelogram text styles.

    This class provides methods to manage and manipulate ShapeTextStyle objects
    specifically tailored for parallelogram within a cache.
    """

    def __init__(
        self,
        shapetextstyles: ShapeTextStyleCache,
        callback_set: Callable[
            [
                str,
            ],
            None,
        ],
        callback_delete: Callable[
            [
                str,
            ],
            None,
        ],
    ) -> None:
        """Initialize ParallelogramTextStyleCache.

        Args:
            shapetextstyles (ShapeTextStyleCache): Cache of shape text styles to use as fallback.
            callback_set: Callback function for set operation.
            callback_delete: Callback function for delete operation.
        """
        self._callback_set = callback_set
        self._callback_delete = callback_delete
        self._styles: Dict[str, ShapeTextStyle] = {}
        self._shapetextstyles = shapetextstyles

    @error_handler
    def has(self, name: str) -> bool:
        """Check if an parallelogram text style exists by name.

        Args:
            name (str): Name of the parallelogram text style.

        Returns:
            bool: True if the parallelogram text style exists, False otherwise.
        """
        return name in self._styles

    @error_handler
    def get(self, name: str = "", use_shapetextstyles_if_not_exist: bool = True) -> ShapeTextStyle:
        """Retrieve an parallelogram text style by name.

        Args:
            name (str, optional): Name of the parallelogram text style to retrieve. Defaults to "".
            use_shapetextstyles_if_not_exist (bool, optional): Whether to fallback to ShapeTextStyleCache if
                the style does not exist in _styles. Defaults to True.

        Returns:
            ShapeTextStyle: The retrieved ShapeTextStyle object.

        Raises:
            ValueError: If the parallelogram text style with the specified name does not exist and
                use_shapetextstyles_if_not_exist is False.
        """
        if self.has(name):
            return self._styles[name].copy()
        if not use_shapetextstyles_if_not_exist:
            raise ValueError('Theme style name "' + name + '" does not exist.')
        return self._shapetextstyles.get(name)

    @error_handler
    def list(self) -> List[str]:
        """List all existing parallelogram text style names.

        Returns:
            List[str]: List of parallelogram text style names.
        """
        return list_(self._styles.keys())

    @error_handler
    def set(self, style: ShapeTextStyle, name: str = "") -> None:
        """Set or update an parallelogram text style with the given name.

        Args:
            style (ShapeTextStyle): The ShapeTextStyle object to cache.
            name (str, optional): Name of the parallelogram text style. Defaults to "".

        Raises:
            ValueError: If the style is invalid or name is not a string.
        """
        style_validator.validate_shapetextstyle("style", style)
        type_validator.validate_str("name", name)
        self._styles[name] = style.copy()
        self._callback_set(name)

    @error_handler
    def delete(self, name: str) -> None:
        """Delete an parallelogram text style by name.

        Args:
            name (str): Name of the parallelogram text style to delete.

        Raises:
            ValueError: If the parallelogram text style with the specified name does not exist.
        """
        if not self.has(name):
            raise ValueError('Theme style name "' + name + '" does not exist.')
        del self._styles[name]
        self._callback_delete(name)

    @error_handler
    def merge(self, style: ShapeTextStyle, targets: Optional[List[str]] = None) -> None:
        """Merge an parallelogram text style into existing parallelogram text styles.

        Args:
            style (ShapeTextStyle): The ShapeTextStyle object to merge.
            targets (Optional[List[str]], optional): List of target parallelogram text style names to merge into.
                If None, merge into all existing parallelogram text styles. Defaults to None.

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


class RhombusTextStyleCache(AbstractStyleCache):
    """Cache for managing rhombus text styles.

    This class provides methods to manage and manipulate ShapeTextStyle objects
    specifically tailored for rhombus within a cache.
    """

    def __init__(
        self,
        shapetextstyles: ShapeTextStyleCache,
        callback_set: Callable[
            [
                str,
            ],
            None,
        ],
        callback_delete: Callable[
            [
                str,
            ],
            None,
        ],
    ) -> None:
        """Initialize RhombusTextStyleCache.

        Args:
            shapetextstyles (ShapeTextStyleCache): Cache of shape text styles to use as fallback.
            callback_set: Callback function for set operation.
            callback_delete: Callback function for delete operation.
        """
        self._callback_set = callback_set
        self._callback_delete = callback_delete
        self._styles: Dict[str, ShapeTextStyle] = {}
        self._shapetextstyles = shapetextstyles

    @error_handler
    def has(self, name: str) -> bool:
        """Check if an rhombus text style exists by name.

        Args:
            name (str): Name of the rhombus text style.

        Returns:
            bool: True if the rhombus text style exists, False otherwise.
        """
        return name in self._styles

    @error_handler
    def get(self, name: str = "", use_shapetextstyles_if_not_exist: bool = True) -> ShapeTextStyle:
        """Retrieve an rhombus text style by name.

        Args:
            name (str, optional): Name of the rhombus text style to retrieve. Defaults to "".
            use_shapetextstyles_if_not_exist (bool, optional): Whether to fallback to ShapeTextStyleCache if
                the style does not exist in _styles. Defaults to True.

        Returns:
            ShapeTextStyle: The retrieved ShapeTextStyle object.

        Raises:
            ValueError: If the rhombus text style with the specified name does not exist and
                use_shapetextstyles_if_not_exist is False.
        """
        if self.has(name):
            return self._styles[name].copy()
        if not use_shapetextstyles_if_not_exist:
            raise ValueError('Theme style name "' + name + '" does not exist.')
        return self._shapetextstyles.get(name)

    @error_handler
    def list(self) -> List[str]:
        """List all existing rhombus text style names.

        Returns:
            List[str]: List of rhombus text style names.
        """
        return list_(self._styles.keys())

    @error_handler
    def set(self, style: ShapeTextStyle, name: str = "") -> None:
        """Set or update an rhombus text style with the given name.

        Args:
            style (ShapeTextStyle): The ShapeTextStyle object to cache.
            name (str, optional): Name of the rhombus text style. Defaults to "".

        Raises:
            ValueError: If the style is invalid or name is not a string.
        """
        style_validator.validate_shapetextstyle("style", style)
        type_validator.validate_str("name", name)
        self._styles[name] = style.copy()
        self._callback_set(name)

    @error_handler
    def delete(self, name: str) -> None:
        """Delete an rhombus text style by name.

        Args:
            name (str): Name of the rhombus text style to delete.

        Raises:
            ValueError: If the rhombus text style with the specified name does not exist.
        """
        if not self.has(name):
            raise ValueError('Theme style name "' + name + '" does not exist.')
        del self._styles[name]
        self._callback_delete(name)

    @error_handler
    def merge(self, style: ShapeTextStyle, targets: Optional[List[str]] = None) -> None:
        """Merge an rhombus text style into existing rhombus text styles.

        Args:
            style (ShapeTextStyle): The ShapeTextStyle object to merge.
            targets (Optional[List[str]], optional): List of target rhombus text style names to merge into.
                If None, merge into all existing rhombus text styles. Defaults to None.

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


class StarTextStyleCache(AbstractStyleCache):
    """Cache for managing star text styles.

    This class provides methods to manage and manipulate ShapeTextStyle objects
    specifically tailored for star within a cache.
    """

    def __init__(
        self,
        shapetextstyles: ShapeTextStyleCache,
        callback_set: Callable[
            [
                str,
            ],
            None,
        ],
        callback_delete: Callable[
            [
                str,
            ],
            None,
        ],
    ) -> None:
        """Initialize StarTextStyleCache.

        Args:
            shapetextstyles (ShapeTextStyleCache): Cache of shape text styles to use as fallback.
            callback_set: Callback function for set operation.
            callback_delete: Callback function for delete operation.
        """
        self._callback_set = callback_set
        self._callback_delete = callback_delete
        self._styles: Dict[str, ShapeTextStyle] = {}
        self._shapetextstyles = shapetextstyles

    @error_handler
    def has(self, name: str) -> bool:
        """Check if an star text style exists by name.

        Args:
            name (str): Name of the star text style.

        Returns:
            bool: True if the star text style exists, False otherwise.
        """
        return name in self._styles

    @error_handler
    def get(self, name: str = "", use_shapetextstyles_if_not_exist: bool = True) -> ShapeTextStyle:
        """Retrieve an star text style by name.

        Args:
            name (str, optional): Name of the star text style to retrieve. Defaults to "".
            use_shapetextstyles_if_not_exist (bool, optional): Whether to fallback to ShapeTextStyleCache if
                the style does not exist in _styles. Defaults to True.

        Returns:
            ShapeTextStyle: The retrieved ShapeTextStyle object.

        Raises:
            ValueError: If the star text style with the specified name does not exist and
                use_shapetextstyles_if_not_exist is False.
        """
        if self.has(name):
            return self._styles[name].copy()
        if not use_shapetextstyles_if_not_exist:
            raise ValueError('Theme style name "' + name + '" does not exist.')
        return self._shapetextstyles.get(name)

    @error_handler
    def list(self) -> List[str]:
        """List all existing star text style names.

        Returns:
            List[str]: List of star text style names.
        """
        return list_(self._styles.keys())

    @error_handler
    def set(self, style: ShapeTextStyle, name: str = "") -> None:
        """Set or update an star text style with the given name.

        Args:
            style (ShapeTextStyle): The ShapeTextStyle object to cache.
            name (str, optional): Name of the star text style. Defaults to "".

        Raises:
            ValueError: If the style is invalid or name is not a string.
        """
        style_validator.validate_shapetextstyle("style", style)
        type_validator.validate_str("name", name)
        self._styles[name] = style.copy()
        self._callback_set(name)

    @error_handler
    def delete(self, name: str) -> None:
        """Delete an star text style by name.

        Args:
            name (str): Name of the star text style to delete.

        Raises:
            ValueError: If the star text style with the specified name does not exist.
        """
        if not self.has(name):
            raise ValueError('Theme style name "' + name + '" does not exist.')
        del self._styles[name]
        self._callback_delete(name)

    @error_handler
    def merge(self, style: ShapeTextStyle, targets: Optional[List[str]] = None) -> None:
        """Merge an star text style into existing star text styles.

        Args:
            style (ShapeTextStyle): The ShapeTextStyle object to merge.
            targets (Optional[List[str]], optional): List of target star text style names to merge into.
                If None, merge into all existing star text styles. Defaults to None.

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


class TrapezoidTextStyleCache(AbstractStyleCache):
    """Cache for managing trapezoid text styles.

    This class provides methods to manage and manipulate ShapeTextStyle objects
    specifically tailored for trapezoid within a cache.
    """

    def __init__(
        self,
        shapetextstyles: ShapeTextStyleCache,
        callback_set: Callable[
            [
                str,
            ],
            None,
        ],
        callback_delete: Callable[
            [
                str,
            ],
            None,
        ],
    ) -> None:
        """Initialize TrapezoidTextStyleCache.

        Args:
            shapetextstyles (ShapeTextStyleCache): Cache of shape text styles to use as fallback.
            callback_set: Callback function for set operation.
            callback_delete: Callback function for delete operation.
        """
        self._callback_set = callback_set
        self._callback_delete = callback_delete
        self._styles: Dict[str, ShapeTextStyle] = {}
        self._shapetextstyles = shapetextstyles

    @error_handler
    def has(self, name: str) -> bool:
        """Check if an trapezoid text style exists by name.

        Args:
            name (str): Name of the trapezoid text style.

        Returns:
            bool: True if the trapezoid text style exists, False otherwise.
        """
        return name in self._styles

    @error_handler
    def get(self, name: str = "", use_shapetextstyles_if_not_exist: bool = True) -> ShapeTextStyle:
        """Retrieve an trapezoid text style by name.

        Args:
            name (str, optional): Name of the trapezoid text style to retrieve. Defaults to "".
            use_shapetextstyles_if_not_exist (bool, optional): Whether to fallback to ShapeTextStyleCache if
                the style does not exist in _styles. Defaults to True.

        Returns:
            ShapeTextStyle: The retrieved ShapeTextStyle object.

        Raises:
            ValueError: If the trapezoid text style with the specified name does not exist and
                use_shapetextstyles_if_not_exist is False.
        """
        if self.has(name):
            return self._styles[name].copy()
        if not use_shapetextstyles_if_not_exist:
            raise ValueError('Theme style name "' + name + '" does not exist.')
        return self._shapetextstyles.get(name)

    @error_handler
    def list(self) -> List[str]:
        """List all existing trapezoid text style names.

        Returns:
            List[str]: List of trapezoid text style names.
        """
        return list_(self._styles.keys())

    @error_handler
    def set(self, style: ShapeTextStyle, name: str = "") -> None:
        """Set or update an trapezoid text style with the given name.

        Args:
            style (ShapeTextStyle): The ShapeTextStyle object to cache.
            name (str, optional): Name of the trapezoid text style. Defaults to "".

        Raises:
            ValueError: If the style is invalid or name is not a string.
        """
        style_validator.validate_shapetextstyle("style", style)
        type_validator.validate_str("name", name)
        self._styles[name] = style.copy()
        self._callback_set(name)

    @error_handler
    def delete(self, name: str) -> None:
        """Delete an trapezoid text style by name.

        Args:
            name (str): Name of the trapezoid text style to delete.

        Raises:
            ValueError: If the trapezoid text style with the specified name does not exist.
        """
        if not self.has(name):
            raise ValueError('Theme style name "' + name + '" does not exist.')
        del self._styles[name]
        self._callback_delete(name)

    @error_handler
    def merge(self, style: ShapeTextStyle, targets: Optional[List[str]] = None) -> None:
        """Merge an trapezoid text style into existing trapezoid text styles.

        Args:
            style (ShapeTextStyle): The ShapeTextStyle object to merge.
            targets (Optional[List[str]], optional): List of target trapezoid text style names to merge into.
                If None, merge into all existing trapezoid text styles. Defaults to None.

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


class TriangleTextStyleCache(AbstractStyleCache):
    """Cache for managing triangle text styles.

    This class provides methods to manage and manipulate ShapeTextStyle objects
    specifically tailored for triangle within a cache.
    """

    def __init__(
        self,
        shapetextstyles: ShapeTextStyleCache,
        callback_set: Callable[
            [
                str,
            ],
            None,
        ],
        callback_delete: Callable[
            [
                str,
            ],
            None,
        ],
    ) -> None:
        """Initialize TriangleTextStyleCache.

        Args:
            shapetextstyles (ShapeTextStyleCache): Cache of shape text styles to use as fallback.
            callback_set: Callback function for set operation.
            callback_delete: Callback function for delete operation.
        """
        self._callback_set = callback_set
        self._callback_delete = callback_delete
        self._styles: Dict[str, ShapeTextStyle] = {}
        self._shapetextstyles = shapetextstyles

    @error_handler
    def has(self, name: str) -> bool:
        """Check if an triangle text style exists by name.

        Args:
            name (str): Name of the triangle text style.

        Returns:
            bool: True if the triangle text style exists, False otherwise.
        """
        return name in self._styles

    @error_handler
    def get(self, name: str = "", use_shapetextstyles_if_not_exist: bool = True) -> ShapeTextStyle:
        """Retrieve an triangle text style by name.

        Args:
            name (str, optional): Name of the triangle text style to retrieve. Defaults to "".
            use_shapetextstyles_if_not_exist (bool, optional): Whether to fallback to ShapeTextStyleCache if
                the style does not exist in _styles. Defaults to True.

        Returns:
            ShapeTextStyle: The retrieved ShapeTextStyle object.

        Raises:
            ValueError: If the triangle text style with the specified name does not exist and
                use_shapetextstyles_if_not_exist is False.
        """
        if self.has(name):
            return self._styles[name].copy()
        if not use_shapetextstyles_if_not_exist:
            raise ValueError('Theme style name "' + name + '" does not exist.')
        return self._shapetextstyles.get(name)

    @error_handler
    def list(self) -> List[str]:
        """List all existing triangle text style names.

        Returns:
            List[str]: List of triangle text style names.
        """
        return list_(self._styles.keys())

    @error_handler
    def set(self, style: ShapeTextStyle, name: str = "") -> None:
        """Set or update an triangle text style with the given name.

        Args:
            style (ShapeTextStyle): The ShapeTextStyle object to cache.
            name (str, optional): Name of the triangle text style. Defaults to "".

        Raises:
            ValueError: If the style is invalid or name is not a string.
        """
        style_validator.validate_shapetextstyle("style", style)
        type_validator.validate_str("name", name)
        self._styles[name] = style.copy()
        self._callback_set(name)

    @error_handler
    def delete(self, name: str) -> None:
        """Delete an triangle text style by name.

        Args:
            name (str): Name of the triangle text style to delete.

        Raises:
            ValueError: If the triangle text style with the specified name does not exist.
        """
        if not self.has(name):
            raise ValueError('Theme style name "' + name + '" does not exist.')
        del self._styles[name]
        self._callback_delete(name)

    @error_handler
    def merge(self, style: ShapeTextStyle, targets: Optional[List[str]] = None) -> None:
        """Merge an triangle text style into existing triangle text styles.

        Args:
            style (ShapeTextStyle): The ShapeTextStyle object to merge.
            targets (Optional[List[str]], optional): List of target triangle text style names to merge into.
                If None, merge into all existing triangle text styles. Defaults to None.

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


class BubblespeechTextStyleCache(AbstractStyleCache):
    """Cache for managing bubble speech text styles.

    This class provides methods to manage and manipulate ShapeTextStyle objects
    specifically tailored for bubble speech within a cache.
    """

    def __init__(
        self,
        shapetextstyles: ShapeTextStyleCache,
        callback_set: Callable[
            [
                str,
            ],
            None,
        ],
        callback_delete: Callable[
            [
                str,
            ],
            None,
        ],
    ) -> None:
        """Initialize BubblespeechTextStyleCache.

        Args:
            shapetextstyles (ShapeTextStyleCache): Cache of shape text styles to use as fallback.
            callback_set: Callback function for set operation.
            callback_delete: Callback function for delete operation.
        """
        self._callback_set = callback_set
        self._callback_delete = callback_delete
        self._styles: Dict[str, ShapeTextStyle] = {}
        self._shapetextstyles = shapetextstyles

    @error_handler
    def has(self, name: str) -> bool:
        """Check if an bubble speech text style exists by name.

        Args:
            name (str): Name of the bubble speech text style.

        Returns:
            bool: True if the bubble speech text style exists, False otherwise.
        """
        return name in self._styles

    @error_handler
    def get(self, name: str = "", use_shapetextstyles_if_not_exist: bool = True) -> ShapeTextStyle:
        """Retrieve an bubble speech text style by name.

        Args:
            name (str, optional): Name of the bubble speech text style to retrieve. Defaults to "".
            use_shapetextstyles_if_not_exist (bool, optional): Whether to fallback to ShapeTextStyleCache if
                the style does not exist in _styles. Defaults to True.

        Returns:
            ShapeTextStyle: The retrieved ShapeTextStyle object.

        Raises:
            ValueError: If the bubble speech text style with the specified name does not exist and
                use_shapetextstyles_if_not_exist is False.
        """
        if self.has(name):
            return self._styles[name].copy()
        if not use_shapetextstyles_if_not_exist:
            raise ValueError('Theme style name "' + name + '" does not exist.')
        return self._shapetextstyles.get(name)

    @error_handler
    def list(self) -> List[str]:
        """List all existing bubble speech text style names.

        Returns:
            List[str]: List of bubble speech text style names.
        """
        return list_(self._styles.keys())

    @error_handler
    def set(self, style: ShapeTextStyle, name: str = "") -> None:
        """Set or update an bubble speech text style with the given name.

        Args:
            style (ShapeTextStyle): The ShapeTextStyle object to cache.
            name (str, optional): Name of the bubble speech text style. Defaults to "".

        Raises:
            ValueError: If the style is invalid or name is not a string.
        """
        style_validator.validate_shapetextstyle("style", style)
        type_validator.validate_str("name", name)
        self._styles[name] = style.copy()
        self._callback_set(name)

    @error_handler
    def delete(self, name: str) -> None:
        """Delete an bubble speech text style by name.

        Args:
            name (str): Name of the bubble speech text style to delete.

        Raises:
            ValueError: If the bubble speech text style with the specified name does not exist.
        """
        if not self.has(name):
            raise ValueError('Theme style name "' + name + '" does not exist.')
        del self._styles[name]
        self._callback_delete(name)

    @error_handler
    def merge(self, style: ShapeTextStyle, targets: Optional[List[str]] = None) -> None:
        """Merge an bubble speech text style into existing bubble speech text styles.

        Args:
            style (ShapeTextStyle): The ShapeTextStyle object to merge.
            targets (Optional[List[str]], optional): List of target bubble speech text style names to merge into.
                If None, merge into all existing bubble speech text styles. Defaults to None.

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
