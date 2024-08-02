import math

from drawlib.apis import *


def bezier_arc_approximation(x, y, width, height, a1, a2):
    if abs(a1 - a2) > 180:
        a1_5 = int((a1 + a2) / 2)
        p1, p2, p3, p4 = _bezier_arc_approximation(x, y, width, height, a1, a1_5)
        _, p6, p7, p8 = _bezier_arc_approximation(x, y, width, height, a1_5, a2)

        return (p1, [(p2, p3, p4), (p6, p7, p8)])

    p1, p2, p3, p4 = _bezier_arc_approximation(x, y, width, height, a1, a2)
    return (p1, [(p2, p3, p4)])


def _bezier_arc_approximation(x, y, width, height, start_angle, end_angle):
    # Convert angles from degrees to radians
    start_angle = math.radians(start_angle)
    end_angle = math.radians(end_angle)

    # Calculate the points on the ellipse at the start and end angles
    start_point = (x + width / 2 * math.cos(start_angle), y + height / 2 * math.sin(start_angle))
    end_point = (x + width / 2 * math.cos(end_angle), y + height / 2 * math.sin(end_angle))

    # Calculate the control points for the Bezier curve
    t = (4 / 3) * math.tan((end_angle - start_angle) / 4)
    control_point1 = (
        start_point[0] - t * width / 2 * math.sin(start_angle),
        start_point[1] + t * height / 2 * math.cos(start_angle),
    )
    control_point2 = (
        end_point[0] + t * width / 2 * math.sin(end_angle),
        end_point[1] - t * height / 2 * math.cos(end_angle),
    )

    return start_point, control_point1, control_point2, end_point


# Example usage


def test():
    x, y = (50, 50)  # Center of the circle
    width = 40
    height = 20
    a1, a2 = 270, 90  # Angles in degrees

    ellipse((x, y), width=width, height=height, style="dashed")
    start_point, path_points = bezier_arc_approximation(x, y, width, height, a1, a2)
    circle(start_point, radius=1, style="black")
    circle(path_points[0][0], radius=1, style="blue")
    circle(path_points[0][1], radius=1, style="red")
    circle(path_points[0][2], radius=1, style="black")
    # circle((x, y), radius=20, style="dashed")

    lines_bezier(start_point, path_points, arrowhead="->", style="red_bold")
    save()
