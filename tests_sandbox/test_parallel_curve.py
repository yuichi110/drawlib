import math
from typing import List, Literal, Optional, Tuple, Union

from drawlib.apis import *


class ArrowsHelper:
    def __init__(self, xys: List[Tuple[float, float]], r: float, num_points=100):
        def get_mid_points(
            a: Tuple[float, float],
            b: Tuple[float, float],
        ) -> Tuple[Tuple[float, float], Tuple[float, float]]:
            ab = [b[0] - a[0], b[1] - a[1]]
            ab_distance = math.sqrt(ab[0] ** 2 + ab[1] ** 2)
            ab_unit = [ab[0] / ab_distance, ab[1] / ab_distance]
            c = (a[0] + r * ab_unit[0], a[1] + r * ab_unit[1])
            d = (b[0] - r * ab_unit[0], b[1] - r * ab_unit[1])
            return c, d

        def bernstein_poly(i, n, t):
            return math.comb(n, i) * (t**i) * ((1 - t) ** (n - i))

        def get_points(
            bezier_points: List[Tuple[float, float]],
        ) -> List[Tuple[float, float]]:
            n = len(bezier_points) - 1
            curve = []
            for t in [i / (num_points - 1) for i in range(num_points)]:
                x = sum(bernstein_poly(i, n, t) * bezier_points[i][0] for i in range(n + 1))
                y = sum(bernstein_poly(i, n, t) * bezier_points[i][1] for i in range(n + 1))
                curve.append((x, y))
            return curve

        points = []
        bezier_start: Tuple[float, float] = (0, 0)
        last_i = len(xys) - 2
        # last_xy = (0, 0)
        for i in range(len(xys)):
            # first straight line
            if i == 0:
                _, bezier_start = get_mid_points(xys[0], xys[1])
                points.append(xys[0])
                continue

            # last straight line
            if i == last_i:
                p1, _ = get_mid_points(xys[i], xys[i + 1])
                bezier_points = [bezier_start, xys[i], p1]
                points.extend(get_points(bezier_points))
                points.append(xys[i + 1])
                break

            p1, p2 = get_mid_points(xys[i], xys[i + 1])
            bezier_points = [bezier_start, xys[i], p1]
            points.extend(get_points(bezier_points))
            bezier_start = p2

        self._original_curve_points = points

    def get_parallel_curve_points(self, distance: float):
        def get_distance(p1, p2):
            return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

        parallel_curve_points = []
        for i in range(1, len(self._original_curve_points)):
            p0, p1 = self._original_curve_points[i - 1], self._original_curve_points[i]
            dx, dy = p1[0] - p0[0], p1[1] - p0[1]
            length = get_distance(p0, p1)
            nx, ny = -dy / length, dx / length
            px0, py0 = p0[0] + distance * nx, p0[1] + distance * ny
            px1, py1 = p1[0] + distance * nx, p1[1] + distance * ny
            parallel_curve_points.append((px0, py0))
            if i == len(self._original_curve_points) - 1:
                parallel_curve_points.append((px1, py1))

        return parallel_curve_points


# Example control points for a cubic Bezier curve


def test():
    points: List[Tuple[float, float]] = [(10, 10), (20, 20), (30, 80), (80, 80), (60, 20)]
    ah = ArrowsHelper(points, 10, 100)
    for p in points:
        circle(p, radius=0.5, style="black_solid")

    lines(ah._original_curve_points, style="black_dashed")

    lines(ah.get_parallel_curve_points(1), style="red")
    lines(ah.get_parallel_curve_points(-1), style="red")
    save()
