# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Font type definitions for drawlib."""

import os
from enum import Enum

from pydantic import BaseModel, ConfigDict, InstanceOf, field_validator


class FontBase(str, Enum):
    """Base class of all font classes."""


class FontFile(BaseModel):
    """A class representing a font file"""

    model_config = ConfigDict(validate_assignment=True)

    file: str

    def __init__(self, file: str) -> None:
        """Initialize the font file."""
        super().__init__(file=file)

    @field_validator("file")
    @classmethod
    def validate_file(cls, value: str) -> str:
        """Validate the font file path.

        Validates that the provided path exists and is a valid file path. If not,
        raises an appropriate exception.

        Args:
            value (str): The path to the font file.

        Returns:
            str: The absolute path to the font file.

        Raises:
            FileNotFoundError: If the file does not exist at the specified path.
        """
        from drawlib.v0_2.private.util import get_script_relative_path

        path = get_script_relative_path(value)
        if not os.path.exists(path):
            raise FileNotFoundError(f'font file "{path}" does not exist.')
        return path


TypeFont = InstanceOf[FontBase] | InstanceOf[FontFile]
