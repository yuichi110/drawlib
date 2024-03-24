"""write docstring later"""

import inspect
from typing import Optional
import warnings


def set_logging_quiet(): ...


def set_logging_normal(): ...


def set_logging_verbose(): ...


def set_logging_developer(): ...


def is_logging_developer(): ...


def warning_suppress(module: Optional[str] = None):
    """write docstring later"""

    if module is None:
        warnings.filterwarnings("ignore")
    else:
        warnings.filterwarnings("ignore", module=module)
