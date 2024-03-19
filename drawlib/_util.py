from typing import Optional
import math
import warnings


def get_angle(x1: float, y1: float, x2: float, y2: float) -> float:
    dx = x2 - x1
    dy = y2 - y1
    angle_rad = math.atan2(dy, dx)
    angle_deg = math.degrees(angle_rad)
    return (angle_deg + 360) % 360


def warning_suppress(module: Optional[str] = None):
    if module is None:
        warnings.filterwarnings("ignore")
    else:
        warnings.filterwarnings("ignore", module=module)
