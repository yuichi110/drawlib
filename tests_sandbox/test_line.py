import math
from typing import List, Literal, Optional, Tuple, Union

from drawlib.apis import *

"""
def test():
    points = [(10, 10), (20, 20), (30, 80), (80, 80), (60, 20)]
    parallel_points1 = ArrowsHelper.get_parallel_lines_xys(points, 5)
    parallel_points2 = ArrowsHelper.get_parallel_lines_xys(points, -5)

    lines(points)
    lines(parallel_points1, style="blue")
    lines(parallel_points2, style="red")

    circle(
        xy=ArrowsHelper.get_point_on_line(parallel_points1[0], parallel_points1[1], 5),
        radius=1,
        style="black_flat",
    )

    
    
    lines(points)

    ls = []
    for i in range(len(points) - 1):
        xy1, xy2 = parallel_line_coordinates(points[i], points[i + 1], 5)
        line(xy1, xy2, style="blue")
        ls.append((xy1, xy2))

        xy3, xy4 = parallel_line_coordinates(points[i], points[i + 1], -5)
        line(xy3, xy4, style="red")

    for i in range(len(ls) - 1):
        xy1, xy2 = ls[i]
        xy3, xy4 = ls[i + 1]
        xy = find_intersection(xy1, xy2, xy3, xy4)
        circle(xy, radius=1, style="black_flat")


    save()
"""


def test():
    xys = [(10, 10), (20, 20), (30, 80), (80, 80), (60, 20)]
    tail_width = 2
    head_length = 3
    head_width = 5
    head = "->"
    r = 5

    parallel_xys1 = ArrowsHelper.get_parallel_lines_xys(xys, tail_width / 2)
    parallel_xys2 = ArrowsHelper.get_parallel_lines_xys(xys, tail_width / 2 * -1)

    arrowhead_start_tail_xy1 = ArrowsHelper.get_point_on_line(parallel_xys1[0], parallel_xys1[1], head_length)
    arrowhead_start_tail_xy2 = ArrowsHelper.get_point_on_line(parallel_xys2[0], parallel_xys2[1], head_length)
    arrowhead_end_tail_xy1 = ArrowsHelper.get_point_on_line(
        parallel_xys1[len(parallel_xys1) - 1],
        parallel_xys1[len(parallel_xys1) - 2],
        head_length,
    )
    arrowhead_end_tail_xy2 = ArrowsHelper.get_point_on_line(
        parallel_xys2[len(parallel_xys1) - 1],
        parallel_xys2[len(parallel_xys1) - 2],
        head_length,
    )

    xy1, xy2 = ArrowsHelper.get_parallel_line_xys(xys[0], xys[1], head_width / 2)
    arrowhead_start_head_xy1 = ArrowsHelper.get_point_on_line(xy1, xy2, head_length)
    xy1, xy2 = ArrowsHelper.get_parallel_line_xys(xys[0], xys[1], head_width / 2 * -1)
    arrowhead_start_head_xy2 = ArrowsHelper.get_point_on_line(xy1, xy2, head_length)
    xy1, xy2 = ArrowsHelper.get_parallel_line_xys(
        xys[len(xys) - 1], xys[len(xys) - 2], head_width / 2 * -1
    )  # since poinrts are reversed, having * -1 here
    arrowhead_end_head_xy1 = ArrowsHelper.get_point_on_line(xy1, xy2, head_length)
    xy1, xy2 = ArrowsHelper.get_parallel_line_xys(xys[len(xys) - 1], xys[len(xys) - 2], head_width / 2)
    arrowhead_end_head_xy2 = ArrowsHelper.get_point_on_line(xy1, xy2, head_length)

    points1: list[tuple[float, float]] = []
    if head == "->":
        points1.append(parallel_xys1[0])
    else:
        points1.append(arrowhead_start_tail_xy1)
    points1.extend(parallel_xys1[1:-1])
    if head == "<-":
        points1.append(parallel_xys1[len(parallel_xys1) - 1])
    else:
        points1.append(arrowhead_end_tail_xy1)

    points2: list[tuple[float, float]] = []
    if head == "<-":
        points2.append(parallel_xys2[len(parallel_xys2) - 1])
    else:
        points2.append(arrowhead_end_tail_xy2)
    temp = parallel_xys2[1:-1]
    temp.reverse()
    points2.extend(temp)
    if head == "->":
        points2.append(parallel_xys2[0])
    else:
        points2.append(arrowhead_start_tail_xy2)

    # apply r here
    if r != 0:
        pass_points1: List[
            Union[
                Tuple[float, float],
                Tuple[Tuple[float, float], Tuple[float, float]],
                Tuple[Tuple[float, float], Tuple[float, float], Tuple[float, float]],
            ]
        ] = ArrowsHelper.get_points_curved(points1, r)
        pass_points2: List[
            Union[
                Tuple[float, float],
                Tuple[Tuple[float, float], Tuple[float, float]],
                Tuple[Tuple[float, float], Tuple[float, float], Tuple[float, float]],
            ]
        ] = ArrowsHelper.get_points_curved(points2, r)
    else:
        pass_points1 = points1
        pass_points2 = points2

    if head != "->":
        pass_points1.insert(0, xys[0])
        pass_points1.insert(1, arrowhead_start_head_xy1)
    if head != "<-":
        pass_points1.append(arrowhead_end_head_xy1)
        pass_points1.append(xys[len(xys) - 1])

    if head != "<-":
        pass_points2.insert(0, arrowhead_end_head_xy2)
    if head != "->":
        pass_points2.append(arrowhead_start_head_xy2)

    pass_points1.extend(pass_points2)
    lines_bezier(pass_points1[0], pass_points1[1:])
    save()


