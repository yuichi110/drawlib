import math

from drawlib.apis import *


def bezier_arc_approximation(x, y, r, a1, a2):
    if abs(a1 - a2) > 180:
        a1_5 = int((a1 + a2) / 2)
        p1, p2, p3, p4 = _bezier_arc_approximation(x, y, r, a1, a1_5)
        _, p6, p7, p8 = _bezier_arc_approximation(x, y, r, a1_5, a2)

        return (p1, [(p2, p3, p4), (p6, p7, p8)])

    p1, p2, p3, p4 = _bezier_arc_approximation(x, y, r, a1, a2)
    return (p1, [(p2, p3, p4)])


def _bezier_arc_approximation(x, y, r, a1, a2):
    # Convert angles from degrees to radians
    a1 = math.radians(a1)
    a2 = math.radians(a2)

    # Calculate the start and end points of the arc
    start_point = (x + r * math.cos(a1), y + r * math.sin(a1))
    end_point = (x + r * math.cos(a2), y + r * math.sin(a2))

    phi = a2 - a1
    alpha = (4 / 3) * math.tan(phi / 4)

    control_point1 = (start_point[0] - alpha * r * math.sin(a1), start_point[1] + alpha * r * math.cos(a1))
    control_point2 = (end_point[0] + alpha * r * math.sin(a2), end_point[1] - alpha * r * math.cos(a2))

    return start_point, control_point1, control_point2, end_point


# Example usage


def test():
    x, y = (50, 50)  # Center of the circle
    r = 20  # Radius
    a1, a2 = 270, 0  # Angles in degrees

    start_point, path_points = bezier_arc_approximation(x, y, r, a1, a2)

    circle((x, y), radius=20, style="dashed")

    lines_bezier(start_point, path_points, arrowhead="->", style="red_bold")
    save()
