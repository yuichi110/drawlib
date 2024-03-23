"""write docstring later"""

import inspect
from typing import Optional
import warnings

from drawlib._util import error_handler


@error_handler
def get_function_name():
    """write docstring later"""

    return inspect.stack()[1][3]


@error_handler
def warning_suppress(module: Optional[str] = None):
    """write docstring later"""

    if module is None:
        warnings.filterwarnings("ignore")
    else:
        warnings.filterwarnings("ignore", module=module)
