# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Base type definitions for drawlib."""

from typing import Any, NoReturn


class StaticContainer:
    """Base class to prevent instantiation for static constant containers.

    Inherit from this class to create a namespace that only holds constants
    and static data, ensuring it cannot be initialized as an object.
    """

    def __new__(cls) -> NoReturn:
        """Raise TypeError upon any attempt to instantiate the class.

        Returns:
            NoReturn: This method never returns normally.

        Raises:
            TypeError: Always raised to prevent instantiation.
        """
        raise TypeError(
            f"'{cls.__name__}' is a static container (namespace) and cannot be instantiated. "
            f"Access its attributes directly, e.g., {cls.__name__}.AttributeName"
        )


def validate_literal(v: Any, supported: set[Any], name: str) -> Any:  # noqa: ANN401
    """Helper to validate literal values with a custom error message."""
    if v not in supported:
        raise ValueError(f'Arg/Attr "{name}" must be one of {sorted(list(supported))}. But "{v}" is given.')
    return v