class ArrowsHelper:
    @classmethod
    def get_points_curved(
        cls,
        xys: list[tuple[float, float]],
        r: float,
    ):
        def _get_mid_points(
            a: Tuple[float, float],
            b: Tuple[float, float],
            r: float,
        ) -> Tuple[Tuple[float, float], Tuple[float, float]]:
            # Calculate the vector from A to B
            ab = [b[0] - a[0], b[1] - a[1]]

            # Calculate the distance from A to B
            ab_distance = math.sqrt(ab[0] ** 2 + ab[1] ** 2)

            # Normalize the vector AB to get the unit vector
            ab_unit = [ab[0] / ab_distance, ab[1] / ab_distance]

            # Calculate point C: A + X * unit vector AB
            c = (a[0] + r * ab_unit[0], a[1] + r * ab_unit[1])

            # Calculate point D: B - X * unit vector AB
            d = (b[0] - r * ab_unit[0], b[1] - r * ab_unit[1])

            return c, d

        path_points: List[
            Union[
                Tuple[float, float],
                Tuple[Tuple[float, float], Tuple[float, float]],
                Tuple[Tuple[float, float], Tuple[float, float], Tuple[float, float]],
            ]
        ] = []

        last_i = len(xys) - 2
        # last_xy = (0, 0)
        for i, xy in enumerate(xys):
            if i == 0:
                _, p = _get_mid_points(xy, xys[i + 1], r)
                path_points.append(p)
                continue

            if i == last_i:
                p, _ = _get_mid_points(xy, xys[i + 1], r)
                path_points.append((xy, p))
                path_points.append(xys[i + 1])
                break

            p1, p2 = _get_mid_points(xy, xys[i + 1], r)
            path_points.append((xy, p1))
            path_points.append(p2)

        path_points.insert(0, xys[0])
        return path_points

    @classmethod
    def get_point_on_line(
        cls,
        xy1: tuple[float, float],
        xy2: tuple[float, float],
        distance: float,
    ) -> tuple[float, float]:
        x1, y1 = xy1
        x2, y2 = xy2

        v_length = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        u_x = (x2 - x1) / v_length
        u_y = (y2 - y1) / v_length

        x = x1 + distance * u_x
        y = y1 + distance * u_y

        return (x, y)

    @classmethod
    def get_parallel_lines_xys(
        cls,
        xys: list[tuple[float, float]],
        distance: float,
    ) -> list[tuple[float, float]]:
        parallel_lines: list[tuple[tuple[float, float], tuple[float, float]]] = []
        for i in range(len(xys) - 1):
            xy1, xy2 = cls.get_parallel_line_xys(xys[i], xys[i + 1], distance)
            parallel_lines.append((xy1, xy2))

        points: list[tuple[float, float]] = []
        for i in range(len(parallel_lines) - 1):
            xy1, xy2 = parallel_lines[i]
            xy3, xy4 = parallel_lines[i + 1]
            xy = cls.find_lines_intersection(xy1, xy2, xy3, xy4)
            points.append(xy)

        first_point = parallel_lines[0][0]
        last_point = parallel_lines[len(parallel_lines) - 1][1]

        points.insert(0, first_point)
        points.append(last_point)

        return points

    @classmethod
    def get_parallel_line_xys(
        cls,
        xy1: tuple[float, float],
        xy2: tuple[float, float],
        distance: float,
    ):
        x1, y1 = xy1
        x2, y2 = xy2

        # calc vector
        vx = x2 - x1
        vy = y2 - y1
        length = math.sqrt(vx**2 + vy**2)
        dx = -vy / length * distance
        dy = vx / length * distance

        # add vector
        x1_prime = x1 + dx
        y1_prime = y1 + dy
        x2_prime = x2 + dx
        y2_prime = y2 + dy

        return (x1_prime, y1_prime), (x2_prime, y2_prime)

    @classmethod
    def find_lines_intersection(
        cls,
        xy1: tuple[float, float],
        xy2: tuple[float, float],
        xy3: tuple[float, float],
        xy4: tuple[float, float],
    ):
        x1, y1 = xy1
        x2, y2 = xy2
        x3, y3 = xy3
        x4, y4 = xy4

        m1 = (y2 - y1) / (x2 - x1)
        b1 = y1 - m1 * x1
        m2 = (y4 - y3) / (x4 - x3)
        b2 = y3 - m2 * x3

        x = (b2 - b1) / (m1 - m2)
        y = m1 * x + b1

        return (x, y)
